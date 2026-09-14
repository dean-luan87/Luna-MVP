# -*- coding: utf-8 -*-
"""OCR Provider Selection / Dependency / Environment Planning v1 — planning-only."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.ocr_controlled_provider_authorization_roadmap_decision_v1 import (
    BLOCKED_ROUTE_C,
    DEFERRED_ROUTE_A,
    FINAL_DECISION_GO as ROADMAP_FINAL_GO,
    NEXT_PHASE_GO as ROADMAP_NEXT_PHASE,
    SELECTED_ROUTE,
)
from capabilities.governance.ocr_controlled_provider_dryrun_v1 import BLOCKED_PATHS

PHASE_ID = "Phase-OCR-Provider-Selection-Dependency-Environment-Planning-v1-001"
SCOPE = "ocr_provider_selection_dependency_environment_planning_only"
SOURCE_CHAIN = "ocr_provider_selection_dependency_environment_planning_v1"

UPSTREAM_ROADMAP_FINAL = ROADMAP_FINAL_GO
UPSTREAM_ROADMAP_NEXT = ROADMAP_NEXT_PHASE

FINAL_DECISION_GO = "OCR_PROVIDER_SELECTION_DEPENDENCY_ENVIRONMENT_PLANNING_READY_FOR_DRYRUN"
FINAL_DECISION_HOLD = "OCR_PROVIDER_SELECTION_DEPENDENCY_ENVIRONMENT_PLANNING_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-OCR-Provider-Selection-Dependency-Environment-DryRun-v1-001"
NEXT_PHASE_HOLD = "Phase-OCR-Provider-Selection-Issue-Review-v1-001"

SELECTION_CRITERIA: Tuple[str, ...] = (
    "local_availability",
    "dependency_complexity",
    "model_file_readiness",
    "runtime_isolation",
    "cpu_memory_pressure",
    "latency_expectation",
    "chinese_text_support",
    "small_text_support",
    "rotated_text_support",
    "multi_region_ocr_support",
    "confidence_output_support",
    "layout_bbox_output_support",
    "failure_timeout_handling",
    "candidate_output_compatibility",
    "evidence_pack_compatibility",
    "offline_readiness",
    "license_usage_constraint",
)

DEPENDENCY_CHECKS_PLANNED: Tuple[str, ...] = (
    "python_package_existence_check_planned",
    "model_cache_path_check_planned",
    "model_file_hash_check_planned",
    "provider_import_check_planned",
    "runtime_smoke_check_planned",
    "sample_ocr_check_planned_later",
)

HEALTH_BINDINGS: Tuple[Dict[str, str], ...] = (
    {"trigger": "provider_import_failed", "target": "dependency_issue_candidate"},
    {"trigger": "model_file_missing", "target": "model_cache_issue_candidate"},
    {"trigger": "provider_timeout", "target": "hold_candidate"},
    {"trigger": "provider_runtime_error", "target": "fallback_candidate"},
    {"trigger": "low_confidence", "target": "reobserve_or_retry_candidate"},
    {"trigger": "unsupported_layout", "target": "fallback_to_visual_candidate"},
)

PROVIDER_INVENTORY: Tuple[Dict[str, Any], ...] = (
    {
        "provider_candidate_id": "ocr_provider_mock_fixture",
        "provider_family": "mock_or_fixture",
        "provider_status": "planned_candidate",
        "invocation_allowed": False,
        "install_required": False,
        "model_files_required": False,
        "local_runtime_required": False,
        "network_required": False,
        "expected_output_contract": "ocr_result_candidate",
        "evidence_pack_required": True,
        "health_binding_required": True,
        "constitution_gate_required": True,
    },
    {
        "provider_candidate_id": "ocr_provider_paddleocr_later",
        "provider_family": "paddleocr_later",
        "provider_status": "planned_candidate",
        "invocation_allowed": False,
        "install_required": True,
        "model_files_required": True,
        "local_runtime_required": True,
        "network_required": False,
        "expected_output_contract": "ocr_result_candidate",
        "evidence_pack_required": True,
        "health_binding_required": True,
        "constitution_gate_required": True,
    },
    {
        "provider_candidate_id": "ocr_provider_rapidocr_later",
        "provider_family": "rapidocr_later",
        "provider_status": "planned_candidate",
        "invocation_allowed": False,
        "install_required": True,
        "model_files_required": True,
        "local_runtime_required": True,
        "network_required": False,
        "expected_output_contract": "ocr_result_candidate",
        "evidence_pack_required": True,
        "health_binding_required": True,
        "constitution_gate_required": True,
    },
    {
        "provider_candidate_id": "ocr_provider_external_ocr_later",
        "provider_family": "external_ocr_later",
        "provider_status": "planned_candidate",
        "invocation_allowed": False,
        "install_required": True,
        "model_files_required": False,
        "local_runtime_required": False,
        "network_required": True,
        "expected_output_contract": "ocr_result_candidate",
        "evidence_pack_required": True,
        "health_binding_required": True,
        "constitution_gate_required": True,
    },
)

SECURITY_CONFIRMATIONS: Tuple[str, ...] = (
    "provider_candidate_not_provider_authorization",
    "dependency_plan_not_dependency_install",
    "model_cache_plan_not_model_download",
    "import_check_plan_not_provider_import_executed",
    "environment_readiness_plan_not_runtime_enabled",
    "provider_comparison_not_provider_selected_for_execution",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Planning GO ≠ provider selected for execution",
    "Planning GO ≠ PaddleOCR/RapidOCR/external OCR invoked",
    "dependency readiness plan ≠ dependency check executed",
    "model cache plan ≠ model downloaded",
    "import check plan ≠ provider import executed",
    "environment readiness plan ≠ runtime enabled",
    "provider comparison matrix ≠ primary provider finalized",
    "DryRun next ≠ real dependency install or OCR execution",
    "selection criteria defined ≠ PaddleOCR chosen over RapidOCR",
    "Route B planning ≠ provider authorization",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "provider_selection_finalized_now",
    "provider_dependency_check_executed_now",
    "environment_readiness_check_executed_now",
    "dependency_install_executed_now",
    "model_download_executed_now",
    "provider_authorization_started_now",
    "controlled_trial_started_now",
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
    "dependency_check_executed_now",
    "import_check_executed_now",
    "provider_invoked_now",
    "sample_ocr_executed_now",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_provider_selection_dependency_environment_planning"
)


def _planning_meta() -> Dict[str, Any]:
    meta = {
        "ocr_provider_selection_dependency_environment_planning_only": True,
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


def _dependency_plan_base(provider_family: str) -> Dict[str, Any]:
    return {
        "planning_only": True,
        "provider_family": provider_family,
        "checks_planned": list(DEPENDENCY_CHECKS_PLANNED),
        "dependency_check_executed_now": False,
        "import_check_executed_now": False,
        "provider_invoked_now": False,
        "sample_ocr_executed_now": False,
        "dependency_install_executed_now": False,
        "model_download_executed_now": False,
    }


def run_ocr_provider_selection_dependency_environment_planning_v1(
    *,
    ocr_controlled_provider_authorization_roadmap_decision_root: str,
    ocr_controlled_provider_post_dryrun_review_root: Optional[str] = None,
    ocr_controlled_provider_dryrun_root: Optional[str] = None,
    model_registry_canonicalization_post_dryrun_review_root: Optional[str] = None,
    health_management_layer_integration_post_dryrun_review_root: Optional[str] = None,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    roadmap_root = Path(ocr_controlled_provider_authorization_roadmap_decision_root).expanduser().resolve()
    roadmap_sm = _try_read_json(roadmap_root / "summary.json") or {}
    roadmap_vr = _try_read_json(roadmap_root / "verifier_report.json") or {}
    matrix = _try_read_json(roadmap_root / "ocr_authorization_route_selection_matrix_v1.json") or {}

    post_root = Path(
        ocr_controlled_provider_post_dryrun_review_root
        or roadmap_sm.get("upstream_post_dryrun_review_root")
        or roadmap_root.parent / "ocr_controlled_provider_post_dryrun_review"
    ).expanduser().resolve()
    dryrun_root = Path(
        ocr_controlled_provider_dryrun_root
        or roadmap_sm.get("upstream_dryrun_root")
        or roadmap_root.parent / "ocr_controlled_provider_dryrun"
    ).expanduser().resolve()
    canonical_root = Path(
        model_registry_canonicalization_post_dryrun_review_root
        or roadmap_root.parent / "model_registry_canonicalization_post_dryrun_review"
    ).expanduser().resolve()
    health_post_root = Path(
        health_management_layer_integration_post_dryrun_review_root
        or roadmap_root.parent / "health_management_layer_integration_post_dryrun_review"
    ).expanduser().resolve()

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_planning_meta(),
        "upstream_roadmap_decision_root": str(roadmap_root),
        "upstream_post_dryrun_review_root": str(post_root),
        "upstream_dryrun_root": str(dryrun_root),
        "output_root": str(out_root),
    }

    post_sm = _try_read_json(post_root / "summary.json") or {}
    post_vr = _try_read_json(post_root / "verifier_report.json") or {}
    dryrun_sm = _try_read_json(dryrun_root / "summary.json") or {}
    dryrun_vr = _try_read_json(dryrun_root / "verifier_report.json") or {}
    readiness = _try_read_json(dryrun_root / "ocr_provider_readiness_candidate_samples_v1.json") or {}
    blocked = _try_read_json(dryrun_root / "ocr_blocked_path_result_v1.json") or {}
    canonical_sm = _try_read_json(canonical_root / "summary.json") or {}
    health_sm = _try_read_json(health_post_root / "summary.json") or {}

    roadmap_go = roadmap_vr.get("verifier") == "GO" and roadmap_vr.get("passed") is True
    if not roadmap_go:
        blockers.append("authorization roadmap decision verifier must be GO")
    if roadmap_sm.get("final_decision") != UPSTREAM_ROADMAP_FINAL:
        blockers.append("roadmap final_decision mismatch")
    if roadmap_sm.get("recommended_next_phase") != UPSTREAM_ROADMAP_NEXT:
        blockers.append("roadmap recommended_next_phase mismatch")
    if roadmap_sm.get("selected_route") != SELECTED_ROUTE:
        blockers.append("selected_route must be Route B")
    if matrix.get("selected_route") != SELECTED_ROUTE:
        blockers.append("route matrix selected_route mismatch")

    if post_sm.get("ocr_candidate_chain_trusted") is not True:
        blockers.append("ocr_candidate_chain_trusted required")
    if post_vr.get("verifier") != "GO":
        blockers.append("post-dryrun review should be GO")
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
        "external_ocr_invoked_now",
        "real_ocr_provider_invoked_now",
        "provider_authorization_started_now",
        "controlled_trial_started_now",
    ):
        if roadmap_sm.get(field) is True or dryrun_sm.get(field) is True or post_sm.get(field) is True:
            blockers.append(f"{field} must be false upstream")

    if canonical_sm.get("b_lite_canonical_v0_baseline_closed") is not True:
        blockers.append("model_registry_canonical_v0 must be closed")
    if health_sm.get("health_management_integration_dryrun_closed") is not True:
        blockers.append("health management must be closed")

    input_review = {
        "review_id": "authorization_roadmap_input_review_v1",
        "upstream_roadmap_root": str(roadmap_root),
        "upstream_post_review_root": str(post_root),
        "upstream_dryrun_root": str(dryrun_root),
        "roadmap_verifier_go": roadmap_go,
        "roadmap_final_decision": roadmap_sm.get("final_decision"),
        "selected_route": roadmap_sm.get("selected_route"),
        "deferred_route_a": roadmap_sm.get("deferred_route_a") or DEFERRED_ROUTE_A,
        "blocked_route_c": roadmap_sm.get("blocked_route_c") or BLOCKED_ROUTE_C,
        "ocr_candidate_chain_trusted": post_sm.get("ocr_candidate_chain_trusted"),
        "readiness_count": readiness.get("sample_count"),
        "blocked_paths_count": len(blocked.get("paths") or []),
        "review_pass": len(blockers) == 0,
        "blockers": blockers,
        **meta,
    }

    policy = {
        "policy_id": "ocr_provider_selection_dependency_environment_planning_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "goals": [
            "define provider selection criteria",
            "plan local dependency checks without execution",
            "plan environment and model cache readiness",
            "plan capability / cost / latency / health / fallback",
            "no provider invocation in planning",
        ],
        **meta,
    }

    inventory = {
        "inventory_id": "ocr_provider_candidate_inventory_v1",
        "candidates": list(PROVIDER_INVENTORY),
        "candidate_count": len(PROVIDER_INVENTORY),
        "required_families": [
            "mock_or_fixture",
            "paddleocr_later",
            "rapidocr_later",
            "external_ocr_later",
        ],
        "all_invocation_allowed_false": True,
        **meta,
    }

    selection_criteria = {
        "criteria_id": "ocr_provider_selection_criteria_v1",
        "dimensions": list(SELECTION_CRITERIA),
        "dimension_count": len(SELECTION_CRITERIA),
        "selection_finalized_now": False,
        "note": "criteria define evaluation rules — not a provider pick for execution",
        **meta,
    }

    paddle_dep = {
        "plan_id": "paddleocr_dependency_readiness_plan_v1",
        **_dependency_plan_base("paddleocr_later"),
        "python_packages_planned": ["paddlepaddle", "paddleocr"],
        "model_cache_paths_planned": ["~/.paddleocr/", "vendor/paddleocr_models/"],
        **meta,
    }
    rapid_dep = {
        "plan_id": "rapidocr_dependency_readiness_plan_v1",
        **_dependency_plan_base("rapidocr_later"),
        "python_packages_planned": ["rapidocr-onnxruntime", "onnxruntime"],
        "model_cache_paths_planned": ["~/.rapidocr/", "vendor/rapidocr_models/"],
        **meta,
    }
    external_dep = {
        "plan_id": "external_ocr_dependency_readiness_plan_v1",
        **_dependency_plan_base("external_ocr_later"),
        "python_packages_planned": ["httpx", "external_ocr_client_stub"],
        "network_endpoint_check_planned": True,
        **meta,
    }

    local_env = {
        "plan_id": "local_environment_readiness_plan_v1",
        "python_version_requirement": ">=3.10,<3.13",
        "virtualenv_isolation_required": True,
        "model_cache_directory": "${LUNA_OCR_MODEL_CACHE:-./_tmp_eval_out/ocr_model_cache_candidate}",
        "writable_output_directory": "${LUNA_OCR_OUTPUT_DIR:-./_tmp_eval_out/ocr_output_candidate}",
        "readonly_input_fixture_directory_later": "${LUNA_OCR_FIXTURE_DIR:-./fixtures/ocr_readonly_later}",
        "cpu_memory_guard": {"max_memory_mb_candidate": 2048, "max_cpu_percent_candidate": 80},
        "timeout_guard_seconds_candidate": 30,
        "no_network_dependency_by_default": True,
        "sandbox_boundary": "evaluation_governance_only",
        "no_production_path_write": True,
        "environment_readiness_check_executed_now": False,
        **meta,
    }

    model_cache = {
        "plan_id": "model_file_and_cache_readiness_plan_v1",
        "checks_planned": [
            "model_cache_path_exists_planned",
            "model_file_presence_planned",
            "model_file_hash_planned",
            "writable_cache_dir_planned",
        ],
        "model_download_executed_now": False,
        "per_family": {
            "paddleocr_later": {"model_files_required": True},
            "rapidocr_later": {"model_files_required": True},
            "external_ocr_later": {"model_files_required": False},
            "mock_or_fixture": {"model_files_required": False},
        },
        **meta,
    }

    capability_matrix = {
        "matrix_id": "provider_capability_comparison_matrix_v1",
        "comparison_only": True,
        "rows": [
            {
                "provider_family": "mock_or_fixture",
                "chinese_text": "fixture_only",
                "small_text": "fixture_only",
                "rotated_text": "limited",
                "multi_region": True,
                "confidence_output": True,
                "layout_bbox": True,
            },
            {
                "provider_family": "paddleocr_later",
                "chinese_text": "planned_strong",
                "small_text": "planned_medium",
                "rotated_text": "planned_medium",
                "multi_region": True,
                "confidence_output": True,
                "layout_bbox": True,
            },
            {
                "provider_family": "rapidocr_later",
                "chinese_text": "planned_medium",
                "small_text": "planned_medium",
                "rotated_text": "planned_low",
                "multi_region": True,
                "confidence_output": True,
                "layout_bbox": True,
            },
            {
                "provider_family": "external_ocr_later",
                "chinese_text": "vendor_dependent",
                "small_text": "vendor_dependent",
                "rotated_text": "vendor_dependent",
                "multi_region": True,
                "confidence_output": "vendor_dependent",
                "layout_bbox": "vendor_dependent",
            },
        ],
        **meta,
    }

    cost_latency = {
        "matrix_id": "provider_cost_latency_resource_matrix_v1",
        "comparison_only": True,
        "rows": [
            {"provider_family": "mock_or_fixture", "latency_class": "minimal", "cpu_pressure": "low", "memory_pressure": "low"},
            {"provider_family": "paddleocr_later", "latency_class": "high", "cpu_pressure": "high", "memory_pressure": "high"},
            {"provider_family": "rapidocr_later", "latency_class": "medium", "cpu_pressure": "medium", "memory_pressure": "medium"},
            {"provider_family": "external_ocr_later", "latency_class": "network_bound", "cpu_pressure": "low", "memory_pressure": "low"},
        ],
        **meta,
    }

    health_binding = {
        "plan_id": "provider_health_binding_plan_v1",
        "bindings": list(HEALTH_BINDINGS),
        "health_signal_candidate_only": True,
        "fallback_executed_now": False,
        **meta,
    }

    fallback_strategy = {
        "plan_id": "provider_fallback_strategy_plan_v1",
        "primary_provider_candidate": "paddleocr_later",
        "fallback_provider_candidate": "rapidocr_later",
        "fallback_chain": [
            "paddleocr_later",
            "rapidocr_later",
            "mock_or_fixture",
            "visual_candidate",
            "hold",
        ],
        "fallback_to_mock_or_fixture": True,
        "fallback_to_visual_candidate": True,
        "fallback_to_hold": True,
        "no_automatic_switch_execution": True,
        "provider_switch_executed_now": False,
        **meta,
    }

    security_boundary = {
        "plan_id": "provider_security_and_boundary_plan_v1",
        "confirmations": {k: True for k in SECURITY_CONFIRMATIONS},
        "confirmation_keys": list(SECURITY_CONFIRMATIONS),
        **meta,
    }

    dryrun_plan = {
        "plan_id": "provider_selection_dryrun_plan_v1",
        "next_phase": NEXT_PHASE_GO,
        "dryrun_goals": [
            "generate provider selection candidate",
            "generate dependency readiness candidate",
            "generate environment readiness candidate",
            "generate provider comparison matrix sample",
            "no import provider",
            "no install dependency",
            "no download model",
            "no execute OCR",
        ],
        **meta,
    }

    non_claims = {
        "register_id": "ocr_provider_selection_non_claims_register_v1",
        "non_claims": list(NON_CLAIMS),
        **meta,
    }

    planning_ok = len(blockers) == 0 and input_review.get("review_pass") is True
    boundary_ok = planning_ok

    planning_decision = {
        "decision_id": "ocr_provider_selection_planning_decision_v1",
        "planning_pass": planning_ok,
        "ready_for_dryrun": boundary_ok,
        "final_decision": FINAL_DECISION_GO if boundary_ok else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if boundary_ok else NEXT_PHASE_HOLD,
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": planning_decision["final_decision"],
        "recommended_next_phase": planning_decision["recommended_next_phase"],
        "high_risk_count": 0 if boundary_ok else 1,
        **meta,
    }

    return {
        "ocr_provider_selection_dependency_environment_planning_policy": policy,
        "authorization_roadmap_input_review": input_review,
        "ocr_provider_candidate_inventory": inventory,
        "ocr_provider_selection_criteria": selection_criteria,
        "paddleocr_dependency_readiness_plan": paddle_dep,
        "rapidocr_dependency_readiness_plan": rapid_dep,
        "external_ocr_dependency_readiness_plan": external_dep,
        "local_environment_readiness_plan": local_env,
        "model_file_and_cache_readiness_plan": model_cache,
        "provider_capability_comparison_matrix": capability_matrix,
        "provider_cost_latency_resource_matrix": cost_latency,
        "provider_health_binding_plan": health_binding,
        "provider_fallback_strategy_plan": fallback_strategy,
        "provider_security_and_boundary_plan": security_boundary,
        "provider_selection_dryrun_plan": dryrun_plan,
        "ocr_provider_selection_non_claims_register": non_claims,
        "ocr_provider_selection_planning_decision": planning_decision,
        "summary": summary,
    }
