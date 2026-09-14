# -*- coding: utf-8 -*-
"""OCR Controlled Provider Authorization Roadmap Decision v1 — Route B selected."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.ocr_controlled_provider_dryrun_v1 import BLOCKED_PATHS
from capabilities.governance.ocr_controlled_provider_post_dryrun_review_v1 import (
    FINAL_DECISION_GO as POST_REVIEW_FINAL_GO,
    NEXT_PHASE_GO as POST_REVIEW_NEXT_PHASE,
)

PHASE_ID = "Phase-OCR-Controlled-Provider-Authorization-Roadmap-Decision-v1-001"
SCOPE = "ocr_controlled_provider_authorization_roadmap_decision_only"
SOURCE_CHAIN = "ocr_controlled_provider_authorization_roadmap_decision_v1"

UPSTREAM_POST_REVIEW_FINAL = POST_REVIEW_FINAL_GO
UPSTREAM_POST_REVIEW_NEXT = POST_REVIEW_NEXT_PHASE

FINAL_DECISION_GO = (
    "OCR_CONTROLLED_PROVIDER_AUTHORIZATION_ROADMAP_DECISION_READY_FOR_PROVIDER_SELECTION_DEPENDENCY_ENVIRONMENT_PLANNING"
)
FINAL_DECISION_HOLD = "OCR_CONTROLLED_PROVIDER_AUTHORIZATION_ROADMAP_DECISION_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-OCR-Provider-Selection-Dependency-Environment-Planning-v1-001"
NEXT_PHASE_HOLD = "Phase-OCR-Controlled-Provider-Issue-Review-v1-001"

ROUTE_A = "Route A — OCR Provider Authorization Planning"
ROUTE_B = "Route B — OCR Provider Selection / Local Dependency / Environment Readiness Planning"
ROUTE_C = "Route C — OCR Controlled Trial Planning"
ROUTE_D = "Route D — Defer OCR Provider and return to Vision / Voice"

SELECTED_ROUTE = ROUTE_B
DEFERRED_ROUTE_A = ROUTE_A
BLOCKED_ROUTE_C = ROUTE_C
DEFERRED_ROUTE_D = ROUTE_D

BOUNDARY_FALSE: Tuple[str, ...] = (
    "provider_authorization_started_now",
    "provider_selection_started_now",
    "provider_dependency_check_started_now",
    "environment_readiness_check_started_now",
    "controlled_trial_started_now",
    "ocr_controlled_provider_enabled_now",
    "ocr_controlled_provider_invoked_now",
    "ocr_provider_invoked_now",
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
    "Roadmap Decision GO ≠ provider authorization enabled",
    "Route B selected ≠ PaddleOCR/RapidOCR invoked",
    "Route B selected ≠ OCRRequest submitted",
    "provider readiness candidate ≠ provider callable",
    "deferred Route A ≠ authorization abandoned forever",
    "blocked Route C ≠ trial abandoned forever",
    "provider selection planning next ≠ controlled trial allowed",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_controlled_provider_authorization_roadmap_decision"
)


def _boundary_meta() -> Dict[str, Any]:
    meta = {
        "ocr_controlled_provider_authorization_roadmap_decision_only": True,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
    }
    for field in BOUNDARY_FALSE:
        meta[field] = False
    return meta


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def run_ocr_controlled_provider_authorization_roadmap_decision_v1(
    *,
    ocr_controlled_provider_post_dryrun_review_root: str,
    ocr_controlled_provider_dryrun_root: Optional[str] = None,
    ocr_controlled_provider_planning_root: Optional[str] = None,
    model_registry_canonicalization_post_dryrun_review_root: Optional[str] = None,
    health_management_layer_integration_post_dryrun_review_root: Optional[str] = None,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    post_root = Path(ocr_controlled_provider_post_dryrun_review_root).expanduser().resolve()
    post_sm = _try_read_json(post_root / "summary.json") or {}
    post_vr = _try_read_json(post_root / "verifier_report.json") or {}
    next_route = _try_read_json(post_root / "next_route_readiness_decision_v1.json") or {}

    dryrun_root = Path(
        ocr_controlled_provider_dryrun_root
        or post_sm.get("upstream_dryrun_root")
        or post_root.parent / "ocr_controlled_provider_dryrun"
    ).expanduser().resolve()
    planning_root = Path(
        ocr_controlled_provider_planning_root
        or dryrun_root.parent / "ocr_controlled_provider_planning"
    ).expanduser().resolve()
    canonical_root = Path(
        model_registry_canonicalization_post_dryrun_review_root
        or post_root.parent / "model_registry_canonicalization_post_dryrun_review"
    ).expanduser().resolve()
    health_post_root = Path(
        health_management_layer_integration_post_dryrun_review_root
        or post_root.parent / "health_management_layer_integration_post_dryrun_review"
    ).expanduser().resolve()

    out_root = (
        Path(output_root).expanduser().resolve()
        if output_root
        else post_root.parent / "ocr_controlled_provider_authorization_roadmap_decision"
    )
    meta = {
        **_boundary_meta(),
        "upstream_post_dryrun_review_root": str(post_root),
        "upstream_dryrun_root": str(dryrun_root),
        "upstream_planning_root": str(planning_root),
        "output_root": str(out_root),
    }

    dryrun_sm = _try_read_json(dryrun_root / "summary.json") or {}
    dryrun_vr = _try_read_json(dryrun_root / "verifier_report.json") or {}
    planning_sm = _try_read_json(planning_root / "summary.json") or {}
    readiness = _try_read_json(dryrun_root / "ocr_provider_readiness_candidate_samples_v1.json") or {}
    blocked = _try_read_json(dryrun_root / "ocr_blocked_path_result_v1.json") or {}
    canonical_sm = _try_read_json(canonical_root / "summary.json") or {}
    health_sm = _try_read_json(health_post_root / "summary.json") or {}

    post_go = post_vr.get("verifier") == "GO" and post_vr.get("passed") is True
    if not post_go:
        blockers.append("post-dryrun review verifier must be GO")
    if post_sm.get("final_decision") != UPSTREAM_POST_REVIEW_FINAL:
        blockers.append("post-review final_decision mismatch")
    if post_sm.get("recommended_next_phase") != UPSTREAM_POST_REVIEW_NEXT:
        blockers.append("post-review recommended_next_phase mismatch")
    if post_sm.get("ocr_controlled_provider_dryrun_closed") is not True:
        blockers.append("ocr_controlled_provider_dryrun_closed required")
    if post_sm.get("ocr_candidate_chain_trusted") is not True:
        blockers.append("ocr_candidate_chain_trusted required")
    if next_route.get("do_not_start_provider_trial_now") is not True:
        blockers.append("must not start provider trial now")

    if dryrun_vr.get("verifier") != "GO":
        blockers.append("dryrun verifier should be GO")
    if readiness.get("sample_count") != 4:
        blockers.append("provider readiness count must be 4")
    for sample in readiness.get("samples") or []:
        if sample.get("invocation_allowed") is not False:
            blockers.append("all readiness invocation_allowed must be false")
            break
    if blocked.get("all_blocked") is not True or len(blocked.get("paths") or []) != len(BLOCKED_PATHS):
        blockers.append("all blocked paths must be blocked")

    for field in (
        "paddleocr_invoked_now",
        "rapidocr_invoked_now",
        "real_ocr_provider_invoked_now",
        "ocr_request_submitted_now",
        "image_read_executed_now",
        "crop_executed_now",
        "ocr_fact_generated_now",
    ):
        if dryrun_sm.get(field) is True or post_sm.get(field) is True:
            blockers.append(f"{field} must be false")

    if planning_sm.get("boundary_ok") is not True:
        blockers.append("planning should be boundary_ok")
    if canonical_sm.get("b_lite_canonical_v0_baseline_closed") is not True:
        blockers.append("model_registry_canonical_v0 must be closed")
    if health_sm.get("health_management_integration_dryrun_closed") is not True:
        blockers.append("health management must be closed")

    input_review = {
        "review_id": "ocr_post_dryrun_review_input_review_v1",
        "upstream_post_review_root": str(post_root),
        "upstream_dryrun_root": str(dryrun_root),
        "upstream_planning_root": str(planning_root),
        "upstream_verifier_go": post_go,
        "upstream_final_decision": post_sm.get("final_decision"),
        "ocr_controlled_provider_dryrun_closed": post_sm.get("ocr_controlled_provider_dryrun_closed"),
        "ocr_candidate_chain_trusted": post_sm.get("ocr_candidate_chain_trusted"),
        "readiness_count": readiness.get("sample_count"),
        "blocked_paths_count": len(blocked.get("paths") or []),
        "cannot_start_trial_now": True,
        "review_pass": len(blockers) == 0,
        "blockers": blockers,
        **meta,
    }

    route_a = {
        "assessment_id": "route_a_provider_authorization_planning_assessment_v1",
        "route_id": "A",
        "route_label": ROUTE_A,
        "status": "deferred",
        "defer_reasons": [
            "provider readiness is candidate only — not authorization-ready",
            "provider selection not completed",
            "local dependency / model files / environment / resource boundary not checked",
            "direct authorization risks misreading readiness as provider callable",
        ],
        **meta,
    }

    route_b = {
        "assessment_id": "route_b_provider_selection_dependency_environment_assessment_v1",
        "route_id": "B",
        "route_label": ROUTE_B,
        "status": "selected",
        "selection_reasons": [
            "paddleocr_later / rapidocr_later / external_later provider candidates already defined",
            "need provider evaluation rules before authorization",
            "must check local dependency, model files, Python packages, hardware resources, path permissions, runtime isolation",
            "define provider capability / cost / latency / fallback / health binding without invoking provider",
            "still no provider call in this phase",
        ],
        "planning_scope": [
            "provider_selection_rules",
            "local_dependency_inventory",
            "model_file_readiness",
            "environment_readiness",
            "resource_boundary",
        ],
        **meta,
    }

    route_c = {
        "assessment_id": "route_c_controlled_trial_planning_assessment_v1",
        "route_id": "C",
        "route_label": ROUTE_C,
        "status": "blocked_until_authorization",
        "block_reasons": [
            "trial must follow provider selection and authorization",
            "cannot enter controlled trial now",
        ],
        **meta,
    }

    route_d = {
        "assessment_id": "route_d_defer_ocr_provider_assessment_v1",
        "route_id": "D",
        "route_label": ROUTE_D,
        "status": "deferred",
        "defer_reasons": [
            "OCR remains P0 after controlled provider planning and dryrun",
            "continuing provider readiness path is more reasonable than returning to Vision/Voice now",
        ],
        **meta,
    }

    selection_matrix = {
        "matrix_id": "ocr_authorization_route_selection_matrix_v1",
        "routes": [
            {"route": ROUTE_A, "status": "deferred"},
            {"route": ROUTE_B, "status": "selected"},
            {"route": ROUTE_C, "status": "blocked_until_authorization"},
            {"route": ROUTE_D, "status": "deferred"},
        ],
        "selected_route": SELECTED_ROUTE,
        "deferred_route_a": DEFERRED_ROUTE_A,
        "blocked_route_c": BLOCKED_ROUTE_C,
        "deferred_route_d": DEFERRED_ROUTE_D,
        **meta,
    }

    preconditions = {
        "preconditions_id": "selected_route_preconditions_v1",
        "selected_route": SELECTED_ROUTE,
        "preconditions": [
            "ocr_controlled_provider_dryrun_closed",
            "ocr_candidate_chain_trusted",
            "provider readiness invocation_allowed=false for all 4 candidates",
            "15 blocked paths remain blocked",
            "no PaddleOCR / RapidOCR / real OCR invocation in roadmap decision",
        ],
        "forbidden_now": [
            "provider authorization",
            "provider invocation",
            "OCRRequest submit",
            "image read / crop",
            "controlled trial execution",
        ],
        **meta,
    }

    deferred_register = {
        "register_id": "deferred_routes_register_v1",
        "deferred_items": [
            {"route": ROUTE_A, "status": "deferred", "resume_after": "provider_selection_and_environment_readiness"},
            {"route": ROUTE_C, "status": "blocked_until_authorization", "resume_after": "authorization_planning"},
            {"route": ROUTE_D, "status": "deferred", "note": "OCR P0 continues"},
        ],
        **meta,
    }

    decision_ok = len(blockers) == 0
    boundary_ok = decision_ok

    next_readiness = {
        "readiness_id": "next_phase_readiness_decision_v1",
        "ready_for_provider_selection_dependency_environment_planning": boundary_ok,
        "selected_route": SELECTED_ROUTE,
        "do_not_authorize_provider_now": True,
        "do_not_start_controlled_trial_now": True,
        "recommended_next_phase": NEXT_PHASE_GO if boundary_ok else PHASE_ID,
        "final_decision": FINAL_DECISION_GO if boundary_ok else FINAL_DECISION_HOLD,
        **meta,
    }

    policy = {
        "policy_id": "ocr_authorization_roadmap_decision_policy_v1",
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
        "deferred_route_a": DEFERRED_ROUTE_A,
        "blocked_route_c": BLOCKED_ROUTE_C,
        "deferred_route_d": DEFERRED_ROUTE_D,
        "high_risk_count": 0 if boundary_ok else 1,
        **meta,
    }

    return {
        "ocr_authorization_roadmap_decision_policy": policy,
        "ocr_post_dryrun_review_input_review": input_review,
        "route_a_provider_authorization_planning_assessment": route_a,
        "route_b_provider_selection_dependency_environment_assessment": route_b,
        "route_c_controlled_trial_planning_assessment": route_c,
        "route_d_defer_ocr_provider_assessment": route_d,
        "ocr_authorization_route_selection_matrix": selection_matrix,
        "selected_route_preconditions": preconditions,
        "deferred_routes_register": deferred_register,
        "next_phase_readiness_decision": next_readiness,
        "non_claims_register": non_claims,
        "summary": summary,
    }
