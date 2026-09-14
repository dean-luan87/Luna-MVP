# -*- coding: utf-8 -*-
"""OCR Real Dependency Formal Execution Request Generation Planning v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.capability_factory_authorization_standard_extension_planning_v1 import (
    AUTHORIZATION_STANDARD_ID,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.ocr_real_dependency_execution_authorization_dryrun_and_review_v1 import (
    BLOCKED_PATHS as DRYRUN_BLOCKED_PATHS,
    SCOPE_ALLOWED_CHECKS,
)
from capabilities.governance.ocr_real_dependency_execution_authorization_planning_v1 import (
    EVIDENCE_ARTIFACTS,
)
from capabilities.governance.ocr_real_dependency_execution_request_generation_roadmap_decision_v1 import (
    FINAL_DECISION_GO as UPSTREAM_ROADMAP_FINAL_GO,
    NEXT_PHASE_GO as UPSTREAM_ROADMAP_NEXT_PHASE,
    SELECTED_ROUTE,
)

PHASE_ID = "Phase-OCR-Real-Dependency-Formal-Execution-Request-Generation-Planning-v1-001"
SCOPE = "formal_execution_request_generation_planning_only"
SOURCE_CHAIN = "ocr_real_dependency_formal_execution_request_generation_planning_v1"

UPSTREAM_ROADMAP_FINAL = UPSTREAM_ROADMAP_FINAL_GO
UPSTREAM_ROADMAP_NEXT = UPSTREAM_ROADMAP_NEXT_PHASE

FINAL_DECISION_GO = (
    "OCR_REAL_DEPENDENCY_FORMAL_EXECUTION_REQUEST_GENERATION_PLANNING_READY_FOR_DRYRUN_AND_REVIEW"
)
FINAL_DECISION_HOLD = (
    "OCR_REAL_DEPENDENCY_FORMAL_EXECUTION_REQUEST_GENERATION_PLANNING_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = "Phase-OCR-Real-Dependency-Formal-Execution-Request-Generation-DryRunAndReview-v1-001"
NEXT_PHASE_HOLD = "Phase-OCR-Real-Dependency-Formal-Execution-Request-Generation-Issue-Review-v1-001"

ARTIFACT_SCHEMA_VERSION = "formal_execution_request_artifact_schema_v1"
GENERATION_POLICY_VERSION = "formal_execution_request_generation_policy_v1"

FIELD_SOURCE_BINDINGS: Tuple[Tuple[str, str], ...] = (
    ("execution_authorization_request_candidate", "formal request artifact"),
    ("execution_grant_candidate", "grant candidate ref"),
    ("execution_window_candidate", "window candidate ref"),
    ("allowed_check_plan_candidate", "requested allowed checks"),
    ("forbidden_action_review", "forbidden actions ref"),
    ("evidence_collection_candidate", "evidence collection ref"),
    ("rollback_failure_route_candidate", "rollback ref"),
    ("validation_gate_path_dryrun_review", "validation gate path ref"),
    ("domain_config_candidate", "source domain config ref"),
    ("Factory Authorization Standard", "authorization standard ref"),
    ("Validation Engineering", "validation engineering ref"),
)

VALIDATION_RULES: Tuple[str, ...] = (
    "request_type_must_equal_ocr_real_dependency_execution_authorization_request",
    "artifact_version_present",
    "lifecycle_state_valid",
    "provider_domain_must_equal_ocr",
    "authorization_target_must_equal_real_dependency_check_execution",
    "target_scope_excludes_provider_selection_finalize",
    "target_scope_excludes_controlled_trial",
    "target_scope_excludes_production_runtime",
    "allowed_checks_must_remain_not_executed_now",
    "selected_provider_for_execution_must_remain_null",
    "execution_window_must_not_be_opened",
    "request_must_not_be_sent",
    "grant_must_not_be_issued",
    "provider_import_must_remain_false",
    "evidence_collection_required",
    "validation_gate_path_required",
    "formal_request_generated_remains_false_in_planning",
)

GATE_BINDINGS: Tuple[str, ...] = (
    "AuthorizationValidationGate",
    "BoundaryGate",
    "EvidenceChainValidator",
    "NoRuntimeBoundaryAudit",
    "ControlledProviderReadinessHarness",
    "Validation Factory",
)

BLOCKED_PATHS: Tuple[str, ...] = (
    "planning_to_formal_execution_request_generation",
    "planning_to_request_persist",
    "planning_to_request_send",
    "planning_to_approval_collect",
    "planning_to_grant_issue",
    "planning_to_execution_window_open",
    "planning_to_real_dependency_check",
    "planning_to_package_check",
    "planning_to_provider_import",
    "planning_to_model_cache_check",
    "planning_to_model_file_hash_check",
    "planning_to_dependency_install",
    "planning_to_model_download",
    "planning_to_cache_mutation",
    "planning_to_provider_invoke",
    "planning_to_provider_selection_finalize",
    "planning_to_controlled_trial",
    "planning_to_ocr_request_submit",
    "planning_to_image_read",
    "planning_to_crop",
    "planning_to_ocr_fact",
    "planning_to_user_output",
    "planning_to_memory_write",
    "planning_to_world_model_write",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Formal Request Generation Planning GO ≠ formal request generated",
    "formal request schema planned ≠ request sent",
    "next DryRunAndReview ≠ grant issued",
    "request generation planning ≠ execution window opened",
    "request generation planning ≠ provider import allowed",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "formal_execution_request_generated_now",
    "formal_execution_request_persisted_now",
    "formal_execution_request_sent_now",
    "formal_execution_request_approved_now",
    "execution_grant_issued_now",
    "execution_window_opened_now",
    "real_dependency_check_executed_now",
    "package_check_executed_now",
    "provider_import_check_executed_now",
    "model_cache_path_check_executed_now",
    "model_file_existence_check_executed_now",
    "model_file_hash_check_executed_now",
    "provider_initialization_dry_check_executed_now",
    "runtime_smoke_check_executed_now",
    "sample_ocr_check_executed_now",
    "provider_imported_now",
    "provider_invoked_now",
    "dependency_install_executed_now",
    "model_download_executed_now",
    "cache_mutation_executed_now",
    "provider_selection_finalized_now",
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
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_real_dependency_formal_execution_request_generation_planning"
)


def _planning_meta() -> Dict[str, Any]:
    meta = {
        "formal_execution_request_generation_planning_only": True,
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


def run_ocr_real_dependency_formal_execution_request_generation_planning_v1(
    *,
    ocr_real_dependency_execution_request_generation_roadmap_decision_root: str,
    ocr_real_dependency_execution_authorization_dryrun_and_review_root: str,
    ocr_real_dependency_execution_authorization_planning_root: Optional[str] = None,
    ocr_real_dependency_authorization_via_factory_standard_dryrun_and_review_root: Optional[str] = None,
    midplatform_validation_engineering_separation_dryrun_and_review_root: Optional[str] = None,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    roadmap_root = Path(
        ocr_real_dependency_execution_request_generation_roadmap_decision_root
    ).expanduser().resolve()
    dryrun_root = Path(
        ocr_real_dependency_execution_authorization_dryrun_and_review_root
    ).expanduser().resolve()
    plan_root = Path(
        ocr_real_dependency_execution_authorization_planning_root
        or dryrun_root.parent / "ocr_real_dependency_execution_authorization_planning"
    ).expanduser().resolve()
    ocr_dr_root = Path(
        ocr_real_dependency_authorization_via_factory_standard_dryrun_and_review_root
        or dryrun_root.parent / "ocr_real_dependency_authorization_via_factory_standard_dryrun_and_review"
    ).expanduser().resolve()
    val_dr_root = Path(
        midplatform_validation_engineering_separation_dryrun_and_review_root
        or dryrun_root.parent / "midplatform_validation_engineering_separation_dryrun_and_review"
    ).expanduser().resolve()

    roadmap_sm = _try_read_json(roadmap_root / "summary.json") or {}
    roadmap_vr = _try_read_json(roadmap_root / "verifier_report.json") or {}
    dryrun_sm = _try_read_json(dryrun_root / "summary.json") or {}
    dryrun_vr = _try_read_json(dryrun_root / "verifier_report.json") or {}
    dryrun_blocked = _try_read_json(
        dryrun_root / "execution_authorization_blocked_path_result_v1.json"
    ) or {}

    request_cand = _try_read_json(
        dryrun_root / "execution_authorization_request_candidate_v1.json"
    ) or {}
    grant_cand = _try_read_json(dryrun_root / "execution_grant_candidate_v1.json") or {}
    window_cand = _try_read_json(dryrun_root / "execution_window_candidate_v1.json") or {}
    allowed_cand = _try_read_json(dryrun_root / "allowed_check_plan_candidate_v1.json") or {}
    evidence_cand = _try_read_json(dryrun_root / "evidence_collection_candidate_v1.json") or {}
    gate_review = _try_read_json(dryrun_root / "validation_gate_path_dryrun_review_v1.json") or {}

    domain_config_ref = str(
        ocr_dr_root / "ocr_real_dependency_domain_config_candidate_v1.json"
    )

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_planning_meta(),
        "upstream_roadmap_decision_root": str(roadmap_root),
        "upstream_dryrun_and_review_root": str(dryrun_root),
        "upstream_execution_authorization_planning_root": str(plan_root),
        "upstream_ocr_via_factory_dryrun_review_root": str(ocr_dr_root),
        "upstream_validation_separation_dryrun_review_root": str(val_dr_root),
        "output_root": str(out_root),
    }

    if roadmap_vr.get("verifier") != "GO":
        blockers.append("roadmap decision verifier must be GO")
    if roadmap_sm.get("final_decision") != UPSTREAM_ROADMAP_FINAL:
        blockers.append("roadmap final_decision mismatch")
    if roadmap_sm.get("recommended_next_phase") != UPSTREAM_ROADMAP_NEXT:
        blockers.append("roadmap recommended_next_phase mismatch")
    if roadmap_sm.get("selected_route") != SELECTED_ROUTE:
        blockers.append("selected_route must be Route A")
    if dryrun_vr.get("verifier") != "GO":
        blockers.append("execution authorization dryrun must be GO")
    if not request_cand.get("request_candidate_id"):
        blockers.append("execution_authorization_request_candidate required")
    if not grant_cand.get("grant_candidate_id"):
        blockers.append("execution_grant_candidate required")
    if not window_cand.get("execution_window_candidate_id"):
        blockers.append("execution_window_candidate required")
    if not allowed_cand.get("candidate_id"):
        blockers.append("allowed_check_plan_candidate required")
    if not evidence_cand.get("candidate_id"):
        blockers.append("evidence_collection_candidate required")
    if gate_review.get("simulated_gate_path_pass") is not True:
        blockers.append("validation gate path must simulated pass")

    if request_cand.get("formal_request_generated_now") is True:
        blockers.append("formal_request_generated_now must be false")
    if request_cand.get("request_sent_now") is True:
        blockers.append("request_sent_now must be false")
    if grant_cand.get("grant_issued_now") is True:
        blockers.append("grant_issued_now must be false")
    if window_cand.get("execution_window_opened_now") is True:
        blockers.append("execution_window_opened_now must be false")

    for item in allowed_cand.get("checks") or []:
        if item.get("current_executed_now") is True:
            blockers.append("all allowed checks current_executed_now=false required")
            break

    dryrun_blocked_ok = dryrun_blocked.get("all_blocked") is True

    roadmap_input = {
        "review_id": "execution_request_generation_roadmap_input_review_v1",
        "upstream_roadmap_root": str(roadmap_root),
        "verifier_go": roadmap_vr.get("verifier") == "GO",
        "final_decision": roadmap_sm.get("final_decision"),
        "selected_route": roadmap_sm.get("selected_route"),
        "review_pass": roadmap_vr.get("verifier") == "GO"
        and roadmap_sm.get("final_decision") == UPSTREAM_ROADMAP_FINAL
        and roadmap_sm.get("selected_route") == SELECTED_ROUTE,
        "blockers": blockers,
        **meta,
    }

    refs = {
        "source_execution_authorization_request_candidate_ref": str(
            dryrun_root / "execution_authorization_request_candidate_v1.json"
        ),
        "source_domain_config_ref": domain_config_ref,
        "execution_grant_candidate_ref": str(dryrun_root / "execution_grant_candidate_v1.json"),
        "execution_window_candidate_ref": str(dryrun_root / "execution_window_candidate_v1.json"),
        "evidence_collection_ref": str(dryrun_root / "evidence_collection_candidate_v1.json"),
        "rollback_failure_route_ref": str(
            dryrun_root / "rollback_failure_route_candidate_v1.json"
        ),
        "validation_gate_path_ref": str(
            dryrun_root / "validation_gate_path_dryrun_review_v1.json"
        ),
        "forbidden_actions_ref": str(dryrun_root / "forbidden_action_review_v1.json"),
    }

    artifact_schema = {
        "schema_id": "formal_execution_request_artifact_schema_v1",
        "formal_execution_request_artifact_id": "ocr_real_dependency_formal_execution_request_artifact_v1",
        "request_type": "ocr_real_dependency_execution_authorization_request",
        "artifact_version": ARTIFACT_SCHEMA_VERSION,
        "lifecycle_state": "formal_execution_request_planned",
        "provider_domain": "ocr",
        "authorization_target": "real_dependency_check_execution",
        "source_execution_authorization_request_candidate_ref": refs[
            "source_execution_authorization_request_candidate_ref"
        ],
        "source_domain_config_ref": refs["source_domain_config_ref"],
        "factory_authorization_standard_ref": AUTHORIZATION_STANDARD_ID,
        "validation_engineering_ref": "validation_engineering_model_v1",
        "requested_allowed_checks": list(SCOPE_ALLOWED_CHECKS),
        "forbidden_actions_ref": refs["forbidden_actions_ref"],
        "evidence_collection_ref": refs["evidence_collection_ref"],
        "rollback_failure_route_ref": refs["rollback_failure_route_ref"],
        "execution_window_candidate_ref": refs["execution_window_candidate_ref"],
        "execution_grant_candidate_ref": refs["execution_grant_candidate_ref"],
        "validation_gate_path_ref": refs["validation_gate_path_ref"],
        "owner_operator_approval_required": True,
        "verifier_required": True,
        "post_execution_review_required": True,
        "generated_now": False,
        "persisted_now": False,
        "sent_now": False,
        "approved_now": False,
        **meta,
    }

    preconditions = {
        "precondition_id": "formal_execution_request_generation_precondition_v1",
        "roadmap_decision_go": roadmap_vr.get("verifier") == "GO",
        "route_a_selected": roadmap_sm.get("selected_route") == SELECTED_ROUTE,
        "execution_authorization_dryrun_go": dryrun_vr.get("verifier") == "GO",
        "execution_authorization_request_candidate_available": bool(
            request_cand.get("request_candidate_id")
        ),
        "execution_grant_candidate_available": bool(grant_cand.get("grant_candidate_id")),
        "execution_window_candidate_available": bool(
            window_cand.get("execution_window_candidate_id")
        ),
        "allowed_check_plan_candidate_available": bool(allowed_cand.get("candidate_id")),
        "evidence_collection_candidate_available": bool(evidence_cand.get("candidate_id")),
        "validation_gate_path_simulated_pass": gate_review.get("simulated_gate_path_pass") is True,
        "selected_provider_for_execution": None,
        "provider_selection_finalized": False,
        "all_allowed_checks_current_executed_now_false": all(
            item.get("current_executed_now") is False
            for item in (allowed_cand.get("checks") or [])
        ),
        "all_blocked_paths_blocked": dryrun_blocked_ok,
        "preconditions_pass": False,
        **meta,
    }
    precond_values = [
        preconditions["roadmap_decision_go"],
        preconditions["route_a_selected"],
        preconditions["execution_authorization_dryrun_go"],
        preconditions["execution_authorization_request_candidate_available"],
        preconditions["execution_grant_candidate_available"],
        preconditions["execution_window_candidate_available"],
        preconditions["allowed_check_plan_candidate_available"],
        preconditions["evidence_collection_candidate_available"],
        preconditions["validation_gate_path_simulated_pass"],
        preconditions["selected_provider_for_execution"] is None,
        preconditions["provider_selection_finalized"] is False,
        preconditions["all_allowed_checks_current_executed_now_false"],
        preconditions["all_blocked_paths_blocked"],
    ]
    preconditions["preconditions_pass"] = all(precond_values)

    field_source_map = {
        "map_id": "formal_execution_request_field_source_map_v1",
        "bindings": [
            {"source": src, "target_field": tgt} for src, tgt in FIELD_SOURCE_BINDINGS
        ],
        "binding_count": len(FIELD_SOURCE_BINDINGS),
        **meta,
    }

    validation_rules = {
        "rules_id": "formal_execution_request_validation_rule_v1",
        "rules": {rule: True for rule in VALIDATION_RULES},
        "rule_count": len(VALIDATION_RULES),
        **meta,
    }

    versioning_policy = {
        "policy_id": "formal_execution_request_versioning_policy_v1",
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "generation_policy_version": GENERATION_POLICY_VERSION,
        "source_candidate_version_refs": [
            "execution_authorization_request_candidate_v1",
            "execution_grant_candidate_v1",
            "execution_window_candidate_v1",
            "allowed_check_plan_candidate_v1",
            "evidence_collection_candidate_v1",
        ],
        "backward_compatibility_required": True,
        "version_bump_required_on_schema_change": True,
        "old_candidate_evidence_remains_read_only": True,
        **meta,
    }

    signature_placeholder = {
        "placeholder_id": "formal_execution_request_signature_approval_placeholder_v1",
        "owner_operator_approval_required_later": True,
        "signer_identity_later": None,
        "approval_record_later": None,
        "signature_required_later": True,
        "signature_generated_now": False,
        "approval_collected_now": False,
        **meta,
    }

    storage_boundary = {
        "plan_id": "formal_execution_request_storage_boundary_plan_v1",
        "planning_does_not_persist_artifact": True,
        "future_artifact_workspace_controlled_output_only": True,
        "no_production_path_write": True,
        "no_global_registry_write": True,
        "no_external_transmission": True,
        "persisted_now": False,
        **meta,
    }

    send_boundary = {
        "plan_id": "formal_execution_request_send_boundary_plan_v1",
        "chain": [
            "formal request planned ≠ formal request generated",
            "formal request generated later ≠ request sent",
            "request sent later ≠ grant issued",
            "grant issued later ≠ execution window opened",
            "execution window opened later ≠ real dependency check executed",
            "execution authorized later ≠ provider selection finalized",
        ],
        **meta,
    }

    evidence_binding = {
        "plan_id": "formal_execution_request_evidence_binding_plan_v1",
        "future_execution_evidence": [
            "formal_execution_request_ref",
            *list(EVIDENCE_ARTIFACTS),
        ],
        "evidence_count": len(EVIDENCE_ARTIFACTS) + 1,
        **meta,
    }

    gate_binding = {
        "plan_id": "formal_execution_request_validation_gate_binding_plan_v1",
        "gates_required_later": list(GATE_BINDINGS),
        "authorization_validation_gate_precheck_later": True,
        "gate_runtime_enabled_now": False,
        "validation_factory_runtime_enforced_now": False,
        **meta,
    }

    blocked_matrix = {
        "matrix_id": "formal_execution_request_blocked_path_matrix_v1",
        "blocked_paths": [
            {"blocked_path": bp, "blocked": True, "planning_only": True} for bp in BLOCKED_PATHS
        ],
        "all_blocked": True,
        "blocked_count": len(BLOCKED_PATHS),
        "dryrun_blocked_count": len(DRYRUN_BLOCKED_PATHS),
        **meta,
    }

    dryrun_plan = {
        "plan_id": "formal_execution_request_dryrun_plan_v1",
        "next_phase": NEXT_PHASE_GO,
        "dryrun_and_review_objectives": [
            "generate formal_execution_request_candidate",
            "verify schema / preconditions / source map / validation rules",
            "verify storage boundary / send boundary",
            "verify formal request generation remains blocked",
            "no formal request generation",
            "no persist / send / approval / grant / window open / real-dep",
        ],
        **meta,
    }

    input_ok = len(blockers) == 0 and preconditions.get("preconditions_pass") is True
    boundary_ok = (
        input_ok
        and roadmap_input.get("review_pass") is True
        and blocked_matrix.get("all_blocked") is True
        and artifact_schema.get("generated_now") is False
    )

    planning_decision = {
        "decision_id": "formal_execution_request_generation_planning_decision_v1",
        "planning_pass": boundary_ok,
        "high_risk": not boundary_ok,
        "final_decision": FINAL_DECISION_GO if boundary_ok else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if boundary_ok else NEXT_PHASE_HOLD,
        **meta,
    }

    policy = {
        "policy_id": "formal_execution_request_generation_planning_policy_v1",
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
        "validation_rule_count": len(VALIDATION_RULES),
        "blocked_path_count": len(BLOCKED_PATHS),
        "field_source_binding_count": len(FIELD_SOURCE_BINDINGS),
        "high_risk_count": 0 if boundary_ok else 1,
        **meta,
    }

    return {
        "formal_execution_request_generation_planning_policy": policy,
        "execution_request_generation_roadmap_input_review": roadmap_input,
        "formal_execution_request_artifact_schema": artifact_schema,
        "formal_execution_request_generation_precondition": preconditions,
        "formal_execution_request_field_source_map": field_source_map,
        "formal_execution_request_validation_rule": validation_rules,
        "formal_execution_request_versioning_policy": versioning_policy,
        "formal_execution_request_signature_approval_placeholder": signature_placeholder,
        "formal_execution_request_storage_boundary_plan": storage_boundary,
        "formal_execution_request_send_boundary_plan": send_boundary,
        "formal_execution_request_evidence_binding_plan": evidence_binding,
        "formal_execution_request_validation_gate_binding_plan": gate_binding,
        "formal_execution_request_blocked_path_matrix": blocked_matrix,
        "formal_execution_request_dryrun_plan": dryrun_plan,
        "non_claims_register": non_claims,
        "formal_execution_request_generation_planning_decision": planning_decision,
        "summary": summary,
    }
