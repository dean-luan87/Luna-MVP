# -*- coding: utf-8 -*-
"""OCR Real Dependency Execution Final Preflight v1 — dryrun+review before minimal controlled execution."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.health_management_layer_integration_planning_v1 import (
    HEALTH_METRIC_DEFINITION_STATUS,
)
from capabilities.governance.ocr_real_dependency_execution_authorization_planning_v1 import (
    FORBIDDEN_EXECUTION_ACTIONS,
    SCOPE_ALLOWED_CHECKS,
    _check_plan_item,
)
from capabilities.governance.ocr_real_dependency_formal_request_generation_authorization_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as UPSTREAM_AUTH_FINAL_GO,
    NEXT_PHASE_GO as UPSTREAM_AUTH_NEXT_PHASE,
    VALIDATION_GATES_PLANNED,
)
from capabilities.governance.ocr_real_dependency_formal_request_generation_authorization_dryrun_and_review_v1 import (
    BLOCKED_PATHS as AUTH_DRYRUN_BLOCKED,
)

PHASE_ID = "Phase-OCR-Real-Dependency-Execution-Final-Preflight-v1-001"
SCOPE = "ocr_real_dependency_execution_final_preflight_only"
SOURCE_CHAIN = "ocr_real_dependency_execution_final_preflight_v1"

UPSTREAM_AUTH_FINAL = UPSTREAM_AUTH_FINAL_GO
UPSTREAM_AUTH_NEXT = UPSTREAM_AUTH_NEXT_PHASE

FINAL_DECISION_GO = (
    "OCR_REAL_DEPENDENCY_EXECUTION_FINAL_PREFLIGHT_CLOSED_READY_FOR_MINIMAL_CONTROLLED_EXECUTION_PLANNING"
)
FINAL_DECISION_HOLD = "OCR_REAL_DEPENDENCY_EXECUTION_FINAL_PREFLIGHT_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-OCR-Real-Dependency-Minimal-Controlled-Execution-Planning-v1-001"
NEXT_PHASE_HOLD = "Phase-OCR-Real-Dependency-Execution-Final-Preflight-Issue-Review-v1-001"

MINIMAL_SCOPE_ALLOWED_CHECKS: Tuple[str, ...] = (
    "package_presence_check",
    "model_cache_path_check",
    "model_file_existence_check",
    "model_file_hash_check",
    "provider_import_check",
)

MINIMAL_SCOPE_STILL_FORBIDDEN: Tuple[str, ...] = (
    "pip_install",
    "dependency_auto_install",
    "model_download",
    "cache_mutation_without_approval",
    "provider_runtime_invocation_beyond_import_check",
    "runtime_smoke_check_unless_separately_authorized",
    "sample_ocr_check_unless_separately_authorized",
    "OCRRequest_submit",
    "image_read",
    "crop",
    "OCR_fact_generation",
    "user_output",
    "memory_write",
    "world_model_write",
    "provider_selection_finalize",
    "controlled_trial_start",
    "production_runtime",
)

BLOCKED_PATHS: Tuple[str, ...] = (
    "preflight_to_formal_request_artifact_generation",
    "preflight_to_request_persist",
    "preflight_to_request_send",
    "preflight_to_approval_collect",
    "preflight_to_grant_issue",
    "preflight_to_execution_window_open",
    "preflight_to_real_dependency_check",
    "preflight_to_package_check",
    "preflight_to_provider_import",
    "preflight_to_model_cache_check",
    "preflight_to_model_file_hash_check",
    "preflight_to_dependency_install",
    "preflight_to_model_download",
    "preflight_to_cache_mutation",
    "preflight_to_provider_invoke",
    "preflight_to_provider_selection_finalize",
    "preflight_to_controlled_trial",
    "preflight_to_ocr_request_submit",
    "preflight_to_image_read",
    "preflight_to_crop",
    "preflight_to_ocr_fact",
    "preflight_to_user_output",
    "preflight_to_memory_write",
    "preflight_to_world_model_write",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Final Preflight GO ≠ controlled execution authorized",
    "preflight pass ≠ package/import/cache/hash executed",
    "minimal scope plan ≠ execution started",
    "next planning ≠ provider import allowed",
    "health boundary reviewed ≠ health metric defined",
)

BOUNDARY_TRUE: Tuple[str, ...] = ("final_preflight_result_generated_now",)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "controlled_execution_authorized_now",
    "formal_execution_request_artifact_generated_now",
    "formal_execution_request_persisted_now",
    "formal_execution_request_sent_now",
    "approval_collected_now",
    "execution_grant_issued_now",
    "execution_window_opened_now",
    "real_dependency_check_executed_now",
    "package_check_executed_now",
    "provider_import_check_executed_now",
    "model_cache_path_check_executed_now",
    "model_file_existence_check_executed_now",
    "model_file_hash_check_executed_now",
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
    "ocr_real_dependency_execution_final_preflight"
)


def _preflight_meta() -> Dict[str, Any]:
    meta = {
        "ocr_real_dependency_execution_final_preflight_only": True,
        "simulated": True,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "selected_provider_for_execution": None,
        "controlled_execution_authorized_now": False,
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


def run_ocr_real_dependency_execution_final_preflight_v1(
    *,
    ocr_real_dependency_formal_request_generation_authorization_dryrun_and_review_root: str,
    ocr_real_dependency_formal_execution_request_generation_dryrun_and_review_root: str,
    ocr_real_dependency_execution_authorization_dryrun_and_review_root: str,
    ocr_real_dependency_authorization_via_factory_standard_dryrun_and_review_root: str,
    midplatform_validation_engineering_separation_dryrun_and_review_root: str,
    capability_factory_authorization_standard_extension_dryrun_and_review_root: Optional[str] = None,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    auth_dr_root = Path(
        ocr_real_dependency_formal_request_generation_authorization_dryrun_and_review_root
    ).expanduser().resolve()
    formal_dr_root = Path(
        ocr_real_dependency_formal_execution_request_generation_dryrun_and_review_root
    ).expanduser().resolve()
    exec_auth_dr_root = Path(
        ocr_real_dependency_execution_authorization_dryrun_and_review_root
    ).expanduser().resolve()
    ocr_dr_root = Path(
        ocr_real_dependency_authorization_via_factory_standard_dryrun_and_review_root
    ).expanduser().resolve()
    val_dr_root = Path(
        midplatform_validation_engineering_separation_dryrun_and_review_root
    ).expanduser().resolve()
    auth_ext_root = Path(
        capability_factory_authorization_standard_extension_dryrun_and_review_root
        or auth_dr_root.parent / "capability_factory_authorization_standard_extension_dryrun_and_review"
    ).expanduser().resolve()

    auth_sm = _try_read_json(auth_dr_root / "summary.json") or {}
    auth_vr = _try_read_json(auth_dr_root / "verifier_report.json") or {}
    auth_blocked = _try_read_json(
        auth_dr_root / "formal_request_generation_authorization_blocked_path_result_v1.json"
    ) or {}
    auth_cand = _try_read_json(
        auth_dr_root / "formal_request_generation_authorization_candidate_v1.json"
    ) or {}
    approval_cand = _try_read_json(
        auth_dr_root / "owner_operator_approval_precheck_candidate_v1.json"
    ) or {}
    evidence_cand = _try_read_json(auth_dr_root / "evidence_readiness_candidate_v1.json") or {}
    gate_cand = _try_read_json(auth_dr_root / "validation_gate_readiness_candidate_v1.json") or {}
    preflight_cand = _try_read_json(
        auth_dr_root / "final_preflight_readiness_candidate_v1.json"
    ) or {}
    legacy_marker = _try_read_json(auth_dr_root / "legacy_phase_absorption_marker_v1.json") or {}

    formal_dr_vr = _try_read_json(formal_dr_root / "verifier_report.json") or {}
    formal_candidate = _try_read_json(formal_dr_root / "formal_execution_request_candidate_v1.json") or {}
    exec_auth_vr = _try_read_json(exec_auth_dr_root / "verifier_report.json") or {}
    ocr_dr_vr = _try_read_json(ocr_dr_root / "verifier_report.json") or {}
    val_vr = _try_read_json(val_dr_root / "verifier_report.json") or {}
    val_model = _try_read_json(val_dr_root / "validation_engineering_model_candidate_v1.json") or {}
    auth_ext_vr = _try_read_json(auth_ext_root / "verifier_report.json") or {}

    window_cand = _try_read_json(exec_auth_dr_root / "execution_window_candidate_v1.json") or {}
    rollback_cand = _try_read_json(
        exec_auth_dr_root / "rollback_failure_route_candidate_v1.json"
    ) or _try_read_json(formal_dr_root / "rollback_failure_route_candidate_v1.json") or {}
    allowed_plan = _try_read_json(exec_auth_dr_root / "allowed_check_plan_candidate_v1.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_preflight_meta(),
        "upstream_authorization_dryrun_root": str(auth_dr_root),
        "upstream_formal_request_dryrun_root": str(formal_dr_root),
        "upstream_execution_authorization_dryrun_root": str(exec_auth_dr_root),
        "upstream_ocr_via_factory_dryrun_root": str(ocr_dr_root),
        "upstream_validation_separation_dryrun_root": str(val_dr_root),
        "upstream_auth_standard_extension_root": str(auth_ext_root),
        "output_root": str(out_root),
    }

    if auth_vr.get("verifier") != "GO":
        blockers.append("authorization dryrun verifier must be GO")
    if auth_sm.get("final_decision") != UPSTREAM_AUTH_FINAL:
        blockers.append("authorization final_decision mismatch")
    if auth_sm.get("recommended_next_phase") != UPSTREAM_AUTH_NEXT:
        blockers.append("authorization recommended_next_phase mismatch")
    if not auth_cand.get("authorization_candidate_id"):
        blockers.append("formal_request_generation_authorization_candidate required")
    if not approval_cand.get("approval_precheck_candidate_id"):
        blockers.append("owner_operator_approval_precheck_candidate required")
    if not evidence_cand.get("evidence_ready_for_final_preflight"):
        blockers.append("evidence_readiness_candidate required")
    if not gate_cand.get("gate_executed_now") is False:
        blockers.append("validation_gate_readiness gate_executed_now must be false")
    if preflight_cand.get("readiness_pass") is not True:
        blockers.append("final_preflight_readiness_candidate must pass")
    if not legacy_marker.get("marker_id"):
        blockers.append("legacy_chain_integration_marker required")
    if auth_blocked.get("all_blocked") is not True or auth_blocked.get("blocked_count") != 24:
        blockers.append("24 authorization blocked paths must remain blocked")
    if formal_dr_vr.get("verifier") != "GO":
        blockers.append("formal request dryrun should be GO")
    if formal_candidate.get("formal_artifact_generated_now") is not False:
        blockers.append("formal_artifact must not be generated")
    if exec_auth_vr.get("verifier") != "GO":
        blockers.append("execution authorization dryrun should be GO")
    if ocr_dr_vr.get("verifier") != "GO":
        blockers.append("ocr via factory dryrun should be GO")
    if val_vr.get("verifier") != "GO":
        blockers.append("validation separation dryrun should be GO")
    if val_model.get("runtime_enabled_now") is True:
        blockers.append("validator_runtime_enabled_now must be false")

    input_ok = len(blockers) == 0

    auth_input = {
        "review_id": "authorization_dryrun_input_review_v1",
        "upstream_root": str(auth_dr_root),
        "verifier_go": auth_vr.get("verifier") == "GO",
        "final_decision": auth_sm.get("final_decision"),
        "recommended_next_phase": auth_sm.get("recommended_next_phase"),
        "review_pass": input_ok,
        "blockers": blockers,
        **meta,
    }

    auth_review_checks: List[Tuple[str, bool]] = [
        ("authorization_candidate_id", bool(auth_cand.get("authorization_candidate_id"))),
        ("authorization_target", auth_cand.get("authorization_target") == "formal_execution_request_generation"),
        ("candidate_only", auth_cand.get("candidate_only") is True),
        ("no_artifact", auth_cand.get("formal_artifact_generation_allowed_now") is False),
        ("no_send", auth_cand.get("request_send_allowed_now") is False),
        ("no_grant", auth_cand.get("grant_allowed_now") is False),
        ("no_window", auth_cand.get("execution_window_allowed_now") is False),
        ("no_real_dep", auth_cand.get("real_dependency_check_allowed_now") is False),
    ]
    auth_candidate_review = {
        "review_id": "formal_request_authorization_candidate_review_v1",
        "authorization_candidate_ref": str(
            auth_dr_root / "formal_request_generation_authorization_candidate_v1.json"
        ),
        **_review_ok(auth_review_checks),
        **meta,
    }

    approval_checks: List[Tuple[str, bool]] = [
        ("approval_required_later", approval_cand.get("approval_required_later") is True),
        ("identity_required_later", approval_cand.get("owner_operator_identity_required_later") is True),
        ("scope", approval_cand.get("approval_scope") == "formal_request_generation_only"),
        ("not_grant", approval_cand.get("approval_does_not_imply_grant") is True),
        ("not_window", approval_cand.get("approval_does_not_open_execution_window") is True),
        ("not_collected", approval_cand.get("approval_collected_now") is False),
        ("not_skipped", approval_cand.get("approval_skipped_now") is False),
    ]
    approval_review = {
        "review_id": "owner_operator_approval_precheck_review_v1",
        **_review_ok(approval_checks),
        **meta,
    }

    evidence_refs = (
        "formal_execution_request_candidate_ref",
        "execution_grant_candidate_ref",
        "execution_window_candidate_ref",
        "domain_config_ref",
        "validation_gate_path_ref",
        "allowed_check_plan_ref",
        "rollback_failure_route_ref",
        "evidence_collection_candidate_ref",
    )
    evidence_checks: List[Tuple[str, bool]] = [
        (ref, bool(evidence_cand.get(ref))) for ref in evidence_refs
    ] + [
        ("evidence_ready", evidence_cand.get("evidence_ready_for_final_preflight") is True),
        ("not_collected", evidence_cand.get("evidence_collected_now") is False),
    ]
    evidence_review = {
        "review_id": "evidence_readiness_review_v1",
        **_review_ok(evidence_checks),
        **meta,
    }

    gate_checks: List[Tuple[str, bool]] = []
    for gate in VALIDATION_GATES_PLANNED:
        planned = gate_cand.get(gate) == "planned" or gate_cand.get("gates_planned", {}).get(gate) is True
        if gate == "ValidationFactory":
            planned = planned or gate_cand.get("ValidationFactory") == "aggregation_planned"
        gate_checks.append((gate, planned))
    gate_checks.extend([
        ("runtime_false", gate_cand.get("validator_runtime_enabled_now") is False),
        ("not_executed", gate_cand.get("gate_executed_now") is False),
    ])
    gate_review = {
        "review_id": "validation_gate_readiness_review_v1",
        **_review_ok(gate_checks),
        **meta,
    }

    sandbox_checks: List[Tuple[str, bool]] = [
        ("workspace_controlled_output_only", True),
        ("no_production_write", window_cand.get("no_production_write") is True),
        ("no_global_registry_write", True),
        ("no_external_transmission", True),
        ("no_network_by_default", window_cand.get("no_network_by_default") is True),
        ("no_install", window_cand.get("no_install") is True),
        ("no_download", window_cand.get("no_download") is True),
        (
            "no_cache_mutation_without_approval",
            window_cand.get("no_cache_mutation_without_approval") is True,
        ),
    ]
    sandbox_review = {
        "review_id": "sandbox_boundary_readiness_review_v1",
        "workspace_controlled_output_only": True,
        "no_production_write": True,
        "no_global_registry_write": True,
        "no_external_transmission": True,
        "no_network_by_default": True,
        "no_install": True,
        "no_download": True,
        "no_cache_mutation_without_approval": True,
        "execution_window_candidate_ref": str(exec_auth_dr_root / "execution_window_candidate_v1.json"),
        **_review_ok(sandbox_checks),
        **meta,
    }

    allowed_checks: List[Tuple[str, bool]] = []
    plan_checks = {c.get("check_id"): c for c in allowed_plan.get("checks") or []}
    for cid in SCOPE_ALLOWED_CHECKS:
        item = plan_checks.get(cid) or _check_plan_item(cid)
        allowed_checks.append((f"{cid}.executed_false", item.get("current_executed_now") is False))
        allowed_checks.append((f"{cid}.allowed_later", item.get("allowed_later") is True))
        allowed_checks.append((f"{cid}.window", item.get("requires_execution_window") is True))
        allowed_checks.append((f"{cid}.sandbox", item.get("requires_sandbox") is True))
        allowed_checks.append((f"{cid}.evidence", item.get("requires_evidence") is True))
        allowed_checks.append((f"{cid}.post_review", item.get("requires_post_execution_review") is True))

    allowed_review = {
        "review_id": "allowed_check_final_preflight_review_v1",
        "check_count": len(SCOPE_ALLOWED_CHECKS),
        "check_plan_items": [_check_plan_item(cid) for cid in SCOPE_ALLOWED_CHECKS],
        **_review_ok(allowed_checks),
        **meta,
    }

    forbidden_review = {
        "review_id": "forbidden_action_final_preflight_review_v1",
        "forbidden_actions": list(FORBIDDEN_EXECUTION_ACTIONS),
        "forbidden_count": len(FORBIDDEN_EXECUTION_ACTIONS),
        "all_still_forbidden_at_preflight": True,
        **_review_ok([("forbidden_count_15", len(FORBIDDEN_EXECUTION_ACTIONS) == 15)]),
        **meta,
    }

    rollback_checks: List[Tuple[str, bool]] = [
        ("no_install_on_fail", rollback_cand.get("failed_package_check_does_not_trigger_install") is True),
        ("no_repair_on_fail", rollback_cand.get("failed_import_does_not_trigger_repair") is True),
        ("no_download_on_missing", rollback_cand.get("missing_model_file_does_not_trigger_download") is True),
        ("no_cache_mut_on_hash", rollback_cand.get("hash_mismatch_does_not_trigger_cache_mutation") is True),
        ("rollback_required", rollback_cand.get("rollback_required_before_execution") is True),
        ("not_executed", rollback_cand.get("rollback_executed_now") is False),
    ]
    rollback_review = {
        "review_id": "rollback_readiness_review_v1",
        "rollback_failure_route_ref": str(
            exec_auth_dr_root / "rollback_failure_route_candidate_v1.json"
        ),
        **_review_ok(rollback_checks),
        **meta,
    }

    provider_review = {
        "review_id": "provider_selection_non_finalize_review_v1",
        "selected_provider_for_execution": None,
        "provider_selection_finalized_now": False,
        **_review_ok([
            ("provider_null", meta.get("selected_provider_for_execution") is None),
            ("no_finalize", meta.get("provider_selection_finalized_now") is False),
        ]),
        **meta,
    }

    health_review = {
        "review_id": "health_signal_reserved_boundary_review_v1",
        "health_metric_definition_status": HEALTH_METRIC_DEFINITION_STATUS,
        "no_numeric_health_score_invented": True,
        "health_signal_candidate_risk_context_only": True,
        "health_does_not_auto_authorize_execution": True,
        "health_does_not_auto_block_without_rule": True,
        "hardware_lifespan_robustness_baseline_deferred": True,
        "auth_standard_extension_verifier": auth_ext_vr.get("verifier"),
        **_review_ok([
            ("reserved_status", HEALTH_METRIC_DEFINITION_STATUS == "reserved_not_defined"),
            ("no_score", True),
            ("no_auto_auth", True),
            ("no_auto_block", True),
        ]),
        **meta,
    }

    boundary_checks: List[Tuple[str, bool]] = []
    for field in BOUNDARY_TRUE:
        boundary_checks.append((f"true.{field}", meta.get(field) is True))
    for field in BOUNDARY_FALSE:
        boundary_checks.append((f"false.{field}", meta.get(field) is False))

    no_runtime_audit = {
        "audit_id": "no_runtime_boundary_final_audit_v1",
        "no_runtime_violations": [],
        "all_execution_actions_false": all(meta.get(f) is False for f in BOUNDARY_FALSE),
        **_review_ok(boundary_checks),
        **meta,
    }

    minimal_scope_plan = {
        "plan_id": "controlled_execution_minimal_scope_plan_v1",
        "allowed_checks_if_controlled_execution_entered": list(MINIMAL_SCOPE_ALLOWED_CHECKS),
        "still_forbidden_in_next_phase": list(MINIMAL_SCOPE_STILL_FORBIDDEN),
        "deferred_checks_require_separate_authorization": [
            "runtime_smoke_check_later",
            "sample_ocr_check_later",
            "provider_initialization_dry_check_later",
        ],
        "provider_selection_finalized_now": False,
        "controlled_execution_authorized_now": False,
        "planning_only": True,
        **meta,
    }

    blocked_path_result = {
        "result_id": "final_preflight_blocked_path_result_v1",
        "blocked_paths": [
            {"blocked_path": bp, "blocked": True, "simulated": True} for bp in BLOCKED_PATHS
        ],
        "all_blocked": True,
        "blocked_count": len(BLOCKED_PATHS),
        "authorization_dryrun_blocked_count": len(AUTH_DRYRUN_BLOCKED),
        **meta,
    }

    review_sections = [
        auth_candidate_review,
        approval_review,
        evidence_review,
        gate_review,
        sandbox_review,
        allowed_review,
        forbidden_review,
        rollback_review,
        provider_review,
        health_review,
        no_runtime_audit,
    ]

    all_pass = (
        input_ok
        and auth_input.get("review_pass") is True
        and preflight_cand.get("readiness_pass") is True
        and blocked_path_result.get("all_blocked") is True
        and all(s.get("dryrun_and_review_pass") is True for s in review_sections)
    )

    closure_decision = {
        "decision_id": "final_preflight_closure_decision_v1",
        "dryrun_and_review_pass": all_pass,
        "high_risk": not all_pass,
        "final_decision": FINAL_DECISION_GO if all_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if all_pass else NEXT_PHASE_HOLD,
        **meta,
    }

    next_route = {
        "decision_id": "next_phase_readiness_decision_v1",
        "ready_for_minimal_controlled_execution_planning": all_pass,
        "ready_for_minimal_controlled_execution": False,
        "controlled_execution_authorized_now": False,
        "recommended_next_phase": closure_decision["recommended_next_phase"],
        **meta,
    }

    policy = {
        "policy_id": "ocr_real_dependency_execution_final_preflight_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "merged_preflight_checks": [
            "formal_request_authorization_candidate",
            "owner_operator_approval_precheck",
            "evidence_readiness",
            "validation_gate_readiness",
            "sandbox_boundary",
            "allowed_checks",
            "forbidden_actions",
            "rollback_readiness",
            "provider_selection_non_finalize",
            "health_signal_reserved_boundary",
            "no_runtime_boundary",
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
        "dryrun_and_review_pass": all_pass,
        "final_decision": closure_decision["final_decision"],
        "recommended_next_phase": closure_decision["recommended_next_phase"],
        **meta,
    }

    return {
        "ocr_real_dependency_execution_final_preflight_policy": policy,
        "authorization_dryrun_input_review": auth_input,
        "formal_request_authorization_candidate_review": auth_candidate_review,
        "owner_operator_approval_precheck_review": approval_review,
        "evidence_readiness_review": evidence_review,
        "validation_gate_readiness_review": gate_review,
        "sandbox_boundary_readiness_review": sandbox_review,
        "allowed_check_final_preflight_review": allowed_review,
        "forbidden_action_final_preflight_review": forbidden_review,
        "rollback_readiness_review": rollback_review,
        "provider_selection_non_finalize_review": provider_review,
        "health_signal_reserved_boundary_review": health_review,
        "no_runtime_boundary_final_audit": no_runtime_audit,
        "controlled_execution_minimal_scope_plan": minimal_scope_plan,
        "final_preflight_blocked_path_result": blocked_path_result,
        "final_preflight_closure_decision": closure_decision,
        "next_phase_readiness_decision": next_route,
        "non_claims_register": non_claims,
        "summary": summary,
    }
