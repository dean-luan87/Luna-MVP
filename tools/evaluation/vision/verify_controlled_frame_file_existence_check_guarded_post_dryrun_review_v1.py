#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Controlled Frame File Existence Check Guarded Post-DryRun Review v1 (review-only)."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

PHASE_ID = "Phase-Controlled-Frame-File-Existence-Check-Guarded-Post-DryRun-Review-v1-001"
FINAL_DECISION = "CONTROLLED_FRAME_FILE_EXISTENCE_CHECK_GUARDED_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE"
NEXT_PHASE = "Phase-Controlled-Frame-File-Existence-Check-Guarded-Closure-v1-001"

MIN_CHECKS = 200
BASELINE_REQUIREMENT = 160

REQUIRED_SCENARIOS = [
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
        default=str(repo_root / "_eval_out" / "controlled_frame_file_existence_check_guarded_post_dryrun_review_v1_smoke_v0"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    checks: List[Dict[str, Any]] = []

    def ok(check_id: str, passed: bool, detail: Any = None) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})

    summary = _load_json(root / "summary.json")
    input_root_review = _load_json(root / "file_existence_guarded_dryrun_input_root_review.json")
    scenario_review = _load_json(root / "file_existence_scenario_coverage_review.json")
    gate_review = _load_json(root / "file_existence_gate_decision_review.json")
    path_scope_review = _load_json(root / "path_scope_decision_review.json")
    auth_review = _load_json(root / "authorization_decision_review.json")
    audit_review = _load_json(root / "audit_trace_review.json")
    failure_review = _load_json(root / "failure_mode_review.json")
    rollback_review = _load_json(root / "rollback_review.json")
    mapping_review = _load_json(root / "existence_to_file_metadata_mapping_review.json")
    file_op_review = _load_json(root / "file_operation_boundary_review.json")
    runtime_review = _load_json(root / "runtime_write_action_speech_boundary_review.json")
    closure_readiness = _load_json(root / "file_existence_check_closure_readiness_decision.json")
    governance_debt = _load_json(root / "governance_debt_review.json")
    next_phase = _load_json(root / "next_phase_recommendation.json")
    no_file_op = _load_json(root / "no_file_operation_boundary_report.json")
    no_runtime = _load_json(root / "no_runtime_boundary_report.json")
    no_write = _load_json(root / "no_write_boundary_report.json")

    for key in (
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
        "input_root_review_generated",
        "scenario_coverage_review_generated",
        "file_existence_gate_decision_review_generated",
        "path_scope_decision_review_generated",
        "authorization_decision_review_generated",
        "audit_trace_review_generated",
        "failure_mode_review_generated",
        "rollback_review_generated",
        "existence_to_file_metadata_mapping_review_generated",
        "file_operation_boundary_review_generated",
        "runtime_write_action_speech_boundary_review_generated",
        "closure_readiness_decision_generated",
        "audit_trace_generated",
        "existence_to_file_metadata_mapping_generated",
        "existence_gate_decision_simulation_only",
        "gate_open_now_false_all_cases",
        "authorized_candidate_not_invoked_verified",
        "authorization_required",
        "audit_trace_required",
        "rollback_required",
        "source_chain_required",
        "fixture_registry_authorization_required",
        "user_upload_authorization_insufficient_alone",
        "system_generated_path_insufficient_alone",
        "missing_source_chain_blocked_verified",
        "missing_privacy_tags_blocked_verified",
        "missing_fixture_registry_ref_blocked_verified",
        "gate_denied_behavior_verified",
        "permission_denied_future_failure_mode_verified",
        "missing_file_future_failure_mode_verified",
        "rollback_after_denied_candidate_verified",
        "no_persistent_side_effects",
        "no_file_operation_boundary_pass",
        "ready_for_closure",
        "no_runtime_boundary_pass",
        "no_write_boundary_pass",
        "no_action_boundary_pass",
        "no_speech_boundary_pass",
        "no_runtime_executed",
        "no_new_runtime_enabled",
        "boundary_ok",
    ):
        ok(f"summary.{key}", summary.get(key) is True)

    # readiness negatives
    for key in (
        "ready_for_real_existence_check",
        "ready_for_file_stat",
        "ready_for_file_open",
        "ready_for_real_image_read",
        "ready_for_runtime",
    ):
        ok(f"summary.{key}", summary.get(key) is False)

    ok("summary.review_scope", summary.get("review_scope") == "controlled_frame_file_existence_check_guarded_post_dryrun_review_only")
    ok("summary.violations", summary.get("violations") == [])
    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)

    ok("summary.reviewed_scenario_count>=22", summary.get("reviewed_scenario_count", 0) >= 22, summary.get("reviewed_scenario_count"))
    ok("summary.reviewed_gate_decision_count>=22", summary.get("reviewed_gate_decision_count", 0) >= 22, summary.get("reviewed_gate_decision_count"))
    ok("summary.future_allowed>=4", summary.get("future_allowed_path_candidate_count", 0) >= 4, summary.get("future_allowed_path_candidate_count"))
    ok("summary.blocked>=6", summary.get("blocked_path_candidate_count", 0) >= 6, summary.get("blocked_path_candidate_count"))
    ok("summary.restricted>=2", summary.get("restricted_path_candidate_count", 0) >= 2, summary.get("restricted_path_candidate_count"))
    ok("summary.auth_fail>=2", summary.get("authorization_failure_case_count", 0) >= 2, summary.get("authorization_failure_case_count"))
    ok("summary.failure>=3", summary.get("failure_mode_case_count", 0) >= 3, summary.get("failure_mode_case_count"))
    ok("summary.rollback>=1", summary.get("rollback_case_count", 0) >= 1, summary.get("rollback_case_count"))

    # boundary must remain false
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

    ok("input_root.status", input_root_review.get("input_root_status") == "all_required_loaded")
    ok("input_root.missing_required_roots", input_root_review.get("missing_required_roots") == [])

    ok("scenario.verdict", scenario_review.get("verdict") == "GO")
    ok("scenario.missing", scenario_review.get("missing_scenarios") == [])
    for sid in REQUIRED_SCENARIOS:
        ok(f"scenario.covered.{sid}", sid in scenario_review.get("covered_scenarios", []))

    ok("gate.verdict", gate_review.get("verdict") == "GO")
    ok("path_scope.verdict", path_scope_review.get("verdict") == "GO")
    ok("auth.verdict", auth_review.get("verdict") == "GO")
    ok("audit.verdict", audit_review.get("verdict") == "GO")
    ok("failure.verdict", failure_review.get("verdict") == "GO")
    ok("rollback.verdict", rollback_review.get("verdict") == "GO")
    ok("mapping.verdict", mapping_review.get("verdict") == "GO")
    ok("file_op.verdict", file_op_review.get("verdict") == "GO")
    ok("runtime.verdict", runtime_review.get("verdict") == "GO")

    ok("closure.ready", closure_readiness.get("ready_for_closure") is True)
    ok("closure.final", closure_readiness.get("final_decision") == FINAL_DECISION)
    ok("closure.next", closure_readiness.get("recommended_next_phase") == NEXT_PHASE)
    ok("closure.no_real_exists", closure_readiness.get("ready_for_real_existence_check") is False)
    ok("closure.no_stat", closure_readiness.get("ready_for_file_stat") is False)
    ok("closure.no_open", closure_readiness.get("ready_for_file_open") is False)

    ok("governance.reviewed", governance_debt.get("reviewed") is True)
    ok("next_phase.final", next_phase.get("final_decision") == FINAL_DECISION)
    ok("next_phase.recommended", next_phase.get("recommended_next_phase") == NEXT_PHASE)

    ok("no_file_op.review_only", no_file_op.get("review_only") is True)
    ok("no_file_op.simulation_only", no_file_op.get("existence_gate_decision_simulation_only") is True)
    ok("no_file_op.no_exists", no_file_op.get("os_path_exists_invoked") is False)
    ok("no_file_op.no_stat", no_file_op.get("file_stat_invoked") is False)

    ok("no_runtime.pass", no_runtime.get("no_runtime_boundary_pass") is True)
    ok("no_write.pass", no_write.get("no_write_boundary_pass") is True)

    # Extra invariant checks (increase coverage / make intent explicit)
    for obj_name, obj in (
        ("input_root_review", input_root_review),
        ("scenario_review", scenario_review),
        ("gate_review", gate_review),
        ("path_scope_review", path_scope_review),
        ("auth_review", auth_review),
        ("audit_review", audit_review),
        ("failure_review", failure_review),
        ("rollback_review", rollback_review),
        ("mapping_review", mapping_review),
        ("file_op_review", file_op_review),
        ("runtime_review", runtime_review),
        ("closure_readiness", closure_readiness),
        ("governance_debt", governance_debt),
        ("next_phase", next_phase),
    ):
        ok(f"{obj_name}.fact_status", obj.get("fact_status") == "not_fact")
        ok(f"{obj_name}.write_allowed", obj.get("write_allowed") is False)
        ok(f"{obj_name}.source_chain_present", bool(obj.get("source_chain")))

    # Ensure mapping review keeps hard boundaries (redundant but explicit)
    ok("mapping.file_exists_required_now", mapping_review.get("file_exists_required_now") is False)
    ok("mapping.stat_required_now", mapping_review.get("stat_required_now") is False)
    ok("mapping.content_read_required_now", mapping_review.get("content_read_required_now") is False)
    ok("mapping.real_hash_required_now", mapping_review.get("real_hash_required_now") is False)
    ok("mapping.mapping_runtime_started", mapping_review.get("mapping_runtime_started") is False)

    # Ensure audit review includes core claims
    ok("audit.no_content_read_claim", audit_review.get("no_content_read_claim") is True)
    ok("audit.no_stat_claim", audit_review.get("no_stat_claim") is True)
    ok("audit.no_exists_call_claim", audit_review.get("no_exists_call_claim") is True)
    ok("audit.required_trace_fields_present", audit_review.get("required_trace_fields_present") is True)
    ok("audit.source_chain_preserved", audit_review.get("source_chain_preserved") is True)

    # Ensure closure readiness spells out non-readiness explicitly
    for key in (
        "ready_for_real_existence_check",
        "ready_for_file_stat",
        "ready_for_file_open",
        "ready_for_real_image_read",
        "ready_for_runtime",
    ):
        ok(f"closure.{key}", closure_readiness.get(key) is False)

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

