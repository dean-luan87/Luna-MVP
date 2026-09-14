#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Controlled Frame Input Post-DryRun Review v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

PHASE_ID = "Phase-Controlled-Frame-Input-Post-DryRun-Review-v1-001"
FINAL_DECISION = "CONTROLLED_FRAME_INPUT_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE"
NEXT_PHASE = "Phase-Controlled-Frame-Input-Closure-v1-001"
MIN_CHECKS = 180
BASELINE_REQUIREMENT = 140

REQUIRED_SCENARIOS = [
    "static_test_image_good_quality",
    "prerecorded_video_frame_degraded_quality",
    "simulation_frame_allowed",
    "controlled_uploaded_frame_privacy_sensitive",
    "missing_source_chain_rejected",
    "missing_timestamp_rejected",
    "missing_privacy_tags_rejected",
    "live_camera_attempt_blocked",
    "device_camera_attempt_blocked",
    "external_stream_attempt_blocked",
    "stale_frame_archive_only",
    "frame_with_text_requires_visual_focus_for_ocr",
    "frame_with_motion_requires_visual_focus_for_tracking",
    "dual_device_placeholder_review_only",
]


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-root", default="/Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/controlled_frame_input_post_dryrun_review_v1_smoke_v0")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    checks: List[Dict[str, Any]] = []

    def ok(check_id: str, passed: bool, detail: Any = None) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})

    summary = _load_json(root / "summary.json")
    input_root_matrix = _load_json(root / "input_root_matrix.json")
    controlled_frame_dryrun_input_root_review = _load_json(root / "controlled_frame_dryrun_input_root_review.json")
    controlled_frame_scenario_coverage_review = _load_json(root / "controlled_frame_scenario_coverage_review.json")
    frame_intake_gate_review = _load_json(root / "frame_intake_gate_review.json")
    frame_quality_gate_review = _load_json(root / "frame_quality_gate_review.json")
    frame_privacy_tagging_review = _load_json(root / "frame_privacy_tagging_review.json")
    frame_stc_freshness_review = _load_json(root / "frame_stc_freshness_review.json")
    frame_downstream_handoff_review = _load_json(root / "frame_downstream_handoff_review.json")
    dual_device_placeholder_review = _load_json(root / "dual_device_placeholder_review.json")
    runtime_write_action_speech_boundary_review = _load_json(root / "runtime_write_action_speech_boundary_review.json")
    controlled_frame_input_closure_readiness_decision = _load_json(root / "controlled_frame_input_closure_readiness_decision.json")
    governance_debt_review = _load_json(root / "governance_debt_review.json")
    next_phase_recommendation = _load_json(root / "next_phase_recommendation.json")
    no_runtime_boundary_report = _load_json(root / "no_runtime_boundary_report.json")
    no_write_boundary_report = _load_json(root / "no_write_boundary_report.json")

    rows = input_root_matrix.get("rows", [])
    idx = {row.get("intake_id"): row for row in rows}
    for intake_id in (
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
        "controlled_frame_input_dryrun_input_loaded",
        "controlled_frame_input_planning_input_loaded",
        "map_location_readonly_context_input_loaded",
        "post_vision_strengthening_roadmap_decision_input_loaded",
        "vision_strengthening_closure_input_loaded",
        "task_aware_visual_focus_input_loaded",
        "midplatform_perception_orchestration_input_loaded",
        "minimal_runtime_integration_closure_loaded",
        "ocr_final_closure_loaded",
        "input_root_review_generated",
        "scenario_coverage_review_generated",
        "frame_intake_gate_review_generated",
        "frame_quality_gate_review_generated",
        "frame_privacy_tagging_review_generated",
        "frame_stc_freshness_review_generated",
        "frame_downstream_handoff_review_generated",
        "dual_device_placeholder_review_generated",
        "runtime_write_action_speech_boundary_review_generated",
        "closure_readiness_decision_generated",
        "governance_debt_review_generated",
        "source_chain_required_verified",
        "timestamp_required_verified",
        "privacy_tags_required_verified",
        "live_camera_blocked_verified",
        "device_camera_blocked_verified",
        "external_stream_blocked_verified",
        "frame_to_ocr_requires_visual_focus",
        "frame_to_tracking_requires_visual_focus",
        "frame_to_world_observation_requires_policy",
        "dual_device_redundant_perception_placeholder_loaded",
        "hardware_stage_deferred",
        "no_runtime_boundary_pass",
        "no_write_boundary_pass",
        "no_action_boundary_pass",
        "no_speech_boundary_pass",
        "no_runtime_executed",
        "no_new_runtime_enabled",
        "boundary_ok",
    ):
        ok(f"summary.{key}", summary.get(key) is True)
    ok("summary.review_scope", summary.get("review_scope") == "controlled_frame_input_post_dryrun_review_only")
    ok("summary.reviewed_scenario_count", summary.get("reviewed_scenario_count", 0) >= 14, summary.get("reviewed_scenario_count"))
    ok("summary.accepted_candidate_count", summary.get("accepted_candidate_count", 0) >= 5, summary.get("accepted_candidate_count"))
    ok("summary.rejected_candidate_count", summary.get("rejected_candidate_count", 0) >= 6, summary.get("rejected_candidate_count"))
    ok("summary.restricted_candidate_count", summary.get("restricted_candidate_count", 0) >= 1, summary.get("restricted_candidate_count"))
    ok("summary.stale_archive_only_candidate_count", summary.get("stale_archive_only_candidate_count", 0) >= 1, summary.get("stale_archive_only_candidate_count"))
    for key in (
        "frame_to_navigation_action_allowed",
        "frame_to_speech_output_allowed",
        "frame_to_worldmodel_write_allowed",
        "frame_to_memory_write_allowed",
        "frame_to_fact_write_allowed",
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

    ok("root_review.review_id", controlled_frame_dryrun_input_root_review.get("review_id") == "cfippr_v1_001")
    ok("root_review.required_count", len(controlled_frame_dryrun_input_root_review.get("required_roots", [])) >= 9)
    ok("root_review.loaded_roots", len(controlled_frame_dryrun_input_root_review.get("loaded_roots", [])) >= 9)
    ok("root_review.optional_missing_list", isinstance(controlled_frame_dryrun_input_root_review.get("optional_missing_roots"), list))
    ok("root_review.missing_required_empty", controlled_frame_dryrun_input_root_review.get("missing_required_roots") == [])
    ok("root_review.status", controlled_frame_dryrun_input_root_review.get("input_root_status") == "all_required_loaded")
    ok("root_review.source_chain", controlled_frame_dryrun_input_root_review.get("source_chain") == "controlled_frame_input_post_dryrun_review_v1")

    ok("scenario_review.reviewed_count", controlled_frame_scenario_coverage_review.get("reviewed_scenario_count", 0) >= 14)
    ok("scenario_review.expected_count", controlled_frame_scenario_coverage_review.get("expected_scenario_count") == 14)
    ok("scenario_review.missing_empty", controlled_frame_scenario_coverage_review.get("missing_scenarios") == [])
    ok("scenario_review.allowed_present", controlled_frame_scenario_coverage_review.get("allowed_source_cases_present") is True)
    ok("scenario_review.rejected_present", controlled_frame_scenario_coverage_review.get("rejected_source_cases_present") is True)
    ok("scenario_review.restricted_present", controlled_frame_scenario_coverage_review.get("restricted_privacy_cases_present") is True)
    ok("scenario_review.stale_present", controlled_frame_scenario_coverage_review.get("stale_archive_only_cases_present") is True)
    ok("scenario_review.dual_present", controlled_frame_scenario_coverage_review.get("dual_device_placeholder_case_present") is True)
    ok("scenario_review.verdict", controlled_frame_scenario_coverage_review.get("verdict") == "GO")
    covered_scenarios = set(controlled_frame_scenario_coverage_review.get("covered_scenarios", []))
    for scenario_name in REQUIRED_SCENARIOS:
        ok(f"scenario_review.covered.{scenario_name}", scenario_name in covered_scenarios)

    ok("intake_review.accepted", frame_intake_gate_review.get("accepted_candidate_count", 0) >= 5)
    ok("intake_review.rejected", frame_intake_gate_review.get("rejected_candidate_count", 0) >= 6)
    ok("intake_review.restricted", frame_intake_gate_review.get("restricted_candidate_count", 0) >= 1)
    ok("intake_review.stale_archive_only", frame_intake_gate_review.get("stale_archive_only_candidate_count", 0) >= 1)
    for key in (
        "source_chain_required_verified",
        "timestamp_required_verified",
        "privacy_tags_required_verified",
        "live_camera_blocked_verified",
        "device_camera_blocked_verified",
        "external_stream_blocked_verified",
        "unknown_source_blocked_verified",
    ):
        ok(f"intake_review.{key}", frame_intake_gate_review.get(key) is True)
    ok("intake_review.verdict", frame_intake_gate_review.get("verdict") == "GO")

    quality_profiles = set(frame_quality_gate_review.get("quality_profiles_reviewed", []))
    for quality in ("GOOD", "DEGRADED", "BLOCKED", "UNKNOWN_MARKED"):
        ok(f"quality_review.profile.{quality}", quality in quality_profiles, sorted(quality_profiles))
    for key in (
        "good_quality_downstream_allowed_verified",
        "degraded_quality_downstream_limited_verified",
        "poor_or_blocked_degradation_verified",
        "active_view_adjustment_candidate_allowed_if_needed",
    ):
        ok(f"quality_review.{key}", frame_quality_gate_review.get(key) is True)
    ok("quality_review.quality_fact_written", frame_quality_gate_review.get("quality_fact_written") is False)
    ok("quality_review.verdict", frame_quality_gate_review.get("verdict") == "GO")

    for key in (
        "privacy_sensitive_case_reviewed",
        "privacy_tags_required_for_downstream",
        "restricted_use_verified",
        "long_term_write_blocked",
    ):
        ok(f"privacy_review.{key}", frame_privacy_tagging_review.get(key) is True)
    for key in ("face_identity_inference_allowed", "emotion_inference_allowed"):
        ok(f"privacy_review.{key}", frame_privacy_tagging_review.get(key) is False)
    ok("privacy_review.verdict", frame_privacy_tagging_review.get("verdict") == "GO")

    for key in (
        "timestamp_required",
        "monotonic_seq_reviewed",
        "stale_frame_reviewed",
        "expired_or_stale_current_action_blocked",
        "archive_candidate_allowed",
        "stc_freshness_reuse_required",
        "no_new_stc_module_created",
    ):
        ok(f"freshness_review.{key}", frame_stc_freshness_review.get(key) is True)
    ok("freshness_review.verdict", frame_stc_freshness_review.get("verdict") == "GO")

    for key in (
        "frame_to_view_quality_allowed_candidate",
        "frame_to_scene_sketch_allowed_candidate",
        "frame_to_visual_focus_allowed_candidate",
        "frame_to_ocr_requires_visual_focus",
        "frame_to_tracking_requires_visual_focus",
        "frame_to_world_observation_requires_policy",
    ):
        ok(f"handoff_review.{key}", frame_downstream_handoff_review.get(key) is True)
    for key in (
        "frame_to_navigation_action_allowed",
        "frame_to_speech_output_allowed",
        "frame_to_worldmodel_write_allowed",
        "frame_to_memory_write_allowed",
        "frame_to_fact_write_allowed",
    ):
        ok(f"handoff_review.{key}", frame_downstream_handoff_review.get(key) is False)
    ok("handoff_review.verdict", frame_downstream_handoff_review.get("verdict") == "GO")

    for key in (
        "dual_device_redundant_perception_placeholder_loaded",
        "perception_input_channel_placeholder_present",
        "perception_device_health_placeholder_present",
        "perception_lane_failover_placeholder_present",
        "dual_input_consistency_placeholder_present",
        "hardware_stage_deferred",
    ):
        ok(f"dual_review.{key}", dual_device_placeholder_review.get(key) is True)
    for key in (
        "dual_device_runtime_allowed",
        "dual_model_runtime_allowed",
        "failover_runtime_allowed",
        "automatic_hardware_switch_allowed",
        "multi_input_fusion_runtime_allowed",
    ):
        ok(f"dual_review.{key}", dual_device_placeholder_review.get(key) is False)
    ok("dual_review.verdict", dual_device_placeholder_review.get("verdict") == "GO")

    for key in (
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
        "scene_delta_generated",
        "world_model_written",
        "memory_written",
        "library_written",
        "fact_written",
    ):
        ok(f"boundary_review.{key}", runtime_write_action_speech_boundary_review.get(key) is False)
    ok("boundary_review.verdict", runtime_write_action_speech_boundary_review.get("verdict") == "GO")

    ok("closure_readiness.verdict", controlled_frame_input_closure_readiness_decision.get("post_dryrun_review_verdict") == "GO")
    ok("closure_readiness.blockers", controlled_frame_input_closure_readiness_decision.get("blockers") == [])
    ok("closure_readiness.notes", len(controlled_frame_input_closure_readiness_decision.get("conditional_notes", [])) >= 2)
    ok("closure_readiness.ready_for_closure", controlled_frame_input_closure_readiness_decision.get("ready_for_closure") is True)
    ok("closure_readiness.ready_for_controlled_sample_planning", controlled_frame_input_closure_readiness_decision.get("ready_for_controlled_sample_planning") is False)
    ok("closure_readiness.next_phase", controlled_frame_input_closure_readiness_decision.get("recommended_next_phase") == NEXT_PHASE)
    ok("closure_readiness.final_decision", controlled_frame_input_closure_readiness_decision.get("final_decision") == FINAL_DECISION)

    ok("governance.review_id", controlled_frame_dryrun_input_root_review.get("review_id") == "cfippr_v1_001")
    ok("governance.future_midplatform_function_governance_required", governance_debt_review.get("future_midplatform_function_governance_required") is True)
    ok("governance.no_duplicate_governance_module_allowed", governance_debt_review.get("no_duplicate_governance_module_allowed") is True)
    ok("governance.carryover_count", len(governance_debt_review.get("carryover_topics", [])) >= 5, len(governance_debt_review.get("carryover_topics", [])))
    ok("governance.review_notes", len(governance_debt_review.get("review_notes", [])) >= 3)

    ok("next_phase.final_decision", next_phase_recommendation.get("final_decision") == FINAL_DECISION)
    ok("next_phase.recommended_next_phase", next_phase_recommendation.get("recommended_next_phase") == NEXT_PHASE)

    for report_name, report in (
        ("no_runtime_boundary_report", no_runtime_boundary_report),
        ("no_write_boundary_report", no_write_boundary_report),
    ):
        ok(f"{report_name}.review_scope", report.get("review_scope") == "controlled_frame_input_post_dryrun_review_only")
        for key in (
            "review_only",
            "no_runtime_boundary_pass",
            "no_write_boundary_pass",
            "no_action_boundary_pass",
            "no_speech_boundary_pass",
            "no_runtime_executed",
            "no_new_runtime_enabled",
            "boundary_ok",
        ):
            ok(f"{report_name}.{key}", report.get(key) is True)
        for key in (
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
    print(json.dumps({k: verifier_report[k] for k in ("verifier", "check_count", "passed_count", "failed_count", "final_decision", "recommended_next_phase")}, ensure_ascii=False))
    return 0 if verifier_report["verifier"] == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
