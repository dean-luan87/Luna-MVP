#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Controlled Frame File Existence Check Guarded Planning v1 (planning-only)."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

PHASE_ID = "Phase-Controlled-Frame-File-Existence-Check-Guarded-Planning-v1-001"
FINAL_DECISION = "CONTROLLED_FRAME_FILE_EXISTENCE_CHECK_GUARDED_PLANNING_READY_FOR_DRYRUN"
NEXT_PHASE = "Phase-Controlled-Frame-File-Existence-Check-Guarded-DryRun-v1-001"

MIN_CHECKS = 200
BASELINE_REQUIREMENT = 160

REQUIRED_SCENARIO_IDS = [
    "repo_fixture_future_candidate",
    "eval_out_fixture_future_candidate",
    "registered_fixture_future_candidate",
    "controlled_test_asset_future_candidate",
    "user_upload_restricted",
    "external_absolute_path_blocked",
    "path_traversal_blocked",
    "unknown_path_blocked",
    "symlink_restricted",
    "system_sensitive_path_blocked",
    "home_arbitrary_path_blocked",
    "network_mount_path_blocked",
    "missing_source_chain_blocked",
    "missing_privacy_tags_blocked",
    "missing_fixture_registry_ref_blocked",
    "authorized_candidate_but_not_invoked",
    "gate_denied_behavior",
    "permission_denied_future_failure_mode",
]


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-root",
        default=str(repo_root / "_eval_out" / "controlled_frame_file_existence_check_guarded_planning_v1_smoke_v0"),
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
    planning_policy = _load_json(root / "controlled_frame_file_existence_check_guarded_planning_policy.json")
    gate_policy = _load_json(root / "file_existence_check_gate_policy.json")
    allowed_scope = _load_json(root / "allowed_path_scope_policy.json")
    blocked_scope = _load_json(root / "blocked_path_scope_policy.json")
    auth_policy = _load_json(root / "file_existence_authorization_policy.json")
    audit_policy = _load_json(root / "file_existence_audit_trace_policy.json")
    failure_policy = _load_json(root / "file_existence_failure_mode_policy.json")
    rollback_policy = _load_json(root / "file_existence_rollback_policy.json")
    candidate_schema = _load_json(root / "file_existence_decision_candidate_schema.json")
    mapping_policy = _load_json(root / "existence_check_to_file_metadata_candidate_mapping_policy.json")
    scenario_matrix = _load_json(root / "controlled_frame_file_existence_check_guarded_planning_scenario_matrix.json")
    boundary_matrix = _load_json(root / "file_existence_check_boundary_matrix.json")
    governance_debt = _load_json(root / "governance_debt_register.json")
    next_phase = _load_json(root / "next_phase_recommendation.json")
    no_file_op = _load_json(root / "no_file_operation_boundary_report.json")
    no_runtime = _load_json(root / "no_runtime_boundary_report.json")
    no_write = _load_json(root / "no_write_boundary_report.json")

    rows = input_root_matrix.get("rows", [])
    idx = {row.get("intake_id"): row for row in rows}
    for intake_id in (
        "post_file_metadata_boundary_roadmap_decision",
        "file_metadata_boundary_closure",
        "file_metadata_boundary_post_review",
        "file_metadata_boundary_dryrun",
        "file_metadata_boundary_planning",
        "post_controlled_frame_sample_roadmap_decision",
        "controlled_frame_sample_closure",
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
        ok(
            f"input.{intake_id}.optional",
            idx.get(intake_id, {}).get("status") in {"loaded", "optional_missing"},
            idx.get(intake_id, {}).get("status"),
        )

    for key in (
        "post_file_metadata_boundary_roadmap_input_loaded",
        "file_metadata_boundary_closure_input_loaded",
        "file_metadata_boundary_post_review_input_loaded",
        "file_metadata_boundary_dryrun_input_loaded",
        "file_metadata_boundary_planning_input_loaded",
        "controlled_frame_sample_closure_input_loaded",
        "controlled_frame_input_closure_input_loaded",
        "map_location_readonly_context_input_loaded",
        "safety_constitution_input_loaded",
        "minimal_runtime_integration_closure_loaded",
        "ocr_final_closure_loaded",
        "controlled_frame_file_existence_check_guarded_planning_policy_defined",
        "file_existence_check_gate_policy_defined",
        "allowed_path_scope_policy_defined",
        "blocked_path_scope_policy_defined",
        "file_existence_authorization_policy_defined",
        "file_existence_audit_trace_policy_defined",
        "file_existence_failure_mode_policy_defined",
        "file_existence_rollback_policy_defined",
        "file_existence_decision_candidate_schema_defined",
        "existence_check_to_file_metadata_candidate_mapping_policy_defined",
        "scenario_matrix_generated",
        "authorization_required",
        "audit_trace_required",
        "rollback_required",
        "source_chain_required",
        "fixture_registry_authorization_required",
        "user_upload_authorization_insufficient_alone",
        "system_generated_path_insufficient_alone",
        "no_runtime_executed",
        "no_new_runtime_enabled",
        "boundary_ok",
    ):
        ok(f"summary.{key}", summary.get(key) is True)

    ok("summary.scenario_count>=18", summary.get("scenario_count", 0) >= 18, summary.get("scenario_count"))
    ok(
        "summary.future_allowed_path_candidate_count>=4",
        summary.get("future_allowed_path_candidate_count", 0) >= 4,
        summary.get("future_allowed_path_candidate_count"),
    )
    ok(
        "summary.blocked_path_candidate_count>=6",
        summary.get("blocked_path_candidate_count", 0) >= 6,
        summary.get("blocked_path_candidate_count"),
    )
    ok(
        "summary.restricted_path_candidate_count>=2",
        summary.get("restricted_path_candidate_count", 0) >= 2,
        summary.get("restricted_path_candidate_count"),
    )

    for key in (
        "file_existence_check_allowed_now",
        "exists_call_allowed_now",
        "stat_allowed_now",
        "open_allowed_now",
        "content_read_allowed_now",
        "hash_allowed_now",
        "file_existence_check_invoked",
        "os_path_exists_invoked",
        "pathlib_exists_invoked",
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

    ok("summary.planning_scope", summary.get("planning_scope") == "controlled_frame_file_existence_check_guarded_planning_only")
    ok("summary.violations", summary.get("violations") == [])
    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)

    ok("planning_policy.planning_only", planning_policy.get("planning_only") is True)
    ok("planning_policy.allowed_now", planning_policy.get("existence_check_allowed_now") is False)
    ok("planning_policy.gate_ref", planning_policy.get("file_existence_check_gate_ref") == "file_existence_check_gate_policy.json")

    ok("gate_policy.closed", gate_policy.get("current_phase_gate_open") is False)
    ok("gate_policy.future", gate_policy.get("future_gate_candidate") is True)
    ok("gate_policy.veto_count", len(gate_policy.get("veto_conditions", [])) >= 6)

    allowed_entries = allowed_scope.get("allowed_for_future_existence_check_candidate", [])
    ok("allowed_scope.count>=4", len(allowed_entries) >= 4, len(allowed_entries))
    ok("allowed_scope.allowed_now", allowed_scope.get("allowed_now") is False)
    ok("blocked_scope.blocked_now", blocked_scope.get("blocked_now") is True)
    ok("auth_policy.authorization_required", auth_policy.get("authorization_required") is True)
    ok("auth_policy.fixture_registry_required", auth_policy.get("fixture_registry_authorization_required") is True)
    ok("audit_policy.audit_required", audit_policy.get("audit_required") is True)
    ok("rollback_policy.rollback_required", rollback_policy.get("rollback_required") is True)
    ok("candidate_schema.not_checked", candidate_schema.get("invariants", {}).get("existence_status") == "not_checked")
    ok("mapping.output_status", mapping_policy.get("output_status") == "planning_only")

    scenario_rows = scenario_matrix.get("scenarios", [])
    scenario_idx = {row.get("scenario_id"): row for row in scenario_rows}
    ok("scenarios.count>=18", scenario_matrix.get("scenario_count", 0) >= 18, scenario_matrix.get("scenario_count"))
    for sid in REQUIRED_SCENARIO_IDS:
        row = scenario_idx.get(sid, {})
        ok(f"scenario.{sid}.present", sid in scenario_idx)
        ok(f"scenario.{sid}.planning_only", row.get("planning_only") is True)
        ok(f"scenario.{sid}.invoked", row.get("current_existence_check_invoked") is False)
        ok(f"scenario.{sid}.exists", row.get("exists_call_invoked") is False)
        ok(f"scenario.{sid}.stat", row.get("stat_invoked") is False)
        ok(f"scenario.{sid}.status", row.get("existence_status") == "not_checked", row.get("existence_status"))

    ok("boundary_matrix.blocked.exists", boundary_matrix.get("blocked_now", {}).get("os_path_exists") is True)
    ok("boundary_matrix.blocked.pathlib", boundary_matrix.get("blocked_now", {}).get("pathlib_path_exists") is True)
    ok("boundary_matrix.blocked.file_stat", boundary_matrix.get("blocked_now", {}).get("file_stat") is True)
    ok("boundary_matrix.blocked.file_open", boundary_matrix.get("blocked_now", {}).get("file_open") is True)

    ok("governance_debt.topics>=4", len(governance_debt.get("carryover_topics", [])) >= 4)
    ok("next_phase.final", next_phase.get("final_decision") == FINAL_DECISION)
    ok("next_phase.recommended", next_phase.get("recommended_next_phase") == NEXT_PHASE)

    for report_name, report in (("no_file_op", no_file_op), ("no_runtime", no_runtime), ("no_write", no_write)):
        ok(f"{report_name}.no_runtime_executed", report.get("no_runtime_executed") is True)
        ok(f"{report_name}.file_existence_check_invoked", report.get("file_existence_check_invoked") is False)
        ok(f"{report_name}.file_stat_invoked", report.get("file_stat_invoked") is False)
        ok(f"{report_name}.file_opened", report.get("file_opened") is False)
        ok(f"{report_name}.hash", report.get("real_file_hash_computed") is False)
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

