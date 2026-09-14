# -*- coding: utf-8 -*-
"""OCR Provider Selection / Dependency / Environment DryRun v1 — candidates only."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.ocr_controlled_provider_authorization_roadmap_decision_v1 import (
    SELECTED_ROUTE,
)
from capabilities.governance.ocr_controlled_provider_dryrun_v1 import BLOCKED_PATHS as OCR_CONTROLLED_BLOCKED
from capabilities.governance.ocr_provider_selection_dependency_environment_planning_v1 import (
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
    HEALTH_BINDINGS,
    NEXT_PHASE_GO as PLANNING_NEXT_PHASE,
    PROVIDER_INVENTORY,
    SELECTION_CRITERIA,
    SECURITY_CONFIRMATIONS,
)

PHASE_ID = "Phase-OCR-Provider-Selection-Dependency-Environment-DryRun-v1-001"
SCOPE = "ocr_provider_selection_dependency_environment_dryrun_only"
SOURCE_CHAIN = "ocr_provider_selection_dependency_environment_dryrun_v1"

UPSTREAM_PLANNING_FINAL = PLANNING_FINAL_GO
UPSTREAM_PLANNING_NEXT = PLANNING_NEXT_PHASE

FINAL_DECISION_GO = "OCR_PROVIDER_SELECTION_DEPENDENCY_ENVIRONMENT_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
FINAL_DECISION_HOLD = "OCR_PROVIDER_SELECTION_DEPENDENCY_ENVIRONMENT_DRYRUN_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-OCR-Provider-Selection-Dependency-Environment-Post-DryRun-Review-v1-001"
NEXT_PHASE_HOLD = "Phase-OCR-Provider-Selection-Dependency-Environment-Issue-Review-v1-001"

BLOCKED_PATHS: Tuple[str, ...] = (
    "provider_candidate_to_authorization",
    "provider_selection_candidate_to_final_selection",
    "dependency_plan_to_dependency_install",
    "model_cache_plan_to_model_download",
    "provider_import_plan_to_import_execution",
    "environment_plan_to_runtime_enabled",
    "provider_comparison_to_execution_selection",
    "paddleocr_later_to_paddleocr_import",
    "rapidocr_later_to_rapidocr_import",
    "external_ocr_later_to_external_call",
    "sample_ocr_plan_to_ocr_execution",
    "provider_readiness_to_provider_invocation",
    "ocr_request_to_submit",
    "image_fixture_to_image_read",
    "ocr_result_candidate_to_fact",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "provider_selection_finalized_now",
    "provider_dependency_check_executed_now",
    "environment_readiness_check_executed_now",
    "dependency_install_executed_now",
    "model_download_executed_now",
    "provider_import_check_executed_now",
    "provider_smoke_check_executed_now",
    "sample_ocr_executed_now",
    "provider_authorization_started_now",
    "controlled_trial_started_now",
    "paddleocr_imported_now",
    "rapidocr_imported_now",
    "external_ocr_imported_now",
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
    "fallback_executed_now",
    "retry_executed_now",
    "provider_switch_executed_now",
    "python_package_check_executed_now",
    "model_cache_check_executed_now",
    "model_file_hash_check_executed_now",
    "provider_import_check_executed_now",
    "runtime_smoke_check_executed_now",
)

NON_CLAIMS: Tuple[str, ...] = (
    "DryRun GO ≠ provider selected for execution",
    "DryRun GO ≠ PaddleOCR/RapidOCR imported or invoked",
    "dependency_readiness_candidate ≠ dependency check executed",
    "environment_readiness_candidate ≠ runtime enabled",
    "provider_comparison_matrix_sample ≠ final provider selection",
    "Post-DryRun Review next ≠ real dependency install or OCR",
    "selection candidate generated ≠ provider authorization",
    "model cache plan sample ≠ model downloaded",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_provider_selection_dependency_environment_dryrun"
)

_COMPARISON_SAMPLE: Dict[str, Dict[str, str]] = {
    "mock_or_fixture": {
        "local_availability": "high_fixture",
        "dependency_complexity": "minimal",
        "model_file_readiness": "not_required",
        "runtime_isolation": "sandbox_ok",
        "cpu_memory_pressure": "low",
        "latency_expectation": "minimal",
        "chinese_text_support": "fixture_only",
        "small_text_support": "fixture_only",
        "rotated_text_support": "limited",
        "multi_region_ocr_support": "yes",
        "confidence_output_support": "yes",
        "layout_bbox_output_support": "yes",
        "failure_timeout_handling": "deterministic",
        "candidate_output_compatibility": "full",
        "evidence_pack_compatibility": "full",
        "offline_readiness": "full",
        "license_usage_constraint": "none",
    },
    "paddleocr_later": {
        "local_availability": "pending_dependency",
        "dependency_complexity": "high",
        "model_file_readiness": "pending_download",
        "runtime_isolation": "required",
        "cpu_memory_pressure": "high",
        "latency_expectation": "high",
        "chinese_text_support": "planned_strong",
        "small_text_support": "planned_medium",
        "rotated_text_support": "planned_medium",
        "multi_region_ocr_support": "yes",
        "confidence_output_support": "yes",
        "layout_bbox_output_support": "yes",
        "failure_timeout_handling": "hold_fallback",
        "candidate_output_compatibility": "planned",
        "evidence_pack_compatibility": "planned",
        "offline_readiness": "planned_offline",
        "license_usage_constraint": "apache_review_required",
    },
    "rapidocr_later": {
        "local_availability": "pending_dependency",
        "dependency_complexity": "medium",
        "model_file_readiness": "pending_download",
        "runtime_isolation": "required",
        "cpu_memory_pressure": "medium",
        "latency_expectation": "medium",
        "chinese_text_support": "planned_medium",
        "small_text_support": "planned_medium",
        "rotated_text_support": "planned_low",
        "multi_region_ocr_support": "yes",
        "confidence_output_support": "yes",
        "layout_bbox_output_support": "yes",
        "failure_timeout_handling": "hold_fallback",
        "candidate_output_compatibility": "planned",
        "evidence_pack_compatibility": "planned",
        "offline_readiness": "planned_offline",
        "license_usage_constraint": "apache_review_required",
    },
    "external_ocr_later": {
        "local_availability": "network_required",
        "dependency_complexity": "low_client",
        "model_file_readiness": "not_local",
        "runtime_isolation": "network_sandbox",
        "cpu_memory_pressure": "low",
        "latency_expectation": "network_bound",
        "chinese_text_support": "vendor_dependent",
        "small_text_support": "vendor_dependent",
        "rotated_text_support": "vendor_dependent",
        "multi_region_ocr_support": "vendor_dependent",
        "confidence_output_support": "vendor_dependent",
        "layout_bbox_output_support": "vendor_dependent",
        "failure_timeout_handling": "hold_fallback",
        "candidate_output_compatibility": "planned",
        "evidence_pack_compatibility": "planned",
        "offline_readiness": "none_default",
        "license_usage_constraint": "vendor_tos_required",
    },
}


def _dryrun_meta() -> Dict[str, Any]:
    meta = {
        "ocr_provider_selection_dependency_environment_dryrun_only": True,
        "simulated": True,
        "provider_selection_candidate_generated_now": True,
        "dependency_readiness_candidate_generated_now": True,
        "environment_readiness_candidate_generated_now": True,
        "provider_comparison_matrix_sample_generated_now": True,
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


def _candidate_defaults() -> Dict[str, Any]:
    return {
        "candidate_only": True,
        "simulated": True,
        "action_allowed": False,
        "timestamp": "dryrun_simulated",
    }


def _dependency_row(provider_family: str, meta: Dict[str, Any]) -> Dict[str, Any]:
    return {
        **_candidate_defaults(),
        "provider_family": provider_family,
        "python_package_check_planned": True,
        "model_cache_check_planned": True,
        "model_file_hash_check_planned": True,
        "provider_import_check_planned": True,
        "runtime_smoke_check_planned": True,
        "sample_ocr_check_planned_later": True,
        "python_package_check_executed_now": False,
        "model_cache_check_executed_now": False,
        "model_file_hash_check_executed_now": False,
        "provider_import_check_executed_now": False,
        "runtime_smoke_check_executed_now": False,
        "sample_ocr_check_executed_now": False,
        **meta,
    }


def run_ocr_provider_selection_dependency_environment_dryrun_v1(
    *,
    ocr_provider_selection_dependency_environment_planning_root: str,
    ocr_controlled_provider_authorization_roadmap_decision_root: Optional[str] = None,
    ocr_controlled_provider_post_dryrun_review_root: Optional[str] = None,
    ocr_controlled_provider_dryrun_root: Optional[str] = None,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    planning_root = Path(ocr_provider_selection_dependency_environment_planning_root).expanduser().resolve()
    plan_sm = _try_read_json(planning_root / "summary.json") or {}
    plan_vr = _try_read_json(planning_root / "verifier_report.json") or {}
    plan_decision = _try_read_json(planning_root / "ocr_provider_selection_planning_decision_v1.json") or {}

    roadmap_root = Path(
        ocr_controlled_provider_authorization_roadmap_decision_root
        or planning_root.parent / "ocr_controlled_provider_authorization_roadmap_decision"
    ).expanduser().resolve()
    post_root = Path(
        ocr_controlled_provider_post_dryrun_review_root
        or planning_root.parent / "ocr_controlled_provider_post_dryrun_review"
    ).expanduser().resolve()
    ocr_dryrun_root = Path(
        ocr_controlled_provider_dryrun_root
        or planning_root.parent / "ocr_controlled_provider_dryrun"
    ).expanduser().resolve()

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_dryrun_meta(),
        "upstream_planning_root": str(planning_root),
        "upstream_roadmap_decision_root": str(roadmap_root),
        "upstream_post_dryrun_review_root": str(post_root),
        "upstream_ocr_controlled_provider_dryrun_root": str(ocr_dryrun_root),
        "output_root": str(out_root),
    }

    roadmap_sm = _try_read_json(roadmap_root / "summary.json") or {}
    roadmap_vr = _try_read_json(roadmap_root / "verifier_report.json") or {}
    post_sm = _try_read_json(post_root / "summary.json") or {}
    ocr_dryrun_sm = _try_read_json(ocr_dryrun_root / "summary.json") or {}
    inventory_plan = _try_read_json(planning_root / "ocr_provider_candidate_inventory_v1.json") or {}

    planning_go = plan_vr.get("verifier") == "GO" and plan_vr.get("passed") is True
    if not planning_go:
        blockers.append("planning verifier must be GO")
    if plan_sm.get("final_decision") != UPSTREAM_PLANNING_FINAL:
        blockers.append("planning final_decision mismatch")
    if plan_sm.get("recommended_next_phase") != UPSTREAM_PLANNING_NEXT:
        blockers.append("planning recommended_next_phase mismatch")
    if plan_sm.get("boundary_ok") is not True:
        blockers.append("planning boundary_ok required")
    if plan_decision.get("ready_for_dryrun") is not True:
        blockers.append("planning ready_for_dryrun required")
    if inventory_plan.get("candidate_count") != 4:
        blockers.append("planning provider count must be 4")

    if roadmap_vr.get("verifier") != "GO":
        blockers.append("roadmap decision should be GO")
    if roadmap_sm.get("selected_route") != SELECTED_ROUTE:
        blockers.append("selected_route must be Route B")
    if post_sm.get("ocr_candidate_chain_trusted") is not True:
        blockers.append("ocr_candidate_chain_trusted required")
    if post_sm.get("ocr_controlled_provider_dryrun_closed") is not True:
        blockers.append("ocr_controlled_provider_dryrun_closed required")

    if plan_sm.get("provider_selection_finalized_now") is True:
        blockers.append("provider_selection_finalized_now must be false upstream")
    if plan_sm.get("provider_dependency_check_executed_now") is True:
        blockers.append("dependency checks must not be executed upstream")
    if plan_sm.get("environment_readiness_check_executed_now") is True:
        blockers.append("environment checks must not be executed upstream")

    for field in (
        "paddleocr_invoked_now",
        "rapidocr_invoked_now",
        "external_ocr_invoked_now",
        "paddleocr_imported_now",
        "rapidocr_imported_now",
    ):
        if plan_sm.get(field) is True or ocr_dryrun_sm.get(field) is True:
            blockers.append(f"{field} must be false upstream")

    input_review = {
        "review_id": "provider_selection_planning_input_review_v1",
        "upstream_planning_root": str(planning_root),
        "upstream_roadmap_root": str(roadmap_root),
        "upstream_verifier_go": planning_go,
        "upstream_final_decision": plan_sm.get("final_decision"),
        "selected_route": roadmap_sm.get("selected_route"),
        "provider_candidate_count": inventory_plan.get("candidate_count"),
        "provider_selection_finalized_upstream": plan_sm.get("provider_selection_finalized_now"),
        "dependency_check_executed_upstream": plan_sm.get("provider_dependency_check_executed_now"),
        "environment_check_executed_upstream": plan_sm.get("environment_readiness_check_executed_now"),
        "ocr_controlled_provider_dryrun_closed": post_sm.get("ocr_controlled_provider_dryrun_closed"),
        "review_pass": len(blockers) == 0,
        "blockers": blockers,
        **meta,
    }

    selection_candidates = [
        {
            **_candidate_defaults(),
            "candidate_type": "provider_selection_candidate",
            "provider_candidate_id": p["provider_candidate_id"],
            "provider_family": p["provider_family"],
            "provider_status": "planned_candidate",
            "invocation_allowed": False,
            "authorization_required": True,
            "dependency_check_required": True,
            "environment_check_required": True,
            "controlled_trial_required": True,
            "health_binding_required": True,
            "constitution_gate_required": True,
            **meta,
        }
        for p in PROVIDER_INVENTORY
    ]

    selection_candidate = {
        "artifact_id": "provider_selection_candidate_v1",
        "candidates": selection_candidates,
        "candidate_count": len(selection_candidates),
        "selected_provider_for_execution": None,
        "provider_selection_finalized_now": False,
        "provider_authorization_started_now": False,
        **meta,
    }

    dependency_rows = [_dependency_row(p["provider_family"], meta) for p in PROVIDER_INVENTORY]
    dependency_matrix = {
        "matrix_id": "dependency_readiness_candidate_matrix_v1",
        "rows": dependency_rows,
        "row_count": len(dependency_rows),
        "all_checks_planned_not_executed": True,
        **meta,
    }

    environment_candidate = {
        "artifact_id": "environment_readiness_candidate_v1",
        "candidate_type": "environment_readiness_candidate",
        "python_version_requirement_planned": ">=3.10,<3.13",
        "virtualenv_isolation_required": True,
        "model_cache_directory_planned": "${LUNA_OCR_MODEL_CACHE:-./_tmp_eval_out/ocr_model_cache_candidate}",
        "writable_output_directory_planned": "${LUNA_OCR_OUTPUT_DIR:-./_tmp_eval_out/ocr_output_candidate}",
        "readonly_fixture_directory_planned_later": "${LUNA_OCR_FIXTURE_DIR:-./fixtures/ocr_readonly_later}",
        "cpu_memory_guard_planned": True,
        "timeout_guard_planned": True,
        "network_dependency_default": False,
        "sandbox_boundary_required": True,
        "production_path_write_allowed": False,
        "environment_readiness_check_executed_now": False,
        **_candidate_defaults(),
        **meta,
    }

    comparison_rows = []
    for p in PROVIDER_INVENTORY:
        fam = p["provider_family"]
        sample = _COMPARISON_SAMPLE.get(fam, {})
        comparison_rows.append(
            {
                "provider_family": fam,
                "dimensions": {dim: sample.get(dim, "sample_pending") for dim in SELECTION_CRITERIA},
                "sample_only": True,
                "final_selection": False,
            }
        )

    comparison_sample = {
        "matrix_id": "provider_comparison_matrix_sample_v1",
        "dimension_count": len(SELECTION_CRITERIA),
        "dimensions": list(SELECTION_CRITERIA),
        "rows": comparison_rows,
        "comparison_only_not_final_selection": True,
        **meta,
    }

    cost_latency_sample = {
        "sample_id": "provider_cost_latency_resource_sample_v1",
        "rows": [
            {"provider_family": "mock_or_fixture", "latency_class": "minimal", "cpu_pressure": "low", "memory_pressure": "low"},
            {"provider_family": "paddleocr_later", "latency_class": "high", "cpu_pressure": "high", "memory_pressure": "high"},
            {"provider_family": "rapidocr_later", "latency_class": "medium", "cpu_pressure": "medium", "memory_pressure": "medium"},
            {"provider_family": "external_ocr_later", "latency_class": "network_bound", "cpu_pressure": "low", "memory_pressure": "low"},
        ],
        "sample_only": True,
        **meta,
    }

    capability_fit_sample = {
        "sample_id": "provider_capability_fit_sample_v1",
        "fit_notes": [
            {"provider_family": "mock_or_fixture", "fit_class": "dryrun_fixture_baseline"},
            {"provider_family": "paddleocr_later", "fit_class": "pending_real_dependency_check"},
            {"provider_family": "rapidocr_later", "fit_class": "pending_real_dependency_check"},
            {"provider_family": "external_ocr_later", "fit_class": "pending_network_policy"},
        ],
        "sample_only": True,
        **meta,
    }

    health_rows = [
        {
            "trigger": hb["trigger"],
            "target_candidate": hb["target"],
            "routed": True,
            "executed_now": False,
            "fallback_executed_now": False,
            "retry_executed_now": False,
            "provider_switch_executed_now": False,
            **meta,
        }
        for hb in HEALTH_BINDINGS
    ]
    health_dryrun = {
        "result_id": "provider_health_binding_dryrun_result_v1",
        "bindings": health_rows,
        "all_routed_not_executed": True,
        **meta,
    }

    fallback_dryrun = {
        "result_id": "provider_fallback_strategy_dryrun_result_v1",
        "primary_provider_candidate": "paddleocr_later",
        "fallback_provider_candidate": "rapidocr_later",
        "fallback_chain": [
            "paddleocr_later",
            "rapidocr_later",
            "mock_or_fixture",
            "visual_candidate",
            "hold",
        ],
        "no_automatic_switch_execution": True,
        "fallback_executed_now": False,
        "retry_executed_now": False,
        "provider_switch_executed_now": False,
        **meta,
    }

    security_dryrun = {
        "result_id": "provider_security_boundary_dryrun_result_v1",
        "confirmations": {k: True for k in SECURITY_CONFIRMATIONS},
        "additional_confirmations": {
            "dependency_readiness_candidate_not_dependency_check_executed": True,
            "environment_readiness_candidate_not_runtime_enabled": True,
            "provider_comparison_not_provider_selected": True,
            "sample_ocr_plan_not_ocr_executed": True,
        },
        "boundary_pass": True,
        **meta,
    }

    no_import_audit = {
        "audit_id": "provider_no_import_no_install_audit_v1",
        "paddleocr_imported_now": False,
        "rapidocr_imported_now": False,
        "external_ocr_imported_now": False,
        "paddleocr_invoked_now": False,
        "rapidocr_invoked_now": False,
        "external_ocr_invoked_now": False,
        "dependency_install_executed_now": False,
        "model_download_executed_now": False,
        "provider_import_check_executed_now": False,
        "provider_smoke_check_executed_now": False,
        "sample_ocr_executed_now": False,
        "audit_pass": True,
        **meta,
    }

    blocked_paths = [
        {"path_id": path_id, "blocked": True, "reason": "dryrun_simulated_boundary"}
        for path_id in BLOCKED_PATHS
    ]
    blocked_result = {
        "result_id": "provider_selection_blocked_path_result_v1",
        "paths": blocked_paths,
        "path_count": len(blocked_paths),
        "all_blocked": True,
        **meta,
    }

    checks_pass = (
        len(blockers) == 0
        and input_review.get("review_pass")
        and selection_candidate.get("selected_provider_for_execution") is None
        and blocked_result.get("all_blocked")
        and no_import_audit.get("audit_pass")
        and security_dryrun.get("boundary_pass")
        and len(health_rows) == len(HEALTH_BINDINGS)
        and len(comparison_rows) == 4
    )

    readiness = {
        "decision_id": "provider_selection_dryrun_readiness_decision_v1",
        "selection_pass": checks_pass,
        "dependency_pass": checks_pass,
        "environment_pass": checks_pass,
        "comparison_pass": checks_pass,
        "health_pass": checks_pass,
        "fallback_pass": checks_pass,
        "boundary_pass": checks_pass,
        "all_pass": checks_pass,
        "high_risk_count": 0 if checks_pass else 1,
        "final_decision": FINAL_DECISION_GO if checks_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if checks_pass else NEXT_PHASE_HOLD,
        **meta,
    }

    policy = {
        "policy_id": "ocr_provider_selection_dependency_environment_dryrun_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "dryrun_goals": [
            "generate provider_selection_candidate",
            "generate dependency_readiness_candidate",
            "generate environment_readiness_candidate",
            "generate provider_comparison_matrix_sample",
            "verify no import / install / download / invoke",
        ],
        **meta,
    }

    non_claims = {
        "register_id": "non_claims_register_v1",
        "non_claims": list(NON_CLAIMS),
        **meta,
    }

    boundary_ok = checks_pass
    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": readiness["final_decision"],
        "recommended_next_phase": readiness["recommended_next_phase"],
        "high_risk_count": readiness["high_risk_count"],
        "ocr_provider_selection_dependency_environment_dryrun_closed": boundary_ok,
        "upstream_ocr_controlled_blocked_path_count": len(OCR_CONTROLLED_BLOCKED),
        **meta,
    }

    return {
        "ocr_provider_selection_dependency_environment_dryrun_policy": policy,
        "provider_selection_planning_input_review": input_review,
        "provider_selection_candidate": selection_candidate,
        "dependency_readiness_candidate_matrix": dependency_matrix,
        "environment_readiness_candidate": environment_candidate,
        "provider_comparison_matrix_sample": comparison_sample,
        "provider_cost_latency_resource_sample": cost_latency_sample,
        "provider_capability_fit_sample": capability_fit_sample,
        "provider_health_binding_dryrun_result": health_dryrun,
        "provider_fallback_strategy_dryrun_result": fallback_dryrun,
        "provider_security_boundary_dryrun_result": security_dryrun,
        "provider_no_import_no_install_audit": no_import_audit,
        "provider_selection_blocked_path_result": blocked_result,
        "provider_selection_dryrun_readiness_decision": readiness,
        "non_claims_register": non_claims,
        "summary": summary,
    }
