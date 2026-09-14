# -*- coding: utf-8 -*-
"""OCR Real Minimal Controlled Execution Final Ready Check v1 — compressed gate before real execution."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.ocr_real_dependency_execution_final_preflight_v1 import (
    FINAL_DECISION_GO as UPSTREAM_PREFLIGHT_FINAL_GO,
    MINIMAL_SCOPE_ALLOWED_CHECKS,
)
from capabilities.governance.ocr_real_dependency_minimal_controlled_execution_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as UPSTREAM_MINIMAL_DRYRUN_FINAL_GO,
)
from capabilities.governance.ocr_real_dependency_minimal_controlled_execution_planning_v1 import (
    EVIDENCE_OUTPUT_ITEMS,
    FAILURE_ROUTES,
    MINIMAL_FORBIDDEN_ACTIONS,
)
from capabilities.governance.ocr_real_dependency_real_minimal_execution_authorization_decision_v1 import (
    FINAL_DECISION_GO as UPSTREAM_AUTH_DECISION_FINAL_GO,
    SELECTED_ROUTE as UPSTREAM_SELECTED_ROUTE,
)

PHASE_ID = "Phase-OCR-Real-Dependency-Real-Minimal-Controlled-Execution-Final-Ready-Check-v1-001"
SCOPE = "final_ready_check_only"
SOURCE_CHAIN = "ocr_real_dependency_real_minimal_controlled_execution_final_ready_check_v1"

UPSTREAM_AUTH_DECISION_FINAL = UPSTREAM_AUTH_DECISION_FINAL_GO
UPSTREAM_MINIMAL_DRYRUN_FINAL = UPSTREAM_MINIMAL_DRYRUN_FINAL_GO
UPSTREAM_PREFLIGHT_FINAL = UPSTREAM_PREFLIGHT_FINAL_GO

FINAL_DECISION_GO = (
    "OCR_REAL_DEPENDENCY_REAL_MINIMAL_CONTROLLED_EXECUTION_FINAL_READY_CHECK_"
    "CLOSED_READY_FOR_REAL_EXECUTION"
)
FINAL_DECISION_HOLD = (
    "OCR_REAL_DEPENDENCY_REAL_MINIMAL_CONTROLLED_EXECUTION_FINAL_READY_CHECK_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = "Phase-OCR-Real-Dependency-Real-Minimal-Controlled-Execution-v1-001"
NEXT_PHASE_HOLD = "Phase-OCR-Real-Dependency-Real-Minimal-Controlled-Execution-Final-Ready-Check-Issue-Review-v1-001"

FORBIDDEN_READY_CHECK: Tuple[str, ...] = (
    "install",
    "download",
    "cache_mutation",
    "runtime_smoke",
    "sample_ocr",
    "OCRRequest",
    "image_read",
    "crop",
    "fact_write",
    "user_output",
    "memory_write",
    "world_model_write",
    "provider_finalize",
    "controlled_trial",
    "production_runtime",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Final Ready Check GO ≠ real execution started",
    "next phase is the first phase allowed to execute the 5 checks",
    "smoke/sample OCR still forbidden",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "real_execution_started_now",
    "execution_window_opened_now",
    "owner_confirmation_collected_now",
    "package_check_executed_now",
    "provider_import_check_executed_now",
    "provider_imported_now",
    "provider_invoked_now",
    "dependency_install_executed_now",
    "model_download_executed_now",
    "cache_mutation_executed_now",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_real_dependency_real_minimal_controlled_execution_final_ready_check"
)


def _ready_meta() -> Dict[str, Any]:
    meta = {
        "final_ready_check_only": True,
        "compressed_short_chain": True,
        "skipped_real_planning_dryrun_repeat": True,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "selected_provider_for_execution": None,
        "execution_scope": "minimal_real_dependency_check",
        "sandbox_required": True,
        "evidence_required": True,
        "rollback_required": True,
        "post_execution_review_required": True,
        "owner_operator_confirmation_required": True,
    }
    for field in BOUNDARY_FALSE:
        meta[field] = False
    return meta


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def run_ocr_real_dependency_real_minimal_controlled_execution_final_ready_check_v1(
    *,
    ocr_real_dependency_real_minimal_execution_authorization_decision_root: str,
    ocr_real_dependency_minimal_controlled_execution_dryrun_and_review_root: str,
    ocr_real_dependency_execution_final_preflight_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    auth_root = Path(
        ocr_real_dependency_real_minimal_execution_authorization_decision_root
    ).expanduser().resolve()
    dryrun_root = Path(
        ocr_real_dependency_minimal_controlled_execution_dryrun_and_review_root
    ).expanduser().resolve()
    preflight_root = Path(
        ocr_real_dependency_execution_final_preflight_root
    ).expanduser().resolve()

    auth_sm = _try_read_json(auth_root / "summary.json") or {}
    auth_vr = _try_read_json(auth_root / "verifier_report.json") or {}
    dryrun_sm = _try_read_json(dryrun_root / "summary.json") or {}
    dryrun_vr = _try_read_json(dryrun_root / "verifier_report.json") or {}
    preflight_sm = _try_read_json(preflight_root / "summary.json") or {}
    preflight_vr = _try_read_json(preflight_root / "verifier_report.json") or {}

    plan_cand = _try_read_json(
        dryrun_root / "minimal_controlled_execution_plan_candidate_v1.json"
    ) or {}
    allowed_review = _try_read_json(
        dryrun_root / "minimal_allowed_check_plan_dryrun_review_v1.json"
    ) or {}
    forbidden_review = _try_read_json(
        dryrun_root / "minimal_forbidden_action_dryrun_review_v1.json"
    ) or {}
    evidence_review = _try_read_json(
        dryrun_root / "minimal_evidence_output_dryrun_review_v1.json"
    ) or {}
    failure_review = _try_read_json(
        dryrun_root / "minimal_failure_route_dryrun_review_v1.json"
    ) or {}
    rollback_review = _try_read_json(dryrun_root / "minimal_rollback_dryrun_review_v1.json") or {}
    post_review = _try_read_json(
        dryrun_root / "minimal_post_execution_review_dryrun_review_v1.json"
    ) or {}
    window_review = _try_read_json(
        dryrun_root / "minimal_execution_window_candidate_review_v1.json"
    ) or {}
    sandbox_review = _try_read_json(dryrun_root / "minimal_execution_sandbox_review_v1.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_ready_meta(),
        "upstream_authorization_decision_root": str(auth_root),
        "upstream_minimal_dryrun_root": str(dryrun_root),
        "upstream_final_preflight_root": str(preflight_root),
        "output_root": str(out_root),
        "allowed_checks": list(MINIMAL_SCOPE_ALLOWED_CHECKS),
        "forbidden": list(FORBIDDEN_READY_CHECK),
    }

    if auth_vr.get("verifier") != "GO":
        blockers.append("authorization decision verifier must be GO")
    if auth_sm.get("final_decision") != UPSTREAM_AUTH_DECISION_FINAL:
        blockers.append("authorization decision final_decision mismatch")
    if auth_sm.get("selected_route") != UPSTREAM_SELECTED_ROUTE:
        blockers.append("selected_route must be Route A")
    if dryrun_vr.get("verifier") != "GO":
        blockers.append("minimal dryrun verifier must be GO")
    if dryrun_sm.get("final_decision") != UPSTREAM_MINIMAL_DRYRUN_FINAL:
        blockers.append("minimal dryrun final_decision mismatch")
    if preflight_vr.get("verifier") != "GO":
        blockers.append("final preflight verifier must be GO")
    if preflight_sm.get("final_decision") != UPSTREAM_PREFLIGHT_FINAL:
        blockers.append("final preflight final_decision mismatch")
    if not plan_cand.get("plan_candidate_id"):
        blockers.append("plan_candidate required")
    if plan_cand.get("allowed_checks_count") != 5:
        blockers.append("5 allowed checks must be locked")
    if allowed_review.get("dryrun_and_review_pass") is not True:
        blockers.append("allowed check review must pass")
    if forbidden_review.get("dryrun_and_review_pass") is not True:
        blockers.append("forbidden action review must pass")
    if evidence_review.get("dryrun_and_review_pass") is not True:
        blockers.append("evidence review must pass")
    if failure_review.get("dryrun_and_review_pass") is not True:
        blockers.append("failure route review must pass")
    if rollback_review.get("dryrun_and_review_pass") is not True:
        blockers.append("rollback review must pass")
    if post_review.get("dryrun_and_review_pass") is not True:
        blockers.append("post-review review must pass")
    if sandbox_review.get("dryrun_and_review_pass") is not True:
        blockers.append("sandbox review must pass")
    if meta.get("selected_provider_for_execution") is not None:
        blockers.append("selected_provider_for_execution must be null")

    for item in allowed_review.get("check_plan_items") or []:
        if item.get("current_executed_now") is True:
            blockers.append("allowed checks must not be executed yet")
            break

    input_ok = len(blockers) == 0

    upstream_input = {
        "review_id": "upstream_input_review_v1",
        "authorization_decision_go": auth_vr.get("verifier") == "GO",
        "minimal_dryrun_go": dryrun_vr.get("verifier") == "GO",
        "final_preflight_go": preflight_vr.get("verifier") == "GO",
        "selected_route": auth_sm.get("selected_route"),
        "review_pass": input_ok,
        "blockers": blockers,
        **meta,
    }

    scope_lock_checks = {
        "execution_scope": meta.get("execution_scope") == "minimal_real_dependency_check",
        "allowed_checks_locked": list(MINIMAL_SCOPE_ALLOWED_CHECKS),
        "allowed_count_5": len(MINIMAL_SCOPE_ALLOWED_CHECKS) == 5,
        "forbidden_locked": list(FORBIDDEN_READY_CHECK),
        "forbidden_full_18_upstream": forbidden_review.get("forbidden_count") == len(
            MINIMAL_FORBIDDEN_ACTIONS
        ),
        "evidence_locked": evidence_review.get("evidence_count") == len(EVIDENCE_OUTPUT_ITEMS),
        "failure_routes_locked": failure_review.get("dryrun_and_review_pass") is True,
        "rollback_locked": rollback_review.get("dryrun_and_review_pass") is True,
        "post_review_locked": post_review.get("dryrun_and_review_pass") is True,
        "sandbox_confirmed": sandbox_review.get("dryrun_and_review_pass") is True,
        "output_path_confirmed": bool(window_review.get("execution_window_candidate_id")),
        "owner_confirmation_required": True,
        "no_smoke_sample_ocr": True,
        "no_provider_finalize": meta.get("selected_provider_for_execution") is None,
    }
    scope_lock_review = {
        "review_id": "minimal_execution_scope_lock_review_v1",
        "scope_lock_checks": scope_lock_checks,
        "scope_lock_pass": input_ok and all(
            v is True or isinstance(v, list) for v in scope_lock_checks.values()
        ),
        "upstream_evidence_items": list(EVIDENCE_OUTPUT_ITEMS),
        "upstream_failure_route_count": len(FAILURE_ROUTES),
        **meta,
    }

    all_pass = (
        input_ok
        and upstream_input.get("review_pass") is True
        and scope_lock_review.get("scope_lock_pass") is True
    )

    ready_result = {
        "result_id": "final_ready_check_result_v1",
        "ready_check_pass": all_pass,
        "high_risk": not all_pass,
        "final_decision": FINAL_DECISION_GO if all_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if all_pass else NEXT_PHASE_HOLD,
        "ready_for_real_execution": all_pass,
        "owner_operator_confirmation_required_before_execution": True,
        "owner_confirmation_collected_now": False,
        **meta,
    }

    policy = {
        "policy_id": "final_ready_check_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "short_chain": [
            "Phase-OCR-Real-Dependency-Real-Minimal-Controlled-Execution-Final-Ready-Check-v1-001",
            "Phase-OCR-Real-Dependency-Real-Minimal-Controlled-Execution-v1-001",
            "Phase-OCR-Real-Dependency-Real-Minimal-Controlled-Execution-Post-Review-v1-001",
        ],
        "cancelled_phases": [
            "Phase-OCR-Real-Dependency-Real-Minimal-Controlled-Execution-Planning-v1-001",
            "Phase-OCR-Real-Dependency-Real-Minimal-Controlled-Execution-DryRunAndReview-v1-001",
        ],
        **meta,
    }

    non_claims = {
        "register_id": "non_claims_register_v1",
        "non_claims": list(NON_CLAIMS),
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "boundary_ok": all_pass,
        "violations": blockers,
        "ready_check_pass": all_pass,
        "final_decision": ready_result["final_decision"],
        "recommended_next_phase": ready_result["recommended_next_phase"],
        **meta,
    }

    return {
        "final_ready_check_policy": policy,
        "upstream_input_review": upstream_input,
        "minimal_execution_scope_lock_review": scope_lock_review,
        "final_ready_check_result": ready_result,
        "non_claims_register": non_claims,
        "summary": summary,
    }
