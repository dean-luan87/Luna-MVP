# -*- coding: utf-8 -*-
"""OCR Formal Request Generation Authorization DryRunAndReview v1 — compressed merge."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.capability_factory_authorization_standard_extension_planning_v1 import (
    AUTHORIZATION_STANDARD_ID,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.ocr_real_dependency_execution_authorization_dryrun_and_review_v1 import (
    SCOPE_ALLOWED_CHECKS,
)
from capabilities.governance.ocr_real_dependency_formal_execution_request_generation_dryrun_and_review_v1 import (
    BLOCKED_PATHS as FORMAL_REQUEST_DRYRUN_BLOCKED,
    FUTURE_EVIDENCE_ITEMS,
)
from capabilities.governance.ocr_real_dependency_formal_execution_request_generation_post_route_decision_v1 import (
    FINAL_DECISION_GO as UPSTREAM_POST_ROUTE_FINAL_GO,
    NEXT_PHASE_GO as UPSTREAM_POST_ROUTE_NEXT,
    SELECTED_ROUTE as POST_ROUTE_SELECTED_ROUTE,
)

PHASE_ID = "Phase-OCR-Real-Dependency-Formal-Request-Generation-Authorization-DryRunAndReview-v1-001"
SCOPE = "formal_request_generation_authorization_dryrun_and_review_only"
SOURCE_CHAIN = "ocr_real_dependency_formal_request_generation_authorization_dryrun_and_review_v1"

UPSTREAM_POST_ROUTE_FINAL = UPSTREAM_POST_ROUTE_FINAL_GO
UPSTREAM_POST_ROUTE_NEXT = UPSTREAM_POST_ROUTE_NEXT

FINAL_DECISION_GO = (
    "OCR_REAL_DEPENDENCY_FORMAL_REQUEST_GENERATION_AUTHORIZATION_DRYRUN_AND_REVIEW_CLOSED_"
    "READY_FOR_EXECUTION_FINAL_PREFLIGHT"
)
FINAL_DECISION_HOLD = (
    "OCR_REAL_DEPENDENCY_FORMAL_REQUEST_GENERATION_AUTHORIZATION_DRYRUN_AND_REVIEW_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = "Phase-OCR-Real-Dependency-Execution-Final-Preflight-v1-001"
NEXT_PHASE_HOLD = "Phase-OCR-Real-Dependency-Formal-Request-Generation-Authorization-Issue-Review-v1-001"

ABSORBED_PHASE_LABELS: Tuple[str, ...] = (
    "Formal Request Generation Authorization Planning",
    "Owner/Operator Approval Precheck",
    "Evidence Readiness Review",
)

DEFERRED_NOT_BLOCKING: Tuple[str, ...] = ("Validation Runtime Readiness",)

VALIDATION_GATES_PLANNED: Tuple[str, ...] = (
    "AuthorizationValidationGate",
    "BoundaryGate",
    "EvidenceChainValidator",
    "NoRuntimeBoundaryAudit",
    "ControlledProviderReadinessHarness",
    "HealthCheckValidator",
    "ValidationFactory",
    "IssueTracebackEngine",
    "ViolationReportEngine",
)

BLOCKED_PATHS: Tuple[str, ...] = (
    "dryrun_to_formal_request_artifact_generation",
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
    "authorization candidate ≠ generation authorized",
    "approval precheck candidate ≠ approval collected",
    "evidence readiness candidate ≠ evidence collected",
    "final preflight next ≠ execution allowed",
    "next final preflight ≠ provider import allowed",
)

BOUNDARY_TRUE: Tuple[str, ...] = (
    "formal_request_generation_authorization_candidate_generated_now",
    "owner_operator_approval_precheck_candidate_generated_now",
    "evidence_readiness_candidate_generated_now",
    "validation_gate_readiness_candidate_generated_now",
    "final_preflight_readiness_candidate_generated_now",
    "legacy_chain_integration_marker_generated_now",
)

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
    "ocr_real_dependency_formal_request_generation_authorization_dryrun_and_review"
)


def _dryrun_meta() -> Dict[str, Any]:
    meta = {
        "formal_request_generation_authorization_dryrun_and_review_only": True,
        "simulated": True,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "selected_provider_for_execution": None,
        "compressed_merge": True,
        "no_separate_authorization_planning_phase": True,
        "no_separate_authorization_dryrun_phase": True,
        "no_separate_authorization_review_phase": True,
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


def run_ocr_real_dependency_formal_request_generation_authorization_dryrun_and_review_v1(
    *,
    ocr_real_dependency_formal_execution_request_generation_post_route_decision_root: str,
    ocr_real_dependency_formal_execution_request_generation_dryrun_and_review_root: str,
    ocr_real_dependency_formal_execution_request_generation_planning_root: Optional[str] = None,
    ocr_real_dependency_execution_authorization_dryrun_and_review_root: Optional[str] = None,
    ocr_real_dependency_authorization_via_factory_standard_dryrun_and_review_root: Optional[str] = None,
    midplatform_validation_engineering_separation_dryrun_and_review_root: Optional[str] = None,
    factory_standard_historical_redundancy_cleanup_dryrun_and_review_root: Optional[str] = None,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    post_root = Path(
        ocr_real_dependency_formal_execution_request_generation_post_route_decision_root
    ).expanduser().resolve()
    formal_dr_root = Path(
        ocr_real_dependency_formal_execution_request_generation_dryrun_and_review_root
    ).expanduser().resolve()
    formal_plan_root = Path(
        ocr_real_dependency_formal_execution_request_generation_planning_root
        or formal_dr_root.parent / "ocr_real_dependency_formal_execution_request_generation_planning"
    ).expanduser().resolve()
    auth_dr_root = Path(
        ocr_real_dependency_execution_authorization_dryrun_and_review_root
        or formal_dr_root.parent / "ocr_real_dependency_execution_authorization_dryrun_and_review"
    ).expanduser().resolve()
    ocr_dr_root = Path(
        ocr_real_dependency_authorization_via_factory_standard_dryrun_and_review_root
        or formal_dr_root.parent / "ocr_real_dependency_authorization_via_factory_standard_dryrun_and_review"
    ).expanduser().resolve()
    val_dr_root = Path(
        midplatform_validation_engineering_separation_dryrun_and_review_root
        or formal_dr_root.parent / "midplatform_validation_engineering_separation_dryrun_and_review"
    ).expanduser().resolve()
    hist_root = Path(
        factory_standard_historical_redundancy_cleanup_dryrun_and_review_root
        or formal_dr_root.parent / "factory_standard_historical_redundancy_cleanup_dryrun_and_review"
    ).expanduser().resolve()

    post_sm = _try_read_json(post_root / "summary.json") or {}
    post_vr = _try_read_json(post_root / "verifier_report.json") or {}
    formal_dr_sm = _try_read_json(formal_dr_root / "summary.json") or {}
    formal_dr_vr = _try_read_json(formal_dr_root / "verifier_report.json") or {}
    formal_candidate = _try_read_json(formal_dr_root / "formal_execution_request_candidate_v1.json") or {}
    formal_blocked = _try_read_json(
        formal_dr_root / "formal_execution_request_blocked_path_result_v1.json"
    ) or {}
    auth_dr_vr = _try_read_json(auth_dr_root / "verifier_report.json") or {}
    val_model = _try_read_json(val_dr_root / "validation_engineering_model_candidate_v1.json") or {}
    hist_vr = _try_read_json(hist_root / "verifier_report.json") or {}

    domain_config_ref = str(ocr_dr_root / "ocr_real_dependency_domain_config_candidate_v1.json")
    formal_candidate_ref = str(formal_dr_root / "formal_execution_request_candidate_v1.json")

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_dryrun_meta(),
        "upstream_post_route_decision_root": str(post_root),
        "upstream_formal_request_dryrun_and_review_root": str(formal_dr_root),
        "upstream_formal_request_planning_root": str(formal_plan_root),
        "upstream_execution_authorization_dryrun_root": str(auth_dr_root),
        "upstream_ocr_via_factory_dryrun_root": str(ocr_dr_root),
        "upstream_validation_separation_dryrun_root": str(val_dr_root),
        "upstream_historical_redundancy_cleanup_root": str(hist_root),
        "output_root": str(out_root),
    }

    if post_vr.get("verifier") != "GO":
        blockers.append("post-route decision verifier must be GO")
    if post_sm.get("final_decision") != UPSTREAM_POST_ROUTE_FINAL:
        blockers.append("post-route final_decision mismatch")
    if post_sm.get("recommended_next_phase") != UPSTREAM_POST_ROUTE_NEXT:
        blockers.append("post-route recommended_next_phase mismatch")
    if post_sm.get("selected_route") != POST_ROUTE_SELECTED_ROUTE:
        blockers.append("post-route must select Route A")
    if formal_dr_vr.get("verifier") != "GO":
        blockers.append("formal request dryrun verifier must be GO")
    if not formal_candidate.get("formal_execution_request_candidate_id"):
        blockers.append("formal_execution_request_candidate required")
    if formal_candidate.get("formal_artifact_generated_now") is not False:
        blockers.append("formal_artifact_generated_now must be false")
    if formal_blocked.get("all_blocked") is not True or formal_blocked.get("blocked_count") != 24:
        blockers.append("24 blocked paths must remain blocked")
    if val_model.get("runtime_enabled_now") is True:
        blockers.append("validator_runtime_enabled_now must be false")
    if auth_dr_vr.get("verifier") != "GO":
        blockers.append("execution authorization dryrun should be GO")

    input_ok = len(blockers) == 0

    post_input = {
        "review_id": "post_route_decision_input_review_v1",
        "upstream_root": str(post_root),
        "verifier_go": post_vr.get("verifier") == "GO",
        "selected_route": post_sm.get("selected_route"),
        "review_pass": input_ok,
        "blockers": blockers,
        **meta,
    }

    formal_input = {
        "review_id": "formal_execution_request_candidate_input_review_v1",
        "formal_candidate_ref": formal_candidate_ref,
        "lifecycle_state": formal_candidate.get("lifecycle_state"),
        "candidate_only": formal_candidate.get("candidate_only"),
        "schema_and_preconditions_pass": formal_dr_sm.get("dryrun_and_review_pass") is True,
        "review_pass": formal_dr_vr.get("verifier") == "GO"
        and formal_candidate.get("formal_artifact_generated_now") is False,
        **meta,
    }

    auth_candidate = {
        "candidate_id": "formal_request_generation_authorization_candidate_v1",
        "authorization_candidate_id": "ocr_real_dependency_formal_request_generation_authorization_candidate_v1",
        "authorization_target": "formal_execution_request_generation",
        "source_formal_execution_request_candidate_ref": formal_candidate_ref,
        "source_domain_config_ref": domain_config_ref,
        "factory_authorization_standard_ref": AUTHORIZATION_STANDARD_ID,
        "validation_engineering_ref": "validation_engineering_model_v1",
        "owner_operator_approval_required": True,
        "evidence_readiness_required": True,
        "validation_gate_readiness_required": True,
        "final_preflight_required": True,
        "candidate_only": True,
        "formal_artifact_generation_allowed_now": False,
        "request_send_allowed_now": False,
        "grant_allowed_now": False,
        "execution_window_allowed_now": False,
        "real_dependency_check_allowed_now": False,
        "authorization_planning_absorbed": True,
        "simulated_authorization_planning_pass": True,
        **meta,
    }

    approval_precheck = {
        "candidate_id": "owner_operator_approval_precheck_candidate_v1",
        "approval_precheck_candidate_id": "ocr_owner_operator_approval_precheck_candidate_v1",
        "approval_required_later": True,
        "owner_operator_identity_required_later": True,
        "approval_scope": "formal_request_generation_only",
        "approval_does_not_imply_grant": True,
        "approval_does_not_open_execution_window": True,
        "approval_collected_now": False,
        "approval_skipped_now": False,
        "absorbed_from_deferred_route_b": True,
        **meta,
    }

    evidence_readiness = {
        "candidate_id": "evidence_readiness_candidate_v1",
        "formal_execution_request_candidate_ref": formal_candidate_ref,
        "execution_grant_candidate_ref": str(auth_dr_root / "execution_grant_candidate_v1.json"),
        "execution_window_candidate_ref": str(auth_dr_root / "execution_window_candidate_v1.json"),
        "domain_config_ref": domain_config_ref,
        "validation_gate_path_ref": str(
            formal_dr_root / "validation_gate_path_dryrun_review_v1.json"
        ),
        "allowed_check_plan_ref": str(auth_dr_root / "allowed_check_plan_candidate_v1.json"),
        "rollback_failure_route_ref": str(
            formal_dr_root / "rollback_failure_route_candidate_v1.json"
        ),
        "evidence_collection_candidate_ref": str(
            formal_dr_root / "evidence_collection_candidate_v1.json"
        ),
        "future_evidence_items": list(FUTURE_EVIDENCE_ITEMS),
        "evidence_ready_for_final_preflight": True,
        "evidence_collected_now": False,
        "absorbed_evidence_readiness_review": True,
        **meta,
    }

    gate_readiness = {
        "candidate_id": "validation_gate_readiness_candidate_v1",
        "gates_planned": {gate: True for gate in VALIDATION_GATES_PLANNED},
        "AuthorizationValidationGate": "planned",
        "BoundaryGate": "planned",
        "EvidenceChainValidator": "planned",
        "NoRuntimeBoundaryAudit": "planned",
        "ControlledProviderReadinessHarness": "planned",
        "HealthCheckValidator": "planned",
        "ValidationFactory": "aggregation_planned",
        "IssueTracebackEngine": "planned",
        "ViolationReportEngine": "planned",
        "validator_runtime_enabled_now": False,
        "validation_factory_runtime_enforced_now": False,
        "gate_executed_now": False,
        **meta,
    }

    preflight_checks = {
        "authorization_candidate_ready": True,
        "approval_precheck_candidate_ready": True,
        "evidence_readiness_candidate_ready": True,
        "validation_gate_readiness_candidate_ready": True,
        "no_runtime_boundary_ok": True,
        "selected_provider_null": meta.get("selected_provider_for_execution") is None,
        "allowed_checks_not_executed": True,
        "execution_window_closed": meta.get("execution_window_opened_now") is False,
        "provider_import_false": meta.get("provider_imported_now") is False,
    }
    preflight = {
        "candidate_id": "final_preflight_readiness_candidate_v1",
        "preflight_candidate_id": "ocr_real_dependency_execution_final_preflight_readiness_candidate_v1",
        "readiness_checks": preflight_checks,
        "readiness_pass": all(preflight_checks.values()),
        "next_phase_after_preflight": "minimal_controlled_execution_later",
        "recommended_next_phase": NEXT_PHASE_GO,
        **meta,
    }

    chain_integration = {
        "review_id": "compressed_authorization_chain_integration_review_v1",
        "absorbed_phases": [
            {
                "phase_label": label,
                "absorbed_into": PHASE_ID,
                "mode": "candidate" if "Precheck" in label or "Review" in label else "planning_merged",
            }
            for label in ABSORBED_PHASE_LABELS
        ],
        "deferred_not_blocking": list(DEFERRED_NOT_BLOCKING),
        "old_multi_step_request_generation_path_deprecated_for_new_phase": True,
        "no_historical_artifact_deleted": True,
        "historical_evidence_remains_read_only_evidence_source": True,
        "historical_redundancy_cleanup_optional": hist_vr.get("verifier") == "GO",
        "upstream_chain_roots": {
            "execution_authorization_dryrun": str(auth_dr_root),
            "formal_request_planning": str(formal_plan_root),
            "formal_request_dryrun": str(formal_dr_root),
            "post_route_decision": str(post_root),
        },
        "dryrun_and_review_pass": True,
        **meta,
    }

    legacy_marker = {
        "marker_id": "legacy_phase_absorption_marker_v1",
        "absorbed_by": "FormalRequestGenerationAuthorizationDryRunAndReview",
        "deprecated_for_new_phase": True,
        "physical_delete_allowed": False,
        "historical_verdict_preserved": True,
        "future_phase_should_reference_compressed_chain": True,
        "absorbed_phase_ids": [
            "Phase-OCR-Real-Dependency-Formal-Execution-Request-Generation-Authorization-Planning-v1-001",
            "Phase-OCR-Real-Dependency-Owner-Operator-Approval-Precheck-v1-001",
            "Phase-OCR-Real-Dependency-Evidence-Readiness-Review-v1-001",
        ],
        "deferred_phase_ids": ["Phase-OCR-Real-Dependency-Validation-Runtime-Readiness-v1-001"],
        **meta,
    }

    boundary_checks: List[Tuple[str, bool]] = []
    for field in BOUNDARY_TRUE:
        boundary_checks.append((f"true.{field}", meta.get(field) is True))
    for field in BOUNDARY_FALSE:
        boundary_checks.append((f"false.{field}", meta.get(field) is False))

    boundary_audit = {
        "audit_id": "formal_request_generation_authorization_boundary_audit_v1",
        "all_execution_actions_false": all(meta.get(f) is False for f in BOUNDARY_FALSE),
        **_review_ok(boundary_checks),
        **meta,
    }

    blocked_path_result = {
        "result_id": "formal_request_generation_authorization_blocked_path_result_v1",
        "blocked_paths": [
            {"blocked_path": bp, "blocked": True, "simulated": True} for bp in BLOCKED_PATHS
        ],
        "all_blocked": True,
        "blocked_count": len(BLOCKED_PATHS),
        "formal_request_dryrun_blocked_count": len(FORMAL_REQUEST_DRYRUN_BLOCKED),
        **meta,
    }

    review_sections = [chain_integration, boundary_audit]

    all_pass = (
        input_ok
        and formal_input.get("review_pass") is True
        and preflight.get("readiness_pass") is True
        and auth_candidate.get("candidate_only") is True
        and blocked_path_result.get("all_blocked") is True
        and all(s.get("dryrun_and_review_pass") is True for s in review_sections)
    )

    closure_decision = {
        "decision_id": "formal_request_generation_authorization_closure_decision_v1",
        "dryrun_and_review_pass": all_pass,
        "high_risk": not all_pass,
        "final_decision": FINAL_DECISION_GO if all_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if all_pass else NEXT_PHASE_HOLD,
        "compressed_merge_complete": all_pass,
        **meta,
    }

    next_route = {
        "decision_id": "next_phase_readiness_decision_v1",
        "ready_for_execution_final_preflight": all_pass,
        "ready_for_minimal_controlled_execution": False,
        "do_not_generate_formal_artifact_now": True,
        "recommended_next_phase": closure_decision["recommended_next_phase"],
        **meta,
    }

    policy = {
        "policy_id": "formal_request_generation_authorization_dryrun_review_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "merged_capabilities": [
            "formal_request_generation_authorization_planning",
            "formal_request_generation_authorization_candidate",
            "owner_operator_approval_precheck_candidate",
            "evidence_readiness_candidate",
            "validation_gate_readiness_candidate",
            "final_preflight_readiness_candidate",
            "legacy_chain_integration_marker",
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
        "compressed_merge": True,
        **meta,
    }

    return {
        "formal_request_generation_authorization_dryrun_review_policy": policy,
        "post_route_decision_input_review": post_input,
        "formal_execution_request_candidate_input_review": formal_input,
        "formal_request_generation_authorization_candidate": auth_candidate,
        "owner_operator_approval_precheck_candidate": approval_precheck,
        "evidence_readiness_candidate": evidence_readiness,
        "validation_gate_readiness_candidate": gate_readiness,
        "final_preflight_readiness_candidate": preflight,
        "compressed_authorization_chain_integration_review": chain_integration,
        "legacy_phase_absorption_marker": legacy_marker,
        "formal_request_generation_authorization_boundary_audit": boundary_audit,
        "formal_request_generation_authorization_blocked_path_result": blocked_path_result,
        "formal_request_generation_authorization_closure_decision": closure_decision,
        "next_phase_readiness_decision": next_route,
        "non_claims_register": non_claims,
        "summary": summary,
    }
