#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Post File Existence Check Roadmap Decision v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

PHASE_ID = "Phase-Post-File-Existence-Check-Roadmap-Decision-v1-001"
FINAL_DECISION = "POST_FILE_EXISTENCE_CHECK_ROADMAP_DECISION_READY_FOR_FILE_STAT_GUARDED_PLANNING"
NEXT_PHASE = "Phase-Controlled-Frame-File-Stat-Guarded-Planning-v1-001"
MIN_CHECKS = 180
BASELINE_REQUIREMENT = 140


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-root",
        default=str(repo_root / "_eval_out" / "post_file_existence_check_roadmap_decision_v1_smoke_v0"),
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
    current_status = _load_json(root / "current_file_existence_check_status_summary.json")
    route_option_matrix = _load_json(root / "route_option_matrix.json")
    priority_ranking = _load_json(root / "priority_ranking.json")
    _load_json(root / "completed_capability_summary.json")
    _load_json(root / "recommended_next_phase_decision.json")
    _load_json(root / "deferred_real_file_operation_register.json")
    _load_json(root / "deferred_gate_taxonomy_register.json")
    _load_json(root / "deferred_midplatform_governance_register.json")
    _load_json(root / "deferred_resilience_distributed_midplatform_register.json")
    _load_json(root / "deferred_worldmodel_memory_library_emotion_register.json")
    _load_json(root / "boundary_freeze.json")
    _load_json(root / "governance_debt_roadmap_register.json")
    _load_json(root / "non_claims_register.json")
    next_phase_recommendation = _load_json(root / "next_phase_recommendation.json")
    no_file_operation_boundary_report = _load_json(root / "no_file_operation_boundary_report.json")
    no_runtime_boundary_report = _load_json(root / "no_runtime_boundary_report.json")
    no_write_boundary_report = _load_json(root / "no_write_boundary_report.json")

    rows = input_root_matrix.get("rows", [])
    idx = {row.get("intake_id"): row for row in rows}

    for intake_id in (
        "file_existence_check_guarded_closure",
        "file_existence_check_guarded_post_review",
        "file_existence_check_guarded_dryrun",
        "file_existence_check_guarded_planning",
        "post_file_metadata_boundary_roadmap_decision",
        "file_metadata_boundary_closure",
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
        status = idx.get(intake_id, {}).get("status")
        ok(f"input.{intake_id}.optional", status in {"loaded", "optional_missing"}, status)

    ok("input.row_count", input_root_matrix.get("row_count") == len(rows), input_root_matrix.get("row_count"))

    # Summary required true
    ok("summary.decision_scope", summary.get("decision_scope") == "post_file_existence_check_roadmap_decision_only")
    for key in (
        "file_existence_check_guarded_closure_input_loaded",
        "file_existence_check_guarded_post_review_input_loaded",
        "file_existence_check_guarded_dryrun_input_loaded",
        "file_existence_check_guarded_planning_input_loaded",
        "post_file_metadata_boundary_roadmap_input_loaded",
        "file_metadata_boundary_closure_input_loaded",
        "controlled_frame_sample_closure_input_loaded",
        "controlled_frame_input_closure_input_loaded",
        "map_location_readonly_context_input_loaded",
        "safety_constitution_input_loaded",
        "minimal_runtime_integration_closure_loaded",
        "ocr_final_closure_loaded",
        "current_status_summary_generated",
        "completed_capability_summary_generated",
        "route_option_matrix_generated",
        "priority_ranking_generated",
        "recommended_next_phase_decision_generated",
        "deferred_real_file_operation_register_generated",
        "deferred_gate_taxonomy_register_generated",
        "deferred_midplatform_governance_register_generated",
        "deferred_resilience_distributed_midplatform_register_generated",
        "deferred_worldmodel_memory_library_emotion_register_generated",
        "boundary_freeze_generated",
        "governance_debt_roadmap_register_generated",
        "non_claims_register_generated",
        "file_stat_guarded_planning_route_exists",
        "real_file_existence_check_guarded_trial_route_exists",
        "real_metadata_read_guarded_planning_route_exists",
        "real_hash_computation_guarded_planning_route_exists",
        "exif_video_probe_guarded_planning_route_exists",
        "controlled_static_image_read_preplan_route_exists",
        "gate_taxonomy_route_exists",
        "midplatform_function_governance_route_exists",
        "midplatform_resilience_route_exists",
        "offline_distributed_midplatform_route_exists",
        "worldmodel_memory_library_route_exists",
        "exploration_emotion_route_exists",
        "controlled_visual_runtime_route_exists",
        "file_existence_check_guarded_closed",
        "existence_gate_decision_simulation_only",
        "real_exists_call_deferred",
        "real_file_stat_deferred",
        "real_file_open_deferred",
        "real_image_read_deferred",
        "real_video_read_deferred",
        "real_hash_deferred",
        "exif_video_probe_deferred",
        "gate_taxonomy_deferred",
        "midplatform_function_governance_deferred",
        "midplatform_resilience_deferred",
        "offline_distributed_midplatform_deferred",
        "worldmodel_candidate_layer_deferred",
        "memory_library_governance_deferred",
        "exploration_drive_deferred",
        "emotion_engine_deferred",
        "cross_repo_input_roots_observed",
        "output_root_fixed_to_luna_core",
        "no_runtime_executed",
        "no_new_runtime_enabled",
        "boundary_ok",
    ):
        ok(f"summary.{key}", summary.get(key) is True, summary.get(key))

    ok("summary.route_option_count>=12", summary.get("route_option_count", 0) >= 12, summary.get("route_option_count"))
    ok("summary.p0_route_count>=3", summary.get("p0_route_count", 0) >= 3, summary.get("p0_route_count"))
    ok("summary.p1_route_count>=6", summary.get("p1_route_count", 0) >= 6, summary.get("p1_route_count"))
    ok("summary.p2_route_count>=3", summary.get("p2_route_count", 0) >= 3, summary.get("p2_route_count"))

    ok("summary.selected_route", summary.get("selected_route") == "File Stat Guarded Planning")
    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.violations", summary.get("violations") == [])

    # Summary required false
    for key in (
        "real_existence_check_readiness_claimed",
        "file_stat_readiness_claimed",
        "file_open_readiness_claimed",
        "real_image_readiness_claimed",
        "visual_runtime_claimed",
        "production_readiness_claimed",
        "runtime_enablement_claimed",
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
        "emotion_engine_invoked",
    ):
        ok(f"summary.{key}", summary.get(key) is False, summary.get(key))

    # Current status checks
    for key in (
        "file_existence_check_guarded_planning_closed",
        "file_existence_check_guarded_dryrun_closed",
        "file_existence_check_guarded_post_review_closed",
        "file_existence_check_guarded_closed",
        "existence_gate_decision_simulation_only",
        "cross_repo_input_roots_observed",
        "output_root_fixed_to_luna_core",
    ):
        ok(f"current_status.{key}", current_status.get(key) is True, current_status.get(key))
    for key in (
        "real_existence_check_readiness_claimed",
        "file_stat_readiness_claimed",
        "file_open_readiness_claimed",
        "real_image_readiness_claimed",
        "visual_runtime_claimed",
        "production_readiness_claimed",
        "runtime_enablement_claimed",
    ):
        ok(f"current_status.{key}", current_status.get(key) is False, current_status.get(key))

    ok("routes.count>=12", route_option_matrix.get("route_option_count", 0) >= 12, route_option_matrix.get("route_option_count"))
    ok("routes.selected_id", route_option_matrix.get("selected_route_id") == "A", route_option_matrix.get("selected_route_id"))

    ok("priority.p0>=3", priority_ranking.get("p0_route_count", 0) >= 3, priority_ranking.get("p0_route_count"))
    ok("priority.p1>=6", priority_ranking.get("p1_route_count", 0) >= 6, priority_ranking.get("p1_route_count"))
    ok("priority.p2>=3", priority_ranking.get("p2_route_count", 0) >= 3, priority_ranking.get("p2_route_count"))

    ok("next_phase.final", next_phase_recommendation.get("final_decision") == FINAL_DECISION)
    ok("next_phase.recommended", next_phase_recommendation.get("recommended_next_phase") == NEXT_PHASE)

    for payload_name, payload in (
        ("no_file_op", no_file_operation_boundary_report),
        ("no_runtime", no_runtime_boundary_report),
        ("no_write", no_write_boundary_report),
    ):
        ok(f"{payload_name}.scope", payload.get("decision_scope") == "post_file_existence_check_roadmap_decision_only")
        for key in ("no_runtime_executed", "no_new_runtime_enabled", "boundary_ok"):
            ok(f"{payload_name}.{key}", payload.get(key) is True)
        for key in (
            "file_existence_check_invoked",
            "os_path_exists_invoked",
            "pathlib_exists_invoked",
            "file_stat_invoked",
            "file_opened",
            "file_content_read",
            "image_content_read",
            "video_content_read",
            "exif_parsed",
            "video_probe_invoked",
            "real_file_hash_computed",
            "visual_model_invoked",
            "ocr_provider_invoked",
            "tracking_runtime_invoked",
            "map_api_invoked",
            "world_model_written",
            "memory_written",
            "fact_written",
        ):
            ok(f"{payload_name}.{key}.false", payload.get(key) is False)
        ok(f"{payload_name}.violations==[]", payload.get("violations") == [])

    ok("meta.check_ids.unique", len({c["check_id"] for c in checks}) == len(checks), len(checks))
    ok("meta.checks_total>=180", len(checks) >= 180, len(checks))
    ok("meta.baseline_requirement==140", BASELINE_REQUIREMENT == 140)
    ok("meta.min_checks_required==180", MIN_CHECKS == 180)

    passed_count = sum(1 for c in checks if c["passed"])
    verdict = "GO" if len(checks) >= MIN_CHECKS and passed_count == len(checks) else "NO_GO"
    report = {
        "phase": PHASE_ID,
        "verifier": verdict,
        "check_count": len(checks),
        "passed_count": passed_count,
        "failed_count": len(checks) - passed_count,
        "min_checks": MIN_CHECKS,
        "baseline_requirement": BASELINE_REQUIREMENT,
        "final_decision": FINAL_DECISION if verdict == "GO" else "POST_FILE_EXISTENCE_CHECK_ROADMAP_DECISION_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if verdict == "GO" else PHASE_ID,
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "verifier": report["verifier"],
                "check_count": report["check_count"],
                "passed_count": report["passed_count"],
                "failed_count": report["failed_count"],
                "final_decision": report["final_decision"],
                "recommended_next_phase": report["recommended_next_phase"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())

