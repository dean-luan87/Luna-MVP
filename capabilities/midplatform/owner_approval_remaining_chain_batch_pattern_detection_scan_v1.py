# -*- coding: utf-8 -*-
"""Static scan helpers for owner approval remaining chain batch pattern detection."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List

from capabilities.midplatform.canonical_go_checkpoint_rebuild_scan_v1 import runner_script_to_verify_script
from capabilities.midplatform.owner_approval_remaining_chain_batch_pattern_detection_items_v1 import (
    GAP_CLASSES,
    ROLE_TO_FAMILY,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
TOOLS = REPO_ROOT / "tools" / "evaluation" / "midplatform"

DOWNSTREAM_KEYWORDS = (
    "issuance_dryrun",
    "issuance_post_dryrun",
    "post_dryrun_review",
    "closure",
    "record_",
    "governance_gate",
    "functional_slice",
    "module_governance",
    "module_handoff",
    "broader_midplatform",
)

GROUP_G_STAGES = {
    "governance_gate_integrated_implementation",
    "module_governance_closure",
    "module_handoff",
    "broader_midplatform_closure_roadmap",
}

GROUP_M_STAGES = {
    "model_workflow_protocol_reuse_review",
    "model_adapter_priority_sequence_planning",
    "slam_spatial_mapping_model_smoke_io_inspection",
    "slam_spatial_mapping_adapter_skeleton",
    "slam_spatial_mapping_task_collaboration_planning",
    "slam_spatial_mapping_task_collaboration_revalidation",
}


def read_json(path: Path) -> Dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
    except (json.JSONDecodeError, OSError):
        return {}


def stage_family(stage_role: str, stage_key: str) -> str:
    if "record_approval_closure" in stage_key:
        return "closure"
    return ROLE_TO_FAMILY.get(stage_role, "unknown")


def analyze_source(text: str) -> Dict[str, Any]:
    requires_all_linked = bool(
        re.search(r'all\(\s*node\.get\("linked"\)', text)
        or re.search(r"all\(\s*node\.get\('linked'\)", text)
        or re.search(r"all\(\s*node\.get\(\"linked\"\)", text)
    )
    downstream_go_refs = sorted(
        set(re.findall(r"prior_[a-z0-9_]+_(?:dryrun|post_review|issuance|closure)[a-z0-9_]*_go", text))
    )
    downstream_go_blockers = [
        ref
        for ref in downstream_go_refs
        if any(kw in ref for kw in DOWNSTREAM_KEYWORDS)
        and "planning_go" not in ref
    ]
    return {
        "requires_all_linked": requires_all_linked,
        "downstream_go_refs": downstream_go_refs,
        "downstream_go_blockers_in_source": downstream_go_blockers,
        "decision_drift_pattern": (
            "final_decision = FINAL_DECISION_GO" in text
            and "all(go_condition_values.values())" in text
        ),
        "pass_flag_pattern": bool(
            re.search(r"(planning_pass|dryrun_pass|post_dryrun_review_pass|review_pass)\s*=", text)
        ),
        "evidence_chain_field_present": "evidence_chain_ok" in text or "evidence_chain_complete" in text,
        "verifier_linked_check_count": len(re.findall(r'evidence\.linked\.|"evidence\.linked\.', text)),
        "downstream_readiness_gaps_field": "downstream_readiness_gaps" in text,
        "relaxed_traceability_pattern": "dryrun_ref_linked" in text or "review_node_linked" in text,
    }


def analyze_verifier_source(text: str) -> Dict[str, Any]:
    return {
        "naive_replace_run_verify": bool(re.search(r'\.replace\("run_",\s*"verify_"\)', text)),
        "verifier_linked_check_count": len(re.findall(r"evidence\.linked\.", text)),
        "verifier_declared_check_count": len(re.findall(r"evidence\.declared\.", text)),
    }


def artifact_signals(output_dir: str) -> Dict[str, Any]:
    root = Path(output_dir)
    summary = read_json(root / "summary.json")
    verifier = read_json(root / "verifier_report.json")
    final_decision = str(summary.get("final_decision") or "")
    ready = "READY" in final_decision.upper() and "BLOCKED" not in final_decision.upper()
    pass_flags = [
        summary.get("planning_pass"),
        summary.get("issuance_planning_pass"),
        summary.get("dryrun_pass"),
        summary.get("issuance_dryrun_pass"),
        summary.get("post_dryrun_review_pass"),
        summary.get("review_pass"),
    ]
    any_pass_false = any(v is False for v in pass_flags if v is not None)
    return {
        "summary_exists": (root / "summary.json").is_file(),
        "verifier_report_exists": (root / "verifier_report.json").is_file(),
        "verifier_status": verifier.get("verifier"),
        "final_decision": final_decision or None,
        "ready_final_decision": ready,
        "pass_flag_false": any_pass_false,
        "blocker_count": summary.get("blocker_count"),
        "issues_empty": (summary.get("issues") or []) == [],
        "verifier_hold": verifier.get("verifier") == "HOLD",
        "verifier_final_decision": verifier.get("final_decision"),
        "failed_checks": verifier.get("failed_checks"),
        "decision_drift_observed": ready and (any_pass_false or verifier.get("verifier") == "HOLD"),
        "schema_drift_observed": (
            verifier.get("final_decision") in ("HOLD", "HOLD_FOR_ISSUE_REVIEW")
            and ready
            and summary.get("final_decision")
        ),
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
) -> Dict[str, Any]:
    gaps: Dict[str, bool] = {g: False for g in GAP_CLASSES}
    evidence: List[str] = []

    if source.get("requires_all_linked") and not source.get("relaxed_traceability_pattern"):
        gaps["evidence_traceability_gap"] = True
        evidence.append("capability_requires_all_nodes_linked")

    if source.get("downstream_go_blockers_in_source"):
        gaps["downstream_expectation_gap"] = True
        evidence.append("downstream_go_refs_in_capability")

    if stage_family_name in ("planning", "closure") and source.get("requires_all_linked"):
        gaps["downstream_expectation_gap"] = True
        evidence.append("planning_requires_full_chain_linked")

    if stage_family_name == "dryrun" and source.get("evidence_chain_field_present"):
        gaps["evidence_traceability_gap"] = True
        evidence.append("dryrun_evidence_chain_field_present")

    if source.get("decision_drift_pattern"):
        gaps["runner_verifier_decision_drift"] = True
        evidence.append("pass_flag_uses_all_go_conditions_but_final_decision_else_go")

    if artifacts.get("decision_drift_observed"):
        gaps["runner_verifier_decision_drift"] = True
        evidence.append("checkpoint_ready_but_pass_false_or_verifier_hold")

    if artifacts.get("schema_drift_observed"):
        gaps["schema_output_gap"] = True
        evidence.append("verifier_final_decision_hold_vs_summary_ready")

    if (
        verifier_src.get("verifier_linked_check_count", 0) > 0
        and verifier_src.get("verifier_declared_check_count", 0) == 0
        and source.get("requires_all_linked")
    ):
        gaps["evidence_traceability_gap"] = True
        evidence.append("verifier_requires_linked_without_declared_fallback")

    verify_script = runner_script_to_verify_script(runner_script)
    if "dryrun" in runner_script and runner_script.replace("run_", "verify_") != verify_script:
        gaps["verifier_locator_gap"] = True
        evidence.append("naive_run_to_verify_would_corrupt_dryrun_path")

    if checkpoint.get("checkpoint_status") == "missing_verifier_report":
        gaps["verifier_locator_gap"] = True
        evidence.append("checkpoint_missing_verifier_report")

    if not any(gaps.values()):
        if stage_family_name in ("governance", "handoff", "model_workflow", "model_adapter", "slam_readiness"):
            gaps["genuine_logic_hold"] = True
            evidence.append("no_template_pattern_matched_individual_stage")
        elif checkpoint.get("checkpoint_status") in ("blocked_readable", "hold_readable"):
            gaps["genuine_logic_hold"] = True
            evidence.append("blocked_without_known_template_pattern")

    primary = next((g for g in GAP_CLASSES if gaps[g]), "genuine_logic_hold")
    verify_path = TOOLS / f"{verify_script}.py"
    runner_path = TOOLS / f"{runner_script}.py"

    return {
        "stage_key": stage_key,
        "stage_family": stage_family_name,
        "gap_classification": gaps,
        "primary_gap": primary,
        "secondary_gaps": [g for g in GAP_CLASSES if gaps[g] and g != primary],
        "evidence": evidence,
        "safe_template_repair": (
            stage_family_name in ("planning", "dryrun", "post_dryrun_review", "closure")
            and primary in (
                "downstream_expectation_gap",
                "runner_verifier_decision_drift",
                "evidence_traceability_gap",
                "schema_output_gap",
                "verifier_locator_gap",
            )
            and stage_key not in GROUP_G_STAGES
            and stage_key not in GROUP_M_STAGES
        ),
        "requires_individual_repair": (
            stage_key in GROUP_G_STAGES
            or stage_key in GROUP_M_STAGES
            or primary == "genuine_logic_hold"
        ),
        "verifier_path": str(verify_path),
        "verifier_exists": verify_path.is_file(),
        "runner_exists": runner_path.is_file(),
    }


def repair_direction(stage_family_name: str, primary: str) -> List[str]:
    if stage_family_name in ("planning", "closure"):
        return [
            "downstream linked -> declared",
            "downstream GO blocker -> downstream_readiness_gaps",
            "align final_decision with pass flag",
            "planning node linked + paths declared",
        ]
    if stage_family_name == "dryrun":
        return [
            "direct planning ref linked",
            "current dryrun node linked",
            "evidence paths declared",
            "downstream review readiness declared",
            "no execution leakage",
        ]
    if stage_family_name == "post_dryrun_review":
        return [
            "dryrun accepted",
            "dryrun ref linked",
            "review node linked",
            "traceability declared",
            "final_decision/pass/blocker aligned",
        ]
    if primary == "verifier_locator_gap":
        return ["use runner_script_to_verify_script", "regenerate verifier_report"]
    if primary == "genuine_logic_hold":
        return ["individual repair only — do not apply P/D/R template"]
    return ["review capability and verifier manually"]
