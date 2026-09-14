#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Controlled Frame File Existence Check Guarded Closure v1 (closure-only)."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

PHASE_ID = "Phase-Controlled-Frame-File-Existence-Check-Guarded-Closure-v1-001"
FINAL_DECISION = "CONTROLLED_FRAME_FILE_EXISTENCE_CHECK_GUARDED_CLOSED_FOR_CURRENT_MAINLINE"
NEXT_PHASE = "Phase-Post-File-Existence-Check-Roadmap-Decision-v1-001"

MIN_CHECKS = 180
BASELINE_REQUIREMENT = 140

EXPECTED_PHASES = [
    (
        "Controlled Frame File Existence Check Guarded Planning v1",
        "GO",
        "CONTROLLED_FRAME_FILE_EXISTENCE_CHECK_GUARDED_PLANNING_READY_FOR_DRYRUN",
    ),
    (
        "Controlled Frame File Existence Check Guarded DryRun v1",
        "GO",
        "CONTROLLED_FRAME_FILE_EXISTENCE_CHECK_GUARDED_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW",
    ),
    (
        "Controlled Frame File Existence Check Guarded Post-DryRun Review v1",
        "GO",
        "CONTROLLED_FRAME_FILE_EXISTENCE_CHECK_GUARDED_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE",
    ),
]

EXPECTED_CAPABILITIES = [
    "file existence check gate policy",
    "allowed path scope policy",
    "blocked path scope policy",
    "authorization policy",
    "audit trace policy",
    "failure mode policy",
    "rollback policy",
    "existence decision candidate schema",
    "existence-to-file-metadata mapping policy",
    "future allowed / restricted / blocked path classification",
    "missing source_chain blocking",
    "missing privacy tags blocking",
    "missing fixture registry ref blocking",
    "authorization insufficiency detection",
    "gate denied behavior",
    "permission denied future failure mode",
    "missing file future failure mode",
    "rollback after denied candidate",
    "dry-run simulation",
    "post-dryrun review",
]

EXPECTED_DISABLED_FILE_OPS = [
    "os.path.exists",
    "pathlib.Path.exists",
    "file existence check",
    "file stat",
    "file open",
    "file content read",
    "image content read",
    "video content read",
    "image open",
    "video open",
    "video decode",
    "frame extraction",
    "EXIF parse",
    "video probe",
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
    "closure 不等于 os.path.exists 可用",
    "closure 不等于 pathlib.Path.exists 可用",
    "closure 不等于 stat 文件可用",
    "closure 不等于文件打开可用",
    "closure 不等于真实文件系统访问可用",
    "closure 不等于图像读取",
    "closure 不等于视频读取",
    "closure 不等于真实 hash",
    "closure 不等于 EXIF / video probe",
    "closure 不等于视觉模型 runtime",
    "closure 不等于 OCR/tracking/map/crossing runtime",
    "existence decision candidate 不等于文件事实",
    "existence gate dry-run 不等于 production readiness",
]


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-root",
        default=str(repo_root / "_eval_out" / "controlled_frame_file_existence_check_guarded_closure_v1_smoke_v0"),
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
    closure_summary = _load_json(root / "controlled_frame_file_existence_check_guarded_closure_summary.json")
    completed_phase_matrix = _load_json(root / "completed_phase_matrix.json")
    validated_capability_summary = _load_json(root / "validated_capability_summary.json")
    disabled_file_operation_summary = _load_json(root / "disabled_file_operation_summary.json")
    disabled_runtime_summary = _load_json(root / "disabled_runtime_summary.json")
    closure_boundary_freeze = _load_json(root / "closure_boundary_freeze.json")
    non_claims_register = _load_json(root / "file_existence_check_non_claims_register.json")
    deferred_capability_pool = _load_json(root / "deferred_capability_pool.json")
    governance_debt_carryover = _load_json(root / "governance_debt_carryover.json")
    closure_readiness_gate = _load_json(root / "closure_readiness_gate.json")
    next_phase_recommendation = _load_json(root / "next_phase_recommendation.json")
    no_file_op_boundary_report = _load_json(root / "no_file_operation_boundary_report.json")
    no_runtime_boundary_report = _load_json(root / "no_runtime_boundary_report.json")
    no_write_boundary_report = _load_json(root / "no_write_boundary_report.json")

    rows = input_root_matrix.get("rows", [])
    idx = {row.get("intake_id"): row for row in rows}
    for intake_id in (
        "post_dryrun_review",
        "dryrun",
        "planning",
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
        ok(f"input.{intake_id}.optional", idx.get(intake_id, {}).get("status") in {"loaded", "optional_missing"}, idx.get(intake_id, {}).get("status"))

    # Summary required true
    for key in (
        "post_dryrun_review_input_loaded",
        "dryrun_input_loaded",
        "planning_input_loaded",
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
        "completed_phase_matrix_generated",
        "validated_capability_summary_generated",
        "disabled_file_operation_summary_generated",
        "disabled_runtime_summary_generated",
        "closure_boundary_freeze_generated",
        "non_claims_register_generated",
        "deferred_capability_pool_generated",
        "governance_debt_carryover_generated",
        "closure_readiness_gate_generated",
        "file_existence_check_guarded_planning_closed",
        "file_existence_check_guarded_dryrun_closed",
        "file_existence_check_guarded_post_review_closed",
        "file_existence_check_guarded_closed",
        "existence_gate_decision_simulation_only",
        "cross_repo_input_roots_observed",
        "output_root_fixed_to_luna_core",
        "gate_taxonomy_required_later",
        "midplatform_function_governance_required_later",
        "midplatform_resilience_required_later",
        "no_runtime_executed",
        "no_new_runtime_enabled",
        "boundary_ok",
    ):
        ok(f"summary.{key}", summary.get(key) is True)

    ok("summary.closure_scope", summary.get("closure_scope") == "controlled_frame_file_existence_check_guarded_closure_only")
    ok("summary.completed_phase_count>=3", summary.get("completed_phase_count", 0) >= 3, summary.get("completed_phase_count"))

    # Summary required false (non-claims)
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

    ok("summary.violations==[]", summary.get("violations") == [])
    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)

    # Closure summary sanity
    ok("closure_summary.scope", closure_summary.get("closure_scope") == "controlled_frame_file_existence_check_guarded_closure_only")
    ok("closure_summary.final_decision", closure_summary.get("final_decision") == FINAL_DECISION)

    # Completed phase matrix
    phases = completed_phase_matrix.get("phases", [])
    ok("completed_phase.count>=3", completed_phase_matrix.get("phase_count", 0) >= 3)
    # Historical closure verifiers sometimes keyed by "phase_id" carrying a human label.
    # This closure matrix carries both "phase_id" (canonical phase string) and "phase_name" (human label).
    name_to_row: Dict[str, Dict[str, Any]] = {}
    for p in phases:
        if p.get("phase_name"):
            name_to_row[p["phase_name"]] = p
        if p.get("phase_id"):
            name_to_row[p["phase_id"]] = p
    for phase_name, expected_status, expected_final_decision in EXPECTED_PHASES:
        row = name_to_row.get(phase_name, {})
        ok(f"completed_phase.{phase_name}.present", bool(row))
        ok(f"completed_phase.{phase_name}.status", row.get("status") == expected_status, row.get("status"))
        ok(f"completed_phase.{phase_name}.final_decision", row.get("final_decision") == expected_final_decision, row.get("final_decision"))
        ok(f"completed_phase.{phase_name}.runtime_disabled", row.get("runtime_enabled") is False)
        ok(f"completed_phase.{phase_name}.file_op_disabled", row.get("file_operation_enabled") is False)
        ok(f"completed_phase.{phase_name}.write_disabled", row.get("write_enabled") is False)

    # Validated capabilities
    caps = [c.get("capability") for c in validated_capability_summary.get("capabilities", [])]
    for cap in EXPECTED_CAPABILITIES:
        ok(f"capability.{cap}", cap in caps)

    # Disabled file operations
    disabled_ops = [o.get("operation") for o in disabled_file_operation_summary.get("disabled_operations", [])]
    for op in EXPECTED_DISABLED_FILE_OPS:
        ok(f"disabled_op.{op}", op in disabled_ops)

    # Disabled runtimes
    disabled_rt = [r.get("runtime") for r in disabled_runtime_summary.get("disabled_runtimes", [])]
    for item in EXPECTED_DISABLED_RUNTIMES:
        ok(f"disabled_runtime.{item}", item in disabled_rt)

    # Non-claims register
    non_claims = [n.get("non_claim") for n in non_claims_register.get("non_claims", [])]
    for item in EXPECTED_NON_CLAIMS:
        ok(f"non_claim.{item}", item in non_claims)

    # Closure readiness gate
    ok("readiness_gate.verdict", closure_readiness_gate.get("verdict") == "GO")
    ok("readiness_gate.ready_for_next_phase", closure_readiness_gate.get("ready_for_next_phase") is True)

    # Next phase recommendation
    ok("next_phase.final_decision", next_phase_recommendation.get("final_decision") == FINAL_DECISION)
    ok("next_phase.recommended", next_phase_recommendation.get("recommended_next_phase") == NEXT_PHASE)

    # Boundary reports must remain strict
    for payload_name, payload in (
        ("no_file_op", no_file_op_boundary_report),
        ("no_runtime", no_runtime_boundary_report),
        ("no_write", no_write_boundary_report),
    ):
        ok(f"{payload_name}.scope", payload.get("closure_scope") == "controlled_frame_file_existence_check_guarded_closure_only")
        if payload_name != "no_file_op":
            for key in ("no_runtime_executed", "no_new_runtime_enabled", "boundary_ok"):
                ok(f"{payload_name}.{key}", payload.get(key) is True)
        ok(f"{payload_name}.violations==[]", payload.get("violations") == [])
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
        "perceptual_hash_computed",
    ):
        ok(f"no_file_op.{key}.false", no_file_op_boundary_report.get(key) is False)

    # Ensure freeze contains critical boundaries
    frozen = closure_boundary_freeze.get("frozen_boundaries", [])
    for b in (
        "no-exists-call",
        "no-os-path-exists",
        "no-pathlib-exists",
        "no-file-stat",
        "no-file-open",
        "no-image-read",
        "no-video-read",
        "no-real-hash",
        "no-runtime",
        "no-write",
        "no-action",
        "no-speech",
        "candidate-only",
        "existence-gate-simulation-only",
    ):
        ok(f"freeze.{b}", b in frozen)

    # Meta checks
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
        "final_decision": FINAL_DECISION if verdict == "GO" else "CONTROLLED_FRAME_FILE_EXISTENCE_CHECK_GUARDED_CLOSURE_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if verdict == "GO" else PHASE_ID,
        "failed_checks": [item for item in checks if not item["passed"]],
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"verdict": verdict, "checks_passed": passed, "checks_total": len(checks)}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())

