#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Post Controlled Frame Sample Roadmap Decision v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

PHASE_ID = "Phase-Post-Controlled-Frame-Sample-Roadmap-Decision-v1-001"
FINAL_DECISION = "POST_CONTROLLED_FRAME_SAMPLE_ROADMAP_DECISION_READY_FOR_FILE_METADATA_BOUNDARY_PLANNING"
NEXT_PHASE = "Phase-Controlled-Frame-File-Metadata-Boundary-Planning-v1-001"
MIN_CHECKS = 170
BASELINE_REQUIREMENT = 130

EXPECTED_ROUTES = [
    ("A", "Controlled Frame File Existence / Metadata Boundary Planning", "P0", True, NEXT_PHASE),
    ("B", "Guarded Image Read Preplan", "P0", False, "Phase-Guarded-Image-Read-Preplan-v1-001"),
    ("C", "Controlled Static Image Read Guarded Trial", "P1", False, "Phase-Controlled-Static-Image-Read-Guarded-Trial-v1-001"),
    ("D", "Gate Taxonomy / Gate Requirement Framework", "P0", False, "Phase-Gate-Taxonomy-Gate-Requirement-Framework-v1-001"),
    ("E", "MidPlatform Function Governance / Consolidation", "P1", False, "Phase-MidPlatform-Function-Governance-Consolidation-v1-001"),
    ("F", "MidPlatform Resilience / Robustness Preplan", "P1", False, "Phase-MidPlatform-Resilience-Robustness-Preplan-v1-001"),
    ("G", "Offline Distributed MidPlatform Architecture Preplan", "P1", False, "Phase-Offline-Distributed-MidPlatform-Architecture-Preplan-v1-001"),
    ("H", "Minimal Controlled Visual Runtime Planning", "P1", False, "Phase-Minimal-Controlled-Visual-Runtime-Planning-v1-001"),
    ("I", "WorldModel / Memory / Library Governance", "P2", False, "Phase-WorldModel-Memory-Library-Governance-v1-001"),
    ("J", "Exploration Drive / Emotion Map / Affective Engine", "P2", False, "Phase-Exploration-Drive-Emotion-Affective-Engine-v1-001"),
]


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-root",
        default="/Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/post_controlled_frame_sample_roadmap_decision_v1_smoke_v0",
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
    current_status = _load_json(root / "current_controlled_frame_sample_status_summary.json")
    completed_capability_summary = _load_json(root / "completed_capability_summary.json")
    route_option_matrix = _load_json(root / "route_option_matrix.json")
    priority_ranking = _load_json(root / "priority_ranking.json")
    recommended_next_phase_decision = _load_json(root / "recommended_next_phase_decision.json")
    deferred_gate_taxonomy_register = _load_json(root / "deferred_gate_taxonomy_register.json")
    deferred_resilience_distributed_midplatform_register = _load_json(root / "deferred_resilience_distributed_midplatform_register.json")
    deferred_worldmodel_memory_library_emotion_register = _load_json(root / "deferred_worldmodel_memory_library_emotion_register.json")
    boundary_freeze = _load_json(root / "boundary_freeze.json")
    governance_debt_roadmap_register = _load_json(root / "governance_debt_roadmap_register.json")
    non_claims_register = _load_json(root / "non_claims_register.json")
    next_phase_recommendation = _load_json(root / "next_phase_recommendation.json")
    no_runtime_boundary_report = _load_json(root / "no_runtime_boundary_report.json")
    no_write_boundary_report = _load_json(root / "no_write_boundary_report.json")

    rows = input_root_matrix.get("rows", [])
    idx = {row.get("intake_id"): row for row in rows}

    for intake_id in (
        "controlled_frame_sample_closure",
        "controlled_frame_sample_post_review",
        "controlled_frame_sample_dryrun",
        "controlled_frame_sample_planning",
        "post_crossing_decision_roadmap_decision",
        "crossing_decision_closure",
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

    for key in (
        "controlled_frame_sample_closure_input_loaded",
        "controlled_frame_sample_post_review_input_loaded",
        "controlled_frame_sample_dryrun_input_loaded",
        "controlled_frame_sample_planning_input_loaded",
        "post_crossing_decision_roadmap_input_loaded",
        "crossing_decision_closure_input_loaded",
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
        "deferred_resilience_distributed_midplatform_register_generated",
        "deferred_worldmodel_memory_library_emotion_register_generated",
        "boundary_freeze_generated",
        "governance_debt_roadmap_register_generated",
        "non_claims_register_generated",
        "controlled_frame_file_metadata_boundary_route_exists",
        "guarded_image_read_preplan_route_exists",
        "controlled_static_image_read_guarded_trial_route_exists",
        "gate_taxonomy_route_exists",
        "midplatform_function_governance_route_exists",
        "midplatform_resilience_route_exists",
        "offline_distributed_midplatform_route_exists",
        "minimal_controlled_visual_runtime_route_exists",
        "worldmodel_memory_library_route_exists",
        "exploration_emotion_route_exists",
        "controlled_frame_sample_closed",
        "manifest_metadata_only",
        "gate_taxonomy_deferred",
        "gate_taxonomy_project_optimization",
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
        ok(f"summary.{key}", summary.get(key) is True, summary.get(key))

    ok("summary.route_option_count", summary.get("route_option_count", 0) >= 9, summary.get("route_option_count"))
    ok("summary.p0_route_count", summary.get("p0_route_count", 0) >= 3, summary.get("p0_route_count"))
    ok("summary.p1_route_count", summary.get("p1_route_count", 0) >= 4, summary.get("p1_route_count"))
    ok("summary.p2_route_count", summary.get("p2_route_count", 0) >= 2, summary.get("p2_route_count"))

    for key in (
        "real_image_readiness_claimed",
        "real_video_readiness_claimed",
        "visual_runtime_claimed",
        "production_readiness_claimed",
        "runtime_enablement_claimed",
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

    ok("summary.decision_scope", summary.get("decision_scope") == "post_controlled_frame_sample_roadmap_decision_only")
    ok("summary.violations", summary.get("violations") == [])
    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.selected_route", summary.get("selected_route") == "Controlled Frame File Existence / Metadata Boundary Planning")

    for key in (
        "controlled_frame_sample_planning_closed",
        "controlled_frame_sample_dryrun_closed",
        "controlled_frame_sample_post_review_closed",
        "controlled_frame_sample_closed",
        "manifest_metadata_only",
    ):
        ok(f"current_status.{key}", current_status.get(key) is True)

    for key in (
        "real_image_readiness_claimed",
        "real_video_readiness_claimed",
        "visual_runtime_claimed",
        "production_readiness_claimed",
        "runtime_enablement_claimed",
    ):
        ok(f"current_status.{key}", current_status.get(key) is False)

    ok("routes.count", route_option_matrix.get("route_option_count", 0) >= 9, route_option_matrix.get("route_option_count"))
    ok("routes.selected_route_id", route_option_matrix.get("selected_route_id") == "A")
    route_rows = route_option_matrix.get("routes", [])
    ok("routes.selected_single", sum(1 for row in route_rows if row.get("selected_now") is True) == 1)
    route_idx = {row.get("route_id"): row for row in route_rows}
    for route_id, route_name, priority, selected_now, phase_name in EXPECTED_ROUTES:
        row = route_idx.get(route_id, {})
        ok(f"route.{route_id}.present", route_id in route_idx)
        ok(f"route.{route_id}.name", row.get("route_name") == route_name, row.get("route_name"))
        ok(f"route.{route_id}.priority", row.get("recommended_priority") == priority, row.get("recommended_priority"))
        ok(f"route.{route_id}.selected_now", row.get("selected_now") is selected_now, row.get("selected_now"))
        ok(f"route.{route_id}.phase_name", row.get("recommended_phase_name") == phase_name, row.get("recommended_phase_name"))
        ok(f"route.{route_id}.dependency", isinstance(row.get("dependency"), list) and len(row.get("dependency", [])) >= 2)
        ok(f"route.{route_id}.risk_level", isinstance(row.get("risk_level"), str) and bool(row.get("risk_level")))
        ok(f"route.{route_id}.expected_value", isinstance(row.get("expected_value"), str) and bool(row.get("expected_value")))
        if not selected_now:
            ok(f"route.{route_id}.defer_reason", bool(row.get("defer_reason")))
        else:
            ok(f"route.{route_id}.defer_reason_empty", row.get("defer_reason") == "")

    ok("priority.p0_count", priority_ranking.get("p0_route_count", 0) >= 3, priority_ranking.get("p0_route_count"))
    ok("priority.p1_count", priority_ranking.get("p1_route_count", 0) >= 4, priority_ranking.get("p1_route_count"))
    ok("priority.p2_count", priority_ranking.get("p2_route_count", 0) >= 2, priority_ranking.get("p2_route_count"))
    ok("priority.selected_top", priority_ranking.get("selected_top_priority_route") == "Controlled Frame File Existence / Metadata Boundary Planning")

    ok("recommended.scope", recommended_next_phase_decision.get("decision_scope") == "post_controlled_frame_sample_roadmap_decision_only")
    ok("recommended.selected_next_phase", recommended_next_phase_decision.get("selected_next_phase") == NEXT_PHASE)
    ok("recommended.reason_count", len(recommended_next_phase_decision.get("decision_reason", [])) >= 5)
    ok("recommended.rejected_count", len(recommended_next_phase_decision.get("rejected_or_deferred_routes", [])) >= 9)

    ok("defer_gate.taxonomy_deferred", deferred_gate_taxonomy_register.get("gate_taxonomy_deferred") is True)
    ok("defer_gate.project", deferred_gate_taxonomy_register.get("current_status") == "project_optimization_deferred")
    ok("defer_gate.impl_now", deferred_gate_taxonomy_register.get("implementation_allowed_now") is False)

    ok("defer_resilience.midplatform_resilience_deferred", deferred_resilience_distributed_midplatform_register.get("midplatform_resilience_deferred") is True)
    ok("defer_resilience.offline_distributed_midplatform_deferred", deferred_resilience_distributed_midplatform_register.get("offline_distributed_midplatform_deferred") is True)

    ok("defer_wml.worldmodel_candidate_layer_deferred", deferred_worldmodel_memory_library_emotion_register.get("worldmodel_candidate_layer_deferred") is True)
    ok("defer_wml.memory_library_governance_deferred", deferred_worldmodel_memory_library_emotion_register.get("memory_library_governance_deferred") is True)
    ok("defer_wml.exploration_drive_deferred", deferred_worldmodel_memory_library_emotion_register.get("exploration_drive_deferred") is True)
    ok("defer_wml.emotion_engine_deferred", deferred_worldmodel_memory_library_emotion_register.get("emotion_engine_deferred") is True)

    for key in (
        "no_runtime",
        "no_write",
        "no_action",
        "no_speech",
        "no_fact",
        "no_live_camera",
        "no_image_read",
        "no_video_read",
        "no_file_open",
        "no_video_decode",
        "no_frame_extract",
        "no_real_hash",
        "no_visual_model",
        "no_map_api",
        "no_OCR_provider",
        "no_tracking_runtime",
        "no_crossing_runtime",
        "no_worldmodel_write",
        "no_memory_write",
        "no_library_write",
        "no_entity_resolution",
        "no_fact_admission",
        "no_emotion_engine",
    ):
        ok(f"boundary.{key}", boundary_freeze.get(key) is True)

    ok("non_claims.count", len(non_claims_register.get("non_claims", [])) >= 10, len(non_claims_register.get("non_claims", [])))
    for key in ("file_content_read", "image_content_read", "video_content_read", "runtime_enablement_claimed", "production_readiness_claimed"):
        ok(f"non_claims.{key}", non_claims_register.get(key) is False)

    ok("next_phase.route_name", next_phase_recommendation.get("route_name") == "Controlled Frame File Existence / Metadata Boundary Planning")
    ok("next_phase.priority_level", next_phase_recommendation.get("priority_level") == "P0")
    ok("next_phase.final_decision", next_phase_recommendation.get("final_decision") == FINAL_DECISION)
    ok("next_phase.recommended_next_phase", next_phase_recommendation.get("recommended_next_phase") == NEXT_PHASE)

    for report_name, report in (
        ("no_runtime_boundary_report", no_runtime_boundary_report),
        ("no_write_boundary_report", no_write_boundary_report),
    ):
        ok(f"{report_name}.decision_scope", report.get("decision_scope") == "post_controlled_frame_sample_roadmap_decision_only")
        ok(f"{report_name}.roadmap_decision_only", report.get("roadmap_decision_only") is True)
        for k in ("no_runtime_executed", "no_new_runtime_enabled", "boundary_ok"):
            ok(f"{report_name}.{k}", report.get(k) is True)
        ok(f"{report_name}.violations", report.get("violations") == [])
        for k in (
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
            ok(f"{report_name}.{k}", report.get(k) is False)

    ok("completed_capability_summary.present", completed_capability_summary.get("completed_capability_count", 0) >= 10)
    ok("completed_capability_summary.rows", isinstance(completed_capability_summary.get("capabilities"), list))

    ok("governance_debt.count", len(governance_debt_roadmap_register.get("carryover_topics", [])) >= 8)
    ok("governance_debt.no_duplicate", governance_debt_roadmap_register.get("no_duplicate_governance_module_allowed") is True)

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

