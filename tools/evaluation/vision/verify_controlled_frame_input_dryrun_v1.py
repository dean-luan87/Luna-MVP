#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Controlled Frame Input DryRun v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

PHASE_ID = "Phase-Controlled-Frame-Input-DryRun-v1-001"
FINAL_DECISION = "CONTROLLED_FRAME_INPUT_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
NEXT_PHASE = "Phase-Controlled-Frame-Input-Post-DryRun-Review-v1-001"
MIN_CHECKS = 200
BASELINE_REQUIREMENT = 160


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-root", default="/Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/controlled_frame_input_dryrun_v1_smoke_v0")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    checks: List[Dict[str, Any]] = []

    def ok(check_id: str, passed: bool, detail: Any = None) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})

    summary = _load_json(root / "summary.json")
    input_root_matrix = _load_json(root / "input_root_matrix.json")
    dryrun_case_schema = _load_json(root / "dryrun_case_schema.json")
    simulated_frame_metadata_schema = _load_json(root / "simulated_frame_metadata_schema.json")
    frame_intake_decision_candidate_schema = _load_json(root / "frame_intake_decision_candidate_schema.json")
    frame_quality_decision_candidate_schema = _load_json(root / "frame_quality_decision_candidate_schema.json")
    frame_privacy_decision_candidate_schema = _load_json(root / "frame_privacy_decision_candidate_schema.json")
    frame_freshness_decision_candidate_schema = _load_json(root / "frame_freshness_decision_candidate_schema.json")
    frame_downstream_handoff_candidate_schema = _load_json(root / "frame_downstream_handoff_candidate_schema.json")
    controlled_frame_input_dryrun_result_schema = _load_json(root / "controlled_frame_input_dryrun_result_schema.json")
    dual_device_placeholder_dryrun_review = _load_json(root / "dual_device_placeholder_dryrun_review.json")
    controlled_frame_input_dryrun_scenario_matrix = _load_json(root / "controlled_frame_input_dryrun_scenario_matrix.json")
    controlled_frame_input_dryrun_results = _load_json(root / "controlled_frame_input_dryrun_results.json")
    controlled_frame_input_boundary_matrix = _load_json(root / "controlled_frame_input_boundary_matrix.json")
    governance_debt_register = _load_json(root / "governance_debt_register.json")
    next_phase_recommendation = _load_json(root / "next_phase_recommendation.json")
    no_runtime_boundary_report = _load_json(root / "no_runtime_boundary_report.json")
    no_write_boundary_report = _load_json(root / "no_write_boundary_report.json")

    rows = input_root_matrix.get("rows", [])
    idx = {row.get("intake_id"): row for row in rows}
    for intake_id in (
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
        "vision_frame_trace_stream_registry",
        "vision_frame_input_governance",
        "vision_roi_proposal_stub",
        "hardware_profile_capability_registry",
        "system_health_center_governance",
        "simulation_lab_profile",
    ):
        ok(f"input.{intake_id}.optional", idx.get(intake_id, {}).get("status") in {"loaded", "optional_missing"}, idx.get(intake_id, {}).get("status"))
    ok("input.row_count", input_root_matrix.get("row_count") == len(rows), input_root_matrix.get("row_count"))

    for key in (
        "controlled_frame_input_planning_input_loaded",
        "map_location_readonly_context_input_loaded",
        "post_vision_strengthening_roadmap_decision_input_loaded",
        "vision_strengthening_closure_input_loaded",
        "task_aware_visual_focus_input_loaded",
        "midplatform_perception_orchestration_input_loaded",
        "minimal_runtime_integration_closure_loaded",
        "ocr_final_closure_loaded",
        "dryrun_case_schema_defined",
        "simulated_frame_metadata_schema_defined",
        "frame_intake_decision_candidate_schema_defined",
        "frame_quality_decision_candidate_schema_defined",
        "frame_privacy_decision_candidate_schema_defined",
        "frame_freshness_decision_candidate_schema_defined",
        "frame_downstream_handoff_candidate_schema_defined",
        "controlled_frame_input_dryrun_result_schema_defined",
        "dual_device_placeholder_dryrun_review_generated",
        "scenario_matrix_generated",
        "dryrun_results_generated",
        "frame_to_ocr_requires_visual_focus",
        "frame_to_tracking_requires_visual_focus",
        "frame_to_world_observation_requires_policy",
        "privacy_tags_required_for_downstream",
        "source_chain_required",
        "timestamp_required",
        "stc_freshness_reuse_required",
        "dual_device_redundant_perception_placeholder_loaded",
        "hardware_stage_deferred",
        "no_runtime_executed",
        "no_new_runtime_enabled",
        "boundary_ok",
    ):
        ok(f"summary.{key}", summary.get(key) is True)
    ok("summary.dryrun_scope", summary.get("dryrun_scope") == "controlled_frame_input_dryrun_only")
    ok("summary.scenario_count", summary.get("scenario_count", 0) >= 14, summary.get("scenario_count"))
    ok("summary.accepted_candidate_count", summary.get("accepted_candidate_count", 0) >= 3, summary.get("accepted_candidate_count"))
    ok("summary.rejected_candidate_count", summary.get("rejected_candidate_count", 0) >= 5, summary.get("rejected_candidate_count"))
    ok("summary.restricted_candidate_count", summary.get("restricted_candidate_count", 0) >= 1, summary.get("restricted_candidate_count"))
    ok("summary.stale_archive_only_candidate_count", summary.get("stale_archive_only_candidate_count", 0) >= 1, summary.get("stale_archive_only_candidate_count"))
    for key in (
        "frame_to_navigation_action_allowed",
        "frame_to_speech_output_allowed",
        "frame_to_worldmodel_write_allowed",
        "frame_to_memory_write_allowed",
        "frame_to_fact_write_allowed",
        "live_camera_allowed",
        "device_camera_allowed",
        "external_stream_allowed",
        "dual_device_runtime_allowed",
        "dual_model_runtime_allowed",
        "failover_runtime_allowed",
        "automatic_hardware_switch_allowed",
        "multi_input_fusion_runtime_allowed",
        "frame_content_loaded",
        "actual_image_read",
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
    ):
        ok(f"summary.{key}", summary.get(key) is False)
    ok("summary.violations", summary.get("violations") == [])
    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)

    def fields(schema: Dict[str, Any]) -> List[str]:
        return [field.get("name") for field in schema.get("field_specs", [])]

    schema_expectations = {
        "dryrun_case_schema": (
            dryrun_case_schema,
            "ControlledFrameInputDryRunCase",
            [
                "dryrun_case_id",
                "case_type",
                "simulated_frame_source",
                "simulated_frame_metadata",
                "expected_intake_decision",
                "expected_quality_decision",
                "expected_privacy_decision",
                "expected_freshness_decision",
                "expected_downstream_handoff",
                "expected_boundary_flags",
                "source_chain",
            ],
        ),
        "simulated_frame_metadata_schema": (
            simulated_frame_metadata_schema,
            "SimulatedFrameMetadata",
            [
                "frame_id",
                "source_type",
                "source_origin",
                "frame_timestamp",
                "monotonic_seq",
                "source_chain",
                "privacy_tags",
                "task_context_ref",
                "location_context_ref",
                "pose_or_view_context_ref",
                "device_context_ref",
                "simulated_quality_profile",
                "freshness_profile",
                "ttl_policy_ref",
                "storage_policy_candidate",
                "frame_content_loaded",
                "actual_image_read",
                "visual_model_invoked",
            ],
        ),
        "frame_intake_decision_candidate_schema": (
            frame_intake_decision_candidate_schema,
            "FrameIntakeDecisionCandidate",
            [
                "intake_decision_id",
                "source_case_id",
                "frame_id",
                "intake_status",
                "accepted_for_downstream_candidate",
                "blocked_reason",
                "required_missing_fields",
                "live_runtime_blocked",
                "privacy_gate_required",
                "source_chain_valid",
                "timestamp_valid",
                "fact_status",
                "source_chain",
            ],
        ),
        "frame_quality_decision_candidate_schema": (
            frame_quality_decision_candidate_schema,
            "FrameQualityDecisionCandidate",
            [
                "quality_decision_id",
                "source_case_id",
                "frame_id",
                "quality_level",
                "scene_sketch_allowed_candidate",
                "visual_focus_allowed_candidate",
                "ocr_activation_allowed_candidate",
                "tracking_request_allowed_candidate",
                "world_observation_allowed_candidate",
                "active_view_adjustment_recommended",
                "safety_only_recommended",
                "reject_reason",
                "fact_status",
                "source_chain",
            ],
        ),
        "frame_privacy_decision_candidate_schema": (
            frame_privacy_decision_candidate_schema,
            "FramePrivacyDecisionCandidate",
            [
                "privacy_decision_id",
                "source_case_id",
                "frame_id",
                "privacy_tags_present",
                "privacy_risk_level",
                "downstream_allowed_candidate",
                "restricted_use_required",
                "long_term_storage_allowed",
                "worldmodel_handoff_allowed_candidate",
                "memory_handoff_allowed_candidate",
                "fact_status",
                "source_chain",
            ],
        ),
        "frame_freshness_decision_candidate_schema": (
            frame_freshness_decision_candidate_schema,
            "FrameFreshnessDecisionCandidate",
            [
                "freshness_decision_id",
                "source_case_id",
                "frame_id",
                "freshness_status",
                "ttl_policy_ref",
                "current_action_allowed",
                "archive_candidate_allowed",
                "stale_blocks_task_feedback",
                "expired_blocks_current_action",
                "fact_status",
                "source_chain",
            ],
        ),
        "frame_downstream_handoff_candidate_schema": (
            frame_downstream_handoff_candidate_schema,
            "FrameDownstreamHandoffCandidate",
            [
                "handoff_candidate_id",
                "source_case_id",
                "frame_id",
                "view_quality_candidate_allowed",
                "scene_sketch_input_allowed",
                "visual_focus_input_allowed",
                "ocr_activation_input_allowed",
                "tracking_request_input_allowed",
                "world_observation_input_allowed",
                "debug_review_artifact_allowed",
                "blocked_downstream_targets",
                "source_chain",
            ],
        ),
        "controlled_frame_input_dryrun_result_schema": (
            controlled_frame_input_dryrun_result_schema,
            "ControlledFrameInputDryRunResult",
            [
                "result_id",
                "source_case_id",
                "intake_decision_ref",
                "quality_decision_ref",
                "privacy_decision_ref",
                "freshness_decision_ref",
                "downstream_handoff_ref",
                "boundary_decision_ref",
                "dryrun_status",
                "violations",
                "source_chain",
            ],
        ),
    }
    for key, (schema, name, expected_fields) in schema_expectations.items():
        ok(f"{key}.schema_name", schema.get("schema_name") == name)
        ok(f"{key}.field_count", len(schema.get("field_specs", [])) >= len(expected_fields))
        field_names = fields(schema)
        for field_name in expected_fields:
            ok(f"{key}.field.{field_name}", field_name in field_names)

    ok("dual.review.loaded", dual_device_placeholder_dryrun_review.get("dual_device_placeholder_loaded") is True)
    for key in (
        "perception_input_channel_placeholder_present",
        "perception_device_health_placeholder_present",
        "perception_lane_failover_placeholder_present",
        "dual_input_consistency_placeholder_present",
        "hardware_stage_deferred",
    ):
        ok(f"dual.review.{key}", dual_device_placeholder_dryrun_review.get(key) is True)
    for key in (
        "dual_device_runtime_allowed",
        "dual_model_runtime_allowed",
        "failover_runtime_allowed",
        "automatic_hardware_switch_allowed",
        "multi_input_fusion_runtime_allowed",
    ):
        ok(f"dual.review.{key}", dual_device_placeholder_dryrun_review.get(key) is False)
    ok("dual.review.verdict", dual_device_placeholder_dryrun_review.get("verdict") == "GO")

    scenarios = controlled_frame_input_dryrun_scenario_matrix.get("scenarios", [])
    scenario_idx = {row.get("dryrun_case_id"): row for row in scenarios}
    scenario_names = {row.get("dryrun_case_id"): row.get("simulated_frame_source") for row in scenarios}
    ok("scenario.count", controlled_frame_input_dryrun_scenario_matrix.get("scenario_count") >= 14, controlled_frame_input_dryrun_scenario_matrix.get("scenario_count"))
    required_cases = {
        "case_static_test_image_good_quality": "static_test_image",
        "case_prerecorded_degraded_quality": "pre_recorded_video_frame",
        "case_simulation_frame_allowed": "simulation_frame",
        "case_controlled_uploaded_privacy_sensitive": "controlled_uploaded_frame",
        "case_missing_source_chain_rejected": "static_test_image",
        "case_missing_timestamp_rejected": "simulation_frame",
        "case_missing_privacy_tags_rejected": "controlled_uploaded_frame",
        "case_live_camera_attempt_blocked": "live_camera_placeholder",
        "case_device_camera_attempt_blocked": "device_camera_placeholder",
        "case_external_stream_attempt_blocked": "external_stream_placeholder",
        "case_stale_frame_archive_only": "archived_frame_candidate",
        "case_frame_with_text_requires_visual_focus_for_ocr": "static_test_image",
        "case_frame_with_motion_requires_visual_focus_for_tracking": "pre_recorded_video_frame",
        "case_dual_device_placeholder_review_only": "simulation_frame",
    }
    for case_id, source_type in required_cases.items():
        ok(f"scenario.{case_id}.present", case_id in scenario_idx)
        ok(f"scenario.{case_id}.source_type", scenario_idx.get(case_id, {}).get("simulated_frame_source") == source_type, scenario_names.get(case_id))

    for case_id in required_cases:
        row = scenario_idx.get(case_id, {})
        metadata = row.get("simulated_frame_metadata", {})
        ok(f"scenario.{case_id}.metadata.present", bool(metadata))
        ok(f"scenario.{case_id}.frame_content_loaded", metadata.get("frame_content_loaded") is False)
        ok(f"scenario.{case_id}.actual_image_read", metadata.get("actual_image_read") is False)
        ok(f"scenario.{case_id}.visual_model_invoked", metadata.get("visual_model_invoked") is False)
        ok(f"scenario.{case_id}.source_chain", row.get("source_chain") == "controlled_frame_input_dryrun_v1")

    results = controlled_frame_input_dryrun_results.get("results", [])
    intake_decisions = controlled_frame_input_dryrun_results.get("intake_decisions", [])
    quality_decisions = controlled_frame_input_dryrun_results.get("quality_decisions", [])
    privacy_decisions = controlled_frame_input_dryrun_results.get("privacy_decisions", [])
    freshness_decisions = controlled_frame_input_dryrun_results.get("freshness_decisions", [])
    downstream_handoffs = controlled_frame_input_dryrun_results.get("downstream_handoffs", [])
    result_idx = {row.get("source_case_id"): row for row in results}
    intake_idx = {row.get("source_case_id"): row for row in intake_decisions}
    quality_idx = {row.get("source_case_id"): row for row in quality_decisions}
    privacy_idx = {row.get("source_case_id"): row for row in privacy_decisions}
    freshness_idx = {row.get("source_case_id"): row for row in freshness_decisions}
    handoff_idx = {row.get("source_case_id"): row for row in downstream_handoffs}

    ok("results.count", controlled_frame_input_dryrun_results.get("result_count") == len(results), controlled_frame_input_dryrun_results.get("result_count"))
    ok("results.accepted_count", controlled_frame_input_dryrun_results.get("accepted_candidate_count", 0) >= 3)
    ok("results.rejected_count", controlled_frame_input_dryrun_results.get("rejected_candidate_count", 0) >= 5)
    ok("results.restricted_count", controlled_frame_input_dryrun_results.get("restricted_candidate_count", 0) >= 1)
    ok("results.archive_only_count", controlled_frame_input_dryrun_results.get("stale_archive_only_candidate_count", 0) >= 1)

    status_expectations = {
        "case_static_test_image_good_quality": "accepted_candidate",
        "case_prerecorded_degraded_quality": "accepted_candidate",
        "case_simulation_frame_allowed": "accepted_candidate",
        "case_controlled_uploaded_privacy_sensitive": "restricted_candidate",
        "case_missing_source_chain_rejected": "rejected_candidate",
        "case_missing_timestamp_rejected": "rejected_candidate",
        "case_missing_privacy_tags_rejected": "rejected_candidate",
        "case_live_camera_attempt_blocked": "rejected_candidate",
        "case_device_camera_attempt_blocked": "rejected_candidate",
        "case_external_stream_attempt_blocked": "rejected_candidate",
        "case_stale_frame_archive_only": "archive_only_candidate",
        "case_frame_with_text_requires_visual_focus_for_ocr": "accepted_candidate",
        "case_frame_with_motion_requires_visual_focus_for_tracking": "accepted_candidate",
        "case_dual_device_placeholder_review_only": "review_only_candidate",
    }
    for case_id, expected_status in status_expectations.items():
        ok(f"result.{case_id}.present", case_id in result_idx)
        ok(f"result.{case_id}.status", result_idx.get(case_id, {}).get("dryrun_status") == expected_status, result_idx.get(case_id, {}).get("dryrun_status"))
        ok(f"result.{case_id}.violations", result_idx.get(case_id, {}).get("violations") == [])

    intake_expectations = {
        "case_static_test_image_good_quality": "accepted_candidate",
        "case_prerecorded_degraded_quality": "accepted_candidate",
        "case_simulation_frame_allowed": "accepted_candidate",
        "case_controlled_uploaded_privacy_sensitive": "accepted_candidate",
        "case_missing_source_chain_rejected": "rejected_missing_source_chain",
        "case_missing_timestamp_rejected": "rejected_missing_timestamp",
        "case_missing_privacy_tags_rejected": "rejected_missing_privacy_tags",
        "case_live_camera_attempt_blocked": "rejected_live_camera",
        "case_device_camera_attempt_blocked": "rejected_device_camera",
        "case_external_stream_attempt_blocked": "rejected_external_stream",
        "case_stale_frame_archive_only": "accepted_candidate",
        "case_frame_with_text_requires_visual_focus_for_ocr": "accepted_candidate",
        "case_frame_with_motion_requires_visual_focus_for_tracking": "accepted_candidate",
        "case_dual_device_placeholder_review_only": "accepted_candidate",
    }
    for case_id, expected in intake_expectations.items():
        row = intake_idx.get(case_id, {})
        ok(f"intake.{case_id}.present", case_id in intake_idx)
        ok(f"intake.{case_id}.status", row.get("intake_status") == expected, row.get("intake_status"))
        ok(f"intake.{case_id}.privacy_gate_required", row.get("privacy_gate_required") is True)
        ok(f"intake.{case_id}.fact_status", row.get("fact_status") == "not_fact")
        ok(f"intake.{case_id}.source_chain", row.get("source_chain") == "controlled_frame_input_dryrun_v1")

    quality_expectations = {
        "case_static_test_image_good_quality": "GOOD",
        "case_prerecorded_degraded_quality": "DEGRADED",
        "case_simulation_frame_allowed": "GOOD",
        "case_controlled_uploaded_privacy_sensitive": "GOOD",
        "case_missing_source_chain_rejected": "BLOCKED",
        "case_missing_timestamp_rejected": "BLOCKED",
        "case_missing_privacy_tags_rejected": "BLOCKED",
        "case_live_camera_attempt_blocked": "BLOCKED",
        "case_device_camera_attempt_blocked": "BLOCKED",
        "case_external_stream_attempt_blocked": "BLOCKED",
        "case_stale_frame_archive_only": "GOOD",
        "case_frame_with_text_requires_visual_focus_for_ocr": "GOOD",
        "case_frame_with_motion_requires_visual_focus_for_tracking": "GOOD",
        "case_dual_device_placeholder_review_only": "UNKNOWN_MARKED",
    }
    for case_id, expected in quality_expectations.items():
        row = quality_idx.get(case_id, {})
        ok(f"quality.{case_id}.present", case_id in quality_idx)
        ok(f"quality.{case_id}.level", row.get("quality_level") == expected, row.get("quality_level"))
        ok(f"quality.{case_id}.fact_status", row.get("fact_status") == "not_fact")

    privacy_expectations = {
        "case_controlled_uploaded_privacy_sensitive": ("HIGH", False, True),
        "case_missing_privacy_tags_rejected": ("BLOCKED", False, False),
        "case_static_test_image_good_quality": ("MEDIUM", True, False),
        "case_simulation_frame_allowed": ("MEDIUM", True, False),
    }
    for case_id, (risk, allowed, restricted) in privacy_expectations.items():
        row = privacy_idx.get(case_id, {})
        ok(f"privacy.{case_id}.present", case_id in privacy_idx)
        ok(f"privacy.{case_id}.risk", row.get("privacy_risk_level") == risk, row.get("privacy_risk_level"))
        ok(f"privacy.{case_id}.downstream_allowed", row.get("downstream_allowed_candidate") is allowed)
        ok(f"privacy.{case_id}.restricted", row.get("restricted_use_required") is restricted)
        ok(f"privacy.{case_id}.long_term_storage_allowed", row.get("long_term_storage_allowed") is False)
        ok(f"privacy.{case_id}.worldmodel_handoff_allowed_candidate", row.get("worldmodel_handoff_allowed_candidate") is False)
        ok(f"privacy.{case_id}.memory_handoff_allowed_candidate", row.get("memory_handoff_allowed_candidate") is False)

    freshness_expectations = {
        "case_stale_frame_archive_only": ("expired", False, True, True, True),
        "case_static_test_image_good_quality": ("fresh", False, False, False, False),
        "case_prerecorded_degraded_quality": ("fresh", False, False, False, False),
    }
    for case_id, (status, current_allowed, archive_allowed, stale_blocks, expired_blocks) in freshness_expectations.items():
        row = freshness_idx.get(case_id, {})
        ok(f"freshness.{case_id}.present", case_id in freshness_idx)
        ok(f"freshness.{case_id}.status", row.get("freshness_status") == status, row.get("freshness_status"))
        ok(f"freshness.{case_id}.current_action_allowed", row.get("current_action_allowed") is current_allowed)
        ok(f"freshness.{case_id}.archive_allowed", row.get("archive_candidate_allowed") is archive_allowed)
        ok(f"freshness.{case_id}.stale_blocks", row.get("stale_blocks_task_feedback") is stale_blocks)
        ok(f"freshness.{case_id}.expired_blocks", row.get("expired_blocks_current_action") is expired_blocks)

    handoff_expectations = {
        "case_static_test_image_good_quality": (True, True, True, False, False, True),
        "case_prerecorded_degraded_quality": (True, True, True, False, False, True),
        "case_simulation_frame_allowed": (True, True, True, False, False, True),
        "case_controlled_uploaded_privacy_sensitive": (True, False, False, False, False, False),
        "case_stale_frame_archive_only": (True, False, False, False, False, False),
        "case_frame_with_text_requires_visual_focus_for_ocr": (True, True, True, True, False, True),
        "case_frame_with_motion_requires_visual_focus_for_tracking": (True, True, True, False, True, True),
    }
    for case_id, expected in handoff_expectations.items():
        row = handoff_idx.get(case_id, {})
        ok(f"handoff.{case_id}.present", case_id in handoff_idx)
        ok(f"handoff.{case_id}.view_quality", row.get("view_quality_candidate_allowed") is expected[0])
        ok(f"handoff.{case_id}.scene_sketch", row.get("scene_sketch_input_allowed") is expected[1])
        ok(f"handoff.{case_id}.visual_focus", row.get("visual_focus_input_allowed") is expected[2])
        ok(f"handoff.{case_id}.ocr", row.get("ocr_activation_input_allowed") is expected[3])
        ok(f"handoff.{case_id}.tracking", row.get("tracking_request_input_allowed") is expected[4])
        ok(f"handoff.{case_id}.world_obs", row.get("world_observation_input_allowed") is expected[5])

    for case_id in (
        "case_missing_source_chain_rejected",
        "case_missing_timestamp_rejected",
        "case_missing_privacy_tags_rejected",
        "case_live_camera_attempt_blocked",
        "case_device_camera_attempt_blocked",
        "case_external_stream_attempt_blocked",
    ):
        row = handoff_idx.get(case_id, {})
        ok(f"handoff.{case_id}.all_blocked.scene_sketch", row.get("scene_sketch_input_allowed") is False)
        ok(f"handoff.{case_id}.all_blocked.visual_focus", row.get("visual_focus_input_allowed") is False)
        ok(f"handoff.{case_id}.all_blocked.ocr", row.get("ocr_activation_input_allowed") is False)
        ok(f"handoff.{case_id}.all_blocked.tracking", row.get("tracking_request_input_allowed") is False)
        ok(f"handoff.{case_id}.all_blocked.world_obs", row.get("world_observation_input_allowed") is False)

    for key in (
        "frame_to_ocr_requires_visual_focus",
        "frame_to_tracking_requires_visual_focus",
        "frame_to_world_observation_requires_policy",
        "privacy_tags_required_for_downstream",
        "source_chain_required",
        "timestamp_required",
        "stc_freshness_reuse_required",
        "hardware_stage_deferred",
    ):
        ok(f"boundary.{key}", controlled_frame_input_boundary_matrix.get(key) is True)
    for key in (
        "frame_to_navigation_action_allowed",
        "frame_to_speech_output_allowed",
        "frame_to_worldmodel_write_allowed",
        "frame_to_memory_write_allowed",
        "frame_to_fact_write_allowed",
        "live_camera_allowed",
        "device_camera_allowed",
        "external_stream_allowed",
        "dual_device_runtime_allowed",
        "dual_model_runtime_allowed",
        "failover_runtime_allowed",
        "automatic_hardware_switch_allowed",
        "multi_input_fusion_runtime_allowed",
    ):
        ok(f"boundary.{key}", controlled_frame_input_boundary_matrix.get(key) is False)

    for report_name, report in (
        ("no_runtime_boundary_report", no_runtime_boundary_report),
        ("no_write_boundary_report", no_write_boundary_report),
    ):
        ok(f"{report_name}.dryrun_scope", report.get("dryrun_scope") == "controlled_frame_input_dryrun_only")
        for key in (
            "no_runtime_executed",
            "no_new_runtime_enabled",
            "boundary_ok",
        ):
            ok(f"{report_name}.{key}", report.get(key) is True)
        for key in (
            "frame_content_loaded",
            "actual_image_read",
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
        ):
            ok(f"{report_name}.{key}", report.get(key) is False)
        ok(f"{report_name}.violations", report.get("violations") == [])

    carryover_topics = governance_debt_register.get("carryover_topics", [])
    ok("governance.topic_count", len(carryover_topics) >= 10, len(carryover_topics))
    ok("governance.future_midplatform_function_governance_required", governance_debt_register.get("future_midplatform_function_governance_required") is True)
    ok("governance.no_duplicate_governance_module_allowed", governance_debt_register.get("no_duplicate_governance_module_allowed") is True)
    for topic in (
        "frame source trust calibration debt",
        "privacy tag completeness debt",
        "quality grade calibration debt",
        "stc and ttl reuse mapping debt",
        "simulation-to-real source gap debt",
        "midplatform frame ownership debt",
        "dual-device placeholder misuse risk",
    ):
        ok(f"governance.topic.{topic}", any(row.get("topic") == topic for row in carryover_topics))

    ok("next_phase.final_decision", next_phase_recommendation.get("final_decision") == FINAL_DECISION)
    ok("next_phase.recommended_next_phase", next_phase_recommendation.get("recommended_next_phase") == NEXT_PHASE)

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
    print(json.dumps({k: verifier_report[k] for k in ("verifier", "check_count", "passed_count", "failed_count", "final_decision", "recommended_next_phase")}, ensure_ascii=False))
    return 0 if verifier_report["verifier"] == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
