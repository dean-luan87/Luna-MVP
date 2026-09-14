# -*- coding: utf-8 -*-
"""Model-SLAM readiness chain batch detection — scan helpers v1."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List

from capabilities.midplatform.canonical_go_checkpoint_rebuild_scan_v1 import runner_script_to_verify_script
from capabilities.midplatform.model_slam_readiness_chain_batch_detection_items_v1 import (
    GAP_CLASSES,
    GROUP_M_STAGES,
    ROLE_TO_FAMILY,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
TOOLS = REPO_ROOT / "tools" / "evaluation" / "midplatform"

MODEL_EXEC_PATTERNS = (
    r"torch\.load",
    r"model\.download",
    r"download_weights",
    r"camera\.open",
    r"cv2\.VideoCapture",
    r"WorldModelCandidate",
    r"WorldModelEntry",
    r"WorldEntity",
    r"real_inference",
    r"run_real_model",
)

DOWNSTREAM_PRIOR_PATTERNS = (
    r"prior_[a-z0-9_]+_go",
    r"if not prior_[a-z0-9_]+",
)


def read_json(path: Path) -> Dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
    except (json.JSONDecodeError, OSError):
        return {}


def stage_family(stage_role: str, stage_key: str) -> str:
    if stage_key in GROUP_M_STAGES:
        for sk, fam in (
            ("model_workflow", "model_workflow"),
            ("model_adapter", "model_adapter_priority"),
            ("smoke_io", "slam_smoke_io"),
            ("adapter_skeleton", "slam_adapter_skeleton"),
            ("task_collaboration_planning", "slam_task_collaboration_planning"),
            ("revalidation", "slam_revalidation"),
        ):
            if sk in stage_key:
                return fam
    return ROLE_TO_FAMILY.get(stage_role, "unknown")


def analyze_source(text: str, *, stage_key: str) -> Dict[str, Any]:
    prior_refs = sorted(set(re.findall(r"prior_[a-z0-9_]+_go", text)))
    downstream_blockers = [
        ref
        for ref in prior_refs
        if any(
            kw in ref
            for kw in (
                "adapter",
                "smoke",
                "skeleton",
                "collaboration",
                "revalidation",
                "model_workflow",
                "slam",
            )
        )
    ]
    model_exec_hits = [p for p in MODEL_EXEC_PATTERNS if re.search(p, text)]
    subprocess_run = "subprocess.run" in text and "run_" in text
    return {
        "prior_go_refs": prior_refs,
        "downstream_prior_go_refs": downstream_blockers,
        "model_execution_pattern_hits": model_exec_hits,
        "subprocess_upstream_rerun": subprocess_run,
        "downstream_readiness_gaps_field": "downstream_readiness_gaps" in text,
        "candidate_only_declared": "candidate_only" in text or "no_model_download" in text,
        "no_world_model_declared": "no_world_model" in text or "world_model_candidate_only" in text,
        "requires_all_linked": bool(re.search(r'all\([^)]*\.get\("linked"\)', text)),
    }


def analyze_verifier_source(text: str) -> Dict[str, Any]:
    verify_script_derived = bool(re.search(r'\.replace\("run_",\s*"verify_"\)', text))
    return {
        "naive_replace_run_verify": verify_script_derived,
        "verifier_linked_check_count": len(re.findall(r"\.linked\.", text)),
        "verifier_declared_check_count": len(re.findall(r"\.declared\.", text)),
        "checks_verifier_report_field": "verifier_report" in text,
    }


def artifact_signals(output_dir: str) -> Dict[str, Any]:
    root = Path(output_dir)
    summary = read_json(root / "summary.json")
    verifier = read_json(root / "verifier_report.json")
    final_decision = str(summary.get("final_decision") or "")
    ready = "READY" in final_decision.upper() and "BLOCKED" not in final_decision.upper()
    pass_keys = (
        "review_pass",
        "planning_pass",
        "revalidation_pass",
        "slam_task_collaboration_planning_revalidation_pass",
        "slam_spatial_mapping_smoke_io_inspection_pass",
        "adapter_skeleton_pass",
        "model_adapter_priority_sequence_planning_pass",
        "model_workflow_protocol_reuse_review_pass",
    )
    pass_vals = [summary.get(k) for k in pass_keys if k in summary]
    any_pass_false = any(v is False for v in pass_vals)
    return {
        "summary_exists": (root / "summary.json").is_file(),
        "verifier_report_exists": (root / "verifier_report.json").is_file(),
        "verifier_status": verifier.get("verifier"),
        "final_decision": final_decision or None,
        "ready_final_decision": ready,
        "pass_flag_false": any_pass_false,
        "blocker_count": summary.get("blocker_count"),
        "issues": summary.get("issues") or [],
        "verifier_hold": verifier.get("verifier") == "HOLD",
        "failed_checks": verifier.get("failed_checks"),
        "decision_drift_observed": ready and (any_pass_false or verifier.get("verifier") == "HOLD"),
    }


def classify_gaps(
    *,
    stage_key: str,
    stage_family_name: str,
    source: Dict[str, Any],
    verifier_src: Dict[str, Any],
    artifacts: Dict[str, Any],
    checkpoint: Dict[str, Any],
    runner_script: str,
    canonical_upstream_refs: List[str],
) -> Dict[str, Any]:
    gaps: Dict[str, bool] = {g: False for g in GAP_CLASSES}
    evidence: List[str] = []

    verify_script = runner_script_to_verify_script(runner_script)
    verify_path = TOOLS / f"{verify_script}.py"
    runner_path = TOOLS / f"{runner_script}.py"

    if checkpoint.get("checkpoint_status") == "missing_verifier_report":
        gaps["verifier_locator_gap"] = True
        evidence.append("checkpoint_missing_verifier_report")
    if artifacts.get("summary_exists") and not artifacts.get("verifier_report_exists"):
        gaps["verifier_locator_gap"] = True
        evidence.append("summary_without_verifier_report")
    if verify_script != runner_script.replace("run_", "verify_") and "dryrun" not in runner_script:
        if not verify_path.is_file():
            gaps["verifier_locator_gap"] = True
            evidence.append("runner_script_to_verify_script_mismatch")

    if artifacts.get("decision_drift_observed"):
        gaps["schema_output_gap"] = True
        evidence.append("decision_drift_summary_vs_verifier")

    if source.get("downstream_prior_go_refs") and not source.get("downstream_readiness_gaps_field"):
        gaps["downstream_expectation_gap"] = True
        evidence.append("prior_go_refs_without_downstream_readiness_gaps")

    if stage_key == "model_workflow_protocol_reuse_review":
        gaps["downstream_expectation_gap"] = True
        evidence.append("canonical_upstream_broader_roadmap_but_capability_reads_exec_path_hardening")

    if source.get("requires_all_linked"):
        gaps["evidence_traceability_gap"] = True
        evidence.append("requires_all_linked")

    if source.get("model_execution_pattern_hits"):
        if stage_family_name in ("slam_smoke_io", "slam_revalidation"):
            gaps["model_execution_leakage"] = len(source["model_execution_pattern_hits"]) > 2
            if gaps["model_execution_leakage"]:
                evidence.append("model_execution_patterns_in_source")
        else:
            gaps["model_execution_leakage"] = bool(
                any(h in ("torch.load", "camera.open", "cv2.VideoCapture") for h in source["model_execution_pattern_hits"])
            )

    if source.get("subprocess_upstream_rerun") and stage_key == "slam_spatial_mapping_task_collaboration_revalidation":
        gaps["schema_output_gap"] = True
        evidence.append("revalidation_reruns_upstream_without_verifier_report_emit")

    if checkpoint.get("checkpoint_status") in ("blocked_readable", "hold_readable") and not any(gaps.values()):
        if stage_key != "slam_spatial_mapping_task_collaboration_revalidation":
            gaps["downstream_expectation_gap"] = True
            evidence.append("blocked_by_upstream_chain_cascade")
        else:
            gaps["genuine_logic_hold"] = True
            evidence.append("p0_visibility_or_bootstrap_not_ready")

    primary = next((g for g in GAP_CLASSES if gaps[g]), "genuine_logic_hold")
    if primary == "genuine_logic_hold" and gaps.get("downstream_expectation_gap"):
        primary = "downstream_expectation_gap"

    safe_readiness_repair = (
        primary
        in (
            "verifier_locator_gap",
            "schema_output_gap",
            "downstream_expectation_gap",
            "evidence_traceability_gap",
        )
        and not gaps.get("model_execution_leakage")
        and primary != "genuine_logic_hold"
    )

    return {
        "stage_key": stage_key,
        "stage_family": stage_family_name,
        "gap_classification": gaps,
        "primary_gap": primary,
        "secondary_gaps": [g for g in GAP_CLASSES if gaps[g] and g != primary],
        "evidence": evidence,
        "safe_readiness_repair": safe_readiness_repair,
        "requires_individual_repair": primary in ("genuine_logic_hold", "model_execution_leakage"),
        "verifier_path": str(verify_path),
        "verifier_exists": verify_path.is_file(),
        "runner_exists": runner_path.is_file(),
        "runner_script": runner_script,
        "verify_script": verify_script,
        "canonical_upstream_refs": canonical_upstream_refs,
    }


def repair_direction(stage_family_name: str, primary: str) -> List[str]:
    if primary == "downstream_expectation_gap":
        return [
            "align direct upstream with canonical checkpoint refs",
            "move downstream stage GO requirements to downstream_readiness_gaps",
            "declare model readiness refs without requiring downstream GO",
        ]
    if primary == "verifier_locator_gap":
        return ["use runner_script_to_verify_script", "emit verifier_report from runner or scan-only verify"]
    if primary == "schema_output_gap":
        return ["align summary/verifier_report fields", "align pass flag and final_decision"]
    if primary == "evidence_traceability_gap":
        return ["direct upstream linked + current node linked + paths declared"]
    if primary == "model_execution_leakage":
        return ["individual repair — remove model/camera/sensor execution paths"]
    return ["individual repair — genuine logic hold"]
