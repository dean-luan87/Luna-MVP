# -*- coding: utf-8 -*-
"""Compressed OCR Authorization Roadmap Decision v1 — Route A compressed lifecycle selected."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.capability_factory_admission_and_operation_standard_dryrun_and_review_v1 import (
    COMPRESSED_PATH,
    FINAL_DECISION_GO as FACTORY_DRYRUN_REVIEW_FINAL_GO,
    NEXT_PHASE_GO as FACTORY_DRYRUN_REVIEW_NEXT_PHASE,
)
from capabilities.governance.capability_factory_admission_and_operation_standard_planning_v1 import (
    STANDARD_ID,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.ocr_provider_authorization_formal_request_artifact_generation_planning_v1 import (
    FINAL_DECISION_GO as FORMAL_PLANNING_FINAL_GO,
)
from capabilities.governance.ocr_provider_authorization_request_dryrun_v1 import (
    CURRENT_REQUEST_DRYRUN_STATE,
)
from capabilities.governance.ocr_provider_authorization_request_post_dryrun_review_v1 import (
    FINAL_DECISION_GO as REQUEST_POST_REVIEW_FINAL_GO,
)

PHASE_ID = "Phase-Compressed-OCR-Authorization-Roadmap-Decision-v1-001"
SCOPE = "compressed_ocr_authorization_roadmap_decision_only"
SOURCE_CHAIN = "compressed_ocr_authorization_roadmap_decision_v1"

UPSTREAM_FACTORY_DRYRUN_REVIEW_FINAL = FACTORY_DRYRUN_REVIEW_FINAL_GO
UPSTREAM_FACTORY_DRYRUN_REVIEW_NEXT = FACTORY_DRYRUN_REVIEW_NEXT_PHASE

FINAL_DECISION_GO = (
    "COMPRESSED_OCR_AUTHORIZATION_ROADMAP_DECISION_READY_FOR_COMPRESSED_AUTHORIZATION_LIFECYCLE_PLANNING"
)
FINAL_DECISION_HOLD = "COMPRESSED_OCR_AUTHORIZATION_ROADMAP_DECISION_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Compressed-OCR-Authorization-Lifecycle-Planning-v1-001"
NEXT_PHASE_HOLD = "Phase-Compressed-OCR-Authorization-Roadmap-Issue-Review-v1-001"

ROUTE_A = "Route A — Compressed OCR Authorization Lifecycle via Factory Standard"
ROUTE_B = "Route B — Resume Formal Artifact / Send / Grant Triple Chain"
ROUTE_C = "Route C — Real Dependency Check Authorization"
ROUTE_D = "Route D — Historical Redundancy Cleanup"

SELECTED_ROUTE = ROUTE_A
BLOCKED_ROUTE_B = "Resume Formal Artifact / Send / Grant Triple Chain"
DEFERRED_ROUTE_C = "Real Dependency Check Authorization"
DEFERRED_ROUTE_D = "Historical Redundancy Cleanup"

FACTORY_STANDARDS_REQUIRED: Tuple[str, ...] = (
    "Candidate Standard",
    "Artifact Standard",
    "Lifecycle Standard",
    "Boundary Standard",
    "Evidence Standard",
    "Approval/Grant Standard",
    "Sandbox/Rollback Standard",
    "Provider/Machine Standard",
    "Transfer Standard",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Roadmap Decision GO ≠ compressed lifecycle executed",
    "compressed authorization route selected ≠ formal artifact generated",
    "Factory Standard adoption ≠ grant issued",
    "compressed lifecycle planning ≠ real dependency check allowed",
    "triple-chain blocked ≠ historical evidence deleted",
    "cleanup deferred ≠ cleanup skipped",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "formal_artifact_triple_chain_resumed_now",
    "formal_request_artifact_generated_now",
    "formal_request_artifact_persisted_now",
    "authorization_request_sent_now",
    "authorization_request_approved_now",
    "grant_issued_now",
    "execution_window_opened_now",
    "real_dependency_check_executed_now",
    "provider_selection_finalized_now",
    "provider_imported_now",
    "provider_invoked_now",
    "dependency_install_executed_now",
    "model_download_executed_now",
    "ocr_request_submitted_now",
    "image_read_executed_now",
    "crop_executed_now",
    "ocr_fact_generated_now",
    "user_facing_output_generated_now",
    "memory_written_now",
    "world_model_written_now",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/compressed_ocr_authorization_roadmap_decision"
)


def _boundary_meta() -> Dict[str, Any]:
    meta = {
        "compressed_ocr_authorization_roadmap_decision_only": True,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "standard_id": STANDARD_ID,
        "selected_provider_for_execution": None,
    }
    for field in BOUNDARY_FALSE:
        meta[field] = False
    meta["formal_artifact_triple_chain_resumed_now"] = False
    meta["provider_selection_finalized_now"] = False
    meta["selected_provider_for_execution"] = None
    return meta


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def run_compressed_ocr_authorization_roadmap_decision_v1(
    *,
    capability_factory_admission_and_operation_standard_dryrun_and_review_root: str,
    capability_factory_admission_and_operation_standard_planning_root: Optional[str] = None,
    ocr_provider_authorization_formal_request_artifact_generation_planning_root: Optional[str] = None,
    ocr_provider_authorization_request_post_dryrun_review_root: Optional[str] = None,
    controlled_provider_readiness_harness_factory_registration_post_dryrun_review_root: Optional[str] = None,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    factory_dr_root = Path(
        capability_factory_admission_and_operation_standard_dryrun_and_review_root
    ).expanduser().resolve()
    factory_dr_sm = _try_read_json(factory_dr_root / "summary.json") or {}
    factory_dr_vr = _try_read_json(factory_dr_root / "verifier_report.json") or {}
    readiness = _try_read_json(factory_dr_root / "factory_standard_adoption_readiness_decision_v1.json") or {}
    compression_r = _try_read_json(factory_dr_root / "compression_impact_review_v1.json") or {}

    factory_plan_root = Path(
        capability_factory_admission_and_operation_standard_planning_root
        or factory_dr_root.parent / "capability_factory_admission_and_operation_standard_planning"
    ).expanduser().resolve()
    factory_plan_vr = _try_read_json(factory_plan_root / "verifier_report.json") or {}

    formal_plan_root = Path(
        ocr_provider_authorization_formal_request_artifact_generation_planning_root
        or factory_dr_root.parent / "ocr_provider_authorization_formal_request_artifact_generation_planning"
    ).expanduser().resolve()
    formal_plan_sm = _try_read_json(formal_plan_root / "summary.json") or {}
    formal_plan_vr = _try_read_json(formal_plan_root / "verifier_report.json") or {}

    req_post_root = Path(
        ocr_provider_authorization_request_post_dryrun_review_root
        or factory_dr_root.parent / "ocr_provider_authorization_request_post_dryrun_review"
    ).expanduser().resolve()
    req_post_sm = _try_read_json(req_post_root / "summary.json") or {}
    req_post_vr = _try_read_json(req_post_root / "verifier_report.json") or {}
    req_post_closure = _try_read_json(req_post_root / "authorization_request_closure_decision_v1.json") or {}

    factory_post_root = Path(
        controlled_provider_readiness_harness_factory_registration_post_dryrun_review_root
        or factory_dr_root.parent / "controlled_provider_readiness_harness_factory_registration_post_dryrun_review"
    ).expanduser().resolve()
    factory_post_vr = _try_read_json(factory_post_root / "verifier_report.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_boundary_meta(),
        "upstream_factory_dryrun_review_root": str(factory_dr_root),
        "upstream_factory_planning_root": str(factory_plan_root),
        "upstream_formal_artifact_planning_root": str(formal_plan_root),
        "upstream_request_post_dryrun_review_root": str(req_post_root),
        "upstream_factory_post_review_root": str(factory_post_root),
        "output_root": str(out_root),
    }

    factory_dr_go = factory_dr_vr.get("verifier") == "GO" and factory_dr_vr.get("passed") is True
    if not factory_dr_go:
        blockers.append("factory standard dryrun and review verifier must be GO")
    if factory_dr_sm.get("final_decision") != UPSTREAM_FACTORY_DRYRUN_REVIEW_FINAL:
        blockers.append("factory dryrun review final_decision mismatch")
    if factory_dr_sm.get("recommended_next_phase") != UPSTREAM_FACTORY_DRYRUN_REVIEW_NEXT:
        blockers.append("factory dryrun review recommended_next_phase mismatch")
    if factory_dr_sm.get("nine_standards_validated") is not True:
        blockers.append("nine_standards_validated must be true")
    if factory_dr_sm.get("ocr_chain_coverage") is not True:
        blockers.append("ocr_chain_coverage must be true")
    if factory_dr_sm.get("compression_validated") is not True:
        blockers.append("compression_validated must be true")
    if readiness.get("do_not_resume_formal_artifact_triple_chain") is not True:
        blockers.append("do_not_resume_formal_artifact_triple_chain must be true")

    if factory_plan_vr.get("verifier") != "GO":
        blockers.append("factory standard planning must be GO")

    if formal_plan_vr.get("verifier") != "GO":
        blockers.append("formal artifact generation planning must be GO")
    if formal_plan_sm.get("final_decision") != FORMAL_PLANNING_FINAL_GO:
        blockers.append("formal planning final_decision mismatch")
    if compression_r.get("formal_artifact_triple_compressible") is not True:
        blockers.append("formal artifact triple chain must be compressible")

    if req_post_vr.get("verifier") != "GO":
        blockers.append("request post-dryrun review must be GO")
    if req_post_sm.get("final_decision") != REQUEST_POST_REVIEW_FINAL_GO:
        blockers.append("request post-dryrun final_decision mismatch")
    if req_post_closure.get("request_artifact_candidate_trusted") is not True:
        blockers.append("request_artifact_candidate must be trusted")
    if req_post_sm.get("current_lifecycle_state") != CURRENT_REQUEST_DRYRUN_STATE:
        blockers.append("lifecycle must be request_artifact_candidate_ready")

    if factory_post_vr.get("verifier") != "GO":
        blockers.append("harness factory registration post-review must be GO")

    for field in BOUNDARY_FALSE:
        if factory_dr_sm.get(field) is True or req_post_sm.get(field) is True or formal_plan_sm.get(field) is True:
            blockers.append(f"{field} must be false")

    input_review = {
        "review_id": "factory_standard_dryrun_review_input_review_v1",
        "upstream_root": str(factory_dr_root),
        "upstream_verifier_go": factory_dr_go,
        "upstream_final_decision": factory_dr_sm.get("final_decision"),
        "nine_standards_validated": factory_dr_sm.get("nine_standards_validated"),
        "ocr_chain_coverage": factory_dr_sm.get("ocr_chain_coverage"),
        "compression_validated": factory_dr_sm.get("compression_validated"),
        "do_not_resume_triple_chain": readiness.get("do_not_resume_formal_artifact_triple_chain"),
        "review_pass": len(blockers) == 0,
        "blockers": blockers,
        **meta,
    }

    compression_readiness = {
        "review_id": "compression_readiness_review_v1",
        "formal_planning_go": formal_plan_vr.get("verifier") == "GO",
        "superseded_by_factory_standard": True,
        "mergeable_phase_count": len(compression_r.get("mergeable_phases") or []),
        "formal_triple_compressible": compression_r.get("formal_artifact_triple_compressible"),
        "send_triple_compressible": compression_r.get("send_triple_compressible"),
        "grant_triple_compressible": compression_r.get("grant_triple_compressible"),
        "compression_readiness_pass": len(blockers) == 0,
        **meta,
    }

    route_a = {
        "assessment_id": "route_a_compressed_authorization_lifecycle_assessment_v1",
        "route_id": "A",
        "route_label": ROUTE_A,
        "status": "selected",
        "selection_reasons": [
            "Factory Standard validated 9 standard categories",
            "OCR authorization chain coverage 13/13",
            "compression_validated=true",
            "Formal Artifact / Send / Grant triple chain 9 phases compressible",
            "non-claims / boundary / lifecycle / evidence absorbed as factory defaults",
            "May enter compressed authorization lifecycle planning",
            "Still no grant, no execute",
        ],
        **meta,
    }

    route_b = {
        "assessment_id": "route_b_resume_formal_artifact_triple_chain_assessment_v1",
        "route_id": "B",
        "route_label": ROUTE_B,
        "status": "blocked",
        "block_reasons": [
            "do_not_resume_formal_artifact_triple_chain=true",
            "Would duplicate rules already absorbed into factory standard",
            "Violates Standard / Harness / Contract first principle",
        ],
        **meta,
    }

    route_c = {
        "assessment_id": "route_c_real_dependency_check_authorization_assessment_v1",
        "route_id": "C",
        "route_label": ROUTE_C,
        "status": "deferred_after_compressed_authorization_lifecycle",
        "defer_reasons": [
            "real_dependency_check still requires standalone authorization",
            "Must follow compressed authorization lifecycle confirmation",
            "Cannot execute real dependency check now",
        ],
        **meta,
    }

    route_d = {
        "assessment_id": "route_d_historical_redundancy_cleanup_assessment_v1",
        "route_id": "D",
        "route_label": ROUTE_D,
        "status": "deferred_next",
        "defer_reasons": [
            "Historical redundancy cleanup important but not before compressed route",
            "After roadmap decision enter Factory Standard Historical Redundancy Cleanup Planning",
            "Cleanup uses superseded/absorbed/deprecated/read_only markers only — no physical delete",
        ],
        **meta,
    }

    selection_matrix = {
        "matrix_id": "compressed_ocr_authorization_route_selection_matrix_v1",
        "routes": [
            {"route": ROUTE_A, "status": "selected"},
            {"route": ROUTE_B, "status": "blocked"},
            {"route": ROUTE_C, "status": "deferred_after_compressed_authorization_lifecycle"},
            {"route": ROUTE_D, "status": "deferred_next"},
        ],
        "selected_route": SELECTED_ROUTE,
        "blocked_route_b": BLOCKED_ROUTE_B,
        "deferred_route_c": DEFERRED_ROUTE_C,
        "deferred_route_d": DEFERRED_ROUTE_D,
        **meta,
    }

    preconditions = {
        "preconditions_id": "selected_route_preconditions_v1",
        "selected_route": SELECTED_ROUTE,
        "preconditions": [
            "factory standard dryrun and review GO",
            "nine_standards_validated=true",
            "ocr_chain_coverage=true",
            "compression_validated=true",
            "request_artifact_candidate_ready",
            "formal artifact triple chain not resumed",
            "selected_provider_for_execution=null",
        ],
        "forbidden_now": [
            "formal artifact generation",
            "request send",
            "grant issue",
            "execution window open",
            "real dependency check",
            "provider import/invoke",
        ],
        **meta,
    }

    deferred_register = {
        "register_id": "deferred_routes_register_v1",
        "deferred_items": [
            {
                "route": DEFERRED_ROUTE_C,
                "status": "deferred_after_compressed_authorization_lifecycle",
                "resume_after": "compressed_authorization_lifecycle_planning_closure",
            },
            {
                "route": DEFERRED_ROUTE_D,
                "status": "deferred_next",
                "next_phase": "Phase-Factory-Standard-Historical-Redundancy-Cleanup-Planning-v1-001",
                "note": "mark only — superseded_by / absorbed_by / deprecated_for_new_phase / read_only_evidence_source",
            },
            {
                "route": BLOCKED_ROUTE_B,
                "status": "blocked",
                "note": "do_not_resume_formal_artifact_triple_chain",
            },
        ],
        **meta,
    }

    execution_model = {
        "model_id": "compressed_authorization_execution_model_v1",
        "compressed_path": list(COMPRESSED_PATH),
        "step_count": len(COMPRESSED_PATH),
        "formal_request_artifact_generated_now": False,
        "request_sent_now": False,
        "grant_issued_now": False,
        "execution_window_opened_now": False,
        "provider_invoked_now": False,
        "real_dependency_check_executed_now": False,
        **meta,
    }

    adoption_binding = {
        "binding_id": "factory_standard_adoption_binding_v1",
        "standards_required": list(FACTORY_STANDARDS_REQUIRED),
        "standard_count": len(FACTORY_STANDARDS_REQUIRED),
        "validation_factory_pass_required_before_midplatform": True,
        "all_standards_required": True,
        **meta,
    }

    decision_ok = len(blockers) == 0
    boundary_ok = decision_ok

    next_readiness = {
        "readiness_id": "next_phase_readiness_decision_v1",
        "ready_for_compressed_authorization_lifecycle_planning": boundary_ok,
        "selected_route": SELECTED_ROUTE,
        "do_not_resume_formal_artifact_triple_chain": True,
        "do_not_generate_formal_artifact_now": True,
        "do_not_send_request_now": True,
        "do_not_grant_authorization_now": True,
        "do_not_execute_real_dependency_check_now": True,
        "recommended_next_phase": NEXT_PHASE_GO if boundary_ok else PHASE_ID,
        "final_decision": FINAL_DECISION_GO if boundary_ok else FINAL_DECISION_HOLD,
        **meta,
    }

    policy = {
        "policy_id": "compressed_ocr_authorization_roadmap_policy_v1",
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
        "blocked_route_b": BLOCKED_ROUTE_B,
        "deferred_route_c": DEFERRED_ROUTE_C,
        "deferred_route_d": DEFERRED_ROUTE_D,
        "high_risk_count": 0 if boundary_ok else 1,
        **meta,
    }

    return {
        "compressed_ocr_authorization_roadmap_policy": policy,
        "factory_standard_dryrun_review_input_review": input_review,
        "compression_readiness_review": compression_readiness,
        "route_a_compressed_authorization_lifecycle_assessment": route_a,
        "route_b_resume_formal_artifact_triple_chain_assessment": route_b,
        "route_c_real_dependency_check_authorization_assessment": route_c,
        "route_d_historical_redundancy_cleanup_assessment": route_d,
        "compressed_ocr_authorization_route_selection_matrix": selection_matrix,
        "selected_route_preconditions": preconditions,
        "deferred_routes_register": deferred_register,
        "compressed_authorization_execution_model": execution_model,
        "factory_standard_adoption_binding": adoption_binding,
        "next_phase_readiness_decision": next_readiness,
        "non_claims_register": non_claims,
        "summary": summary,
    }
