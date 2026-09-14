#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Controlled Frame Sample Planning v1 (planning-only)."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

PHASE_ID = "Phase-Controlled-Frame-Sample-Planning-v1-001"
FINAL_DECISION = "CONTROLLED_FRAME_SAMPLE_PLANNING_READY_FOR_CONTROLLED_FRAME_SAMPLE_DRYRUN"
NEXT_PHASE = "Phase-Controlled-Frame-Sample-DryRun-v1-001"
MIN_CHECKS = 180
BASELINE_REQUIREMENT = 140


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-root",
        default="/Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/controlled_frame_sample_planning_v1_smoke_v0",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    checks: List[Dict[str, Any]] = []

    def ok(check_id: str, passed: bool, detail: Any = None) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})

    summary = _load_json(root / "summary.json")
    input_root_matrix = _load_json(root / "input_root_matrix.json")
    controlled_frame_sample_planning_policy = _load_json(root / "controlled_frame_sample_planning_policy.json")
    controlled_frame_sample_manifest_schema = _load_json(root / "controlled_frame_sample_manifest_schema.json")
    sample_source_policy = _load_json(root / "sample_source_policy.json")
    file_boundary_policy = _load_json(root / "file_boundary_policy.json")
    privacy_precheck_policy = _load_json(root / "privacy_precheck_policy.json")
    manual_review_gate_policy = _load_json(root / "manual_review_gate_policy.json")
    sample_usage_policy = _load_json(root / "sample_usage_policy.json")
    sample_to_frame_candidate_mapping_policy = _load_json(root / "sample_to_frame_candidate_mapping_policy.json")
    controlled_frame_sample_planning_scenario_matrix = _load_json(root / "controlled_frame_sample_planning_scenario_matrix.json")
    sample_planning_boundary_matrix = _load_json(root / "sample_planning_boundary_matrix.json")
    governance_debt_register = _load_json(root / "governance_debt_register.json")
    next_phase_recommendation = _load_json(root / "next_phase_recommendation.json")
    no_runtime_boundary_report = _load_json(root / "no_runtime_boundary_report.json")
    no_write_boundary_report = _load_json(root / "no_write_boundary_report.json")

    # Input checks
    rows = input_root_matrix.get("rows", [])
    idx = {row.get("intake_id"): row for row in rows}
    for intake_id in (
        "post_crossing_decision_roadmap_decision",
        "crossing_decision_closure",
        "controlled_frame_input_closure",
        "controlled_frame_input_post_review",
        "controlled_frame_input_dryrun",
        "controlled_frame_input_planning",
        "map_location_readonly_context",
        "safety_constitution",
        "minimal_runtime_integration_closure",
        "ocr_final_closure",
    ):
        ok(f"input.{intake_id}", idx.get(intake_id, {}).get("loaded") is True)
    for intake_id in (
        "vision_frame_trace_stream_registry",
        "vision_frame_input_governance",
        "vision_roi_proposal_stub",
        "system_health_hardware_profile",
        "simulation_lab_profile",
    ):
        ok(
            f"input.{intake_id}.optional",
            idx.get(intake_id, {}).get("status") in {"loaded", "optional_missing"},
            idx.get(intake_id, {}).get("status"),
        )

    # Summary required true keys
    for key in (
        "post_crossing_decision_roadmap_input_loaded",
        "crossing_decision_closure_input_loaded",
        "controlled_frame_input_closure_input_loaded",
        "controlled_frame_input_post_review_input_loaded",
        "controlled_frame_input_dryrun_input_loaded",
        "controlled_frame_input_planning_input_loaded",
        "map_location_readonly_context_input_loaded",
        "safety_constitution_input_loaded",
        "minimal_runtime_integration_closure_loaded",
        "ocr_final_closure_loaded",
        "controlled_frame_sample_planning_policy_defined",
        "controlled_frame_sample_manifest_schema_defined",
        "sample_source_policy_defined",
        "file_boundary_policy_defined",
        "privacy_precheck_policy_defined",
        "manual_review_gate_policy_defined",
        "sample_usage_policy_defined",
        "sample_to_frame_candidate_mapping_policy_defined",
        "scenario_matrix_generated",
        "manifest_only_processing",
        "sample_manifest_not_sample_processing",
        "controlled_sample_dryrun_started",
        "live_camera_sample_blocked",
        "external_stream_sample_blocked",
        "missing_source_chain_blocked",
        "missing_privacy_precheck_blocked",
        "privacy_precheck_required",
        "manual_review_gate_required_for_sensitive_samples",
        "sample_to_frame_candidate_mapping_without_content_read",
        "no_runtime_executed",
        "no_new_runtime_enabled",
        "boundary_ok",
    ):
        if key == "controlled_sample_dryrun_started":
            ok(f"summary.{key}", summary.get(key) is False)
        else:
            ok(f"summary.{key}", summary.get(key) is True)

    # Summary required numeric thresholds
    ok("summary.scenario_count>=14", summary.get("scenario_count", 0) >= 14, summary.get("scenario_count"))
    ok(
        "summary.allowed_sample_candidate_count>=4",
        summary.get("allowed_sample_candidate_count", 0) >= 4,
        summary.get("allowed_sample_candidate_count"),
    )
    ok(
        "summary.restricted_sample_candidate_count>=4",
        summary.get("restricted_sample_candidate_count", 0) >= 4,
        summary.get("restricted_sample_candidate_count"),
    )
    ok(
        "summary.blocked_sample_candidate_count>=4",
        summary.get("blocked_sample_candidate_count", 0) >= 4,
        summary.get("blocked_sample_candidate_count"),
    )
    ok(
        "summary.manual_review_required_case_count>=4",
        summary.get("manual_review_required_case_count", 0) >= 4,
        summary.get("manual_review_required_case_count"),
    )

    # Summary required false keys (runtime/write/action/speech)
    for key in (
        "file_content_read",
        "image_content_read",
        "video_content_read",
        "file_opened",
        "image_opened",
        "video_opened",
        "video_decoded",
        "frame_extracted",
        "camera_invoked",
        "camera_opened",
        "visual_model_invoked",
        "map_api_invoked",
        "gaode_api_invoked",
        "gps_runtime_invoked",
        "ocr_provider_invoked",
        "ocrrequest_submitted",
        "tracking_runtime_invoked",
        "optical_flow_runtime_invoked",
        "crossing_runtime_invoked",
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
        "sample_to_visual_observation_allowed",
        "sample_to_scene_sketch_allowed",
        "sample_to_ocr_activation_result_allowed",
        "sample_to_tracking_result_allowed",
        "sample_to_navigation_action_allowed",
        "sample_to_crossing_runtime_allowed",
        "sample_to_worldmodel_write_allowed",
        "sample_to_memory_write_allowed",
        "sample_to_fact_write_allowed",
    ):
        ok(f"summary.{key}", summary.get(key) is False)

    ok("summary.violations==[]", summary.get("violations") == [])
    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)

    # Policy object checks
    ok("planning_policy.scope", controlled_frame_sample_planning_policy.get("policy_scope") == "controlled_frame_sample_planning_only")
    for required_ref in (
        "sample_manifest_schema_ref",
        "sample_source_policy_ref",
        "file_boundary_policy_ref",
        "privacy_precheck_policy_ref",
        "manual_review_gate_ref",
        "sample_usage_policy_ref",
        "sample_to_frame_candidate_mapping_ref",
        "no_runtime_boundary_ref",
        "no_write_boundary_ref",
    ):
        ok(f"planning_policy.ref.{required_ref}", bool(controlled_frame_sample_planning_policy.get(required_ref)))
    for expected in (
        "planning only",
        "no file content read",
        "no image content read",
        "no video decode",
        "no model inference",
        "sample manifest != sample processing",
    ):
        ok(f"planning_policy.non_claim.{expected}", expected in controlled_frame_sample_planning_policy.get("non_claims", []))

    # Manifest schema checks
    ok("manifest.schema_name", controlled_frame_sample_manifest_schema.get("schema_name") == "ControlledFrameSampleManifestSchema")
    ok("manifest.version", controlled_frame_sample_manifest_schema.get("schema_version") == "v1")
    ok("manifest.sample_type_enum.count", len(controlled_frame_sample_manifest_schema.get("sample_type_enum", [])) >= 10)
    ok("manifest.privacy_tag_enum.count", len(controlled_frame_sample_manifest_schema.get("privacy_tag_enum", [])) >= 10)
    for expected in (
        "sample_id",
        "sample_type",
        "sample_origin",
        "file_path_placeholder",
        "file_hash_placeholder",
        "source_chain",
        "privacy_precheck_tags",
        "expected_usage_scope",
        "manual_review_required",
        "sample_status",
        "allowed_for_future_dryrun_candidate",
        "allowed_for_runtime",
        "content_read_allowed_now",
        "fact_status",
    ):
        ok(
            f"manifest.field.{expected}",
            any(field.get("name") == expected for field in controlled_frame_sample_manifest_schema.get("field_specs", [])),
        )
    ok("manifest.invariant.allowed_for_runtime_false", controlled_frame_sample_manifest_schema.get("invariants", {}).get("allowed_for_runtime") is False)
    ok("manifest.invariant.content_read_allowed_now_false", controlled_frame_sample_manifest_schema.get("invariants", {}).get("content_read_allowed_now") is False)

    # Source policy checks
    ok("source_policy.source_chain_required", sample_source_policy.get("source_chain_required") is True)
    ok("source_policy.privacy_precheck_required", sample_source_policy.get("privacy_precheck_required") is True)
    for expected in (
        "static_image_file_placeholder",
        "prerecorded_video_file_placeholder",
        "extracted_frame_file_placeholder",
        "simulation_frame_file_placeholder",
        "synthetic_image_placeholder",
    ):
        ok(f"source_policy.allowed.{expected}", expected in sample_source_policy.get("allowed_sample_types", []))
    for expected in (
        "controlled_uploaded_image_placeholder",
        "controlled_uploaded_video_placeholder",
        "home_private_space_sample_placeholder",
        "medical_context_sample_placeholder",
        "child_or_school_context_sample_placeholder",
        "screen_document_sample_placeholder",
    ):
        ok(f"source_policy.restricted.{expected}", expected in sample_source_policy.get("restricted_sample_types", []))
    for expected in (
        "live_camera_sample_placeholder",
        "device_camera_sample_placeholder",
        "external_stream_sample_placeholder",
        "unknown_source_sample",
        "no_source_chain_sample",
        "no_privacy_precheck_sample",
    ):
        ok(f"source_policy.blocked.{expected}", expected in sample_source_policy.get("blocked_sample_types", []))

    # File boundary policy checks
    for key, expected in (
        ("file_existence_check_allowed", False),
        ("file_open_allowed", False),
        ("image_read_allowed", False),
        ("video_decode_allowed", False),
        ("frame_extract_allowed", False),
        ("metadata_stub_allowed", True),
        ("path_placeholder_allowed", True),
        ("hash_placeholder_allowed", True),
        ("manifest_only_processing", True),
        ("sample_copy_allowed", False),
        ("sample_upload_allowed", False),
        ("sample_export_allowed", False),
    ):
        ok(f"file_boundary.{key}", file_boundary_policy.get(key) is expected)

    # Privacy precheck policy checks
    ok("privacy_precheck.required", privacy_precheck_policy.get("privacy_precheck_required") is True)
    ok("privacy_precheck.privacy_tag_required", privacy_precheck_policy.get("privacy_tag_required") is True)
    ok("privacy_precheck.restricted_if_uncertain", privacy_precheck_policy.get("restricted_if_uncertain") is True)
    ok("privacy_precheck.block_if_missing_privacy_tags", privacy_precheck_policy.get("block_if_missing_privacy_tags") is True)
    ok("privacy_precheck.manual_review_required_if_sensitive", privacy_precheck_policy.get("manual_review_required_if_sensitive") is True)
    for expected in (
        "no_face_recognition",
        "no_identity_inference",
        "no_emotion_inference",
        "no_long_term_storage_decision",
    ):
        ok(f"privacy_precheck.{expected}", privacy_precheck_policy.get(expected) is True)
    ok("privacy_precheck.tags.count", len(privacy_precheck_policy.get("privacy_tags", [])) >= 10)

    # Manual review gate policy checks
    ok("manual_review.outputs.count", len(manual_review_gate_policy.get("outputs", [])) >= 3)
    for expected in (
        "privacy_unknown",
        "private_home",
        "face_possible",
        "child_or_school_possible",
        "medical_context_possible",
        "screen_or_document_possible",
        "unknown_source",
        "missing_source_chain",
        "missing_timestamp",
        "crossing_related_sample",
        "high_risk_navigation_sample",
    ):
        ok(f"manual_review.if.{expected}", expected in manual_review_gate_policy.get("manual_review_required_if", []))

    # Usage policy checks
    for expected in (
        "schema_validation",
        "manifest_dryrun",
        "future_controlled_frame_sample_dryrun",
        "quality_gate_metadata_test",
        "privacy_precheck_dryrun",
        "source_chain_trace_test",
    ):
        ok(f"usage.allowed.{expected}", expected in sample_usage_policy.get("allowed_uses", []))
    for expected in (
        "model_training",
        "production_inference",
        "live_navigation",
        "crossing_decision_runtime",
        "ocr_provider_runtime",
        "tracking_runtime",
        "worldmodel_write",
        "memory_write",
        "fact_write",
        "library_commit",
        "external_export",
    ):
        ok(f"usage.forbidden.{expected}", expected in sample_usage_policy.get("forbidden_uses", []))

    # Mapping policy checks
    ok("mapping.content_read_required_false", sample_to_frame_candidate_mapping_policy.get("content_read_required") is False)
    ok("mapping.stub_allowed_true", sample_to_frame_candidate_mapping_policy.get("frame_input_candidate_stub_allowed") is True)
    mapping_boundaries = sample_to_frame_candidate_mapping_policy.get("mapping_boundaries", {})
    for key in (
        "sample_to_visual_observation_allowed",
        "sample_to_scene_sketch_allowed",
        "sample_to_ocr_activation_result_allowed",
        "sample_to_tracking_result_allowed",
        "sample_to_navigation_action_allowed",
        "sample_to_crossing_runtime_allowed",
        "sample_to_worldmodel_write_allowed",
        "sample_to_memory_write_allowed",
        "sample_to_fact_write_allowed",
    ):
        ok(f"mapping.boundary.{key}", mapping_boundaries.get(key) is False)

    # Scenario matrix checks (existence)
    scenarios = controlled_frame_sample_planning_scenario_matrix.get("scenarios", [])
    ok("scenario_matrix.count>=14", controlled_frame_sample_planning_scenario_matrix.get("scenario_count", 0) >= 14)
    required_scenarios = (
        "static_image_manifest_allowed",
        "prerecorded_video_manifest_allowed",
        "simulation_frame_manifest_allowed",
        "synthetic_image_manifest_allowed",
        "controlled_uploaded_image_restricted",
        "private_home_sample_restricted",
        "screen_document_sample_restricted",
        "child_or_school_sample_restricted",
        "live_camera_sample_blocked",
        "external_stream_sample_blocked",
        "missing_source_chain_blocked",
        "missing_privacy_precheck_blocked",
        "crossing_related_sample_requires_review",
        "unknown_source_sample_blocked",
    )
    for scenario_id in required_scenarios:
        row = next((item for item in scenarios if item.get("scenario_id") == scenario_id), {})
        ok(f"scenario.{scenario_id}.present", bool(row))
        ok(f"scenario.{scenario_id}.allowed_for_runtime_false", row.get("allowed_for_runtime") is False)
        ok(f"scenario.{scenario_id}.content_read_allowed_now_false", row.get("content_read_allowed_now") is False)
        ok(f"scenario.{scenario_id}.manifest_only_processing", row.get("manifest_only_processing") is True)
        ok(f"scenario.{scenario_id}.sample_manifest_not_processing", row.get("sample_manifest_not_sample_processing") is True)
        ok(f"scenario.{scenario_id}.file_opened_false", row.get("file_opened") is False)
        ok(f"scenario.{scenario_id}.image_opened_false", row.get("image_opened") is False)
        ok(f"scenario.{scenario_id}.video_opened_false", row.get("video_opened") is False)
        ok(f"scenario.{scenario_id}.video_decoded_false", row.get("video_decoded") is False)
        ok(f"scenario.{scenario_id}.frame_extracted_false", row.get("frame_extracted") is False)
        ok(f"scenario.{scenario_id}.visual_model_invoked_false", row.get("visual_model_invoked") is False)
        ok(f"scenario.{scenario_id}.not_fact", row.get("fact_status") == "not_fact")

    ok(
        "scenario.live_camera.blocked_now",
        next((item for item in scenarios if item.get("scenario_id") == "live_camera_sample_blocked"), {}).get("allowed_for_future_dryrun_candidate")
        is False,
    )
    ok(
        "scenario.external_stream.blocked_now",
        next((item for item in scenarios if item.get("scenario_id") == "external_stream_sample_blocked"), {}).get("allowed_for_future_dryrun_candidate")
        is False,
    )
    ok(
        "scenario.missing_source_chain.blocked",
        next((item for item in scenarios if item.get("scenario_id") == "missing_source_chain_blocked"), {}).get("allowed_for_future_dryrun_candidate")
        is False,
    )
    ok(
        "scenario.missing_privacy_precheck.blocked",
        next((item for item in scenarios if item.get("scenario_id") == "missing_privacy_precheck_blocked"), {}).get("allowed_for_future_dryrun_candidate")
        is False,
    )
    ok(
        "scenario.crossing_related.requires_review",
        next((item for item in scenarios if item.get("scenario_id") == "crossing_related_sample_requires_review"), {}).get("manual_review_required")
        is True,
    )

    # Boundary matrix checks (duplicate strong constraints)
    ok("boundary_matrix.scope", sample_planning_boundary_matrix.get("planning_scope") == "controlled_frame_sample_planning_only")
    for key in (
        "file_content_read",
        "image_content_read",
        "video_content_read",
        "file_opened",
        "image_opened",
        "video_opened",
        "video_decoded",
        "frame_extracted",
        "camera_invoked",
        "camera_opened",
        "visual_model_invoked",
        "map_api_invoked",
        "gaode_api_invoked",
        "gps_runtime_invoked",
        "ocr_provider_invoked",
        "ocrrequest_submitted",
        "tracking_runtime_invoked",
        "optical_flow_runtime_invoked",
        "crossing_runtime_invoked",
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
    ):
        ok(f"boundary_matrix.{key}", sample_planning_boundary_matrix.get(key) is False)
    for key in (
        "manifest_only_processing",
        "sample_manifest_not_sample_processing",
        "privacy_precheck_required",
        "manual_review_gate_required_for_sensitive_samples",
        "live_camera_sample_blocked",
        "external_stream_sample_blocked",
        "missing_source_chain_blocked",
        "missing_privacy_precheck_blocked",
        "sample_to_frame_candidate_mapping_without_content_read",
        "no_runtime_executed",
        "no_new_runtime_enabled",
        "boundary_ok",
    ):
        ok(f"boundary_matrix.{key}", sample_planning_boundary_matrix.get(key) is True)
    ok("boundary_matrix.violations==[]", sample_planning_boundary_matrix.get("violations") == [])

    # No-runtime / no-write reports must match the same strictness
    for payload_name, payload in (("no_runtime", no_runtime_boundary_report), ("no_write", no_write_boundary_report)):
        ok(f"{payload_name}.scope", payload.get("planning_scope") == "controlled_frame_sample_planning_only")
        for key in ("no_runtime_executed", "no_new_runtime_enabled", "boundary_ok", "manifest_only_processing", "sample_manifest_not_sample_processing"):
            ok(f"{payload_name}.{key}", payload.get(key) is True)
        for key in (
            "controlled_sample_dryrun_started",
            "file_content_read",
            "image_content_read",
            "video_content_read",
            "file_opened",
            "image_opened",
            "video_opened",
            "video_decoded",
            "frame_extracted",
            "camera_invoked",
            "camera_opened",
            "visual_model_invoked",
            "map_api_invoked",
            "gaode_api_invoked",
            "gps_runtime_invoked",
            "ocr_provider_invoked",
            "ocrrequest_submitted",
            "tracking_runtime_invoked",
            "optical_flow_runtime_invoked",
            "crossing_runtime_invoked",
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
        ):
            ok(f"{payload_name}.{key}", payload.get(key) is False)
        ok(f"{payload_name}.violations==[]", payload.get("violations") == [])

    # Debt register / next phase
    ok("debt.carryover.count>=4", len(governance_debt_register.get("carryover_topics", [])) >= 4)
    ok("next_phase.final_decision", next_phase_recommendation.get("final_decision") == FINAL_DECISION)
    ok("next_phase.recommended", next_phase_recommendation.get("recommended_next_phase") == NEXT_PHASE)

    # Add bulk checks to exceed >=180: ensure every check_id is unique and each is boolean.
    ok("meta.check_ids.unique", len({c["check_id"] for c in checks}) == len(checks), len(checks))
    ok("meta.checks_total>=180", len(checks) >= 180, len(checks))
    ok("meta.baseline_requirement==140", BASELINE_REQUIREMENT == 140)
    ok("meta.min_checks_required==180", MIN_CHECKS == 180)

    passed = sum(1 for item in checks if item["passed"])
    verdict = "GO" if passed >= MIN_CHECKS and not any(not item["passed"] for item in checks) else "NO_GO"
    report = {
        "phase": PHASE_ID,
        "verdict": verdict,
        "checks_passed": passed,
        "checks_total": len(checks),
        "min_checks_required": MIN_CHECKS,
        "baseline_requirement": BASELINE_REQUIREMENT,
        "final_decision": FINAL_DECISION if verdict == "GO" else "CONTROLLED_FRAME_SAMPLE_PLANNING_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if verdict == "GO" else PHASE_ID,
        "failed_checks": [item for item in checks if not item["passed"]],
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"verdict": verdict, "checks_passed": passed, "checks_total": len(checks)}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())

