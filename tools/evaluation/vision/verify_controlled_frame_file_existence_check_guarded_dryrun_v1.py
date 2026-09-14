#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Controlled Frame File Existence Check Guarded DryRun v1 (gate decision simulation only)."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

PHASE_ID = "Phase-Controlled-Frame-File-Existence-Check-Guarded-DryRun-v1-001"
FINAL_DECISION = "CONTROLLED_FRAME_FILE_EXISTENCE_CHECK_GUARDED_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
NEXT_PHASE = "Phase-Controlled-Frame-File-Existence-Check-Guarded-Post-DryRun-Review-v1-001"

MIN_CHECKS = 240
BASELINE_REQUIREMENT = 200

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
    "user_upload_authorization_insufficient",
    "system_generated_path_insufficient",
    "authorized_candidate_but_not_invoked",
    "gate_denied_behavior",
    "permission_denied_future_failure_mode",
    "missing_file_future_failure_mode",
    "rollback_after_denied_candidate",
]


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-root",
        default=str(repo_root / "_eval_out" / "controlled_frame_file_existence_check_guarded_dryrun_v1_smoke_v0"),
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
    request_stub_schema = _load_json(root / "simulated_file_existence_check_request_stub_schema.json")
    gate_schema = _load_json(root / "file_existence_gate_decision_candidate_schema.json")
    path_scope_schema = _load_json(root / "path_scope_dryrun_decision_candidate_schema.json")
    auth_schema = _load_json(root / "file_existence_authorization_decision_candidate_schema.json")
    audit_schema = _load_json(root / "file_existence_audit_trace_candidate_schema.json")
    failure_schema = _load_json(root / "file_existence_failure_mode_decision_candidate_schema.json")
    rollback_schema = _load_json(root / "file_existence_rollback_decision_candidate_schema.json")
    mapping_schema = _load_json(root / "existence_check_to_file_metadata_mapping_decision_candidate_schema.json")
    result_schema = _load_json(root / "file_existence_check_guarded_dryrun_result_schema.json")

    scenario_matrix = _load_json(root / "controlled_frame_file_existence_check_guarded_dryrun_scenario_matrix.json")
    dryrun_results = _load_json(root / "controlled_frame_file_existence_check_guarded_dryrun_results.json")
    gate_results = _load_json(root / "file_existence_gate_decision_results.json")
    path_scope_results = _load_json(root / "path_scope_dryrun_decision_results.json")
    auth_results = _load_json(root / "authorization_decision_results.json")
    audit_results = _load_json(root / "audit_trace_results.json")
    failure_results = _load_json(root / "failure_mode_decision_results.json")
    rollback_results = _load_json(root / "rollback_decision_results.json")
    mapping_results = _load_json(root / "existence_to_file_metadata_mapping_results.json")
    request_results = _load_json(root / "simulated_request_stub_results.json")

    boundary_matrix = _load_json(root / "file_existence_check_boundary_matrix.json")
    governance_debt = _load_json(root / "governance_debt_register.json")
    next_phase = _load_json(root / "next_phase_recommendation.json")
    no_file_op = _load_json(root / "no_file_operation_boundary_report.json")
    no_runtime = _load_json(root / "no_runtime_boundary_report.json")
    no_write = _load_json(root / "no_write_boundary_report.json")

    rows = input_root_matrix.get("rows", [])
    idx = {row.get("intake_id"): row for row in rows}
    for intake_id in (
        "controlled_frame_file_existence_check_guarded_planning",
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
        "dryrun_case_schema_defined",
        "simulated_file_existence_check_request_stub_schema_defined",
        "file_existence_gate_decision_candidate_schema_defined",
        "path_scope_dryrun_decision_candidate_schema_defined",
        "file_existence_authorization_decision_candidate_schema_defined",
        "file_existence_audit_trace_candidate_schema_defined",
        "file_existence_failure_mode_decision_candidate_schema_defined",
        "file_existence_rollback_decision_candidate_schema_defined",
        "existence_check_to_file_metadata_mapping_decision_candidate_schema_defined",
        "file_existence_check_guarded_dryrun_result_schema_defined",
        "scenario_matrix_generated",
        "dryrun_results_generated",
        "audit_trace_generated",
        "existence_to_file_metadata_mapping_generated",
        "existence_gate_decision_simulation_only",
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

    ok("summary.scenario_count>=22", summary.get("scenario_count", 0) >= 22, summary.get("scenario_count"))
    ok(
        "summary.future_allowed_path_candidate_count>=4",
        summary.get("future_allowed_path_candidate_count", 0) >= 4,
        summary.get("future_allowed_path_candidate_count"),
    )
    ok("summary.blocked_path_candidate_count>=6", summary.get("blocked_path_candidate_count", 0) >= 6, summary.get("blocked_path_candidate_count"))
    ok(
        "summary.restricted_path_candidate_count>=2",
        summary.get("restricted_path_candidate_count", 0) >= 2,
        summary.get("restricted_path_candidate_count"),
    )
    ok(
        "summary.authorization_failure_case_count>=2",
        summary.get("authorization_failure_case_count", 0) >= 2,
        summary.get("authorization_failure_case_count"),
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

    ok("summary.dryrun_scope", summary.get("dryrun_scope") == "controlled_frame_file_existence_check_guarded_dryrun_only")
    ok("summary.violations", summary.get("violations") == [])
    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)

    ok("schema.case", dryrun_case_schema.get("schema_name") == "ControlledFrameFileExistenceCheckGuardedDryRunCase")
    ok("schema.request_stub.invariants", request_stub_schema.get("invariants", {}).get("current_exists_call_allowed") is False)
    ok("schema.gate.values>=6", len(gate_schema.get("gate_decision_values", [])) >= 6)
    ok("schema.result.refs", "gate_decision_ref" in {f["name"] for f in result_schema.get("field_specs", [])})

    scenario_rows = scenario_matrix.get("scenarios", [])
    scenario_idx = {row.get("scenario_id"): row for row in scenario_rows}
    ok("scenarios.count>=22", scenario_matrix.get("scenario_count", 0) >= 22, scenario_matrix.get("scenario_count"))
    for sid in REQUIRED_SCENARIO_IDS:
        row = scenario_idx.get(sid, {})
        ok(f"scenario.{sid}.present", sid in scenario_idx)
        ok(f"scenario.{sid}.simulation_only", row.get("existence_gate_decision_simulation_only") is True)
        ok(f"scenario.{sid}.exists", row.get("exists_call_invoked") is False)
        ok(f"scenario.{sid}.stat", row.get("stat_invoked") is False)

    ok("dryrun_results.count>=22", dryrun_results.get("result_count", 0) >= 22, dryrun_results.get("result_count"))
    ok("gate_results.count>=22", gate_results.get("decision_count", 0) >= 22, gate_results.get("decision_count"))
    ok("path_scope_results.count>=22", path_scope_results.get("decision_count", 0) >= 22, path_scope_results.get("decision_count"))
    ok("auth_results.count>=22", auth_results.get("decision_count", 0) >= 22, auth_results.get("decision_count"))
    ok("audit_results.count>=22", audit_results.get("decision_count", 0) >= 22, audit_results.get("decision_count"))
    ok("failure_results.count>=22", failure_results.get("decision_count", 0) >= 22, failure_results.get("decision_count"))
    ok("rollback_results.count>=22", rollback_results.get("decision_count", 0) >= 22, rollback_results.get("decision_count"))
    ok("mapping_results.count>=22", mapping_results.get("decision_count", 0) >= 22, mapping_results.get("decision_count"))
    ok("request_results.count>=22", request_results.get("request_count", 0) >= 22, request_results.get("request_count"))

    # Key decision presence checks
    gate_decisions = gate_results.get("decisions", [])
    ok("gate.future_allowed", any(d.get("gate_decision") == "future_allowed_candidate_not_invoked" for d in gate_decisions))
    ok("gate.restricted", any(d.get("gate_decision") == "restricted_requires_manual_review" for d in gate_decisions))
    ok("gate.blocked_path", any(d.get("gate_decision") == "blocked_path_scope" for d in gate_decisions))
    ok("gate.blocked_source_chain", any(d.get("gate_decision") == "blocked_missing_source_chain" for d in gate_decisions))
    ok("gate.blocked_privacy", any(d.get("gate_decision") == "blocked_missing_privacy_tags" for d in gate_decisions))
    ok("gate.blocked_fixture", any(d.get("gate_decision") == "blocked_missing_fixture_registry_ref" for d in gate_decisions))
    ok("gate.blocked_auth", any(d.get("gate_decision") == "blocked_authorization_insufficient" for d in gate_decisions))
    ok("gate.denied", any(d.get("gate_decision") == "blocked_gate_denied" for d in gate_decisions))
    for d in gate_decisions:
        ok(f"gate.{d.get('gate_decision_id')}.no_exists", d.get("exists_call_invoked") is False)
        ok(f"gate.{d.get('gate_decision_id')}.no_stat", d.get("stat_invoked") is False)
        ok(f"gate.{d.get('gate_decision_id')}.no_verified", d.get("file_exists_verified") is False)

    # Boundary matrix enforcement
    ok("boundary.blocked.os_path_exists", boundary_matrix.get("blocked_now", {}).get("os_path_exists") is True)
    ok("boundary.blocked.pathlib_path_exists", boundary_matrix.get("blocked_now", {}).get("pathlib_path_exists") is True)
    ok("boundary.blocked.file_stat", boundary_matrix.get("blocked_now", {}).get("file_stat") is True)
    ok("boundary.blocked.file_open", boundary_matrix.get("blocked_now", {}).get("file_open") is True)

    ok("governance_debt.topics>=3", len(governance_debt.get("carryover_topics", [])) >= 3)
    ok("next_phase.final", next_phase.get("final_decision") == FINAL_DECISION)
    ok("next_phase.recommended", next_phase.get("recommended_next_phase") == NEXT_PHASE)

    for report_name, report in (("no_file_op", no_file_op), ("no_runtime", no_runtime), ("no_write", no_write)):
        ok(f"{report_name}.no_runtime_executed", report.get("no_runtime_executed") is True)
        ok(f"{report_name}.no_exists", report.get("os_path_exists_invoked") is False)
        ok(f"{report_name}.no_pathlib", report.get("pathlib_exists_invoked") is False)
        ok(f"{report_name}.no_stat", report.get("file_stat_invoked") is False)
        ok(f"{report_name}.no_open", report.get("file_opened") is False)
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

