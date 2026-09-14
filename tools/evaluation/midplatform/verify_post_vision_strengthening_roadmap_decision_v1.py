#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Post Vision Strengthening Roadmap Decision v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

PHASE_ID = "Phase-Post-Vision-Strengthening-Roadmap-Decision-v1-001"
FINAL_DECISION = "POST_VISION_STRENGTHENING_ROADMAP_DECISION_READY_FOR_MAP_LOCATION_READONLY_CONTEXT_POLICY"
NEXT_PHASE = "Phase-Map-Location-ReadOnly-Context-Policy-v1-001"
MIN_CHECKS = 160
BASELINE_REQUIREMENT = 120


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-root", default="/Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/post_vision_strengthening_roadmap_decision_v1_smoke_v0")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    checks: List[Dict[str, Any]] = []

    def ok(check_id: str, passed: bool, detail: Any = None) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})

    summary = _load_json(root / "summary.json")
    input_root_matrix = _load_json(root / "input_root_matrix.json")
    current_mainline_status_summary = _load_json(root / "current_mainline_status_summary.json")
    completed_capability_summary = _load_json(root / "completed_capability_summary.json")
    route_option_matrix = _load_json(root / "route_option_matrix.json")
    priority_ranking = _load_json(root / "priority_ranking.json")
    recommended_next_phase_decision = _load_json(root / "recommended_next_phase_decision.json")
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
        "vision_strengthening_closure",
        "post_dryrun_review",
        "dryrun",
        "visual_ocr_map_task_feedback",
        "selective_tracking",
        "world_observation_entity_feature",
        "task_aware_visual_focus",
        "midplatform_perception_orchestration",
        "return_to_vision_planning",
        "return_to_vision_preplan",
        "minimal_runtime_integration_closure",
        "ocr_final_closure",
    ):
        ok(f"input.{intake_id}", idx.get(intake_id, {}).get("loaded") is True)
    for intake_id in (
        "basic_navigation_loop_stabilization",
        "safety_task_arbitration_policy",
        "navigation_guidance_speech_adapter",
        "voice_interruption_governance_dryrun",
        "voice_command_ownership_gate_policy",
        "map_location_readonly_context_policy",
        "map_route_location_context_integration",
        "gps_route_context_dryrun",
    ):
        status = idx.get(intake_id, {}).get("status")
        ok(f"input.{intake_id}.optional", status in {"loaded", "optional_missing"}, status)

    for key in (
        "vision_strengthening_closure_input_loaded",
        "post_dryrun_review_input_loaded",
        "dryrun_input_loaded",
        "visual_ocr_map_task_feedback_input_loaded",
        "selective_tracking_input_loaded",
        "world_observation_entity_feature_input_loaded",
        "task_aware_visual_focus_input_loaded",
        "midplatform_perception_orchestration_input_loaded",
        "minimal_runtime_integration_closure_loaded",
        "ocr_final_closure_loaded",
        "current_mainline_status_summary_generated",
        "completed_capability_summary_generated",
        "route_option_matrix_generated",
        "priority_ranking_generated",
        "recommended_next_phase_decision_generated",
        "deferred_exploration_drive_register_generated",
        "deferred_worldmodel_memory_library_emotion_register_generated",
        "boundary_freeze_generated",
        "governance_debt_roadmap_register_generated",
        "non_claims_register_generated",
        "exploration_drive_deferred",
        "task_driven_perception_priority_first",
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
    ok("summary.p1_route_count", summary.get("p1_route_count", 0) >= 2, summary.get("p1_route_count"))
    ok("summary.p2_route_count", summary.get("p2_route_count", 0) >= 3, summary.get("p2_route_count"))
    for key in ("live_navigation_claimed", "production_readiness_claimed", "runtime_enablement_claimed"):
        ok(f"summary.{key}", summary.get(key) is False)
    for key in (
        "camera_invoked",
        "visual_model_invoked",
        "map_api_invoked",
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
    ok("summary.violations_empty", summary.get("violations") == [])
    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)

    for key in (
        "basic_navigation_loop_vision_strengthening_closed",
        "policy_chain_closed",
        "dryrun_chain_closed",
        "feedback_chain_closed",
        "navigation_loop_vision_strengthening_closed",
    ):
        ok(f"current_mainline_status.{key}", current_mainline_status_summary.get(key) is True)
    ok("current_mainline_status.runtime_enabled", current_mainline_status_summary.get("runtime_enabled") is False)
    ok("current_mainline_status.live_navigation_claimed", current_mainline_status_summary.get("live_navigation_claimed") is False)
    ok("current_mainline_status.production_readiness_claimed", current_mainline_status_summary.get("production_readiness_claimed") is False)
    ok("current_mainline_status.source_ref", bool(current_mainline_status_summary.get("source_closure_ref")))

    capability_rows = completed_capability_summary.get("capabilities", [])
    ok("completed_capability_summary.count", completed_capability_summary.get("completed_capability_count", 0) >= 9, completed_capability_summary.get("completed_capability_count"))
    for expected in (
        "Return-To-Vision Mainline Planning",
        "MidPlatform Perception Orchestration Policy",
        "Task-Aware Visual Focus Policy",
        "World Observation and Entity Feature Policy",
        "Selective Tracking Adapter Policy",
        "Visual-OCR-Map-Task Feedback DryRun",
        "Basic Navigation Loop Vision Strengthening DryRun",
        "Post-DryRun Review",
        "Closure",
    ):
        row = next((item for item in capability_rows if item.get("capability_name") == expected), {})
        ok(f"completed_capability.{expected}.present", bool(row))
        ok(f"completed_capability.{expected}.runtime_disabled", row.get("runtime_enabled") is False)
        ok(f"completed_capability.{expected}.prod_disabled", row.get("production_ready") is False)
        ok(f"completed_capability.{expected}.live_disabled", row.get("live_navigation_ready") is False)

    route_rows = route_option_matrix.get("routes", [])
    ok("route_option_matrix.count", route_option_matrix.get("route_option_count", 0) >= 8, route_option_matrix.get("route_option_count"))
    ok("route_option_matrix.selected_route_id", route_option_matrix.get("selected_route_id") == "A")
    ok("route_option_matrix.selected_single", sum(1 for row in route_rows if row.get("selected_now") is True) == 1)
    for route_name in (
        "Map / Location Read-Only Context Policy",
        "Controlled Frame Input Planning / Policy",
        "Crossing Decision Safety Governance Policy",
        "MidPlatform Function Governance / Consolidation",
        "Minimal Controlled Runtime Trial Planning",
        "Exploration Drive Policy",
        "WorldModel Candidate Layer",
        "Memory / Library Governance",
        "Emotion Map / Affective Engine",
    ):
        row = next((item for item in route_rows if item.get("route_name") == route_name), {})
        ok(f"route.{route_name}.present", bool(row))
        ok(f"route.{route_name}.priority", row.get("recommended_priority") in {"P0", "P1", "P2"}, row.get("recommended_priority"))
        ok(f"route.{route_name}.phase_name", bool(row.get("recommended_phase_name")))

    selected_row = next((item for item in route_rows if item.get("route_name") == "Map / Location Read-Only Context Policy"), {})
    ok("route.map_location.selected", selected_row.get("selected_now") is True)
    ok("route.map_location.priority", selected_row.get("recommended_priority") == "P0")
    ok("route.map_location.phase", selected_row.get("recommended_phase_name") == NEXT_PHASE)

    for route_name in (
        "Controlled Frame Input Planning / Policy",
        "Crossing Decision Safety Governance Policy",
        "MidPlatform Function Governance / Consolidation",
        "Minimal Controlled Runtime Trial Planning",
        "Exploration Drive Policy",
        "WorldModel Candidate Layer",
        "Memory / Library Governance",
        "Emotion Map / Affective Engine",
    ):
        row = next((item for item in route_rows if item.get("route_name") == route_name), {})
        ok(f"route.{route_name}.deferred", row.get("selected_now") is False)
        ok(f"route.{route_name}.defer_reason", bool(row.get("defer_reason")))

    ok("priority_ranking.p0_count", priority_ranking.get("p0_route_count", 0) >= 3, priority_ranking.get("p0_route_count"))
    ok("priority_ranking.p1_count", priority_ranking.get("p1_route_count", 0) >= 2, priority_ranking.get("p1_route_count"))
    ok("priority_ranking.p2_count", priority_ranking.get("p2_route_count", 0) >= 3, priority_ranking.get("p2_route_count"))
    ok("priority_ranking.task_driven_perception_priority_first", priority_ranking.get("task_driven_perception_priority_first") is True)
    for expected in (
        "Map / Location Read-Only Context Policy",
        "Controlled Frame Input Planning / Policy",
        "Crossing Decision Safety Governance Policy",
    ):
        ok(f"priority_ranking.P0.{expected}", expected in priority_ranking.get("P0", []))
    for expected in (
        "MidPlatform Function Governance / Consolidation",
        "Minimal Controlled Runtime Trial Planning",
    ):
        ok(f"priority_ranking.P1.{expected}", expected in priority_ranking.get("P1", []))
    for expected in (
        "Exploration Drive Policy",
        "WorldModel Candidate Layer",
        "Memory / Library Governance",
        "Emotion Map / Affective Engine",
    ):
        ok(f"priority_ranking.P2.{expected}", expected in priority_ranking.get("P2", []))

    ok("recommended_next_phase_decision.scope", recommended_next_phase_decision.get("decision_scope") == "post_vision_strengthening_roadmap_decision_only")
    ok("recommended_next_phase_decision.selected_next_phase", recommended_next_phase_decision.get("selected_next_phase") == NEXT_PHASE)
    ok("recommended_next_phase_decision.route_ref", recommended_next_phase_decision.get("route_option_matrix_ref") == "route_option_matrix.json")
    ok("recommended_next_phase_decision.priority_ref", recommended_next_phase_decision.get("priority_ranking_ref") == "priority_ranking.json")
    ok("recommended_next_phase_decision.completed_ref", recommended_next_phase_decision.get("completed_capability_summary_ref") == "completed_capability_summary.json")
    ok("recommended_next_phase_decision.boundary_ref", recommended_next_phase_decision.get("boundary_freeze_ref") == "boundary_freeze.json")
    ok("recommended_next_phase_decision.reason_count", len(recommended_next_phase_decision.get("decision_reason", [])) >= 4, len(recommended_next_phase_decision.get("decision_reason", [])))
    ok("recommended_next_phase_decision.rejected_count", len(recommended_next_phase_decision.get("rejected_or_deferred_routes", [])) >= 8, len(recommended_next_phase_decision.get("rejected_or_deferred_routes", [])))

    ok("exploration.capability_name", deferred_exploration_drive_register.get("capability_name") == "Survival-Oriented Exploration Drive / Adaptive Exploration Layer")
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
    for direction in (
        "safety_exploration",
        "task_exploration",
        "worldmodel_gap_exploration",
        "conflict_validation_exploration",
        "resource_environment_adaptation_exploration",
        "emotion_map_precursor_exploration",
    ):
        ok(f"exploration.direction.{direction}", direction in deferred_exploration_drive_register.get("exploration_directions", []))
    ok("exploration.defer_reason_count", len(deferred_exploration_drive_register.get("defer_reason", [])) >= 5)

    deferred_rows = deferred_worldmodel_memory_library_emotion_register.get("deferred_items", [])
    ok("deferred_register.worldmodel_flag", deferred_worldmodel_memory_library_emotion_register.get("worldmodel_candidate_layer_deferred") is True)
    ok("deferred_register.memory_flag", deferred_worldmodel_memory_library_emotion_register.get("memory_library_governance_deferred") is True)
    ok("deferred_register.emotion_flag", deferred_worldmodel_memory_library_emotion_register.get("emotion_engine_deferred") is True)
    for expected in (
        "WorldModel Candidate Layer",
        "Memory / Library Governance",
        "Emotion Map / Affective Engine",
    ):
        row = next((item for item in deferred_rows if item.get("capability_name") == expected), {})
        ok(f"deferred_register.{expected}.present", bool(row))
        ok(f"deferred_register.{expected}.status", row.get("current_status") == "deferred_future_candidate")
        ok(f"deferred_register.{expected}.runtime_disabled", row.get("runtime_allowed_now") is False)
        ok(f"deferred_register.{expected}.write_disabled", row.get("write_allowed_now") is False)

    for key in (
        "no_runtime",
        "no_write",
        "no_action",
        "no_speech",
        "no_fact",
        "no_live_navigation",
        "no_production_readiness",
        "no_camera",
        "no_map_api",
        "no_ocr_provider",
        "no_tracking_runtime",
        "no_worldmodel_write",
        "no_memory_write",
        "no_library_write",
        "no_entity_resolution",
        "no_fact_admission",
        "no_emotion_engine",
    ):
        ok(f"boundary_freeze.{key}", boundary_freeze.get(key) is True)

    carryover = governance_debt_roadmap_register.get("carryover_topics", [])
    ok("governance_debt.count", len(carryover) >= 10, len(carryover))
    ok("governance_debt.midplatform_p1", governance_debt_roadmap_register.get("midplatform_function_governance_retained_in_p1") is True)
    ok("governance_debt.map_p0", governance_debt_roadmap_register.get("map_location_contract_gap_selected_for_p0") is True)
    for topic in (
        "midplatform capability expansion debt",
        "resource budget complexity",
        "privacy filtering complexity",
        "conflict correction complexity",
        "temporary facility governance complexity",
        "world observation handoff complexity",
        "duplicated schema risk",
        "visual focus policy complexity",
        "selective tracking policy complexity",
        "feedback candidate proliferation",
        "map/location context contract gap",
        "crossing safety governance gap",
        "controlled frame input governance gap",
    ):
        row = next((item for item in carryover if item.get("topic") == topic), {})
        ok(f"governance_debt.topic.{topic}", bool(row))

    non_claims = non_claims_register.get("non_claims", [])
    ok("non_claims.count", len(non_claims) >= 15, len(non_claims))
    for expected in (
        "roadmap decision 不等于 runtime enablement",
        "roadmap decision 不等于 live navigation",
        "roadmap priority 不等于 production readiness",
        "selected next phase 不等于 camera 接入",
        "selected next phase 不等于 map API 接入",
        "selected next phase 不等于 OCR provider 接入",
        "selected next phase 不等于 tracking runtime 接入",
        "Map / Location Read-Only Context Policy 不等于真实地图调用",
        "Controlled Frame Input Planning 不等于 live camera",
        "Crossing Decision Safety Governance 不等于允许过街动作",
        "MidPlatform Function Governance 不等于新增 runtime module",
        "Exploration Drive Policy 当前不进入 runtime",
        "WorldModel Candidate Layer 当前不进入 fact admission",
        "Memory / Library Governance 当前不进入 write path",
        "Emotion Map / Affective Engine 当前不进入实现",
    ):
        ok(f"non_claims.{expected}", expected in non_claims)
    for key in ("live_navigation_claimed", "production_readiness_claimed", "runtime_enablement_claimed"):
        ok(f"non_claims_register.{key}", non_claims_register.get(key) is False)

    ok("next_phase_recommendation.final_decision", next_phase_recommendation.get("final_decision") == FINAL_DECISION)
    ok("next_phase_recommendation.next_phase", next_phase_recommendation.get("recommended_next_phase") == NEXT_PHASE)
    ok("next_phase_recommendation.priority", next_phase_recommendation.get("priority_level") == "P0")
    ok("next_phase_recommendation.route_name", next_phase_recommendation.get("route_name") == "Map / Location Read-Only Context Policy")

    for payload_name, payload in (("no_runtime", no_runtime_boundary_report), ("no_write", no_write_boundary_report)):
        for key in ("roadmap_decision_only", "no_runtime_executed", "no_new_runtime_enabled", "boundary_ok"):
            ok(f"{payload_name}.{key}", payload.get(key) is True)
        for key in (
            "camera_invoked",
            "visual_model_invoked",
            "map_api_invoked",
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
        "final_decision": FINAL_DECISION if verdict == "GO" else "POST_VISION_STRENGTHENING_ROADMAP_DECISION_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if verdict == "GO" else PHASE_ID,
        "failed_checks": [item for item in checks if not item["passed"]],
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"verdict": verdict, "checks_passed": passed, "checks_total": len(checks)}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
