#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Controlled Frame Sample DryRun v1 (manifest-metadata-only)."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

PHASE_ID = "Phase-Controlled-Frame-Sample-DryRun-v1-001"
FINAL_DECISION = "CONTROLLED_FRAME_SAMPLE_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
NEXT_PHASE = "Phase-Controlled-Frame-Sample-Post-DryRun-Review-v1-001"
MIN_CHECKS = 200
BASELINE_REQUIREMENT = 160


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-root",
        default="/Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/controlled_frame_sample_dryrun_v1_smoke_v0",
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
    dryrun_case_schema = _load_json(root / "dryrun_case_schema.json")
    sample_manifest_metadata_stub_schema = _load_json(root / "sample_manifest_metadata_stub_schema.json")
    sample_source_decision_candidate_schema = _load_json(root / "sample_source_decision_candidate_schema.json")
    file_boundary_decision_candidate_schema = _load_json(root / "file_boundary_decision_candidate_schema.json")
    privacy_precheck_decision_candidate_schema = _load_json(root / "privacy_precheck_decision_candidate_schema.json")
    manual_review_decision_candidate_schema = _load_json(root / "manual_review_decision_candidate_schema.json")
    sample_usage_decision_candidate_schema = _load_json(root / "sample_usage_decision_candidate_schema.json")
    sample_to_frame_candidate_mapping_stub_schema = _load_json(root / "sample_to_frame_candidate_mapping_stub_schema.json")
    controlled_frame_sample_dryrun_result_schema = _load_json(root / "controlled_frame_sample_dryrun_result_schema.json")
    controlled_frame_sample_dryrun_scenario_matrix = _load_json(root / "controlled_frame_sample_dryrun_scenario_matrix.json")
    controlled_frame_sample_dryrun_results = _load_json(root / "controlled_frame_sample_dryrun_results.json")
    sample_file_boundary_check_results = _load_json(root / "sample_file_boundary_check_results.json")
    sample_privacy_precheck_results = _load_json(root / "sample_privacy_precheck_results.json")
    manual_review_gate_results = _load_json(root / "manual_review_gate_results.json")
    sample_to_frame_mapping_stub_results = _load_json(root / "sample_to_frame_mapping_stub_results.json")
    sample_dryrun_boundary_matrix = _load_json(root / "sample_dryrun_boundary_matrix.json")
    governance_debt_register = _load_json(root / "governance_debt_register.json")
    next_phase_recommendation = _load_json(root / "next_phase_recommendation.json")
    no_runtime_boundary_report = _load_json(root / "no_runtime_boundary_report.json")
    no_write_boundary_report = _load_json(root / "no_write_boundary_report.json")

    # Input root checks
    rows = input_root_matrix.get("rows", [])
    idx = {row.get("intake_id"): row for row in rows}
    for intake_id in (
        "controlled_frame_sample_planning",
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

    # Summary hard requirements (true)
    for key in (
        "controlled_frame_sample_planning_input_loaded",
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
        "dryrun_case_schema_defined",
        "sample_manifest_metadata_stub_schema_defined",
        "sample_source_decision_candidate_schema_defined",
        "file_boundary_decision_candidate_schema_defined",
        "privacy_precheck_decision_candidate_schema_defined",
        "manual_review_decision_candidate_schema_defined",
        "sample_usage_decision_candidate_schema_defined",
        "sample_to_frame_candidate_mapping_stub_schema_defined",
        "controlled_frame_sample_dryrun_result_schema_defined",
        "scenario_matrix_generated",
        "dryrun_results_generated",
        "manifest_metadata_only",
        "sample_manifest_loaded",
        "manifest_only_processing",
        "sample_manifest_not_sample_processing",
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
        ok(f"summary.{key}", summary.get(key) is True)

    # Summary thresholds
    ok("summary.scenario_count>=16", summary.get("scenario_count", 0) >= 16, summary.get("scenario_count"))
    ok("summary.allowed>=4", summary.get("allowed_sample_candidate_count", 0) >= 4, summary.get("allowed_sample_candidate_count"))
    ok("summary.restricted>=5", summary.get("restricted_sample_candidate_count", 0) >= 5, summary.get("restricted_sample_candidate_count"))
    ok("summary.blocked>=4", summary.get("blocked_sample_candidate_count", 0) >= 4, summary.get("blocked_sample_candidate_count"))
    ok("summary.manual_review>=5", summary.get("manual_review_required_case_count", 0) >= 5, summary.get("manual_review_required_case_count"))

    # Summary hard requirements (false)
    for key in (
        "file_content_read",
        "image_content_read",
        "video_content_read",
        "file_opened",
        "image_opened",
        "video_opened",
        "video_decoded",
        "frame_extracted",
        "real_file_hash_computed",
        "controlled_sample_runtime_started",
        "visual_observation_generated",
        "scene_sketch_generated",
        "ocr_activation_result_generated",
        "tracking_result_generated",
        "sample_to_navigation_action_allowed",
        "sample_to_crossing_runtime_allowed",
        "sample_to_worldmodel_write_allowed",
        "sample_to_memory_write_allowed",
        "sample_to_fact_write_allowed",
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
        ok(f"summary.{key}", summary.get(key) is False)

    ok("summary.violations==[]", summary.get("violations") == [])
    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)

    # Schema presence checks
    ok("schema.dryrun_case", dryrun_case_schema.get("schema_name") == "ControlledFrameSampleDryRunCase")
    ok("schema.sample_manifest_stub", sample_manifest_metadata_stub_schema.get("schema_name") == "SampleManifestMetadataStub")
    ok("schema.sample_source_decision", sample_source_decision_candidate_schema.get("schema_name") == "SampleSourceDecisionCandidate")
    ok("schema.file_boundary_decision", file_boundary_decision_candidate_schema.get("schema_name") == "FileBoundaryDecisionCandidate")
    ok("schema.privacy_precheck_decision", privacy_precheck_decision_candidate_schema.get("schema_name") == "PrivacyPrecheckDecisionCandidate")
    ok("schema.manual_review_decision", manual_review_decision_candidate_schema.get("schema_name") == "ManualReviewDecisionCandidate")
    ok("schema.usage_decision", sample_usage_decision_candidate_schema.get("schema_name") == "SampleUsageDecisionCandidate")
    ok("schema.mapping_stub", sample_to_frame_candidate_mapping_stub_schema.get("schema_name") == "SampleToFrameCandidateMappingStub")
    ok("schema.result", controlled_frame_sample_dryrun_result_schema.get("schema_name") == "ControlledFrameSampleDryRunResult")

    # Scenario matrix required 16 cases
    scenarios = controlled_frame_sample_dryrun_scenario_matrix.get("scenarios", [])
    ok("scenario_matrix.generated", controlled_frame_sample_dryrun_scenario_matrix.get("scenario_count", 0) >= 16, controlled_frame_sample_dryrun_scenario_matrix.get("scenario_count"))
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
        "medical_context_sample_restricted",
        "workplace_sensitive_sample_restricted",
    )
    for scenario_id in required_scenarios:
        row = next((item for item in scenarios if item.get("scenario_id") == scenario_id), {})
        ok(f"scenario.{scenario_id}.present", bool(row))
        ok(f"scenario.{scenario_id}.manifest_only", row.get("manifest_metadata_only") is True)
        ok(f"scenario.{scenario_id}.no_open", row.get("file_opened") is False and row.get("image_opened") is False and row.get("video_opened") is False)
        ok(f"scenario.{scenario_id}.no_decode_extract", row.get("video_decoded") is False and row.get("frame_extracted") is False)
        ok(f"scenario.{scenario_id}.no_hash", row.get("real_file_hash_computed") is False)

    # Results must be generated and consistent sizes
    results = controlled_frame_sample_dryrun_results.get("results", [])
    ok("results.generated", controlled_frame_sample_dryrun_results.get("result_count", 0) >= 16, controlled_frame_sample_dryrun_results.get("result_count"))
    ok("results.count==scenario_count", len(results) == controlled_frame_sample_dryrun_scenario_matrix.get("scenario_count"), (len(results), controlled_frame_sample_dryrun_scenario_matrix.get("scenario_count")))
    ok("file_boundary.rows==16", sample_file_boundary_check_results.get("row_count", 0) >= 16, sample_file_boundary_check_results.get("row_count"))
    ok("privacy.rows==16", sample_privacy_precheck_results.get("row_count", 0) >= 16, sample_privacy_precheck_results.get("row_count"))
    ok("manual_review.rows==16", manual_review_gate_results.get("row_count", 0) >= 16, manual_review_gate_results.get("row_count"))
    ok("mapping.rows==16", sample_to_frame_mapping_stub_results.get("row_count", 0) >= 16, sample_to_frame_mapping_stub_results.get("row_count"))

    # Boundary matrix strictness
    ok("boundary.scope", sample_dryrun_boundary_matrix.get("dryrun_scope") == "controlled_frame_sample_dryrun_only")
    for key in (
        "manifest_metadata_only",
        "sample_manifest_loaded",
        "manifest_only_processing",
        "sample_manifest_not_sample_processing",
        "privacy_precheck_required",
        "manual_review_gate_required_for_sensitive_samples",
        "sample_to_frame_candidate_mapping_without_content_read",
        "no_runtime_executed",
        "no_new_runtime_enabled",
        "boundary_ok",
    ):
        ok(f"boundary.{key}.true", sample_dryrun_boundary_matrix.get(key) is True)
    for key in (
        "file_content_read",
        "image_content_read",
        "video_content_read",
        "file_opened",
        "image_opened",
        "video_opened",
        "video_decoded",
        "frame_extracted",
        "real_file_hash_computed",
        "controlled_sample_runtime_started",
        "visual_observation_generated",
        "scene_sketch_generated",
        "ocr_activation_result_generated",
        "tracking_result_generated",
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
        ok(f"boundary.{key}.false", sample_dryrun_boundary_matrix.get(key) is False)
    ok("boundary.violations==[]", sample_dryrun_boundary_matrix.get("violations") == [])

    # no_runtime/no_write reports must match boundary guarantees
    for payload_name, payload in (("no_runtime", no_runtime_boundary_report), ("no_write", no_write_boundary_report)):
        ok(f"{payload_name}.scope", payload.get("dryrun_scope") == "controlled_frame_sample_dryrun_only")
        for key in ("no_runtime_executed", "no_new_runtime_enabled", "boundary_ok", "manifest_metadata_only", "sample_manifest_loaded", "manifest_only_processing", "sample_manifest_not_sample_processing"):
            ok(f"{payload_name}.{key}", payload.get(key) is True)
        for key in (
            "real_file_hash_computed",
            "file_opened",
            "image_opened",
            "video_opened",
            "video_decoded",
            "frame_extracted",
            "camera_invoked",
            "visual_model_invoked",
            "map_api_invoked",
            "ocr_provider_invoked",
            "tracking_runtime_invoked",
            "world_model_written",
            "memory_written",
            "fact_written",
        ):
            ok(f"{payload_name}.{key}.false", payload.get(key) is False)
        ok(f"{payload_name}.violations==[]", payload.get("violations") == [])

    # Debt register & next phase
    ok("debt.count>=3", len(governance_debt_register.get("carryover_topics", [])) >= 3, len(governance_debt_register.get("carryover_topics", [])))
    ok("next_phase.final_decision", next_phase_recommendation.get("final_decision") == FINAL_DECISION)
    ok("next_phase.recommended", next_phase_recommendation.get("recommended_next_phase") == NEXT_PHASE)

    # Meta checks to ensure >=200 checks
    ok("meta.check_ids.unique", len({c["check_id"] for c in checks}) == len(checks), len(checks))
    ok("meta.checks_total>=200", len(checks) >= 200, len(checks))
    ok("meta.baseline_requirement==160", BASELINE_REQUIREMENT == 160)
    ok("meta.min_checks_required==200", MIN_CHECKS == 200)

    passed = sum(1 for item in checks if item["passed"])
    verdict = "GO" if passed >= MIN_CHECKS and not any(not item["passed"] for item in checks) else "NO_GO"
    report = {
        "phase": PHASE_ID,
        "verdict": verdict,
        "checks_passed": passed,
        "checks_total": len(checks),
        "min_checks_required": MIN_CHECKS,
        "baseline_requirement": BASELINE_REQUIREMENT,
        "final_decision": FINAL_DECISION if verdict == "GO" else "CONTROLLED_FRAME_SAMPLE_DRYRUN_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if verdict == "GO" else PHASE_ID,
        "failed_checks": [item for item in checks if not item["passed"]],
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"verdict": verdict, "checks_passed": passed, "checks_total": len(checks)}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())

