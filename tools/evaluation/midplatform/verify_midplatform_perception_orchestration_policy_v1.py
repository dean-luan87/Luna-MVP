#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify MidPlatform Perception Orchestration Policy v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Dict, List

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


DEFAULT_WORKSPACE_ROOT = Path("/Users/luanlei/Desktop/Luna-Workspace-Min")
DEFAULT_OUTPUT_ROOT = DEFAULT_WORKSPACE_ROOT / "_eval_out" / "midplatform_perception_orchestration_policy_v1_smoke_v0"
PHASE_ID = "Phase-MidPlatform-Perception-Orchestration-Policy-v1-001"
FINAL_DECISION = "MIDPLATFORM_PERCEPTION_ORCHESTRATION_POLICY_READY_FOR_TASK_AWARE_VISUAL_FOCUS_POLICY"
NEXT_PHASE = "Phase-Task-Aware-Visual-Focus-Policy-v1-001"
MIN_CHECKS = 140
BASELINE_REQUIREMENT = 100


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verify MidPlatform Perception Orchestration Policy v1")
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_root = Path(args.output_root)
    checks: List[Dict[str, Any]] = []

    def expect(check_id: str, passed: bool, detail: Any = None) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})

    summary = _load_json(output_root / "summary.json")
    input_root_matrix = _load_json(output_root / "input_root_matrix.json")
    work_order = _load_json(output_root / "perception_work_order_schema.json")
    task_phase_matrix = _load_json(output_root / "task_phase_perception_policy_matrix.json")
    safety_lane = _load_json(output_root / "safety_lane_orchestration_policy.json")
    task_lane = _load_json(output_root / "task_lane_orchestration_policy.json")
    budget = _load_json(output_root / "midplatform_resource_budget_policy.json")
    privacy = _load_json(output_root / "midplatform_privacy_filtering_policy.json")
    conflict = _load_json(output_root / "perception_conflict_correction_policy.json")
    map_memory = _load_json(output_root / "map_memory_context_hint_policy.json")
    wml_boundary = _load_json(output_root / "worldmodel_memory_library_handoff_boundary.json")
    feedback = _load_json(output_root / "perception_feedback_candidate_policy.json")
    orchestration_boundary = _load_json(output_root / "orchestration_boundary_matrix.json")
    governance_debt = _load_json(output_root / "governance_debt_register.json")
    next_phase = _load_json(output_root / "next_phase_recommendation.json")
    no_runtime = _load_json(output_root / "no_runtime_boundary_report.json")
    no_write = _load_json(output_root / "no_write_boundary_report.json")

    # Input checks
    expect("input.return_to_vision_planning_input_loaded", summary.get("return_to_vision_planning_input_loaded") is True)
    expect("input.preplan_input_loaded", summary.get("preplan_input_loaded") is True)
    expect("input.ocr_final_closure_loaded", summary.get("ocr_final_closure_loaded") is True)
    expect("input.minimal_runtime_integration_closure_loaded", summary.get("minimal_runtime_integration_closure_loaded") is True)
    expect("input.root_matrix_rows_present", isinstance(input_root_matrix.get("rows"), list))
    expect("input.root_matrix_row_count_match", input_root_matrix.get("row_count") == len(input_root_matrix.get("rows", [])))
    for intake_id in (
        "return_to_vision_planning",
        "preplan_input",
        "ocr_final_closure",
        "minimal_runtime_integration_closure",
        "vision_planning_doc",
        "vision_preplan_doc",
        "ocr_final_closure_doc",
        "minimal_runtime_integration_closure_doc",
        "ocr_phase_verdict_table",
    ):
        expect(
            f"input.required.{intake_id}",
            any(row.get("intake_id") == intake_id and row.get("loaded") is True for row in input_root_matrix.get("rows", [])),
        )

    # Summary / policy checks
    expect("summary.policy_scope", summary.get("policy_scope") == "midplatform_perception_orchestration_policy_only")
    expect("summary.perception_work_order_schema_defined", summary.get("perception_work_order_schema_defined") is True)
    expect("summary.task_phase_perception_policy_defined", summary.get("task_phase_perception_policy_defined") is True)
    expect("summary.safety_lane_orchestration_defined", summary.get("safety_lane_orchestration_defined") is True)
    expect("summary.task_lane_orchestration_defined", summary.get("task_lane_orchestration_defined") is True)
    expect("summary.midplatform_resource_budget_policy_defined", summary.get("midplatform_resource_budget_policy_defined") is True)
    expect("summary.midplatform_privacy_filtering_policy_defined", summary.get("midplatform_privacy_filtering_policy_defined") is True)
    expect("summary.perception_conflict_correction_policy_defined", summary.get("perception_conflict_correction_policy_defined") is True)
    expect("summary.map_memory_context_hint_policy_defined", summary.get("map_memory_context_hint_policy_defined") is True)
    expect("summary.worldmodel_memory_library_handoff_boundary_defined", summary.get("worldmodel_memory_library_handoff_boundary_defined") is True)
    expect("summary.perception_feedback_candidate_policy_defined", summary.get("perception_feedback_candidate_policy_defined") is True)
    expect("summary.governance_debt_register_generated", summary.get("governance_debt_register_generated") is True)

    # Principles
    expect("principles.resource_budget_owned_by_midplatform", summary.get("resource_budget_owned_by_midplatform") is True)
    expect("principles.privacy_filtering_owned_by_midplatform", summary.get("privacy_filtering_owned_by_midplatform") is True)
    expect("principles.safety_lane_always_on", summary.get("safety_lane_always_on") is True)
    expect("principles.task_lane_task_dependent", summary.get("task_lane_task_dependent") is True)
    expect("principles.full_scene_tracking_allowed", summary.get("full_scene_tracking_allowed") is False)
    expect("principles.full_frame_ocr_allowed", summary.get("full_frame_ocr_allowed") is False)
    expect("principles.map_memory_context_hint_only", summary.get("map_memory_context_hint_only") is True)

    # Work order schema checks
    work_order_fields = [item.get("name") for item in work_order.get("fields", [])]
    expect("work_order.object_name", work_order.get("object_name") == "MidPlatformPerceptionWorkOrder")
    expect("work_order.field_count", work_order.get("field_count") == len(work_order.get("fields", [])))
    for field_name in (
        "work_order_id",
        "related_task_id",
        "task_type",
        "task_phase",
        "priority",
        "perception_time_window",
        "safety_lane_required",
        "task_lane_required",
        "scene_context_ref",
        "map_context_ref",
        "route_context_ref",
        "location_context_ref",
        "memory_context_ref",
        "system_health_ref",
        "hardware_state_ref",
        "focus_request_targets",
        "ocr_activation_request",
        "tracking_request",
        "map_memory_hint_request",
        "world_observation_handoff_allowed",
        "privacy_filtering_required",
        "resource_budget_ref",
        "freshness_policy_ref",
        "stc_policy_ref",
        "conflict_policy_ref",
        "output_handoff_policy_ref",
        "runtime_action_allowed",
        "task_commit_allowed",
        "fact_write_allowed",
        "worldmodel_write_allowed",
        "memory_write_allowed",
        "library_write_allowed",
        "source_chain",
    ):
        expect(f"work_order.field.{field_name}", field_name in work_order_fields)
    expect("work_order.runtime_action_allowed", work_order.get("runtime_action_allowed") is False)
    expect("work_order.task_commit_allowed", work_order.get("task_commit_allowed") is False)
    expect("work_order.fact_write_allowed", work_order.get("fact_write_allowed") is False)
    expect("work_order.worldmodel_write_allowed", work_order.get("worldmodel_write_allowed") is False)
    expect("work_order.memory_write_allowed", work_order.get("memory_write_allowed") is False)
    expect("work_order.library_write_allowed", work_order.get("library_write_allowed") is False)
    expect("work_order.non_claims_count", len(work_order.get("non_claims", [])) >= 3, len(work_order.get("non_claims", [])))
    expect("work_order.allowed_downstream_consumers_count", len(work_order.get("allowed_downstream_consumers", [])) >= 4)
    expect("work_order.forbidden_direct_triggers_count", len(work_order.get("forbidden_direct_triggers", [])) >= 5)

    # Task phase matrix checks
    matrix_rows = task_phase_matrix.get("rows", [])
    matrix_task_types = task_phase_matrix.get("task_types", [])
    expect("task_phase_matrix.phase_count", task_phase_matrix.get("phase_count") == len(matrix_rows))
    expect("task_phase_matrix.count_ge_20", len(matrix_rows) >= 20, len(matrix_rows))
    for task_type in (
        "navigation",
        "shop_search",
        "object_search",
        "reading_task",
        "queue_or_crowd_observation",
        "target_confirmation",
        "user_visual_feedback_response",
    ):
        expect(f"task_phase_matrix.task_type.{task_type}", task_type in matrix_task_types)
    for phase_name in (
        "ROUTE_START",
        "ROUTE_WALKING",
        "APPROACHING_CROSSING",
        "CROSSING_DECISION",
        "APPROACHING_TARGET",
        "TARGET_SEARCH",
        "TARGET_CONFIRMATION",
        "ARRIVED_CANDIDATE",
        "SAFETY_HOLD",
        "SEARCH_AREA_APPROACHING",
        "SHOPFRONT_SCAN",
        "SIGNAGE_CONFIRMATION",
        "ENTRANCE_CONFIRMATION",
        "TARGET_FOUND_CANDIDATE",
        "SEARCH_CONTEXT_IDENTIFICATION",
        "LIKELY_SURFACE_SCAN",
        "OBJECT_CANDIDATE_CONFIRMATION",
        "OBJECT_LOCATION_GUIDANCE",
    ):
        expect(
            f"task_phase_matrix.phase.{phase_name}",
            any(row.get("task_phase") == phase_name for row in matrix_rows),
        )
    for idx, row in enumerate(matrix_rows):
        expect(f"task_phase_matrix.required_focus_targets_nonempty_{idx}", len(row.get("required_focus_targets", [])) >= 1)
        expect(f"task_phase_matrix.optional_focus_targets_present_{idx}", isinstance(row.get("optional_focus_targets"), list))
        expect(f"task_phase_matrix.safety_lane_policy_present_{idx}", isinstance(row.get("safety_lane_policy"), str) and bool(row.get("safety_lane_policy")))
        expect(f"task_phase_matrix.task_lane_policy_present_{idx}", isinstance(row.get("task_lane_policy"), str) and bool(row.get("task_lane_policy")))
        expect(f"task_phase_matrix.ocr_activation_policy_present_{idx}", isinstance(row.get("ocr_activation_policy"), str) and bool(row.get("ocr_activation_policy")))
        expect(f"task_phase_matrix.tracking_policy_present_{idx}", isinstance(row.get("tracking_policy"), str) and bool(row.get("tracking_policy")))
        expect(f"task_phase_matrix.map_memory_hint_policy_present_{idx}", isinstance(row.get("map_memory_hint_policy"), str) and bool(row.get("map_memory_hint_policy")))
        expect(f"task_phase_matrix.output_policy_present_{idx}", isinstance(row.get("output_policy"), str) and bool(row.get("output_policy")))
        expect(f"task_phase_matrix.handoff_boundary_present_{idx}", row.get("handoff_boundary") == "handoff_only_no_fact_write_no_runtime")
        expect(f"task_phase_matrix.forbidden_runtime_actions_present_{idx}", len(row.get("forbidden_runtime_actions", [])) >= 10)
        expect(f"task_phase_matrix.runtime_action_allowed_{idx}", row.get("runtime_action_allowed") is False)
        expect(f"task_phase_matrix.task_commit_allowed_{idx}", row.get("task_commit_allowed") is False)
        expect(f"task_phase_matrix.fact_write_allowed_{idx}", row.get("fact_write_allowed") is False)
        expect(f"task_phase_matrix.worldmodel_write_allowed_{idx}", row.get("worldmodel_write_allowed") is False)
        expect(f"task_phase_matrix.memory_write_allowed_{idx}", row.get("memory_write_allowed") is False)
        expect(f"task_phase_matrix.library_write_allowed_{idx}", row.get("library_write_allowed") is False)

    # Safety lane checks
    expect("safety_lane.always_on", safety_lane.get("always_on") is True)
    expect("safety_lane.task_disable_allowed", safety_lane.get("task_disable_allowed") is False)
    expect("safety_lane.output_candidate", safety_lane.get("output_candidates") == ["SafetyObservationCandidate"])
    expect("safety_lane.must_enter_arbitration", safety_lane.get("must_enter_safety_task_arbitration") is True)
    expect("safety_lane.can_preempt_task_lane_budget", safety_lane.get("can_preempt_task_lane_budget") is True)
    expect("safety_lane.can_request_view_quality_candidate", safety_lane.get("can_request_view_quality_candidate") is True)
    expect("safety_lane.can_request_active_adjustment_candidate", safety_lane.get("can_request_active_adjustment_candidate") is True)
    expect("safety_lane.fact_write_allowed", safety_lane.get("fact_write_allowed") is False)
    expect("safety_lane.runtime_action_allowed", safety_lane.get("runtime_action_allowed") is False)
    for target in (
        "near_field_obstacle",
        "moving_vehicle",
        "pedestrian_approach",
        "bike_or_e_scooter",
        "traffic_light",
        "crosswalk",
        "curb_or_step",
        "pothole_or_ground_risk",
        "walkable_path_interruption",
        "sudden_dynamic_risk",
    ):
        expect(f"safety_lane.target.{target}", target in safety_lane.get("coverage_targets", []))

    # Task lane checks
    expect("task_lane.task_dependent", task_lane.get("task_dependent") is True)
    expect("task_lane.approved_focus_targets_only", task_lane.get("approved_focus_targets_only") is True)
    expect("task_lane.resource_budget_controlled", task_lane.get("resource_budget_controlled") is True)
    expect("task_lane.full_scene_tracking_allowed", task_lane.get("full_scene_tracking_allowed") is False)
    expect("task_lane.full_frame_ocr_allowed", task_lane.get("full_frame_ocr_allowed") is False)
    expect("task_lane.safety_lane_bypass_allowed", task_lane.get("safety_lane_bypass_allowed") is False)
    expect("task_lane.must_enter_arbitration_or_speech_prechain", task_lane.get("must_enter_arbitration_or_speech_prechain") is True)
    expect("task_lane.runtime_action_allowed", task_lane.get("runtime_action_allowed") is False)
    expect("task_lane.fact_write_allowed", task_lane.get("fact_write_allowed") is False)
    for category in (
        "navigation",
        "shop_search",
        "object_search",
        "reading_task",
        "queue_or_crowd_observation",
        "target_confirmation",
        "user_visual_feedback_response",
    ):
        expect(f"task_lane.category.{category}", category in task_lane.get("supported_task_categories", []))

    # Resource budget checks
    expect("budget.owned_by_midplatform", budget.get("resource_budget_owned_by_midplatform") is True)
    expect("budget.hardware_state_ref_required", budget.get("hardware_state_ref_required") is True)
    expect("budget.system_health_ref_required", budget.get("system_health_ref_required") is True)
    expect("budget.task_priority_ref_required", budget.get("task_priority_ref_required") is True)
    expect("budget.safety_reserved_budget", budget.get("safety_reserved_budget") == "always_reserved")
    expect("budget.background_world_observation_budget", budget.get("background_world_observation_budget") == "low_frequency_only")
    expect("budget.ocr_budget", budget.get("ocr_budget") == "focus_triggered_only")
    expect("budget.tracking_budget", budget.get("tracking_budget") == "selective_tracking_only")
    expect("budget.map_memory_query_budget", budget.get("map_memory_query_budget") == "hint_query_only")
    expect("budget.max_active_focus_slots", budget.get("max_active_focus_slots") >= 1)
    expect("budget.max_active_tracklets", budget.get("max_active_tracklets") >= 1)
    expect("budget.max_ocr_requests_per_window", budget.get("max_ocr_requests_per_window") >= 1)
    expect("budget.max_background_observation_items", budget.get("max_background_observation_items") >= 1)
    expect("budget.degradation_policy", budget.get("degradation_policy") == "safety_first_then_primary_task_only")
    expect("budget.preemption_policy", budget.get("preemption_policy") == "safety_lane_may_preempt_task_lane")
    expect("budget.vision_module_may_expand_budget", budget.get("vision_module_may_expand_budget") is False)

    # Privacy checks
    expect("privacy.owned_by_midplatform", privacy.get("privacy_filtering_owned_by_midplatform") is True)
    expect("privacy.candidate_stage_count", len(privacy.get("candidate_stages", [])) >= 4)
    for stage in (
        "Raw Observation Candidate",
        "Privacy-Filtered Candidate",
        "Restricted Use Candidate",
        "Long-Term Eligible Candidate",
    ):
        expect(f"privacy.stage.{stage}", stage in privacy.get("candidate_stages", []))
    for tag in (
        "human_identity_sensitive",
        "face_visible",
        "license_plate_visible",
        "private_space_candidate",
        "medical_context_candidate",
        "school_or_child_context_candidate",
        "home_context_candidate",
        "workplace_context_candidate",
        "commercial_sensitive_candidate",
        "personal_item_candidate",
        "bystander_presence_candidate",
    ):
        expect(f"privacy.tag.{tag}", tag in privacy.get("privacy_tags", []))

    # Conflict correction checks
    for source in (
        "visual_vs_ocr",
        "visual_vs_map",
        "visual_vs_memory",
        "visual_vs_user_feedback",
        "ocr_vs_actual_function",
        "signboard_vs_business_function",
        "map_poi_vs_current_scene",
        "historical_observation_vs_current_observation",
        "temporary_facility_vs_static_poi",
        "fresh_vs_stale_conflict",
    ):
        expect(f"conflict.source.{source}", source in conflict.get("conflict_sources", []))
    for output_name in (
        "PerceptionConflictCandidate",
        "PerceptionCorrectionCandidate",
        "RealityMismatchCandidate",
        "WorldModelCorrectionHandoffCandidate",
    ):
        expect(f"conflict.output.{output_name}", output_name in conflict.get("output_candidates", []))

    # Map/memory checks
    expect("map_memory.hint_only", map_memory.get("map_memory_context_hint_only") is True)
    expect("map_memory.realtime_safety_visual_priority", map_memory.get("realtime_safety_visual_priority") is True)
    for allowed in (
        "目标接近 hint",
        "路线阶段 hint",
        "方向 / 左右侧 / 入口 / 路口 / POI hint",
        "历史混淆点",
        "过去观察候选",
        "下次观察优先级",
    ):
        expect(f"map_memory.allowed.{allowed}", allowed in map_memory.get("allowed_uses", []))
    for forbidden in (
        "直接触发行动",
        "直接播报为事实",
        "覆盖实时安全视觉",
        "直接写 WorldModel / Memory / Fact",
        "直接触发 OCR / tracking runtime",
        "直接判定到达",
    ):
        expect(f"map_memory.forbidden.{forbidden}", forbidden in map_memory.get("forbidden_uses", []))

    # WML boundary checks
    expect("wml_boundary.entity_resolution_deferred", wml_boundary.get("entity_resolution_deferred") is True)
    expect("wml_boundary.fact_admission_deferred", wml_boundary.get("fact_admission_deferred") is True)
    expect("wml_boundary.memory_consolidation_deferred", wml_boundary.get("memory_consolidation_deferred") is True)
    expect("wml_boundary.library_experience_governance_deferred", wml_boundary.get("library_experience_governance_deferred") is True)
    expect("wml_boundary.worldmodel_write_allowed", wml_boundary.get("worldmodel_write_allowed") is False)
    expect("wml_boundary.memory_write_allowed", wml_boundary.get("memory_write_allowed") is False)
    expect("wml_boundary.library_write_allowed", wml_boundary.get("library_write_allowed") is False)
    expect("wml_boundary.handoff_candidate_not_fact", wml_boundary.get("handoff_candidate_not_fact") is True)
    expect("wml_boundary.placeholder_not_runtime", wml_boundary.get("placeholder_not_runtime") is True)
    for allowed in (
        "WorldModelHandoffCandidate",
        "MemoryHandoffCandidate",
        "LibraryHandoffPlaceholder",
        "ExperienceCandidatePlaceholder",
    ):
        expect(f"wml_boundary.allowed.{allowed}", allowed in wml_boundary.get("allowed_now", []))
    for forbidden in (
        "entity_resolution_runtime",
        "fact_admission",
        "worldmodel_write",
        "memory_write",
        "library_experience_commit",
        "memory_consolidation",
        "object_identity_fact_commit",
        "emotional_attachment_fact_commit",
        "temporary_facility_long_term_promotion",
        "route_experience_commit",
    ):
        expect(f"wml_boundary.forbidden.{forbidden}", forbidden in wml_boundary.get("forbidden_now", []))
    expect("wml_boundary.planning_boundary_loaded", wml_boundary.get("planning_boundary_loaded") is True)
    expect("wml_boundary.planning_placeholder_loaded", wml_boundary.get("planning_placeholder_loaded") is True)
    expect("wml_boundary.preplan_boundary_loaded", wml_boundary.get("preplan_boundary_loaded") is True)
    expect("wml_boundary.preplan_placeholder_loaded", wml_boundary.get("preplan_placeholder_loaded") is True)

    # Feedback policy checks
    expect("feedback.requires_arbitration", feedback.get("feedback_candidate_requires_arbitration") is True)
    expect("feedback.speech_allowed_false_until_gate", feedback.get("speech_allowed_false_until_gate") is True)
    expect("feedback.action_allowed_false", feedback.get("action_allowed_false") is True)
    expect("feedback.fact_status_not_fact", feedback.get("fact_status_not_fact") is True)
    for output_name in (
        "SafetyFeedbackCandidate",
        "TaskFeedbackCandidate",
        "ViewAdjustmentFeedbackCandidate",
        "OCRActivationFeedbackCandidate",
        "MapMemoryConflictFeedbackCandidate",
        "UserVisualFeedbackCandidate",
    ):
        expect(f"feedback.output.{output_name}", output_name in feedback.get("output_candidates", []))
    for field_name in (
        "feedback_id",
        "feedback_type",
        "related_task_id",
        "evidence_refs",
        "source_chain",
        "requires_arbitration",
        "speech_allowed",
        "action_allowed",
        "fact_status",
    ):
        expect(f"feedback.field.{field_name}", field_name in feedback.get("feedback_common_fields", []))

    # Orchestration boundary checks
    expect("boundary.camera_runtime_allowed", orchestration_boundary.get("camera_runtime_allowed") is False)
    expect("boundary.ocr_provider_runtime_allowed", orchestration_boundary.get("ocr_provider_runtime_allowed") is False)
    expect("boundary.tracking_runtime_allowed", orchestration_boundary.get("tracking_runtime_allowed") is False)
    expect("boundary.optical_flow_runtime_allowed", orchestration_boundary.get("optical_flow_runtime_allowed") is False)
    expect("boundary.map_api_allowed", orchestration_boundary.get("map_api_allowed") is False)
    expect("boundary.full_scene_tracking_allowed", orchestration_boundary.get("full_scene_tracking_allowed") is False)
    expect("boundary.full_frame_ocr_allowed", orchestration_boundary.get("full_frame_ocr_allowed") is False)
    expect("boundary.worldmodel_write_allowed", orchestration_boundary.get("worldmodel_write_allowed") is False)
    expect("boundary.memory_write_allowed", orchestration_boundary.get("memory_write_allowed") is False)
    expect("boundary.library_write_allowed", orchestration_boundary.get("library_write_allowed") is False)
    expect("boundary.fact_write_allowed", orchestration_boundary.get("fact_write_allowed") is False)
    expect("boundary.entity_resolution_runtime_allowed", orchestration_boundary.get("entity_resolution_runtime_allowed") is False)
    expect("boundary.fact_admission_allowed", orchestration_boundary.get("fact_admission_allowed") is False)
    expect("boundary.memory_consolidation_allowed", orchestration_boundary.get("memory_consolidation_allowed") is False)
    expect("boundary.library_experience_commit_allowed", orchestration_boundary.get("library_experience_commit_allowed") is False)
    expect("boundary.scene_delta_allowed", orchestration_boundary.get("scene_delta_allowed") is False)
    expect("boundary.task_commit_allowed", orchestration_boundary.get("task_commit_allowed") is False)
    expect("boundary.navigation_action_allowed", orchestration_boundary.get("navigation_action_allowed") is False)
    expect("boundary.map_memory_context_hint_only", orchestration_boundary.get("map_memory_context_hint_only") is True)

    # Governance debt checks
    debt_rows = governance_debt.get("debts", [])
    expect("governance_debt.count_ge_7", len(debt_rows) >= 7, len(debt_rows))
    expect(
        "governance_debt.future_midplatform_function_governance_required",
        governance_debt.get("future_midplatform_function_governance_required") is True,
    )
    expect(
        "governance_debt.no_duplicate_governance_module_allowed",
        governance_debt.get("no_duplicate_governance_module_allowed") is True,
    )
    for topic in (
        "resource budget complexity",
        "privacy filtering complexity",
        "conflict correction complexity",
        "temporary facility governance complexity",
        "world observation handoff complexity",
        "duplicated schema risk",
        "future midplatform function governance required",
    ):
        expect(
            f"governance_debt.topic.{topic}",
            any(row.get("topic") == topic for row in debt_rows),
        )
    for idx, row in enumerate(debt_rows):
        expect(f"governance_debt.future_owner_phase_{idx}", row.get("future_owner_phase") == "MidPlatform Function Governance / Consolidation")
        expect(f"governance_debt.reuse_or_consolidation_required_{idx}", row.get("reuse_or_consolidation_required") is True)
        expect(f"governance_debt.duplicate_governance_module_allowed_{idx}", row.get("duplicate_governance_module_allowed") is False)

    # Runtime/write checks
    expect("runtime.no_runtime_executed", summary.get("no_runtime_executed") is True)
    expect("runtime.no_new_runtime_enabled", summary.get("no_new_runtime_enabled") is True)
    expect("runtime.camera_invoked", summary.get("camera_invoked") is False)
    expect("runtime.map_api_invoked", summary.get("map_api_invoked") is False)
    expect("runtime.ocr_provider_invoked", summary.get("ocr_provider_invoked") is False)
    expect("runtime.tracking_runtime_invoked", summary.get("tracking_runtime_invoked") is False)
    expect("runtime.optical_flow_runtime_invoked", summary.get("optical_flow_runtime_invoked") is False)
    expect("runtime.world_model_written", summary.get("world_model_written") is False)
    expect("runtime.memory_written", summary.get("memory_written") is False)
    expect("runtime.library_written", summary.get("library_written") is False)
    expect("runtime.fact_written", summary.get("fact_written") is False)
    expect("runtime.scene_delta_generated", summary.get("scene_delta_generated") is False)
    expect("runtime.task_state_committed_now", summary.get("task_state_committed_now") is False)
    expect("runtime.navigation_action_triggered", summary.get("navigation_action_triggered") is False)
    expect("runtime.boundary_ok", summary.get("boundary_ok") is True)
    expect("runtime.violations_empty", summary.get("violations") == [])
    for payload_name, payload in (("no_runtime", no_runtime), ("no_write", no_write)):
        expect(f"{payload_name}.no_runtime_executed", payload.get("no_runtime_executed") is True)
        expect(f"{payload_name}.no_new_runtime_enabled", payload.get("no_new_runtime_enabled") is True)
        expect(f"{payload_name}.camera_invoked", payload.get("camera_invoked") is False)
        expect(f"{payload_name}.map_api_invoked", payload.get("map_api_invoked") is False)
        expect(f"{payload_name}.ocr_provider_invoked", payload.get("ocr_provider_invoked") is False)
        expect(f"{payload_name}.tracking_runtime_invoked", payload.get("tracking_runtime_invoked") is False)
        expect(f"{payload_name}.optical_flow_runtime_invoked", payload.get("optical_flow_runtime_invoked") is False)
        expect(f"{payload_name}.world_model_written", payload.get("world_model_written") is False)
        expect(f"{payload_name}.memory_written", payload.get("memory_written") is False)
        expect(f"{payload_name}.library_written", payload.get("library_written") is False)
        expect(f"{payload_name}.fact_written", payload.get("fact_written") is False)
        expect(f"{payload_name}.scene_delta_generated", payload.get("scene_delta_generated") is False)
        expect(f"{payload_name}.task_state_committed_now", payload.get("task_state_committed_now") is False)
        expect(f"{payload_name}.navigation_action_triggered", payload.get("navigation_action_triggered") is False)
        expect(f"{payload_name}.boundary_ok", payload.get("boundary_ok") is True)
        expect(f"{payload_name}.violations_empty", payload.get("violations") == [])

    # Readiness/final checks
    expect("final.final_decision", summary.get("final_decision") == FINAL_DECISION)
    expect("final.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)
    expect("next_phase.final_decision", next_phase.get("final_decision") == FINAL_DECISION)
    expect("next_phase.recommended_next_phase", next_phase.get("recommended_next_phase") == NEXT_PHASE)

    passed_count = sum(1 for item in checks if item["passed"])
    verdict = "GO" if passed_count >= MIN_CHECKS and not any(not item["passed"] for item in checks) else "NO_GO"
    report = {
        "phase": PHASE_ID,
        "verdict": verdict,
        "checks_passed": passed_count,
        "checks_total": len(checks),
        "min_checks_required": MIN_CHECKS,
        "baseline_requirement": BASELINE_REQUIREMENT,
        "final_decision": FINAL_DECISION if verdict == "GO" else "MIDPLATFORM_PERCEPTION_ORCHESTRATION_POLICY_REVIEW_REQUIRED",
        "recommended_next_phase": NEXT_PHASE if verdict == "GO" else PHASE_ID,
        "failed_checks": [item for item in checks if not item["passed"]],
        "checks": checks,
    }
    (output_root / "verifier_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"verdict": verdict, "checks_passed": passed_count, "checks_total": len(checks)}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
