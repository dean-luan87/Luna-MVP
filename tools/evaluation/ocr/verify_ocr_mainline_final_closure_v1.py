#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify OCR Mainline Final Closure v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Dict, List

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


DEFAULT_WORKSPACE_ROOT = Path("/Users/luanlei/Desktop/Luna-Workspace-Min")
DEFAULT_OUTPUT_ROOT = DEFAULT_WORKSPACE_ROOT / "_eval_out" / "ocr_mainline_final_closure_v1_smoke_v0"

FINAL_DECISION = "OCR_MAINLINE_FINAL_CLOSURE_RETURN_TO_VISION_MAINLINE"
NEXT_PHASE = "Phase-Return-To-Vision-Mainline-Planning-v1-001"
MIN_CHECKS = 100
BASELINE_REQUIREMENT = 80


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _contains_any(texts: List[str], needle: str) -> bool:
    lowered = needle.lower()
    return any(lowered in text.lower() for text in texts)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verify OCR mainline final closure v1")
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_root = Path(args.output_root)
    checks: List[Dict[str, Any]] = []

    def expect(check_id: str, passed: bool, detail: Any = None) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})

    summary = _load_json(output_root / "summary.json")
    input_root_matrix = _load_json(output_root / "input_root_matrix.json")
    closure_report = _load_json(output_root / "ocr_mainline_final_closure_report.json")
    phase_matrix = _load_json(output_root / "ocr_completed_phase_matrix.json")
    validated = _load_json(output_root / "ocr_validated_capability_summary.json")
    runtime_disabled = _load_json(output_root / "ocr_runtime_disabled_summary.json")
    non_claims = _load_json(output_root / "ocr_non_claims_register.json")
    deferred = _load_json(output_root / "deferred_ocr_capability_pool.json")
    handoff = _load_json(output_root / "ocr_to_vision_handoff_plan.json")
    next_phase = _load_json(output_root / "next_phase_recommendation.json")
    no_runtime = _load_json(output_root / "no_runtime_boundary_report.json")
    no_write = _load_json(output_root / "no_write_boundary_report.json")

    # Input checks
    expect("input.minimal_runtime_integration_closure_loaded", summary.get("minimal_runtime_integration_closure_loaded") is True)
    expect("input.ocr_phase_verdict_table_loaded", summary.get("ocr_phase_verdict_table_loaded") is True)
    expect("input.loaded_phase_count_ge_5", summary.get("loaded_phase_count", 0) >= 5, summary.get("loaded_phase_count"))
    expect("input.input_root_matrix_present", isinstance(input_root_matrix.get("rows"), list))
    expect("input.input_root_matrix_row_count_match", input_root_matrix.get("row_count") == len(input_root_matrix.get("rows", [])))
    expect(
        "input.required_root_present",
        any(
            row.get("intake_id") == "minimal_runtime_integration_closure" and row.get("loaded") is True
            for row in input_root_matrix.get("rows", [])
        ),
    )
    expect(
        "input.required_doc_present",
        any(
            row.get("intake_id") == "ocr_phase_verdict_table" and row.get("loaded") is True
            for row in input_root_matrix.get("rows", [])
        ),
    )

    # Closure checks
    expect("closure.scope", summary.get("closure_scope") == "ocr_mainline_final_closure_only", summary.get("closure_scope"))
    expect("closure.closure_only", summary.get("closure_only") is True)
    expect("closure.phase_matrix_generated", summary.get("ocr_completed_phase_matrix_generated") is True)
    expect("closure.validated_summary_generated", summary.get("ocr_validated_capability_summary_generated") is True)
    expect("closure.runtime_disabled_generated", summary.get("ocr_runtime_disabled_summary_generated") is True)
    expect("closure.non_claims_generated", summary.get("ocr_non_claims_register_generated") is True)
    expect("closure.deferred_pool_generated", summary.get("deferred_ocr_capability_pool_generated") is True)
    expect("closure.handoff_generated", summary.get("ocr_to_vision_handoff_plan_generated") is True)
    expect("closure.mainline_status", summary.get("ocr_mainline_status") == "closed_for_current_mainline", summary.get("ocr_mainline_status"))
    expect("closure.report_scope", closure_report.get("closure_scope") == "ocr_mainline_final_closure")
    expect("closure.report_final_decision", closure_report.get("final_closure_decision") == FINAL_DECISION)
    expect("closure.report_next_phase", closure_report.get("next_phase_recommendation") == NEXT_PHASE)
    expect("closure.report_status", closure_report.get("ocr_mainline_status") == "closed_for_current_mainline")
    expect("closure.report_loaded_phase_count_match", closure_report.get("loaded_phase_count") == summary.get("loaded_phase_count"))

    # OCR boundary checks from summary
    expect("boundary.ocr_runtime_allowed", summary.get("ocr_runtime_allowed") is False)
    expect("boundary.ocr_provider_allowed", summary.get("ocr_provider_allowed") is False)
    expect("boundary.ocrrequest_submission_allowed", summary.get("ocrrequest_submission_allowed") is False)
    expect("boundary.fact_write_allowed", summary.get("fact_write_allowed") is False)
    expect("boundary.worldmodel_write_allowed", summary.get("worldmodel_write_allowed") is False)
    expect("boundary.memory_write_allowed", summary.get("memory_write_allowed") is False)
    expect("boundary.scene_delta_allowed", summary.get("scene_delta_allowed") is False)
    expect("boundary.new_runtime_enabled", summary.get("new_runtime_enabled") is False)

    # Validated capability checks
    expect("validated.ocr_activation_governance_exists", validated.get("ocr_activation_governance_exists") is True)
    expect("validated.ocrrequest_reference_path_exists", validated.get("ocrrequest_reference_path_exists") is True)
    expect(
        "validated.roi_crop_dryrun_reference_path_exists_where_available",
        validated.get("roi_crop_dryrun_reference_path_exists_where_available") is True,
    )
    expect("validated.gated_path_replaces_direct_provider_call", validated.get("gated_path_replaces_direct_provider_call") is True)
    expect(
        "validated.evidence_pack_adapter_supports_scan_observation_alignment",
        validated.get("evidence_pack_adapter_supports_scan_observation_alignment") is True,
    )
    expect("validated.scan_observation_not_text_evidence", validated.get("scan_observation_not_text_evidence") is True)
    expect("validated.sq_e_low_quality_input_blocked", validated.get("sq_e_low_quality_input_blocked") is True)
    expect("validated.full_frame_ocr_default_forbidden", validated.get("full_frame_ocr_default_forbidden") is True)
    expect(
        "validated.static_reading_requires_readable_region_discovery",
        validated.get("static_reading_requires_readable_region_discovery") is True,
    )
    expect(
        "validated.poster_ocr_uses_segment_first_governance_first_logic",
        validated.get("poster_ocr_uses_segment_first_governance_first_logic") is True,
    )
    expect(
        "validated.realvideo_text_bearing_sample_planning_exists",
        validated.get("realvideo_text_bearing_sample_planning_exists") is True,
    )
    expect(
        "validated.empty_ocr_text_is_not_automatically_failure_or_fact",
        validated.get("empty_ocr_text_is_not_automatically_failure_or_fact") is True,
    )
    expect(
        "validated.memory_worldmodel_write_remains_blocked",
        validated.get("memory_worldmodel_write_remains_blocked") is True,
    )
    expect(
        "validated.ocr_can_support_future_vision_mainline_as_candidate_reference_layer",
        validated.get("ocr_can_support_future_vision_mainline_as_candidate_reference_layer") is True,
    )
    expect("validated.direct_provider_bypass_forbidden", validated.get("direct_provider_bypass_forbidden") is True)
    expect("validated.evidence_pack_not_fact", validated.get("evidence_pack_not_fact") is True)
    expect("validated.semantic_candidate_not_fact", validated.get("semantic_candidate_not_fact") is True)

    # Disabled runtime summary checks
    for key in (
        "real_ocr_provider_runtime_allowed",
        "ocrrequest_submission_allowed",
        "paddleocr_runtime_allowed",
        "rapidocr_runtime_allowed",
        "deepseek_ocr_runtime_allowed",
        "camera_runtime_allowed",
        "frame_sampling_runtime_allowed",
        "detector_runtime_allowed",
        "segmentation_runtime_allowed",
        "tracking_runtime_allowed",
        "provider_comparison_runtime_allowed",
        "benchmark_accuracy_update_allowed",
        "memory_write_allowed",
        "worldmodel_write_allowed",
        "fact_write_allowed",
        "scene_delta_commit_allowed",
        "navigation_action_allowed",
        "task_commit_allowed",
        "map_api_allowed",
    ):
        expect(f"runtime_disabled.{key}", runtime_disabled.get(key) is False)

    # Disabled invocation checks from summary
    for key in (
        "ocr_runtime_invoked",
        "ocr_provider_invoked",
        "ocrrequest_submitted",
        "paddleocr_invoked",
        "rapidocr_invoked",
        "deepseek_ocr_invoked",
        "camera_invoked",
        "frame_sampled",
        "new_crop_generated",
        "detector_invoked",
        "segmentation_invoked",
        "tracking_invoked",
        "benchmark_accuracy_updated",
        "world_model_written",
        "memory_written",
        "fact_written",
        "scene_delta_generated",
        "navigation_action_triggered",
        "task_state_committed_now",
        "map_api_invoked",
        "runtime_routing_changed",
    ):
        expect(f"summary.invocation.{key}", summary.get(key) is False)

    expect("summary.boundary_ok", summary.get("boundary_ok") is True)
    expect("summary.violations_empty", summary.get("violations") == [])

    # Boundary report checks
    for payload_name, payload in (("no_runtime", no_runtime), ("no_write", no_write)):
        expect(f"{payload_name}.boundary_ok", payload.get("boundary_ok") is True)
        expect(f"{payload_name}.violations_empty", payload.get("violations") == [])
        expect(f"{payload_name}.closure_only", payload.get("closure_only") is True)
        expect(f"{payload_name}.ocr_runtime_invoked", payload.get("ocr_runtime_invoked") is False)
        expect(f"{payload_name}.ocr_provider_invoked", payload.get("ocr_provider_invoked") is False)
        expect(f"{payload_name}.ocrrequest_submitted", payload.get("ocrrequest_submitted") is False)
        expect(f"{payload_name}.camera_invoked", payload.get("camera_invoked") is False)
        expect(f"{payload_name}.frame_sampled", payload.get("frame_sampled") is False)
        expect(f"{payload_name}.new_crop_generated", payload.get("new_crop_generated") is False)
        expect(f"{payload_name}.detector_invoked", payload.get("detector_invoked") is False)
        expect(f"{payload_name}.segmentation_invoked", payload.get("segmentation_invoked") is False)
        expect(f"{payload_name}.tracking_invoked", payload.get("tracking_invoked") is False)
        expect(f"{payload_name}.benchmark_accuracy_updated", payload.get("benchmark_accuracy_updated") is False)
        expect(f"{payload_name}.world_model_written", payload.get("world_model_written") is False)
        expect(f"{payload_name}.memory_written", payload.get("memory_written") is False)
        expect(f"{payload_name}.fact_written", payload.get("fact_written") is False)
        expect(f"{payload_name}.scene_delta_generated", payload.get("scene_delta_generated") is False)
        expect(f"{payload_name}.navigation_action_triggered", payload.get("navigation_action_triggered") is False)
        expect(f"{payload_name}.task_state_committed_now", payload.get("task_state_committed_now") is False)
        expect(f"{payload_name}.map_api_invoked", payload.get("map_api_invoked") is False)
        expect(f"{payload_name}.runtime_routing_changed", payload.get("runtime_routing_changed") is False)

    # Non-claims checks
    statements = non_claims.get("statements", [])
    expect("non_claims.count_ge_10", len(statements) >= 10, len(statements))
    expect("non_claims.ocr_closure_not_production", _contains_any(statements, "not equal production ocr runtime"))
    expect("non_claims.ocrrequest_reference_not_submitted", _contains_any(statements, "ocrrequest reference does not equal ocrrequest submitted"))
    expect("non_claims.evidence_pack_candidate_not_fact", _contains_any(statements, "evidence pack candidate does not equal fact"))
    expect("non_claims.semantic_candidate_not_worldmodel_write", _contains_any(statements, "semantic candidate does not equal worldmodel write"))
    expect("non_claims.readable_region_not_detected_text_fact", _contains_any(statements, "readable region candidate does not equal detected text fact"))
    expect("non_claims.static_reading_not_camera_capture", _contains_any(statements, "static reading handoff does not equal camera capture"))
    expect("non_claims.realvideo_planning_not_benchmark", _contains_any(statements, "realvideo planning does not equal real video ocr benchmark"))
    expect("non_claims.no_memory_worldmodel_fact_write", _contains_any(statements, "not equal worldmodel write") and _contains_any(statements, "evidence pack candidate does not equal fact"))
    expect("non_claims.no_bypass_gates", _contains_any(statements, "must not bypass stc"))

    # Handoff checks
    handoff_focus = handoff.get("next_mainline_focus", [])
    handoff_roles = handoff.get("ocr_future_role_in_vision_mainline", [])
    expect("handoff.exists", isinstance(handoff_focus, list) and isinstance(handoff_roles, list))
    expect("handoff.recommendation", handoff.get("next_phase_recommendation") == NEXT_PHASE)
    expect("handoff.includes_viewpoint_segmentation", "viewpoint_segmentation_or_view_slicing" in handoff_focus)
    expect("handoff.includes_object_tracking", "object_tracking" in handoff_focus)
    expect("handoff.includes_visual_candidate_stabilization", "visual_candidate_stabilization" in handoff_focus)
    expect("handoff.includes_map_route_location", "map_route_location_context_integration" in handoff_focus)
    expect("handoff.includes_basic_navigation_loop_strengthening", "basic_navigation_loop_strengthening" in handoff_focus)
    expect(
        "handoff.role_candidate_reference_provider",
        "candidate_or_reference_evidence_provider" in handoff_roles,
    )
    expect("handoff.role_text_region_hint", "text_region_hint_provider" in handoff_roles)
    expect("handoff.role_readable_region_support", "readable_region_support" in handoff_roles)
    expect("handoff.role_posterior_verification", "posterior_verification_tool" in handoff_roles)
    expect(
        "handoff.role_worldmodel_verification_candidate",
        "worldmodel_verification_candidate_not_fact_writer" in handoff_roles,
    )
    expect(
        "handoff.role_map_route_auxiliary_only",
        "map_route_scene_label_auxiliary_source_not_route_authority" in handoff_roles,
    )
    expect("handoff.not_recommend_ocr_provider_runtime_next", handoff.get("must_not_recommend_ocr_provider_runtime_next") is True)
    expect("handoff.not_recommend_ocr_benchmark_next", handoff.get("must_not_recommend_ocr_benchmark_execution_next") is True)
    expect("handoff.not_recommend_memory_worldmodel_write_next", handoff.get("must_not_recommend_memory_worldmodel_write_next") is True)
    expect("handoff.not_recommend_map_api_next", handoff.get("must_not_recommend_map_api_next") is True)

    # Readiness checks
    expect("readiness.final_decision", summary.get("final_decision") == FINAL_DECISION)
    expect("readiness.next_phase_recommendation", next_phase.get("next_phase_recommendation") == NEXT_PHASE)

    # Phase matrix checks
    rows = phase_matrix.get("rows", [])
    expected_phase_names = [
        "RealVideo OCR Text-Bearing Sample Planning",
        "Mixed Video Poster Batch Smoke v2 Gated Path Only",
        "OCR Evidence Pack Adapter v1",
        "ROI Crop Execution DryRun",
        "ROI-to-OCRRequest Reference",
        "ROI BBox Expansion Proposal",
        "Better Frame Extraction DryRun",
        "BBox Adjustment Proposal v2 Multiframe",
        "Static Readable Region Discovery Guidance Policy",
        "Hardware Camera Control Contract",
        "WorldModel Lookup for Reading Framework",
        "OCR StaticReading Poster RealVideo Regression Route Compliance",
        "Minimal Runtime Integration Closure",
    ]
    expect("matrix.row_count_13", len(rows) == 13, len(rows))
    expect("matrix.loaded_phase_count_match", phase_matrix.get("loaded_phase_count") == summary.get("loaded_phase_count"))
    row_map = {row["phase_name"]: row for row in rows}
    for phase_name in expected_phase_names:
        expect(f"matrix.phase_present.{phase_name}", phase_name in row_map)
        if phase_name in row_map:
            row = row_map[phase_name]
            expect(f"matrix.output_dir_present.{phase_name}", bool(row.get("output_dir")))
            expect(
                f"matrix.loaded_status_valid.{phase_name}",
                row.get("loaded_status") in {"loaded", "optional_missing"},
                row.get("loaded_status"),
            )
            expect(f"matrix.runtime_invoked_false.{phase_name}", row.get("runtime_invoked") is False)
            expect(
                f"matrix.write_boundary_ok.{phase_name}",
                row.get("write_boundary_status") == "NO_WRITE_BOUNDARY_OK",
                row.get("write_boundary_status"),
            )
            expect(f"matrix.key_artifacts_present.{phase_name}", isinstance(row.get("key_artifacts"), list) and len(row.get("key_artifacts")) >= 1)

    # Additional row checks for loaded rows
    loaded_rows = [row for row in rows if row.get("loaded_status") == "loaded"]
    expect("matrix.loaded_rows_ge_5", len(loaded_rows) >= 5, len(loaded_rows))
    for index, row in enumerate(loaded_rows):
        expect(f"matrix.loaded_row_has_verdict.{index}", row.get("verdict_if_available") not in (None, "", "optional_missing"))
        expect(f"matrix.loaded_row_has_scope.{index}", bool(row.get("scope")))
        expect(f"matrix.loaded_row_has_closure_relevance.{index}", bool(row.get("closure_relevance")))

    # Deferred capability pool checks
    deferred_items = deferred.get("deferred_capabilities", [])
    expect("deferred.count_ge_15", len(deferred_items) >= 15, len(deferred_items))
    expected_deferred = {
        "real_ocr_provider_integration",
        "paddleocr_heavy_runtime",
        "rapidocr_runtime_execution",
        "deepseek_ocr_remote_runtime",
        "ocrrequest_actual_submission",
        "provider_comparison_benchmark",
        "real_camera_capture",
        "real_frame_sampling",
        "real_crop_generation_from_live_stream",
        "text_detector_runtime",
        "segmentation_or_tracking_assisted_ocr",
        "worldmodel_ocr_fact_write",
        "memory_ocr_write",
        "scene_delta_generation",
        "public_facility_semantic_correction_runtime",
        "poster_ocr_production_route",
        "realvideo_ocr_benchmark_execution",
    }
    deferred_caps = {item.get("capability") for item in deferred_items}
    for cap in sorted(expected_deferred):
        expect(f"deferred.present.{cap}", cap in deferred_caps)
    for index, item in enumerate(deferred_items):
        expect(f"deferred.separate_phase.{index}", item.get("requires_separate_phase") is True)
        expect(f"deferred.not_next_priority.{index}", item.get("deferred_from_next_mainline_priority") is True)

    passed_count = sum(1 for item in checks if item["passed"])
    total_checks = len(checks)
    failed_checks = [item for item in checks if not item["passed"]]
    verifier = "GO" if total_checks >= MIN_CHECKS and passed_count == total_checks else "NO_GO"

    report = {
        "phase": "Phase-OCR-Mainline-Final-Closure-v1-001",
        "verifier": verifier,
        "closure_verdict": "GO" if verifier == "GO" else "NO_GO",
        "final_decision": FINAL_DECISION if verifier == "GO" else "HOLD",
        "next_phase_recommendation": NEXT_PHASE if verifier == "GO" else "HOLD",
        "baseline_requirement": BASELINE_REQUIREMENT,
        "minimum_check_target": MIN_CHECKS,
        "total_checks": total_checks,
        "passed_checks": passed_count,
        "failed_checks": len(failed_checks),
        "boundary_ok": verifier == "GO",
        "violations": failed_checks,
        "checks": checks,
    }
    (output_root / "verifier_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return 0 if verifier == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
