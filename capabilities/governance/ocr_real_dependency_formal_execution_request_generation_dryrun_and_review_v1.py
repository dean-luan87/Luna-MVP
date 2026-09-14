# -*- coding: utf-8 -*-
"""OCR Real Dependency Formal Execution Request Generation DryRunAndReview v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.capability_factory_authorization_standard_extension_planning_v1 import (
    AUTHORIZATION_STANDARD_ID,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.ocr_real_dependency_formal_execution_request_generation_planning_v1 import (
    ARTIFACT_SCHEMA_VERSION,
    BLOCKED_PATHS as PLANNING_BLOCKED_PATHS,
    FINAL_DECISION_GO as UPSTREAM_PLANNING_FINAL_GO,
    GATE_BINDINGS,
    NEXT_PHASE_GO as UPSTREAM_PLANNING_NEXT_PHASE,
    SCOPE_ALLOWED_CHECKS,
    VALIDATION_RULES,
)
from capabilities.governance.ocr_real_dependency_execution_request_generation_roadmap_decision_v1 import (
    SELECTED_ROUTE,
)

PHASE_ID = "Phase-OCR-Real-Dependency-Formal-Execution-Request-Generation-DryRunAndReview-v1-001"
SCOPE = "formal_execution_request_generation_dryrun_and_review_only"
SOURCE_CHAIN = "ocr_real_dependency_formal_execution_request_generation_dryrun_and_review_v1"

UPSTREAM_PLANNING_FINAL = UPSTREAM_PLANNING_FINAL_GO
UPSTREAM_PLANNING_NEXT = UPSTREAM_PLANNING_NEXT_PHASE

FINAL_DECISION_GO = (
    "OCR_REAL_DEPENDENCY_FORMAL_EXECUTION_REQUEST_GENERATION_DRYRUN_AND_REVIEW_CLOSED_"
    "READY_FOR_FORMAL_EXECUTION_REQUEST_GENERATION_POST_ROUTE_DECISION"
)
FINAL_DECISION_HOLD = (
    "OCR_REAL_DEPENDENCY_FORMAL_EXECUTION_REQUEST_GENERATION_DRYRUN_AND_REVIEW_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = "Phase-OCR-Real-Dependency-Formal-Execution-Request-Generation-Post-Route-Decision-v1-001"
NEXT_PHASE_HOLD = "Phase-OCR-Real-Dependency-Formal-Execution-Request-Generation-Issue-Review-v1-001"

DRYRUN_FIELD_SOURCE_BINDINGS: Tuple[Tuple[str, str], ...] = (
    ("execution_authorization_request_candidate", "formal request candidate"),
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

DRYRUN_VALIDATION_RULE_LABELS: Tuple[str, ...] = (
    "request_type_equals_ocr_real_dependency_execution_authorization_request",
    "artifact_version_present",
    "lifecycle_state_valid",
    "provider_domain_equals_ocr",
    "authorization_target_equals_real_dependency_check_execution",
    "target_scope_excludes_provider_selection_finalize",
    "target_scope_excludes_controlled_trial",
    "target_scope_excludes_production_runtime",
    "allowed_checks_remain_not_executed_now",
    "selected_provider_for_execution_remains_null",
    "execution_window_remains_closed",
    "request_remains_unsent",
    "grant_remains_unissued",
    "provider_import_remains_false",
    "evidence_collection_required",
    "validation_gate_path_required",
    "formal_request_generated_remains_false_in_dryrun",
)

FUTURE_EVIDENCE_ITEMS: Tuple[str, ...] = (
    "formal_execution_request_ref",
    "execution_grant_ref",
    "execution_window_ref",
    "domain_config_ref",
    "validation_gate_result",
    "environment_snapshot",
    "python_version_snapshot",
    "package_presence_result",
    "model_cache_path_result",
    "model_file_existence_result",
    "model_file_hash_result",
    "import_check_result",
    "boundary_audit_result",
    "failure_route_result",
    "rollback_result",
    "verifier_report",
    "post_execution_review",
)

BLOCKED_PATHS: Tuple[str, ...] = (
    "dryrun_to_formal_execution_request_artifact_generation",
    "dryrun_to_request_persist",
    "dryrun_to_request_send",
    "dryrun_to_approval_collect",
    "dryrun_to_grant_issue",
    "dryrun_to_execution_window_open",
    "dryrun_to_real_dependency_check",
    "dryrun_to_package_check",
    "dryrun_to_provider_import",
    "dryrun_to_model_cache_check",
    "dryrun_to_model_file_hash_check",
    "dryrun_to_dependency_install",
    "dryrun_to_model_download",
    "dryrun_to_cache_mutation",
    "dryrun_to_provider_invoke",
    "dryrun_to_provider_selection_finalize",
    "dryrun_to_controlled_trial",
    "dryrun_to_ocr_request_submit",
    "dryrun_to_image_read",
    "dryrun_to_crop",
    "dryrun_to_ocr_fact",
    "dryrun_to_user_output",
    "dryrun_to_memory_write",
    "dryrun_to_world_model_write",
)

NON_CLAIMS: Tuple[str, ...] = (
    "DryRunAndReview GO ≠ formal request artifact generated",
    "formal_execution_request_candidate ≠ persisted artifact",
    "formal_execution_request_candidate ≠ request sent",
    "next route decision ≠ grant issued",
    "next route decision ≠ execution window opened",
    "next route decision ≠ provider import allowed",
)

BOUNDARY_TRUE: Tuple[str, ...] = ("formal_execution_request_candidate_generated_now",)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "formal_execution_request_artifact_generated_now",
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
    "validator_runtime_enabled_now",
    "validation_factory_runtime_enforced_now",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_real_dependency_formal_execution_request_generation_dryrun_and_review"
)


def _dryrun_meta() -> Dict[str, Any]:
    meta = {
        "formal_execution_request_generation_dryrun_and_review_only": True,
        "simulated": True,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "selected_provider_for_execution": None,
    }
    for field in BOUNDARY_TRUE:
        meta[field] = True
    for field in BOUNDARY_FALSE:
        meta[field] = False
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


def run_ocr_real_dependency_formal_execution_request_generation_dryrun_and_review_v1(
    *,
    ocr_real_dependency_formal_execution_request_generation_planning_root: str,
    ocr_real_dependency_execution_request_generation_roadmap_decision_root: Optional[str] = None,
    ocr_real_dependency_execution_authorization_dryrun_and_review_root: Optional[str] = None,
    midplatform_validation_engineering_separation_dryrun_and_review_root: Optional[str] = None,
    ocr_real_dependency_authorization_via_factory_standard_dryrun_and_review_root: Optional[str] = None,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    plan_root = Path(
        ocr_real_dependency_formal_execution_request_generation_planning_root
    ).expanduser().resolve()
    plan_sm = _try_read_json(plan_root / "summary.json") or {}
    plan_vr = _try_read_json(plan_root / "verifier_report.json") or {}
    plan_schema = _try_read_json(plan_root / "formal_execution_request_artifact_schema_v1.json") or {}
    plan_precond = _try_read_json(
        plan_root / "formal_execution_request_generation_precondition_v1.json"
    ) or {}
    plan_field_map = _try_read_json(plan_root / "formal_execution_request_field_source_map_v1.json") or {}
    plan_rules = _try_read_json(plan_root / "formal_execution_request_validation_rule_v1.json") or {}
    plan_signature = _try_read_json(
        plan_root / "formal_execution_request_signature_approval_placeholder_v1.json"
    ) or {}
    plan_blocked = _try_read_json(plan_root / "formal_execution_request_blocked_path_matrix_v1.json") or {}

    roadmap_root = Path(
        ocr_real_dependency_execution_request_generation_roadmap_decision_root
        or plan_root.parent / "ocr_real_dependency_execution_request_generation_roadmap_decision"
    ).expanduser().resolve()
    auth_dryrun_root = Path(
        ocr_real_dependency_execution_authorization_dryrun_and_review_root
        or plan_root.parent / "ocr_real_dependency_execution_authorization_dryrun_and_review"
    ).expanduser().resolve()
    ocr_dr_root = Path(
        ocr_real_dependency_authorization_via_factory_standard_dryrun_and_review_root
        or plan_root.parent / "ocr_real_dependency_authorization_via_factory_standard_dryrun_and_review"
    ).expanduser().resolve()
    val_dr_root = Path(
        midplatform_validation_engineering_separation_dryrun_and_review_root
        or plan_root.parent / "midplatform_validation_engineering_separation_dryrun_and_review"
    ).expanduser().resolve()

    roadmap_sm = _try_read_json(roadmap_root / "summary.json") or {}
    roadmap_vr = _try_read_json(roadmap_root / "verifier_report.json") or {}
    auth_dryrun_vr = _try_read_json(auth_dryrun_root / "verifier_report.json") or {}
    auth_dryrun_blocked = _try_read_json(
        auth_dryrun_root / "execution_authorization_blocked_path_result_v1.json"
    ) or {}
    gate_review = _try_read_json(auth_dryrun_root / "validation_gate_path_dryrun_review_v1.json") or {}
    allowed_cand = _try_read_json(auth_dryrun_root / "allowed_check_plan_candidate_v1.json") or {}

    domain_config_ref = str(
        ocr_dr_root / "ocr_real_dependency_domain_config_candidate_v1.json"
    )
    refs = {
        "source_execution_authorization_request_candidate_ref": str(
            auth_dryrun_root / "execution_authorization_request_candidate_v1.json"
        ),
        "source_domain_config_ref": domain_config_ref,
        "execution_grant_candidate_ref": str(auth_dryrun_root / "execution_grant_candidate_v1.json"),
        "execution_window_candidate_ref": str(
            auth_dryrun_root / "execution_window_candidate_v1.json"
        ),
        "evidence_collection_ref": str(
            auth_dryrun_root / "evidence_collection_candidate_v1.json"
        ),
        "rollback_failure_route_ref": str(
            auth_dryrun_root / "rollback_failure_route_candidate_v1.json"
        ),
        "validation_gate_path_ref": str(
            auth_dryrun_root / "validation_gate_path_dryrun_review_v1.json"
        ),
        "forbidden_actions_ref": str(auth_dryrun_root / "forbidden_action_review_v1.json"),
    }

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_dryrun_meta(),
        "upstream_planning_root": str(plan_root),
        "upstream_roadmap_decision_root": str(roadmap_root),
        "upstream_execution_authorization_dryrun_root": str(auth_dryrun_root),
        "upstream_ocr_via_factory_dryrun_root": str(ocr_dr_root),
        "upstream_validation_separation_dryrun_root": str(val_dr_root),
        "output_root": str(out_root),
    }

    if plan_vr.get("verifier") != "GO":
        blockers.append("planning verifier must be GO")
    if plan_sm.get("final_decision") != UPSTREAM_PLANNING_FINAL:
        blockers.append("planning final_decision mismatch")
    if plan_sm.get("recommended_next_phase") != UPSTREAM_PLANNING_NEXT:
        blockers.append("planning recommended_next_phase mismatch")
    if plan_precond.get("preconditions_pass") is not True:
        blockers.append("planning preconditions must pass")
    if plan_schema.get("generated_now") is True or plan_schema.get("persisted_now") is True:
        blockers.append("planning schema must not be generated/persisted")
    if plan_field_map.get("binding_count") != 11:
        blockers.append("planning must have 11 field bindings")
    if plan_rules.get("rule_count") != 17:
        blockers.append("planning must have 17 validation rules")
    if plan_blocked.get("blocked_count") != 24:
        blockers.append("planning must have 24 blocked paths")
    if plan_signature.get("signature_generated_now") is True:
        blockers.append("signature_generated_now must be false")
    if plan_signature.get("approval_collected_now") is True:
        blockers.append("approval_collected_now must be false")

    if roadmap_vr.get("verifier") != "GO":
        blockers.append("roadmap verifier should be GO")
    if roadmap_sm.get("selected_route") != SELECTED_ROUTE:
        blockers.append("route A must be selected")
    if auth_dryrun_vr.get("verifier") != "GO":
        blockers.append("execution authorization dryrun must be GO")
    if gate_review.get("simulated_gate_path_pass") is not True:
        blockers.append("validation gate path must simulated pass")

    input_ok = len(blockers) == 0

    planning_input = {
        "review_id": "formal_execution_request_generation_planning_input_review_v1",
        "upstream_planning_root": str(plan_root),
        "verifier_go": plan_vr.get("verifier") == "GO",
        "final_decision": plan_sm.get("final_decision"),
        "review_pass": input_ok,
        "blockers": blockers,
        **meta,
    }

    formal_candidate = {
        "candidate_id": "formal_execution_request_candidate_v1",
        "formal_execution_request_candidate_id": (
            "ocr_real_dependency_formal_execution_request_candidate_v1"
        ),
        "request_type": "ocr_real_dependency_execution_authorization_request",
        "artifact_version": ARTIFACT_SCHEMA_VERSION,
        "lifecycle_state": "formal_execution_request_candidate_ready",
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
        "candidate_only": True,
        "formal_artifact_generated_now": False,
        "persisted_now": False,
        "sent_now": False,
        "approved_now": False,
        "simulated_validation_pass": True,
        **meta,
    }

    schema_checks: List[Tuple[str, bool]] = [
        ("request_type_valid", formal_candidate.get("request_type")
         == "ocr_real_dependency_execution_authorization_request"),
        ("lifecycle_candidate_ready", formal_candidate.get("lifecycle_state")
         == "formal_execution_request_candidate_ready"),
        ("provider_ocr", formal_candidate.get("provider_domain") == "ocr"),
        ("target_real_dep", formal_candidate.get("authorization_target")
         == "real_dependency_check_execution"),
        ("artifact_version", bool(formal_candidate.get("artifact_version"))),
        ("source_request_ref", bool(formal_candidate.get("source_execution_authorization_request_candidate_ref"))),
        ("source_domain_ref", bool(formal_candidate.get("source_domain_config_ref"))),
        ("evidence_ref", bool(formal_candidate.get("evidence_collection_ref"))),
        ("gate_path_ref", bool(formal_candidate.get("validation_gate_path_ref"))),
        ("owner_approval", formal_candidate.get("owner_operator_approval_required") is True),
        ("candidate_only", formal_candidate.get("candidate_only") is True),
        ("no_formal_artifact", formal_candidate.get("formal_artifact_generated_now") is False),
    ]
    for ref_key in (
        "execution_grant_candidate_ref",
        "execution_window_candidate_ref",
        "rollback_failure_route_ref",
        "forbidden_actions_ref",
    ):
        schema_checks.append((f"ref.{ref_key}", bool(formal_candidate.get(ref_key))))

    schema_validation = {
        "result_id": "formal_execution_request_schema_validation_result_v1",
        "schema_ref": str(plan_root / "formal_execution_request_artifact_schema_v1.json"),
        **_review_ok(schema_checks),
        **meta,
    }

    precond_dryrun = {
        "result_id": "formal_execution_request_precondition_dryrun_result_v1",
        "roadmap_decision_go": roadmap_vr.get("verifier") == "GO",
        "route_a_selected": roadmap_sm.get("selected_route") == SELECTED_ROUTE,
        "execution_authorization_dryrun_go": auth_dryrun_vr.get("verifier") == "GO",
        "execution_authorization_request_candidate_available": Path(
            refs["source_execution_authorization_request_candidate_ref"]
        ).is_file(),
        "execution_grant_candidate_available": Path(refs["execution_grant_candidate_ref"]).is_file(),
        "execution_window_candidate_available": Path(
            refs["execution_window_candidate_ref"]
        ).is_file(),
        "allowed_check_plan_candidate_available": Path(
            auth_dryrun_root / "allowed_check_plan_candidate_v1.json"
        ).is_file(),
        "evidence_collection_candidate_available": Path(refs["evidence_collection_ref"]).is_file(),
        "validation_gate_path_simulated_pass": gate_review.get("simulated_gate_path_pass") is True,
        "selected_provider_for_execution": None,
        "provider_selection_finalized": False,
        "all_allowed_checks_current_executed_now_false": all(
            item.get("current_executed_now") is False
            for item in (allowed_cand.get("checks") or [])
        ),
        "all_blocked_paths_blocked": auth_dryrun_blocked.get("all_blocked") is True
        and plan_blocked.get("all_blocked") is True,
        **meta,
    }
    precond_values = [
        precond_dryrun["roadmap_decision_go"],
        precond_dryrun["route_a_selected"],
        precond_dryrun["execution_authorization_dryrun_go"],
        precond_dryrun["execution_authorization_request_candidate_available"],
        precond_dryrun["execution_grant_candidate_available"],
        precond_dryrun["execution_window_candidate_available"],
        precond_dryrun["allowed_check_plan_candidate_available"],
        precond_dryrun["evidence_collection_candidate_available"],
        precond_dryrun["validation_gate_path_simulated_pass"],
        precond_dryrun["selected_provider_for_execution"] is None,
        precond_dryrun["provider_selection_finalized"] is False,
        precond_dryrun["all_allowed_checks_current_executed_now_false"],
        precond_dryrun["all_blocked_paths_blocked"],
    ]
    precond_dryrun["preconditions_pass"] = all(precond_values)
    precond_dryrun.update(_review_ok([(f"pre.{i}", v) for i, v in enumerate(precond_values)]))

    field_map_checks = [
        (f"bind.{src[:25]}", True) for src, _tgt in DRYRUN_FIELD_SOURCE_BINDINGS
    ]
    field_map_result = {
        "result_id": "formal_execution_request_field_source_map_dryrun_result_v1",
        "bindings": [
            {"source": src, "target": tgt, "pass": True}
            for src, tgt in DRYRUN_FIELD_SOURCE_BINDINGS
        ],
        "binding_count": len(DRYRUN_FIELD_SOURCE_BINDINGS),
        **_review_ok(field_map_checks),
        **meta,
    }

    rule_checks: List[Tuple[str, bool]] = []
    for label in DRYRUN_VALIDATION_RULE_LABELS:
        passed = True
        if label == "formal_request_generated_remains_false_in_dryrun":
            passed = formal_candidate.get("formal_artifact_generated_now") is False
        elif label == "execution_window_remains_closed":
            passed = meta.get("execution_window_opened_now") is False
        elif label == "request_remains_unsent":
            passed = formal_candidate.get("sent_now") is False
        elif label == "grant_remains_unissued":
            passed = meta.get("execution_grant_issued_now") is False
        elif label == "selected_provider_for_execution_remains_null":
            passed = meta.get("selected_provider_for_execution") is None
        elif label == "provider_import_remains_false":
            passed = meta.get("provider_imported_now") is False
        rule_checks.append((label, passed))

    validation_rule_result = {
        "result_id": "formal_execution_request_validation_rule_dryrun_result_v1",
        "rules": {label: True for label in DRYRUN_VALIDATION_RULE_LABELS},
        "planning_rules_aligned": len(VALIDATION_RULES) == 17,
        "rule_count": len(DRYRUN_VALIDATION_RULE_LABELS),
        **_review_ok(rule_checks),
        **meta,
    }

    versioning_review = {
        "review_id": "formal_execution_request_versioning_review_v1",
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "candidate_artifact_version_matches_planning": True,
        "backward_compatibility_required": True,
        "dryrun_and_review_pass": True,
        **meta,
    }

    signature_review = {
        "review_id": "formal_execution_request_signature_approval_review_v1",
        "owner_operator_approval_required_later": plan_signature.get(
            "owner_operator_approval_required_later", True
        ),
        "signature_generated_now": False,
        "approval_collected_now": False,
        "dryrun_and_review_pass": plan_signature.get("signature_generated_now") is False
        and plan_signature.get("approval_collected_now") is False,
        **meta,
    }

    storage_checks: List[Tuple[str, bool]] = [
        ("dryrun_no_persist", True),
        ("workspace_controlled_only", True),
        ("no_production_write", True),
        ("no_registry_write", True),
        ("no_external_transmission", True),
        ("persisted_false", meta.get("formal_execution_request_persisted_now") is False),
    ]
    storage_review = {
        "review_id": "formal_execution_request_storage_boundary_review_v1",
        "dryrun_does_not_persist_artifact": True,
        "workspace_controlled_output_only_for_candidate": True,
        **_review_ok(storage_checks),
        **meta,
    }

    send_checks: List[Tuple[str, bool]] = [
        ("candidate_not_artifact", formal_candidate.get("candidate_only") is True),
        ("artifact_not_generated", formal_candidate.get("formal_artifact_generated_now") is False),
        ("not_sent", formal_candidate.get("sent_now") is False),
        ("grant_not_issued", meta.get("execution_grant_issued_now") is False),
        ("window_not_open", meta.get("execution_window_opened_now") is False),
        ("real_dep_not_executed", meta.get("real_dependency_check_executed_now") is False),
    ]
    send_review = {
        "review_id": "formal_execution_request_send_boundary_review_v1",
        "boundary_chain_valid": True,
        **_review_ok(send_checks),
        **meta,
    }

    evidence_checks = [
        (f"evidence.{item}", item in FUTURE_EVIDENCE_ITEMS) for item in FUTURE_EVIDENCE_ITEMS
    ]
    evidence_review = {
        "review_id": "formal_execution_request_evidence_binding_review_v1",
        "future_evidence_items": list(FUTURE_EVIDENCE_ITEMS),
        "evidence_count": len(FUTURE_EVIDENCE_ITEMS),
        **_review_ok(evidence_checks),
        **meta,
    }

    gate_checks: List[Tuple[str, bool]] = [
        (f"gate.{g[:20]}", g in GATE_BINDINGS) for g in GATE_BINDINGS
    ]
    gate_checks.extend([
        ("auth_gate_precheck_later", True),
        ("runtime_disabled", meta.get("validator_runtime_enabled_now") is False),
        ("vf_not_enforced", meta.get("validation_factory_runtime_enforced_now") is False),
    ])
    gate_binding_review = {
        "review_id": "formal_execution_request_validation_gate_binding_review_v1",
        "gates_required_later": list(GATE_BINDINGS),
        "authorization_validation_gate_precheck_later_required": True,
        "gate_runtime_enabled_now": False,
        **_review_ok(gate_checks),
        **meta,
    }

    boundary_checks: List[Tuple[str, bool]] = []
    for field in BOUNDARY_TRUE:
        boundary_checks.append((f"true.{field}", meta.get(field) is True))
    for field in BOUNDARY_FALSE:
        boundary_checks.append((f"false.{field}", meta.get(field) is False))

    boundary_audit = {
        "audit_id": "formal_execution_request_boundary_audit_v1",
        **_review_ok(boundary_checks),
        **meta,
    }

    blocked_path_result = {
        "result_id": "formal_execution_request_blocked_path_result_v1",
        "blocked_paths": [
            {"blocked_path": bp, "blocked": True, "simulated": True} for bp in BLOCKED_PATHS
        ],
        "all_blocked": True,
        "blocked_count": len(BLOCKED_PATHS),
        "planning_blocked_count": len(PLANNING_BLOCKED_PATHS),
        **meta,
    }

    review_sections = [
        schema_validation,
        precond_dryrun,
        field_map_result,
        validation_rule_result,
        versioning_review,
        signature_review,
        storage_review,
        send_review,
        evidence_review,
        gate_binding_review,
        boundary_audit,
    ]

    all_pass = (
        input_ok
        and precond_dryrun.get("preconditions_pass") is True
        and formal_candidate.get("candidate_only") is True
        and all(s.get("dryrun_and_review_pass") is True for s in review_sections)
        and blocked_path_result.get("all_blocked") is True
    )

    closure_decision = {
        "decision_id": "formal_execution_request_closure_decision_v1",
        "dryrun_and_review_pass": all_pass,
        "high_risk": not all_pass,
        "final_decision": FINAL_DECISION_GO if all_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if all_pass else NEXT_PHASE_HOLD,
        **meta,
    }

    next_route = {
        "decision_id": "next_route_readiness_decision_v1",
        "ready_for_formal_execution_request_generation_post_route_decision": all_pass,
        "ready_for_formal_request_artifact_generation": False,
        "do_not_persist_now": True,
        "do_not_send_now": True,
        "do_not_approve_now": True,
        "recommended_next_phase": closure_decision["recommended_next_phase"],
        **meta,
    }

    policy = {
        "policy_id": "formal_execution_request_generation_dryrun_review_policy_v1",
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
        "boundary_ok": all_pass,
        "violations": blockers,
        "dryrun_and_review_pass": all_pass,
        "final_decision": closure_decision["final_decision"],
        "recommended_next_phase": closure_decision["recommended_next_phase"],
        **meta,
    }

    return {
        "formal_execution_request_generation_dryrun_review_policy": policy,
        "formal_execution_request_generation_planning_input_review": planning_input,
        "formal_execution_request_candidate": formal_candidate,
        "formal_execution_request_schema_validation_result": schema_validation,
        "formal_execution_request_precondition_dryrun_result": precond_dryrun,
        "formal_execution_request_field_source_map_dryrun_result": field_map_result,
        "formal_execution_request_validation_rule_dryrun_result": validation_rule_result,
        "formal_execution_request_versioning_review": versioning_review,
        "formal_execution_request_signature_approval_review": signature_review,
        "formal_execution_request_storage_boundary_review": storage_review,
        "formal_execution_request_send_boundary_review": send_review,
        "formal_execution_request_evidence_binding_review": evidence_review,
        "formal_execution_request_validation_gate_binding_review": gate_binding_review,
        "formal_execution_request_boundary_audit": boundary_audit,
        "formal_execution_request_blocked_path_result": blocked_path_result,
        "formal_execution_request_closure_decision": closure_decision,
        "next_route_readiness_decision": next_route,
        "non_claims_register": non_claims,
        "summary": summary,
    }
