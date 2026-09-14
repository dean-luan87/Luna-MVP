#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Controlled Frame File Stat Guarded Planning v1 (planning-only)."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

PHASE_ID = "Phase-Controlled-Frame-File-Stat-Guarded-Planning-v1-001"
FINAL_DECISION = "CONTROLLED_FRAME_FILE_STAT_GUARDED_PLANNING_READY_FOR_DRYRUN"
NEXT_PHASE = "Phase-Controlled-Frame-File-Stat-Guarded-DryRun-v1-001"

MIN_CHECKS = 220
BASELINE_REQUIREMENT = 180

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
    "authorized_stat_candidate_but_not_invoked",
    "stat_metadata_allowed_candidate",
    "stat_metadata_restricted_candidate",
    "stat_metadata_blocked_or_deferred",
    "stat_permission_denied_future_failure_mode",
    "stat_missing_file_future_failure_mode",
    "stat_gate_denied_behavior",
    "stat_rollback_after_denied_candidate",
]


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-root",
        default=str(repo_root / "_eval_out" / "controlled_frame_file_stat_guarded_planning_v1_smoke_v0"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    checks: List[Dict[str, Any]] = []

    def ok(check_id: str, passed: bool, detail: Any = None) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})

    # ---- Load artifacts ----
    summary = _load_json(root / "summary.json")
    input_root_matrix = _load_json(root / "input_root_matrix.json")
    planning_policy = _load_json(root / "controlled_frame_file_stat_guarded_planning_policy.json")
    gate_policy = _load_json(root / "file_stat_gate_policy.json")
    exposure_policy = _load_json(root / "file_stat_metadata_exposure_boundary_policy.json")
    allowed_scope = _load_json(root / "allowed_stat_path_scope_policy.json")
    blocked_scope = _load_json(root / "blocked_stat_path_scope_policy.json")
    auth_policy = _load_json(root / "file_stat_authorization_policy.json")
    audit_policy = _load_json(root / "file_stat_audit_trace_policy.json")
    failure_policy = _load_json(root / "file_stat_failure_mode_policy.json")
    rollback_policy = _load_json(root / "file_stat_rollback_policy.json")
    candidate_schema = _load_json(root / "file_stat_decision_candidate_schema.json")
    mapping_policy = _load_json(root / "stat_to_file_metadata_candidate_mapping_policy.json")
    scenario_matrix = _load_json(root / "controlled_frame_file_stat_guarded_planning_scenario_matrix.json")
    boundary_matrix = _load_json(root / "file_stat_boundary_matrix.json")
    governance_debt = _load_json(root / "governance_debt_register.json")
    next_phase = _load_json(root / "next_phase_recommendation.json")
    no_file_op = _load_json(root / "no_file_operation_boundary_report.json")
    no_runtime = _load_json(root / "no_runtime_boundary_report.json")
    no_write = _load_json(root / "no_write_boundary_report.json")

    # ---- Input checks ----
    rows = input_root_matrix.get("rows", [])
    idx = {row.get("intake_id"): row for row in rows}

    required_intakes = (
        "post_file_existence_check_roadmap_decision",
        "file_existence_check_guarded_closure",
        "file_existence_check_guarded_post_review",
        "file_existence_check_guarded_dryrun",
        "file_existence_check_guarded_planning",
        "post_file_metadata_boundary_roadmap_decision",
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
    )
    for intake_id in required_intakes:
        ok(f"input.{intake_id}.loaded", idx.get(intake_id, {}).get("loaded") is True)

    optional_intakes = (
        "vision_frame_trace_stream_registry",
        "vision_frame_input_governance",
        "vision_roi_proposal_stub",
        "system_health_hardware_profile",
        "simulation_lab_profile",
        "privacy_governance_docs",
    )
    for intake_id in optional_intakes:
        ok(
            f"input.{intake_id}.optional_status",
            idx.get(intake_id, {}).get("status") in {"loaded", "optional_missing"},
            idx.get(intake_id, {}).get("status"),
        )

    # ---- Summary: loaded flags ----
    must_true_keys = [
        "post_file_existence_check_roadmap_input_loaded",
        "file_existence_check_guarded_closure_input_loaded",
        "file_existence_check_guarded_post_review_input_loaded",
        "file_existence_check_guarded_dryrun_input_loaded",
        "file_existence_check_guarded_planning_input_loaded",
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
        "controlled_frame_file_stat_guarded_planning_policy_defined",
        "file_stat_gate_policy_defined",
        "file_stat_metadata_exposure_boundary_policy_defined",
        "allowed_stat_path_scope_policy_defined",
        "blocked_stat_path_scope_policy_defined",
        "file_stat_authorization_policy_defined",
        "file_stat_audit_trace_policy_defined",
        "file_stat_failure_mode_policy_defined",
        "file_stat_rollback_policy_defined",
        "file_stat_decision_candidate_schema_defined",
        "stat_to_file_metadata_candidate_mapping_policy_defined",
        "scenario_matrix_generated",
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
    ]
    for key in must_true_keys:
        ok(f"summary.{key}", summary.get(key) is True)

    ok("summary.planning_scope", summary.get("planning_scope") == "controlled_frame_file_stat_guarded_planning_only")
    ok("summary.violations", summary.get("violations") == [])
    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)

    # ---- Summary: counts ----
    ok("summary.scenario_count>=24", summary.get("scenario_count", 0) >= 24, summary.get("scenario_count"))
    ok(
        "summary.future_allowed_stat_path_candidate_count>=4",
        summary.get("future_allowed_stat_path_candidate_count", 0) >= 4,
        summary.get("future_allowed_stat_path_candidate_count"),
    )
    ok(
        "summary.blocked_stat_path_candidate_count>=6",
        summary.get("blocked_stat_path_candidate_count", 0) >= 6,
        summary.get("blocked_stat_path_candidate_count"),
    )
    ok(
        "summary.restricted_stat_path_candidate_count>=2",
        summary.get("restricted_stat_path_candidate_count", 0) >= 2,
        summary.get("restricted_stat_path_candidate_count"),
    )
    ok(
        "summary.stat_metadata_allowed_candidate_count>=3",
        summary.get("stat_metadata_allowed_candidate_count", 0) >= 3,
        summary.get("stat_metadata_allowed_candidate_count"),
    )
    ok(
        "summary.stat_metadata_restricted_candidate_count>=3",
        summary.get("stat_metadata_restricted_candidate_count", 0) >= 3,
        summary.get("stat_metadata_restricted_candidate_count"),
    )
    ok(
        "summary.stat_metadata_blocked_or_deferred_count>=2",
        summary.get("stat_metadata_blocked_or_deferred_count", 0) >= 2,
        summary.get("stat_metadata_blocked_or_deferred_count"),
    )
    ok(
        "summary.failure_mode_case_count>=3",
        summary.get("failure_mode_case_count", 0) >= 3,
        summary.get("failure_mode_case_count"),
    )
    ok(
        "summary.rollback_case_count>=1",
        summary.get("rollback_case_count", 0) >= 1,
        summary.get("rollback_case_count"),
    )

    # ---- Summary: hard boundary false keys ----
    must_false_keys = [
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
    ]
    for key in must_false_keys:
        ok(f"summary.{key}", summary.get(key) is False)

    # ---- Policy/schema sanity checks ----
    ok("planning_policy.planning_only", planning_policy.get("planning_only") is True)
    ok("planning_policy.stat_allowed_now", planning_policy.get("stat_allowed_now") is False)
    ok("planning_policy.stat_gate_ref", planning_policy.get("file_stat_gate_ref") == "file_stat_gate_policy.json")
    ok("planning_policy.allowed_scope_ref", planning_policy.get("allowed_path_scope_policy_ref") == "allowed_stat_path_scope_policy.json")
    ok("planning_policy.blocked_scope_ref", planning_policy.get("blocked_path_scope_policy_ref") == "blocked_stat_path_scope_policy.json")
    ok(
        "planning_policy.existence_inherited_ref.present",
        isinstance(planning_policy.get("inherited_file_existence_check_ref"), str) and bool(planning_policy.get("inherited_file_existence_check_ref")),
        planning_policy.get("inherited_file_existence_check_ref"),
    )

    ok("gate_policy.closed", gate_policy.get("current_phase_gate_open") is False)
    ok("gate_policy.future", gate_policy.get("future_gate_candidate") is True)
    ok("gate_policy.separate_from_exists", any("separate" in s for s in gate_policy.get("risk_notes", [])), gate_policy.get("risk_notes"))
    ok("gate_policy.veto_count>=6", len(gate_policy.get("veto_conditions", [])) >= 6, len(gate_policy.get("veto_conditions", [])))

    ok("exposure_policy.output_candidate_only", exposure_policy.get("output_candidate_only") is True)
    ok("exposure_policy.privacy_risk_level", exposure_policy.get("privacy_risk_level") in {"medium", "high"}, exposure_policy.get("privacy_risk_level"))
    ok(
        "exposure_policy.allowed_count>=3",
        len(exposure_policy.get("allowed_stat_metadata_candidate", [])) >= 3,
        len(exposure_policy.get("allowed_stat_metadata_candidate", [])),
    )
    ok(
        "exposure_policy.restricted_count>=3",
        len(exposure_policy.get("restricted_stat_metadata_candidate", [])) >= 3,
        len(exposure_policy.get("restricted_stat_metadata_candidate", [])),
    )
    ok(
        "exposure_policy.blocked_count>=2",
        len(exposure_policy.get("blocked_stat_metadata_candidate", [])) >= 2,
        len(exposure_policy.get("blocked_stat_metadata_candidate", [])),
    )

    allowed_entries = allowed_scope.get("allowed_for_future_stat_candidate", [])
    ok("allowed_scope.count>=4", len(allowed_entries) >= 4, len(allowed_entries))
    ok("allowed_scope.allowed_now", allowed_scope.get("allowed_now") is False)
    for i, entry in enumerate(allowed_entries[:6]):
        ok(f"allowed_scope.entry[{i}].requires_registry_ref", entry.get("required_registry_ref") is True)
        ok(f"allowed_scope.entry[{i}].requires_privacy_tags", entry.get("required_privacy_tags") is True)
        ok(f"allowed_scope.entry[{i}].requires_review_status", entry.get("required_review_status") is True)

    ok("blocked_scope.blocked_now", blocked_scope.get("blocked_now") is True)
    ok("blocked_scope.blocked_types>=6", len(blocked_scope.get("blocked_path_types", [])) >= 6, len(blocked_scope.get("blocked_path_types", [])))
    ok("blocked_scope.restricted_types>=2", len(blocked_scope.get("restricted_path_types", [])) >= 2, len(blocked_scope.get("restricted_path_types", [])))

    ok("auth.authorization_required", auth_policy.get("authorization_required") is True)
    ok("auth.fixture_registry_required", auth_policy.get("fixture_registry_authorization_required") is True)
    ok("auth.exists_pass_insufficient", auth_policy.get("existence_check_pass_insufficient_alone") is True)
    ok("audit.audit_required", audit_policy.get("audit_required") is True)
    ok("audit.trace_required", audit_policy.get("trace_required") is True)
    ok("rollback.rollback_required", rollback_policy.get("rollback_required") is True)
    ok("failure.no_worldmodel_write", failure_policy.get("no_worldmodel_write") is True)
    ok("failure.no_task_action", failure_policy.get("no_task_action") is True)

    ok("candidate_schema.invariants.stat_status", candidate_schema.get("invariants", {}).get("stat_status") == "not_checked")
    ok("candidate_schema.invariants.os_stat_invoked", candidate_schema.get("invariants", {}).get("os_stat_invoked") is False)
    ok("candidate_schema.invariants.pathlib_stat_invoked", candidate_schema.get("invariants", {}).get("pathlib_stat_invoked") is False)
    ok("mapping.output_status", mapping_policy.get("output_status") == "planning_only")
    ok("mapping.stat_required_now", mapping_policy.get("stat_required_now") is False)
    ok("mapping.exists_required_now", mapping_policy.get("exists_required_now") is False)

    # ---- Scenario matrix checks ----
    scenario_rows = scenario_matrix.get("scenarios", [])
    scenario_idx = {row.get("scenario_id"): row for row in scenario_rows}
    ok("scenarios.count>=24", scenario_matrix.get("scenario_count", 0) >= 24, scenario_matrix.get("scenario_count"))
    for sid in REQUIRED_SCENARIO_IDS:
        row = scenario_idx.get(sid, {})
        ok(f"scenario.{sid}.present", sid in scenario_idx)
        ok(f"scenario.{sid}.planning_only", row.get("planning_only") is True)
        ok(f"scenario.{sid}.current_stat_invoked", row.get("current_stat_invoked") is False)
        ok(f"scenario.{sid}.os_stat_invoked", row.get("os_stat_invoked") is False)
        ok(f"scenario.{sid}.pathlib_stat_invoked", row.get("pathlib_stat_invoked") is False)
        ok(f"scenario.{sid}.lstat_invoked", row.get("lstat_invoked") is False)
        ok(f"scenario.{sid}.file_stat_verified", row.get("file_stat_verified") is False)
        ok(f"scenario.{sid}.stat_status", row.get("stat_status") == "not_checked", row.get("stat_status"))

    # ---- Boundary matrix checks ----
    ok("boundary_matrix.blocked.file_stat", boundary_matrix.get("blocked_now", {}).get("file_stat") is True)
    ok("boundary_matrix.blocked.os_stat", boundary_matrix.get("blocked_now", {}).get("os_stat") is True)
    ok("boundary_matrix.blocked.pathlib_stat", boundary_matrix.get("blocked_now", {}).get("pathlib_stat") is True)
    ok("boundary_matrix.blocked.lstat", boundary_matrix.get("blocked_now", {}).get("lstat") is True)
    ok("boundary_matrix.blocked.exists", boundary_matrix.get("blocked_now", {}).get("os_path_exists") is True)
    ok("boundary_matrix.blocked.pathlib_exists", boundary_matrix.get("blocked_now", {}).get("pathlib_path_exists") is True)
    ok("boundary_matrix.blocked.file_open", boundary_matrix.get("blocked_now", {}).get("file_open") is True)

    ok("governance_debt.topics>=4", len(governance_debt.get("carryover_topics", [])) >= 4)
    ok("next_phase.final", next_phase.get("final_decision") == FINAL_DECISION)
    ok("next_phase.recommended", next_phase.get("recommended_next_phase") == NEXT_PHASE)

    # ---- No-file-op/no-runtime/no-write reports must mirror hard boundary ----
    report_groups = (("no_file_op", no_file_op), ("no_runtime", no_runtime), ("no_write", no_write))
    for report_name, report in report_groups:
        ok(f"{report_name}.no_runtime_executed", report.get("no_runtime_executed") is True)
        ok(f"{report_name}.stat_invoked", report.get("stat_invoked") is False)
        ok(f"{report_name}.os_stat_invoked", report.get("os_stat_invoked") is False)
        ok(f"{report_name}.pathlib_stat_invoked", report.get("pathlib_stat_invoked") is False)
        ok(f"{report_name}.lstat_invoked", report.get("lstat_invoked") is False)
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

