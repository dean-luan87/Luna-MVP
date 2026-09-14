#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Basic Navigation Loop Vision Strengthening Closure v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

PHASE_ID = "Phase-Basic-Navigation-Loop-Vision-Strengthening-Closure-v1-001"
FINAL_DECISION = "BASIC_NAVIGATION_LOOP_VISION_STRENGTHENING_CLOSED_FOR_CURRENT_MAINLINE"
NEXT_PHASE = "Phase-Post-Vision-Strengthening-Roadmap-Decision-v1-001"
MIN_CHECKS = 200
BASELINE_REQUIREMENT = 160


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-root", default="/Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/basic_navigation_loop_vision_strengthening_closure_v1_smoke_v0")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    checks: List[Dict[str, Any]] = []

    def ok(check_id: str, passed: bool, detail: Any = None) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})

    summary = _load_json(root / "summary.json")
    input_root_matrix = _load_json(root / "input_root_matrix.json")
    closure_summary = _load_json(root / "vision_strengthening_closure_summary.json")
    completed_phase_matrix = _load_json(root / "completed_phase_matrix.json")
    validated_capability_summary = _load_json(root / "validated_capability_summary.json")
    disabled_runtime_summary = _load_json(root / "disabled_runtime_summary.json")
    closure_boundary_freeze = _load_json(root / "closure_boundary_freeze.json")
    non_claims_register = _load_json(root / "vision_strengthening_non_claims_register.json")
    deferred_capability_pool = _load_json(root / "deferred_capability_pool.json")
    governance_debt_carryover = _load_json(root / "governance_debt_carryover.json")
    closure_readiness_gate = _load_json(root / "closure_readiness_gate.json")
    next_phase_recommendation = _load_json(root / "next_phase_recommendation.json")
    no_runtime_boundary_report = _load_json(root / "no_runtime_boundary_report.json")
    no_write_boundary_report = _load_json(root / "no_write_boundary_report.json")

    rows = input_root_matrix.get("rows", [])
    idx = {row.get("intake_id"): row for row in rows}
    for intake_id in (
        "post_dryrun_review",
        "dryrun",
        "visual_ocr_map_task_feedback",
        "selective_tracking",
        "world_observation_entity_feature",
        "task_aware_visual_focus",
        "midplatform_perception_orchestration",
        "return_to_vision_planning",
        "return_to_vision_preplan",
        "minimal_runtime_integration_closure",
        "ocr_final_closure",
    ):
        ok(f"input.{intake_id}", idx.get(intake_id, {}).get("loaded") is True)

    for key in (
        "post_dryrun_review_input_loaded",
        "dryrun_input_loaded",
        "visual_ocr_map_task_feedback_input_loaded",
        "selective_tracking_input_loaded",
        "world_observation_entity_feature_input_loaded",
        "task_aware_visual_focus_input_loaded",
        "midplatform_perception_orchestration_input_loaded",
        "return_to_vision_planning_input_loaded",
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
        "policy_chain_closed",
        "dryrun_chain_closed",
        "feedback_chain_closed",
        "navigation_loop_vision_strengthening_closed",
        "no_runtime_executed",
        "no_new_runtime_enabled",
        "handoff_candidate_not_fact",
        "placeholder_not_runtime",
        "boundary_ok",
    ):
        ok(f"summary.{key}", summary.get(key) is True)

    ok("summary.completed_phase_count", summary.get("completed_phase_count", 0) >= 9, summary.get("completed_phase_count"))
    for key in ("production_readiness_claimed", "live_navigation_claimed", "runtime_enablement_claimed"):
        ok(f"summary.{key}", summary.get(key) is False)
    for key in (
        "camera_invoked",
        "visual_model_invoked",
        "map_api_invoked",
        "ocr_provider_invoked",
        "ocrrequest_submitted",
        "tracking_runtime_invoked",
        "optical_flow_runtime_invoked",
        "supervision_imported",
        "supervision_invoked",
        "bytetrack_imported",
        "bytetrack_invoked",
        "ocsort_imported",
        "ocsort_invoked",
        "safety_task_arbitration_runtime_invoked",
        "speech_gate_invoked",
        "vop_invoked",
        "tts_invoked",
        "user_heard_assumed",
        "task_state_committed_now",
        "navigation_action_triggered",
        "route_modified",
        "scene_delta_generated",
        "world_model_written",
        "memory_written",
        "library_written",
        "fact_written",
        "entity_resolution_runtime_invoked",
        "fact_admission_runtime_invoked",
        "memory_consolidation_invoked",
        "library_experience_commit_invoked",
        "full_frame_ocr_allowed",
        "full_scene_tracking_allowed",
        "crowd_flow_follow_action_allowed",
        "crossing_action_instruction_allowed",
        "fixed_poi_commit_allowed",
        "identity_fact_allowed",
        "emotional_attachment_fact_allowed",
    ):
        ok(f"summary.{key}", summary.get(key) is False)
    ok("summary.violations_empty", summary.get("violations") == [])
    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)

    ok("closure_summary.scope", closure_summary.get("closure_scope") == "basic_navigation_loop_vision_strengthening_closure_only")
    ok("closure_summary.completed_phase_count", closure_summary.get("completed_phase_count", 0) >= 9)
    ok("closure_summary.final_decision", closure_summary.get("final_decision") == FINAL_DECISION)
    for ref_key in (
        "completed_phase_matrix_ref",
        "validated_capability_summary_ref",
        "disabled_runtime_summary_ref",
        "boundary_freeze_ref",
        "non_claims_register_ref",
        "deferred_capability_pool_ref",
        "governance_debt_carryover_ref",
    ):
        ok(f"closure_summary.{ref_key}", bool(closure_summary.get(ref_key)))

    phases = completed_phase_matrix.get("phases", [])
    ok("completed_phase_matrix.count", completed_phase_matrix.get("completed_phase_count", 0) >= 9)
    ok("completed_phase_matrix.all_status_ok", all(row.get("status") in {"GO", "COMPLETE"} for row in phases))
    for phase_name in (
        "Return-To-Vision Mainline Preplan v1",
        "Return-To-Vision Mainline Planning v1",
        "MidPlatform Perception Orchestration Policy v1",
        "Task-Aware Visual Focus Policy v1",
        "World Observation and Entity Feature Policy v1",
        "Selective Tracking Adapter Policy v1",
        "Visual-OCR-Map-Task Feedback DryRun v1",
        "Basic Navigation Loop Vision Strengthening DryRun v1",
        "Basic Navigation Loop Vision Strengthening Post-DryRun Review v1",
    ):
        row = next((item for item in phases if item.get("phase_id") == phase_name), {})
        ok(f"completed_phase.{phase_name}.present", bool(row))
        ok(f"completed_phase.{phase_name}.runtime_disabled", row.get("runtime_enabled") is False)
        ok(f"completed_phase.{phase_name}.write_disabled", row.get("write_enabled") is False)
        ok(f"completed_phase.{phase_name}.final_decision", bool(row.get("final_decision")))

    caps = validated_capability_summary.get("validated_capabilities", [])
    ok("validated_capability_summary.count", len(caps) >= 16, len(caps))
    for cap in (
        "MidPlatform perception orchestration policy",
        "task-aware visual focus policy",
        "scene sketch candidate schema",
        "visual focus plan schema",
        "visual focus slot schema",
        "view quality candidate",
        "active view adjustment candidate",
        "world observation candidate policy",
        "world entity feature candidate policy",
        "selective tracking adapter policy",
        "OCR activation candidate policy",
        "tracking request candidate policy",
        "map/memory context feedback candidate",
        "visual/OCR/map/task feedback dry-run",
        "basic navigation loop vision strengthening dry-run",
        "post-dryrun review",
    ):
        row = next((item for item in caps if item.get("capability_name") == cap), {})
        ok(f"validated_capability.{cap}.present", bool(row))
        ok(f"validated_capability.{cap}.runtime_disabled", row.get("runtime_enablement") is False)

    runtimes = disabled_runtime_summary.get("disabled_runtime_capabilities", [])
    ok("disabled_runtime_summary.count", len(runtimes) >= 17, len(runtimes))
    for runtime_name in (
        "camera runtime",
        "visual model runtime",
        "OCR provider runtime",
        "OCRRequest submission",
        "map API / 高德 API",
        "tracking runtime",
        "optical flow runtime",
        "Supervision / ByteTrack / OC-SORT",
        "Speech Gate runtime",
        "VOP runtime",
        "TTS runtime",
        "Safety-Task Arbitration runtime",
        "NavigationAction runtime",
        "WorldModel write runtime",
        "Memory write runtime",
        "Library write runtime",
        "SceneDelta runtime",
    ):
        row = next((item for item in runtimes if item.get("runtime_name") == runtime_name), {})
        ok(f"disabled_runtime.{runtime_name}.present", bool(row))
        ok(f"disabled_runtime.{runtime_name}.disabled", row.get("enabled") is False)

    for key in (
        "no_runtime",
        "no_write",
        "no_action",
        "no_speech",
        "no_fact",
        "candidate_only",
        "handoff_only_for_worldmodel_memory_library",
        "no_entity_resolution",
        "no_fact_admission",
        "no_memory_consolidation",
        "no_library_experience_commit",
        "no_full_frame_ocr",
        "no_full_scene_tracking",
        "no_crowd_flow_follow_action",
        "no_crossing_action_instruction",
        "no_fixed_poi_commit_for_temporary_facility",
        "no_identity_fact",
        "no_emotional_attachment_fact",
    ):
        ok(f"boundary_freeze.{key}", closure_boundary_freeze.get(key) is True)

    non_claims = non_claims_register.get("non_claims", [])
    ok("non_claims.count", len(non_claims) >= 15, len(non_claims))
    for expected in (
        "closure 不等于 live navigation",
        "dry-run 闭环不等于真实导航能力",
        "guidance candidate 不等于导航动作",
        "text-only dry output 不等于用户听见",
        "OCR activation candidate 不等于 OCRRequest 提交",
        "tracking request candidate 不等于 tracking runtime",
        "map/memory hint 不等于现实事实",
        "WorldObservationCandidate 不等于 WorldModel fact",
        "WorldEntityFeatureCandidate 不等于实体事实",
        "ObjectIdentityCandidate 不等于身份事实",
        "TemporaryFacilityCandidate 不等于固定 POI",
        "CrowdFlowFeedback 不等于跟随人流指令",
        "CrossingUncertainFeedback 不等于允许过马路",
        "SafetyArbitrationBridgeCandidate 不等于真实 arbitration runtime",
        "closure 不等于 production readiness",
    ):
        ok(f"non_claim.{expected}", expected in non_claims)
    for key in ("production_readiness_claimed", "live_navigation_claimed", "runtime_enablement_claimed"):
        ok(f"non_claims_register.{key}", non_claims_register.get(key) is False)

    deferreds = deferred_capability_pool.get("deferred_capabilities", [])
    ok("deferred_pool.count", len(deferreds) >= 19, len(deferreds))
    for expected in (
        "real camera runtime",
        "visual model integration",
        "OCR provider re-enable",
        "OCRRequest gated submission for live flow",
        "map API / 高德 API integration",
        "GPS / route context runtime",
        "tracking runtime",
        "Supervision / ByteTrack / OC-SORT experiment branch",
        "optical flow runtime",
        "real Speech Gate / VOP / TTS output",
        "Safety-Task Arbitration runtime integration",
        "NavigationAction guarded runtime",
        "WorldModel Candidate Layer",
        "Memory Governance",
        "Library Experience Governance",
        "Entity Resolution",
        "Fact Admission",
        "Crossing Decision Safety Governance",
        "MidPlatform Function Governance / Consolidation",
    ):
        row = next((item for item in deferreds if item.get("capability_name") == expected), {})
        ok(f"deferred_pool.{expected}.present", bool(row))
        ok(f"deferred_pool.{expected}.deferred", row.get("deferred") is True)

    carryover = governance_debt_carryover.get("carryover_items", [])
    ok("governance_debt.count", len(carryover) >= 10, len(carryover))
    for topic in (
        "midplatform capability expansion debt",
        "resource budget complexity",
        "privacy filtering complexity",
        "conflict correction complexity",
        "temporary facility governance complexity",
        "world observation handoff complexity",
        "duplicated schema risk",
        "visual focus policy complexity",
        "selective tracking policy complexity",
        "feedback candidate proliferation",
    ):
        row = next((item for item in carryover if item.get("topic") == topic), {})
        ok(f"governance_debt.{topic}.present", bool(row))
        ok(f"governance_debt.{topic}.carried", row.get("carried_over") is True)
    ok("governance_debt.future_midplatform_function_governance_required", governance_debt_carryover.get("future_midplatform_function_governance_required") is True)
    ok("governance_debt.no_duplicate_governance_module_allowed", governance_debt_carryover.get("no_duplicate_governance_module_allowed") is True)

    ok("readiness_gate.ready", closure_readiness_gate.get("ready_for_closure") is True)
    ok("readiness_gate.verdict", closure_readiness_gate.get("verdict") == "GO")
    ok("readiness_gate.blockers_empty", closure_readiness_gate.get("blockers") == [])
    ok("next_phase_recommendation.final_decision", next_phase_recommendation.get("final_decision") == FINAL_DECISION)
    ok("next_phase_recommendation.next_phase", next_phase_recommendation.get("recommended_next_phase") == NEXT_PHASE)

    for payload_name, payload in (("no_runtime", no_runtime_boundary_report), ("no_write", no_write_boundary_report)):
        for key in (
            "closure_only",
            "no_runtime_executed",
            "no_new_runtime_enabled",
            "handoff_candidate_not_fact",
            "placeholder_not_runtime",
            "boundary_ok",
        ):
            ok(f"{payload_name}.{key}", payload.get(key) is True)
        for key in (
            "camera_invoked",
            "visual_model_invoked",
            "map_api_invoked",
            "ocr_provider_invoked",
            "ocrrequest_submitted",
            "tracking_runtime_invoked",
            "optical_flow_runtime_invoked",
            "supervision_imported",
            "supervision_invoked",
            "bytetrack_imported",
            "bytetrack_invoked",
            "ocsort_imported",
            "ocsort_invoked",
            "safety_task_arbitration_runtime_invoked",
            "speech_gate_invoked",
            "vop_invoked",
            "tts_invoked",
            "user_heard_assumed",
            "task_state_committed_now",
            "navigation_action_triggered",
            "route_modified",
            "scene_delta_generated",
            "world_model_written",
            "memory_written",
            "library_written",
            "fact_written",
            "entity_resolution_runtime_invoked",
            "fact_admission_runtime_invoked",
            "memory_consolidation_invoked",
            "library_experience_commit_invoked",
            "full_frame_ocr_allowed",
            "full_scene_tracking_allowed",
            "crowd_flow_follow_action_allowed",
            "crossing_action_instruction_allowed",
            "fixed_poi_commit_allowed",
            "identity_fact_allowed",
            "emotional_attachment_fact_allowed",
        ):
            ok(f"{payload_name}.{key}", payload.get(key) is False)
        ok(f"{payload_name}.violations_empty", payload.get("violations") == [])

    passed = sum(1 for item in checks if item["passed"])
    verdict = "GO" if passed >= MIN_CHECKS and not any(not item["passed"] for item in checks) else "NO_GO"
    report = {
        "phase": PHASE_ID,
        "verdict": verdict,
        "checks_passed": passed,
        "checks_total": len(checks),
        "min_checks_required": MIN_CHECKS,
        "baseline_requirement": BASELINE_REQUIREMENT,
        "final_decision": FINAL_DECISION if verdict == "GO" else "BASIC_NAVIGATION_LOOP_VISION_STRENGTHENING_CLOSURE_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if verdict == "GO" else PHASE_ID,
        "failed_checks": [item for item in checks if not item["passed"]],
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"verdict": verdict, "checks_passed": passed, "checks_total": len(checks)}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
