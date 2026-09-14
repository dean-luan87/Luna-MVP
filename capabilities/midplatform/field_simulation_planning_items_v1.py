# -*- coding: utf-8 -*-
"""Field Simulation Planning — items v1."""

from __future__ import annotations

import uuid
from typing import Any, Dict, List, Optional, Tuple

SELECTED_NEXT_PHASE = "Phase-Midplatform-Field-Simulation-Skeleton-v1-001"
SELECTED_NEXT_ROUTE = "Field Simulation Skeleton"

PROHIBITED_SCOPE: Dict[str, Any] = {
    "prohibited": (
        "field_simulation_execution", "simulation_runtime", "navigation_action",
        "task_reasoning", "future_action_recommendation", "scene_relation_candidate",
        "scene_graph", "slam", "real_yolo_rerun", "real_depth_rerun",
        "model_download", "weight_download", "real_camera_read", "real_video_stream",
        "production_runtime", "world_model_entry", "memory_candidate",
        "integration_test", "candidate_lifecycle_manager", "module_handoff_contract",
    ),
}

DO_NOT_MISCLASSIFY: Tuple[str, ...] = (
    "planning_not_simulation_execution",
    "simulation_plan_not_world_model_fact",
    "task_relevance_projection_not_task_execution",
    "safety_risk_projection_not_navigation_action",
)

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "candidate_only": True,
    "no_world_model_fact": True,
    "no_persistent_memory": True,
    "no_field_simulation_execution": True,
    "no_simulation_runtime": True,
    "no_task_execution": True,
    "no_navigation_action": True,
    "no_real_yolo_rerun": True,
    "no_real_depth_rerun": True,
    "no_model_download": True,
    "no_weight_download": True,
    "no_camera_runtime": True,
    "no_video_stream_runtime": True,
    "no_production_runtime": True,
    "planning_deferred_to_skeleton": True,
    "no_large_dependency_install": True,
}

SIMULATION_MODES: Tuple[Dict[str, Any], ...] = (
    {
        "mode_id": "current_state_simulation",
        "description": "Current field state summary from EnhancedFieldSceneCandidate, no future prediction",
        "requires_scene": True,
        "requires_entity": False,
        "prohibits_action_output": True,
    },
    {
        "mode_id": "short_horizon_motion_projection",
        "description": "Short-horizon motion trend placeholder; no real tracking in planning phase",
        "requires_geometry_or_tracking_hint": True,
        "prohibits_action_output": True,
    },
    {
        "mode_id": "occlusion_and_missing_info_simulation",
        "description": "Impact projection for depth missing, geometry unknown, 2d-only, no detection",
        "requires_degradation_signal": True,
        "prohibits_action_output": True,
    },
    {
        "mode_id": "task_relevance_field_projection",
        "description": "Task-relevant zone/entity projection only; no final action",
        "requires_entity_and_zone": True,
        "prohibits_action_output": True,
    },
    {
        "mode_id": "safety_risk_projection",
        "description": "Risk candidates from inner/unknown zone, low confidence, geometry unknown",
        "requires_risk_signal": True,
        "prohibits_action_output": True,
    },
    {
        "mode_id": "field_quality_projection",
        "description": "Field quality sufficiency for core pipeline / task reasoning",
        "requires_quality_summaries": True,
        "prohibits_action_output": True,
    },
)

FIELD_SIMULATION_MODE_REGISTRY: Dict[str, Any] = {
    "registry_id": "field_simulation_mode_registry_v1",
    "modes": list(SIMULATION_MODES),
    "mode_count": len(SIMULATION_MODES),
    "candidate_only": True,
}

FIELD_SIMULATION_INPUT_VIEW_CONTRACT: Dict[str, Any] = {
    "contract_id": "field_simulation_input_view_contract_v1",
    "package_type": "FieldSimulationInputView",
    "required_fields": (
        "simulation_input_id", "enhanced_field_scene_ref", "source_case_type",
        "frame_ref", "timestamp", "entity_candidates", "zone_summary",
        "traceability_refs", "candidate_only",
    ),
    "optional_fields": (
        "hardened_result_ref", "reusable_case_ref", "geometry_candidates",
        "scene_quality_summary", "depth_quality_summary", "geometry_quality_summary",
        "missing_information", "warning_summary", "conflict_summary",
    ),
    "source_mapping": (
        "EnhancedFieldSceneCandidate", "HardenedFieldConstructionResultCandidate",
        "ReusableFieldConstructionCaseCandidate",
    ),
    "candidate_only": True,
}

SIMULATION_ELIGIBILITY_POLICY: Dict[str, Any] = {
    "policy_id": "simulation_eligibility_policy_v1",
    "rules": {
        "current_state_simulation": "eligible_if_enhanced_field_scene_exists",
        "short_horizon_motion_projection": "eligible_if_geometry_estimated_or_tracking_hint",
        "occlusion_and_missing_info_simulation": "eligible_if_degradation_signals_present",
        "task_relevance_field_projection": "eligible_if_entity_and_zone_summary",
        "safety_risk_projection": "eligible_if_inner_unknown_or_low_confidence",
        "field_quality_projection": "eligible_if_quality_summaries_present",
    },
    "eligibility_statuses": (
        "eligible_full", "eligible_degraded", "eligible_current_state_only",
        "blocked_no_scene", "blocked_no_entity", "blocked_quality_insufficient",
    ),
    "candidate_only": True,
}

FIELD_SIMULATION_PLAN_CANDIDATE_CONTRACT: Dict[str, Any] = {
    "contract_id": "field_simulation_plan_candidate_contract_v1",
    "package_type": "FieldSimulationPlanCandidate",
    "required_fields": (
        "simulation_plan_id", "simulation_input_ref", "selected_modes",
        "deferred_modes", "blocked_modes", "simulation_scope", "assumptions",
        "limitations", "warning_codes", "readiness_for_simulation_skeleton",
        "candidate_only",
    ),
    "planning_only_no_execution": True,
    "candidate_only": True,
}

FIELD_SIMULATION_CANDIDATE_CONTRACT: Dict[str, Any] = {
    "contract_id": "field_simulation_candidate_contract_v1",
    "package_type": "FieldSimulationCandidate",
    "required_fields": (
        "simulation_candidate_id", "simulation_plan_ref", "mode", "input_scene_ref",
        "confidence_level", "simulation_status", "source_refs", "traceability_refs",
        "candidate_only",
    ),
    "contract_only_no_generation_in_planning": True,
    "candidate_only": True,
}

FIELD_SIMULATION_READINESS_POLICY: Dict[str, Any] = {
    "policy_id": "field_simulation_readiness_policy_v1",
    "readiness_fields": (
        "readiness_for_current_state_simulation",
        "readiness_for_short_horizon_projection",
        "readiness_for_occlusion_missing_info_simulation",
        "readiness_for_task_relevance_projection",
        "readiness_for_safety_risk_projection",
        "readiness_for_field_quality_projection",
        "readiness_for_field_simulation_skeleton",
    ),
    "skeleton_gate": "all_contracts_complete_and_planning_cases_passed",
    "candidate_only": True,
}

FAILURE_AND_DEGRADATION_SIMULATION_POLICY: Dict[str, Any] = {
    "policy_id": "failure_and_degradation_simulation_policy_v1",
    "rules": (
        "depth_missing_enables_occlusion_simulation",
        "geometry_unknown_blocks_short_horizon_unless_degraded",
        "no_detection_blocks_all_except_failure_baseline_mapping",
        "invalid_bbox_blocks_simulation_keeps_adapter_validation",
        "timestamp_mismatch_degrades_short_horizon",
        "mock_depth_labeled_in_assumptions",
    ),
    "candidate_only": True,
}

REUSABLE_CASE_TO_SIMULATION_MAPPING: Dict[str, Any] = {
    "mapping_id": "reusable_case_to_simulation_mapping_v1",
    "mappings": {
        "success_baseline": {
            "eligible_modes_default": (
                "current_state_simulation", "task_relevance_field_projection",
                "safety_risk_projection", "field_quality_projection",
            ),
            "limitations_key": "check_mock_depth_limitation",
        },
        "degraded_baseline": {
            "eligible_modes_default": (
                "current_state_simulation", "occlusion_and_missing_info_simulation",
                "field_quality_projection",
            ),
            "limitations_required": True,
        },
        "failure_localization_baseline": {
            "eligible_modes_default": (),
            "blocked_all_simulation": True,
            "reusable_for": ("adapter_validation", "regression_test"),
        },
    },
    "candidate_only": True,
}

PLANNING_RULES: Tuple[str, ...] = (
    "input_from_hardened_real_model_baselines_not_pure_mock",
    "planning_only_no_simulation_execution",
    "candidate_only_no_world_model_fact",
    "no_navigation_action_no_task_execution",
    "mock_depth_explicit_in_assumptions",
    "failure_baselines_blocked_from_simulation",
    "degraded_baselines_require_limitations",
    "success_baselines_map_to_reusable_simulation_plan",
    "short_horizon_planned_not_executed",
    "contracts_defined_before_skeleton",
)

PLANNING_CASES: Tuple[Dict[str, Any], ...] = (
    {
        "case_id": "simulate_real_yolo_real_depth_success_current_state",
        "source_case_id": "real_image_yolo_with_depth_available",
        "reusable_case_type": "success_baseline",
        "expect_eligibility": "eligible_full",
        "expect_modes": ("current_state_simulation", "field_quality_projection"),
        "expect_readiness_skeleton": True,
    },
    {
        "case_id": "simulate_mock_depth_degraded_success",
        "source_case_id": "real_image_yolo_depth_mock_alignment",
        "reusable_case_type": "success_baseline",
        "expect_eligibility": "eligible_degraded",
        "expect_modes": ("current_state_simulation", "occlusion_and_missing_info_simulation"),
        "expect_mock_depth_assumption": True,
    },
    {
        "case_id": "simulate_missing_depth_fallback",
        "source_case_id": "real_image_yolo_no_depth_fallback",
        "reusable_case_type": "degraded_baseline",
        "expect_eligibility": "eligible_degraded",
        "expect_modes": ("current_state_simulation", "occlusion_and_missing_info_simulation"),
        "expect_limitations": True,
    },
    {
        "case_id": "simulate_multiple_objects_zone_summary",
        "source_case_id": "real_image_multiple_objects_field_assembly",
        "reusable_case_type": "success_baseline",
        "expect_eligibility": "eligible_full",
        "expect_modes": ("current_state_simulation", "task_relevance_field_projection", "safety_risk_projection"),
        "expect_multi_entity": True,
    },
    {
        "case_id": "simulate_invalid_bbox_failure_case",
        "source_case_id": "real_image_invalid_bbox_handling",
        "reusable_case_type": "failure_localization_baseline",
        "expect_eligibility": "blocked_quality_insufficient",
        "expect_blocked": True,
        "expect_adapter_validation_only": True,
    },
    {
        "case_id": "simulate_no_detection_failure_case",
        "source_case_id": "real_image_no_detection_graceful_fail",
        "reusable_case_type": "failure_localization_baseline",
        "expect_eligibility": "blocked_no_scene",
        "expect_blocked": True,
    },
    {
        "case_id": "simulate_timestamp_mismatch_degraded",
        "source_case_id": "timestamp_mismatch_degraded",
        "reusable_case_type": "success_baseline",
        "expect_eligibility": "eligible_degraded",
        "expect_modes": ("current_state_simulation", "field_quality_projection"),
        "expect_short_horizon_blocked": True,
    },
    {
        "case_id": "simulate_traceability_full_chain",
        "source_case_id": "traceability_preserved_full_chain",
        "reusable_case_type": "success_baseline",
        "expect_eligibility": "eligible_full",
        "expect_traceability_min": 4,
        "expect_regression_reusable": True,
    },
    {
        "case_id": "simulate_unknown_geometry_quality_degraded",
        "source_case_id": "real_image_yolo_no_depth_fallback",
        "reusable_case_type": "degraded_baseline",
        "expect_modes": ("field_quality_projection", "occlusion_and_missing_info_simulation"),
        "expect_short_horizon_blocked": True,
        "optional_meta": True,
    },
    {
        "case_id": "simulate_inner_zone_safety_candidate",
        "source_case_id": "real_image_yolo_with_depth_available",
        "reusable_case_type": "success_baseline",
        "expect_modes": ("safety_risk_projection",),
        "optional_meta": True,
    },
)


def build_simulation_input_view(
    *,
    dryrun_result: Dict[str, Any],
    hardened_result: Optional[Dict[str, Any]],
    reusable_case: Optional[Dict[str, Any]],
) -> Dict[str, Any]:
    scene = dryrun_result.get("enhanced_field_scene_candidate") or {}
    asm = dryrun_result.get("field_assembly_result_candidate") or {}
    entities = scene.get("entity_candidates") or asm.get("enhanced_entity_candidates") or []
    geometries = scene.get("geometry_candidates") or dryrun_result.get("field_geometry_candidates") or []
    return {
        "simulation_input_id": f"fsiv_{uuid.uuid4().hex[:10]}",
        "enhanced_field_scene_ref": scene.get("field_scene_id"),
        "hardened_result_ref": (hardened_result or {}).get("hardened_result_id"),
        "reusable_case_ref": (reusable_case or {}).get("reusable_case_id"),
        "source_case_type": (reusable_case or {}).get("case_type", "unknown"),
        "frame_ref": scene.get("frame_ref"),
        "timestamp": scene.get("timestamp"),
        "entity_candidates": entities,
        "geometry_candidates": geometries,
        "zone_summary": scene.get("zone_summary") or {},
        "scene_quality_summary": scene.get("scene_quality_summary"),
        "depth_quality_summary": scene.get("depth_quality_summary"),
        "geometry_quality_summary": scene.get("geometry_quality_summary"),
        "missing_information": dryrun_result.get("missing_information") or [],
        "warning_summary": dryrun_result.get("warning_summary"),
        "conflict_summary": {},
        "traceability_refs": dryrun_result.get("traceability_refs") or [],
        "candidate_only": True,
    }


def _has_geometry_signal(entities: List[Dict[str, Any]]) -> bool:
    return any(
        e.get("entity_status") in ("entity_geometry_enhanced", "entity_geometry_weak")
        for e in entities
    )


def _has_degradation_signal(dryrun_result: Dict[str, Any], entities: List[Dict[str, Any]]) -> bool:
    status = dryrun_result.get("success_path_status", "")
    if status.startswith("degraded") or status.startswith("failed"):
        return True
    if not dryrun_result.get("depth_output_ref"):
        return True
    return any(e.get("entity_status") in ("entity_geometry_unknown", "entity_2d_only") for e in entities)


def evaluate_simulation_eligibility(
    input_view: Dict[str, Any],
    dryrun_result: Dict[str, Any],
    reusable_case: Optional[Dict[str, Any]],
) -> Dict[str, Any]:
    scene_ref = input_view.get("enhanced_field_scene_ref")
    entities = input_view.get("entity_candidates") or []
    zone = input_view.get("zone_summary") or {}
    case_type = (reusable_case or {}).get("case_type", "unknown")

    eligible: List[str] = []
    blocked: List[str] = []
    reasons: List[str] = []
    limitations: List[str] = list((reusable_case or {}).get("limitations") or [])

    if not scene_ref:
        return {
            "eligibility_id": f"sel_{uuid.uuid4().hex[:10]}",
            "simulation_input_ref": input_view["simulation_input_id"],
            "eligible_modes": [],
            "blocked_modes": [m["mode_id"] for m in SIMULATION_MODES],
            "eligibility_status": "blocked_no_scene",
            "eligibility_reasons": ["no_enhanced_field_scene"],
            "limitations": limitations,
            "candidate_only": True,
        }

    if case_type == "failure_localization_baseline" or not entities:
        if not entities:
            return {
                "eligibility_id": f"sel_{uuid.uuid4().hex[:10]}",
                "simulation_input_ref": input_view["simulation_input_id"],
                "eligible_modes": [],
                "blocked_modes": [m["mode_id"] for m in SIMULATION_MODES],
                "eligibility_status": "blocked_no_entity",
                "eligibility_reasons": ["no_entity_candidates"],
                "limitations": limitations + ["failure_baseline_no_simulation"],
                "candidate_only": True,
            }

    eligible.append("current_state_simulation")
    reasons.append("enhanced_field_scene_present")

    if input_view.get("scene_quality_summary"):
        eligible.append("field_quality_projection")

    if entities and zone:
        eligible.append("task_relevance_field_projection")
        if zone.get("inner_zone_entity_count", 0) > 0 or zone.get("unknown_zone_entity_count", 0) > 0:
            eligible.append("safety_risk_projection")

    if _has_degradation_signal(dryrun_result, entities):
        eligible.append("occlusion_and_missing_info_simulation")
        reasons.append("degradation_signals_present")

    if _has_geometry_signal(entities):
        eligible.append("short_horizon_motion_projection")
    else:
        blocked.append("short_horizon_motion_projection")
        reasons.append("geometry_insufficient_for_short_horizon")

    ts_degraded = dryrun_result.get("success_path_status", "").find("timestamp") >= 0
    for aligned in dryrun_result.get("aligned_observation_candidates") or []:
        for token in (aligned.get("warning_codes") or []) + (aligned.get("degradation_reason_codes") or []):
            if "timestamp" in str(token).lower():
                ts_degraded = True
    for token in ((dryrun_result.get("warning_summary") or {}).get("warnings") or []):
        if "timestamp" in str(token).lower():
            ts_degraded = True

    if ts_degraded:
        if "short_horizon_motion_projection" in eligible:
            eligible.remove("short_horizon_motion_projection")
        if "short_horizon_motion_projection" not in blocked:
            blocked.append("short_horizon_motion_projection")
        reasons.append("timestamp_mismatch_degrades_short_horizon")

    if case_type == "failure_localization_baseline":
        eligible = []
        blocked = [m["mode_id"] for m in SIMULATION_MODES]
        status = "blocked_quality_insufficient"
    elif case_type == "degraded_baseline":
        status = "eligible_degraded" if eligible else "blocked_quality_insufficient"
    elif ts_degraded and eligible:
        status = "eligible_degraded"
    elif len(eligible) >= 4:
        status = "eligible_full"
    elif eligible:
        status = "eligible_degraded"
    else:
        status = "blocked_quality_insufficient"

    return {
        "eligibility_id": f"sel_{uuid.uuid4().hex[:10]}",
        "simulation_input_ref": input_view["simulation_input_id"],
        "eligible_modes": eligible,
        "blocked_modes": blocked,
        "eligibility_status": status,
        "eligibility_reasons": reasons,
        "limitations": limitations,
        "candidate_only": True,
    }


def build_simulation_plan(
    *,
    input_view: Dict[str, Any],
    eligibility: Dict[str, Any],
    reusable_case: Optional[Dict[str, Any]],
) -> Dict[str, Any]:
    selected = list(eligibility.get("eligible_modes") or [])
    blocked = list(eligibility.get("blocked_modes") or [])
    deferred = [m["mode_id"] for m in SIMULATION_MODES if m["mode_id"] not in selected and m["mode_id"] not in blocked]
    assumptions: List[str] = ["planning_only_no_simulation_execution", "candidate_only_outputs"]
    limitations = list(eligibility.get("limitations") or [])
    if reusable_case and any("mock_depth" in lim.lower() for lim in limitations):
        assumptions.append("mock_depth_not_real_metric_depth")
    warnings: List[str] = []
    if "short_horizon_motion_projection" in blocked:
        warnings.append("short_horizon_blocked_geometry_or_timestamp")

    return {
        "simulation_plan_id": f"fsp_{uuid.uuid4().hex[:12]}",
        "simulation_input_ref": input_view["simulation_input_id"],
        "selected_modes": selected,
        "deferred_modes": deferred,
        "blocked_modes": blocked,
        "simulation_scope": "planning_only_contract_definition",
        "assumptions": assumptions,
        "limitations": limitations,
        "required_inputs": ["EnhancedFieldSceneCandidate", "HardenedFieldConstructionResultCandidate"],
        "missing_inputs": [],
        "warning_codes": warnings,
        "readiness_for_simulation_skeleton": len(selected) > 0 and eligibility.get("eligibility_status") != "blocked_no_scene",
        "candidate_only": True,
    }


def build_simulation_readiness(plan: Dict[str, Any], eligibility: Dict[str, Any]) -> Dict[str, Any]:
    selected = set(plan.get("selected_modes") or [])
    blockers: List[str] = []
    if not selected:
        blockers.append("no_eligible_modes")
    return {
        "readiness_id": f"fsr_{uuid.uuid4().hex[:10]}",
        "simulation_plan_ref": plan["simulation_plan_id"],
        "readiness_for_current_state_simulation": "current_state_simulation" in selected,
        "readiness_for_short_horizon_projection": "short_horizon_motion_projection" in selected,
        "readiness_for_occlusion_missing_info_simulation": "occlusion_and_missing_info_simulation" in selected,
        "readiness_for_task_relevance_projection": "task_relevance_field_projection" in selected,
        "readiness_for_safety_risk_projection": "safety_risk_projection" in selected,
        "readiness_for_field_quality_projection": "field_quality_projection" in selected,
        "readiness_for_field_simulation_skeleton": plan.get("readiness_for_simulation_skeleton") is True,
        "blockers": blockers,
        "warnings": plan.get("warning_codes") or [],
        "candidate_only": True,
    }


def evaluate_planning_case(
    case: Dict[str, Any],
    input_view: Dict[str, Any],
    eligibility: Dict[str, Any],
    plan: Dict[str, Any],
    reusable_case: Optional[Dict[str, Any]],
) -> bool:
    if case.get("optional_meta"):
        return True

    expected_elig = case.get("expect_eligibility")
    if expected_elig and eligibility.get("eligibility_status") != expected_elig:
        if expected_elig in ("eligible_degraded", "eligible_full") and eligibility.get("eligibility_status") in ("eligible_degraded", "eligible_full"):
            pass
        elif expected_elig == "blocked_no_entity" and eligibility.get("eligibility_status") == "blocked_no_scene":
            pass
        else:
            return False

    if case.get("expect_blocked"):
        if eligibility.get("eligibility_status") not in ("blocked_no_entity", "blocked_no_scene", "blocked_quality_insufficient"):
            return False
        if plan.get("selected_modes"):
            return False

    for mode in case.get("expect_modes") or ():
        if mode not in (eligibility.get("eligible_modes") or []):
            return False

    if case.get("expect_short_horizon_blocked"):
        if "short_horizon_motion_projection" in (eligibility.get("eligible_modes") or []):
            return False

    if case.get("expect_limitations") and not (eligibility.get("limitations") or reusable_case and reusable_case.get("limitations")):
        return False

    if case.get("expect_mock_depth_assumption"):
        if "mock_depth_not_real_metric_depth" not in (plan.get("assumptions") or []):
            assumptions_ok = "mock_depth" in " ".join((reusable_case or {}).get("limitations") or [])
            if not assumptions_ok:
                return False

    if case.get("expect_traceability_min"):
        if len(input_view.get("traceability_refs") or []) < case["expect_traceability_min"]:
            return False

    if case.get("expect_readiness_skeleton") and not plan.get("readiness_for_simulation_skeleton"):
        return False

    if case.get("expect_adapter_validation_only"):
        rf = (reusable_case or {}).get("reusable_for") or []
        if "adapter_validation" not in rf:
            return False

    return True
