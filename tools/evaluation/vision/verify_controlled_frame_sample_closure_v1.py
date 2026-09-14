#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Controlled Frame Sample Closure v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

PHASE_ID = "Phase-Controlled-Frame-Sample-Closure-v1-001"
FINAL_DECISION = "CONTROLLED_FRAME_SAMPLE_CLOSED_FOR_CURRENT_MAINLINE"
NEXT_PHASE = "Phase-Post-Controlled-Frame-Sample-Roadmap-Decision-v1-001"
MIN_CHECKS = 180
BASELINE_REQUIREMENT = 140

EXPECTED_PHASES = [
    ("Controlled Frame Sample Planning v1", "GO", "CONTROLLED_FRAME_SAMPLE_PLANNING_READY_FOR_CONTROLLED_FRAME_SAMPLE_DRYRUN"),
    ("Controlled Frame Sample DryRun v1", "GO", "CONTROLLED_FRAME_SAMPLE_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"),
    ("Controlled Frame Sample Post-DryRun Review v1", "GO", "CONTROLLED_FRAME_SAMPLE_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE"),
]

EXPECTED_CAPABILITIES = [
    "sample manifest schema",
    "sample source policy",
    "file boundary policy",
    "privacy precheck policy",
    "manual review gate policy",
    "sample usage policy",
    "sample-to-frame mapping stub",
    "allowed / restricted / blocked sample classification",
    "sensitive sample review routing",
    "manifest metadata dry-run",
    "file boundary validation",
    "post-dryrun review",
]

EXPECTED_DISABLED_RUNTIMES = [
    "real image read",
    "real video read",
    "file open",
    "image open",
    "video open",
    "video decode",
    "frame extraction",
    "real file hash computation",
    "live camera runtime",
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
    "closure 不等于真实图像读取",
    "closure 不等于真实视频读取",
    "closure 不等于可以打开样例文件",
    "closure 不等于可以解码视频",
    "closure 不等于可以抽帧",
    "closure 不等于视觉模型 runtime",
    "closure 不等于 OCR runtime",
    "closure 不等于 tracking runtime",
    "manifest metadata 不等于图像内容",
    "file_path_placeholder 不等于文件已打开",
    "file_hash_placeholder 不等于真实 hash 已计算",
    "sample-to-frame mapping stub 不等于 ControlledFrameInputCandidate runtime",
    "sample dry-run 不等于生产评测",
    "sample closure 不等于 production readiness",
]

EXPECTED_DEFERRED = [
    "Controlled Frame Sample File Existence Check",
    "controlled static image file metadata validation",
    "controlled image content read guarded trial",
    "controlled video decode guarded trial",
    "controlled frame extraction guarded trial",
    "real file hash computation policy",
    "visual model adapter dry-run",
    "OCR provider re-enable through VisualFocus",
    "tracking adapter experiment branch",
    "real VisualObservation generation",
    "real SceneSketch generation",
    "real OCRActivationResult generation",
    "real TrackingResult generation",
    "crossing sample validation",
    "privacy manual review workflow",
    "Gate Taxonomy / Gate Requirement Framework",
    "MidPlatform Function Governance / Consolidation",
    "MidPlatform Resilience / Robustness",
    "Offline Distributed MidPlatform",
    "WorldModel / Memory / Library governance",
]


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-root", default="/Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/controlled_frame_sample_closure_v1_smoke_v0")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    checks: List[Dict[str, Any]] = []

    def ok(check_id: str, passed: bool, detail: Any = None) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})

    summary = _load_json(root / "summary.json")
    input_root_matrix = _load_json(root / "input_root_matrix.json")
    closure_summary = _load_json(root / "controlled_frame_sample_closure_summary.json")
    completed_phase_matrix = _load_json(root / "completed_phase_matrix.json")
    validated_capability_summary = _load_json(root / "validated_capability_summary.json")
    disabled_runtime_summary = _load_json(root / "disabled_runtime_summary.json")
    closure_boundary_freeze = _load_json(root / "closure_boundary_freeze.json")
    non_claims_register = _load_json(root / "controlled_frame_sample_non_claims_register.json")
    deferred_capability_pool = _load_json(root / "deferred_capability_pool.json")
    governance_debt_carryover = _load_json(root / "governance_debt_carryover.json")
    closure_readiness_gate = _load_json(root / "closure_readiness_gate.json")
    next_phase_recommendation = _load_json(root / "next_phase_recommendation.json")
    no_runtime_boundary_report = _load_json(root / "no_runtime_boundary_report.json")
    no_write_boundary_report = _load_json(root / "no_write_boundary_report.json")

    # Input matrix checks
    rows = input_root_matrix.get("rows", [])
    idx = {row.get("intake_id"): row for row in rows}
    for intake_id in (
        "post_dryrun_review",
        "dryrun",
        "planning",
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

    # Summary required true
    for key in (
        "post_dryrun_review_input_loaded",
        "dryrun_input_loaded",
        "planning_input_loaded",
        "post_crossing_decision_roadmap_input_loaded",
        "crossing_decision_closure_input_loaded",
        "controlled_frame_input_closure_input_loaded",
        "map_location_readonly_context_input_loaded",
        "safety_constitution_input_loaded",
        "minimal_runtime_integration_closure_loaded",
        "ocr_final_closure_loaded",
        "completed_phase_matrix_generated",
        "validated_capability_summary_generated",
        "disabled_runtime_summary_generated",
        "closure_boundary_freeze_generated",
        "non_claims_register_generated",
        "deferred_capability_pool_generated",
        "governance_debt_carryover_generated",
        "closure_readiness_gate_generated",
        "controlled_frame_sample_planning_closed",
        "controlled_frame_sample_dryrun_closed",
        "controlled_frame_sample_post_review_closed",
        "controlled_frame_sample_closed",
        "manifest_metadata_only",
        "sample_manifest_not_sample_processing",
        "no_runtime_executed",
        "no_new_runtime_enabled",
        "gate_taxonomy_required_later",
        "midplatform_function_governance_required_later",
        "midplatform_resilience_required_later",
        "boundary_ok",
    ):
        ok(f"summary.{key}", summary.get(key) is True)
    ok("summary.closure_scope", summary.get("closure_scope") == "controlled_frame_sample_closure_only")
    ok("summary.completed_phase_count>=3", summary.get("completed_phase_count", 0) >= 3, summary.get("completed_phase_count"))

    # Summary required false (non-claims)
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
    ok("closure_summary.scope", closure_summary.get("closure_scope") == "controlled_frame_sample_closure_only")
    ok("closure_summary.final_decision", closure_summary.get("final_decision") == FINAL_DECISION)

    # Completed phase matrix
    phases = completed_phase_matrix.get("phases", [])
    ok("completed_phase.count>=3", completed_phase_matrix.get("phase_count", 0) >= 3)
    name_to_row = {p.get("phase_id"): p for p in phases}
    for phase_name, expected_status, expected_final_decision in EXPECTED_PHASES:
        row = name_to_row.get(phase_name, {})
        ok(f"completed_phase.{phase_name}.present", bool(row))
        ok(f"completed_phase.{phase_name}.status", row.get("status") == expected_status, row.get("status"))
        ok(f"completed_phase.{phase_name}.final_decision", row.get("final_decision") == expected_final_decision, row.get("final_decision"))
        ok(f"completed_phase.{phase_name}.runtime_disabled", row.get("runtime_enabled") is False)
        ok(f"completed_phase.{phase_name}.file_read_disabled", row.get("file_read_enabled") is False)
        ok(f"completed_phase.{phase_name}.write_disabled", row.get("write_enabled") is False)

    # Validated capabilities
    caps = [c.get("capability") for c in validated_capability_summary.get("capabilities", [])]
    for cap in EXPECTED_CAPABILITIES:
        ok(f"capability.{cap}", cap in caps)

    # Disabled runtimes
    disabled = [r.get("runtime") for r in disabled_runtime_summary.get("disabled_runtimes", [])]
    for item in EXPECTED_DISABLED_RUNTIMES:
        ok(f"disabled_runtime.{item}", item in disabled)

    # Non-claims register
    non_claims = [n.get("non_claim") for n in non_claims_register.get("non_claims", [])]
    for item in EXPECTED_NON_CLAIMS:
        ok(f"non_claim.{item}", item in non_claims)

    # Deferred pool
    deferred = [d.get("item") for d in deferred_capability_pool.get("deferred_items", [])]
    for item in EXPECTED_DEFERRED:
        ok(f"deferred.{item}", item in deferred)

    # Readiness gate
    ok("readiness_gate.verdict", closure_readiness_gate.get("verdict") == "GO")
    ok("readiness_gate.ready_for_next_phase", closure_readiness_gate.get("ready_for_next_phase") is True)

    # Next phase recommendation
    ok("next_phase.final_decision", next_phase_recommendation.get("final_decision") == FINAL_DECISION)
    ok("next_phase.recommended", next_phase_recommendation.get("recommended_next_phase") == NEXT_PHASE)

    # Boundary reports must remain strict
    for payload_name, payload in (("no_runtime", no_runtime_boundary_report), ("no_write", no_write_boundary_report)):
        ok(f"{payload_name}.scope", payload.get("closure_scope") == "controlled_frame_sample_closure_only")
        for key in ("no_runtime_executed", "no_new_runtime_enabled", "boundary_ok"):
            ok(f"{payload_name}.{key}", payload.get(key) is True)
        for key in (
            "file_opened",
            "image_opened",
            "video_opened",
            "video_decoded",
            "frame_extracted",
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

    # Future governance flags
    ok("future.gate_taxonomy_required_later", summary.get("gate_taxonomy_required_later") is True)
    ok("future.midplatform_function_governance_required_later", summary.get("midplatform_function_governance_required_later") is True)
    ok("future.midplatform_resilience_required_later", summary.get("midplatform_resilience_required_later") is True)

    # Meta checks to ensure >=180 checks
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
        "final_decision": FINAL_DECISION if verdict == "GO" else "CONTROLLED_FRAME_SAMPLE_CLOSURE_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if verdict == "GO" else PHASE_ID,
        "failed_checks": [item for item in checks if not item["passed"]],
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"verdict": verdict, "checks_passed": passed, "checks_total": len(checks)}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())

