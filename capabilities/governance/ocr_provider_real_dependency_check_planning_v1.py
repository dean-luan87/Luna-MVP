# -*- coding: utf-8 -*-
"""OCR Provider Real Dependency Check Planning v1 — planning-only, no real checks."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.ocr_provider_selection_dependency_environment_dryrun_v1 import (
    BLOCKED_PATHS as SELECTION_DRYRUN_BLOCKED,
)
from capabilities.governance.ocr_provider_selection_dependency_environment_post_dryrun_review_v1 import (
    FINAL_DECISION_GO as POST_REVIEW_FINAL_GO,
    NEXT_PHASE_GO as POST_REVIEW_NEXT_PHASE,
)

PHASE_ID = "Phase-OCR-Provider-Real-Dependency-Check-Planning-v1-001"
SCOPE = "ocr_provider_real_dependency_check_planning_only"
SOURCE_CHAIN = "ocr_provider_real_dependency_check_planning_v1"

UPSTREAM_POST_REVIEW_FINAL = POST_REVIEW_FINAL_GO
UPSTREAM_POST_REVIEW_NEXT = POST_REVIEW_NEXT_PHASE

FINAL_DECISION_GO = "OCR_PROVIDER_REAL_DEPENDENCY_CHECK_PLANNING_READY_FOR_DRYRUN"
FINAL_DECISION_HOLD = "OCR_PROVIDER_REAL_DEPENDENCY_CHECK_PLANNING_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-OCR-Provider-Real-Dependency-Check-DryRun-v1-001"
NEXT_PHASE_HOLD = "Phase-OCR-Provider-Real-Dependency-Check-Issue-Review-v1-001"

FUTURE_CHECK_SCOPE: Tuple[str, ...] = (
    "python_package_presence_check",
    "provider_import_check",
    "model_cache_path_check",
    "model_file_existence_check",
    "model_file_hash_check",
    "runtime_smoke_check_later",
    "sample_ocr_check_later",
)

CHECK_SEQUENCE: Tuple[Dict[str, str], ...] = (
    {
        "step_id": "01_environment_isolation_check",
        "step_label": "environment isolation check",
        "precondition": "sandbox_path_confirmed_and_no_production_write",
        "failure_route": "environment_issue_candidate",
        "rollback_required": False,
    },
    {
        "step_id": "02_python_package_presence_check",
        "step_label": "python package presence check",
        "precondition": "environment_isolation_pass",
        "failure_route": "dependency_issue_candidate",
        "rollback_required": False,
    },
    {
        "step_id": "03_model_cache_directory_check",
        "step_label": "model cache directory check",
        "precondition": "package_presence_pass_or_documented_skip",
        "failure_route": "model_cache_issue_candidate",
        "rollback_required": False,
    },
    {
        "step_id": "04_model_file_existence_check",
        "step_label": "model file existence check",
        "precondition": "cache_directory_pass",
        "failure_route": "model_cache_issue_candidate",
        "rollback_required": False,
    },
    {
        "step_id": "05_model_file_hash_check",
        "step_label": "model file hash check",
        "precondition": "model_files_exist",
        "failure_route": "model_integrity_issue_candidate",
        "rollback_required": True,
    },
    {
        "step_id": "06_provider_import_check",
        "step_label": "provider import check",
        "precondition": "hash_check_pass_or_waived_with_evidence",
        "failure_route": "provider_import_failure_candidate",
        "rollback_required": True,
    },
    {
        "step_id": "07_provider_initialization_dry_check",
        "step_label": "provider initialization dry check",
        "precondition": "import_check_pass",
        "failure_route": "provider_runtime_issue_candidate",
        "rollback_required": True,
    },
    {
        "step_id": "08_runtime_smoke_check",
        "step_label": "runtime smoke check",
        "precondition": "initialization_dry_pass",
        "failure_route": "provider_runtime_issue_candidate",
        "rollback_required": True,
    },
    {
        "step_id": "09_sample_ocr_check_later",
        "step_label": "sample OCR check later",
        "precondition": "smoke_check_pass_and_trial_authorization",
        "failure_route": "provider_quality_issue_candidate",
        "rollback_required": True,
    },
)

FAILURE_HANDLING: Tuple[Dict[str, str], ...] = (
    {"condition": "missing_package", "route": "dependency_issue_candidate"},
    {"condition": "import_failure", "route": "provider_import_failure_candidate"},
    {"condition": "model_file_missing", "route": "model_cache_issue_candidate"},
    {"condition": "hash_mismatch", "route": "model_integrity_issue_candidate"},
    {"condition": "smoke_failure", "route": "provider_runtime_issue_candidate"},
    {"condition": "sample_ocr_failure", "route": "provider_quality_issue_candidate"},
    {"condition": "timeout", "route": "hold_candidate"},
    {"condition": "high_memory_pressure", "route": "degradation_candidate"},
)

EVIDENCE_ARTIFACTS: Tuple[str, ...] = (
    "environment_snapshot",
    "python_version_snapshot",
    "package_presence_result",
    "import_result",
    "model_cache_result",
    "model_file_hash_result",
    "smoke_check_result",
    "sample_ocr_result_later",
    "boundary_audit_result",
    "verifier_report",
)

ROLLBACK_RULES: Tuple[str, ...] = (
    "no_production_path_write",
    "no_global_environment_modification",
    "no_untracked_install",
    "no_model_download_without_authorization",
    "no_cache_mutation_without_approval",
    "evidence_only_output",
    "failed_check_does_not_trigger_install",
)

BLOCKED_PATHS: Tuple[str, ...] = (
    "planning_to_dependency_check_execution",
    "planning_to_pip_install",
    "planning_to_model_download",
    "planning_to_provider_import",
    "planning_to_provider_initialization",
    "planning_to_smoke_check",
    "planning_to_sample_ocr",
    "planning_to_provider_selection_finalize",
    "planning_to_provider_authorization",
    "planning_to_controlled_trial",
    "planning_to_ocr_request_submit",
    "planning_to_image_read",
    "planning_to_ocr_fact",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "real_dependency_check_executed_now",
    "provider_import_check_executed_now",
    "dependency_install_executed_now",
    "model_download_executed_now",
    "model_cache_hash_check_executed_now",
    "provider_smoke_check_executed_now",
    "sample_ocr_executed_now",
    "provider_selection_finalized_now",
    "provider_authorization_started_now",
    "controlled_trial_started_now",
    "paddleocr_imported_now",
    "rapidocr_imported_now",
    "external_ocr_imported_now",
    "paddleocr_invoked_now",
    "rapidocr_invoked_now",
    "external_ocr_invoked_now",
    "real_ocr_provider_invoked_now",
    "ocr_request_submitted_now",
    "image_read_executed_now",
    "crop_executed_now",
    "ocr_fact_generated_now",
    "memory_written_now",
    "world_model_written_now",
    "user_facing_output_generated_now",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Planning GO ≠ real dependency check executed",
    "Planning GO ≠ pip install or model download",
    "Planning GO ≠ provider import or invocation",
    "future check sequence planned ≠ checks run now",
    "evidence package plan ≠ evidence collected now",
    "execution gate defined ≠ authorization granted",
    "DryRun next ≠ real import/install allowed",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/ocr_provider_real_dependency_check_planning"
)


def _planning_meta() -> Dict[str, Any]:
    meta = {
        "ocr_provider_real_dependency_check_planning_only": True,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "selected_provider_for_execution": None,
    }
    for field in BOUNDARY_FALSE:
        meta[field] = False
    return meta


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _sequence_steps(meta: Dict[str, Any]) -> List[Dict[str, Any]]:
    steps: List[Dict[str, Any]] = []
    for spec in CHECK_SEQUENCE:
        steps.append(
            {
                "step_id": spec["step_id"],
                "step_label": spec["step_label"],
                "precondition": spec["precondition"],
                "execution_allowed_later": True,
                "evidence_required": True,
                "failure_route": spec["failure_route"],
                "rollback_required": bool(spec["rollback_required"]),
                "current_executed_now": False,
                **meta,
            }
        )
    return steps


def _provider_plan(
    *,
    provider_family: str,
    package_ref: str,
    model_files_required: bool,
    cache_path: str,
    meta: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "plan_id": f"{provider_family}_real_dependency_check_plan_v1",
        "provider_family": provider_family,
        "package_name_or_provider_ref": package_ref,
        "model_file_requirement": model_files_required,
        "cache_path_requirement": cache_path,
        "import_check_later": True,
        "smoke_check_later": True,
        "sample_ocr_later": True,
        "current_invocation_allowed": False,
        "current_import_executed_now": False,
        "planning_only": True,
        **meta,
    }


def run_ocr_provider_real_dependency_check_planning_v1(
    *,
    ocr_provider_selection_dependency_environment_post_dryrun_review_root: str,
    ocr_provider_selection_dependency_environment_dryrun_root: Optional[str] = None,
    ocr_provider_selection_dependency_environment_planning_root: Optional[str] = None,
    ocr_controlled_provider_post_dryrun_review_root: Optional[str] = None,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    post_root = Path(ocr_provider_selection_dependency_environment_post_dryrun_review_root).expanduser().resolve()
    post_sm = _try_read_json(post_root / "summary.json") or {}
    post_vr = _try_read_json(post_root / "verifier_report.json") or {}
    next_route = _try_read_json(post_root / "next_route_readiness_decision_v1.json") or {}
    closure = _try_read_json(post_root / "provider_selection_dependency_environment_closure_decision_v1.json") or {}

    sel_dryrun_root = Path(
        ocr_provider_selection_dependency_environment_dryrun_root
        or post_sm.get("upstream_dryrun_root")
        or post_root.parent / "ocr_provider_selection_dependency_environment_dryrun"
    ).expanduser().resolve()
    sel_planning_root = Path(
        ocr_provider_selection_dependency_environment_planning_root
        or post_root.parent / "ocr_provider_selection_dependency_environment_planning"
    ).expanduser().resolve()
    ocr_post_root = Path(
        ocr_controlled_provider_post_dryrun_review_root
        or post_root.parent / "ocr_controlled_provider_post_dryrun_review"
    ).expanduser().resolve()

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_planning_meta(),
        "upstream_post_dryrun_review_root": str(post_root),
        "upstream_selection_dryrun_root": str(sel_dryrun_root),
        "upstream_selection_planning_root": str(sel_planning_root),
        "output_root": str(out_root),
    }

    sel_dryrun_sm = _try_read_json(sel_dryrun_root / "summary.json") or {}
    blocked_sel = _try_read_json(sel_dryrun_root / "provider_selection_blocked_path_result_v1.json") or {}
    ocr_post_sm = _try_read_json(ocr_post_root / "summary.json") or {}

    post_go = post_vr.get("verifier") == "GO" and post_vr.get("passed") is True
    if not post_go:
        blockers.append("post-dryrun review verifier must be GO")
    if post_sm.get("final_decision") != UPSTREAM_POST_REVIEW_FINAL:
        blockers.append("post-review final_decision mismatch")
    if post_sm.get("recommended_next_phase") != UPSTREAM_POST_REVIEW_NEXT:
        blockers.append("post-review recommended_next_phase mismatch")
    if closure.get("ocr_provider_selection_dependency_environment_dryrun_closed") is not True:
        blockers.append("selection dryrun must be closed")
    if post_sm.get("provider_selection_candidate_trusted") is not True:
        blockers.append("provider_selection_candidate_trusted required")

    for flag in (
        "do_not_import_provider_now",
        "do_not_install_dependency_now",
        "do_not_invoke_provider_now",
        "do_not_finalize_provider_selection_now",
    ):
        if next_route.get(flag) is not True:
            blockers.append(f"{flag} required in next_route")

    if sel_dryrun_sm.get("selected_provider_for_execution") is not None:
        blockers.append("selected_provider_for_execution must be null")
    if sel_dryrun_sm.get("provider_selection_finalized_now") is True:
        blockers.append("provider_selection_finalized_now must be false")

    if blocked_sel.get("all_blocked") is not True or len(blocked_sel.get("paths") or []) != len(
        SELECTION_DRYRUN_BLOCKED
    ):
        blockers.append("15 selection dryrun blocked paths must remain blocked")

    if ocr_post_sm.get("ocr_controlled_provider_dryrun_closed") is not True:
        blockers.append("ocr controlled provider dryrun should be closed")

    input_review = {
        "review_id": "provider_selection_post_review_input_review_v1",
        "upstream_post_review_root": str(post_root),
        "upstream_selection_dryrun_root": str(sel_dryrun_root),
        "upstream_verifier_go": post_go,
        "upstream_final_decision": post_sm.get("final_decision"),
        "selection_candidate_trusted": post_sm.get("provider_selection_candidate_trusted"),
        "dependency_candidate_trusted": closure.get("dependency_readiness_candidate_trusted"),
        "environment_candidate_trusted": closure.get("environment_readiness_candidate_trusted"),
        "blocked_paths_count": len(blocked_sel.get("paths") or []),
        "review_pass": len(blockers) == 0,
        "blockers": blockers,
        **meta,
    }

    policy = {
        "policy_id": "ocr_real_dependency_check_planning_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "forbidden_in_planning": list(FUTURE_CHECK_SCOPE),
        "all_future_checks_executed_now": False,
        **meta,
    }

    scope = {
        "scope_id": "real_dependency_check_scope_v1",
        "future_checks_allowed_after_authorization": list(FUTURE_CHECK_SCOPE),
        "forbidden_now": list(FUTURE_CHECK_SCOPE),
        "planning_does_not_execute_checks": True,
        **meta,
    }

    sequence_plan = {
        "plan_id": "provider_dependency_check_sequence_plan_v1",
        "sequence_order": [s["step_id"] for s in CHECK_SEQUENCE],
        "steps": _sequence_steps(meta),
        "step_count": len(CHECK_SEQUENCE),
        "all_current_executed_now_false": True,
        **meta,
    }

    paddle_plan = _provider_plan(
        provider_family="paddleocr_later",
        package_ref="paddlepaddle,paddleocr",
        model_files_required=True,
        cache_path="${LUNA_OCR_MODEL_CACHE}/paddleocr",
        meta=meta,
    )
    rapid_plan = _provider_plan(
        provider_family="rapidocr_later",
        package_ref="rapidocr-onnxruntime,onnxruntime",
        model_files_required=True,
        cache_path="${LUNA_OCR_MODEL_CACHE}/rapidocr",
        meta=meta,
    )
    external_plan = _provider_plan(
        provider_family="external_ocr_later",
        package_ref="httpx,external_ocr_client",
        model_files_required=False,
        cache_path="n/a_network_client",
        meta=meta,
    )

    model_integrity = {
        "plan_id": "model_cache_and_file_integrity_check_plan_v1",
        "checks_planned": [
            "model_cache_path_check",
            "model_file_existence_check",
            "model_file_hash_check",
        ],
        "hash_mismatch_route": "model_integrity_issue_candidate",
        "model_cache_hash_check_executed_now": False,
        "model_download_executed_now": False,
        **meta,
    }

    import_boundary = {
        "plan_id": "import_check_authorization_boundary_plan_v1",
        "import_check_requires_authorization": True,
        "import_check_executed_now": False,
        "provider_import_check_executed_now": False,
        "paddleocr_imported_now": False,
        "rapidocr_imported_now": False,
        "external_ocr_imported_now": False,
        "failed_import_does_not_trigger_install": True,
        **meta,
    }

    isolation_plan = {
        "plan_id": "environment_isolation_and_sandbox_plan_v1",
        "virtualenv_required": True,
        "sandbox_path": "${LUNA_OCR_SANDBOX:-./_tmp_eval_out/ocr_real_dependency_sandbox}",
        "no_production_path_write": True,
        "no_global_environment_modification": True,
        "network_dependency_default": False,
        **meta,
    }

    evidence_plan = {
        "plan_id": "evidence_package_plan_v1",
        "artifacts": list(EVIDENCE_ARTIFACTS),
        "evidence_only_output": True,
        "verifier_report_required": True,
        "evidence_collected_now": False,
        **meta,
    }

    failure_plan = {
        "plan_id": "failure_handling_and_rollback_plan_v1",
        "failure_routes": list(FAILURE_HANDLING),
        "rollback_rules": list(ROLLBACK_RULES),
        "failed_check_does_not_trigger_install": True,
        **meta,
    }

    blocked_matrix = {
        "matrix_id": "real_dependency_check_blocked_path_matrix_v1",
        "paths": [{"path_id": p, "blocked": True} for p in BLOCKED_PATHS],
        "path_count": len(BLOCKED_PATHS),
        "all_blocked": True,
        **meta,
    }

    execution_gate = {
        "gate_id": "real_dependency_check_future_execution_gate_v1",
        "real_dependency_check_authorization_required": True,
        "execution_window_required": True,
        "sandbox_path_confirmed": True,
        "no_production_path_write": True,
        "rollback_plan_ready": True,
        "evidence_package_required": True,
        "verifier_required": True,
        "owner_operator_approval_later_if_needed": True,
        "gate_open_now": False,
        **meta,
    }

    planning_ok = len(blockers) == 0 and input_review.get("review_pass") is True
    boundary_ok = planning_ok

    planning_decision = {
        "decision_id": "real_dependency_check_planning_decision_v1",
        "planning_pass": planning_ok,
        "ready_for_dryrun": boundary_ok,
        "final_decision": FINAL_DECISION_GO if boundary_ok else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if boundary_ok else NEXT_PHASE_HOLD,
        **meta,
    }

    non_claims = {
        "register_id": "real_dependency_check_non_claims_register_v1",
        "non_claims": list(NON_CLAIMS),
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": planning_decision["final_decision"],
        "recommended_next_phase": planning_decision["recommended_next_phase"],
        "high_risk_count": 0 if boundary_ok else 1,
        **meta,
    }

    return {
        "ocr_real_dependency_check_planning_policy": policy,
        "provider_selection_post_review_input_review": input_review,
        "real_dependency_check_scope": scope,
        "provider_dependency_check_sequence_plan": sequence_plan,
        "paddleocr_real_dependency_check_plan": paddle_plan,
        "rapidocr_real_dependency_check_plan": rapid_plan,
        "external_ocr_real_dependency_check_plan": external_plan,
        "model_cache_and_file_integrity_check_plan": model_integrity,
        "import_check_authorization_boundary_plan": import_boundary,
        "environment_isolation_and_sandbox_plan": isolation_plan,
        "evidence_package_plan": evidence_plan,
        "failure_handling_and_rollback_plan": failure_plan,
        "real_dependency_check_blocked_path_matrix": blocked_matrix,
        "real_dependency_check_future_execution_gate": execution_gate,
        "real_dependency_check_non_claims_register": non_claims,
        "real_dependency_check_planning_decision": planning_decision,
        "summary": summary,
    }
