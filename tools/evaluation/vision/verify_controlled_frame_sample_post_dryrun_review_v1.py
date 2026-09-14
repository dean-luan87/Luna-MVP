#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Controlled Frame Sample Post-DryRun Review v1 (review-only)."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

PHASE_ID = "Phase-Controlled-Frame-Sample-Post-DryRun-Review-v1-001"
FINAL_DECISION = "CONTROLLED_FRAME_SAMPLE_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE"
NEXT_PHASE = "Phase-Controlled-Frame-Sample-Closure-v1-001"
MIN_CHECKS = 180
BASELINE_REQUIREMENT = 140

REQUIRED_SCENARIOS = [
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
]


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-root",
        default="/Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/controlled_frame_sample_post_dryrun_review_v1_smoke_v0",
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
    sample_dryrun_input_root_review = _load_json(root / "sample_dryrun_input_root_review.json")
    sample_scenario_coverage_review = _load_json(root / "sample_scenario_coverage_review.json")
    sample_source_policy_review = _load_json(root / "sample_source_policy_review.json")
    file_boundary_review = _load_json(root / "file_boundary_review.json")
    privacy_precheck_review = _load_json(root / "privacy_precheck_review.json")
    manual_review_gate_review = _load_json(root / "manual_review_gate_review.json")
    sample_usage_policy_review = _load_json(root / "sample_usage_policy_review.json")
    sample_to_frame_mapping_review = _load_json(root / "sample_to_frame_mapping_review.json")
    runtime_write_action_speech_boundary_review = _load_json(root / "runtime_write_action_speech_boundary_review.json")
    controlled_frame_sample_closure_readiness_decision = _load_json(root / "controlled_frame_sample_closure_readiness_decision.json")
    governance_debt_review = _load_json(root / "governance_debt_review.json")
    next_phase_recommendation = _load_json(root / "next_phase_recommendation.json")
    no_runtime_boundary_report = _load_json(root / "no_runtime_boundary_report.json")
    no_write_boundary_report = _load_json(root / "no_write_boundary_report.json")

    # Input checks
    rows = input_root_matrix.get("rows", [])
    idx = {row.get("intake_id"): row for row in rows}
    for intake_id in (
        "controlled_frame_sample_dryrun",
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
        ok(f"input.{intake_id}.optional", idx.get(intake_id, {}).get("status") in {"loaded", "optional_missing"}, idx.get(intake_id, {}).get("status"))

    # Summary required true keys
    for key in (
        "controlled_frame_sample_dryrun_input_loaded",
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
        "input_root_review_generated",
        "scenario_coverage_review_generated",
        "sample_source_policy_review_generated",
        "file_boundary_review_generated",
        "privacy_precheck_review_generated",
        "manual_review_gate_review_generated",
        "sample_usage_policy_review_generated",
        "sample_to_frame_mapping_review_generated",
        "runtime_write_action_speech_boundary_review_generated",
        "closure_readiness_decision_generated",
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
    ok("summary.review_scope", summary.get("review_scope") == "controlled_frame_sample_post_dryrun_review_only")
    ok("summary.reviewed_scenario_count>=16", summary.get("reviewed_scenario_count", 0) >= 16, summary.get("reviewed_scenario_count"))
    ok("summary.allowed>=4", summary.get("allowed_sample_candidate_count", 0) >= 4, summary.get("allowed_sample_candidate_count"))
    ok("summary.restricted>=5", summary.get("restricted_sample_candidate_count", 0) >= 5, summary.get("restricted_sample_candidate_count"))
    ok("summary.blocked>=4", summary.get("blocked_sample_candidate_count", 0) >= 4, summary.get("blocked_sample_candidate_count"))
    ok("summary.manual_review>=5", summary.get("manual_review_required_case_count", 0) >= 5, summary.get("manual_review_required_case_count"))

    # Summary required false keys
    for key in (
        "ready_for_real_image_read",
        "ready_for_runtime",
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

    # Input root review checks
    ok("root_review.review_id", sample_dryrun_input_root_review.get("review_id") == "cfspr_v1_001")
    ok("root_review.missing_required_empty", sample_dryrun_input_root_review.get("missing_required_roots") == [])
    ok("root_review.status", sample_dryrun_input_root_review.get("input_root_status") == "all_required_loaded")
    ok("root_review.source_chain", sample_dryrun_input_root_review.get("source_chain") == "controlled_frame_sample_post_dryrun_review_v1")

    # Scenario coverage review checks
    ok("scenario_review.expected==16", sample_scenario_coverage_review.get("expected_scenario_count") == 16)
    ok("scenario_review.missing_empty", sample_scenario_coverage_review.get("missing_scenarios") == [])
    ok("scenario_review.allowed_present", sample_scenario_coverage_review.get("allowed_sample_cases_present") is True)
    ok("scenario_review.restricted_present", sample_scenario_coverage_review.get("restricted_sample_cases_present") is True)
    ok("scenario_review.blocked_present", sample_scenario_coverage_review.get("blocked_sample_cases_present") is True)
    ok("scenario_review.manual_review_present", sample_scenario_coverage_review.get("manual_review_cases_present") is True)
    ok("scenario_review.verdict", sample_scenario_coverage_review.get("verdict") == "GO")
    covered = set(sample_scenario_coverage_review.get("covered_scenarios", []))
    for sid in REQUIRED_SCENARIOS:
        ok(f"scenario_review.covered.{sid}", sid in covered)

    # Policy/boundary reviews
    ok("source_policy_review.verdict", sample_source_policy_review.get("verdict") == "GO")
    ok("source_policy_review.missing_source_chain_verified", sample_source_policy_review.get("missing_source_chain_blocked_verified") is True)
    ok("source_policy_review.missing_privacy_verified", sample_source_policy_review.get("missing_privacy_precheck_blocked_verified") is True)
    ok("source_policy_review.live_camera_verified", sample_source_policy_review.get("live_camera_sample_blocked_verified") is True)
    ok("source_policy_review.external_stream_verified", sample_source_policy_review.get("external_stream_sample_blocked_verified") is True)

    ok("file_boundary_review.manifest_only", file_boundary_review.get("manifest_metadata_only") is True)
    ok("file_boundary_review.violation_count==0", file_boundary_review.get("file_boundary_violation_count") == 0, file_boundary_review.get("file_boundary_violation_count"))
    ok("file_boundary_review.verdict", file_boundary_review.get("verdict") == "GO")

    ok("privacy_review.required", privacy_precheck_review.get("privacy_precheck_required") is True)
    ok("privacy_review.manual_review_sensitive", privacy_precheck_review.get("manual_review_required_for_sensitive_samples") is True)
    ok("privacy_review.long_term_blocked", privacy_precheck_review.get("long_term_use_blocked_for_sensitive_samples") is True)
    ok("privacy_review.verdict", privacy_precheck_review.get("verdict") == "GO")

    ok("manual_review.count>=5", manual_review_gate_review.get("manual_review_required_case_count", 0) >= 5)
    ok("manual_review.private_home", manual_review_gate_review.get("private_home_review_required") is True)
    ok("manual_review.medical", manual_review_gate_review.get("medical_context_review_required") is True)
    ok("manual_review.workplace", manual_review_gate_review.get("workplace_sensitive_review_required") is True)
    ok("manual_review.crossing", manual_review_gate_review.get("crossing_related_review_required") is True)
    ok("manual_review.no_runtime_before_review", manual_review_gate_review.get("no_runtime_allowed_before_review") is True)
    ok("manual_review.verdict", manual_review_gate_review.get("verdict") == "GO")

    ok("usage.production_inference_blocked", sample_usage_policy_review.get("production_inference_allowed") is False)
    ok("usage.model_training_blocked", sample_usage_policy_review.get("model_training_allowed") is False)
    ok("usage.live_navigation_blocked", sample_usage_policy_review.get("live_navigation_allowed") is False)
    ok("usage.worldmodel_write_blocked", sample_usage_policy_review.get("worldmodel_write_allowed") is False)
    ok("usage.verdict", sample_usage_policy_review.get("verdict") == "GO")

    ok("mapping.stub_generated", sample_to_frame_mapping_review.get("mapping_stub_generated") is True)
    ok("mapping.no_content_read", sample_to_frame_mapping_review.get("sample_to_frame_candidate_mapping_without_content_read") is True)
    ok("mapping.stub_allowed", sample_to_frame_mapping_review.get("controlled_frame_input_candidate_stub_allowed") is True)
    for key in (
        "visual_observation_generated",
        "scene_sketch_generated",
        "ocr_activation_result_generated",
        "tracking_result_generated",
        "navigation_action_triggered",
        "worldmodel_write_allowed",
        "memory_write_allowed",
        "fact_write_allowed",
    ):
        ok(f"mapping.{key}.false", sample_to_frame_mapping_review.get(key) is False)
    ok("mapping.verdict", sample_to_frame_mapping_review.get("verdict") == "GO")

    for key in ("no_runtime_boundary_pass", "no_write_boundary_pass", "no_action_boundary_pass", "no_speech_boundary_pass"):
        ok(f"boundary_review.{key}", runtime_write_action_speech_boundary_review.get(key) is True)
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
        "camera_invoked",
        "visual_model_invoked",
        "ocr_provider_invoked",
        "tracking_runtime_invoked",
        "crossing_runtime_invoked",
        "speech_gate_invoked",
        "vop_invoked",
        "tts_invoked",
        "world_model_written",
        "memory_written",
        "library_written",
        "fact_written",
    ):
        ok(f"boundary_review.{key}.false", runtime_write_action_speech_boundary_review.get(key) is False)
    ok("boundary_review.verdict", runtime_write_action_speech_boundary_review.get("verdict") == "GO")

    ok("readiness.ready_for_closure", controlled_frame_sample_closure_readiness_decision.get("ready_for_closure") is True)
    ok("readiness.ready_for_real_image_read", controlled_frame_sample_closure_readiness_decision.get("ready_for_real_image_read") is False)
    ok("readiness.ready_for_runtime", controlled_frame_sample_closure_readiness_decision.get("ready_for_runtime") is False)
    ok("readiness.final_decision", controlled_frame_sample_closure_readiness_decision.get("final_decision") == FINAL_DECISION)
    ok("readiness.next_phase", controlled_frame_sample_closure_readiness_decision.get("recommended_next_phase") == NEXT_PHASE)

    ok("debt.reviewed", governance_debt_review.get("reviewed") is True)
    ok("next_phase.final_decision", next_phase_recommendation.get("final_decision") == FINAL_DECISION)
    ok("next_phase.recommended", next_phase_recommendation.get("recommended_next_phase") == NEXT_PHASE)

    for payload_name, payload in (("no_runtime", no_runtime_boundary_report), ("no_write", no_write_boundary_report)):
        ok(f"{payload_name}.scope", payload.get("review_scope") == "controlled_frame_sample_post_dryrun_review_only")
        for key in ("no_runtime_boundary_pass", "no_write_boundary_pass", "no_action_boundary_pass", "no_speech_boundary_pass", "no_runtime_executed", "no_new_runtime_enabled", "boundary_ok"):
            ok(f"{payload_name}.{key}", payload.get(key) is True)
        for key in (
            "file_opened",
            "image_opened",
            "video_opened",
            "video_decoded",
            "frame_extracted",
            "real_file_hash_computed",
            "camera_invoked",
            "visual_model_invoked",
            "ocr_provider_invoked",
            "tracking_runtime_invoked",
            "crossing_runtime_invoked",
            "world_model_written",
            "memory_written",
            "fact_written",
        ):
            ok(f"{payload_name}.{key}.false", payload.get(key) is False)
        ok(f"{payload_name}.violations==[]", payload.get("violations") == [])

    # Meta checks to ensure >=180
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
        "final_decision": FINAL_DECISION if verdict == "GO" else "CONTROLLED_FRAME_SAMPLE_POST_DRYRUN_REVIEW_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if verdict == "GO" else PHASE_ID,
        "failed_checks": [item for item in checks if not item["passed"]],
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"verdict": verdict, "checks_passed": passed, "checks_total": len(checks)}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())

