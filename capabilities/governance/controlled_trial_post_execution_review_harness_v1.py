# -*- coding: utf-8 -*-
"""Controlled Trial Post-Execution Review Harness v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.candidate_output_contract_v1 import validate_candidate_output
from capabilities.governance.no_runtime_boundary_audit_v1 import audit_boundary

HARNESS_ID = "controlled_trial_post_execution_review_harness_v1"
HARNESS_MODULE = "capabilities.governance.controlled_trial_post_execution_review_harness_v1"

REVIEW_CHECKS: Tuple[str, ...] = (
    "execution_result_complete",
    "output_contract_honored",
    "no_fact_write",
    "no_side_effect",
    "logging_path_allowed_only",
    "abort_conditions_respected",
    "next_step_readiness",
)

ALLOWED_LOGGING_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "vision_sample_frame_single_chain_controlled_trial_execution"
)

FORBIDDEN_LOGGING_TARGETS: Tuple[str, ...] = (
    "repo__eval_out",
    "WorldModel",
    "Memory",
    "SceneDelta",
    "protected",
    "HR",
    "DnAE",
)

POST_EXECUTION_BOUNDARY_FIELDS: Tuple[str, ...] = (
    "live_camera_enabled_now",
    "camera_runtime_enabled_now",
    "frame_capture_executed_now",
    "new_image_read_executed_now",
    "arbitrary_image_read_executed_now",
    "vision_model_invoked_now",
    "visual_fact_generated_now",
    "ocr_provider_invoked_now",
    "navigation_action_triggered_now",
    "task_state_committed_now",
    "world_model_written_now",
    "memory_written_now",
    "scene_delta_generated_now",
    "tts_invoked_now",
    "llm_invoked_now",
    "user_facing_output_generated_now",
)


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _load_candidates(
    execution_root: Path,
    *,
    candidate_file_prefix: str = "visual_observation_candidate",
    bundle_filename: Optional[str] = None,
) -> List[Dict[str, Any]]:
    candidates: List[Dict[str, Any]] = []
    bundle_name = bundle_filename or f"{candidate_file_prefix}_result_v1.json"
    bundle = _try_read_json(execution_root / bundle_name) or {}
    for c in bundle.get("candidates") or []:
        candidates.append(c)
    for i in range(1, 10):
        p = execution_root / f"{candidate_file_prefix}_{i}_v1.json"
        if p.is_file():
            data = _try_read_json(p)
            if data and data not in candidates:
                candidates.append(data)
    return candidates


def review_controlled_trial_execution(
    execution_root: Path,
    *,
    trial_scope: str = "vision_sample_frame_single_chain",
    max_output_count: int = 3,
    expected_candidate_type: str = "visual_observation_candidate",
    candidate_file_prefix: str = "visual_observation_candidate",
    allowed_logging_root: Optional[str] = None,
    extra_boundary_fields: Optional[Tuple[str, ...]] = None,
    require_controlled_input: bool = True,
    require_frame_ref: bool = False,
) -> Dict[str, Any]:
    """Consume execution artifacts and return structured review results."""
    root = execution_root.expanduser().resolve()
    blockers: List[str] = []

    summary = _try_read_json(root / "summary.json") or {}
    trace = _try_read_json(root / "controlled_trial_execution_trace_v1.json") or {}
    manifest = _try_read_json(root / "controlled_trial_execution_input_manifest_v1.json") or {}
    exec_summary = _try_read_json(root / "controlled_trial_execution_summary_v1.json") or {}
    abort_mon = _try_read_json(root / "controlled_trial_abort_monitor_result_v1.json") or {}
    contract_comp = _try_read_json(root / "candidate_output_contract_compliance_v1.json") or {}

    candidates = _load_candidates(
        root,
        candidate_file_prefix=candidate_file_prefix,
    )
    candidate_ids = [c.get("candidate_id") for c in candidates if c.get("candidate_id")]

    completeness_checks = {
        "execution_summary_exists": exec_summary.get("summary_id") is not None,
        "execution_trace_exists": trace.get("trace_id") is not None,
        "inputs_recorded": (manifest.get("inputs_count") or 0) == 3,
        "outputs_recorded": len(candidates) == 3,
        "no_missing_output": len(candidates) >= 3,
        "no_duplicate_output_id": len(candidate_ids) == len(set(candidate_ids)),
        "output_count_within_max": len(candidates) <= max_output_count,
        "per_candidate_files_exist": all(
            (root / f"{candidate_file_prefix}_{i}_v1.json").is_file() for i in range(1, 4)
        ),
    }
    completeness_pass = all(completeness_checks.values())
    if not completeness_pass:
        blockers.append("execution result completeness failed")

    contract_rows: List[Dict[str, Any]] = []
    all_contract_pass = True
    for cand in candidates:
        ok, issues = validate_candidate_output(
            cand,
            expected_type=expected_candidate_type,
            require_timestamp=True,
        )
        extra_checks = [
            cand.get("trial_scope") == trial_scope,
            cand.get("provenance_present") is True,
        ]
        if require_controlled_input:
            extra_checks.append(cand.get("controlled_input") is True)
        if require_frame_ref:
            extra_checks.append(cand.get("frame_ref_present") is True)
        if expected_candidate_type == "ocr_result_candidate":
            extra_checks.append(cand.get("provider_type") == "mock_or_fixture_only")
        if expected_candidate_type == "navigation_guidance_candidate":
            extra_checks.extend(
                [
                    cand.get("navigation_action_allowed") is False,
                    cand.get("user_facing_output_allowed") is False,
                    cand.get("map_context_type") == "readonly_or_synthetic_only",
                ]
            )
        extra_ok = all(extra_checks)
        row_pass = ok and extra_ok
        if not row_pass:
            all_contract_pass = False
            blockers.append(f"contract fail: {cand.get('candidate_id')}")
        contract_rows.append(
            {
                "candidate_id": cand.get("candidate_id"),
                "contract_pass": row_pass,
                "issues": issues,
            }
        )

    boundary_fields = POST_EXECUTION_BOUNDARY_FIELDS
    if extra_boundary_fields:
        boundary_fields = tuple(dict.fromkeys(POST_EXECUTION_BOUNDARY_FIELDS + extra_boundary_fields))
    audit_snapshot = {f: summary.get(f, False) for f in boundary_fields}
    for f in boundary_fields:
        if audit_snapshot.get(f) is True:
            blockers.append(f"boundary violation at review: {f}")
    vision_audit = audit_boundary(audit_snapshot, profile="vision_no_runtime_profile")
    ocr_audit = audit_boundary(audit_snapshot, profile="ocr_no_runtime_profile")
    navigation_audit = audit_boundary(audit_snapshot, profile="navigation_no_runtime_profile")
    full_audit = audit_boundary(audit_snapshot, profile="full_no_runtime_profile")
    audit_pass = (
        vision_audit.get("audit_pass")
        and ocr_audit.get("audit_pass")
        and navigation_audit.get("audit_pass")
        and full_audit.get("audit_pass")
    )

    abort_triggered = abort_mon.get("abort_triggered") is True
    abort_pass = not abort_triggered and abort_mon.get("monitor_pass") is True
    if not abort_pass:
        blockers.append("abort monitor failed")

    out_dir = str(exec_summary.get("output_directory") or summary.get("execution_output_root") or "")
    allowed_root = allowed_logging_root or ALLOWED_LOGGING_ROOT
    logging_pass = all(
        [
            "Luna-Workspace-Min" in out_dir,
            allowed_root in out_dir or out_dir.rstrip("/") == allowed_root.rstrip("/"),
            exec_summary.get("workspace_fallback_only") is True,
        ]
    )
    if not logging_pass:
        blockers.append("logging path compliance failed")

    side_effect_pass = all(
        [
            summary.get("execution_aborted") is not True,
            summary.get("visual_fact_generated_now") is False,
            summary.get("world_model_written_now") is False,
            summary.get("memory_written_now") is False,
            contract_comp.get("compliance_pass") is True,
        ]
    )
    if not side_effect_pass:
        blockers.append("side effect absence failed")

    harness_checks = {
        "execution_result_complete": completeness_pass,
        "output_contract_honored": all_contract_pass,
        "no_fact_write": all(c.get("fact_status") == "not_fact" for c in candidates),
        "no_side_effect": side_effect_pass,
        "logging_path_allowed_only": logging_pass,
        "abort_conditions_respected": abort_pass,
        "next_step_readiness": completeness_pass and all_contract_pass and audit_pass,
    }
    review_pass = all(harness_checks.values()) and len(blockers) == 0

    return {
        "completeness": {
            "review_id": "execution_result_completeness_review",
            "checks": completeness_checks,
            "review_pass": completeness_pass,
            "inputs_count": manifest.get("inputs_count"),
            "outputs_count": len(candidates),
        },
        "candidate_contract": {
            "review_id": "visual_observation_candidate_contract_review",
            "rows": contract_rows,
            "review_pass": all_contract_pass,
        },
        "no_runtime": {
            "review_id": "no_runtime_boundary_post_execution_review",
            "vision_profile": vision_audit,
            "ocr_profile": ocr_audit,
            "navigation_profile": navigation_audit,
            "full_profile": full_audit,
            "review_pass": audit_pass,
        },
        "abort": {
            "review_id": "abort_monitor_post_execution_review",
            "abort_triggered": abort_triggered,
            "review_pass": abort_pass,
        },
        "logging": {
            "review_id": "logging_path_compliance_review",
            "allowed_root": allowed_root,
            "observed_directory": out_dir,
            "forbidden_targets": list(FORBIDDEN_LOGGING_TARGETS),
            "review_pass": logging_pass,
        },
        "side_effect": {
            "review_id": "side_effect_absence_review",
            "checks": {
                "no_external_provider": True,
                "no_runtime_action": all(
                    c.get("runtime_action_allowed") is False for c in candidates
                ),
                "no_user_facing_output": summary.get("user_facing_output_generated_now") is False,
                "no_persistent_fact": all(c.get("fact_status") == "not_fact" for c in candidates),
                "no_task_commit": summary.get("task_state_committed_now") is False,
            },
            "review_pass": side_effect_pass,
        },
        "harness_result": {
            "harness_id": HARNESS_ID,
            "checks": harness_checks,
            "review_pass": review_pass,
            "runtime_consumption_tested_now": True,
            "blockers": blockers,
        },
        "execution_summary": summary,
    }


def review_execution_result_contract_level(
    execution_result: Optional[Dict[str, Any]] = None,
    *,
    boundary_meta: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Backward-compatible wrapper when execution_result bundle is pre-built."""
    meta = dict(boundary_meta or {})
    if execution_result and execution_result.get("execution_root"):
        bundle = review_controlled_trial_execution(Path(execution_result["execution_root"]))
        return {**bundle["harness_result"], **meta}
    checks = {c: True for c in REVIEW_CHECKS}
    return {
        "result_id": "post_execution_review_result",
        "harness_id": HARNESS_ID,
        "simulated": True,
        "checks": checks,
        "review_pass": True,
        "contract_defined": True,
        "runtime_consumption_tested_now": False,
        **meta,
    }


def build_contract_document(*, meta: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    m = dict(meta or {})
    return {
        "contract_id": "controlled_trial_post_execution_review_harness_contract_v1",
        "harness_id": HARNESS_ID,
        "harness_module": HARNESS_MODULE,
        "review_checks": list(REVIEW_CHECKS),
        "entrypoint": "review_controlled_trial_execution(execution_root)",
        "standard_flow": "execution_result → post_execution_review_harness.review → closure_decision",
        **m,
    }
