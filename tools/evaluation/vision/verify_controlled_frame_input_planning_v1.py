#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Controlled Frame Input Planning v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

PHASE_ID = "Phase-Controlled-Frame-Input-Planning-v1-001"
FINAL_DECISION = "CONTROLLED_FRAME_INPUT_PLANNING_READY_FOR_CONTROLLED_FRAME_INPUT_DRYRUN"
NEXT_PHASE = "Phase-Controlled-Frame-Input-DryRun-v1-001"
MIN_CHECKS = 170
BASELINE_REQUIREMENT = 130


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-root", default="/Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/controlled_frame_input_planning_v1_smoke_v0")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    checks: List[Dict[str, Any]] = []

    def ok(check_id: str, passed: bool, detail: Any = None) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})

    summary = _load_json(root / "summary.json")
    input_root_matrix = _load_json(root / "input_root_matrix.json")
    controlled_frame_input_planning_policy = _load_json(root / "controlled_frame_input_planning_policy.json")
    frame_source_candidate_schema = _load_json(root / "frame_source_candidate_schema.json")
    controlled_frame_input_candidate_schema = _load_json(root / "controlled_frame_input_candidate_schema.json")
    frame_intake_gate_policy = _load_json(root / "frame_intake_gate_policy.json")
    frame_quality_gate_policy = _load_json(root / "frame_quality_gate_policy.json")
    frame_privacy_tagging_policy = _load_json(root / "frame_privacy_tagging_policy.json")
    frame_stc_freshness_policy = _load_json(root / "frame_stc_freshness_policy.json")
    frame_downstream_handoff_policy = _load_json(root / "frame_downstream_handoff_policy.json")
    dual_device_redundant_perception_placeholder = _load_json(root / "dual_device_redundant_perception_placeholder.json")
    controlled_frame_input_readiness_gate = _load_json(root / "controlled_frame_input_readiness_gate.json")
    controlled_frame_input_planning_scenario_matrix = _load_json(root / "controlled_frame_input_planning_scenario_matrix.json")
    controlled_frame_input_boundary_matrix = _load_json(root / "controlled_frame_input_boundary_matrix.json")
    governance_debt_register = _load_json(root / "governance_debt_register.json")
    next_phase_recommendation = _load_json(root / "next_phase_recommendation.json")
    no_runtime_boundary_report = _load_json(root / "no_runtime_boundary_report.json")
    no_write_boundary_report = _load_json(root / "no_write_boundary_report.json")

    rows = input_root_matrix.get("rows", [])
    idx = {row.get("intake_id"): row for row in rows}
    for intake_id in (
        "map_location_readonly_context",
        "post_vision_strengthening_roadmap_decision",
        "vision_strengthening_closure",
        "visual_ocr_map_task_feedback",
        "task_aware_visual_focus",
        "midplatform_perception_orchestration",
        "minimal_runtime_integration_closure",
        "ocr_final_closure",
    ):
        ok(f"input.{intake_id}", idx.get(intake_id, {}).get("loaded") is True)
    for intake_id in (
        "vision_frame_trace_stream_registry",
        "vision_frame_input_governance",
        "vision_roi_proposal_stub",
        "hardware_profile_capability_registry",
        "system_health_center_governance",
        "simulation_lab_profile",
    ):
        ok(f"input.{intake_id}.optional", idx.get(intake_id, {}).get("status") in {"loaded", "optional_missing"}, idx.get(intake_id, {}).get("status"))

    for key in (
        "map_location_readonly_context_input_loaded",
        "post_vision_strengthening_roadmap_decision_input_loaded",
        "vision_strengthening_closure_input_loaded",
        "task_aware_visual_focus_input_loaded",
        "midplatform_perception_orchestration_input_loaded",
        "minimal_runtime_integration_closure_loaded",
        "ocr_final_closure_loaded",
        "controlled_frame_input_planning_policy_defined",
        "frame_source_candidate_schema_defined",
        "controlled_frame_input_candidate_schema_defined",
        "frame_intake_gate_policy_defined",
        "frame_quality_gate_policy_defined",
        "frame_privacy_tagging_policy_defined",
        "frame_stc_freshness_policy_defined",
        "frame_downstream_handoff_policy_defined",
        "controlled_frame_input_readiness_gate_generated",
        "scenario_matrix_generated",
        "governance_debt_register_generated",
        "dual_device_redundant_perception_placeholder_defined",
        "perception_input_channel_placeholder_defined",
        "perception_device_health_placeholder_defined",
        "perception_lane_failover_placeholder_defined",
        "dual_input_consistency_placeholder_defined",
        "static_test_image_allowed_candidate",
        "prerecorded_video_frame_allowed_candidate",
        "simulation_frame_allowed_candidate",
        "frame_to_ocr_requires_visual_focus",
        "frame_to_tracking_requires_visual_focus",
        "frame_to_world_observation_requires_policy",
        "privacy_tags_required_for_downstream",
        "source_chain_required",
        "timestamp_required",
        "stc_freshness_reuse_required",
        "no_runtime_executed",
        "no_new_runtime_enabled",
        "boundary_ok",
    ):
        ok(f"summary.{key}", summary.get(key) is True)
    ok("summary.scenario_count", summary.get("scenario_count", 0) >= 10, summary.get("scenario_count"))
    for key in (
        "live_camera_allowed",
        "device_camera_allowed",
        "external_stream_allowed",
        "dual_device_runtime_allowed",
        "dual_model_runtime_allowed",
        "failover_runtime_allowed",
        "automatic_hardware_switch_allowed",
        "frame_to_navigation_action_allowed",
        "frame_to_speech_output_allowed",
        "frame_to_worldmodel_write_allowed",
        "frame_to_memory_write_allowed",
        "frame_to_fact_write_allowed",
    ):
        ok(f"summary.{key}", summary.get(key) is False)
    ok("summary.hardware_stage_deferred", summary.get("hardware_stage_deferred") is True)
    for key in (
        "camera_invoked",
        "camera_opened",
        "video_capture_invoked",
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
    ):
        ok(f"summary.{key}", summary.get(key) is False)
    ok("summary.violations", summary.get("violations") == [])
    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)

    ok("planning_policy.scope", controlled_frame_input_planning_policy.get("policy_scope") == "controlled_frame_input_planning_only")
    for expected in (
        "static_test_image",
        "pre_recorded_video_frame",
        "simulation_frame",
        "synthetic_frame",
        "archived_frame_candidate",
        "controlled_uploaded_frame",
    ):
        ok(f"planning_policy.allowed.{expected}", expected in controlled_frame_input_planning_policy.get("allowed_frame_sources", []))
    for expected in (
        "live_camera_placeholder",
        "device_camera_placeholder",
        "external_stream_placeholder",
    ):
        ok(f"planning_policy.forbidden.{expected}", expected in controlled_frame_input_planning_policy.get("forbidden_frame_sources", []))
    for expected in (
        "controlled frame input planning 不等于 camera runtime",
        "当前不读取 live camera",
        "当前不读取用户设备摄像头",
        "当前不调用视觉模型",
        "当前只定义未来受控 frame 输入的规则",
    ):
        ok(f"planning_policy.non_claim.{expected}", expected in controlled_frame_input_planning_policy.get("non_claims", []))

    ok("frame_source.schema", frame_source_candidate_schema.get("schema_name") == "FrameSourceCandidate")
    ok("frame_source.enum_count", len(frame_source_candidate_schema.get("source_type_enum", [])) >= 9)
    for expected in (
        "static_test_image",
        "pre_recorded_video_frame",
        "simulation_frame",
        "synthetic_frame",
        "archived_frame_candidate",
        "controlled_uploaded_frame",
        "live_camera_placeholder",
        "device_camera_placeholder",
        "external_stream_placeholder",
    ):
        ok(f"frame_source.enum.{expected}", expected in frame_source_candidate_schema.get("source_type_enum", []))
    source_defaults = frame_source_candidate_schema.get("source_defaults", {})
    ok("frame_source.live_camera_blocked", source_defaults.get("live_camera_placeholder", {}).get("allowed_now") is False)
    ok("frame_source.device_camera_blocked", source_defaults.get("device_camera_placeholder", {}).get("allowed_now") is False)
    ok("frame_source.external_stream_blocked", source_defaults.get("external_stream_placeholder", {}).get("allowed_now") is False)
    ok("frame_source.static_allowed", source_defaults.get("static_test_image", {}).get("allowed_now") is True)
    ok("frame_source.prerecorded_allowed", source_defaults.get("pre_recorded_video_frame", {}).get("allowed_now") is True)
    ok("frame_source.simulation_allowed", source_defaults.get("simulation_frame", {}).get("allowed_now") is True)

    ok("controlled_frame.schema", controlled_frame_input_candidate_schema.get("schema_name") == "ControlledFrameInputCandidate")
    for expected in (
        "view_quality_candidate",
        "scene_sketch_candidate",
        "visual_focus_plan_candidate",
        "ocr_activation_candidate",
        "tracking_request_candidate",
        "world_observation_candidate",
        "debug_visualization_candidate",
    ):
        ok(f"controlled_frame.downstream.{expected}", expected in controlled_frame_input_candidate_schema.get("downstream_allowed_targets_enum", []))
    for expected in (
        "frame_input_candidate_id",
        "frame_source_candidate_ref",
        "frame_id",
        "frame_timestamp",
        "monotonic_seq",
        "source_time_ref",
        "location_context_ref",
        "pose_or_view_context_ref",
        "device_context_ref",
        "task_context_ref",
        "privacy_tags",
        "quality_status_candidate",
        "freshness_status",
        "ttl_policy_ref",
        "frame_hash_placeholder",
        "storage_policy",
        "downstream_allowed_targets",
        "runtime_action_allowed",
        "fact_status",
        "source_chain",
    ):
        ok(f"controlled_frame.field.{expected}", any(field.get("name") == expected for field in controlled_frame_input_candidate_schema.get("field_specs", [])))

    for expected in (
        "source allowed",
        "source_chain present",
        "timestamp present",
        "privacy tags present",
        "task context present or explicitly taskless background context",
        "quality status computable or unknown-but-marked",
        "no live runtime required",
        "no write side effect",
        "no direct output side effect",
    ):
        ok(f"intake_gate.allow.{expected}", expected in frame_intake_gate_policy.get("allow_conditions", []))
    for expected in (
        "unknown source",
        "missing source_chain",
        "missing timestamp",
        "live camera attempt",
        "external stream attempt",
        "privacy tags missing",
        "task context missing without background policy",
        "frame tries to trigger runtime",
        "frame tries to write fact",
        "frame tries to bypass MidPlatform",
    ):
        ok(f"intake_gate.reject.{expected}", expected in frame_intake_gate_policy.get("reject_conditions", []))
    ok("intake_gate.source_chain_required", frame_intake_gate_policy.get("source_chain_required") is True)
    ok("intake_gate.timestamp_required", frame_intake_gate_policy.get("timestamp_required") is True)
    ok("intake_gate.privacy_required", frame_intake_gate_policy.get("privacy_tags_required_for_downstream") is True)

    for expected in (
        "blur",
        "brightness",
        "exposure",
        "occlusion",
        "motion_blur",
        "camera_shake",
        "target_distance",
        "angle_quality",
        "resolution_sufficiency",
        "frame_stability",
        "privacy_sensitivity",
    ):
        ok(f"quality_gate.dimension.{expected}", expected in frame_quality_gate_policy.get("quality_dimensions", []))
    for level in ("GOOD", "DEGRADED", "POOR", "BLOCKED", "UNKNOWN_MARKED"):
        row = frame_quality_gate_policy.get("quality_levels", {}).get(level, {})
        ok(f"quality_gate.level.{level}.present", bool(row))
        ok(f"quality_gate.level.{level}.has_scene_sketch", "scene_sketch_allowed_candidate" in row)
        ok(f"quality_gate.level.{level}.has_visual_focus", "visual_focus_allowed_candidate" in row)
        ok(f"quality_gate.level.{level}.has_ocr", "ocr_activation_allowed_candidate" in row)
        ok(f"quality_gate.level.{level}.has_tracking", "tracking_request_allowed_candidate" in row)
        ok(f"quality_gate.level.{level}.has_worldobs", "world_observation_allowed_candidate" in row)
        ok(f"quality_gate.level.{level}.has_reject_reason", "reject_reason" in row)

    for expected in (
        "human_face_visible",
        "bystander_presence",
        "license_plate_visible",
        "private_space_candidate",
        "home_context_candidate",
        "medical_context_candidate",
        "school_or_child_context_candidate",
        "workplace_context_candidate",
        "screen_or_document_visible",
        "personal_item_visible",
        "commercial_sensitive_candidate",
    ):
        ok(f"privacy_tag.{expected}", expected in frame_privacy_tagging_policy.get("privacy_tags", []))
    for expected in (
        "privacy tag missing -> frame blocked from downstream",
        "privacy filtering owned by MidPlatform",
        "frame collection != frame long-term storage",
        "frame usable for task != frame eligible for WorldModel/Memory",
        "private/home/medical/school/workplace contexts require restricted policy",
        "no face recognition",
        "no identity inference",
        "no emotional inference",
    ):
        ok(f"privacy_policy.principle.{expected}", expected in frame_privacy_tagging_policy.get("principles", []))

    for key in (
        "timestamp_required",
        "monotonic_seq_required",
        "location_context_optional_but_marked",
        "pose_or_view_context_optional_but_marked",
        "current_action_allowed_when_stale",
        "archive_candidate_allowed",
        "source_chain_required",
        "stc_freshness_reuse_required",
    ):
        value = frame_stc_freshness_policy.get(key)
        if key == "current_action_allowed_when_stale":
            ok(f"stc_policy.{key}", value is False)
        else:
            ok(f"stc_policy.{key}", value is True)
    ok("stc_policy.freshness_values", len(frame_stc_freshness_policy.get("freshness_status_values", [])) >= 4)

    for expected in (
        "Frame -> ViewQualityCandidate",
        "Frame -> SceneSketchCandidate",
        "Frame -> VisualFocusPlan candidate",
        "Frame -> OCRActivationCandidate only via VisualFocus",
        "Frame -> TrackingRequestCandidate only via VisualFocus/MidPlatform",
        "Frame -> WorldObservationCandidate only via WorldObservation policy",
        "Frame -> Debug/Review artifact if no privacy conflict",
    ):
        ok(f"handoff.allowed.{expected}", expected in frame_downstream_handoff_policy.get("allowed_handoffs", []))
    for expected in (
        "Frame -> OCR provider directly",
        "Frame -> tracking runtime directly",
        "Frame -> map API",
        "Frame -> NavigationAction",
        "Frame -> SpeechOutput",
        "Frame -> WorldModel write",
        "Frame -> Memory write",
        "Frame -> Fact write",
        "Frame -> SceneDelta",
    ):
        ok(f"handoff.forbidden.{expected}", expected in frame_downstream_handoff_policy.get("forbidden_handoffs", []))
    for key in (
        "frame_to_ocr_requires_visual_focus",
        "frame_to_tracking_requires_visual_focus",
        "frame_to_world_observation_requires_policy",
    ):
        ok(f"handoff.{key}", frame_downstream_handoff_policy.get(key) is True)
    for key in (
        "frame_to_navigation_action_allowed",
        "frame_to_speech_output_allowed",
        "frame_to_worldmodel_write_allowed",
        "frame_to_memory_write_allowed",
        "frame_to_fact_write_allowed",
    ):
        ok(f"handoff.{key}", frame_downstream_handoff_policy.get(key) is False)

    ok("dual_placeholder.name", dual_device_redundant_perception_placeholder.get("placeholder_name") == "Dual-Device / Dual-Lane Redundant Perception Placeholder")
    ok("dual_placeholder.scope", dual_device_redundant_perception_placeholder.get("placeholder_scope") == "future_hardware_stage_only")
    for expected in (
        "当前不接真实硬件",
        "当前不接真实 camera",
        "当前不定义最终设备形态",
        "当前不绑定具体模型",
        "当前不执行 failover",
        "当前不做 dual-camera runtime",
        "当前不做 dual-model runtime",
        "当前不做多输入融合",
        "当前只预留字段和边界",
    ):
        ok(f"dual_placeholder.positioning.{expected}", expected in dual_device_redundant_perception_placeholder.get("design_positioning", []))
    for expected in (
        "主输入设备 + 备份输入设备",
        "Safety-World Lane 输入设备 + Task-Focus Lane 输入设备",
        "低功耗安全观察设备 + 高精度任务观察设备",
        "RGB + depth / ToF / wide-angle / secondary camera 等组合",
        "主模型 + 备份模型",
        "轻量安全模型 + 重型任务模型",
    ):
        ok(f"dual_placeholder.future.{expected}", expected in dual_device_redundant_perception_placeholder.get("future_candidate_directions", []))
    ok("dual_placeholder.channel_schema", dual_device_redundant_perception_placeholder.get("perception_input_channel_placeholder", {}).get("schema_name") == "PerceptionInputChannelPlaceholder")
    ok("dual_placeholder.health_schema", dual_device_redundant_perception_placeholder.get("perception_device_health_placeholder", {}).get("schema_name") == "PerceptionDeviceHealthPlaceholder")
    ok("dual_placeholder.failover_schema", dual_device_redundant_perception_placeholder.get("perception_lane_failover_placeholder", {}).get("schema_name") == "PerceptionLaneFailoverPlaceholder")
    ok("dual_placeholder.consistency_schema", dual_device_redundant_perception_placeholder.get("dual_input_consistency_placeholder", {}).get("schema_name") == "DualInputConsistencyPlaceholder")
    for key in (
        "dual_device_runtime_allowed",
        "dual_model_runtime_allowed",
        "failover_runtime_allowed",
        "device_health_fact_allowed",
        "lane_failover_action_allowed",
        "automatic_hardware_switch_allowed",
        "multi_input_fusion_runtime_allowed",
    ):
        ok(f"dual_placeholder.boundary.{key}", dual_device_redundant_perception_placeholder.get("boundaries", {}).get(key) is False)
    ok("dual_placeholder.boundary.hardware_stage_deferred", dual_device_redundant_perception_placeholder.get("boundaries", {}).get("hardware_stage_deferred") is True)

    ok("readiness_gate.ready", controlled_frame_input_readiness_gate.get("ready_for_next_phase") is True)
    ok("readiness_gate.verdict", controlled_frame_input_readiness_gate.get("verdict") == "GO")
    for expected in (
        "source policy defined",
        "frame candidate schema defined",
        "intake gate defined",
        "quality gate defined",
        "privacy tagging defined",
        "STC/freshness policy defined",
        "downstream handoff policy defined",
        "no live camera runtime",
        "no model runtime",
        "no write",
        "next phase clear",
    ):
        ok(f"readiness_gate.go.{expected}", expected in controlled_frame_input_readiness_gate.get("go_conditions", []))
    for expected in (
        "live camera attempted",
        "unknown frame source allowed",
        "missing source_chain allowed",
        "privacy tags optional for downstream",
        "OCR provider allowed directly",
        "tracking runtime allowed directly",
        "WorldModel/Memory/Fact write allowed",
        "NavigationAction allowed",
        "Speech output allowed",
    ):
        ok(f"readiness_gate.no_go.{expected}", expected in controlled_frame_input_readiness_gate.get("no_go_conditions", []))

    scenarios = controlled_frame_input_planning_scenario_matrix.get("scenarios", [])
    ok("scenario_matrix.count", controlled_frame_input_planning_scenario_matrix.get("scenario_count", 0) >= 10, controlled_frame_input_planning_scenario_matrix.get("scenario_count"))
    for scenario_id in (
        "static_test_image_allowed_for_schema_test",
        "pre_recorded_video_frame_allowed_for_controlled_dryrun",
        "simulation_frame_allowed_for_sim_lab",
        "uploaded_frame_requires_privacy_tags",
        "live_camera_placeholder_blocked_now",
        "external_stream_placeholder_blocked_now",
        "low_quality_frame_degraded",
        "privacy_sensitive_home_frame_restricted",
        "stale_frame_archive_candidate_only",
        "frame_to_ocr_requires_visual_focus",
    ):
        row = next((item for item in scenarios if item.get("scenario_id") == scenario_id), {})
        ok(f"scenario.{scenario_id}.present", bool(row))
        ok(f"scenario.{scenario_id}.not_fact", row.get("fact_status") == "not_fact")
        ok(f"scenario.{scenario_id}.runtime_action_disabled", row.get("runtime_action_allowed") is False)
    ok("scenario.live_camera.blocked", next((item for item in scenarios if item.get("scenario_id") == "live_camera_placeholder_blocked_now"), {}).get("allowed_for_future_dryrun") is False)
    ok("scenario.external_stream.blocked", next((item for item in scenarios if item.get("scenario_id") == "external_stream_placeholder_blocked_now"), {}).get("allowed_for_future_dryrun") is False)
    ok("scenario.uploaded_frame.privacy_required", next((item for item in scenarios if item.get("scenario_id") == "uploaded_frame_requires_privacy_tags"), {}).get("privacy_tags_required") is True)

    for key in (
        "planning_scope",
        "live_camera_allowed",
        "device_camera_allowed",
        "external_stream_allowed",
        "dual_device_runtime_allowed",
        "dual_model_runtime_allowed",
        "failover_runtime_allowed",
        "device_health_fact_allowed",
        "lane_failover_action_allowed",
        "automatic_hardware_switch_allowed",
        "multi_input_fusion_runtime_allowed",
        "static_test_image_allowed_candidate",
        "prerecorded_video_frame_allowed_candidate",
        "simulation_frame_allowed_candidate",
        "frame_to_ocr_requires_visual_focus",
        "frame_to_tracking_requires_visual_focus",
        "frame_to_world_observation_requires_policy",
        "frame_to_navigation_action_allowed",
        "frame_to_speech_output_allowed",
        "frame_to_worldmodel_write_allowed",
        "frame_to_memory_write_allowed",
        "frame_to_fact_write_allowed",
        "privacy_tags_required_for_downstream",
        "source_chain_required",
        "timestamp_required",
        "stc_freshness_reuse_required",
        "current_stage_runtime_forbidden",
    ):
        expected_true = key in {
            "static_test_image_allowed_candidate",
            "prerecorded_video_frame_allowed_candidate",
            "simulation_frame_allowed_candidate",
            "frame_to_ocr_requires_visual_focus",
            "frame_to_tracking_requires_visual_focus",
            "frame_to_world_observation_requires_policy",
            "privacy_tags_required_for_downstream",
            "source_chain_required",
            "timestamp_required",
            "stc_freshness_reuse_required",
            "current_stage_runtime_forbidden",
        }
        if key == "planning_scope":
            ok(f"boundary_matrix.{key}", controlled_frame_input_boundary_matrix.get(key) == "controlled_frame_input_planning_only")
        elif expected_true:
            ok(f"boundary_matrix.{key}", controlled_frame_input_boundary_matrix.get(key) is True)
        else:
            ok(f"boundary_matrix.{key}", controlled_frame_input_boundary_matrix.get(key) is False)
    ok("boundary_matrix.hardware_stage_deferred", controlled_frame_input_boundary_matrix.get("hardware_stage_deferred") is True)

    carryover = governance_debt_register.get("carryover_topics", [])
    ok("governance_debt.count", len(carryover) >= 10, len(carryover))
    ok("governance_debt.future_midplatform_function_governance_required", governance_debt_register.get("future_midplatform_function_governance_required") is True)
    ok("governance_debt.no_duplicate_governance_module_allowed", governance_debt_register.get("no_duplicate_governance_module_allowed") is True)

    ok("next_phase.final_decision", next_phase_recommendation.get("final_decision") == FINAL_DECISION)
    ok("next_phase.recommended", next_phase_recommendation.get("recommended_next_phase") == NEXT_PHASE)

    for payload_name, payload in (("no_runtime", no_runtime_boundary_report), ("no_write", no_write_boundary_report)):
        ok(f"{payload_name}.planning_scope", payload.get("planning_scope") == "controlled_frame_input_planning_only")
        for key in ("no_runtime_executed", "no_new_runtime_enabled", "boundary_ok"):
            ok(f"{payload_name}.{key}", payload.get(key) is True)
        for key in (
            "live_camera_allowed",
            "device_camera_allowed",
            "external_stream_allowed",
            "camera_invoked",
            "camera_opened",
            "video_capture_invoked",
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
        "final_decision": FINAL_DECISION if verdict == "GO" else "CONTROLLED_FRAME_INPUT_PLANNING_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if verdict == "GO" else PHASE_ID,
        "failed_checks": [item for item in checks if not item["passed"]],
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"verdict": verdict, "checks_passed": passed, "checks_total": len(checks)}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
