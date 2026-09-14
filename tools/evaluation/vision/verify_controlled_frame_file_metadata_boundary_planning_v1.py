#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Controlled Frame File Metadata Boundary Planning v1 (planning-only)."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

PHASE_ID = "Phase-Controlled-Frame-File-Metadata-Boundary-Planning-v1-001"
FINAL_DECISION = "CONTROLLED_FRAME_FILE_METADATA_BOUNDARY_PLANNING_READY_FOR_DRYRUN"
NEXT_PHASE = "Phase-Controlled-Frame-File-Metadata-Boundary-DryRun-v1-001"
MIN_CHECKS = 200
BASELINE_REQUIREMENT = 160

REQUIRED_SCENARIO_IDS = [
    "repo_fixture_path_candidate",
    "eval_out_fixture_path_candidate",
    "user_uploaded_path_candidate",
    "external_absolute_path_blocked",
    "path_traversal_blocked",
    "symlink_requires_review",
    "unknown_path_blocked",
    "declared_metadata_public_image",
    "declared_metadata_private_home",
    "missing_declared_metadata_blocked",
    "hash_placeholder_allowed",
    "real_hash_attempt_blocked",
    "exif_parse_attempt_blocked",
    "video_probe_attempt_blocked",
    "perceptual_hash_deferred",
    "fixture_registry_entry_candidate",
]

METADATA_FIELDS = [
    "declared_file_name",
    "declared_extension",
    "declared_mime_type",
    "declared_size_bytes",
    "declared_created_at",
    "declared_modified_at",
    "declared_source",
    "declared_capture_context",
    "declared_privacy_tags",
]


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-root",
        default="/Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/controlled_frame_file_metadata_boundary_planning_v1_smoke_v0",
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
    planning_policy = _load_json(root / "controlled_frame_file_metadata_boundary_planning_policy.json")
    file_existence = _load_json(root / "file_existence_check_policy.json")
    path_legality = _load_json(root / "path_legality_policy.json")
    external_metadata = _load_json(root / "external_metadata_boundary_policy.json")
    real_hash = _load_json(root / "real_hash_computation_policy.json")
    fixture_registry = _load_json(root / "fixture_registry_policy.json")
    fixture_schema = _load_json(root / "fixture_registry_entry_schema.json")
    mapping_policy = _load_json(root / "manifest_to_file_metadata_candidate_mapping_policy.json")
    candidate_schema = _load_json(root / "file_metadata_candidate_schema.json")
    scenario_matrix = _load_json(root / "controlled_frame_file_metadata_boundary_planning_scenario_matrix.json")
    boundary_matrix = _load_json(root / "file_metadata_boundary_matrix.json")
    governance_debt = _load_json(root / "governance_debt_register.json")
    next_phase = _load_json(root / "next_phase_recommendation.json")
    no_file_op = _load_json(root / "no_file_operation_boundary_report.json")
    no_runtime = _load_json(root / "no_runtime_boundary_report.json")
    no_write = _load_json(root / "no_write_boundary_report.json")

    rows = input_root_matrix.get("rows", [])
    idx = {row.get("intake_id"): row for row in rows}
    for intake_id in (
        "post_controlled_frame_sample_roadmap_decision",
        "controlled_frame_sample_closure",
        "controlled_frame_sample_post_review",
        "controlled_frame_sample_dryrun",
        "controlled_frame_sample_planning",
        "post_crossing_decision_roadmap_decision",
        "crossing_decision_closure",
        "controlled_frame_input_closure",
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
        "privacy_governance_docs",
    ):
        ok(f"input.{intake_id}.optional", idx.get(intake_id, {}).get("status") in {"loaded", "optional_missing"}, idx.get(intake_id, {}).get("status"))

    for key in (
        "post_controlled_frame_sample_roadmap_input_loaded",
        "controlled_frame_sample_closure_input_loaded",
        "controlled_frame_sample_post_review_input_loaded",
        "controlled_frame_sample_dryrun_input_loaded",
        "controlled_frame_sample_planning_input_loaded",
        "controlled_frame_input_closure_input_loaded",
        "map_location_readonly_context_input_loaded",
        "safety_constitution_input_loaded",
        "minimal_runtime_integration_closure_loaded",
        "ocr_final_closure_loaded",
        "controlled_frame_file_metadata_boundary_policy_defined",
        "file_existence_check_policy_defined",
        "path_legality_policy_defined",
        "external_metadata_boundary_policy_defined",
        "real_hash_computation_policy_defined",
        "fixture_registry_policy_defined",
        "fixture_registry_entry_schema_defined",
        "manifest_to_file_metadata_candidate_mapping_policy_defined",
        "file_metadata_candidate_schema_defined",
        "scenario_matrix_generated",
        "fixture_registry_candidate_defined",
        "hash_placeholder_allowed",
        "perceptual_hash_deferred",
        "no_exif_parse_now",
        "no_video_probe_now",
        "no_runtime_executed",
        "no_new_runtime_enabled",
        "boundary_ok",
    ):
        ok(f"summary.{key}", summary.get(key) is True)

    ok("summary.scenario_count>=16", summary.get("scenario_count", 0) >= 16, summary.get("scenario_count"))
    ok("summary.allowed_path_candidate_count>=2", summary.get("allowed_path_candidate_count", 0) >= 2, summary.get("allowed_path_candidate_count"))
    ok("summary.restricted_path_candidate_count>=2", summary.get("restricted_path_candidate_count", 0) >= 2, summary.get("restricted_path_candidate_count"))
    ok("summary.blocked_path_candidate_count>=3", summary.get("blocked_path_candidate_count", 0) >= 3, summary.get("blocked_path_candidate_count"))
    ok("summary.metadata_candidate_case_count>=2", summary.get("metadata_candidate_case_count", 0) >= 2, summary.get("metadata_candidate_case_count"))
    ok("summary.hash_policy_case_count>=3", summary.get("hash_policy_case_count", 0) >= 3, summary.get("hash_policy_case_count"))

    for key in (
        "file_existence_check_allowed_now",
        "path_legality_check_allowed_now",
        "external_metadata_read_allowed_now",
        "real_hash_computation_allowed_now",
        "file_existence_check_invoked",
        "file_stat_invoked",
        "file_opened",
        "file_content_read",
        "image_content_read",
        "video_content_read",
        "image_opened",
        "video_opened",
        "video_decoded",
        "frame_extracted",
        "exif_parsed",
        "video_probe_invoked",
        "real_file_hash_computed",
        "perceptual_hash_computed",
        "fixture_registry_runtime_started",
        "manifest_to_file_metadata_candidate_mapping_runtime_started",
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
        ok(f"summary.{key}", summary.get(key) is False)

    ok("summary.planning_scope", summary.get("planning_scope") == "controlled_frame_file_metadata_boundary_planning_only")
    ok("summary.violations", summary.get("violations") == [])
    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)

    ok("planning_policy.scope", planning_policy.get("policy_scope") == "controlled_frame_file_metadata_boundary_planning_only")
    ok("planning_policy.planning_only", planning_policy.get("planning_only") is True)
    ok("planning_policy.no_file_stat", planning_policy.get("no_file_stat") is True)
    ok("planning_policy.no_file_open", planning_policy.get("no_file_open") is True)
    ok("planning_policy.no_real_hash", planning_policy.get("no_real_hash_computation") is True)
    ok("planning_policy.file_existence_ref", planning_policy.get("file_existence_policy_ref") == "file_existence_check_policy.json")
    ok("planning_policy.path_ref", planning_policy.get("path_legality_policy_ref") == "path_legality_policy.json")

    ok("file_existence.allowed_now", file_existence.get("file_existence_check_allowed_now") is False)
    ok("file_existence.no_content_read", file_existence.get("no_content_read_guarantee") is True)
    ok("file_existence.gate_count", len(file_existence.get("required_gate", [])) >= 3)

    ok("path_legality.allowed_now", path_legality.get("path_legality_check_allowed_now") is False)
    ok("path_legality.traversal_block", path_legality.get("path_traversal_block_required") is True)
    ok("path_legality.repo_fixture", "repo_fixture_path_candidate" in path_legality.get("allowed_path_pattern_candidate", []))
    ok("path_legality.eval_out", "eval_out_fixture_path_candidate" in path_legality.get("allowed_path_pattern_candidate", []))
    ok("path_legality.external_blocked", "external_absolute_path_blocked" in path_legality.get("blocked_path_pattern_candidate", []))

    ok("external_metadata.allowed_now", external_metadata.get("external_metadata_read_allowed_now") is False)
    ok("external_metadata.no_exif", external_metadata.get("no_exif_parse_now") is True)
    ok("external_metadata.no_probe", external_metadata.get("no_video_probe_now") is True)
    for field in METADATA_FIELDS:
        ok(f"external_metadata.field.{field}", field in external_metadata.get("metadata_fields_candidate", []))

    ok("real_hash.allowed_now", real_hash.get("real_hash_computation_allowed_now") is False)
    ok("real_hash.placeholder", real_hash.get("hash_placeholder_allowed") is True)
    ok("real_hash.not_computed", real_hash.get("hash_currently_not_computed") is True)
    ok("real_hash.perceptual_deferred", real_hash.get("perceptual_hash_deferred") is True)
    ok("real_hash.sha256", "sha256" in real_hash.get("future_hash_algorithm_candidate", []))

    ok("fixture_registry.defined", fixture_registry.get("fixture_registry_defined") is True)
    ok("fixture_registry.runtime", fixture_registry.get("registry_runtime_allowed") is False)
    ok("fixture_schema.file_exists_verified", fixture_schema.get("invariants", {}).get("file_exists_verified") is False)
    ok("fixture_schema.real_hash", fixture_schema.get("invariants", {}).get("real_hash_computed") is False)
    ok("fixture_schema.content_read", fixture_schema.get("invariants", {}).get("content_read") is False)

    ok("mapping.content_read_required", mapping_policy.get("content_read_required") is False)
    ok("mapping.file_existence_now", mapping_policy.get("file_existence_required_now") is False)
    ok("mapping.real_hash_now", mapping_policy.get("real_hash_required_now") is False)
    ok("mapping.output_type", mapping_policy.get("output_candidate_type") == "FileMetadataCandidate")

    ok("candidate_schema.invariants", candidate_schema.get("invariants", {}).get("file_stat_invoked") is False)
    ok("candidate_schema.fact", candidate_schema.get("invariants", {}).get("fact_status") == "not_fact")

    scenario_rows = scenario_matrix.get("scenarios", [])
    scenario_idx = {row.get("scenario_id"): row for row in scenario_rows}
    ok("scenarios.count", scenario_matrix.get("scenario_count", 0) >= 16, scenario_matrix.get("scenario_count"))
    for sid in REQUIRED_SCENARIO_IDS:
        row = scenario_idx.get(sid, {})
        ok(f"scenario.{sid}.present", sid in scenario_idx)
        ok(f"scenario.{sid}.planning_only", row.get("planning_only") is True)
        ok(f"scenario.{sid}.file_stat", row.get("file_stat_invoked") is False)
        ok(f"scenario.{sid}.file_opened", row.get("file_opened") is False)
        ok(f"scenario.{sid}.content_read", row.get("content_read") is False)

    ok("boundary_matrix.frozen_count", len(boundary_matrix.get("frozen_boundaries", [])) >= 10)
    ok("boundary_matrix.blocked.file_existence", boundary_matrix.get("blocked_now", {}).get("file_existence_check") is True)
    ok("boundary_matrix.blocked.real_hash", boundary_matrix.get("blocked_now", {}).get("real_hash_computation") is True)

    ok("governance_debt.topics", len(governance_debt.get("carryover_topics", [])) >= 4)
    ok("next_phase.final", next_phase.get("final_decision") == FINAL_DECISION)
    ok("next_phase.recommended", next_phase.get("recommended_next_phase") == NEXT_PHASE)

    for report_name, report in (("no_file_op", no_file_op),):
        ok(f"{report_name}.planning_only", report.get("planning_only") is True)
        ok(f"{report_name}.no_stat", report.get("no_file_stat") is True)
        ok(f"{report_name}.no_open", report.get("no_file_open") is True)
        ok(f"{report_name}.no_real_hash", report.get("no_real_hash_computation") is True)
        ok(f"{report_name}.file_stat_invoked", report.get("file_stat_invoked") is False)
        ok(f"{report_name}.exif", report.get("exif_parsed") is False)
        ok(f"{report_name}.probe", report.get("video_probe_invoked") is False)
        ok(f"{report_name}.boundary_ok", report.get("boundary_ok") is True)

    for report_name, report in (("no_runtime", no_runtime), ("no_write", no_write)):
        ok(f"{report_name}.no_runtime", report.get("no_runtime_executed") is True)
        ok(f"{report_name}.visual_obs", report.get("visual_observation_generated") is False)
        ok(f"{report_name}.world_model", report.get("world_model_written") is False)

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
