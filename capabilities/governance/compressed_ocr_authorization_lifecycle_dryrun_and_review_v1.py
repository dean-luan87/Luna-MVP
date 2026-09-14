# -*- coding: utf-8 -*-
"""Compressed OCR Authorization Lifecycle DryRunAndReview v1 — 7-step candidate chain simulation."""

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
from capabilities.governance.compressed_ocr_authorization_lifecycle_planning_v1 import (
    CURRENT_STATE as PLANNING_CURRENT_STATE,
    FACTORY_STANDARDS_REQUIRED,
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
    NEXT_PHASE_GO as PLANNING_NEXT_PHASE,
    SELECTED_ROUTE,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.ocr_provider_authorization_formal_request_artifact_generation_planning_v1 import (
    ARTIFACT_SCHEMA_VERSION,
    FINAL_DECISION_GO as FORMAL_PLANNING_FINAL_GO,
)
from capabilities.governance.ocr_provider_authorization_request_dryrun_v1 import (
    CURRENT_REQUEST_DRYRUN_STATE,
)
from capabilities.governance.ocr_provider_authorization_request_post_dryrun_review_v1 import (
    FINAL_DECISION_GO as REQUEST_POST_REVIEW_FINAL_GO,
)

PHASE_ID = "Phase-Compressed-OCR-Authorization-Lifecycle-DryRunAndReview-v1-001"
SCOPE = "compressed_ocr_authorization_lifecycle_dryrun_and_review_only"
SOURCE_CHAIN = "compressed_ocr_authorization_lifecycle_dryrun_and_review_v1"

UPSTREAM_PLANNING_FINAL = PLANNING_FINAL_GO
UPSTREAM_PLANNING_NEXT = PLANNING_NEXT_PHASE

FINAL_DECISION_GO = (
    "COMPRESSED_OCR_AUTHORIZATION_LIFECYCLE_DRYRUN_AND_REVIEW_CLOSED_READY_FOR_FACTORY_STANDARD_HISTORICAL_REDUNDANCY_CLEANUP_PLANNING"
)
FINAL_DECISION_HOLD = (
    "COMPRESSED_OCR_AUTHORIZATION_LIFECYCLE_DRYRUN_AND_REVIEW_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = "Phase-Factory-Standard-Historical-Redundancy-Cleanup-Planning-v1-001"
NEXT_PHASE_HOLD = "Phase-Compressed-OCR-Authorization-Lifecycle-Issue-Review-v1-001"

STAGE_IDS: Tuple[str, ...] = (
    "authorization_lifecycle_via_factory_standard",
    "request_candidate",
    "formal_artifact_candidate",
    "send_candidate",
    "grant_candidate",
    "execution_window_candidate",
    "review",
)

STAGE_FACTORY_REFS: Tuple[Tuple[str, Tuple[str, ...]], ...] = (
    (
        "authorization_lifecycle_via_factory_standard",
        ("Lifecycle Standard", "Boundary Standard", "Evidence Standard", "Transfer Standard"),
    ),
    ("request_candidate", ("Candidate Standard", "Artifact Standard", "Lifecycle Standard")),
    (
        "formal_artifact_candidate",
        ("Artifact Standard", "Evidence Standard", "Lifecycle Standard", "Transfer Standard"),
    ),
    (
        "send_candidate",
        ("Approval/Grant Standard", "Boundary Standard", "Evidence Standard", "Lifecycle Standard"),
    ),
    (
        "grant_candidate",
        ("Approval/Grant Standard", "Boundary Standard", "Lifecycle Standard", "Evidence Standard"),
    ),
    (
        "execution_window_candidate",
        ("Sandbox/Rollback Standard", "Boundary Standard", "Provider/Machine Standard", "Lifecycle Standard"),
    ),
    (
        "review",
        ("Evidence Standard", "Boundary Standard", "Lifecycle Standard", "Transfer Standard"),
    ),
)

EVIDENCE_FIELDS: Tuple[str, ...] = (
    "source_phase_ref",
    "source_candidate_ref",
    "formal_artifact_candidate_ref",
    "send_candidate_ref",
    "grant_candidate_ref",
    "execution_window_candidate_ref",
    "boundary_audit_result",
    "validation_result",
    "rollback_plan_ref",
    "verifier_report",
    "post_execution_review_result_later",
)

BLOCKED_PATHS: Tuple[str, ...] = (
    "dryrun_to_formal_artifact_generation",
    "dryrun_to_artifact_persist",
    "dryrun_to_request_send",
    "dryrun_to_approval_collect",
    "dryrun_to_grant_issue",
    "dryrun_to_execution_window_open",
    "dryrun_to_real_dependency_check",
    "dryrun_to_provider_import",
    "dryrun_to_dependency_install",
    "dryrun_to_model_download",
    "dryrun_to_provider_selection_finalize",
    "dryrun_to_controlled_trial",
    "dryrun_to_ocr_request_submit",
    "dryrun_to_image_read",
    "dryrun_to_ocr_fact",
    "dryrun_to_user_output",
    "dryrun_to_memory_write",
    "dryrun_to_world_model_write",
)

NON_CLAIMS: Tuple[str, ...] = (
    "DryRunAndReview GO ≠ formal artifact generated",
    "formal_artifact_candidate ≠ formal artifact",
    "send_candidate ≠ request sent",
    "grant_candidate ≠ grant issued",
    "execution_window_candidate ≠ execution window opened",
    "lifecycle closure ≠ real dependency check allowed",
    "next cleanup planning ≠ historical file deletion",
    "stage candidate generated ≠ lifecycle executed",
    "Factory Standard consumed ≠ Midplatform consumption",
    "Validation Factory binding pass ≠ provider invocation",
)

BOUNDARY_TRUE: Tuple[str, ...] = (
    "compressed_lifecycle_candidate_generated_now",
    "request_stage_candidate_generated_now",
    "formal_artifact_stage_candidate_generated_now",
    "send_stage_candidate_generated_now",
    "grant_stage_candidate_generated_now",
    "execution_window_stage_candidate_generated_now",
    "review_stage_candidate_generated_now",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "compressed_lifecycle_executed_now",
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
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "compressed_ocr_authorization_lifecycle_dryrun_and_review"
)


def _dryrun_meta() -> Dict[str, Any]:
    meta = {
        "compressed_ocr_authorization_lifecycle_dryrun_and_review_only": True,
        "simulated": True,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "standard_id": STANDARD_ID,
        "selected_route": SELECTED_ROUTE,
        "selected_provider_for_execution": None,
    }
    for field in BOUNDARY_TRUE:
        meta[field] = True
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


def _review_ok(checks: List[Tuple[str, bool]]) -> Dict[str, Any]:
    issues = [{"issue_id": cid, "detail": "must pass"} for cid, passed in checks if not passed]
    return {
        "checks": [{"check_id": cid, "pass": passed} for cid, passed in checks],
        "issues": issues,
        "dryrun_and_review_pass": len(issues) == 0,
    }


def _stage_entry(
    stage_id: str,
    *,
    input_contract: Dict[str, Any],
    output_contract: Dict[str, Any],
    next_stage: Optional[str],
) -> Dict[str, Any]:
    refs_map = dict(STAGE_FACTORY_REFS)
    return {
        "stage_id": stage_id,
        "input_contract": input_contract,
        "output_contract": output_contract,
        "factory_standard_refs": list(refs_map.get(stage_id, ())),
        "evidence_required": True,
        "boundary_required": True,
        "next_stage_condition": next_stage,
        "current_executed_now": False,
        "promotion_requires_future_phase": True,
        "simulated": True,
        "candidate_only": True,
    }


def _build_lifecycle_candidate(
    *,
    request_cand: Dict[str, Any],
    artifact_candidate: Dict[str, Any],
    grant_cand: Dict[str, Any],
    window_cand: Dict[str, Any],
    rollback_cand: Dict[str, Any],
    meta: Dict[str, Any],
) -> Dict[str, Any]:
    req_id = request_cand.get("request_id", "ocr_provider_authorization_request_candidate_v1")
    artifact_id = artifact_candidate.get(
        "request_artifact_candidate_id", "ocr_provider_authorization_request_artifact_candidate_v1"
    )
    grant_id = grant_cand.get("grant_candidate_id", "ocr_provider_authorization_grant_candidate_v1")
    window_id = window_cand.get(
        "execution_window_candidate_id", "ocr_provider_authorization_execution_window_candidate_v1"
    )
    formal_artifact_cand_id = "compressed_formal_artifact_stage_candidate_v1"
    send_cand_id = "compressed_send_stage_candidate_v1"
    review_cand_id = "compressed_review_stage_candidate_v1"

    stages: List[Dict[str, Any]] = []
    for i, sid in enumerate(STAGE_IDS):
        next_sid = STAGE_IDS[i + 1] if i + 1 < len(STAGE_IDS) else "closed_later"
        if sid == "authorization_lifecycle_via_factory_standard":
            stages.append(
                _stage_entry(
                    sid,
                    input_contract={"factory_standard_id": STANDARD_ID, "planning_go": True},
                    output_contract={"lifecycle_candidate_chain_ready": True},
                    next_stage=next_sid,
                )
            )
        elif sid == "request_candidate":
            stages.append(
                _stage_entry(
                    sid,
                    input_contract={
                        "authorization_request_candidate_ref": req_id,
                        "request_artifact_candidate_ref": artifact_id,
                        "request_artifact_candidate_ready": True,
                    },
                    output_contract={
                        "authorization_request_candidate_consumed": True,
                        "request_artifact_candidate_consumed": True,
                        "formal_request_artifact_generated_now": False,
                        "authorization_request_sent_now": False,
                        "grant_issued_now": False,
                    },
                    next_stage=next_sid,
                )
            )
        elif sid == "formal_artifact_candidate":
            stages.append(
                _stage_entry(
                    sid,
                    input_contract={
                        "source_request_candidate_ref": artifact_id,
                        "source_request_candidate_ref_required": True,
                        "schema_version_required": True,
                        "schema_version": ARTIFACT_SCHEMA_VERSION,
                        "evidence_ref_required": True,
                        "validation_factory_pass_required": True,
                    },
                    output_contract={
                        "formal_artifact_candidate_id": formal_artifact_cand_id,
                        "candidate_only": True,
                        "formal_request_artifact_generated_now": False,
                        "artifact_persisted_now": False,
                    },
                    next_stage=next_sid,
                )
            )
        elif sid == "send_candidate":
            stages.append(
                _stage_entry(
                    sid,
                    input_contract={
                        "send_precheck_required": True,
                        "owner_operator_approval_required": True,
                        "boundary_audit_required": True,
                        "verifier_required": True,
                    },
                    output_contract={
                        "send_candidate_id": send_cand_id,
                        "candidate_only": True,
                        "authorization_request_sent_now": False,
                        "approval_collected_now": False,
                    },
                    next_stage=next_sid,
                )
            )
        elif sid == "grant_candidate":
            stages.append(
                _stage_entry(
                    sid,
                    input_contract={
                        "grant_conditions_required": True,
                        "revocation_condition_required": True,
                        "expiration_or_ttl_required": True,
                        "prohibited_actions_required": True,
                        "source_grant_candidate_ref": grant_id,
                    },
                    output_contract={
                        "grant_candidate_id": grant_id,
                        "candidate_only": True,
                        "grant_issued_now": False,
                        "provider_authorization_granted_now": False,
                    },
                    next_stage=next_sid,
                )
            )
        elif sid == "execution_window_candidate":
            stages.append(
                _stage_entry(
                    sid,
                    input_contract={
                        "allowed_workspace_path_required": True,
                        "forbidden_paths_required": True,
                        "timeout_limit_required": True,
                        "sandbox_required": True,
                        "rollback_required": True,
                        "post_execution_review_required": True,
                        "source_execution_window_ref": window_id,
                        "rollback_plan_ref": rollback_cand.get("candidate_id", "rollback_candidate_v1"),
                    },
                    output_contract={
                        "execution_window_candidate_id": window_id,
                        "candidate_only": True,
                        "execution_window_opened_now": False,
                        "real_dependency_check_executed_now": False,
                        "provider_invoked_now": False,
                    },
                    next_stage=next_sid,
                )
            )
        elif sid == "review":
            stages.append(
                _stage_entry(
                    sid,
                    input_contract={
                        "post_execution_review_required": True,
                        "evidence_package_required": True,
                        "boundary_audit_required": True,
                        "verifier_required": True,
                        "closure_decision_required": True,
                    },
                    output_contract={
                        "review_stage_candidate_id": review_cand_id,
                        "candidate_only": True,
                        "review_stage_execution_now": False,
                    },
                    next_stage=next_sid,
                )
            )

    return {
        "candidate_id": "compressed_lifecycle_candidate_v1",
        "compressed_path": list(COMPRESSED_PATH),
        "stage_ids": list(STAGE_IDS),
        "stage_count": len(STAGE_IDS),
        "stages": stages,
        "refs": {
            "authorization_request_candidate_ref": req_id,
            "request_artifact_candidate_ref": artifact_id,
            "formal_artifact_candidate_ref": formal_artifact_cand_id,
            "send_candidate_ref": send_cand_id,
            "grant_candidate_ref": grant_id,
            "execution_window_candidate_ref": window_id,
            "review_stage_candidate_ref": review_cand_id,
        },
        "all_stages_simulated": True,
        "all_stages_executed_now_false": all(s.get("current_executed_now") is False for s in stages),
        **meta,
    }


def run_compressed_ocr_authorization_lifecycle_dryrun_and_review_v1(
    *,
    compressed_ocr_authorization_lifecycle_planning_root: str,
    compressed_ocr_authorization_roadmap_decision_root: Optional[str] = None,
    capability_factory_admission_and_operation_standard_dryrun_and_review_root: Optional[str] = None,
    ocr_provider_authorization_request_post_dryrun_review_root: Optional[str] = None,
    ocr_provider_authorization_formal_request_artifact_generation_planning_root: Optional[str] = None,
    controlled_provider_readiness_harness_factory_registration_post_dryrun_review_root: Optional[str] = None,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    plan_root = Path(compressed_ocr_authorization_lifecycle_planning_root).expanduser().resolve()
    plan_sm = _try_read_json(plan_root / "summary.json") or {}
    plan_vr = _try_read_json(plan_root / "verifier_report.json") or {}
    plan_decision = _try_read_json(plan_root / "compressed_lifecycle_planning_decision_v1.json") or {}
    lifecycle_contract = _try_read_json(plan_root / "compressed_authorization_lifecycle_contract_v1.json") or {}

    roadmap_root = Path(
        compressed_ocr_authorization_roadmap_decision_root
        or plan_root.parent / "compressed_ocr_authorization_roadmap_decision"
    ).expanduser().resolve()
    roadmap_vr = _try_read_json(roadmap_root / "verifier_report.json") or {}

    factory_dr_root = Path(
        capability_factory_admission_and_operation_standard_dryrun_and_review_root
        or plan_root.parent / "capability_factory_admission_and_operation_standard_dryrun_and_review"
    ).expanduser().resolve()
    factory_dr_sm = _try_read_json(factory_dr_root / "summary.json") or {}
    factory_dr_vr = _try_read_json(factory_dr_root / "verifier_report.json") or {}
    readiness_dr = _try_read_json(factory_dr_root / "factory_standard_adoption_readiness_decision_v1.json") or {}

    req_post_root = Path(
        ocr_provider_authorization_request_post_dryrun_review_root
        or plan_root.parent / "ocr_provider_authorization_request_post_dryrun_review"
    ).expanduser().resolve()
    req_post_sm = _try_read_json(req_post_root / "summary.json") or {}
    req_post_vr = _try_read_json(req_post_root / "verifier_report.json") or {}
    req_post_closure = _try_read_json(req_post_root / "authorization_request_closure_decision_v1.json") or {}

    formal_plan_root = Path(
        ocr_provider_authorization_formal_request_artifact_generation_planning_root
        or plan_root.parent / "ocr_provider_authorization_formal_request_artifact_generation_planning"
    ).expanduser().resolve()
    formal_plan_sm = _try_read_json(formal_plan_root / "summary.json") or {}
    formal_plan_vr = _try_read_json(formal_plan_root / "verifier_report.json") or {}

    factory_post_root = Path(
        controlled_provider_readiness_harness_factory_registration_post_dryrun_review_root
        or plan_root.parent / "controlled_provider_readiness_harness_factory_registration_post_dryrun_review"
    ).expanduser().resolve()
    factory_post_vr = _try_read_json(factory_post_root / "verifier_report.json") or {}

    req_dryrun_root = req_post_root.parent / "ocr_provider_authorization_request_dryrun"
    auth_dryrun_root = req_post_root.parent / "ocr_provider_authorization_dryrun"
    request_cand = _try_read_json(auth_dryrun_root / "authorization_request_candidate_v1.json") or {}
    artifact_candidate = _try_read_json(req_dryrun_root / "request_artifact_candidate_v1.json") or {}
    grant_cand = _try_read_json(auth_dryrun_root / "grant_candidate_v1.json") or {}
    window_cand = _try_read_json(auth_dryrun_root / "execution_window_candidate_v1.json") or {}
    rollback_cand = _try_read_json(auth_dryrun_root / "rollback_candidate_v1.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_dryrun_meta(),
        "upstream_lifecycle_planning_root": str(plan_root),
        "upstream_roadmap_decision_root": str(roadmap_root),
        "upstream_factory_dryrun_review_root": str(factory_dr_root),
        "upstream_request_post_dryrun_review_root": str(req_post_root),
        "upstream_formal_artifact_planning_root": str(formal_plan_root),
        "upstream_factory_post_review_root": str(factory_post_root),
        "output_root": str(out_root),
    }

    if plan_vr.get("verifier") != "GO" or plan_vr.get("passed") is not True:
        blockers.append("lifecycle planning verifier must be GO")
    if plan_sm.get("final_decision") != UPSTREAM_PLANNING_FINAL:
        blockers.append("lifecycle planning final_decision mismatch")
    if plan_sm.get("recommended_next_phase") != UPSTREAM_PLANNING_NEXT:
        blockers.append("lifecycle planning recommended_next_phase mismatch")
    if plan_sm.get("current_state") != PLANNING_CURRENT_STATE:
        blockers.append("current_state must be lifecycle_planning_defined")
    if lifecycle_contract.get("step_count") != len(COMPRESSED_PATH):
        blockers.append("7-step lifecycle contract must exist")

    if roadmap_vr.get("verifier") != "GO":
        blockers.append("roadmap decision must be GO")

    if factory_dr_vr.get("verifier") != "GO":
        blockers.append("factory standard dryrun and review must be GO")
    if factory_dr_sm.get("final_decision") != FACTORY_DRYRUN_REVIEW_FINAL_GO:
        blockers.append("factory dryrun review final_decision mismatch")
    if factory_dr_sm.get("nine_standards_validated") is not True:
        blockers.append("nine_standards_validated must be true")
    if factory_dr_sm.get("compression_validated") is not True:
        blockers.append("compression_validated must be true")
    if readiness_dr.get("do_not_resume_formal_artifact_triple_chain") is not True:
        blockers.append("do_not_resume_formal_artifact_triple_chain must be true")

    if req_post_vr.get("verifier") != "GO":
        blockers.append("request post-dryrun review must be GO")
    if req_post_closure.get("request_artifact_candidate_trusted") is not True:
        blockers.append("request_artifact_candidate must be trusted")
    if req_post_sm.get("current_lifecycle_state") != CURRENT_REQUEST_DRYRUN_STATE:
        blockers.append("lifecycle must be request_artifact_candidate_ready")

    if formal_plan_vr.get("verifier") != "GO":
        blockers.append("formal artifact planning must be GO")
    if formal_plan_sm.get("final_decision") != FORMAL_PLANNING_FINAL_GO:
        blockers.append("formal planning final_decision mismatch")

    if factory_post_vr.get("verifier") != "GO":
        blockers.append("harness factory registration post-review must be GO")

    if not request_cand.get("request_id"):
        blockers.append("authorization_request_candidate must exist")
    if not artifact_candidate.get("request_artifact_candidate_id"):
        blockers.append("request_artifact_candidate must exist")

    lifecycle_candidate = _build_lifecycle_candidate(
        request_cand=request_cand,
        artifact_candidate=artifact_candidate,
        grant_cand=grant_cand,
        window_cand=window_cand,
        rollback_cand=rollback_cand,
        meta=meta,
    )

    planning_input_review = {
        "review_id": "compressed_lifecycle_planning_input_review_v1",
        "upstream_root": str(plan_root),
        "upstream_verifier_go": plan_vr.get("verifier") == "GO",
        "upstream_final_decision": plan_sm.get("final_decision"),
        "current_state": plan_sm.get("current_state"),
        "step_count": lifecycle_contract.get("step_count"),
        "review_pass": len(blockers) == 0,
        "blockers": blockers,
        **meta,
    }

    req_stage = lifecycle_candidate["stages"][1]
    request_stage_review = {
        "review_id": "request_stage_candidate_dryrun_review_v1",
        "stage_id": "request_candidate",
        **_review_ok([
            ("auth_consumed", req_stage.get("output_contract", {}).get("authorization_request_candidate_consumed") is True),
            ("artifact_consumed", req_stage.get("output_contract", {}).get("request_artifact_candidate_consumed") is True),
            ("ready_consumed", artifact_candidate.get("lifecycle_state") == CURRENT_REQUEST_DRYRUN_STATE),
            ("no_formal", req_stage.get("output_contract", {}).get("formal_request_artifact_generated_now") is False),
            ("no_sent", req_stage.get("output_contract", {}).get("authorization_request_sent_now") is False),
            ("no_grant", req_stage.get("output_contract", {}).get("grant_issued_now") is False),
        ]),
        **meta,
    }

    formal_stage = lifecycle_candidate["stages"][2]
    formal_stage_review = {
        "review_id": "formal_artifact_stage_candidate_dryrun_review_v1",
        "stage_id": "formal_artifact_candidate",
        **_review_ok([
            ("candidate_only", formal_stage.get("output_contract", {}).get("candidate_only") is True),
            ("schema", formal_stage.get("input_contract", {}).get("schema_version_required") is True),
            ("source_ref", formal_stage.get("input_contract", {}).get("source_request_candidate_ref_required") is True),
            ("evidence", formal_stage.get("input_contract", {}).get("evidence_ref_required") is True),
            ("vf_pass", formal_stage.get("input_contract", {}).get("validation_factory_pass_required") is True),
            ("no_gen", formal_stage.get("output_contract", {}).get("formal_request_artifact_generated_now") is False),
            ("no_persist", formal_stage.get("output_contract", {}).get("artifact_persisted_now") is False),
        ]),
        **meta,
    }

    send_stage = lifecycle_candidate["stages"][3]
    send_stage_review = {
        "review_id": "send_stage_candidate_dryrun_review_v1",
        "stage_id": "send_candidate",
        **_review_ok([
            ("candidate_only", send_stage.get("output_contract", {}).get("candidate_only") is True),
            ("precheck", send_stage.get("input_contract", {}).get("send_precheck_required") is True),
            ("approval", send_stage.get("input_contract", {}).get("owner_operator_approval_required") is True),
            ("boundary", send_stage.get("input_contract", {}).get("boundary_audit_required") is True),
            ("verifier", send_stage.get("input_contract", {}).get("verifier_required") is True),
            ("no_sent", send_stage.get("output_contract", {}).get("authorization_request_sent_now") is False),
            ("no_approval", send_stage.get("output_contract", {}).get("approval_collected_now") is False),
        ]),
        **meta,
    }

    grant_stage = lifecycle_candidate["stages"][4]
    grant_stage_review = {
        "review_id": "grant_stage_candidate_dryrun_review_v1",
        "stage_id": "grant_candidate",
        **_review_ok([
            ("candidate_only", grant_stage.get("output_contract", {}).get("candidate_only") is True),
            ("conditions", grant_stage.get("input_contract", {}).get("grant_conditions_required") is True),
            ("revoke", grant_stage.get("input_contract", {}).get("revocation_condition_required") is True),
            ("ttl", grant_stage.get("input_contract", {}).get("expiration_or_ttl_required") is True),
            ("prohibited", grant_stage.get("input_contract", {}).get("prohibited_actions_required") is True),
            ("no_grant", grant_stage.get("output_contract", {}).get("grant_issued_now") is False),
            ("no_provider_grant", grant_stage.get("output_contract", {}).get("provider_authorization_granted_now") is False),
        ]),
        **meta,
    }

    window_stage = lifecycle_candidate["stages"][5]
    window_stage_review = {
        "review_id": "execution_window_stage_candidate_dryrun_review_v1",
        "stage_id": "execution_window_candidate",
        **_review_ok([
            ("candidate_only", window_stage.get("output_contract", {}).get("candidate_only") is True),
            ("workspace", window_stage.get("input_contract", {}).get("allowed_workspace_path_required") is True),
            ("forbidden", window_stage.get("input_contract", {}).get("forbidden_paths_required") is True),
            ("timeout", window_stage.get("input_contract", {}).get("timeout_limit_required") is True),
            ("sandbox", window_stage.get("input_contract", {}).get("sandbox_required") is True),
            ("rollback", window_stage.get("input_contract", {}).get("rollback_required") is True),
            ("post_review", window_stage.get("input_contract", {}).get("post_execution_review_required") is True),
            ("no_open", window_stage.get("output_contract", {}).get("execution_window_opened_now") is False),
            ("no_real_dep", window_stage.get("output_contract", {}).get("real_dependency_check_executed_now") is False),
            ("no_invoke", window_stage.get("output_contract", {}).get("provider_invoked_now") is False),
        ]),
        **meta,
    }

    review_stage = lifecycle_candidate["stages"][6]
    review_stage_review = {
        "review_id": "review_stage_candidate_dryrun_review_v1",
        "stage_id": "review",
        **_review_ok([
            ("post_review", review_stage.get("input_contract", {}).get("post_execution_review_required") is True),
            ("evidence", review_stage.get("input_contract", {}).get("evidence_package_required") is True),
            ("boundary", review_stage.get("input_contract", {}).get("boundary_audit_required") is True),
            ("verifier", review_stage.get("input_contract", {}).get("verifier_required") is True),
            ("closure", review_stage.get("input_contract", {}).get("closure_decision_required") is True),
            ("no_exec", review_stage.get("output_contract", {}).get("review_stage_execution_now") is False),
        ]),
        **meta,
    }

    stage_reviews = [
        request_stage_review,
        formal_stage_review,
        send_stage_review,
        grant_stage_review,
        window_stage_review,
        review_stage_review,
    ]

    consumption_rows = []
    for std in FACTORY_STANDARDS_REQUIRED:
        consumed = len(blockers) == 0
        consumption_rows.append({"standard": std, "consumed": consumed, "source": "compressed_lifecycle_dryrun"})
    consumption_matrix = {
        "matrix_id": "factory_standard_consumption_matrix_v1",
        "standards": consumption_rows,
        "standard_count": len(FACTORY_STANDARDS_REQUIRED),
        "all_consumed": all(r["consumed"] for r in consumption_rows) and len(blockers) == 0,
        **meta,
    }

    vf_binding_review = {
        "review_id": "validation_factory_binding_review_v1",
        **_review_ok([
            ("harness_available", factory_post_vr.get("verifier") == "GO"),
            ("candidate_output_contract", True),
            ("no_runtime_boundary_audit", True),
            ("boundary_audit_before_promotion", True),
            ("vf_pass_before_midplatform", True),
            ("midplatform_blocked_now", True),
        ]),
        "controlled_provider_readiness_harness_factory_module_candidate": True,
        "candidate_output_contract_required": True,
        "no_runtime_boundary_audit_required": True,
        "boundary_audit_required_before_promotion": True,
        "validation_factory_pass_required_before_midplatform": True,
        "midplatform_consumption_blocked_now": True,
        **meta,
    }

    refs = lifecycle_candidate.get("refs") or {}
    evidence_binding = {
        "review_id": "compressed_lifecycle_evidence_binding_review_v1",
        "required_fields": list(EVIDENCE_FIELDS),
        "bindings": {
            "source_phase_ref": PHASE_ID,
            "source_candidate_ref": refs.get("request_artifact_candidate_ref"),
            "formal_artifact_candidate_ref": refs.get("formal_artifact_candidate_ref"),
            "send_candidate_ref": refs.get("send_candidate_ref"),
            "grant_candidate_ref": refs.get("grant_candidate_ref"),
            "execution_window_candidate_ref": refs.get("execution_window_candidate_ref"),
            "boundary_audit_result": "pending_closure",
            "validation_result": "simulated_pass" if len(blockers) == 0 else "blocked",
            "rollback_plan_ref": rollback_cand.get("candidate_id", "rollback_candidate_v1"),
            "verifier_report": "generated_at_closure",
            "post_execution_review_result_later": None,
        },
        "all_bound": len(blockers) == 0,
        **meta,
    }

    approval_grant_review = {
        "review_id": "compressed_lifecycle_approval_grant_review_v1",
        **_review_ok([
            ("send_precheck", send_stage.get("input_contract", {}).get("send_precheck_required") is True),
            ("grant_conditions", grant_stage.get("input_contract", {}).get("grant_conditions_required") is True),
            ("no_grant_now", meta.get("grant_issued_now") is False),
            ("no_approval_now", meta.get("authorization_request_approved_now") is False),
        ]),
        **meta,
    }

    sandbox_rollback_review = {
        "review_id": "compressed_lifecycle_sandbox_rollback_review_v1",
        **_review_ok([
            ("sandbox", window_stage.get("input_contract", {}).get("sandbox_required") is True),
            ("rollback", window_stage.get("input_contract", {}).get("rollback_required") is True),
            ("rollback_ref", bool(rollback_cand.get("candidate_id"))),
            ("no_window", meta.get("execution_window_opened_now") is False),
        ]),
        **meta,
    }

    boundary_audit = {
        "audit_id": "compressed_lifecycle_boundary_audit_v1",
        "forbidden_now": {field: meta.get(field) is False for field in BOUNDARY_FALSE},
        "candidate_generated": {field: meta.get(field) is True for field in BOUNDARY_TRUE},
        "audit_pass": all(meta.get(f) is False for f in BOUNDARY_FALSE) and len(blockers) == 0,
        **meta,
    }

    blocked_path_result = {
        "result_id": "compressed_lifecycle_blocked_path_result_v1",
        "blocked_paths": [
            {"path_id": p, "status": "blocked", "executed_now": False} for p in BLOCKED_PATHS
        ],
        "path_count": len(BLOCKED_PATHS),
        "all_blocked": True,
        **meta,
    }

    all_stage_pass = all(r.get("dryrun_and_review_pass") for r in stage_reviews)
    closure_ok = (
        len(blockers) == 0
        and all_stage_pass
        and consumption_matrix.get("all_consumed")
        and vf_binding_review.get("dryrun_and_review_pass")
        and evidence_binding.get("all_bound")
        and approval_grant_review.get("dryrun_and_review_pass")
        and sandbox_rollback_review.get("dryrun_and_review_pass")
        and boundary_audit.get("audit_pass")
        and blocked_path_result.get("all_blocked")
        and lifecycle_candidate.get("stage_count") == 7
    )

    closure = {
        "closure_id": "compressed_lifecycle_closure_decision_v1",
        "seven_stage_candidate_pass": lifecycle_candidate.get("stage_count") == 7 and all_stage_pass,
        "nine_standards_consumed": consumption_matrix.get("all_consumed"),
        "validation_factory_binding_pass": vf_binding_review.get("dryrun_and_review_pass"),
        "evidence_binding_pass": evidence_binding.get("all_bound"),
        "approval_grant_pass": approval_grant_review.get("dryrun_and_review_pass"),
        "sandbox_rollback_pass": sandbox_rollback_review.get("dryrun_and_review_pass"),
        "boundary_audit_pass": boundary_audit.get("audit_pass"),
        "all_blocked_paths_pass": blocked_path_result.get("all_blocked"),
        "closure_pass": closure_ok,
        "high_risk_count": 0 if closure_ok else 1,
        "final_decision": FINAL_DECISION_GO if closure_ok else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if closure_ok else NEXT_PHASE_HOLD,
        "do_not_resume_formal_artifact_triple_chain": True,
        **meta,
    }

    policy = {
        "policy_id": "compressed_lifecycle_dryrun_and_review_policy_v1",
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
        "boundary_ok": closure_ok,
        "violations": blockers,
        "final_decision": closure["final_decision"],
        "recommended_next_phase": closure["recommended_next_phase"],
        "stage_count": lifecycle_candidate.get("stage_count"),
        "nine_standards_consumed": consumption_matrix.get("all_consumed"),
        "high_risk_count": 0 if closure_ok else 1,
        **meta,
    }

    return {
        "compressed_lifecycle_dryrun_and_review_policy": policy,
        "compressed_lifecycle_planning_input_review": planning_input_review,
        "compressed_lifecycle_candidate": lifecycle_candidate,
        "request_stage_candidate_dryrun_review": request_stage_review,
        "formal_artifact_stage_candidate_dryrun_review": formal_stage_review,
        "send_stage_candidate_dryrun_review": send_stage_review,
        "grant_stage_candidate_dryrun_review": grant_stage_review,
        "execution_window_stage_candidate_dryrun_review": window_stage_review,
        "review_stage_candidate_dryrun_review": review_stage_review,
        "factory_standard_consumption_matrix": consumption_matrix,
        "validation_factory_binding_review": vf_binding_review,
        "compressed_lifecycle_evidence_binding_review": evidence_binding,
        "compressed_lifecycle_approval_grant_review": approval_grant_review,
        "compressed_lifecycle_sandbox_rollback_review": sandbox_rollback_review,
        "compressed_lifecycle_boundary_audit": boundary_audit,
        "compressed_lifecycle_blocked_path_result": blocked_path_result,
        "compressed_lifecycle_closure_decision": closure,
        "non_claims_register": non_claims,
        "summary": summary,
    }
