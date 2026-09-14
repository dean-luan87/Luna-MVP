#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Map Location ReadOnly Context Policy v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

PHASE_ID = "Phase-Map-Location-ReadOnly-Context-Policy-v1-001"
FINAL_DECISION = "MAP_LOCATION_READONLY_CONTEXT_POLICY_READY_FOR_CONTROLLED_FRAME_INPUT_PLANNING"
NEXT_PHASE = "Phase-Controlled-Frame-Input-Planning-v1-001"
MIN_CHECKS = 180
BASELINE_REQUIREMENT = 140


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-root", default="/Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/map_location_readonly_context_policy_v1_smoke_v0")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    checks: List[Dict[str, Any]] = []

    def ok(check_id: str, passed: bool, detail: Any = None) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})

    summary = _load_json(root / "summary.json")
    input_root_matrix = _load_json(root / "input_root_matrix.json")
    map_location_readonly_context_policy = _load_json(root / "map_location_readonly_context_policy.json")
    map_location_context_candidate_schema = _load_json(root / "map_location_context_candidate_schema.json")
    route_stage_hint_candidate_schema = _load_json(root / "route_stage_hint_candidate_schema.json")
    target_proximity_hint_candidate_schema = _load_json(root / "target_proximity_hint_candidate_schema.json")
    side_orientation_hint_candidate_schema = _load_json(root / "side_orientation_hint_candidate_schema.json")
    entrance_intersection_hint_candidate_schema = _load_json(root / "entrance_intersection_hint_candidate_schema.json")
    map_visual_memory_conflict_policy = _load_json(root / "map_visual_memory_conflict_policy.json")
    map_location_to_visual_focus_binding_policy = _load_json(root / "map_location_to_visual_focus_binding_policy.json")
    map_location_to_ocr_activation_hint_policy = _load_json(root / "map_location_to_ocr_activation_hint_policy.json")
    map_location_feedback_policy = _load_json(root / "map_location_feedback_policy.json")
    map_location_readonly_context_scenario_matrix = _load_json(root / "map_location_readonly_context_scenario_matrix.json")
    map_location_boundary_matrix = _load_json(root / "map_location_boundary_matrix.json")
    governance_debt_register = _load_json(root / "governance_debt_register.json")
    next_phase_recommendation = _load_json(root / "next_phase_recommendation.json")
    no_runtime_boundary_report = _load_json(root / "no_runtime_boundary_report.json")
    no_write_boundary_report = _load_json(root / "no_write_boundary_report.json")

    rows = input_root_matrix.get("rows", [])
    idx = {row.get("intake_id"): row for row in rows}
    for intake_id in (
        "post_vision_strengthening_roadmap_decision",
        "vision_strengthening_closure",
        "post_dryrun_review",
        "dryrun",
        "visual_ocr_map_task_feedback",
        "selective_tracking",
        "world_observation_entity_feature",
        "task_aware_visual_focus",
        "midplatform_perception_orchestration",
        "minimal_runtime_integration_closure",
        "ocr_final_closure",
    ):
        ok(f"input.{intake_id}", idx.get(intake_id, {}).get("loaded") is True)
    for intake_id in (
        "map_anchor_context_output",
        "gps_route_context_output",
        "route_context_preplan",
        "basic_navigation_guidance_loop_output",
        "basic_navigation_loop_stabilization",
        "safety_task_arbitration_policy",
    ):
        ok(f"input.{intake_id}.optional", idx.get(intake_id, {}).get("status") in {"loaded", "optional_missing"}, idx.get(intake_id, {}).get("status"))

    for key in (
        "post_vision_strengthening_roadmap_decision_input_loaded",
        "vision_strengthening_closure_input_loaded",
        "visual_ocr_map_task_feedback_input_loaded",
        "task_aware_visual_focus_input_loaded",
        "midplatform_perception_orchestration_input_loaded",
        "minimal_runtime_integration_closure_loaded",
        "ocr_final_closure_loaded",
        "map_location_readonly_context_policy_defined",
        "map_location_context_candidate_schema_defined",
        "route_stage_hint_candidate_schema_defined",
        "target_proximity_hint_candidate_schema_defined",
        "side_orientation_hint_candidate_schema_defined",
        "entrance_intersection_hint_candidate_schema_defined",
        "map_visual_memory_conflict_policy_defined",
        "map_location_to_visual_focus_binding_policy_defined",
        "map_location_to_ocr_activation_hint_policy_defined",
        "map_location_feedback_policy_defined",
        "scenario_matrix_generated",
        "governance_debt_register_generated",
        "map_location_feedback_candidate_only",
        "map_visual_conflict_candidate_generated",
        "ocr_activation_from_map_requires_visual_focus",
        "tracking_request_from_map_requires_visual_focus",
        "no_runtime_executed",
        "no_new_runtime_enabled",
        "boundary_ok",
    ):
        ok(f"summary.{key}", summary.get(key) is True)
    ok("summary.scenario_count", summary.get("scenario_count", 0) >= 10, summary.get("scenario_count"))
    for key in (
        "map_context_role",
        "location_context_role",
        "route_context_role",
        "poi_context_role",
    ):
        ok(f"summary.{key}", summary.get(key) == "readonly_hint", summary.get(key))
    for key in (
        "map_is_fact_authority",
        "map_is_navigation_authority",
        "map_is_safety_authority",
        "map_can_trigger_action",
        "map_can_prove_arrival",
        "map_can_grant_crossing_permission",
        "map_can_write_worldmodel",
        "map_can_write_memory",
        "map_can_write_fact",
    ):
        ok(f"summary.{key}", summary.get(key) is False)
    for key in (
        "map_api_invoked",
        "gaode_api_invoked",
        "gps_runtime_invoked",
        "route_planning_runtime_invoked",
        "camera_invoked",
        "visual_model_invoked",
        "ocr_provider_invoked",
        "ocrrequest_submitted",
        "tracking_runtime_invoked",
        "optical_flow_runtime_invoked",
        "supervision_invoked",
        "bytetrack_invoked",
        "ocsort_invoked",
        "speech_gate_invoked",
        "vop_invoked",
        "tts_invoked",
        "task_state_committed_now",
        "navigation_action_triggered",
        "route_modified",
        "arrival_fact_written",
        "crossing_action_instruction_allowed",
        "scene_delta_generated",
        "world_model_written",
        "memory_written",
        "library_written",
        "fact_written",
        "entity_resolution_runtime_invoked",
        "fact_admission_runtime_invoked",
        "memory_consolidation_invoked",
        "library_experience_commit_invoked",
    ):
        ok(f"summary.{key}", summary.get(key) is False)
    ok("summary.violations", summary.get("violations") == [])
    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)

    ok("policy.policy_scope", map_location_readonly_context_policy.get("policy_scope") == "map_location_readonly_context_policy_only")
    for key in ("map_context_role", "location_context_role", "route_context_role", "poi_context_role"):
        ok(f"policy.{key}", map_location_readonly_context_policy.get(key) == "readonly_hint", map_location_readonly_context_policy.get(key))
    ok("policy.safety_arbitration_required", map_location_readonly_context_policy.get("safety_arbitration_required") is True)
    for expected in (
        "fact authority",
        "navigation authority",
        "safety authority",
        "action trigger",
        "arrival proof",
        "crossing permission",
        "WorldModel fact write",
        "Memory fact write",
        "direct OCR runtime invocation",
        "direct tracking runtime invocation",
        "direct Navigation Action",
        "direct Task State commit",
    ):
        ok(f"policy.forbidden.{expected}", expected in map_location_readonly_context_policy.get("forbidden_use_cases", []))

    ok("schema.map_location.name", map_location_context_candidate_schema.get("schema_name") == "MapLocationContextCandidate")
    ok("schema.map_location.source_types", len(map_location_context_candidate_schema.get("source_type_enum", [])) >= 8)
    for expected in (
        "map_location_context_id",
        "source_type",
        "source_provider_placeholder",
        "route_context_ref",
        "location_context_ref",
        "poi_context_ref",
        "target_context_ref",
        "route_stage_candidate",
        "distance_to_target_candidate",
        "side_hint_candidate",
        "entrance_hint_candidate",
        "intersection_hint_candidate",
        "crossing_hint_candidate",
        "floor_or_level_hint_candidate",
        "indoor_outdoor_hint_candidate",
        "confidence",
        "uncertainty",
        "freshness_status",
        "ttl_policy_ref",
        "provider_runtime_invoked",
        "fact_status",
        "action_allowed",
        "source_chain",
    ):
        ok(f"schema.map_location.field.{expected}", any(field.get("name") == expected for field in map_location_context_candidate_schema.get("field_specs", [])))

    ok("schema.route_stage.name", route_stage_hint_candidate_schema.get("schema_name") == "RouteStageHintCandidate")
    ok("schema.route_stage.enum_count", len(route_stage_hint_candidate_schema.get("route_stage_enum", [])) >= 11)
    for expected in (
        "route_not_started",
        "route_walking",
        "approaching_crossing",
        "crossing_area_candidate",
        "after_crossing_candidate",
        "approaching_destination",
        "target_search_area",
        "target_confirmation_area",
        "arrived_candidate",
        "off_route_candidate",
        "route_uncertain",
    ):
        ok(f"schema.route_stage.enum.{expected}", expected in route_stage_hint_candidate_schema.get("route_stage_enum", []))
    for expected in (
        "arrived_candidate 不等于已到达事实",
        "crossing_area_candidate 不等于允许过马路",
        "off_route_candidate 不等于真实偏航事实",
    ):
        ok(f"schema.route_stage.non_claim.{expected}", expected in route_stage_hint_candidate_schema.get("non_claims", []))

    ok("schema.target_proximity.name", target_proximity_hint_candidate_schema.get("schema_name") == "TargetProximityHintCandidate")
    for expected in ("far", "nearby", "approaching", "very_close", "uncertain"):
        ok(f"schema.target_proximity.bucket.{expected}", expected in target_proximity_hint_candidate_schema.get("distance_bucket_candidate_enum", []))

    ok("schema.side_orientation.name", side_orientation_hint_candidate_schema.get("schema_name") == "SideAndOrientationHintCandidate")
    for expected in ("left", "right", "front", "behind", "across_road", "same_side", "opposite_side", "unknown"):
        ok(f"schema.side_orientation.side.{expected}", expected in side_orientation_hint_candidate_schema.get("side_candidate_enum", []))

    ok("schema.entrance_intersection.name", entrance_intersection_hint_candidate_schema.get("schema_name") == "EntranceIntersectionHintCandidate")
    for expected in ("entrance_hint", "intersection_hint", "crossing_hint", "floor_hint"):
        ok(f"schema.entrance_intersection.type.{expected}", expected in entrance_intersection_hint_candidate_schema.get("hint_type_enum", []))

    ok("conflict_policy.name", map_visual_memory_conflict_policy.get("policy_name") == "MapVisualMemoryConflictPolicy")
    for expected in (
        "map_vs_visual",
        "map_vs_ocr",
        "map_vs_memory",
        "location_vs_visual",
        "route_vs_visual",
        "poi_vs_signage",
        "side_hint_vs_scene_sketch",
        "arrival_hint_vs_visual_absence",
        "crossing_hint_vs_safety_uncertain",
        "stale_map_vs_current_observation",
    ):
        ok(f"conflict_policy.type.{expected}", expected in map_visual_memory_conflict_policy.get("conflict_types", []))
    for expected in (
        "MapLocationConflictCandidate",
        "ReobserveRequestCandidate",
        "UserConfirmationCandidate",
        "CorrectionHandoffCandidate",
    ):
        ok(f"conflict_policy.output.{expected}", expected in map_visual_memory_conflict_policy.get("outputs", []))
    for expected in (
        "地图冲突不自动修正事实",
        "地图不能覆盖视觉安全",
        "地图不能覆盖用户反馈",
        "地图不能直接更新 WorldModel",
        "地图 conflict 可进入 correction candidate / handoff placeholder",
    ):
        ok(f"conflict_policy.principle.{expected}", expected in map_visual_memory_conflict_policy.get("principles", []))

    for expected in (
        "目标接近时提高 destination_landmark_focus",
        "右侧店铺 hint 触发 right-side shopfront focus",
        "路口 hint 触发 crossing_focus / traffic_light_focus",
        "入口 hint 触发 doorway_or_entrance_focus",
        "POI hint 触发 signage_focus / OCR activation candidate",
        "路线不确定时触发 active view adjustment / reobserve",
    ):
        ok(f"focus_binding.allowed.{expected}", expected in map_location_to_visual_focus_binding_policy.get("allowed_bindings", []))
    for expected in (
        "地图直接触发 OCR runtime",
        "地图直接触发 tracking runtime",
        "地图直接生成导航动作",
        "地图直接判断已到达",
        "地图直接判断可过马路",
    ):
        ok(f"focus_binding.forbidden.{expected}", expected in map_location_to_visual_focus_binding_policy.get("forbidden_bindings", []))
    ok("focus_binding.tracking_requires_visual_focus", map_location_to_visual_focus_binding_policy.get("tracking_request_from_map_requires_visual_focus") is True)

    for expected in (
        "approaching_destination -> signage OCR target candidate",
        "shop_search_area -> shopfront / doorplate OCR target candidate",
        "intersection_area -> traffic sign / countdown text OCR target candidate placeholder",
        "indoor_floor_hint -> directory sign OCR target candidate",
        "temporary_notice_area -> notice OCR target candidate",
    ):
        ok(f"ocr_binding.allowed.{expected}", expected in map_location_to_ocr_activation_hint_policy.get("allowed_bindings", []))
    for expected in (
        "full-frame OCR",
        "OCR provider invocation",
        "OCRRequest submission",
        "OCR from map alone without visual/readable region candidate",
        "OCR on privacy-sensitive text without filtering",
    ):
        ok(f"ocr_binding.forbidden.{expected}", expected in map_location_to_ocr_activation_hint_policy.get("forbidden_bindings", []))
    ok("ocr_binding.requires_visual_focus", map_location_to_ocr_activation_hint_policy.get("ocr_activation_from_map_requires_visual_focus") is True)

    ok("feedback_policy.name", map_location_feedback_policy.get("policy_name") == "MapLocationFeedbackPolicy")
    for expected in (
        "MapLocationFeedbackCandidate",
        "RouteStageFeedbackCandidate",
        "TargetProximityFeedbackCandidate",
        "SideOrientationFeedbackCandidate",
        "EntranceIntersectionFeedbackCandidate",
        "MapVisualMemoryConflictFeedbackCandidate",
    ):
        ok(f"feedback_policy.output.{expected}", expected in map_location_feedback_policy.get("output_candidates", []))
    for key, value in (
        ("feedback_candidate_only", True),
        ("speech_allowed", False),
        ("action_allowed", False),
        ("navigation_action_allowed", False),
        ("requires_arbitration", True),
    ):
        ok(f"feedback_policy.principles.{key}", map_location_feedback_policy.get("principles", {}).get(key) is value)
    ok("feedback_policy.principles.fact_status", map_location_feedback_policy.get("principles", {}).get("fact_status") == "not_fact")

    scenarios = map_location_readonly_context_scenario_matrix.get("scenarios", [])
    ok("scenario_matrix.count", map_location_readonly_context_scenario_matrix.get("scenario_count", 0) >= 10, map_location_readonly_context_scenario_matrix.get("scenario_count"))
    for scenario_id in (
        "route_walking_map_hint",
        "approaching_destination_nearby",
        "right_side_shop_search",
        "intersection_approach_hint",
        "entrance_hint_candidate",
        "off_route_uncertain_hint",
        "map_visual_conflict_shop_absent",
        "stale_map_or_old_poi",
        "indoor_floor_directory_hint",
        "gps_low_confidence_location_uncertain",
    ):
        row = next((item for item in scenarios if item.get("scenario_id") == scenario_id), {})
        ok(f"scenario.{scenario_id}.present", bool(row))
        ok(f"scenario.{scenario_id}.not_fact", row.get("fact_status") == "not_fact")
        ok(f"scenario.{scenario_id}.action_disabled", row.get("expected_boundary_flags", {}).get("action_allowed") is False)
        ok(f"scenario.{scenario_id}.crossing_disabled", row.get("expected_boundary_flags", {}).get("crossing_action_allowed") is False)
    ok("scenario.approaching_destination.effect", "target_proximity_hint_candidate" in next((item for item in scenarios if item.get("scenario_id") == "approaching_destination_nearby"), {}).get("generated_candidates", []))
    ok("scenario.right_side_shop.effect", "side_orientation_hint_candidate" in next((item for item in scenarios if item.get("scenario_id") == "right_side_shop_search"), {}).get("generated_candidates", []))
    ok("scenario.intersection.effect", "entrance_intersection_hint_candidate" in next((item for item in scenarios if item.get("scenario_id") == "intersection_approach_hint"), {}).get("generated_candidates", []))
    ok("scenario.gps_low_confidence.user_confirmation", "user_confirmation_candidate" in next((item for item in scenarios if item.get("scenario_id") == "gps_low_confidence_location_uncertain"), {}).get("generated_candidates", []))

    for key in (
        "map_context_role",
        "location_context_role",
        "route_context_role",
        "poi_context_role",
    ):
        ok(f"boundary_matrix.{key}", map_location_boundary_matrix.get(key) == "readonly_hint", map_location_boundary_matrix.get(key))
    for key in (
        "map_is_fact_authority",
        "map_is_navigation_authority",
        "map_is_safety_authority",
        "map_can_trigger_action",
        "map_can_prove_arrival",
        "map_can_grant_crossing_permission",
        "map_can_write_worldmodel",
        "map_can_write_memory",
        "map_can_write_fact",
    ):
        ok(f"boundary_matrix.{key}", map_location_boundary_matrix.get(key) is False)
    for key in (
        "map_location_feedback_candidate_only",
        "map_visual_conflict_candidate_generated",
        "ocr_activation_from_map_requires_visual_focus",
        "tracking_request_from_map_requires_visual_focus",
    ):
        ok(f"boundary_matrix.{key}", map_location_boundary_matrix.get(key) is True)
    ok("boundary_matrix.freshness_values", len(map_location_boundary_matrix.get("freshness_policy", {}).get("freshness_status_values", [])) >= 4)
    ok("boundary_matrix.gps_degrade", map_location_boundary_matrix.get("freshness_policy", {}).get("gps_low_confidence_degrades_to_route_uncertain") is True)

    carryover = governance_debt_register.get("carryover_topics", [])
    ok("governance_debt.count", len(carryover) >= 10, len(carryover))
    ok("governance_debt.future_midplatform_function_governance_required", governance_debt_register.get("future_midplatform_function_governance_required") is True)
    ok("governance_debt.no_duplicate_governance_module_allowed", governance_debt_register.get("no_duplicate_governance_module_allowed") is True)

    ok("next_phase_recommendation.final_decision", next_phase_recommendation.get("final_decision") == FINAL_DECISION)
    ok("next_phase_recommendation.next_phase", next_phase_recommendation.get("recommended_next_phase") == NEXT_PHASE)

    for payload_name, payload in (("no_runtime", no_runtime_boundary_report), ("no_write", no_write_boundary_report)):
        ok(f"{payload_name}.policy_scope", payload.get("policy_scope") == "map_location_readonly_context_policy_only")
        for key in ("no_runtime_executed", "no_new_runtime_enabled", "boundary_ok"):
            ok(f"{payload_name}.{key}", payload.get(key) is True)
        for key in (
            "map_api_invoked",
            "gaode_api_invoked",
            "gps_runtime_invoked",
            "route_planning_runtime_invoked",
            "camera_invoked",
            "visual_model_invoked",
            "ocr_provider_invoked",
            "ocrrequest_submitted",
            "tracking_runtime_invoked",
            "optical_flow_runtime_invoked",
            "supervision_invoked",
            "bytetrack_invoked",
            "ocsort_invoked",
            "speech_gate_invoked",
            "vop_invoked",
            "tts_invoked",
            "task_state_committed_now",
            "navigation_action_triggered",
            "route_modified",
            "arrival_fact_written",
            "crossing_action_instruction_allowed",
            "scene_delta_generated",
            "world_model_written",
            "memory_written",
            "library_written",
            "fact_written",
            "entity_resolution_runtime_invoked",
            "fact_admission_runtime_invoked",
            "memory_consolidation_invoked",
            "library_experience_commit_invoked",
        ):
            ok(f"{payload_name}.{key}", payload.get(key) is False)
        ok(f"{payload_name}.violations", payload.get("violations") == [])

    passed = sum(1 for item in checks if item["passed"])
    verdict = "GO" if passed >= MIN_CHECKS and not any(not item["passed"] for item in checks) else "NO_GO"
    report = {
        "phase": PHASE_ID,
        "verdict": verdict,
        "checks_passed": passed,
        "checks_total": len(checks),
        "min_checks_required": MIN_CHECKS,
        "baseline_requirement": BASELINE_REQUIREMENT,
        "final_decision": FINAL_DECISION if verdict == "GO" else "MAP_LOCATION_READONLY_CONTEXT_POLICY_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if verdict == "GO" else PHASE_ID,
        "failed_checks": [item for item in checks if not item["passed"]],
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"verdict": verdict, "checks_passed": passed, "checks_total": len(checks)}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
