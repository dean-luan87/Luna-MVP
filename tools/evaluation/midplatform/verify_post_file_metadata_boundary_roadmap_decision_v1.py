#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Post File Metadata Boundary Roadmap Decision v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

PHASE_ID = "Phase-Post-File-Metadata-Boundary-Roadmap-Decision-v1-001"
FINAL_DECISION = "POST_FILE_METADATA_BOUNDARY_ROADMAP_DECISION_READY_FOR_FILE_EXISTENCE_CHECK_GUARDED_PLANNING"
NEXT_PHASE = "Phase-Controlled-Frame-File-Existence-Check-Guarded-Planning-v1-001"
MIN_CHECKS = 170
BASELINE_REQUIREMENT = 130


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-root",
        default="/Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/post_file_metadata_boundary_roadmap_decision_v1_smoke_v0",
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
    current_status = _load_json(root / "current_file_metadata_boundary_status_summary.json")
    route_option_matrix = _load_json(root / "route_option_matrix.json")
    priority_ranking = _load_json(root / "priority_ranking.json")
    _load_json(root / "completed_capability_summary.json")
    _load_json(root / "recommended_next_phase_decision.json")
    _load_json(root / "deferred_gate_taxonomy_register.json")
    _load_json(root / "deferred_real_image_read_register.json")
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
        "file_metadata_boundary_closure",
        "file_metadata_boundary_post_review",
        "file_metadata_boundary_dryrun",
        "file_metadata_boundary_planning",
        "post_controlled_frame_sample_roadmap_decision",
        "controlled_frame_sample_closure",
        "controlled_frame_sample_post_review",
        "controlled_frame_sample_dryrun",
        "controlled_frame_sample_planning",
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
    for key in (
        "file_metadata_boundary_closure_input_loaded",
        "file_metadata_boundary_post_review_input_loaded",
        "file_metadata_boundary_dryrun_input_loaded",
        "file_metadata_boundary_planning_input_loaded",
        "post_controlled_frame_sample_roadmap_input_loaded",
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
        "deferred_gate_taxonomy_register_generated",
        "deferred_real_image_read_register_generated",
        "deferred_resilience_distributed_midplatform_register_generated",
        "deferred_worldmodel_memory_library_emotion_register_generated",
        "boundary_freeze_generated",
        "governance_debt_roadmap_register_generated",
        "non_claims_register_generated",
        "route_option_count>=10",
        "p0_route_count>=3",
        "p1_route_count>=6",
        "p2_route_count>=2",
        "file_existence_check_guarded_planning_route_exists",
        "file_stat_guarded_dryrun_route_exists",
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
        "file_metadata_boundary_closed",
        "metadata_decision_simulation_only",
        "gate_taxonomy_deferred",
        "gate_taxonomy_project_optimization",
        "real_image_read_deferred",
        "controlled_static_image_read_preplan_deferred",
        "midplatform_resilience_deferred",
        "offline_distributed_midplatform_deferred",
        "worldmodel_candidate_layer_deferred",
        "memory_library_governance_deferred",
        "exploration_drive_deferred",
        "emotion_engine_deferred",
        "no_runtime_executed",
        "no_new_runtime_enabled",
        "boundary_ok",
    ):
        if key.endswith(">=10"):
            ok("summary.route_option_count>=10", summary.get("route_option_count", 0) >= 10, summary.get("route_option_count"))
            continue
        if key.endswith(">=3"):
            ok("summary.p0_route_count>=3", summary.get("p0_route_count", 0) >= 3, summary.get("p0_route_count"))
            continue
        if key.endswith(">=6"):
            ok("summary.p1_route_count>=6", summary.get("p1_route_count", 0) >= 6, summary.get("p1_route_count"))
            continue
        if key.endswith(">=2"):
            ok("summary.p2_route_count>=2", summary.get("p2_route_count", 0) >= 2, summary.get("p2_route_count"))
            continue
        ok(f"summary.{key}", summary.get(key) is True, summary.get(key))

    # Summary required false
    for key in (
        "file_existence_check_readiness_claimed",
        "real_metadata_readiness_claimed",
        "real_hash_readiness_claimed",
        "real_image_readiness_claimed",
        "visual_runtime_claimed",
        "production_readiness_claimed",
        "runtime_enablement_claimed",
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

    ok("summary.decision_scope", summary.get("decision_scope") == "post_file_metadata_boundary_roadmap_decision_only")
    ok("summary.violations", summary.get("violations") == [])
    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.selected_route", summary.get("selected_route") == "File Existence Check Guarded Planning")

    for key in (
        "file_metadata_boundary_planning_closed",
        "file_metadata_boundary_dryrun_closed",
        "file_metadata_boundary_post_review_closed",
        "file_metadata_boundary_closed",
        "metadata_decision_simulation_only",
    ):
        ok(f"current_status.{key}", current_status.get(key) is True)

    for key in (
        "file_existence_check_readiness_claimed",
        "real_metadata_readiness_claimed",
        "real_hash_readiness_claimed",
        "real_image_readiness_claimed",
        "visual_runtime_claimed",
        "production_readiness_claimed",
        "runtime_enablement_claimed",
    ):
        ok(f"current_status.{key}", current_status.get(key) is False)

    ok("routes.count>=10", route_option_matrix.get("route_option_count", 0) >= 10, route_option_matrix.get("route_option_count"))
    ok("routes.selected_id", route_option_matrix.get("selected_route_id") == "A", route_option_matrix.get("selected_route_id"))

    ok("priority.p0>=3", priority_ranking.get("p0_route_count", 0) >= 3, priority_ranking.get("p0_route_count"))
    ok("priority.p1>=6", priority_ranking.get("p1_route_count", 0) >= 6, priority_ranking.get("p1_route_count"))
    ok("priority.p2>=2", priority_ranking.get("p2_route_count", 0) >= 2, priority_ranking.get("p2_route_count"))

    ok("next_phase.final", next_phase_recommendation.get("final_decision") == FINAL_DECISION)
    ok("next_phase.recommended", next_phase_recommendation.get("recommended_next_phase") == NEXT_PHASE)

    for payload_name, payload in (
        ("no_file_op", no_file_operation_boundary_report),
        ("no_runtime", no_runtime_boundary_report),
        ("no_write", no_write_boundary_report),
    ):
        ok(f"{payload_name}.scope", payload.get("decision_scope") == "post_file_metadata_boundary_roadmap_decision_only")
        for key in ("no_runtime_executed", "no_new_runtime_enabled", "boundary_ok"):
            ok(f"{payload_name}.{key}", payload.get(key) is True)
        for key in (
            "file_existence_check_invoked",
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

    ok("meta.check_ids.unique", len({c['check_id'] for c in checks}) == len(checks), len(checks))
    ok("meta.checks_total>=170", len(checks) >= 170, len(checks))
    ok("meta.baseline_requirement==130", BASELINE_REQUIREMENT == 130)
    ok("meta.min_checks_required==170", MIN_CHECKS == 170)

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
        "final_decision": FINAL_DECISION if verdict == "GO" else "POST_FILE_METADATA_BOUNDARY_ROADMAP_DECISION_REQUIRES_FIXES",
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

