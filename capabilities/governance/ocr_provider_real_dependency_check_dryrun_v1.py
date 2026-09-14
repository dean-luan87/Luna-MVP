# -*- coding: utf-8 -*-
"""OCR Provider Real Dependency Check DryRun v1 — simulated flow only."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.ocr_provider_real_dependency_check_planning_v1 import (
    CHECK_SEQUENCE,
    EVIDENCE_ARTIFACTS,
    FAILURE_HANDLING,
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
    NEXT_PHASE_GO as PLANNING_NEXT_PHASE,
    ROLLBACK_RULES,
)

PHASE_ID = "Phase-OCR-Provider-Real-Dependency-Check-DryRun-v1-001"
SCOPE = "ocr_provider_real_dependency_check_dryrun_only"
SOURCE_CHAIN = "ocr_provider_real_dependency_check_dryrun_v1"

UPSTREAM_PLANNING_FINAL = PLANNING_FINAL_GO
UPSTREAM_PLANNING_NEXT = PLANNING_NEXT_PHASE

FINAL_DECISION_GO = "OCR_PROVIDER_REAL_DEPENDENCY_CHECK_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
FINAL_DECISION_HOLD = "OCR_PROVIDER_REAL_DEPENDENCY_CHECK_DRYRUN_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-OCR-Provider-Real-Dependency-Check-Post-DryRun-Review-v1-001"
NEXT_PHASE_HOLD = "Phase-OCR-Provider-Real-Dependency-Check-Issue-Review-v1-001"

EVIDENCE_CANDIDATE_SLOTS: Tuple[str, ...] = (
    "environment_snapshot_candidate",
    "python_version_snapshot_candidate",
    "package_presence_result_candidate",
    "import_result_candidate",
    "model_cache_result_candidate",
    "model_file_hash_result_candidate",
    "smoke_check_result_candidate",
    "sample_ocr_result_later_candidate",
    "boundary_audit_result_candidate",
    "verifier_report_candidate",
)

BLOCKED_PATHS: Tuple[str, ...] = (
    "dryrun_to_dependency_check_execution",
    "dryrun_to_pip_install",
    "dryrun_to_model_download",
    "dryrun_to_provider_import",
    "dryrun_to_provider_initialization",
    "dryrun_to_smoke_check",
    "dryrun_to_sample_ocr",
    "dryrun_to_provider_selection_finalize",
    "dryrun_to_provider_authorization",
    "dryrun_to_controlled_trial",
    "dryrun_to_ocr_request_submit",
    "dryrun_to_image_read",
    "dryrun_to_ocr_fact",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "real_dependency_check_executed_now",
    "python_package_check_executed_now",
    "provider_import_check_executed_now",
    "dependency_install_executed_now",
    "model_download_executed_now",
    "model_cache_path_check_executed_now",
    "model_file_existence_check_executed_now",
    "model_file_hash_check_executed_now",
    "provider_initialization_executed_now",
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
    "rollback_executed_now",
    "evidence_collected_now",
    "evidence_package_committed_now",
)

NON_CLAIMS: Tuple[str, ...] = (
    "DryRun GO ≠ real dependency check executed",
    "DryRun GO ≠ pip install or model download",
    "evidence_package_candidate ≠ evidence committed",
    "failure_route_candidate ≠ failure handled now",
    "rollback_plan_candidate ≠ rollback executed",
    "Post-DryRun Review next ≠ import/install allowed",
    "sequence simulated ≠ checks run on host",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/ocr_provider_real_dependency_check_dryrun"
)

_PROVIDER_SPECS: Tuple[Dict[str, str], ...] = (
    {
        "provider_candidate_ref": "ocr_provider_paddleocr_later",
        "provider_family": "paddleocr_later",
        "package_name_or_provider_ref": "paddlepaddle,paddleocr",
        "cache_path_requirement": "${LUNA_OCR_MODEL_CACHE}/paddleocr",
    },
    {
        "provider_candidate_ref": "ocr_provider_rapidocr_later",
        "provider_family": "rapidocr_later",
        "package_name_or_provider_ref": "rapidocr-onnxruntime,onnxruntime",
        "cache_path_requirement": "${LUNA_OCR_MODEL_CACHE}/rapidocr",
    },
    {
        "provider_candidate_ref": "ocr_provider_external_ocr_later",
        "provider_family": "external_ocr_later",
        "package_name_or_provider_ref": "httpx,external_ocr_client",
        "cache_path_requirement": "n/a_network_client",
    },
)


def _dryrun_meta() -> Dict[str, Any]:
    meta = {
        "ocr_provider_real_dependency_check_dryrun_only": True,
        "simulated": True,
        "real_dependency_check_flow_simulated_now": True,
        "evidence_package_candidate_generated_now": True,
        "failure_route_candidate_generated_now": True,
        "rollback_plan_candidate_generated_now": True,
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


def _provider_dryrun_result(spec: Dict[str, str], meta: Dict[str, Any]) -> Dict[str, Any]:
    fam = spec["provider_family"]
    return {
        "result_id": f"{fam}_dependency_check_dryrun_result_v1",
        "provider_candidate_ref": spec["provider_candidate_ref"],
        "provider_family": fam,
        "package_name_or_provider_ref": spec["package_name_or_provider_ref"],
        "cache_path_requirement": spec["cache_path_requirement"],
        "import_check_later": True,
        "smoke_check_later": True,
        "sample_ocr_later": True,
        "current_invocation_allowed": False,
        "current_import_executed_now": False,
        "current_provider_invoked_now": False,
        "simulated_pass": True,
        **meta,
    }


def run_ocr_provider_real_dependency_check_dryrun_v1(
    *,
    ocr_provider_real_dependency_check_planning_root: str,
    ocr_provider_selection_dependency_environment_post_dryrun_review_root: Optional[str] = None,
    ocr_provider_selection_dependency_environment_dryrun_root: Optional[str] = None,
    ocr_controlled_provider_post_dryrun_review_root: Optional[str] = None,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    planning_root = Path(ocr_provider_real_dependency_check_planning_root).expanduser().resolve()
    plan_sm = _try_read_json(planning_root / "summary.json") or {}
    plan_vr = _try_read_json(planning_root / "verifier_report.json") or {}
    gate_plan = _try_read_json(planning_root / "real_dependency_check_future_execution_gate_v1.json") or {}
    blocked_plan = _try_read_json(planning_root / "real_dependency_check_blocked_path_matrix_v1.json") or {}

    sel_post_root = Path(
        ocr_provider_selection_dependency_environment_post_dryrun_review_root
        or planning_root.parent / "ocr_provider_selection_dependency_environment_post_dryrun_review"
    ).expanduser().resolve()
    sel_dryrun_root = Path(
        ocr_provider_selection_dependency_environment_dryrun_root
        or planning_root.parent / "ocr_provider_selection_dependency_environment_dryrun"
    ).expanduser().resolve()
    ocr_post_root = Path(
        ocr_controlled_provider_post_dryrun_review_root
        or planning_root.parent / "ocr_controlled_provider_post_dryrun_review"
    ).expanduser().resolve()

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {**_dryrun_meta(), "upstream_planning_root": str(planning_root), "output_root": str(out_root)}

    sel_post_sm = _try_read_json(sel_post_root / "summary.json") or {}
    sel_dryrun_sm = _try_read_json(sel_dryrun_root / "summary.json") or {}
    ocr_post_sm = _try_read_json(ocr_post_root / "summary.json") or {}

    planning_go = plan_vr.get("verifier") == "GO" and plan_vr.get("passed") is True
    if not planning_go:
        blockers.append("planning verifier must be GO")
    if plan_sm.get("final_decision") != UPSTREAM_PLANNING_FINAL:
        blockers.append("planning final_decision mismatch")
    if plan_sm.get("recommended_next_phase") != UPSTREAM_PLANNING_NEXT:
        blockers.append("planning recommended_next_phase mismatch")
    if plan_sm.get("real_dependency_check_executed_now") is True:
        blockers.append("real_dependency_check_executed_now must be false upstream")
    if gate_plan.get("gate_open_now") is not False:
        blockers.append("future execution gate must be closed")
    if blocked_plan.get("all_blocked") is not True:
        blockers.append("planning blocked paths must be all blocked")

    if sel_dryrun_sm.get("selected_provider_for_execution") is not None:
        blockers.append("selected_provider_for_execution must be null")
    if sel_post_sm.get("provider_selection_candidate_trusted") is not True:
        blockers.append("selection candidates must be trusted")

    input_review = {
        "review_id": "real_dependency_check_planning_input_review_v1",
        "upstream_planning_root": str(planning_root),
        "upstream_verifier_go": planning_go,
        "upstream_final_decision": plan_sm.get("final_decision"),
        "selection_post_review_closed": sel_post_sm.get(
            "ocr_provider_selection_dependency_environment_dryrun_closed"
        ),
        "review_pass": len(blockers) == 0,
        "blockers": blockers,
        **meta,
    }

    sequence_steps = []
    for spec in CHECK_SEQUENCE:
        sequence_steps.append(
            {
                "step_id": spec["step_id"],
                "step_name": spec["step_label"],
                "precondition": spec["precondition"],
                "execution_allowed_later": True,
                "current_executed_now": False,
                "evidence_required": True,
                "evidence_candidate_generated": True,
                "failure_route": spec["failure_route"],
                "rollback_required": True,
                "blocked_now": True,
                "simulated": True,
                **meta,
            }
        )

    sequence_result = {
        "result_id": "dependency_check_sequence_dryrun_result_v1",
        "steps": sequence_steps,
        "step_count": len(sequence_steps),
        "all_current_executed_now_false": True,
        **meta,
    }

    paddle_result = _provider_dryrun_result(_PROVIDER_SPECS[0], meta)
    rapid_result = _provider_dryrun_result(_PROVIDER_SPECS[1], meta)
    external_result = _provider_dryrun_result(_PROVIDER_SPECS[2], meta)

    evidence_slots = [
        {
            "slot_id": slot,
            "artifact_type": slot,
            "candidate_only": True,
            "collected_now": False,
            "simulated_placeholder": f"dryrun_{slot}",
        }
        for slot in EVIDENCE_CANDIDATE_SLOTS
    ]
    evidence_candidate = {
        "artifact_id": "evidence_package_candidate_v1",
        "slots": evidence_slots,
        "slot_count": len(evidence_slots),
        "evidence_collected_now": False,
        "evidence_package_committed_now": False,
        "evidence_only_output": True,
        "mapped_from_plan": list(EVIDENCE_ARTIFACTS),
        **meta,
    }

    failure_rows = [
        {
            "condition": fh["condition"],
            "route": fh["route"],
            "routed": True,
            "executed_now": False,
            "candidate_only": True,
        }
        for fh in FAILURE_HANDLING
    ]
    failure_matrix = {
        "matrix_id": "failure_route_candidate_matrix_v1",
        "routes": failure_rows,
        "route_count": len(failure_rows),
        **meta,
    }

    rollback_candidate = {
        "result_id": "rollback_plan_candidate_result_v1",
        "rules": {rule: True for rule in ROLLBACK_RULES},
        "rule_keys": list(ROLLBACK_RULES),
        "rollback_executed_now": False,
        "failed_check_does_not_trigger_install": True,
        **meta,
    }

    isolation_result = {
        "result_id": "environment_isolation_boundary_dryrun_result_v1",
        "virtualenv_required": True,
        "sandbox_path": "${LUNA_OCR_SANDBOX:-./_tmp_eval_out/ocr_real_dependency_sandbox}",
        "no_production_path_write": True,
        "no_global_environment_modification": True,
        "boundary_pass": True,
        **meta,
    }

    gate_dryrun = {
        "result_id": "future_execution_gate_dryrun_result_v1",
        "real_dependency_check_authorization_required": True,
        "execution_window_required": True,
        "sandbox_path_confirmed_later": True,
        "no_production_path_write": True,
        "rollback_plan_ready": True,
        "evidence_package_required": True,
        "verifier_required": True,
        "owner_operator_approval_later_if_needed": True,
        "gate_open_now": False,
        "execution_allowed_now": False,
        **meta,
    }

    blocked_result = {
        "result_id": "real_dependency_check_blocked_path_result_v1",
        "paths": [{"path_id": p, "blocked": True} for p in BLOCKED_PATHS],
        "path_count": len(BLOCKED_PATHS),
        "all_blocked": True,
        **meta,
    }

    no_execution_audit = {
        "audit_id": "real_dependency_check_no_execution_audit_v1",
        "no_import": True,
        "no_install": True,
        "no_download": True,
        "no_package_check": True,
        "no_hash_check": True,
        "no_smoke": True,
        "no_sample_ocr": True,
        "no_provider_invoke": True,
        "no_ocr_request_submit": True,
        "no_image_read_or_crop": True,
        "no_fact_memory_world_model_write": True,
        "paddleocr_imported_now": False,
        "rapidocr_imported_now": False,
        "dependency_install_executed_now": False,
        "model_download_executed_now": False,
        "audit_pass": True,
        **meta,
    }

    checks_pass = (
        len(blockers) == 0
        and input_review.get("review_pass")
        and sequence_result.get("step_count") == 9
        and blocked_result.get("all_blocked")
        and no_execution_audit.get("audit_pass")
        and gate_dryrun.get("gate_open_now") is False
        and len(evidence_slots) == len(EVIDENCE_CANDIDATE_SLOTS)
    )

    readiness = {
        "decision_id": "real_dependency_check_dryrun_readiness_decision_v1",
        "sequence_pass": checks_pass,
        "provider_specific_pass": checks_pass,
        "evidence_pass": checks_pass,
        "failure_pass": checks_pass,
        "rollback_pass": checks_pass,
        "gate_pass": checks_pass,
        "blocked_pass": checks_pass,
        "audit_pass": checks_pass,
        "all_pass": checks_pass,
        "high_risk_count": 0 if checks_pass else 1,
        "final_decision": FINAL_DECISION_GO if checks_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if checks_pass else NEXT_PHASE_HOLD,
        **meta,
    }

    policy = {
        "policy_id": "ocr_real_dependency_check_dryrun_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        **meta,
    }

    non_claims = {
        "register_id": "non_claims_register_v1",
        "non_claims": list(NON_CLAIMS),
        **meta,
    }

    boundary_ok = checks_pass
    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": readiness["final_decision"],
        "recommended_next_phase": readiness["recommended_next_phase"],
        "high_risk_count": readiness["high_risk_count"],
        **meta,
    }

    return {
        "ocr_real_dependency_check_dryrun_policy": policy,
        "real_dependency_check_planning_input_review": input_review,
        "dependency_check_sequence_dryrun_result": sequence_result,
        "paddleocr_dependency_check_dryrun_result": paddle_result,
        "rapidocr_dependency_check_dryrun_result": rapid_result,
        "external_ocr_dependency_check_dryrun_result": external_result,
        "evidence_package_candidate": evidence_candidate,
        "failure_route_candidate_matrix": failure_matrix,
        "rollback_plan_candidate_result": rollback_candidate,
        "environment_isolation_boundary_dryrun_result": isolation_result,
        "future_execution_gate_dryrun_result": gate_dryrun,
        "real_dependency_check_blocked_path_result": blocked_result,
        "real_dependency_check_no_execution_audit": no_execution_audit,
        "real_dependency_check_dryrun_readiness_decision": readiness,
        "non_claims_register": non_claims,
        "summary": summary,
    }
