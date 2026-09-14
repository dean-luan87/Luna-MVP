# -*- coding: utf-8 -*-
"""OCR Provider Authorization Return Roadmap Decision v1 — Route A authorization planning selected."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.controlled_provider_readiness_harness_factory_registration_dryrun_v1 import (
    NEW_FACTORY_MODULE_ID,
)
from capabilities.governance.controlled_provider_readiness_harness_factory_registration_planning_v1 import (
    EXISTING_FACTORY_MODULE_COUNT,
    FUTURE_CONSUMER_DOMAINS,
    NEW_FACTORY_MODULE_DISPLAY,
)
from capabilities.governance.controlled_provider_readiness_harness_factory_registration_post_dryrun_review_v1 import (
    FINAL_DECISION_GO as FACTORY_POST_FINAL_GO,
    NEXT_PHASE_GO as FACTORY_POST_NEXT_PHASE,
)
from capabilities.governance.controlled_provider_readiness_harness_v1 import HARNESS_ID
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.provider_harness_generalization_roadmap_decision_v1 import SELECTED_ROUTE as HARNESS_ROUTE_B

PHASE_ID = "Phase-OCR-Provider-Authorization-Return-Roadmap-Decision-v1-001"
SCOPE = "ocr_provider_authorization_return_roadmap_decision_only"
SOURCE_CHAIN = "ocr_provider_authorization_return_roadmap_decision_v1"

UPSTREAM_FACTORY_POST_FINAL = FACTORY_POST_FINAL_GO
UPSTREAM_FACTORY_POST_NEXT = FACTORY_POST_NEXT_PHASE

FINAL_DECISION_GO = "OCR_PROVIDER_AUTHORIZATION_RETURN_ROADMAP_DECISION_READY_FOR_AUTHORIZATION_PLANNING"
FINAL_DECISION_HOLD = "OCR_PROVIDER_AUTHORIZATION_RETURN_ROADMAP_DECISION_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-OCR-Provider-Authorization-Planning-v1-001"
NEXT_PHASE_HOLD = "Phase-OCR-Provider-Authorization-Return-Issue-Review-v1-001"

ROUTE_A = "Route A — OCR Provider Authorization Planning"
ROUTE_B = "Route B — Real Dependency Check Authorization"
ROUTE_C = "Route C — Provider Selection Finalize"
ROUTE_D = "Route D — Return to Visual Context Governance"

SELECTED_ROUTE = ROUTE_A
DEFERRED_ROUTE_B = "Real Dependency Check Authorization"
DEFERRED_ROUTE_C = "Provider Selection Finalize"
DEFERRED_ROUTE_D = "Visual Context Governance"

BOUNDARY_FALSE: Tuple[str, ...] = (
    "ocr_authorization_planning_started_now",
    "real_dependency_check_authorization_started_now",
    "provider_authorization_granted_now",
    "provider_selection_finalized_now",
    "provider_runtime_enabled_now",
    "provider_imported_now",
    "provider_invoked_now",
    "dependency_install_executed_now",
    "model_download_executed_now",
    "real_dependency_check_executed_now",
    "controlled_trial_started_now",
    "ocr_request_submitted_now",
    "image_read_executed_now",
    "crop_executed_now",
    "ocr_fact_generated_now",
    "user_facing_output_generated_now",
    "memory_written_now",
    "world_model_written_now",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Roadmap Decision GO ≠ OCR provider authorization granted",
    "Route A selected ≠ real dependency check executed",
    "Route A selected ≠ provider import/install/download",
    "authorization planning next ≠ selected_provider_for_execution set",
    "deferred Route B ≠ real dependency check abandoned",
    "factory registration closure ≠ Validation Factory runtime enforced",
    "OCR return ready ≠ Vision/Voice provider runtime enabled",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/ocr_provider_authorization_return_roadmap_decision"
)


def _boundary_meta() -> Dict[str, Any]:
    meta = {
        "ocr_provider_authorization_return_roadmap_decision_only": True,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "harness_id": HARNESS_ID,
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


def run_ocr_provider_authorization_return_roadmap_decision_v1(
    *,
    controlled_provider_readiness_harness_factory_registration_post_dryrun_review_root: str,
    controlled_provider_readiness_harness_factory_registration_dryrun_root: Optional[str] = None,
    provider_harness_generalization_roadmap_decision_root: Optional[str] = None,
    ocr_provider_real_dependency_check_post_dryrun_review_root: Optional[str] = None,
    ocr_provider_selection_dependency_environment_post_dryrun_review_root: Optional[str] = None,
    ocr_controlled_provider_post_dryrun_review_root: Optional[str] = None,
    controlled_provider_readiness_harness_root: Optional[str] = None,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    factory_post_root = Path(
        controlled_provider_readiness_harness_factory_registration_post_dryrun_review_root
    ).expanduser().resolve()
    factory_post_sm = _try_read_json(factory_post_root / "summary.json") or {}
    factory_post_vr = _try_read_json(factory_post_root / "verifier_report.json") or {}
    closure = _try_read_json(factory_post_root / "factory_registration_closure_decision_v1.json") or {}

    dryrun_root = Path(
        controlled_provider_readiness_harness_factory_registration_dryrun_root
        or factory_post_root.parent / "controlled_provider_readiness_harness_factory_registration_dryrun"
    ).expanduser().resolve()
    dryrun_sm = _try_read_json(dryrun_root / "summary.json") or {}
    dryrun_vr = _try_read_json(dryrun_root / "verifier_report.json") or {}
    registry = _try_read_json(dryrun_root / "validation_factory_registry_candidate_v1.json") or {}

    roadmap_root = Path(
        provider_harness_generalization_roadmap_decision_root
        or factory_post_root.parent / "provider_harness_generalization_roadmap_decision"
    ).expanduser().resolve()
    roadmap_sm = _try_read_json(roadmap_root / "summary.json") or {}

    harness_root = Path(
        controlled_provider_readiness_harness_root
        or factory_post_root.parent / "controlled_provider_readiness_harness"
    ).expanduser().resolve()
    validation = _try_read_json(
        harness_root / "controlled_provider_readiness_harness_validation_result_v1.json"
    ) or {}

    real_post_root = Path(
        ocr_provider_real_dependency_check_post_dryrun_review_root
        or factory_post_root.parent / "ocr_provider_real_dependency_check_post_dryrun_review"
    ).expanduser().resolve()
    sel_post_root = Path(
        ocr_provider_selection_dependency_environment_post_dryrun_review_root
        or factory_post_root.parent / "ocr_provider_selection_dependency_environment_post_dryrun_review"
    ).expanduser().resolve()
    ocr_post_root = Path(
        ocr_controlled_provider_post_dryrun_review_root
        or factory_post_root.parent / "ocr_controlled_provider_post_dryrun_review"
    ).expanduser().resolve()

    real_post_sm = _try_read_json(real_post_root / "summary.json") or {}
    real_post_vr = _try_read_json(real_post_root / "verifier_report.json") or {}
    sel_post_sm = _try_read_json(sel_post_root / "summary.json") or {}
    sel_post_vr = _try_read_json(sel_post_root / "verifier_report.json") or {}
    ocr_post_sm = _try_read_json(ocr_post_root / "summary.json") or {}
    ocr_post_vr = _try_read_json(ocr_post_root / "verifier_report.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_boundary_meta(),
        "upstream_factory_post_review_root": str(factory_post_root),
        "upstream_factory_dryrun_root": str(dryrun_root),
        "upstream_roadmap_root": str(roadmap_root),
        "upstream_harness_root": str(harness_root),
        "upstream_real_dep_post_root": str(real_post_root),
        "upstream_selection_post_root": str(sel_post_root),
        "upstream_ocr_controlled_post_root": str(ocr_post_root),
        "output_root": str(out_root),
    }

    factory_post_go = factory_post_vr.get("verifier") == "GO" and factory_post_vr.get("passed") is True
    if not factory_post_go:
        blockers.append("factory registration post-review verifier must be GO")
    if factory_post_sm.get("final_decision") != UPSTREAM_FACTORY_POST_FINAL:
        blockers.append("factory post-review final_decision mismatch")
    if factory_post_sm.get("recommended_next_phase") != UPSTREAM_FACTORY_POST_NEXT:
        blockers.append("factory post-review recommended_next_phase mismatch")
    if closure.get("factory_registration_dryrun_closed") is not True:
        blockers.append("factory registration dryrun must be closed")
    if closure.get("ready_for_ocr_provider_authorization_return") is not True:
        blockers.append("not ready for OCR authorization return")

    if dryrun_vr.get("verifier") != "GO":
        blockers.append("factory registration dryrun should be GO")
    if dryrun_sm.get("validation_factory_registry_candidate_generated_now") is not True:
        blockers.append("validation_factory_registry_candidate_generated_now must be true")
    if dryrun_sm.get("validation_factory_registry_updated_now") is True:
        blockers.append("validation_factory_registry_updated_now must be false")
    if registry.get("module_count") != EXISTING_FACTORY_MODULE_COUNT + 1:
        blockers.append("registry candidate must have 7 modules")
    if registry.get("proposed_seventh_module_id") != NEW_FACTORY_MODULE_ID:
        blockers.append("seventh module must be controlled_provider_readiness_harness_v1")

    if validation.get("ocr_first_consumer_validated") is not True:
        blockers.append("OCR first consumer must be validated")
    if dryrun_sm.get("three_consumer_validated") is not True:
        blockers.append("Vision/Voice consumers must be validated")

    if roadmap_sm.get("selected_route") != HARNESS_ROUTE_B:
        blockers.append("harness generalization should have selected Route B")

    for vr, label in (
        (real_post_vr, "real dependency check post-review"),
        (sel_post_vr, "selection/dependency/environment post-review"),
        (ocr_post_vr, "controlled provider post-review"),
    ):
        if vr.get("verifier") != "GO":
            blockers.append(f"{label} verifier must be GO")

    if real_post_sm.get("ocr_provider_real_dependency_check_dryrun_closed") is not True:
        blockers.append("OCR real dependency dryrun should be closed")
    if sel_post_sm.get("ocr_provider_selection_dependency_environment_dryrun_closed") is not True:
        blockers.append("OCR selection dryrun should be closed")
    if ocr_post_sm.get("ocr_controlled_provider_dryrun_closed") is not True:
        blockers.append("OCR controlled provider dryrun should be closed")

    for sm in (real_post_sm, sel_post_sm, ocr_post_sm, dryrun_sm, factory_post_sm):
        for field in (
            "provider_imported_now",
            "provider_invoked_now",
            "dependency_install_executed_now",
            "model_download_executed_now",
        ):
            if sm.get(field) is True:
                blockers.append(f"{field} must be false across chain")

    if dryrun_sm.get("map_library_hive_memory_adoption_started_now") is True:
        blockers.append("Map/Library/Hive/Memory must remain future only")

    input_review = {
        "review_id": "factory_registration_post_review_input_review_v1",
        "upstream_factory_post_root": str(factory_post_root),
        "upstream_factory_dryrun_root": str(dryrun_root),
        "upstream_verifier_go": factory_post_go,
        "upstream_final_decision": factory_post_sm.get("final_decision"),
        "registry_candidate_module_count": registry.get("module_count"),
        "seventh_module_id": registry.get("proposed_seventh_module_id"),
        "review_pass": len(blockers) == 0,
        "blockers": blockers,
        **meta,
    }

    chain_review = {
        "review_id": "ocr_provider_chain_readiness_review_v1",
        "ocr_controlled_provider_dryrun_closed": ocr_post_sm.get("ocr_controlled_provider_dryrun_closed"),
        "ocr_selection_dependency_environment_dryrun_closed": sel_post_sm.get(
            "ocr_provider_selection_dependency_environment_dryrun_closed"
        ),
        "ocr_real_dependency_check_dryrun_closed": real_post_sm.get(
            "ocr_provider_real_dependency_check_dryrun_closed"
        ),
        "harness_seventh_module_candidate": NEW_FACTORY_MODULE_DISPLAY,
        "ocr_first_consumer_validated": validation.get("ocr_first_consumer_validated"),
        "vision_voice_validated": dryrun_sm.get("three_consumer_validated"),
        "future_consumers_deferred": list(FUTURE_CONSUMER_DOMAINS),
        "selected_provider_for_execution": None,
        "chain_readiness_pass": len(blockers) == 0,
        **meta,
    }

    route_a = {
        "assessment_id": "route_a_ocr_provider_authorization_planning_assessment_v1",
        "route_id": "A",
        "route_label": ROUTE_A,
        "status": "selected",
        "selection_reasons": [
            "OCR controlled provider planning/dryrun/post-review closed",
            "OCR provider selection/dependency/environment planning/dryrun/post-review closed",
            "OCR real dependency check planning/dryrun/post-review closed",
            "ControlledProviderReadinessHarness extracted and validated with OCR/Vision/Voice",
            "Harness registered as Validation Factory 7th module candidate",
            "May enter authorization planning — still no grant, no execute",
        ],
        "planning_scope": [
            "authorization_request_plan",
            "grant_plan",
            "execution_window_plan",
            "sandbox_plan",
            "rollback_plan",
            "evidence_pack_plan",
        ],
        **meta,
    }

    route_b = {
        "assessment_id": "route_b_real_dependency_check_authorization_assessment_v1",
        "route_id": "B",
        "route_label": ROUTE_B,
        "status": "deferred_after_authorization_planning",
        "defer_reasons": [
            "Real dependency check requires explicit authorization request/grant/execution window/sandbox",
            "Cannot enter real check authorization directly from roadmap",
        ],
        **meta,
    }

    route_c = {
        "assessment_id": "route_c_provider_selection_finalize_assessment_v1",
        "route_id": "C",
        "route_label": ROUTE_C,
        "status": "deferred",
        "defer_reasons": [
            "Provider selection finalize belongs after authorization planning",
            "selected_provider_for_execution must remain null",
        ],
        **meta,
    }

    route_d = {
        "assessment_id": "route_d_return_to_visual_context_governance_assessment_v1",
        "route_id": "D",
        "route_label": ROUTE_D,
        "status": "deferred",
        "defer_reasons": [
            "Visual Context Governance remains important",
            "OCR authorization return is ready — complete authorization planning first",
        ],
        **meta,
    }

    selection_matrix = {
        "matrix_id": "ocr_authorization_return_route_selection_matrix_v1",
        "routes": [
            {"route": ROUTE_A, "status": "selected"},
            {"route": ROUTE_B, "status": "deferred_after_authorization_planning"},
            {"route": ROUTE_C, "status": "deferred"},
            {"route": ROUTE_D, "status": "deferred"},
        ],
        "selected_route": SELECTED_ROUTE,
        "deferred_route_b": DEFERRED_ROUTE_B,
        "deferred_route_c": DEFERRED_ROUTE_C,
        "deferred_route_d": DEFERRED_ROUTE_D,
        **meta,
    }

    preconditions = {
        "preconditions_id": "selected_route_preconditions_v1",
        "selected_route": SELECTED_ROUTE,
        "preconditions": [
            "factory registration post-dryrun review GO",
            "validation_factory_registry_candidate trusted (7 modules)",
            "OCR/Vision/Voice three-consumer harness validated",
            "OCR controlled/selection/real-dep post-reviews GO",
            "no provider import/install/download/invoke",
            "selected_provider_for_execution=null",
        ],
        "forbidden_now": [
            "provider authorization grant",
            "real dependency check execution",
            "provider import/install/download/invoke",
            "provider selection finalize",
            "controlled trial start",
        ],
        **meta,
    }

    deferred_register = {
        "register_id": "deferred_routes_register_v1",
        "deferred_items": [
            {
                "route": DEFERRED_ROUTE_B,
                "status": "deferred_after_authorization_planning",
                "resume_after": "ocr_provider_authorization_planning",
            },
            {
                "route": DEFERRED_ROUTE_C,
                "status": "deferred",
                "note": "selection finalize after authorization flow",
            },
            {
                "route": DEFERRED_ROUTE_D,
                "status": "deferred",
                "resume_after": "ocr_authorization_planning_closure",
            },
        ],
        **meta,
    }

    decision_ok = len(blockers) == 0
    boundary_ok = decision_ok

    next_readiness = {
        "readiness_id": "next_phase_readiness_decision_v1",
        "ready_for_ocr_provider_authorization_planning": boundary_ok,
        "selected_route": SELECTED_ROUTE,
        "do_not_grant_authorization_now": True,
        "do_not_execute_real_dependency_check_now": True,
        "do_not_finalize_provider_selection_now": True,
        "do_not_import_install_invoke_now": True,
        "recommended_next_phase": NEXT_PHASE_GO if boundary_ok else PHASE_ID,
        "final_decision": FINAL_DECISION_GO if boundary_ok else FINAL_DECISION_HOLD,
        **meta,
    }

    policy = {
        "policy_id": "ocr_authorization_return_roadmap_policy_v1",
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
        "deferred_route_c": DEFERRED_ROUTE_C,
        "deferred_route_d": DEFERRED_ROUTE_D,
        "high_risk_count": 0 if boundary_ok else 1,
        **meta,
    }

    return {
        "ocr_authorization_return_roadmap_policy": policy,
        "factory_registration_post_review_input_review": input_review,
        "ocr_provider_chain_readiness_review": chain_review,
        "route_a_ocr_provider_authorization_planning_assessment": route_a,
        "route_b_real_dependency_check_authorization_assessment": route_b,
        "route_c_provider_selection_finalize_assessment": route_c,
        "route_d_return_to_visual_context_governance_assessment": route_d,
        "ocr_authorization_return_route_selection_matrix": selection_matrix,
        "selected_route_preconditions": preconditions,
        "deferred_routes_register": deferred_register,
        "next_phase_readiness_decision": next_readiness,
        "non_claims_register": non_claims,
        "summary": summary,
    }
