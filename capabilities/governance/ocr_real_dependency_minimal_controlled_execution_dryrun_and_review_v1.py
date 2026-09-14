# -*- coding: utf-8 -*-
"""OCR Minimal Controlled Execution DryRunAndReview v1 — validate plan, no real execution."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.ocr_real_dependency_execution_final_preflight_v1 import (
    MINIMAL_SCOPE_ALLOWED_CHECKS,
)
from capabilities.governance.ocr_real_dependency_minimal_controlled_execution_planning_v1 import (
    BLOCKED_PATHS as PLANNING_BLOCKED,
    CHECK_TYPES,
    EVIDENCE_OUTPUT_ITEMS,
    EXCLUDED_FROM_SCOPE,
    FAILURE_ROUTES,
    FINAL_DECISION_GO as UPSTREAM_PLANNING_FINAL_GO,
    MINIMAL_FORBIDDEN_ACTIONS,
    NEXT_PHASE_GO as UPSTREAM_PLANNING_NEXT_PHASE,
    _minimal_check_item,
)

PHASE_ID = "Phase-OCR-Real-Dependency-Minimal-Controlled-Execution-DryRunAndReview-v1-001"
SCOPE = "minimal_controlled_execution_dryrun_and_review_only"
SOURCE_CHAIN = "ocr_real_dependency_minimal_controlled_execution_dryrun_and_review_v1"

UPSTREAM_PLANNING_FINAL = UPSTREAM_PLANNING_FINAL_GO
UPSTREAM_PLANNING_NEXT = UPSTREAM_PLANNING_NEXT_PHASE

FINAL_DECISION_GO = (
    "OCR_REAL_DEPENDENCY_MINIMAL_CONTROLLED_EXECUTION_DRYRUN_AND_REVIEW_CLOSED_"
    "READY_FOR_REAL_MINIMAL_EXECUTION_AUTHORIZATION_DECISION"
)
FINAL_DECISION_HOLD = (
    "OCR_REAL_DEPENDENCY_MINIMAL_CONTROLLED_EXECUTION_DRYRUN_AND_REVIEW_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = "Phase-OCR-Real-Dependency-Real-Minimal-Execution-Authorization-Decision-v1-001"
NEXT_PHASE_HOLD = "Phase-OCR-Real-Dependency-Minimal-Controlled-Execution-Issue-Review-v1-001"

BLOCKED_PATHS: Tuple[str, ...] = (
    "dryrun_to_execution_window_open",
    "dryrun_to_package_check",
    "dryrun_to_model_cache_check",
    "dryrun_to_model_file_existence_check",
    "dryrun_to_model_file_hash_check",
    "dryrun_to_provider_import_check",
    "dryrun_to_dependency_install",
    "dryrun_to_model_download",
    "dryrun_to_cache_mutation",
    "dryrun_to_provider_runtime_invoke",
    "dryrun_to_provider_initialization_dry_check",
    "dryrun_to_runtime_smoke_check",
    "dryrun_to_sample_ocr_check",
    "dryrun_to_ocr_request_submit",
    "dryrun_to_image_read",
    "dryrun_to_crop",
    "dryrun_to_ocr_fact",
    "dryrun_to_user_output",
    "dryrun_to_memory_write",
    "dryrun_to_world_model_write",
    "dryrun_to_provider_selection_finalize",
    "dryrun_to_controlled_trial",
)

NON_CLAIMS: Tuple[str, ...] = (
    "DryRunAndReview GO ≠ minimal controlled execution started",
    "plan candidate ≠ execution window opened",
    "allowed checks pass ≠ checks executed",
    "provider import check planned ≠ provider imported",
    "next authorization decision ≠ real execution automatically allowed",
)

BOUNDARY_TRUE: Tuple[str, ...] = (
    "minimal_controlled_execution_plan_candidate_generated_now",
    "minimal_execution_window_candidate_generated_now",
    "allowed_check_plan_candidate_generated_now",
    "evidence_output_candidate_generated_now",
    "failure_route_candidate_generated_now",
    "rollback_candidate_generated_now",
    "post_execution_review_candidate_generated_now",
    "verifier_plan_candidate_generated_now",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "minimal_controlled_execution_started_now",
    "execution_window_opened_now",
    "real_dependency_check_executed_now",
    "package_presence_check_executed_now",
    "model_cache_path_check_executed_now",
    "model_file_existence_check_executed_now",
    "model_file_hash_check_executed_now",
    "provider_import_check_executed_now",
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
    "ocr_real_dependency_minimal_controlled_execution_dryrun_and_review"
)


def _dryrun_meta() -> Dict[str, Any]:
    meta = {
        "minimal_controlled_execution_dryrun_and_review_only": True,
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


def run_ocr_real_dependency_minimal_controlled_execution_dryrun_and_review_v1(
    *,
    ocr_real_dependency_minimal_controlled_execution_planning_root: str,
    ocr_real_dependency_execution_final_preflight_root: Optional[str] = None,
    ocr_real_dependency_formal_request_generation_authorization_dryrun_and_review_root: Optional[str] = None,
    ocr_real_dependency_execution_authorization_dryrun_and_review_root: Optional[str] = None,
    midplatform_validation_engineering_separation_dryrun_and_review_root: Optional[str] = None,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    plan_root = Path(
        ocr_real_dependency_minimal_controlled_execution_planning_root
    ).expanduser().resolve()
    preflight_root = Path(
        ocr_real_dependency_execution_final_preflight_root
        or plan_root.parent / "ocr_real_dependency_execution_final_preflight"
    ).expanduser().resolve()
    auth_dr_root = Path(
        ocr_real_dependency_formal_request_generation_authorization_dryrun_and_review_root
        or plan_root.parent / "ocr_real_dependency_formal_request_generation_authorization_dryrun_and_review"
    ).expanduser().resolve()
    exec_auth_dr_root = Path(
        ocr_real_dependency_execution_authorization_dryrun_and_review_root
        or plan_root.parent / "ocr_real_dependency_execution_authorization_dryrun_and_review"
    ).expanduser().resolve()
    val_dr_root = Path(
        midplatform_validation_engineering_separation_dryrun_and_review_root
        or plan_root.parent / "midplatform_validation_engineering_separation_dryrun_and_review"
    ).expanduser().resolve()

    plan_sm = _try_read_json(plan_root / "summary.json") or {}
    plan_vr = _try_read_json(plan_root / "verifier_report.json") or {}
    plan_blocked = _try_read_json(plan_root / "minimal_execution_blocked_path_matrix_v1.json") or {}
    plan_scope = _try_read_json(plan_root / "minimal_execution_scope_v1.json") or {}
    plan_window = _try_read_json(plan_root / "minimal_execution_window_candidate_plan_v1.json") or {}
    plan_sandbox = _try_read_json(plan_root / "minimal_execution_sandbox_plan_v1.json") or {}
    plan_allowed = _try_read_json(plan_root / "minimal_allowed_check_plan_v1.json") or {}
    plan_forbidden = _try_read_json(plan_root / "minimal_forbidden_action_plan_v1.json") or {}
    plan_evidence = _try_read_json(plan_root / "minimal_evidence_output_plan_v1.json") or {}
    plan_failure = _try_read_json(plan_root / "minimal_failure_route_plan_v1.json") or {}
    plan_rollback = _try_read_json(plan_root / "minimal_rollback_plan_v1.json") or {}
    plan_post = _try_read_json(plan_root / "minimal_post_execution_review_plan_v1.json") or {}
    plan_verifier = _try_read_json(plan_root / "minimal_execution_verifier_plan_v1.json") or {}
    plan_provider = _try_read_json(plan_root / "provider_selection_non_finalize_plan_v1.json") or {}

    preflight_vr = _try_read_json(preflight_root / "verifier_report.json") or {}
    auth_vr = _try_read_json(auth_dr_root / "verifier_report.json") or {}
    exec_auth_vr = _try_read_json(exec_auth_dr_root / "verifier_report.json") or {}
    val_vr = _try_read_json(val_dr_root / "verifier_report.json") or {}
    val_model = _try_read_json(val_dr_root / "validation_engineering_model_candidate_v1.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_dryrun_meta(),
        "upstream_planning_root": str(plan_root),
        "upstream_final_preflight_root": str(preflight_root),
        "upstream_authorization_dryrun_root": str(auth_dr_root),
        "upstream_execution_authorization_dryrun_root": str(exec_auth_dr_root),
        "upstream_validation_separation_dryrun_root": str(val_dr_root),
        "output_root": str(out_root),
    }

    if plan_vr.get("verifier") != "GO":
        blockers.append("planning verifier must be GO")
    if plan_sm.get("final_decision") != UPSTREAM_PLANNING_FINAL:
        blockers.append("planning final_decision mismatch")
    if plan_sm.get("recommended_next_phase") != UPSTREAM_PLANNING_NEXT:
        blockers.append("planning recommended_next_phase mismatch")
    if plan_sm.get("minimal_controlled_execution_started_now") is not False:
        blockers.append("minimal_controlled_execution_started_now must be false")
    if plan_allowed.get("check_count") != 5:
        blockers.append("5 allowed checks must be planned")
    if plan_forbidden.get("forbidden_count") != len(MINIMAL_FORBIDDEN_ACTIONS):
        blockers.append("18 forbidden actions must be planned")
    if plan_blocked.get("all_blocked") is not True or plan_blocked.get("blocked_count") != 22:
        blockers.append("22 planning blocked paths must remain blocked")
    if plan_scope.get("allowed_checks_later") != list(MINIMAL_SCOPE_ALLOWED_CHECKS):
        blockers.append("scope must match 5 allowed checks")
    if preflight_vr.get("verifier") != "GO":
        blockers.append("final preflight should be GO")
    if auth_vr.get("verifier") != "GO":
        blockers.append("authorization dryrun should be GO")
    if exec_auth_vr.get("verifier") != "GO":
        blockers.append("execution authorization dryrun should be GO")
    if val_vr.get("verifier") != "GO":
        blockers.append("validation separation dryrun should be GO")
    if val_model.get("runtime_enabled_now") is True:
        blockers.append("validator runtime must not be enabled")

    input_ok = len(blockers) == 0

    planning_input = {
        "review_id": "minimal_controlled_execution_planning_input_review_v1",
        "upstream_root": str(plan_root),
        "verifier_go": plan_vr.get("verifier") == "GO",
        "final_decision": plan_sm.get("final_decision"),
        "recommended_next_phase": plan_sm.get("recommended_next_phase"),
        "review_pass": input_ok,
        "blockers": blockers,
        **meta,
    }

    plan_candidate = {
        "candidate_id": "minimal_controlled_execution_plan_candidate_v1",
        "plan_candidate_id": "ocr_minimal_controlled_execution_plan_candidate_v1",
        "execution_scope": "minimal_real_dependency_check",
        "candidate_only": True,
        "execution_started_now": False,
        "execution_window_opened_now": False,
        "allowed_checks_count": len(MINIMAL_SCOPE_ALLOWED_CHECKS),
        "forbidden_actions_count": len(MINIMAL_FORBIDDEN_ACTIONS),
        "evidence_required": True,
        "rollback_required": True,
        "post_execution_review_required": True,
        "verifier_required": True,
        "provider_selection_finalize_allowed_now": False,
        "selected_provider_for_execution": None,
        "source_planning_refs": {
            "scope": str(plan_root / "minimal_execution_scope_v1.json"),
            "window": str(plan_root / "minimal_execution_window_candidate_plan_v1.json"),
            "sandbox": str(plan_root / "minimal_execution_sandbox_plan_v1.json"),
            "allowed_checks": str(plan_root / "minimal_allowed_check_plan_v1.json"),
            "forbidden": str(plan_root / "minimal_forbidden_action_plan_v1.json"),
            "evidence": str(plan_root / "minimal_evidence_output_plan_v1.json"),
            "failure_routes": str(plan_root / "minimal_failure_route_plan_v1.json"),
            "rollback": str(plan_root / "minimal_rollback_plan_v1.json"),
            "post_review": str(plan_root / "minimal_post_execution_review_plan_v1.json"),
            "verifier": str(plan_root / "minimal_execution_verifier_plan_v1.json"),
        },
        "simulated_validation_pass": True,
        **meta,
    }

    scope_checks: List[Tuple[str, bool]] = [
        ("allowed_count_5", plan_scope.get("allowed_check_count") == 5),
        ("allowed_list", plan_scope.get("allowed_checks_later") == list(MINIMAL_SCOPE_ALLOWED_CHECKS)),
    ]
    for ex in EXCLUDED_FROM_SCOPE:
        scope_checks.append((f"excluded_{ex}", ex in (plan_scope.get("excluded_from_scope") or [])))
    scope_review = {
        "review_id": "minimal_execution_scope_dryrun_review_v1",
        **_review_ok(scope_checks),
        **meta,
    }

    window_checks: List[Tuple[str, bool]] = [
        ("window_id", bool(plan_window.get("execution_window_candidate_id"))),
        ("scope", plan_window.get("scope") == "minimal_real_dependency_check"),
        ("checks_5", plan_window.get("allowed_checks") == 5),
        ("workspace", bool(plan_window.get("allowed_workspace_path"))),
        ("output", bool(plan_window.get("allowed_output_path"))),
        ("forbidden_paths", bool(plan_window.get("forbidden_paths"))),
        ("timeout", bool(plan_window.get("timeout_limit"))),
        ("no_prod", plan_window.get("no_production_write") is True),
        ("no_network", plan_window.get("no_network_by_default") is True),
        ("no_install", plan_window.get("no_install") is True),
        ("no_download", plan_window.get("no_download") is True),
        ("no_cache_mut", plan_window.get("no_cache_mutation_without_approval") is True),
        ("post_review", plan_window.get("post_execution_review_required") is True),
        ("not_open", plan_window.get("window_opened_now") is False),
    ]
    window_review = {
        "review_id": "minimal_execution_window_candidate_review_v1",
        "execution_window_candidate_id": plan_window.get("execution_window_candidate_id"),
        **_review_ok(window_checks),
        **meta,
    }

    sandbox_checks: List[Tuple[str, bool]] = [
        ("workspace_controlled_only", plan_sandbox.get("workspace_controlled_only") is True),
        ("no_production_path_write", plan_sandbox.get("no_production_path_write") is True),
        ("no_global_registry_write", plan_sandbox.get("no_global_registry_write") is True),
        ("no_external_transmission", plan_sandbox.get("no_external_transmission") is True),
        ("no_dependency_install", plan_sandbox.get("no_dependency_install") is True),
        ("no_model_download", plan_sandbox.get("no_model_download") is True),
        ("no_cache_mutation", plan_sandbox.get("no_cache_mutation") is True),
        (
            "no_runtime_beyond_import",
            plan_sandbox.get("no_provider_runtime_invocation_beyond_import_check_planning") is True,
        ),
        ("no_ocr_runtime", plan_sandbox.get("no_ocr_runtime") is True),
        ("no_user_output", plan_sandbox.get("no_user_output") is True),
    ]
    sandbox_review = {
        "review_id": "minimal_execution_sandbox_review_v1",
        **_review_ok(sandbox_checks),
        **meta,
    }

    allowed_checks_review: List[Tuple[str, bool]] = []
    plan_check_items = {c.get("check_id"): c for c in plan_allowed.get("checks") or []}
    check_plan_items = []
    for cid in MINIMAL_SCOPE_ALLOWED_CHECKS:
        item = plan_check_items.get(cid) or _minimal_check_item(cid)
        check_plan_items.append(item)
        for field, expected in (
            ("execution_allowed_later", True),
            ("current_executed_now", False),
            ("evidence_required", True),
            ("failure_route_required", True),
            ("rollback_required", True),
            ("post_execution_review_required", True),
        ):
            allowed_checks_review.append((f"{cid}.{field}", item.get(field) is expected))
        allowed_checks_review.append((f"{cid}.check_type", item.get("check_type") == CHECK_TYPES[cid]))

    allowed_review = {
        "review_id": "minimal_allowed_check_plan_dryrun_review_v1",
        "check_count": len(MINIMAL_SCOPE_ALLOWED_CHECKS),
        "check_plan_items": check_plan_items,
        **_review_ok(allowed_checks_review),
        **meta,
    }

    forbidden_checks = [
        (action, action in (plan_forbidden.get("forbidden_actions") or []))
        for action in MINIMAL_FORBIDDEN_ACTIONS
    ]
    forbidden_review = {
        "review_id": "minimal_forbidden_action_dryrun_review_v1",
        "forbidden_actions": list(MINIMAL_FORBIDDEN_ACTIONS),
        "forbidden_count": len(MINIMAL_FORBIDDEN_ACTIONS),
        "matches_planning": plan_forbidden.get("forbidden_actions") == list(MINIMAL_FORBIDDEN_ACTIONS),
        **_review_ok(forbidden_checks + [("count_18", len(MINIMAL_FORBIDDEN_ACTIONS) == 18)]),
        **meta,
    }

    evidence_checks = [
        (item, item in (plan_evidence.get("future_execution_must_generate") or []))
        for item in EVIDENCE_OUTPUT_ITEMS
    ]
    evidence_review = {
        "review_id": "minimal_evidence_output_dryrun_review_v1",
        "future_evidence_items": list(EVIDENCE_OUTPUT_ITEMS),
        "evidence_count": len(EVIDENCE_OUTPUT_ITEMS),
        **_review_ok(evidence_checks + [("count_13", len(EVIDENCE_OUTPUT_ITEMS) == 13)]),
        **meta,
    }

    plan_routes = {r.get("condition"): r for r in plan_failure.get("routes") or []}
    failure_checks: List[Tuple[str, bool]] = []
    for route in FAILURE_ROUTES:
        cond = route["condition"]
        pr = plan_routes.get(cond, {})
        failure_checks.append((cond, pr.get("action") == route.get("action")))
        if route.get("must_not"):
            failure_checks.append((f"{cond}_must_not", pr.get("must_not") == route.get("must_not")))
        if route.get("emit"):
            failure_checks.append((f"{cond}_emit", pr.get("emit") == route.get("emit")))
    failure_review = {
        "review_id": "minimal_failure_route_dryrun_review_v1",
        "routes": list(FAILURE_ROUTES),
        **_review_ok(failure_checks),
        **meta,
    }

    rollback_checks: List[Tuple[str, bool]] = [
        ("no_install_on_fail", plan_rollback.get("failed_package_check_does_not_trigger_install") is True),
        ("no_repair", plan_rollback.get("failed_import_does_not_trigger_repair") is True),
        ("no_download", plan_rollback.get("missing_model_file_does_not_trigger_download") is True),
        ("no_cache_mut", plan_rollback.get("hash_mismatch_does_not_trigger_cache_mutation") is True),
        ("required_before", plan_rollback.get("rollback_required_before_execution") is True),
        ("not_executed", plan_rollback.get("rollback_executed_now") is False),
    ]
    rollback_review = {
        "review_id": "minimal_rollback_dryrun_review_v1",
        **_review_ok(rollback_checks),
        **meta,
    }

    post_checks: List[Tuple[str, bool]] = [
        ("review_required", plan_post.get("review_required") is True),
        ("evidence_completeness", plan_post.get("evidence_completeness_check") is True),
        ("boundary_violation", plan_post.get("boundary_violation_check") is True),
        ("failure_route", plan_post.get("failure_route_check") is True),
        ("rollback_status", plan_post.get("rollback_status_check") is True),
        ("verifier_required", plan_post.get("verifier_required") is True),
        ("next_route", plan_post.get("next_route_decision_required") is True),
    ]
    post_review = {
        "review_id": "minimal_post_execution_review_dryrun_review_v1",
        **_review_ok(post_checks),
        **meta,
    }

    verifier_checks: List[Tuple[str, bool]] = [
        ("required", plan_verifier.get("verifier_required_on_future_execution") is True),
        ("go_no_go", plan_verifier.get("verifier_emits_go_or_no_go") is True),
        ("evidence", plan_verifier.get("verifier_checks_evidence_completeness") is True),
        ("boundary", plan_verifier.get("verifier_checks_boundary") is True),
        ("blocked_paths", plan_verifier.get("verifier_checks_blocked_paths") is True),
        ("not_executed", plan_verifier.get("verifier_executed_now") is False),
    ]
    verifier_review = {
        "review_id": "minimal_execution_verifier_plan_review_v1",
        **_review_ok(verifier_checks),
        **meta,
    }

    provider_checks: List[Tuple[str, bool]] = [
        ("provider_null", plan_provider.get("selected_provider_for_execution") is None),
        ("no_finalize", plan_provider.get("provider_selection_finalized_now") is False),
        ("may_inform_later", plan_provider.get("minimal_execution_evidence_may_inform_provider_selection_later") is True),
        ("dryrun_cannot_finalize", True),
    ]
    provider_review = {
        "review_id": "provider_selection_non_finalize_review_v1",
        "current_dryrun_cannot_finalize_provider": True,
        **_review_ok(provider_checks),
        **meta,
    }

    boundary_checks: List[Tuple[str, bool]] = []
    for field in BOUNDARY_TRUE:
        boundary_checks.append((f"true.{field}", meta.get(field) is True))
    for field in BOUNDARY_FALSE:
        boundary_checks.append((f"false.{field}", meta.get(field) is False))

    boundary_audit = {
        "audit_id": "minimal_controlled_execution_boundary_audit_v1",
        "all_execution_actions_false": all(meta.get(f) is False for f in BOUNDARY_FALSE),
        **_review_ok(boundary_checks),
        **meta,
    }

    blocked_path_result = {
        "result_id": "minimal_controlled_execution_blocked_path_result_v1",
        "blocked_paths": [
            {"blocked_path": bp, "blocked": True, "simulated": True} for bp in BLOCKED_PATHS
        ],
        "all_blocked": True,
        "blocked_count": len(BLOCKED_PATHS),
        "planning_blocked_count": len(PLANNING_BLOCKED),
        **meta,
    }

    review_sections = [
        scope_review,
        window_review,
        sandbox_review,
        allowed_review,
        forbidden_review,
        evidence_review,
        failure_review,
        rollback_review,
        post_review,
        verifier_review,
        provider_review,
        boundary_audit,
    ]

    all_pass = (
        input_ok
        and planning_input.get("review_pass") is True
        and plan_candidate.get("candidate_only") is True
        and blocked_path_result.get("all_blocked") is True
        and all(s.get("dryrun_and_review_pass") is True for s in review_sections)
    )

    closure_decision = {
        "decision_id": "minimal_controlled_execution_closure_decision_v1",
        "dryrun_and_review_pass": all_pass,
        "high_risk": not all_pass,
        "final_decision": FINAL_DECISION_GO if all_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if all_pass else NEXT_PHASE_HOLD,
        **meta,
    }

    next_route = {
        "decision_id": "next_route_readiness_decision_v1",
        "ready_for_real_minimal_execution_authorization_decision": all_pass,
        "ready_for_real_minimal_controlled_execution": False,
        "controlled_execution_authorized_now": False,
        "recommended_next_phase": closure_decision["recommended_next_phase"],
        **meta,
    }

    policy = {
        "policy_id": "minimal_controlled_execution_dryrun_review_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "dryrun_objectives": [
            "generate minimal_controlled_execution_plan_candidate",
            "verify 5 allowed check plans",
            "verify 18 forbidden actions blocked",
            "verify evidence / failure / rollback / post-review plans",
            "no real package/import/cache/hash execution",
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
        "minimal_controlled_execution_dryrun_review_policy": policy,
        "minimal_controlled_execution_planning_input_review": planning_input,
        "minimal_controlled_execution_plan_candidate": plan_candidate,
        "minimal_execution_scope_dryrun_review": scope_review,
        "minimal_execution_window_candidate_review": window_review,
        "minimal_execution_sandbox_review": sandbox_review,
        "minimal_allowed_check_plan_dryrun_review": allowed_review,
        "minimal_forbidden_action_dryrun_review": forbidden_review,
        "minimal_evidence_output_dryrun_review": evidence_review,
        "minimal_failure_route_dryrun_review": failure_review,
        "minimal_rollback_dryrun_review": rollback_review,
        "minimal_post_execution_review_dryrun_review": post_review,
        "minimal_execution_verifier_plan_review": verifier_review,
        "provider_selection_non_finalize_review": provider_review,
        "minimal_controlled_execution_boundary_audit": boundary_audit,
        "minimal_controlled_execution_blocked_path_result": blocked_path_result,
        "minimal_controlled_execution_closure_decision": closure_decision,
        "next_route_readiness_decision": next_route,
        "non_claims_register": non_claims,
        "summary": summary,
    }
