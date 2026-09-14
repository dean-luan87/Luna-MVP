#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Post Controlled Frame Input Roadmap Decision v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

PHASE_ID = "Phase-Post-Controlled-Frame-Input-Roadmap-Decision-v1-001"
FINAL_DECISION = "POST_CONTROLLED_FRAME_INPUT_ROADMAP_DECISION_READY_FOR_CROSSING_DECISION_SAFETY_GOVERNANCE_POLICY"
NEXT_PHASE = "Phase-Crossing-Decision-Safety-Governance-Policy-v1-001"
MIN_CHECKS = 170
BASELINE_REQUIREMENT = 130

EXPECTED_CAPABILITIES = [
    "Basic Navigation Loop Vision Strengthening Closure",
    "Post Vision Strengthening Roadmap Decision",
    "Map / Location Read-Only Context Policy",
    "MidPlatform Perception Orchestration Policy",
    "Task-Aware Visual Focus Policy",
    "Controlled Frame Input Planning",
    "Controlled Frame Input DryRun",
    "Controlled Frame Input Post-DryRun Review",
    "Controlled Frame Input Closure",
]

EXPECTED_ROUTES = [
    ("A", "Controlled Frame Sample Planning", "P0", False, "Phase-Controlled-Frame-Sample-Planning-v1-001"),
    ("B", "Crossing Decision Safety Governance Policy", "P0", True, NEXT_PHASE),
    ("C", "MidPlatform Function Governance / Consolidation", "P0", False, "Phase-MidPlatform-Function-Governance-Consolidation-v1-001"),
    ("D", "MidPlatform Resilience / Robustness Preplan", "P1", False, "Phase-MidPlatform-Resilience-Robustness-Preplan-v1-001"),
    ("E", "Offline Distributed MidPlatform Architecture Preplan", "P1", False, "Phase-Offline-Distributed-MidPlatform-Architecture-Preplan-v1-001"),
    ("F", "Minimal Controlled Visual Runtime Planning", "P1", False, "Phase-Minimal-Controlled-Visual-Runtime-Planning-v1-001"),
    ("G", "Exploration Drive Policy", "P2", False, "Phase-Exploration-Drive-Policy-v1-001"),
    ("H", "WorldModel Candidate Layer / Memory / Library Governance", "P2", False, "Phase-WorldModel-Memory-Library-Governance-v1-001"),
    ("I", "Emotion Map / Affective Engine", "P2", False, "Phase-Emotion-Map-Affective-Engine-v1-001"),
]

EXPECTED_RESILIENCE_TOPICS = [
    "midplatform_single_point_failure",
    "local_minimum_safety_path",
    "module_autonomy",
    "degraded_operation",
    "failover_arbitration",
    "pressure_test",
    "resource_congestion_control",
    "local_first_midplatform",
    "cloud_enhanced_midplatform",
    "distributed_candidate_sync",
    "conflict_merge_rollback",
    "privacy_preserving_sync",
    "offline_weak_network_mode",
    "multi_device_coordination",
]

EXPECTED_EXPLORATION_DIRECTIONS = [
    "safety_exploration",
    "task_exploration",
    "worldmodel_gap_exploration",
    "conflict_validation_exploration",
    "resource_environment_adaptation_exploration",
    "emotion_map_precursor_exploration",
]

EXPECTED_NON_CLAIMS = [
    "roadmap decision 不等于 runtime enablement",
    "roadmap decision 不等于 controlled sample planning 已开始",
    "roadmap decision 不等于真实图像读取",
    "roadmap decision 不等于 live camera 接入",
    "roadmap decision 不等于 map API 接入",
    "roadmap decision 不等于 OCR provider 接入",
    "roadmap decision 不等于 tracking runtime 接入",
    "selected next phase 不等于允许过马路动作",
    "Crossing Decision Safety Governance 不等于真实过街判断 runtime",
    "Controlled Frame Sample Planning 不等于读取真实样例内容",
    "MidPlatform Function Governance 不等于新增 runtime module",
    "MidPlatform Resilience / Robustness 不等于 failover runtime 已开放",
    "Offline Distributed MidPlatform 不等于多设备同步已开放",
    "Exploration Drive 当前不进入 runtime",
    "WorldModel Candidate Layer / Memory / Library Governance 当前不进入写路径",
    "Emotion Map / Affective Engine 当前不进入实现",
]

EXPECTED_GOVERNANCE_TOPICS = [
    "frame source policy complexity",
    "privacy tagging complexity",
    "frame quality gate complexity",
    "STC/freshness integration complexity",
    "downstream handoff complexity",
    "dual-device placeholder future complexity",
    "hardware-stage deferred debt",
    "controlled sample planning deferred",
    "crossing safety governance gap",
    "midplatform function governance accumulation",
    "midplatform resilience planning deferred",
    "offline distributed architecture deferred",
    "no duplicate governance module enforcement",
]


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-root", default="/Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/post_controlled_frame_input_roadmap_decision_v1_smoke_v0")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    checks: List[Dict[str, Any]] = []

    def ok(check_id: str, passed: bool, detail: Any = None) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})

    summary = _load_json(root / "summary.json")
    input_root_matrix = _load_json(root / "input_root_matrix.json")
    post_controlled_frame_input_roadmap_decision = _load_json(root / "post_controlled_frame_input_roadmap_decision.json")
    current_controlled_frame_input_status_summary = _load_json(root / "current_controlled_frame_input_status_summary.json")
    completed_capability_summary = _load_json(root / "completed_capability_summary.json")
    route_option_matrix = _load_json(root / "route_option_matrix.json")
    priority_ranking = _load_json(root / "priority_ranking.json")
    recommended_next_phase_decision = _load_json(root / "recommended_next_phase_decision.json")
    deferred_resilience_distributed_midplatform_register = _load_json(root / "deferred_resilience_distributed_midplatform_register.json")
    deferred_exploration_drive_register = _load_json(root / "deferred_exploration_drive_register.json")
    deferred_worldmodel_memory_library_emotion_register = _load_json(root / "deferred_worldmodel_memory_library_emotion_register.json")
    boundary_freeze = _load_json(root / "boundary_freeze.json")
    governance_debt_roadmap_register = _load_json(root / "governance_debt_roadmap_register.json")
    non_claims_register = _load_json(root / "non_claims_register.json")
    next_phase_recommendation = _load_json(root / "next_phase_recommendation.json")
    no_runtime_boundary_report = _load_json(root / "no_runtime_boundary_report.json")
    no_write_boundary_report = _load_json(root / "no_write_boundary_report.json")

    rows = input_root_matrix.get("rows", [])
    idx = {row.get("intake_id"): row for row in rows}
    for intake_id in (
        "controlled_frame_input_closure",
        "controlled_frame_input_post_review",
        "controlled_frame_input_dryrun",
        "controlled_frame_input_planning",
        "map_location_readonly_context",
        "post_vision_strengthening_roadmap_decision",
        "vision_strengthening_closure",
        "task_aware_visual_focus",
        "midplatform_perception_orchestration",
        "minimal_runtime_integration_closure",
        "ocr_final_closure",
    ):
        ok(f"input.{intake_id}", idx.get(intake_id, {}).get("loaded") is True)
    for intake_id in (
        "hardware_profile_capability_registry",
        "system_health_center_governance",
        "vision_frame_trace_stream_registry",
        "vision_frame_input_governance",
        "safety_task_arbitration_policy",
        "crossing_decision_safety_governance_policy",
        "traffic_safety_semantics_stub",
        "midplatform_function_governance_consolidation",
    ):
        status = idx.get(intake_id, {}).get("status")
        ok(f"input.{intake_id}.optional", status in {"loaded", "optional_missing"}, status)
    ok("input.row_count", input_root_matrix.get("row_count") == len(rows), input_root_matrix.get("row_count"))

    for key in (
        "controlled_frame_input_closure_input_loaded",
        "controlled_frame_input_post_review_input_loaded",
        "controlled_frame_input_dryrun_input_loaded",
        "controlled_frame_input_planning_input_loaded",
        "map_location_readonly_context_input_loaded",
        "post_vision_strengthening_roadmap_decision_input_loaded",
        "vision_strengthening_closure_input_loaded",
        "minimal_runtime_integration_closure_loaded",
        "ocr_final_closure_loaded",
        "current_status_summary_generated",
        "completed_capability_summary_generated",
        "route_option_matrix_generated",
        "priority_ranking_generated",
        "recommended_next_phase_decision_generated",
        "deferred_resilience_distributed_midplatform_register_generated",
        "deferred_exploration_drive_register_generated",
        "deferred_worldmodel_memory_library_emotion_register_generated",
        "boundary_freeze_generated",
        "governance_debt_roadmap_register_generated",
        "non_claims_register_generated",
        "crossing_decision_safety_governance_route_exists",
        "controlled_frame_sample_planning_route_exists",
        "midplatform_function_governance_route_exists",
        "midplatform_resilience_route_exists",
        "offline_distributed_midplatform_route_exists",
        "exploration_drive_deferred",
        "midplatform_resilience_deferred",
        "offline_distributed_midplatform_deferred",
        "worldmodel_candidate_layer_deferred",
        "memory_library_governance_deferred",
        "emotion_engine_deferred",
        "no_runtime_executed",
        "no_new_runtime_enabled",
        "boundary_ok",
    ):
        ok(f"summary.{key}", summary.get(key) is True)
    ok("summary.route_option_count", summary.get("route_option_count", 0) >= 8, summary.get("route_option_count"))
    ok("summary.p0_route_count", summary.get("p0_route_count", 0) >= 3, summary.get("p0_route_count"))
    ok("summary.p1_route_count", summary.get("p1_route_count", 0) >= 3, summary.get("p1_route_count"))
    ok("summary.p2_route_count", summary.get("p2_route_count", 0) >= 3, summary.get("p2_route_count"))
    for key in (
        "controlled_sample_planning_started",
        "live_camera_claimed",
        "visual_runtime_claimed",
        "image_read_claimed",
        "production_readiness_claimed",
        "runtime_enablement_claimed",
        "frame_content_loaded",
        "actual_image_read",
        "camera_invoked",
        "visual_model_invoked",
        "map_api_invoked",
        "gaode_api_invoked",
        "gps_runtime_invoked",
        "ocr_provider_invoked",
        "ocrrequest_submitted",
        "tracking_runtime_invoked",
        "optical_flow_runtime_invoked",
        "supervision_invoked",
        "bytetrack_invoked",
        "ocsort_invoked",
        "dual_device_runtime_invoked",
        "dual_model_runtime_invoked",
        "failover_runtime_invoked",
        "multi_input_fusion_runtime_invoked",
        "speech_gate_invoked",
        "vop_invoked",
        "tts_invoked",
        "task_state_committed_now",
        "navigation_action_triggered",
        "route_modified",
        "scene_delta_generated",
        "world_model_written",
        "memory_written",
        "library_written",
        "fact_written",
        "entity_resolution_runtime_invoked",
        "fact_admission_runtime_invoked",
        "memory_consolidation_invoked",
        "library_experience_commit_invoked",
        "emotion_engine_invoked",
    ):
        ok(f"summary.{key}", summary.get(key) is False)
    ok("summary.decision_scope", summary.get("decision_scope") == "post_controlled_frame_input_roadmap_decision_only")
    ok("summary.violations", summary.get("violations") == [])
    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)

    ok("decision.scope", post_controlled_frame_input_roadmap_decision.get("decision_scope") == "post_controlled_frame_input_roadmap_decision_only")
    ok("decision.id", post_controlled_frame_input_roadmap_decision.get("decision_id") == "pcfird_v1_001")
    ok("decision.current_status", post_controlled_frame_input_roadmap_decision.get("current_mainline_status") == "controlled_frame_input_closed_waiting_for_next_policy_decision")
    ok("decision.completed_ref", post_controlled_frame_input_roadmap_decision.get("completed_capability_summary_ref") == "completed_capability_summary.json")
    ok("decision.route_ref", post_controlled_frame_input_roadmap_decision.get("route_option_matrix_ref") == "route_option_matrix.json")
    ok("decision.priority_ref", post_controlled_frame_input_roadmap_decision.get("priority_ranking_ref") == "priority_ranking.json")
    ok("decision.selected_next_phase", post_controlled_frame_input_roadmap_decision.get("selected_next_phase") == NEXT_PHASE)
    ok("decision.rejected_count", len(post_controlled_frame_input_roadmap_decision.get("rejected_or_deferred_routes", [])) >= 8, len(post_controlled_frame_input_roadmap_decision.get("rejected_or_deferred_routes", [])))
    ok("decision.reason_count", len(post_controlled_frame_input_roadmap_decision.get("decision_reason", [])) >= 5, len(post_controlled_frame_input_roadmap_decision.get("decision_reason", [])))
    ok("decision.boundary_ref", post_controlled_frame_input_roadmap_decision.get("boundary_freeze_ref") == "boundary_freeze.json")

    for key in (
        "controlled_frame_input_planning_closed",
        "controlled_frame_input_dryrun_closed",
        "controlled_frame_input_post_review_closed",
        "controlled_frame_input_closed",
    ):
        ok(f"current_status.{key}", current_controlled_frame_input_status_summary.get(key) is True)
    for key in (
        "controlled_sample_planning_started",
        "live_camera_claimed",
        "visual_runtime_claimed",
        "image_read_claimed",
        "production_readiness_claimed",
        "runtime_enablement_claimed",
    ):
        ok(f"current_status.{key}", current_controlled_frame_input_status_summary.get(key) is False)
    ok("current_status.label", current_controlled_frame_input_status_summary.get("current_mainline_status") == "controlled_frame_input_closed_waiting_for_next_policy_decision")
    ok("current_status.source_ref", bool(current_controlled_frame_input_status_summary.get("source_closure_ref")))

    capability_rows = completed_capability_summary.get("capabilities", [])
    capability_idx = {row.get("capability_name"): row for row in capability_rows}
    ok("completed_capabilities.count", completed_capability_summary.get("completed_capability_count", 0) >= 9, completed_capability_summary.get("completed_capability_count"))
    for capability in EXPECTED_CAPABILITIES:
        row = capability_idx.get(capability, {})
        ok(f"capability.{capability}.present", capability in capability_idx)
        ok(f"capability.{capability}.runtime_enabled", row.get("runtime_enabled") is False)
        ok(f"capability.{capability}.production_ready", row.get("production_ready") is False)
        ok(f"capability.{capability}.live_ready", row.get("live_ready") is False)
        ok(f"capability.{capability}.validated", row.get("validated_in_current_mainline") is True)

    route_rows = route_option_matrix.get("routes", [])
    route_idx = {row.get("route_id"): row for row in route_rows}
    ok("routes.count", route_option_matrix.get("route_option_count", 0) >= 8, route_option_matrix.get("route_option_count"))
    ok("routes.selected_route_id", route_option_matrix.get("selected_route_id") == "B")
    ok("routes.selected_single", sum(1 for row in route_rows if row.get("selected_now") is True) == 1)
    for route_id, route_name, priority, selected_now, phase_name in EXPECTED_ROUTES:
        row = route_idx.get(route_id, {})
        ok(f"route.{route_id}.present", route_id in route_idx)
        ok(f"route.{route_id}.name", row.get("route_name") == route_name, row.get("route_name"))
        ok(f"route.{route_id}.priority", row.get("recommended_priority") == priority, row.get("recommended_priority"))
        ok(f"route.{route_id}.selected_now", row.get("selected_now") is selected_now, row.get("selected_now"))
        ok(f"route.{route_id}.phase_name", row.get("recommended_phase_name") == phase_name, row.get("recommended_phase_name"))
        ok(f"route.{route_id}.route_type", isinstance(row.get("route_type"), str) and bool(row.get("route_type")))
        ok(f"route.{route_id}.readiness_level", isinstance(row.get("readiness_level"), str) and bool(row.get("readiness_level")))
        ok(f"route.{route_id}.dependency", isinstance(row.get("dependency"), list) and len(row.get("dependency", [])) >= 2)
        ok(f"route.{route_id}.risk_level", isinstance(row.get("risk_level"), str) and bool(row.get("risk_level")))
        ok(f"route.{route_id}.expected_value", isinstance(row.get("expected_value"), str) and bool(row.get("expected_value")))
        ok(f"route.{route_id}.runtime_risk", isinstance(row.get("runtime_risk"), str) and bool(row.get("runtime_risk")))
        ok(f"route.{route_id}.write_risk", isinstance(row.get("write_risk"), str) and bool(row.get("write_risk")))
        ok(f"route.{route_id}.governance_debt_impact", bool(row.get("governance_debt_impact")))
        if not selected_now:
            ok(f"route.{route_id}.defer_reason", bool(row.get("defer_reason")))
        else:
            ok(f"route.{route_id}.defer_reason_empty", row.get("defer_reason") == "")

    ok("priority.P0_count", priority_ranking.get("p0_route_count", 0) >= 3, priority_ranking.get("p0_route_count"))
    ok("priority.P1_count", priority_ranking.get("p1_route_count", 0) >= 3, priority_ranking.get("p1_route_count"))
    ok("priority.P2_count", priority_ranking.get("p2_route_count", 0) >= 3, priority_ranking.get("p2_route_count"))
    ok("priority.selected_top", priority_ranking.get("selected_top_priority_route") == "Crossing Decision Safety Governance Policy")
    for expected in (
        "Controlled Frame Sample Planning",
        "Crossing Decision Safety Governance Policy",
        "MidPlatform Function Governance / Consolidation",
    ):
        ok(f"priority.P0.{expected}", expected in priority_ranking.get("P0", []))
    for expected in (
        "MidPlatform Resilience / Robustness Preplan",
        "Offline Distributed MidPlatform Architecture Preplan",
        "Minimal Controlled Visual Runtime Planning",
    ):
        ok(f"priority.P1.{expected}", expected in priority_ranking.get("P1", []))
    for expected in (
        "Exploration Drive Policy",
        "WorldModel Candidate Layer / Memory / Library Governance",
        "Emotion Map / Affective Engine",
    ):
        ok(f"priority.P2.{expected}", expected in priority_ranking.get("P2", []))

    ok("recommended.scope", recommended_next_phase_decision.get("decision_scope") == "post_controlled_frame_input_roadmap_decision_only")
    ok("recommended.selected_next_phase", recommended_next_phase_decision.get("selected_next_phase") == NEXT_PHASE)
    ok("recommended.source_ref", bool(recommended_next_phase_decision.get("source_closure_ref")))
    ok("recommended.reason_count", len(recommended_next_phase_decision.get("decision_reason", [])) >= 5)
    ok("recommended.rejected_count", len(recommended_next_phase_decision.get("rejected_or_deferred_routes", [])) >= 8)
    ok("recommended.route_ref", recommended_next_phase_decision.get("route_option_matrix_ref") == "route_option_matrix.json")
    ok("recommended.priority_ref", recommended_next_phase_decision.get("priority_ranking_ref") == "priority_ranking.json")
    ok("recommended.completed_ref", recommended_next_phase_decision.get("completed_capability_summary_ref") == "completed_capability_summary.json")
    ok("recommended.boundary_ref", recommended_next_phase_decision.get("boundary_freeze_ref") == "boundary_freeze.json")

    ok("resilience.midplatform_resilience_deferred", deferred_resilience_distributed_midplatform_register.get("midplatform_resilience_deferred") is True)
    ok("resilience.offline_distributed_midplatform_deferred", deferred_resilience_distributed_midplatform_register.get("offline_distributed_midplatform_deferred") is True)
    ok("resilience.current_status", deferred_resilience_distributed_midplatform_register.get("current_status") == "future_architecture_candidate")
    ok("resilience.runtime_allowed_now", deferred_resilience_distributed_midplatform_register.get("runtime_allowed_now") is False)
    ok("resilience.direct_action_allowed", deferred_resilience_distributed_midplatform_register.get("direct_action_allowed") is False)
    for topic in EXPECTED_RESILIENCE_TOPICS:
        ok(f"resilience.topic.{topic}", topic in deferred_resilience_distributed_midplatform_register.get("required_future_topics", []))

    ok("exploration.deferred", deferred_exploration_drive_register.get("exploration_drive_deferred") is True)
    ok("exploration.status", deferred_exploration_drive_register.get("current_status") == "deferred_future_candidate")
    ok("exploration.priority", deferred_exploration_drive_register.get("priority") == "P2")
    for key in (
        "runtime_allowed_now",
        "direct_action_allowed",
        "worldmodel_write_allowed",
        "memory_write_allowed",
        "fact_write_allowed",
    ):
        ok(f"exploration.{key}", deferred_exploration_drive_register.get(key) is False)
    for direction in EXPECTED_EXPLORATION_DIRECTIONS:
        ok(f"exploration.direction.{direction}", direction in deferred_exploration_drive_register.get("exploration_directions", []))
    ok("exploration.defer_reason_count", len(deferred_exploration_drive_register.get("defer_reason", [])) >= 4)

    deferred_rows = deferred_worldmodel_memory_library_emotion_register.get("deferred_items", [])
    deferred_idx = {row.get("capability_name"): row for row in deferred_rows}
    ok("deferred.worldmodel_flag", deferred_worldmodel_memory_library_emotion_register.get("worldmodel_candidate_layer_deferred") is True)
    ok("deferred.memory_flag", deferred_worldmodel_memory_library_emotion_register.get("memory_library_governance_deferred") is True)
    ok("deferred.emotion_flag", deferred_worldmodel_memory_library_emotion_register.get("emotion_engine_deferred") is True)
    for capability in ("WorldModel Candidate Layer", "Memory / Library Governance", "Emotion Map / Affective Engine"):
        row = deferred_idx.get(capability, {})
        ok(f"deferred.{capability}.present", capability in deferred_idx)
        ok(f"deferred.{capability}.status", row.get("current_status") == "deferred_future_candidate")
        ok(f"deferred.{capability}.runtime_allowed_now", row.get("runtime_allowed_now") is False)
        ok(f"deferred.{capability}.write_allowed_now", row.get("write_allowed_now") is False)
        ok(f"deferred.{capability}.defer_reason", bool(row.get("defer_reason")))

    for key in (
        "no_runtime",
        "no_write",
        "no_action",
        "no_speech",
        "no_fact",
        "no_live_camera",
        "no_image_read",
        "no_visual_model",
        "no_map_api",
        "no_OCR_provider",
        "no_tracking_runtime",
        "no_worldmodel_write",
        "no_memory_write",
        "no_library_write",
        "no_entity_resolution",
        "no_fact_admission",
        "no_emotion_engine",
        "no_dual_device_runtime",
        "no_failover_runtime",
    ):
        ok(f"boundary.{key}", boundary_freeze.get(key) is True)

    carryover = governance_debt_roadmap_register.get("carryover_topics", [])
    ok("governance.count", len(carryover) >= len(EXPECTED_GOVERNANCE_TOPICS), len(carryover))
    for topic in EXPECTED_GOVERNANCE_TOPICS:
        row = next((item for item in carryover if item.get("topic") == topic), {})
        ok(f"governance.topic.{topic}", bool(row))
    ok("governance.inherited_from_closure", len(governance_debt_roadmap_register.get("inherited_from_controlled_frame_input_closure", [])) >= 4, len(governance_debt_roadmap_register.get("inherited_from_controlled_frame_input_closure", [])))
    ok("governance.future_midplatform_function_governance_required", governance_debt_roadmap_register.get("future_midplatform_function_governance_required") is True)
    ok("governance.future_midplatform_resilience_governance_required", governance_debt_roadmap_register.get("future_midplatform_resilience_governance_required") is True)
    ok("governance.no_duplicate_governance_module_allowed", governance_debt_roadmap_register.get("no_duplicate_governance_module_allowed") is True)
    ok("governance.crossing_selected_for_p0", governance_debt_roadmap_register.get("crossing_safety_governance_selected_for_p0") is True)

    non_claims = set(non_claims_register.get("non_claims", []))
    ok("non_claims.count", len(non_claims) >= len(EXPECTED_NON_CLAIMS), len(non_claims))
    for claim in EXPECTED_NON_CLAIMS:
        ok(f"non_claim.{claim}", claim in non_claims)
    for key in (
        "controlled_sample_planning_started",
        "live_camera_claimed",
        "visual_runtime_claimed",
        "image_read_claimed",
        "production_readiness_claimed",
        "runtime_enablement_claimed",
    ):
        ok(f"non_claims_register.{key}", non_claims_register.get(key) is False)

    ok("next_phase.route_name", next_phase_recommendation.get("route_name") == "Crossing Decision Safety Governance Policy")
    ok("next_phase.priority_level", next_phase_recommendation.get("priority_level") == "P0")
    ok("next_phase.final_decision", next_phase_recommendation.get("final_decision") == FINAL_DECISION)
    ok("next_phase.recommended_next_phase", next_phase_recommendation.get("recommended_next_phase") == NEXT_PHASE)

    for report_name, report in (
        ("no_runtime_boundary_report", no_runtime_boundary_report),
        ("no_write_boundary_report", no_write_boundary_report),
    ):
        ok(f"{report_name}.decision_scope", report.get("decision_scope") == "post_controlled_frame_input_roadmap_decision_only")
        ok(f"{report_name}.roadmap_decision_only", report.get("roadmap_decision_only") is True)
        for key in ("no_runtime_executed", "no_new_runtime_enabled", "boundary_ok"):
            ok(f"{report_name}.{key}", report.get(key) is True)
        for key in (
            "frame_content_loaded",
            "actual_image_read",
            "camera_invoked",
            "visual_model_invoked",
            "map_api_invoked",
            "gaode_api_invoked",
            "gps_runtime_invoked",
            "ocr_provider_invoked",
            "ocrrequest_submitted",
            "tracking_runtime_invoked",
            "optical_flow_runtime_invoked",
            "supervision_invoked",
            "bytetrack_invoked",
            "ocsort_invoked",
            "dual_device_runtime_invoked",
            "dual_model_runtime_invoked",
            "failover_runtime_invoked",
            "multi_input_fusion_runtime_invoked",
            "speech_gate_invoked",
            "vop_invoked",
            "tts_invoked",
            "task_state_committed_now",
            "navigation_action_triggered",
            "route_modified",
            "scene_delta_generated",
            "world_model_written",
            "memory_written",
            "library_written",
            "fact_written",
            "entity_resolution_runtime_invoked",
            "fact_admission_runtime_invoked",
            "memory_consolidation_invoked",
            "library_experience_commit_invoked",
            "emotion_engine_invoked",
        ):
            ok(f"{report_name}.{key}", report.get(key) is False)
        ok(f"{report_name}.violations", report.get("violations") == [])

    passed_count = sum(1 for check in checks if check["passed"])
    verifier_report = {
        "phase": PHASE_ID,
        "min_checks": MIN_CHECKS,
        "baseline_requirement": BASELINE_REQUIREMENT,
        "check_count": len(checks),
        "passed_count": passed_count,
        "failed_count": len(checks) - passed_count,
        "verifier": "GO" if len(checks) >= MIN_CHECKS and passed_count == len(checks) else "NO_GO",
        "final_decision": summary.get("final_decision"),
        "recommended_next_phase": summary.get("recommended_next_phase"),
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(json.dumps(verifier_report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "verifier": verifier_report["verifier"],
                "check_count": verifier_report["check_count"],
                "passed_count": verifier_report["passed_count"],
                "failed_count": verifier_report["failed_count"],
                "final_decision": verifier_report["final_decision"],
                "recommended_next_phase": verifier_report["recommended_next_phase"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if verifier_report["verifier"] == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
