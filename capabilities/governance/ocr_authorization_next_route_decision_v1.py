# -*- coding: utf-8 -*-
"""OCR Authorization Next Route Decision v1 — Route A real-dep authorization selected."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.capability_factory_admission_and_operation_standard_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as FACTORY_DRYRUN_REVIEW_FINAL_GO,
)
from capabilities.governance.capability_factory_admission_and_operation_standard_planning_v1 import (
    STANDARD_ID,
)
from capabilities.governance.compressed_ocr_authorization_lifecycle_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as LIFECYCLE_DR_FINAL_GO,
)
from capabilities.governance.factory_standard_historical_redundancy_cleanup_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as CLEANUP_DR_FINAL_GO,
    NEXT_PHASE_GO as CLEANUP_DR_NEXT_PHASE,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.ocr_provider_real_dependency_check_post_dryrun_review_v1 import (
    FINAL_DECISION_GO as REAL_DEP_POST_FINAL_GO,
)
from capabilities.governance.ocr_provider_selection_dependency_environment_post_dryrun_review_v1 import (
    FINAL_DECISION_GO as SELECTION_POST_FINAL_GO,
)

PHASE_ID = "Phase-OCR-Authorization-Next-Route-Decision-v1-001"
SCOPE = "ocr_authorization_next_route_decision_only"
SOURCE_CHAIN = "ocr_authorization_next_route_decision_v1"

UPSTREAM_CLEANUP_DR_FINAL = CLEANUP_DR_FINAL_GO
UPSTREAM_CLEANUP_DR_NEXT = CLEANUP_DR_NEXT_PHASE

FINAL_DECISION_GO = (
    "OCR_AUTHORIZATION_NEXT_ROUTE_DECISION_READY_FOR_REAL_DEPENDENCY_CHECK_AUTHORIZATION_PLANNING"
)
FINAL_DECISION_HOLD = "OCR_AUTHORIZATION_NEXT_ROUTE_DECISION_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-OCR-Provider-Real-Dependency-Check-Authorization-Planning-v1-001"
NEXT_PHASE_HOLD = "Phase-OCR-Authorization-Next-Route-Issue-Review-v1-001"

ROUTE_A = "Route A — Real Dependency Check Authorization Planning"
ROUTE_B = "Route B — Provider Selection Finalize Planning"
ROUTE_C = "Route C — Controlled Trial Authorization Planning"
ROUTE_D = "Route D — Return to Vision / Voice / Visual Context Governance"

SELECTED_ROUTE = ROUTE_A
DEFERRED_ROUTE_B = "Provider Selection Finalize Planning"
BLOCKED_ROUTE_C = "Controlled Trial Authorization Planning"
DEFERRED_ROUTE_D = "Return to Vision / Voice / Visual Context Governance"

NON_CLAIMS: Tuple[str, ...] = (
    "Next Route Decision GO ≠ real dependency check authorized",
    "Route A selected ≠ real dependency check executed",
    "provider readiness ≠ provider selected",
    "cleanup closed ≠ historical files deleted",
    "compressed lifecycle closed ≠ provider authorization granted",
    "real dependency authorization planning ≠ provider import allowed",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "real_dependency_check_authorization_started_now",
    "provider_selection_finalize_started_now",
    "controlled_trial_authorization_started_now",
    "visual_context_governance_started_now",
    "real_dependency_check_executed_now",
    "provider_selection_finalized_now",
    "provider_imported_now",
    "provider_invoked_now",
    "dependency_install_executed_now",
    "model_download_executed_now",
    "provider_smoke_check_executed_now",
    "sample_ocr_executed_now",
    "controlled_trial_started_now",
    "ocr_request_submitted_now",
    "image_read_executed_now",
    "crop_executed_now",
    "ocr_fact_generated_now",
    "user_facing_output_generated_now",
    "memory_written_now",
    "world_model_written_now",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/ocr_authorization_next_route_decision"
)


def _decision_meta() -> Dict[str, Any]:
    meta = {
        "ocr_authorization_next_route_decision_only": True,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "standard_id": STANDARD_ID,
        "selected_provider_for_execution": None,
    }
    for field in BOUNDARY_FALSE:
        meta[field] = False
    meta["provider_selection_finalized_now"] = False
    meta["selected_provider_for_execution"] = None
    return meta


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def run_ocr_authorization_next_route_decision_v1(
    *,
    factory_standard_historical_redundancy_cleanup_dryrun_and_review_root: str,
    compressed_ocr_authorization_lifecycle_dryrun_and_review_root: Optional[str] = None,
    capability_factory_admission_and_operation_standard_dryrun_and_review_root: Optional[str] = None,
    controlled_provider_readiness_harness_factory_registration_post_dryrun_review_root: Optional[str] = None,
    ocr_provider_real_dependency_check_post_dryrun_review_root: Optional[str] = None,
    ocr_provider_selection_dependency_environment_post_dryrun_review_root: Optional[str] = None,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    cleanup_dr_root = Path(
        factory_standard_historical_redundancy_cleanup_dryrun_and_review_root
    ).expanduser().resolve()
    cleanup_dr_sm = _try_read_json(cleanup_dr_root / "summary.json") or {}
    cleanup_dr_vr = _try_read_json(cleanup_dr_root / "verifier_report.json") or {}
    cleanup_closure = _try_read_json(cleanup_dr_root / "cleanup_dryrun_and_review_closure_decision_v1.json") or {}

    lifecycle_dr_root = Path(
        compressed_ocr_authorization_lifecycle_dryrun_and_review_root
        or cleanup_dr_root.parent / "compressed_ocr_authorization_lifecycle_dryrun_and_review"
    ).expanduser().resolve()
    lifecycle_dr_sm = _try_read_json(lifecycle_dr_root / "summary.json") or {}
    lifecycle_dr_vr = _try_read_json(lifecycle_dr_root / "verifier_report.json") or {}
    lifecycle_closure = _try_read_json(lifecycle_dr_root / "compressed_lifecycle_closure_decision_v1.json") or {}

    factory_dr_root = Path(
        capability_factory_admission_and_operation_standard_dryrun_and_review_root
        or cleanup_dr_root.parent / "capability_factory_admission_and_operation_standard_dryrun_and_review"
    ).expanduser().resolve()
    factory_dr_sm = _try_read_json(factory_dr_root / "summary.json") or {}
    factory_dr_vr = _try_read_json(factory_dr_root / "verifier_report.json") or {}

    factory_post_root = Path(
        controlled_provider_readiness_harness_factory_registration_post_dryrun_review_root
        or cleanup_dr_root.parent
        / "controlled_provider_readiness_harness_factory_registration_post_dryrun_review"
    ).expanduser().resolve()
    factory_post_vr = _try_read_json(factory_post_root / "verifier_report.json") or {}

    real_dep_post_root = Path(
        ocr_provider_real_dependency_check_post_dryrun_review_root
        or cleanup_dr_root.parent / "ocr_provider_real_dependency_check_post_dryrun_review"
    ).expanduser().resolve()
    real_dep_post_sm = _try_read_json(real_dep_post_root / "summary.json") or {}
    real_dep_post_vr = _try_read_json(real_dep_post_root / "verifier_report.json") or {}

    selection_post_root = Path(
        ocr_provider_selection_dependency_environment_post_dryrun_review_root
        or cleanup_dr_root.parent / "ocr_provider_selection_dependency_environment_post_dryrun_review"
    ).expanduser().resolve()
    selection_post_sm = _try_read_json(selection_post_root / "summary.json") or {}
    selection_post_vr = _try_read_json(selection_post_root / "verifier_report.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_decision_meta(),
        "upstream_cleanup_dryrun_review_root": str(cleanup_dr_root),
        "upstream_lifecycle_dryrun_review_root": str(lifecycle_dr_root),
        "upstream_factory_dryrun_review_root": str(factory_dr_root),
        "upstream_factory_post_review_root": str(factory_post_root),
        "upstream_real_dep_post_root": str(real_dep_post_root),
        "upstream_selection_post_root": str(selection_post_root),
        "output_root": str(out_root),
    }

    if cleanup_dr_vr.get("verifier") != "GO" or cleanup_dr_vr.get("passed") is not True:
        blockers.append("cleanup dryrun and review verifier must be GO")
    if cleanup_dr_sm.get("final_decision") != UPSTREAM_CLEANUP_DR_FINAL:
        blockers.append("cleanup dryrun final_decision mismatch")
    if cleanup_dr_sm.get("recommended_next_phase") != UPSTREAM_CLEANUP_DR_NEXT:
        blockers.append("cleanup dryrun recommended_next_phase mismatch")
    if cleanup_dr_sm.get("marking_only") is not True:
        blockers.append("cleanup marking_only must be true")
    if cleanup_closure.get("closure_pass") is not True:
        blockers.append("cleanup closure must pass")
    if cleanup_dr_sm.get("historical_file_delete_executed_now") is True:
        blockers.append("no historical deletion must have occurred")
    if cleanup_dr_sm.get("historical_file_rewrite_executed_now") is True:
        blockers.append("no historical rewrite must have occurred")

    if lifecycle_dr_vr.get("verifier") != "GO":
        blockers.append("compressed lifecycle dryrun review must be GO")
    if lifecycle_dr_sm.get("final_decision") != LIFECYCLE_DR_FINAL_GO:
        blockers.append("compressed lifecycle must be closed")
    if lifecycle_closure.get("closure_pass") is not True:
        blockers.append("compressed lifecycle closure must pass")

    if factory_dr_vr.get("verifier") != "GO":
        blockers.append("factory standard dryrun review must be GO")
    if factory_dr_sm.get("final_decision") != FACTORY_DRYRUN_REVIEW_FINAL_GO:
        blockers.append("factory dryrun review final_decision mismatch")
    if factory_dr_sm.get("nine_standards_validated") is not True:
        blockers.append("nine_standards_validated must be true")

    if factory_post_vr.get("verifier") != "GO":
        blockers.append("harness factory registration post-review must be GO")

    if real_dep_post_vr.get("verifier") != "GO":
        blockers.append("real dependency check post-review must be GO")
    if real_dep_post_sm.get("final_decision") != REAL_DEP_POST_FINAL_GO:
        blockers.append("real dep post-review final_decision mismatch")
    if real_dep_post_sm.get("real_dependency_check_flow_trusted") is not True:
        blockers.append("real dependency check dryrun must be trusted")
    if real_dep_post_sm.get("real_dependency_check_executed_now") is True:
        blockers.append("real dependency check must not be executed")

    if selection_post_vr.get("verifier") != "GO":
        blockers.append("selection dependency environment post-review must be GO")
    if selection_post_sm.get("final_decision") != SELECTION_POST_FINAL_GO:
        blockers.append("selection post-review final_decision mismatch")
    if selection_post_sm.get("provider_selection_candidate_trusted") is not True:
        blockers.append("provider selection candidate must be trusted")

    if meta.get("selected_provider_for_execution") is not None:
        blockers.append("selected_provider_for_execution must be null")
    if meta.get("provider_selection_finalized_now") is True:
        blockers.append("provider_selection_finalized_now must be false")

    for field in BOUNDARY_FALSE:
        if cleanup_dr_sm.get(field) is True or lifecycle_dr_sm.get(field) is True:
            blockers.append(f"{field} must be false upstream")
        if real_dep_post_sm.get(field) is True or selection_post_sm.get(field) is True:
            blockers.append(f"{field} must be false in upstream reviews")

    decision_ok = len(blockers) == 0
    boundary_ok = decision_ok

    cleanup_input_review = {
        "review_id": "cleanup_dryrun_review_input_review_v1",
        "upstream_root": str(cleanup_dr_root),
        "upstream_verifier_go": cleanup_dr_vr.get("verifier") == "GO",
        "upstream_final_decision": cleanup_dr_sm.get("final_decision"),
        "marking_only": cleanup_dr_sm.get("marking_only"),
        "closure_pass": cleanup_closure.get("closure_pass"),
        "review_pass": decision_ok,
        "blockers": blockers,
        **meta,
    }

    lifecycle_readiness = {
        "review_id": "compressed_lifecycle_readiness_review_v1",
        "lifecycle_closed": lifecycle_closure.get("closure_pass") is True,
        "lifecycle_verifier_go": lifecycle_dr_vr.get("verifier") == "GO",
        "compressed_lifecycle_executed": False,
        "provider_authorization_granted": False,
        "readiness_pass": decision_ok,
        **meta,
    }

    readiness_state = {
        "review_id": "ocr_provider_readiness_state_review_v1",
        "selected_provider_for_execution": None,
        "provider_selection_finalized_now": False,
        "real_dependency_check_executed_now": False,
        "real_dependency_check_dryrun_trusted": real_dep_post_sm.get("real_dependency_check_flow_trusted"),
        "provider_selection_candidate_trusted": selection_post_sm.get("provider_selection_candidate_trusted"),
        "harness_factory_registration_go": factory_post_vr.get("verifier") == "GO",
        "missing_real_dependency_evidence": True,
        "readiness_pass": decision_ok,
        **meta,
    }

    route_a = {
        "assessment_id": "route_a_real_dependency_check_authorization_assessment_v1",
        "route_id": "A",
        "route_label": ROUTE_A,
        "status": "selected",
        "selection_reasons": [
            "OCR real dependency check planning/dryrun/post-review completed but real check not executed",
            "Real dependency evidence needed before provider selection finalize",
            "selected_provider_for_execution=null — should not finalize provider first",
            "Real dependency check requires standalone authorization",
            "Plan real dependency check authorization first — do not execute directly",
        ],
        **meta,
    }

    route_b = {
        "assessment_id": "route_b_provider_selection_finalize_assessment_v1",
        "route_id": "B",
        "route_label": ROUTE_B,
        "status": "deferred_after_real_dependency_check_evidence",
        "defer_reasons": [
            "Provider selection/dependency/environment candidate and comparison sample exist",
            "Missing real dependency check evidence",
            "Should not finalize provider without real dependency evidence",
        ],
        **meta,
    }

    route_c = {
        "assessment_id": "route_c_controlled_trial_authorization_assessment_v1",
        "route_id": "C",
        "route_label": ROUTE_C,
        "status": "blocked_until_provider_selection_and_real_dependency",
        "block_reasons": [
            "Controlled trial requires provider selection + real dependency evidence + authorization",
            "Cannot enter controlled trial directly now",
        ],
        **meta,
    }

    route_d = {
        "assessment_id": "route_d_return_visual_context_governance_assessment_v1",
        "route_id": "D",
        "route_label": ROUTE_D,
        "status": "deferred",
        "defer_reasons": [
            "Vision/Voice harness adoption completed",
            "Visual Context Governance important but OCR authorization mainline should complete real-dep authorization first",
        ],
        **meta,
    }

    selection_matrix = {
        "matrix_id": "ocr_authorization_next_route_selection_matrix_v1",
        "routes": [
            {"route": ROUTE_A, "status": "selected"},
            {"route": ROUTE_B, "status": "deferred_after_real_dependency_check_evidence"},
            {"route": ROUTE_C, "status": "blocked_until_provider_selection_and_real_dependency"},
            {"route": ROUTE_D, "status": "deferred"},
        ],
        "selected_route": SELECTED_ROUTE,
        "deferred_route_b": DEFERRED_ROUTE_B,
        "blocked_route_c": BLOCKED_ROUTE_C,
        "deferred_route_d": DEFERRED_ROUTE_D,
        **meta,
    }

    preconditions = {
        "preconditions_id": "selected_route_preconditions_v1",
        "selected_route": SELECTED_ROUTE,
        "preconditions": [
            "cleanup dryrun and review GO",
            "compressed lifecycle closed",
            "factory standard dryrun review GO",
            "harness factory registration GO",
            "real dependency check dryrun trusted",
            "provider selection candidate trusted",
            "selected_provider_for_execution=null",
            "provider_selection_finalized_now=false",
        ],
        "forbidden_now": [
            "real dependency check execution",
            "provider selection finalize",
            "controlled trial authorization",
            "provider import/invoke",
            "dependency install/model download",
        ],
        **meta,
    }

    deferred_register = {
        "register_id": "deferred_routes_register_v1",
        "deferred_items": [
            {
                "route": DEFERRED_ROUTE_B,
                "status": "deferred_after_real_dependency_check_evidence",
                "resume_after": "real_dependency_check_authorization_closure",
            },
            {
                "route": BLOCKED_ROUTE_C,
                "status": "blocked_until_provider_selection_and_real_dependency",
                "resume_after": "provider_selection_finalize_and_real_dep_evidence",
            },
            {
                "route": DEFERRED_ROUTE_D,
                "status": "deferred",
                "note": "Visual Context Governance after OCR authorization mainline milestones",
            },
        ],
        **meta,
    }

    next_readiness = {
        "readiness_id": "next_phase_readiness_decision_v1",
        "ready_for_real_dependency_check_authorization_planning": boundary_ok,
        "selected_route": SELECTED_ROUTE,
        "do_not_execute_real_dependency_check_now": True,
        "do_not_finalize_provider_now": True,
        "do_not_start_controlled_trial_now": True,
        "recommended_next_phase": NEXT_PHASE_GO if boundary_ok else PHASE_ID,
        "final_decision": FINAL_DECISION_GO if boundary_ok else FINAL_DECISION_HOLD,
        **meta,
    }

    policy = {
        "policy_id": "ocr_authorization_next_route_decision_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
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
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": next_readiness["final_decision"],
        "recommended_next_phase": next_readiness["recommended_next_phase"],
        "selected_route": SELECTED_ROUTE,
        "deferred_route_b": DEFERRED_ROUTE_B,
        "blocked_route_c": BLOCKED_ROUTE_C,
        "deferred_route_d": DEFERRED_ROUTE_D,
        "high_risk_count": 0 if boundary_ok else 1,
        **meta,
    }

    return {
        "ocr_authorization_next_route_decision_policy": policy,
        "cleanup_dryrun_review_input_review": cleanup_input_review,
        "compressed_lifecycle_readiness_review": lifecycle_readiness,
        "ocr_provider_readiness_state_review": readiness_state,
        "route_a_real_dependency_check_authorization_assessment": route_a,
        "route_b_provider_selection_finalize_assessment": route_b,
        "route_c_controlled_trial_authorization_assessment": route_c,
        "route_d_return_visual_context_governance_assessment": route_d,
        "ocr_authorization_next_route_selection_matrix": selection_matrix,
        "selected_route_preconditions": preconditions,
        "deferred_routes_register": deferred_register,
        "next_phase_readiness_decision": next_readiness,
        "non_claims_register": non_claims,
        "summary": summary,
    }
