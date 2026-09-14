#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Controlled Frame File Metadata Boundary Closure v1 (closure-only)."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

PHASE_ID = "Phase-Controlled-Frame-File-Metadata-Boundary-Closure-v1-001"
FINAL_DECISION = "CONTROLLED_FRAME_FILE_METADATA_BOUNDARY_CLOSED_FOR_CURRENT_MAINLINE"
NEXT_PHASE = "Phase-Post-File-Metadata-Boundary-Roadmap-Decision-v1-001"
MIN_CHECKS = 180
BASELINE_REQUIREMENT = 140

EXPECTED_PHASES = [
    ("Controlled Frame File Metadata Boundary Planning v1", "GO", "CONTROLLED_FRAME_FILE_METADATA_BOUNDARY_PLANNING_READY_FOR_DRYRUN"),
    ("Controlled Frame File Metadata Boundary DryRun v1", "GO", "CONTROLLED_FRAME_FILE_METADATA_BOUNDARY_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"),
    (
        "Controlled Frame File Metadata Boundary Post-DryRun Review v1",
        "GO",
        "CONTROLLED_FRAME_FILE_METADATA_BOUNDARY_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE",
    ),
]

EXPECTED_CAPABILITIES = [
    "file existence policy",
    "path legality policy",
    "external metadata boundary policy",
    "real hash policy",
    "fixture registry policy",
    "fixture registry entry schema",
    "manifest-to-file-metadata candidate mapping",
    "file metadata candidate schema",
    "path allowed / restricted / blocked classification",
    "declared metadata handling",
    "missing metadata blocking",
    "sensitive metadata manual review routing",
    "hash placeholder allowed",
    "real hash blocked",
    "EXIF / video probe blocked",
    "perceptual hash deferred",
    "dry-run simulation",
    "post-dryrun review",
]

EXPECTED_DISABLED_FILE_OPS = [
    "file existence check",
    "file stat",
    "file open",
    "image open",
    "video open",
    "image content read",
    "video content read",
    "EXIF parse",
    "video probe",
    "video decode",
    "frame extraction",
    "real file hash computation",
    "perceptual hash computation",
    "real metadata read",
]

EXPECTED_DISABLED_RUNTIMES = [
    "camera runtime",
    "visual model runtime",
    "OCR provider runtime",
    "OCRRequest submission",
    "map API / 高德 API",
    "GPS runtime",
    "tracking runtime",
    "optical flow runtime",
    "crossing runtime",
    "Speech Gate / VOP / TTS",
    "NavigationAction",
    "TaskState commit",
    "WorldModel write",
    "Memory write",
    "Library write",
    "Fact write",
    "SceneDelta",
]

EXPECTED_NON_CLAIMS = [
    "closure 不等于文件存在性检查可用",
    "closure 不等于文件 stat 可用",
    "closure 不等于可以打开样例文件",
    "closure 不等于真实 metadata 读取",
    "closure 不等于 EXIF 解析",
    "closure 不等于 video probe",
    "closure 不等于真实 hash 计算",
    "closure 不等于 pHash / 内容分析",
    "closure 不等于真实图像读取",
    "closure 不等于真实视频读取",
    "closure 不等于视觉模型 runtime",
    "closure 不等于 OCR/tracking/map/crossing runtime",
    "fixture registry candidate 不等于真实 registry runtime",
    "file metadata candidate 不等于文件事实",
    "metadata dry-run 不等于 production readiness",
]

EXPECTED_DEFERRED = [
    "File Existence Check Guarded Planning",
    "File Stat Guarded Planning",
    "Real Metadata Read Guarded Planning",
    "Real Hash Computation Guarded Planning",
    "EXIF Parse Guarded Planning",
    "Video Probe Guarded Planning",
    "Controlled Static Image Read Preplan",
    "Controlled Image Content Read Guarded Trial",
    "Controlled Video Decode Guarded Trial",
    "Controlled Frame Extraction Guarded Trial",
    "Real Fixture Registry Runtime",
    "Visual Model Adapter DryRun",
    "OCR Provider Re-enable through VisualFocus",
    "Tracking Adapter Experiment Branch",
    "Real VisualObservation generation",
    "Real SceneSketch generation",
    "Real OCRActivationResult generation",
    "Real TrackingResult generation",
    "Gate Taxonomy / Gate Requirement Framework",
    "MidPlatform Function Governance / Consolidation",
    "MidPlatform Resilience / Robustness",
    "Offline Distributed MidPlatform",
    "WorldModel / Memory / Library Governance",
]


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-root",
        default="/Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/controlled_frame_file_metadata_boundary_closure_v1_smoke_v0",
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
    closure_summary = _load_json(root / "controlled_frame_file_metadata_boundary_closure_summary.json")
    completed_phase_matrix = _load_json(root / "completed_phase_matrix.json")
    validated_capability_summary = _load_json(root / "validated_capability_summary.json")
    disabled_file_ops = _load_json(root / "disabled_file_operation_summary.json")
    disabled_runtime_summary = _load_json(root / "disabled_runtime_summary.json")
    closure_boundary_freeze = _load_json(root / "closure_boundary_freeze.json")
    non_claims_register = _load_json(root / "controlled_frame_file_metadata_boundary_non_claims_register.json")
    deferred_capability_pool = _load_json(root / "deferred_capability_pool.json")
    governance_debt_carryover = _load_json(root / "governance_debt_carryover.json")
    closure_readiness_gate = _load_json(root / "closure_readiness_gate.json")
    next_phase_recommendation = _load_json(root / "next_phase_recommendation.json")
    no_file_op = _load_json(root / "no_file_operation_boundary_report.json")
    no_runtime = _load_json(root / "no_runtime_boundary_report.json")
    no_write = _load_json(root / "no_write_boundary_report.json")

    rows = input_root_matrix.get("rows", [])
    idx = {row.get("intake_id"): row for row in rows}
    for intake_id in (
        "post_dryrun_review",
        "dryrun",
        "planning",
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
        ok(
            f"input.{intake_id}.optional",
            idx.get(intake_id, {}).get("status") in {"loaded", "optional_missing"},
            idx.get(intake_id, {}).get("status"),
        )

    for key in (
        "post_dryrun_review_input_loaded",
        "dryrun_input_loaded",
        "planning_input_loaded",
        "post_controlled_frame_sample_roadmap_input_loaded",
        "controlled_frame_sample_closure_input_loaded",
        "controlled_frame_input_closure_input_loaded",
        "map_location_readonly_context_input_loaded",
        "safety_constitution_input_loaded",
        "minimal_runtime_integration_closure_loaded",
        "ocr_final_closure_loaded",
        "completed_phase_matrix_generated",
        "validated_capability_summary_generated",
        "disabled_file_operation_summary_generated",
        "disabled_runtime_summary_generated",
        "closure_boundary_freeze_generated",
        "non_claims_register_generated",
        "deferred_capability_pool_generated",
        "governance_debt_carryover_generated",
        "closure_readiness_gate_generated",
        "file_metadata_boundary_planning_closed",
        "file_metadata_boundary_dryrun_closed",
        "file_metadata_boundary_post_review_closed",
        "file_metadata_boundary_closed",
        "metadata_decision_simulation_only",
        "no_runtime_executed",
        "no_new_runtime_enabled",
        "gate_taxonomy_required_later",
        "midplatform_function_governance_required_later",
        "midplatform_resilience_required_later",
        "boundary_ok",
    ):
        ok(f"summary.{key}", summary.get(key) is True)

    ok("summary.closure_scope", summary.get("closure_scope") == "controlled_frame_file_metadata_boundary_closure_only")
    ok("summary.completed_phase_count>=3", summary.get("completed_phase_count", 0) >= 3, summary.get("completed_phase_count"))

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
        "fixture_registry_runtime_started",
        "manifest_to_file_metadata_candidate_mapping_runtime_started",
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

    ok("summary.violations", summary.get("violations") == [])
    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)

    ok("closure_summary.scope", closure_summary.get("closure_scope") == "controlled_frame_file_metadata_boundary_closure_only")
    ok("closure_summary.final_decision", closure_summary.get("final_decision") == FINAL_DECISION)

    phases = completed_phase_matrix.get("phases", [])
    ok("completed_phase.count>=3", completed_phase_matrix.get("phase_count", 0) >= 3)
    name_to_row = {p.get("phase_name"): p for p in phases}
    for phase_name, expected_status, expected_final in EXPECTED_PHASES:
        row = name_to_row.get(phase_name, {})
        ok(f"completed_phase.{phase_name}.present", bool(row))
        ok(f"completed_phase.{phase_name}.status", row.get("status") == expected_status, row.get("status"))
        ok(f"completed_phase.{phase_name}.final_decision", row.get("final_decision") == expected_final, row.get("final_decision"))
        ok(f"completed_phase.{phase_name}.file_op_disabled", row.get("file_operation_enabled") is False)
        ok(f"completed_phase.{phase_name}.runtime_disabled", row.get("runtime_enabled") is False)
        ok(f"completed_phase.{phase_name}.write_disabled", row.get("write_enabled") is False)

    caps = [c.get("capability") for c in validated_capability_summary.get("capabilities", [])]
    for cap in EXPECTED_CAPABILITIES:
        ok(f"capability.{cap}", cap in caps)

    disabled_ops = [r.get("operation") for r in disabled_file_ops.get("disabled_operations", [])]
    for item in EXPECTED_DISABLED_FILE_OPS:
        ok(f"disabled_file_op.{item}", item in disabled_ops)

    disabled_rts = [r.get("runtime") for r in disabled_runtime_summary.get("disabled_runtimes", [])]
    for item in EXPECTED_DISABLED_RUNTIMES:
        ok(f"disabled_runtime.{item}", item in disabled_rts)

    non_claims = [n.get("non_claim") for n in non_claims_register.get("non_claims", [])]
    for item in EXPECTED_NON_CLAIMS:
        ok(f"non_claim.{item}", item in non_claims)

    deferred = [d.get("item") for d in deferred_capability_pool.get("deferred_items", [])]
    for item in EXPECTED_DEFERRED:
        ok(f"deferred.{item}", item in deferred)

    ok("readiness_gate.verdict", closure_readiness_gate.get("verdict") == "GO")
    ok("readiness_gate.ready_for_next_phase", closure_readiness_gate.get("ready_for_next_phase") is True)

    ok("next_phase.final_decision", next_phase_recommendation.get("final_decision") == FINAL_DECISION)
    ok("next_phase.recommended", next_phase_recommendation.get("recommended_next_phase") == NEXT_PHASE)

    ok("freeze.no_file_existence", "no-file-existence-check" in closure_boundary_freeze.get("frozen_boundaries", []))
    ok("freeze.metadata_simulation", "metadata-simulation-only" in closure_boundary_freeze.get("frozen_boundaries", []))

    ok("no_file_op.closure_only", no_file_op.get("closure_only") is True)
    ok("no_file_op.simulation", no_file_op.get("metadata_decision_simulation_only") is True)
    ok("no_file_op.stat", no_file_op.get("file_stat_invoked") is False)
    ok("no_file_op.exif", no_file_op.get("exif_parsed") is False)
    ok("no_file_op.existence_claim", no_file_op.get("file_existence_check_readiness_claimed") is False)

    for report_name, report in (("no_runtime", no_runtime), ("no_write", no_write)):
        ok(f"{report_name}.no_runtime", report.get("no_runtime_executed") is True)
        ok(f"{report_name}.visual_obs", report.get("visual_observation_generated") is False)
        ok(f"{report_name}.world_model", report.get("world_model_written") is False)

    ok("governance.no_duplicate", governance_debt_carryover.get("no_duplicate_governance_module_allowed") is True)

    ok("meta.checks_total>=180", len(checks) >= 180, len(checks))
    ok("meta.min_checks", MIN_CHECKS == 180)
    ok("meta.baseline", BASELINE_REQUIREMENT == 140)

    passed = sum(1 for item in checks if item["passed"])
    verdict = "GO" if len(checks) >= MIN_CHECKS and passed == len(checks) else "NO_GO"
    report = {
        "phase": PHASE_ID,
        "verifier": verdict,
        "check_count": len(checks),
        "passed_count": passed,
        "failed_count": len(checks) - passed,
        "min_checks": MIN_CHECKS,
        "baseline_requirement": BASELINE_REQUIREMENT,
        "final_decision": FINAL_DECISION if verdict == "GO" else "CONTROLLED_FRAME_FILE_METADATA_BOUNDARY_CLOSURE_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if verdict == "GO" else PHASE_ID,
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "verifier": verdict,
                "check_count": len(checks),
                "passed_count": passed,
                "failed_count": len(checks) - passed,
                "final_decision": report["final_decision"],
                "recommended_next_phase": report["recommended_next_phase"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if verdict == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
