#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Controlled Frame File Metadata Boundary Post-DryRun Review v1 (review-only)."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

PHASE_ID = "Phase-Controlled-Frame-File-Metadata-Boundary-Post-DryRun-Review-v1-001"
FINAL_DECISION = "CONTROLLED_FRAME_FILE_METADATA_BOUNDARY_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE"
NEXT_PHASE = "Phase-Controlled-Frame-File-Metadata-Boundary-Closure-v1-001"
MIN_CHECKS = 180
BASELINE_REQUIREMENT = 140

REQUIRED_SCENARIOS = [
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
    "manifest_to_metadata_mapping_candidate",
    "metadata_sensitive_requires_manual_review",
]


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-root",
        default="/Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/controlled_frame_file_metadata_boundary_post_dryrun_review_v1_smoke_v0",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    checks: List[Dict[str, Any]] = []

    def ok(check_id: str, passed: bool, detail: Any = None) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})

    summary = _load_json(root / "summary.json")
    input_root_review = _load_json(root / "file_metadata_dryrun_input_root_review.json")
    scenario_review = _load_json(root / "file_metadata_scenario_coverage_review.json")
    path_review = _load_json(root / "path_legality_decision_review.json")
    existence_review = _load_json(root / "file_existence_decision_review.json")
    metadata_review = _load_json(root / "external_metadata_decision_review.json")
    hash_review = _load_json(root / "hash_policy_decision_review.json")
    fixture_review = _load_json(root / "fixture_registry_decision_review.json")
    mapping_review = _load_json(root / "manifest_to_file_metadata_mapping_review.json")
    file_op_review = _load_json(root / "file_operation_boundary_review.json")
    runtime_review = _load_json(root / "runtime_write_action_speech_boundary_review.json")
    closure_readiness = _load_json(root / "file_metadata_boundary_closure_readiness_decision.json")
    governance_debt = _load_json(root / "governance_debt_review.json")
    next_phase = _load_json(root / "next_phase_recommendation.json")
    no_file_op = _load_json(root / "no_file_operation_boundary_report.json")
    no_runtime = _load_json(root / "no_runtime_boundary_report.json")
    no_write = _load_json(root / "no_write_boundary_report.json")

    for key in (
        "file_metadata_boundary_dryrun_input_loaded",
        "file_metadata_boundary_planning_input_loaded",
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
        "input_root_review_generated",
        "scenario_coverage_review_generated",
        "path_legality_decision_review_generated",
        "file_existence_decision_review_generated",
        "external_metadata_decision_review_generated",
        "hash_policy_decision_review_generated",
        "fixture_registry_decision_review_generated",
        "manifest_to_file_metadata_mapping_review_generated",
        "file_operation_boundary_review_generated",
        "runtime_write_action_speech_boundary_review_generated",
        "closure_readiness_decision_generated",
        "fixture_registry_candidate_generated",
        "manifest_to_file_metadata_mapping_generated",
        "metadata_decision_simulation_only",
        "hash_placeholder_allowed",
        "perceptual_hash_deferred",
        "no_exif_parse_now",
        "no_video_probe_now",
        "external_absolute_path_blocked_verified",
        "path_traversal_blocked_verified",
        "unknown_path_blocked_verified",
        "missing_declared_metadata_blocked_verified",
        "real_hash_attempt_blocked_verified",
        "exif_parse_attempt_blocked_verified",
        "video_probe_attempt_blocked_verified",
        "perceptual_hash_deferred_verified",
        "no_file_operation_boundary_pass",
        "ready_for_closure",
        "ready_for_file_existence_check",
        "ready_for_real_metadata_read",
        "ready_for_real_hash",
        "ready_for_real_image_read",
        "ready_for_runtime",
        "no_runtime_boundary_pass",
        "no_write_boundary_pass",
        "no_action_boundary_pass",
        "no_speech_boundary_pass",
        "no_runtime_executed",
        "no_new_runtime_enabled",
        "boundary_ok",
    ):
        expected = True
        if key in {
            "ready_for_file_existence_check",
            "ready_for_real_metadata_read",
            "ready_for_real_hash",
            "ready_for_real_image_read",
            "ready_for_runtime",
        }:
            expected = False
        ok(f"summary.{key}", summary.get(key) is expected)

    ok("summary.reviewed_scenario_count>=18", summary.get("reviewed_scenario_count", 0) >= 18, summary.get("reviewed_scenario_count"))
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

    ok("summary.review_scope", summary.get("review_scope") == "controlled_frame_file_metadata_boundary_post_dryrun_review_only")
    ok("summary.violations", summary.get("violations") == [])
    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)

    ok("input_root.status", input_root_review.get("input_root_status") == "all_required_loaded")
    ok("input_root.missing", input_root_review.get("missing_required_roots") == [])

    ok("scenario.verdict", scenario_review.get("verdict") == "GO")
    ok("scenario.missing", scenario_review.get("missing_scenarios") == [])
    ok("scenario.count", scenario_review.get("reviewed_scenario_count", 0) >= 18)
    for sid in REQUIRED_SCENARIOS:
        ok(f"scenario.covered.{sid}", sid in scenario_review.get("covered_scenarios", []))

    ok("path.verdict", path_review.get("verdict") == "GO")
    ok("path.repo", path_review.get("repo_fixture_allowed_verified") is True)
    ok("path.eval_out", path_review.get("eval_out_fixture_allowed_verified") is True)
    ok("path.user_upload", path_review.get("user_upload_restricted_verified") is True)
    ok("path.external", path_review.get("external_absolute_path_blocked_verified") is True)
    ok("path.traversal", path_review.get("path_traversal_blocked_verified") is True)
    ok("path.symlink", path_review.get("symlink_review_required_verified") is True)
    ok("path.unknown", path_review.get("unknown_path_blocked_verified") is True)

    ok("existence.verdict", existence_review.get("verdict") == "GO")
    ok("existence.not_checked", existence_review.get("existence_status_not_checked") is True)
    ok("existence.not_invoked", existence_review.get("file_existence_check_invoked") is False)
    ok("existence.no_stat", existence_review.get("file_stat_invoked") is False)

    ok("metadata.verdict", metadata_review.get("verdict") == "GO")
    ok("metadata.missing_blocked", metadata_review.get("missing_declared_metadata_blocked_verified") is True)
    ok("metadata.sensitive_review", metadata_review.get("sensitive_metadata_manual_review_verified") is True)
    ok("metadata.no_read", metadata_review.get("external_metadata_read_allowed_now") is False)
    ok("metadata.no_exif", metadata_review.get("exif_parsed") is False)
    ok("metadata.no_probe", metadata_review.get("video_probe_invoked") is False)

    ok("hash.verdict", hash_review.get("verdict") == "GO")
    ok("hash.placeholder", hash_review.get("hash_placeholder_allowed_verified") is True)
    ok("hash.real_blocked", hash_review.get("real_hash_attempt_blocked_verified") is True)
    ok("hash.perceptual", hash_review.get("perceptual_hash_deferred_verified") is True)
    ok("hash.no_real", hash_review.get("real_file_hash_computed") is False)

    ok("fixture.verdict", fixture_review.get("verdict") == "GO")
    ok("fixture.candidate", fixture_review.get("fixture_registry_candidate_generated") is True)
    ok("fixture.no_runtime", fixture_review.get("fixture_registry_runtime_started") is False)
    ok("fixture.candidate_only", fixture_review.get("registry_entry_candidate_only") is True)

    ok("mapping.verdict", mapping_review.get("verdict") == "GO")
    ok("mapping.generated", mapping_review.get("manifest_to_file_metadata_mapping_generated") is True)
    ok("mapping.no_runtime", mapping_review.get("manifest_to_file_metadata_candidate_mapping_runtime_started") is False)
    ok("mapping.no_content", mapping_review.get("content_read_required") is False)
    ok("mapping.no_visual", mapping_review.get("visual_observation_generated") is False)

    ok("file_op.verdict", file_op_review.get("verdict") == "GO")
    ok("file_op.pass", file_op_review.get("no_file_operation_boundary_pass") is True)

    ok("runtime.verdict", runtime_review.get("verdict") == "GO")
    ok("runtime.no_runtime", runtime_review.get("no_runtime_boundary_pass") is True)
    ok("runtime.no_write", runtime_review.get("no_write_boundary_pass") is True)
    ok("runtime.no_action", runtime_review.get("no_action_boundary_pass") is True)
    ok("runtime.no_speech", runtime_review.get("no_speech_boundary_pass") is True)

    ok("closure.ready", closure_readiness.get("ready_for_closure") is True)
    ok("closure.verdict", closure_readiness.get("post_dryrun_review_verdict") == "GO")
    ok("closure.blockers", closure_readiness.get("blockers") == [])
    ok("closure.no_file_existence", closure_readiness.get("ready_for_file_existence_check") is False)
    ok("closure.no_image", closure_readiness.get("ready_for_real_image_read") is False)
    ok("closure.final", closure_readiness.get("final_decision") == FINAL_DECISION)
    ok("closure.next", closure_readiness.get("recommended_next_phase") == NEXT_PHASE)

    ok("governance.reviewed", governance_debt.get("reviewed") is True)
    ok("next_phase.final", next_phase.get("final_decision") == FINAL_DECISION)
    ok("next_phase.recommended", next_phase.get("recommended_next_phase") == NEXT_PHASE)

    ok("no_file_op.review_only", no_file_op.get("review_only") is True)
    ok("no_file_op.simulation", no_file_op.get("metadata_decision_simulation_only") is True)
    ok("no_file_op.stat", no_file_op.get("file_stat_invoked") is False)
    ok("no_file_op.exif", no_file_op.get("exif_parsed") is False)

    ok("no_runtime.pass", no_runtime.get("no_runtime_boundary_pass") is True)
    ok("no_write.pass", no_write.get("no_write_boundary_pass") is True)

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
