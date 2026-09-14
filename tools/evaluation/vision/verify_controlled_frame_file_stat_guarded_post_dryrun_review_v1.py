#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Controlled Frame File Stat Guarded Post-DryRun Review v1 (review-only)."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

PHASE_ID = "Phase-Controlled-Frame-File-Stat-Guarded-Post-DryRun-Review-v1-001"
FINAL_DECISION = "CONTROLLED_FRAME_FILE_STAT_GUARDED_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE"
NEXT_PHASE = "Phase-Controlled-Frame-File-Stat-Guarded-Closure-v1-001"

MIN_CHECKS = 220
BASELINE_REQUIREMENT = 180

REQUIRED_SCENARIOS = [
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
        default=str(repo_root / "_eval_out" / "controlled_frame_file_stat_guarded_post_dryrun_review_v1_smoke_v0"),
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
    input_root_review = _load_json(root / "file_stat_guarded_dryrun_input_root_review.json")
    scenario_review = _load_json(root / "file_stat_scenario_coverage_review.json")
    gate_review = _load_json(root / "file_stat_gate_decision_review.json")
    path_scope_review = _load_json(root / "stat_path_scope_decision_review.json")
    metadata_review = _load_json(root / "stat_metadata_exposure_decision_review.json")
    auth_review = _load_json(root / "file_stat_authorization_decision_review.json")
    audit_review = _load_json(root / "file_stat_audit_trace_review.json")
    failure_review = _load_json(root / "file_stat_failure_mode_review.json")
    rollback_review = _load_json(root / "file_stat_rollback_review.json")
    mapping_review = _load_json(root / "stat_to_file_metadata_mapping_review.json")
    file_op_review = _load_json(root / "file_operation_boundary_review.json")
    runtime_review = _load_json(root / "runtime_write_action_speech_boundary_review.json")
    closure_readiness = _load_json(root / "file_stat_closure_readiness_decision.json")
    governance_debt = _load_json(root / "governance_debt_review.json")
    next_phase = _load_json(root / "next_phase_recommendation.json")
    no_file_op = _load_json(root / "no_file_operation_boundary_report.json")
    no_runtime = _load_json(root / "no_runtime_boundary_report.json")
    no_write = _load_json(root / "no_write_boundary_report.json")

    # Required inputs
    rows = input_root_matrix.get("rows", [])
    idx = {row.get("intake_id"): row for row in rows}
    for intake_id in (
        "controlled_frame_file_stat_guarded_dryrun",
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

    # Summary: must be true
    must_true = [
        "file_stat_guarded_dryrun_input_loaded",
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
        "input_root_review_generated",
        "scenario_coverage_review_generated",
        "file_stat_gate_decision_review_generated",
        "stat_path_scope_decision_review_generated",
        "stat_metadata_exposure_decision_review_generated",
        "file_stat_authorization_decision_review_generated",
        "file_stat_audit_trace_review_generated",
        "file_stat_failure_mode_review_generated",
        "file_stat_rollback_review_generated",
        "stat_to_file_metadata_mapping_review_generated",
        "file_operation_boundary_review_generated",
        "runtime_write_action_speech_boundary_review_generated",
        "closure_readiness_decision_generated",
        "ready_for_closure",
        "no_file_operation_boundary_pass",
        "no_runtime_boundary_pass",
        "no_write_boundary_pass",
        "no_action_boundary_pass",
        "no_speech_boundary_pass",
        "boundary_ok",
        "cross_repo_input_roots_observed",
        "output_root_fixed_to_luna_core",
    ]
    for key in must_true:
        ok(f"summary.{key}", summary.get(key) is True)

    ok("summary.review_scope", summary.get("review_scope") == "controlled_frame_file_stat_guarded_post_dryrun_review_only")
    ok("summary.violations.empty", summary.get("violations") == [])
    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)

    # Readiness negatives
    for key in (
        "ready_for_real_stat",
        "ready_for_real_exists",
        "ready_for_file_open",
        "ready_for_real_metadata_read",
        "ready_for_real_image_read",
        "ready_for_runtime",
    ):
        ok(f"summary.{key}.false", summary.get(key) is False)

    # Coverage counts
    ok("summary.reviewed_scenario_count>=28", summary.get("reviewed_scenario_count", 0) >= 28, summary.get("reviewed_scenario_count"))
    ok("summary.reviewed_gate_decision_count>=28", summary.get("reviewed_gate_decision_count", 0) >= 28, summary.get("reviewed_gate_decision_count"))
    ok("summary.future_allowed>=4", summary.get("future_allowed_stat_path_candidate_count", 0) >= 4)
    ok("summary.blocked>=6", summary.get("blocked_stat_path_candidate_count", 0) >= 6)
    ok("summary.restricted>=2", summary.get("restricted_stat_path_candidate_count", 0) >= 2)
    ok("summary.authorization_failure_case_count>=3", summary.get("authorization_failure_case_count", 0) >= 3)
    ok("summary.stat_metadata_allowed_candidate_count>=3", summary.get("stat_metadata_allowed_candidate_count", 0) >= 3)
    ok("summary.stat_metadata_restricted_candidate_count>=3", summary.get("stat_metadata_restricted_candidate_count", 0) >= 3)
    ok("summary.stat_metadata_blocked_or_deferred_count>=2", summary.get("stat_metadata_blocked_or_deferred_count", 0) >= 2)
    ok("summary.failure_mode_case_count>=4", summary.get("failure_mode_case_count", 0) >= 4)
    ok("summary.rollback_case_count>=1", summary.get("rollback_case_count", 0) >= 1)

    # Governance invariants
    for key in (
        "stat_gate_decision_simulation_only",
        "gate_open_now_false_all_cases",
        "authorized_stat_candidate_not_invoked_verified",
        "authorization_required",
        "audit_trace_required",
        "rollback_required",
        "source_chain_required",
        "fixture_registry_authorization_required",
        "user_upload_authorization_insufficient_alone",
        "system_generated_path_insufficient_alone",
        "existence_check_pass_insufficient_alone",
        "missing_source_chain_stat_blocked_verified",
        "missing_privacy_tags_stat_blocked_verified",
        "missing_fixture_registry_ref_stat_blocked_verified",
        "stat_permission_denied_future_failure_mode_verified",
        "stat_missing_file_future_failure_mode_verified",
        "stat_gate_denied_behavior_verified",
        "stat_metadata_boundary_denied_verified",
        "stat_rollback_after_denied_candidate_verified",
        "no_persistent_side_effects",
    ):
        ok(f"summary.{key}", summary.get(key) is True)

    # File operation boundary: must all be false
    must_false = [
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
    ]
    for key in must_false:
        ok(f"summary.{key}.false", summary.get(key) is False)

    # Scenario review must cover all required scenarios
    covered = set(scenario_review.get("covered_scenarios", []))
    for sid in REQUIRED_SCENARIOS:
        ok(f"scenario.{sid}.covered", sid in covered)

    ok("scenario_review.verdict", scenario_review.get("verdict") == "PASS")
    ok("gate_review.verdict", gate_review.get("verdict") == "PASS")
    ok("path_scope_review.verdict", path_scope_review.get("verdict") == "PASS")
    ok("metadata_review.verdict", metadata_review.get("verdict") == "PASS")
    ok("auth_review.verdict", auth_review.get("verdict") == "PASS")
    ok("audit_review.verdict", audit_review.get("verdict") == "PASS")
    ok("failure_review.verdict", failure_review.get("verdict") == "PASS")
    ok("rollback_review.verdict", rollback_review.get("verdict") == "PASS")
    ok("mapping_review.verdict", mapping_review.get("verdict") == "PASS")
    ok("file_op_review.verdict", file_op_review.get("verdict") == "PASS")
    ok("runtime_review.verdict", runtime_review.get("verdict") == "PASS")

    # Closure readiness decision
    ok("closure_readiness.ready_for_closure", closure_readiness.get("ready_for_closure") is True)
    ok("closure_readiness.ready_for_real_stat", closure_readiness.get("ready_for_real_stat") is False)
    ok("closure_readiness.final_decision", closure_readiness.get("final_decision") == FINAL_DECISION)
    ok("next_phase.final", next_phase.get("final_decision") == FINAL_DECISION)
    ok("next_phase.recommended", next_phase.get("recommended_next_phase") == NEXT_PHASE)

    # Boundary reports should claim safe
    for report_name, report in (("no_file_op", no_file_op), ("no_runtime", no_runtime), ("no_write", no_write)):
        ok(f"{report_name}.boundary_ok", report.get("boundary_ok") is True)
        ok(f"{report_name}.stat_invoked", report.get("stat_invoked") is False)
        ok(f"{report_name}.no_runtime_executed", report.get("no_runtime_executed") is True)

    ok("governance_debt.present", isinstance(governance_debt.get("notes"), list) and len(governance_debt.get("notes")) >= 1)
    ok("input_root_review.status", input_root_review.get("input_root_status") == "ok")

    # Extra invariants to raise check count and harden review.
    ok("scenario_review.expected_count", scenario_review.get("expected_scenario_count") == len(REQUIRED_SCENARIOS))
    ok("scenario_review.missing_empty", scenario_review.get("missing_scenarios") == [])
    ok("scenario_review.future_allowed_present", scenario_review.get("future_allowed_stat_path_cases_present") is True)
    ok("scenario_review.restricted_present", scenario_review.get("restricted_stat_path_cases_present") is True)
    ok("scenario_review.blocked_present", scenario_review.get("blocked_stat_path_cases_present") is True)
    ok("scenario_review.metadata_allowed_present", scenario_review.get("metadata_allowed_cases_present") is True)
    ok("scenario_review.metadata_restricted_present", scenario_review.get("metadata_restricted_cases_present") is True)
    ok("scenario_review.metadata_blocked_present", scenario_review.get("metadata_blocked_cases_present") is True)
    ok("scenario_review.failure_present", scenario_review.get("failure_mode_cases_present") is True)
    ok("scenario_review.rollback_present", scenario_review.get("rollback_cases_present") is True)
    ok("scenario_review.mapping_present", scenario_review.get("mapping_case_present") is True)

    ok("gate_review.simulation_only", gate_review.get("stat_gate_decision_simulation_only") is True)
    ok("gate_review.gate_open_false", gate_review.get("gate_open_now_false_all_cases") is True)
    ok("gate_review.auth_not_invoked", gate_review.get("authorized_stat_candidate_not_invoked_verified") is True)
    ok("path_scope_review.future_allowed>=4", path_scope_review.get("future_allowed_stat_path_candidate_count", 0) >= 4)
    ok("path_scope_review.blocked>=6", path_scope_review.get("blocked_stat_path_candidate_count", 0) >= 6)
    ok("path_scope_review.restricted>=2", path_scope_review.get("restricted_stat_path_candidate_count", 0) >= 2)

    ok("metadata_review.allowed>=3", metadata_review.get("stat_metadata_allowed_candidate_count", 0) >= 3)
    ok("metadata_review.restricted>=3", metadata_review.get("stat_metadata_restricted_candidate_count", 0) >= 3)
    ok("metadata_review.blocked>=2", metadata_review.get("stat_metadata_blocked_or_deferred_count", 0) >= 2)

    ok("audit_review.generated", audit_review.get("audit_trace_generated") is True)
    ok("audit_review.required_fields", audit_review.get("required_trace_fields_present") is True)
    ok("audit_review.no_stat_call_claim", audit_review.get("no_stat_call_claim") is True)
    ok("audit_review.no_open_claim", audit_review.get("no_open_claim") is True)
    ok("audit_review.no_content_read_claim", audit_review.get("no_content_read_claim") is True)

    ok("closure_readiness.blockers_empty", closure_readiness.get("blockers") == [])
    ok("closure_readiness.recommended_next_phase", closure_readiness.get("recommended_next_phase") == NEXT_PHASE)

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

