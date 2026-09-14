#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Controlled Frame File Stat Guarded DryRun v1 (gate decision simulation only)."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

PHASE_ID = "Phase-Controlled-Frame-File-Stat-Guarded-DryRun-v1-001"
FINAL_DECISION = "CONTROLLED_FRAME_FILE_STAT_GUARDED_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
NEXT_PHASE = "Phase-Controlled-Frame-File-Stat-Guarded-Post-DryRun-Review-v1-001"

MIN_CHECKS = 260
BASELINE_REQUIREMENT = 220

REQUIRED_SCENARIO_IDS = [
    "repo_fixture_stat_future_candidate",
    "eval_out_fixture_stat_future_candidate",
    "registered_fixture_stat_future_candidate",
    "controlled_test_asset_stat_future_candidate",
    "user_upload_stat_restricted",
    "external_absolute_path_stat_blocked",
    "path_traversal_stat_blocked",
    "unknown_path_stat_blocked",
    "symlink_stat_restricted",
    "system_sensitive_path_stat_blocked",
    "home_arbitrary_path_stat_blocked",
    "network_mount_path_stat_blocked",
    "missing_source_chain_stat_blocked",
    "missing_privacy_tags_stat_blocked",
    "missing_fixture_registry_ref_stat_blocked",
    "exists_gate_pass_insufficient_for_stat",
    "user_upload_authorization_insufficient_for_stat",
    "system_generated_path_insufficient_for_stat",
    "authorized_stat_candidate_but_not_invoked",
    "stat_metadata_allowed_candidate",
    "stat_metadata_restricted_candidate",
    "stat_metadata_blocked_or_deferred",
    "stat_permission_denied_future_failure_mode",
    "stat_missing_file_future_failure_mode",
    "stat_gate_denied_behavior",
    "stat_rollback_after_denied_candidate",
    "stat_metadata_boundary_denied",
    "stat_to_file_metadata_mapping_candidate",
]


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-root",
        default=str(repo_root / "_eval_out" / "controlled_frame_file_stat_guarded_dryrun_v1_smoke_v0"),
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
    request_stub_schema = _load_json(root / "simulated_file_stat_request_stub_schema.json")
    gate_schema = _load_json(root / "file_stat_gate_decision_candidate_schema.json")
    path_scope_schema = _load_json(root / "stat_path_scope_dryrun_decision_candidate_schema.json")
    metadata_schema = _load_json(root / "stat_metadata_exposure_decision_candidate_schema.json")
    auth_schema = _load_json(root / "file_stat_authorization_decision_candidate_schema.json")
    audit_schema = _load_json(root / "file_stat_audit_trace_candidate_schema.json")
    failure_schema = _load_json(root / "file_stat_failure_mode_decision_candidate_schema.json")
    rollback_schema = _load_json(root / "file_stat_rollback_decision_candidate_schema.json")
    mapping_schema = _load_json(root / "stat_to_file_metadata_mapping_decision_candidate_schema.json")
    result_schema = _load_json(root / "file_stat_guarded_dryrun_result_schema.json")

    scenario_matrix = _load_json(root / "controlled_frame_file_stat_guarded_dryrun_scenario_matrix.json")
    dryrun_results = _load_json(root / "controlled_frame_file_stat_guarded_dryrun_results.json")
    gate_results = _load_json(root / "file_stat_gate_decision_results.json")
    path_scope_results = _load_json(root / "stat_path_scope_dryrun_decision_results.json")
    metadata_results = _load_json(root / "stat_metadata_exposure_decision_results.json")
    auth_results = _load_json(root / "authorization_decision_results.json")
    audit_results = _load_json(root / "audit_trace_results.json")
    failure_results = _load_json(root / "failure_mode_decision_results.json")
    rollback_results = _load_json(root / "rollback_decision_results.json")
    mapping_results = _load_json(root / "stat_to_file_metadata_mapping_results.json")
    request_results = _load_json(root / "simulated_request_stub_results.json")

    boundary_matrix = _load_json(root / "file_stat_boundary_matrix.json")
    governance_debt = _load_json(root / "governance_debt_register.json")
    next_phase = _load_json(root / "next_phase_recommendation.json")
    no_file_op = _load_json(root / "no_file_operation_boundary_report.json")
    no_runtime = _load_json(root / "no_runtime_boundary_report.json")
    no_write = _load_json(root / "no_write_boundary_report.json")

    rows = input_root_matrix.get("rows", [])
    idx = {row.get("intake_id"): row for row in rows}
    for intake_id in (
        "controlled_frame_file_stat_guarded_planning",
        "post_file_existence_check_roadmap_decision",
        "file_existence_check_guarded_closure",
        "file_existence_check_guarded_post_review",
        "file_existence_check_guarded_dryrun",
        "file_existence_check_guarded_planning",
        "file_metadata_boundary_closure",
        "file_metadata_boundary_post_review",
        "file_metadata_boundary_dryrun",
        "file_metadata_boundary_planning",
        "controlled_frame_sample_closure",
        "controlled_frame_input_closure",
        "map_location_readonly_context",
        "safety_constitution",
        "minimal_runtime_integration_closure",
        "ocr_final_closure",
    ):
        ok(f"input.{intake_id}.loaded", idx.get(intake_id, {}).get("loaded") is True)
    for intake_id in (
        "vision_frame_trace_stream_registry",
        "vision_frame_input_governance",
        "vision_roi_proposal_stub",
        "system_health_hardware_profile",
        "simulation_lab_profile",
        "privacy_governance_docs",
    ):
        ok(
            f"input.{intake_id}.optional",
            idx.get(intake_id, {}).get("status") in {"loaded", "optional_missing"},
            idx.get(intake_id, {}).get("status"),
        )

    # Summary required true keys
    for key in (
        "file_stat_guarded_planning_input_loaded",
        "post_file_existence_check_roadmap_input_loaded",
        "file_existence_check_guarded_closure_input_loaded",
        "file_existence_check_guarded_post_review_input_loaded",
        "file_existence_check_guarded_dryrun_input_loaded",
        "file_existence_check_guarded_planning_input_loaded",
        "file_metadata_boundary_closure_input_loaded",
        "controlled_frame_sample_closure_input_loaded",
        "controlled_frame_input_closure_input_loaded",
        "map_location_readonly_context_input_loaded",
        "safety_constitution_input_loaded",
        "minimal_runtime_integration_closure_loaded",
        "ocr_final_closure_loaded",
        "dryrun_case_schema_defined",
        "simulated_file_stat_request_stub_schema_defined",
        "file_stat_gate_decision_candidate_schema_defined",
        "stat_path_scope_dryrun_decision_candidate_schema_defined",
        "stat_metadata_exposure_decision_candidate_schema_defined",
        "file_stat_authorization_decision_candidate_schema_defined",
        "file_stat_audit_trace_candidate_schema_defined",
        "file_stat_failure_mode_decision_candidate_schema_defined",
        "file_stat_rollback_decision_candidate_schema_defined",
        "stat_to_file_metadata_mapping_decision_candidate_schema_defined",
        "file_stat_guarded_dryrun_result_schema_defined",
        "scenario_matrix_generated",
        "dryrun_results_generated",
        "audit_trace_generated",
        "stat_to_file_metadata_mapping_generated",
        "stat_gate_decision_simulation_only",
        "authorization_required",
        "audit_trace_required",
        "rollback_required",
        "source_chain_required",
        "fixture_registry_authorization_required",
        "user_upload_authorization_insufficient_alone",
        "system_generated_path_insufficient_alone",
        "existence_check_pass_insufficient_alone",
        "no_runtime_executed",
        "no_new_runtime_enabled",
        "cross_repo_input_roots_observed",
        "output_root_fixed_to_luna_core",
        "boundary_ok",
    ):
        ok(f"summary.{key}", summary.get(key) is True)

    ok("summary.dryrun_scope", summary.get("dryrun_scope") == "controlled_frame_file_stat_guarded_dryrun_only")
    ok("summary.violations.empty", summary.get("violations") == [])
    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)

    ok("summary.scenario_count>=28", summary.get("scenario_count", 0) >= 28, summary.get("scenario_count"))
    ok("summary.future_allowed_stat_path_candidate_count>=4", summary.get("future_allowed_stat_path_candidate_count", 0) >= 4)
    ok("summary.blocked_stat_path_candidate_count>=6", summary.get("blocked_stat_path_candidate_count", 0) >= 6)
    ok("summary.restricted_stat_path_candidate_count>=2", summary.get("restricted_stat_path_candidate_count", 0) >= 2)
    ok("summary.authorization_failure_case_count>=3", summary.get("authorization_failure_case_count", 0) >= 3)
    ok("summary.stat_metadata_allowed_candidate_count>=3", summary.get("stat_metadata_allowed_candidate_count", 0) >= 3)
    ok("summary.stat_metadata_restricted_candidate_count>=3", summary.get("stat_metadata_restricted_candidate_count", 0) >= 3)
    ok("summary.stat_metadata_blocked_or_deferred_count>=2", summary.get("stat_metadata_blocked_or_deferred_count", 0) >= 2)
    ok("summary.failure_mode_case_count>=4", summary.get("failure_mode_case_count", 0) >= 4)
    ok("summary.rollback_case_count>=1", summary.get("rollback_case_count", 0) >= 1)

    # Summary must-false boundary keys
    for key in (
        "stat_allowed_now",
        "os_stat_allowed_now",
        "pathlib_stat_allowed_now",
        "lstat_allowed_now",
        "exists_allowed_now",
        "open_allowed_now",
        "content_read_allowed_now",
        "hash_allowed_now",
        "stat_invoked",
        "os_stat_invoked",
        "pathlib_stat_invoked",
        "lstat_invoked",
        "file_existence_check_invoked",
        "os_path_exists_invoked",
        "pathlib_exists_invoked",
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
        ok(f"summary.{key}.false", summary.get(key) is False)

    # Schema presence sanity
    ok("schema.dryrun_case.name", dryrun_case_schema.get("schema_name") == "ControlledFrameFileStatGuardedDryRunCase")
    ok("schema.request_stub.name", request_stub_schema.get("schema_name") == "SimulatedFileStatRequestStub")
    ok("schema.gate.name", gate_schema.get("schema_name") == "FileStatGateDecisionCandidate")
    ok("schema.metadata.name", metadata_schema.get("schema_name") == "StatMetadataExposureDecisionCandidate")
    ok("schema.result.name", result_schema.get("schema_name") == "FileStatGuardedDryRunResult")

    # Scenario matrix checks
    scenario_rows = scenario_matrix.get("scenarios", [])
    scenario_idx = {row.get("scenario_id"): row for row in scenario_rows}
    ok("scenario_matrix.count>=28", scenario_matrix.get("scenario_count", 0) >= 28, scenario_matrix.get("scenario_count"))
    for sid in REQUIRED_SCENARIO_IDS:
        row = scenario_idx.get(sid, {})
        ok(f"scenario.{sid}.present", sid in scenario_idx)
        ok(f"scenario.{sid}.simulation_only", row.get("stat_gate_decision_simulation_only") is True)
        ok(f"scenario.{sid}.stat_invoked", row.get("stat_invoked") is False)
        ok(f"scenario.{sid}.file_opened", row.get("file_opened") is False)

    # Results counts
    ok("results.count.match", dryrun_results.get("result_count") == len(dryrun_results.get("results", [])))
    ok("gate_results.count.match", gate_results.get("decision_count") == len(gate_results.get("decisions", [])))
    ok("path_scope_results.count.match", path_scope_results.get("decision_count") == len(path_scope_results.get("decisions", [])))
    ok("metadata_results.count.match", metadata_results.get("decision_count") == len(metadata_results.get("decisions", [])))
    ok("auth_results.count.match", auth_results.get("decision_count") == len(auth_results.get("decisions", [])))
    ok("audit_results.count.match", audit_results.get("decision_count") == len(audit_results.get("decisions", [])))
    ok("failure_results.count.match", failure_results.get("decision_count") == len(failure_results.get("decisions", [])))
    ok("rollback_results.count.match", rollback_results.get("decision_count") == len(rollback_results.get("decisions", [])))
    ok("mapping_results.count.match", mapping_results.get("decision_count") == len(mapping_results.get("decisions", [])))
    ok("request_results.count.match", request_results.get("request_count") == len(request_results.get("requests", [])))

    # Boundary matrix checks
    ok("boundary_matrix.blocked.file_stat", boundary_matrix.get("blocked_now", {}).get("file_stat") is True)
    ok("boundary_matrix.blocked.exists", boundary_matrix.get("blocked_now", {}).get("os_path_exists") is True)
    ok("boundary_matrix.simulated.metadata_exposure", boundary_matrix.get("simulated_now", {}).get("metadata_exposure_decision") is True)

    ok("governance_debt.topics>=3", len(governance_debt.get("carryover_topics", [])) >= 3)
    ok("next_phase.final", next_phase.get("final_decision") == FINAL_DECISION)
    ok("next_phase.recommended", next_phase.get("recommended_next_phase") == NEXT_PHASE)

    for report_name, report in (("no_file_op", no_file_op), ("no_runtime", no_runtime), ("no_write", no_write)):
        ok(f"{report_name}.no_runtime_executed", report.get("no_runtime_executed") is True)
        ok(f"{report_name}.stat_invoked", report.get("stat_invoked") is False)
        ok(f"{report_name}.file_opened", report.get("file_opened") is False)
        ok(f"{report_name}.boundary_ok", report.get("boundary_ok") is True)

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

