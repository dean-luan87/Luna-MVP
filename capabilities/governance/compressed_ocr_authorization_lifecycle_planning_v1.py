# -*- coding: utf-8 -*-
"""Compressed OCR Authorization Lifecycle Planning v1 — unified 7-step lifecycle via Factory Standard."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.capability_factory_admission_and_operation_standard_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as FACTORY_DRYRUN_REVIEW_FINAL_GO,
)
from capabilities.governance.capability_factory_admission_and_operation_standard_planning_v1 import (
    COMPRESSED_PATH,
    STANDARD_ID,
)
from capabilities.governance.compressed_ocr_authorization_roadmap_decision_v1 import (
    FINAL_DECISION_GO as ROADMAP_FINAL_GO,
    NEXT_PHASE_GO as ROADMAP_NEXT_PHASE,
    SELECTED_ROUTE,
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

PHASE_ID = "Phase-Compressed-OCR-Authorization-Lifecycle-Planning-v1-001"
SCOPE = "compressed_ocr_authorization_lifecycle_planning_only"
SOURCE_CHAIN = "compressed_ocr_authorization_lifecycle_planning_v1"

UPSTREAM_ROADMAP_FINAL = ROADMAP_FINAL_GO
UPSTREAM_ROADMAP_NEXT = ROADMAP_NEXT_PHASE

FINAL_DECISION_GO = (
    "COMPRESSED_OCR_AUTHORIZATION_LIFECYCLE_PLANNING_READY_FOR_DRYRUN_AND_REVIEW"
)
FINAL_DECISION_HOLD = "COMPRESSED_OCR_AUTHORIZATION_LIFECYCLE_PLANNING_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Compressed-OCR-Authorization-Lifecycle-DryRunAndReview-v1-001"
NEXT_PHASE_HOLD = "Phase-Compressed-OCR-Authorization-Lifecycle-Issue-Review-v1-001"

CURRENT_STATE = "lifecycle_planning_defined"

LIFECYCLE_STATES: Tuple[str, ...] = (
    "lifecycle_planning_defined",
    "request_candidate_ready",
    "formal_artifact_candidate_ready_later",
    "send_candidate_ready_later",
    "grant_candidate_ready_later",
    "execution_window_candidate_ready_later",
    "review_required_later",
    "closed_later",
)

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

BOUNDARY_MATRIX_BLOCKED: Tuple[str, ...] = (
    "lifecycle_planning_to_formal_artifact_generation",
    "lifecycle_planning_to_request_send",
    "lifecycle_planning_to_grant_issue",
    "lifecycle_planning_to_execution_window_open",
    "lifecycle_planning_to_real_dependency_check",
    "lifecycle_planning_to_provider_import",
    "lifecycle_planning_to_dependency_install",
    "lifecycle_planning_to_model_download",
    "lifecycle_planning_to_provider_selection_finalize",
    "lifecycle_planning_to_controlled_trial",
    "lifecycle_planning_to_ocr_request_submit",
    "lifecycle_planning_to_image_read",
    "lifecycle_planning_to_ocr_fact",
    "compressed_lifecycle_to_user_output",
    "compressed_lifecycle_to_memory_write",
    "compressed_lifecycle_to_world_model_write",
)

EVIDENCE_FIELDS: Tuple[str, ...] = (
    "source_phase_ref",
    "source_candidate_ref",
    "formal_artifact_candidate_ref_later",
    "send_candidate_ref_later",
    "grant_candidate_ref_later",
    "execution_window_candidate_ref_later",
    "boundary_audit_result",
    "validation_result",
    "rollback_plan_ref",
    "verifier_report",
    "post_execution_review_result_later",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Lifecycle Planning GO ≠ compressed lifecycle executed",
    "lifecycle contract defined ≠ formal artifact generated",
    "request_artifact_candidate_ready binding ≠ new request candidate generated",
    "DryRunAndReview next ≠ request sent",
    "DryRunAndReview next ≠ grant issued",
    "DryRunAndReview next ≠ execution window opened",
    "DryRunAndReview next ≠ real dependency check allowed",
    "Factory Standard adoption binding ≠ Midplatform consumption",
    "formal artifact planning superseded ≠ historical evidence deleted",
    "triple-chain blocked ≠ cleanup skipped",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "compressed_lifecycle_executed_now",
    "formal_artifact_triple_chain_resumed_now",
    "request_candidate_generated_now",
    "formal_artifact_candidate_generated_now",
    "send_candidate_generated_now",
    "grant_candidate_generated_now",
    "execution_window_candidate_generated_now",
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

STAGE_FACTORY_REFS: Tuple[Tuple[str, Tuple[str, ...]], ...] = (
    (
        "Authorization Lifecycle via Factory Standard",
        ("Lifecycle Standard", "Boundary Standard", "Evidence Standard", "Transfer Standard"),
    ),
    ("Request Candidate", ("Candidate Standard", "Artifact Standard", "Lifecycle Standard")),
    (
        "Formal Artifact Candidate",
        ("Artifact Standard", "Evidence Standard", "Lifecycle Standard", "Transfer Standard"),
    ),
    (
        "Send Candidate",
        ("Approval/Grant Standard", "Boundary Standard", "Evidence Standard", "Lifecycle Standard"),
    ),
    (
        "Grant Candidate",
        ("Approval/Grant Standard", "Boundary Standard", "Lifecycle Standard", "Evidence Standard"),
    ),
    (
        "Execution Window Candidate",
        ("Sandbox/Rollback Standard", "Boundary Standard", "Provider/Machine Standard", "Lifecycle Standard"),
    ),
    (
        "Review",
        ("Evidence Standard", "Boundary Standard", "Lifecycle Standard", "Transfer Standard"),
    ),
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "compressed_ocr_authorization_lifecycle_planning"
)


def _planning_meta() -> Dict[str, Any]:
    meta = {
        "compressed_ocr_authorization_lifecycle_planning_only": True,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "standard_id": STANDARD_ID,
        "selected_route": SELECTED_ROUTE,
        "current_state": CURRENT_STATE,
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


def _stage_contract(
    stage_id: str,
    *,
    input_contract: Dict[str, Any],
    output_contract: Dict[str, Any],
    factory_standard_refs: Tuple[str, ...],
    evidence_required: Tuple[str, ...],
    boundary_required: Tuple[str, ...],
    next_stage: Optional[str],
) -> Dict[str, Any]:
    return {
        "stage_id": stage_id,
        "input_contract": input_contract,
        "output_contract": output_contract,
        "factory_standard_refs": list(factory_standard_refs),
        "evidence_required": list(evidence_required),
        "boundary_required": list(boundary_required),
        "next_stage_condition": next_stage,
        "current_executed_now": False,
        "promotion_requires_future_phase": True,
    }


def _build_lifecycle_stages() -> List[Dict[str, Any]]:
    refs_map = dict(STAGE_FACTORY_REFS)
    stages: List[Dict[str, Any]] = []
    for i, step in enumerate(COMPRESSED_PATH):
        next_step = COMPRESSED_PATH[i + 1] if i + 1 < len(COMPRESSED_PATH) else "closed_later"
        base_evidence = ("source_phase_ref", "source_candidate_ref", "boundary_audit_result", "validation_result")
        if step == "Authorization Lifecycle via Factory Standard":
            stages.append(
                _stage_contract(
                    step,
                    input_contract={
                        "factory_standard_id": STANDARD_ID,
                        "roadmap_decision_go": True,
                        "selected_route": SELECTED_ROUTE,
                    },
                    output_contract={
                        "lifecycle_planning_defined": True,
                        "compressed_path": list(COMPRESSED_PATH),
                    },
                    factory_standard_refs=refs_map[step],
                    evidence_required=base_evidence,
                    boundary_required=("planning_only", "no_execution"),
                    next_stage=next_step,
                )
            )
        elif step == "Request Candidate":
            stages.append(
                _stage_contract(
                    step,
                    input_contract={
                        "authorization_request_candidate": "bound_from_ocr_provider_authorization_dryrun",
                        "request_artifact_candidate": "bound_from_ocr_provider_authorization_request_dryrun",
                        "request_artifact_candidate_ready": True,
                    },
                    output_contract={
                        "request_candidate_ready": True,
                        "new_request_candidate_generated_now": False,
                        "formal_artifact_generated_now": False,
                        "request_sent_now": False,
                    },
                    factory_standard_refs=refs_map[step],
                    evidence_required=base_evidence + ("source_candidate_ref",),
                    boundary_required=("no_new_candidate_generation", "no_send"),
                    next_stage=next_step,
                )
            )
        elif step == "Formal Artifact Candidate":
            stages.append(
                _stage_contract(
                    step,
                    input_contract={
                        "source_request_candidate_ref_required": True,
                        "schema_version_required": True,
                        "evidence_ref_required": True,
                        "validation_factory_pass_required": True,
                    },
                    output_contract={
                        "formal_artifact_candidate_later": True,
                        "formal_request_artifact_generated_now": False,
                        "formal_artifact_candidate_generated_now": False,
                        "artifact_persisted_now": False,
                    },
                    factory_standard_refs=refs_map[step],
                    evidence_required=base_evidence + ("formal_artifact_candidate_ref_later",),
                    boundary_required=("no_formal_artifact_generation", "no_persist"),
                    next_stage=next_step,
                )
            )
        elif step == "Send Candidate":
            stages.append(
                _stage_contract(
                    step,
                    input_contract={
                        "send_candidate_later": True,
                        "send_precheck_required": True,
                        "owner_operator_approval_required": True,
                        "boundary_audit_required": True,
                        "verifier_required": True,
                    },
                    output_contract={
                        "send_candidate_ready_later": True,
                        "authorization_request_sent_now": False,
                        "approval_collected_now": False,
                    },
                    factory_standard_refs=refs_map[step],
                    evidence_required=base_evidence + ("send_candidate_ref_later",),
                    boundary_required=("no_send", "no_approval_collect"),
                    next_stage=next_step,
                )
            )
        elif step == "Grant Candidate":
            stages.append(
                _stage_contract(
                    step,
                    input_contract={
                        "grant_candidate_later": True,
                        "grant_conditions_required": True,
                        "revocation_condition_required": True,
                        "expiration_or_ttl_required": True,
                        "prohibited_actions_required": True,
                    },
                    output_contract={
                        "grant_candidate_ready_later": True,
                        "grant_issued_now": False,
                        "provider_authorization_granted_now": False,
                    },
                    factory_standard_refs=refs_map[step],
                    evidence_required=base_evidence + ("grant_candidate_ref_later",),
                    boundary_required=("no_grant_issue",),
                    next_stage=next_step,
                )
            )
        elif step == "Execution Window Candidate":
            stages.append(
                _stage_contract(
                    step,
                    input_contract={
                        "execution_window_candidate_later": True,
                        "allowed_workspace_path_required": True,
                        "forbidden_paths_required": True,
                        "timeout_limit_required": True,
                        "sandbox_required": True,
                        "rollback_required": True,
                        "post_execution_review_required": True,
                    },
                    output_contract={
                        "execution_window_candidate_ready_later": True,
                        "execution_window_opened_now": False,
                        "real_dependency_check_executed_now": False,
                        "provider_invoked_now": False,
                    },
                    factory_standard_refs=refs_map[step],
                    evidence_required=base_evidence
                    + ("execution_window_candidate_ref_later", "rollback_plan_ref"),
                    boundary_required=("no_execution_window", "no_real_dep", "no_provider_invoke"),
                    next_stage=next_step,
                )
            )
        elif step == "Review":
            stages.append(
                _stage_contract(
                    step,
                    input_contract={
                        "post_execution_review_required": True,
                        "evidence_package_required": True,
                        "boundary_audit_required": True,
                        "verifier_required": True,
                        "closure_decision_required": True,
                    },
                    output_contract={
                        "review_required_later": True,
                        "closed_later": True,
                    },
                    factory_standard_refs=refs_map[step],
                    evidence_required=base_evidence
                    + ("verifier_report", "post_execution_review_result_later"),
                    boundary_required=("closure_only", "no_user_output"),
                    next_stage=next_step,
                )
            )
    return stages


def run_compressed_ocr_authorization_lifecycle_planning_v1(
    *,
    compressed_ocr_authorization_roadmap_decision_root: str,
    capability_factory_admission_and_operation_standard_dryrun_and_review_root: Optional[str] = None,
    capability_factory_admission_and_operation_standard_planning_root: Optional[str] = None,
    ocr_provider_authorization_request_post_dryrun_review_root: Optional[str] = None,
    ocr_provider_authorization_formal_request_artifact_generation_planning_root: Optional[str] = None,
    controlled_provider_readiness_harness_factory_registration_post_dryrun_review_root: Optional[str] = None,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    roadmap_root = Path(compressed_ocr_authorization_roadmap_decision_root).expanduser().resolve()
    roadmap_sm = _try_read_json(roadmap_root / "summary.json") or {}
    roadmap_vr = _try_read_json(roadmap_root / "verifier_report.json") or {}
    roadmap_next = _try_read_json(roadmap_root / "next_phase_readiness_decision_v1.json") or {}

    factory_dr_root = Path(
        capability_factory_admission_and_operation_standard_dryrun_and_review_root
        or roadmap_root.parent / "capability_factory_admission_and_operation_standard_dryrun_and_review"
    ).expanduser().resolve()
    factory_dr_sm = _try_read_json(factory_dr_root / "summary.json") or {}
    factory_dr_vr = _try_read_json(factory_dr_root / "verifier_report.json") or {}
    readiness_dr = _try_read_json(factory_dr_root / "factory_standard_adoption_readiness_decision_v1.json") or {}

    factory_plan_root = Path(
        capability_factory_admission_and_operation_standard_planning_root
        or roadmap_root.parent / "capability_factory_admission_and_operation_standard_planning"
    ).expanduser().resolve()
    factory_plan_vr = _try_read_json(factory_plan_root / "verifier_report.json") or {}

    req_post_root = Path(
        ocr_provider_authorization_request_post_dryrun_review_root
        or roadmap_root.parent / "ocr_provider_authorization_request_post_dryrun_review"
    ).expanduser().resolve()
    req_post_sm = _try_read_json(req_post_root / "summary.json") or {}
    req_post_vr = _try_read_json(req_post_root / "verifier_report.json") or {}
    req_post_closure = _try_read_json(req_post_root / "authorization_request_closure_decision_v1.json") or {}

    formal_plan_root = Path(
        ocr_provider_authorization_formal_request_artifact_generation_planning_root
        or roadmap_root.parent / "ocr_provider_authorization_formal_request_artifact_generation_planning"
    ).expanduser().resolve()
    formal_plan_sm = _try_read_json(formal_plan_root / "summary.json") or {}
    formal_plan_vr = _try_read_json(formal_plan_root / "verifier_report.json") or {}

    factory_post_root = Path(
        controlled_provider_readiness_harness_factory_registration_post_dryrun_review_root
        or roadmap_root.parent / "controlled_provider_readiness_harness_factory_registration_post_dryrun_review"
    ).expanduser().resolve()
    factory_post_vr = _try_read_json(factory_post_root / "verifier_report.json") or {}

    req_dryrun_root = req_post_root.parent / "ocr_provider_authorization_request_dryrun"
    auth_dryrun_root = req_post_root.parent / "ocr_provider_authorization_dryrun"
    artifact_candidate = _try_read_json(req_dryrun_root / "request_artifact_candidate_v1.json") or {}
    request_cand = _try_read_json(auth_dryrun_root / "authorization_request_candidate_v1.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_planning_meta(),
        "upstream_roadmap_decision_root": str(roadmap_root),
        "upstream_factory_dryrun_review_root": str(factory_dr_root),
        "upstream_factory_planning_root": str(factory_plan_root),
        "upstream_request_post_dryrun_review_root": str(req_post_root),
        "upstream_formal_artifact_planning_root": str(formal_plan_root),
        "upstream_factory_post_review_root": str(factory_post_root),
        "output_root": str(out_root),
    }

    if roadmap_vr.get("verifier") != "GO" or roadmap_vr.get("passed") is not True:
        blockers.append("roadmap decision verifier must be GO")
    if roadmap_sm.get("final_decision") != UPSTREAM_ROADMAP_FINAL:
        blockers.append("roadmap final_decision mismatch")
    if roadmap_sm.get("recommended_next_phase") != UPSTREAM_ROADMAP_NEXT:
        blockers.append("roadmap recommended_next_phase mismatch")
    if roadmap_sm.get("selected_route") != SELECTED_ROUTE:
        blockers.append("selected_route must be Route A")
    if roadmap_next.get("do_not_resume_formal_artifact_triple_chain") is not True:
        blockers.append("do_not_resume_formal_artifact_triple_chain must be true")

    if factory_dr_vr.get("verifier") != "GO":
        blockers.append("factory standard dryrun and review must be GO")
    if factory_dr_sm.get("final_decision") != FACTORY_DRYRUN_REVIEW_FINAL_GO:
        blockers.append("factory dryrun review final_decision mismatch")
    if factory_dr_sm.get("nine_standards_validated") is not True:
        blockers.append("nine_standards_validated must be true")
    if factory_dr_sm.get("compression_validated") is not True:
        blockers.append("compression_validated must be true")
    if readiness_dr.get("do_not_resume_formal_artifact_triple_chain") is not True:
        blockers.append("factory readiness do_not_resume must be true")

    if factory_plan_vr.get("verifier") != "GO":
        blockers.append("factory standard planning must be GO")

    if req_post_vr.get("verifier") != "GO":
        blockers.append("request post-dryrun review must be GO")
    if req_post_sm.get("final_decision") != REQUEST_POST_REVIEW_FINAL_GO:
        blockers.append("request post-dryrun final_decision mismatch")
    if req_post_closure.get("request_artifact_candidate_trusted") is not True:
        blockers.append("request_artifact_candidate must be trusted")
    if req_post_sm.get("current_lifecycle_state") != CURRENT_REQUEST_DRYRUN_STATE:
        blockers.append("lifecycle must be request_artifact_candidate_ready")

    if formal_plan_vr.get("verifier") != "GO":
        blockers.append("formal artifact generation planning must be GO")
    if formal_plan_sm.get("final_decision") != FORMAL_PLANNING_FINAL_GO:
        blockers.append("formal planning final_decision mismatch")

    if factory_post_vr.get("verifier") != "GO":
        blockers.append("harness factory registration post-review must be GO")

    if not request_cand.get("request_id"):
        blockers.append("authorization_request_candidate must exist")
    if not artifact_candidate.get("request_artifact_candidate_id"):
        blockers.append("request_artifact_candidate must exist")
    if artifact_candidate.get("candidate_only") is not True:
        blockers.append("request_artifact_candidate candidate_only must be true")

    for field in BOUNDARY_FALSE:
        if roadmap_sm.get(field) is True or req_post_sm.get(field) is True or formal_plan_sm.get(field) is True:
            blockers.append(f"{field} must be false upstream")

    planning_ok = len(blockers) == 0
    boundary_ok = planning_ok

    roadmap_input_review = {
        "review_id": "compressed_ocr_authorization_roadmap_input_review_v1",
        "upstream_root": str(roadmap_root),
        "upstream_verifier_go": roadmap_vr.get("verifier") == "GO",
        "upstream_final_decision": roadmap_sm.get("final_decision"),
        "selected_route": roadmap_sm.get("selected_route"),
        "do_not_resume_triple_chain": roadmap_next.get("do_not_resume_formal_artifact_triple_chain"),
        "review_pass": planning_ok,
        "blockers": blockers,
        **meta,
    }

    factory_adoption_input = {
        "review_id": "factory_standard_adoption_input_review_v1",
        "factory_dryrun_review_go": factory_dr_vr.get("verifier") == "GO",
        "nine_standards_validated": factory_dr_sm.get("nine_standards_validated"),
        "compression_validated": factory_dr_sm.get("compression_validated"),
        "formal_planning_go_superseded": formal_plan_vr.get("verifier") == "GO",
        "superseded_by_factory_standard": True,
        "review_pass": planning_ok,
        **meta,
    }

    lifecycle_stages = _build_lifecycle_stages()
    lifecycle_contract = {
        "contract_id": "compressed_authorization_lifecycle_contract_v1",
        "compressed_path": list(COMPRESSED_PATH),
        "step_count": len(COMPRESSED_PATH),
        "stages": lifecycle_stages,
        "all_stages_promotion_requires_future_phase": all(
            s.get("promotion_requires_future_phase") is True for s in lifecycle_stages
        ),
        "all_stages_executed_now_false": all(s.get("current_executed_now") is False for s in lifecycle_stages),
        **meta,
    }

    state_machine = {
        "machine_id": "compressed_authorization_state_machine_v1",
        "states": list(LIFECYCLE_STATES),
        "current_state": CURRENT_STATE,
        "transitions": [
            {"from": "lifecycle_planning_defined", "to": "request_candidate_ready", "requires_future_phase": True},
            {
                "from": "request_candidate_ready",
                "to": "formal_artifact_candidate_ready_later",
                "requires_future_phase": True,
            },
            {"from": "formal_artifact_candidate_ready_later", "to": "send_candidate_ready_later", "requires_future_phase": True},
            {"from": "send_candidate_ready_later", "to": "grant_candidate_ready_later", "requires_future_phase": True},
            {
                "from": "grant_candidate_ready_later",
                "to": "execution_window_candidate_ready_later",
                "requires_future_phase": True,
            },
            {"from": "execution_window_candidate_ready_later", "to": "review_required_later", "requires_future_phase": True},
            {"from": "review_required_later", "to": "closed_later", "requires_future_phase": True},
        ],
        **meta,
    }

    stage_key_map = {
        "Request Candidate": "request_candidate_stage_contract",
        "Formal Artifact Candidate": "formal_artifact_candidate_stage_contract",
        "Send Candidate": "send_candidate_stage_contract",
        "Grant Candidate": "grant_candidate_stage_contract",
        "Execution Window Candidate": "execution_window_candidate_stage_contract",
        "Review": "review_stage_contract",
    }
    stage_contracts: Dict[str, Dict[str, Any]] = {}
    for stage in lifecycle_stages:
        sid = stage["stage_id"]
        if sid in stage_key_map:
            stage_contracts[stage_key_map[sid]] = {
                "contract_id": stage_key_map[sid].replace("_stage_contract", "_stage_contract_v1"),
                **stage,
                **meta,
            }

    boundary_matrix = {
        "matrix_id": "compressed_lifecycle_boundary_matrix_v1",
        "blocked_paths": [
            {"path_id": p, "status": "blocked", "executed_now": False} for p in BOUNDARY_MATRIX_BLOCKED
        ],
        "all_blocked": True,
        "path_count": len(BOUNDARY_MATRIX_BLOCKED),
        **meta,
    }

    evidence_requirement = {
        "requirement_id": "compressed_lifecycle_evidence_requirement_v1",
        "factory_standard_evidence_binding": True,
        "required_fields": list(EVIDENCE_FIELDS),
        "field_count": len(EVIDENCE_FIELDS),
        **meta,
    }

    approval_grant_policy = {
        "policy_id": "compressed_lifecycle_approval_grant_policy_v1",
        "send_precheck_required": True,
        "owner_operator_approval_required": True,
        "grant_conditions_required": True,
        "revocation_condition_required": True,
        "expiration_or_ttl_required": True,
        "prohibited_actions_required": True,
        "grant_issued_now": False,
        "approval_collected_now": False,
        **meta,
    }

    sandbox_rollback_policy = {
        "policy_id": "compressed_lifecycle_sandbox_rollback_policy_v1",
        "sandbox_required": True,
        "rollback_required": True,
        "allowed_workspace_path_required": True,
        "forbidden_paths_required": True,
        "timeout_limit_required": True,
        "post_execution_review_required": True,
        "execution_window_opened_now": False,
        **meta,
    }

    validation_factory_binding = {
        "binding_id": "compressed_lifecycle_validation_factory_binding_v1",
        "standards_required": list(FACTORY_STANDARDS_REQUIRED),
        "standard_count": len(FACTORY_STANDARDS_REQUIRED),
        "controlled_provider_readiness_harness_available": factory_post_vr.get("verifier") == "GO",
        "harness_factory_module_candidate": True,
        "validation_factory_pass_required_before_midplatform": True,
        "midplatform_consumption_blocked_until_validation_factory_pass": True,
        **meta,
    }

    dryrun_plan = {
        "plan_id": "compressed_lifecycle_dryrun_plan_v1",
        "next_phase": NEXT_PHASE_GO,
        "dryrun_and_review_merged": True,
        "no_separate_post_review": True,
        "objectives": [
            "generate compressed lifecycle candidate",
            "simulate 7-step lifecycle candidate chain",
            "verify Factory Standard coverage",
            "verify all execution actions remain blocked",
            "no formal artifact generation",
            "no send",
            "no grant",
            "no execution window open",
            "no real dependency check",
        ],
        "formal_request_artifact_generated_now": False,
        "authorization_request_sent_now": False,
        "grant_issued_now": False,
        "execution_window_opened_now": False,
        "real_dependency_check_executed_now": False,
        **meta,
    }

    planning_decision = {
        "decision_id": "compressed_lifecycle_planning_decision_v1",
        "planning_pass": boundary_ok,
        "current_state": CURRENT_STATE,
        "formal_artifact_triple_chain_resumed_now": False,
        "do_not_resume_formal_artifact_triple_chain": True,
        "recommended_next_phase": NEXT_PHASE_GO if boundary_ok else PHASE_ID,
        "final_decision": FINAL_DECISION_GO if boundary_ok else FINAL_DECISION_HOLD,
        **meta,
    }

    policy = {
        "policy_id": "compressed_ocr_authorization_lifecycle_planning_policy_v1",
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
        "final_decision": planning_decision["final_decision"],
        "recommended_next_phase": planning_decision["recommended_next_phase"],
        "current_state": CURRENT_STATE,
        "selected_route": SELECTED_ROUTE,
        "compressed_path_step_count": len(COMPRESSED_PATH),
        "high_risk_count": 0 if boundary_ok else 1,
        **meta,
    }

    result: Dict[str, Any] = {
        "compressed_ocr_authorization_lifecycle_planning_policy": policy,
        "compressed_ocr_authorization_roadmap_input_review": roadmap_input_review,
        "factory_standard_adoption_input_review": factory_adoption_input,
        "compressed_authorization_lifecycle_contract": lifecycle_contract,
        "compressed_authorization_state_machine": state_machine,
        "compressed_lifecycle_boundary_matrix": boundary_matrix,
        "compressed_lifecycle_evidence_requirement": evidence_requirement,
        "compressed_lifecycle_approval_grant_policy": approval_grant_policy,
        "compressed_lifecycle_sandbox_rollback_policy": sandbox_rollback_policy,
        "compressed_lifecycle_validation_factory_binding": validation_factory_binding,
        "compressed_lifecycle_dryrun_plan": dryrun_plan,
        "compressed_lifecycle_planning_decision": planning_decision,
        "non_claims_register": non_claims,
        "summary": summary,
    }
    result.update(stage_contracts)
    return result
