#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Controlled Frame Input Closure v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

PHASE_ID = "Phase-Controlled-Frame-Input-Closure-v1-001"
FINAL_DECISION = "CONTROLLED_FRAME_INPUT_CLOSED_FOR_CURRENT_MAINLINE"
NEXT_PHASE = "Phase-Post-Controlled-Frame-Input-Roadmap-Decision-v1-001"
MIN_CHECKS = 180
BASELINE_REQUIREMENT = 140

EXPECTED_PHASES = [
    ("Controlled Frame Input Planning v1", "GO", "CONTROLLED_FRAME_INPUT_PLANNING_READY_FOR_CONTROLLED_FRAME_INPUT_DRYRUN"),
    ("Controlled Frame Input DryRun v1", "GO", "CONTROLLED_FRAME_INPUT_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"),
    ("Controlled Frame Input Post-DryRun Review v1", "GO", "CONTROLLED_FRAME_INPUT_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE"),
]

EXPECTED_CAPABILITIES = [
    "controlled frame source candidate policy",
    "frame intake gate",
    "frame quality gate",
    "frame privacy tagging policy",
    "frame STC / freshness reuse",
    "frame downstream handoff policy",
    "controlled frame dry-run metadata simulation",
    "allowed / rejected / restricted / stale frame scenario coverage",
    "dual-device redundant perception placeholder",
    "post-dryrun review",
]

EXPECTED_DISABLED_RUNTIMES = [
    "live camera runtime",
    "device camera runtime",
    "external stream runtime",
    "actual image loading",
    "visual model runtime",
    "OCR provider runtime",
    "OCRRequest submission",
    "map API / 高德 API",
    "GPS runtime",
    "tracking runtime",
    "optical flow runtime",
    "Supervision / ByteTrack / OC-SORT",
    "dual-device runtime",
    "dual-model runtime",
    "failover runtime",
    "multi-input fusion runtime",
    "Speech Gate / VOP / TTS",
    "NavigationAction",
    "WorldModel write",
    "Memory write",
    "Library write",
    "Fact write",
]

EXPECTED_NON_CLAIMS = [
    "closure 不等于 live camera 可用",
    "closure 不等于真实视觉 runtime",
    "closure 不等于可以读取真实图像",
    "metadata dry-run 不等于图像推理",
    "static_test_image candidate 不等于真实图像已读取",
    "pre_recorded_video_frame candidate 不等于真实视频已处理",
    "simulation_frame candidate 不等于真实世界 observation",
    "controlled_uploaded_frame candidate 不等于用户文件处理 runtime",
    "dual-device placeholder 不等于硬件阶段",
    "failover placeholder 不等于可自动故障切换",
    "multi-input consistency placeholder 不等于多输入融合",
    "frame candidate 不等于事实",
    "downstream handoff candidate 不等于下游 runtime",
]

EXPECTED_DEFERRED = [
    "Controlled Frame Sample Planning",
    "controlled real file/static image sample trial",
    "live camera guarded trial",
    "device camera capability registry",
    "visual model adapter",
    "OCR provider re-enable through VisualFocus",
    "tracking adapter experiment branch",
    "dual-device hardware planning",
    "device health registry",
    "failover policy runtime",
    "multi-input fusion governance",
    "WorldModel Candidate Layer",
    "Memory Governance",
    "Library Governance",
    "MidPlatform Function Governance / Consolidation",
    "MidPlatform Resilience / Robustness",
    "Offline Distributed MidPlatform Architecture Preplan",
]

EXPECTED_DEBT_TOPICS = [
    "frame source policy complexity",
    "privacy tagging complexity",
    "frame quality gate complexity",
    "STC/freshness integration complexity",
    "downstream handoff complexity",
    "dual-device placeholder future complexity",
    "hardware-stage deferred debt",
    "controlled sample planning deferred",
]


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-root", default="/Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/controlled_frame_input_closure_v1_smoke_v0")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    checks: List[Dict[str, Any]] = []

    def ok(check_id: str, passed: bool, detail: Any = None) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})

    summary = _load_json(root / "summary.json")
    input_root_matrix = _load_json(root / "input_root_matrix.json")
    controlled_frame_input_closure_summary = _load_json(root / "controlled_frame_input_closure_summary.json")
    completed_phase_matrix = _load_json(root / "completed_phase_matrix.json")
    validated_capability_summary = _load_json(root / "validated_capability_summary.json")
    disabled_runtime_summary = _load_json(root / "disabled_runtime_summary.json")
    closure_boundary_freeze = _load_json(root / "closure_boundary_freeze.json")
    controlled_frame_input_non_claims_register = _load_json(root / "controlled_frame_input_non_claims_register.json")
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
        "planning",
        "map_location_readonly_context",
        "post_vision_strengthening_roadmap_decision",
        "vision_strengthening_closure",
        "task_aware_visual_focus",
        "midplatform_perception_orchestration",
        "minimal_runtime_integration_closure",
        "ocr_final_closure",
    ):
        ok(f"input.{intake_id}", idx.get(intake_id, {}).get("loaded") is True)
    for intake_id in (
        "vision_frame_trace_stream_registry",
        "vision_frame_input_governance",
        "vision_roi_proposal_stub",
        "hardware_profile_capability_registry",
        "system_health_center_governance",
        "simulation_lab_profile",
    ):
        ok(f"input.{intake_id}.optional", idx.get(intake_id, {}).get("status") in {"loaded", "optional_missing"}, idx.get(intake_id, {}).get("status"))
    ok("input.row_count", input_root_matrix.get("row_count") == len(rows), input_root_matrix.get("row_count"))

    for key in (
        "post_dryrun_review_input_loaded",
        "dryrun_input_loaded",
        "planning_input_loaded",
        "map_location_readonly_context_input_loaded",
        "post_vision_strengthening_roadmap_decision_input_loaded",
        "vision_strengthening_closure_input_loaded",
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
        "controlled_frame_input_planning_closed",
        "controlled_frame_input_dryrun_closed",
        "controlled_frame_input_post_review_closed",
        "controlled_frame_input_closed",
        "frame_to_ocr_requires_visual_focus",
        "frame_to_tracking_requires_visual_focus",
        "frame_to_world_observation_requires_policy",
        "dual_device_redundant_perception_placeholder_retained",
        "hardware_stage_deferred",
        "no_runtime_executed",
        "no_new_runtime_enabled",
        "boundary_ok",
    ):
        ok(f"summary.{key}", summary.get(key) is True)
    for key in (
        "controlled_sample_planning_started",
        "live_camera_claimed",
        "visual_runtime_claimed",
        "image_read_claimed",
        "production_readiness_claimed",
        "runtime_enablement_claimed",
        "frame_content_loaded",
        "actual_image_read",
        "live_camera_allowed",
        "device_camera_allowed",
        "external_stream_allowed",
        "camera_invoked",
        "camera_opened",
        "video_capture_invoked",
        "visual_model_invoked",
        "map_api_invoked",
        "gaode_api_invoked",
        "gps_runtime_invoked",
        "ocr_provider_invoked",
        "ocrrequest_submitted",
        "tracking_runtime_invoked",
        "optical_flow_runtime_invoked",
        "supervision_invoked",
        "bytetrack_invoked",
        "ocsort_invoked",
        "dual_device_runtime_invoked",
        "dual_model_runtime_invoked",
        "failover_runtime_invoked",
        "multi_input_fusion_runtime_invoked",
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
        "entity_resolution_runtime_invoked",
        "fact_admission_runtime_invoked",
        "memory_consolidation_invoked",
        "library_experience_commit_invoked",
        "frame_to_navigation_action_allowed",
        "frame_to_speech_output_allowed",
        "frame_to_worldmodel_write_allowed",
        "frame_to_memory_write_allowed",
        "frame_to_fact_write_allowed",
    ):
        ok(f"summary.{key}", summary.get(key) is False)
    ok("summary.closure_scope", summary.get("closure_scope") == "controlled_frame_input_closure_only")
    ok("summary.completed_phase_count", summary.get("completed_phase_count", 0) >= 3, summary.get("completed_phase_count"))
    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.violations", summary.get("violations") == [])

    ok("closure_summary.id", controlled_frame_input_closure_summary.get("closure_id") == "cfic_v1_001")
    ok("closure_summary.scope", controlled_frame_input_closure_summary.get("closure_scope") == "controlled_frame_input_closure_only")
    ok("closure_summary.phase_chain", len(controlled_frame_input_closure_summary.get("source_phase_chain", [])) == 3)
    ok("closure_summary.completed_count", controlled_frame_input_closure_summary.get("completed_phase_count", 0) >= 3)
    for key in (
        "completed_phase_matrix_ref",
        "validated_capability_summary_ref",
        "disabled_runtime_summary_ref",
        "closure_boundary_freeze_ref",
        "non_claims_register_ref",
        "deferred_capability_pool_ref",
        "governance_debt_carryover_ref",
    ):
        ok(f"closure_summary.{key}", isinstance(controlled_frame_input_closure_summary.get(key), str) and controlled_frame_input_closure_summary.get(key).endswith(".json"))
    ok("closure_summary.next_phase", controlled_frame_input_closure_summary.get("next_phase_recommendation") == NEXT_PHASE)
    ok("closure_summary.final_decision", controlled_frame_input_closure_summary.get("final_decision") == FINAL_DECISION)
    ok("closure_summary.source_chain", controlled_frame_input_closure_summary.get("source_chain") == "controlled_frame_input_closure_v1")

    phases = completed_phase_matrix.get("phases", [])
    phase_idx = {row.get("phase_id"): row for row in phases}
    ok("completed_phase_matrix.count", completed_phase_matrix.get("completed_phase_count") == len(phases), completed_phase_matrix.get("completed_phase_count"))
    ok("completed_phase_matrix.phase_count_gte_3", len(phases) >= 3, len(phases))
    for phase_name, expected_verdict, expected_decision in EXPECTED_PHASES:
        row = phase_idx.get(phase_name, {})
        ok(f"completed_phase.{phase_name}.present", phase_name in phase_idx)
        ok(f"completed_phase.{phase_name}.status", row.get("status") == "GO", row.get("status"))
        ok(f"completed_phase.{phase_name}.verifier", row.get("verifier_verdict") == expected_verdict, row.get("verifier_verdict"))
        ok(f"completed_phase.{phase_name}.decision", row.get("final_decision") == expected_decision, row.get("final_decision"))
        ok(f"completed_phase.{phase_name}.runtime_enabled", row.get("runtime_enabled") is False)
        ok(f"completed_phase.{phase_name}.write_enabled", row.get("write_enabled") is False)
        ok(f"completed_phase.{phase_name}.output_dir", isinstance(row.get("output_dir"), str) and row.get("output_dir").startswith("_eval_out/"))
        ok(f"completed_phase.{phase_name}.role", bool(row.get("role_in_closure")))

    validated_caps = set(validated_capability_summary.get("validated_capabilities", []))
    for capability in EXPECTED_CAPABILITIES:
        ok(f"validated_capability.{capability}", capability in validated_caps)
    layers = set(validated_capability_summary.get("validation_layers", []))
    for layer in ("planning", "metadata_dryrun", "review"):
        ok(f"validated_layers.{layer}", layer in layers, sorted(layers))
    clarifications = validated_capability_summary.get("clarifications", [])
    ok("validated_clarifications.count", len(clarifications) >= 3)
    ok("validated_clarifications.no_runtime", any("真实 frame runtime" in item for item in clarifications))
    ok("validated_clarifications.no_real_vision", any("真实视觉能力" in item for item in clarifications))

    disabled_runtimes = set(disabled_runtime_summary.get("disabled_runtimes", []))
    for runtime_name in EXPECTED_DISABLED_RUNTIMES:
        ok(f"disabled_runtime.{runtime_name}", runtime_name in disabled_runtimes)
    ok("disabled_runtime.live_camera_allowed", disabled_runtime_summary.get("live_camera_allowed") is False)
    ok("disabled_runtime.device_camera_allowed", disabled_runtime_summary.get("device_camera_allowed") is False)
    ok("disabled_runtime.external_stream_allowed", disabled_runtime_summary.get("external_stream_allowed") is False)

    for key in (
        "no_runtime",
        "no_write",
        "no_action",
        "no_speech",
        "no_fact",
        "no_live_camera",
        "no_device_camera",
        "no_external_stream",
        "no_actual_image_read",
        "no_visual_model",
        "no_OCR_provider",
        "no_tracking_runtime",
        "no_map_api",
        "no_dual_device_runtime",
        "no_failover_runtime",
        "no_multi_input_fusion",
        "frame_to_ocr_requires_visual_focus",
        "frame_to_tracking_requires_visual_focus",
        "frame_to_world_observation_requires_policy",
    ):
        ok(f"boundary_freeze.{key}", closure_boundary_freeze.get(key) is True)
    for key in (
        "frame_to_navigation_action_allowed",
        "frame_to_speech_output_allowed",
        "frame_to_worldmodel_write_allowed",
        "frame_to_memory_write_allowed",
        "frame_to_fact_write_allowed",
    ):
        ok(f"boundary_freeze.{key}", closure_boundary_freeze.get(key) is False)

    non_claims = set(controlled_frame_input_non_claims_register.get("non_claims", []))
    for claim in EXPECTED_NON_CLAIMS:
        ok(f"non_claim.{claim}", claim in non_claims)
    ok("non_claim.count", len(non_claims) >= len(EXPECTED_NON_CLAIMS), len(non_claims))

    deferred = set(deferred_capability_pool.get("deferred_capabilities", []))
    for capability in EXPECTED_DEFERRED:
        ok(f"deferred.{capability}", capability in deferred)
    ok("deferred.count", len(deferred) >= len(EXPECTED_DEFERRED), len(deferred))
    ok("deferred.controlled_sample_planning_started", deferred_capability_pool.get("controlled_sample_planning_started") is False)

    carryover_topics = set(governance_debt_carryover.get("carryover_topics", []))
    for topic in EXPECTED_DEBT_TOPICS:
        ok(f"debt.{topic}", topic in carryover_topics)
    ok("debt.inherited_topics_count", len(governance_debt_carryover.get("inherited_review_topics", [])) >= 5, len(governance_debt_carryover.get("inherited_review_topics", [])))
    ok("debt.future_midplatform_function_governance_required", governance_debt_carryover.get("future_midplatform_function_governance_required") is True)
    ok("debt.future_midplatform_resilience_governance_required", governance_debt_carryover.get("future_midplatform_resilience_governance_required") is True)
    ok("debt.no_duplicate_governance_module_allowed", governance_debt_carryover.get("no_duplicate_governance_module_allowed") is True)

    go_conditions = set(closure_readiness_gate.get("go_conditions", []))
    no_go_conditions = set(closure_readiness_gate.get("no_go_conditions", []))
    for cond in (
        "planning input loaded",
        "dryrun input loaded",
        "post-dryrun review loaded",
        "completed phase matrix generated",
        "boundary freeze generated",
        "non-claims generated",
        "deferred capability pool generated",
        "governance debt carryover generated",
        "no runtime",
        "no write",
        "no action",
        "no speech",
        "no live camera",
        "no image read",
        "no dual-device runtime",
        "next phase fixed",
    ):
        ok(f"closure_gate.go.{cond}", cond in go_conditions)
    for cond in (
        "any required root missing",
        "camera opened",
        "image content loaded",
        "visual model invoked",
        "OCR provider invoked",
        "tracking runtime invoked",
        "map API invoked",
        "WorldModel/Memory/Fact write",
        "NavigationAction triggered",
        "dual-device/failover runtime enabled",
        "closure claims production readiness",
        "next phase unclear",
    ):
        ok(f"closure_gate.no_go.{cond}", cond in no_go_conditions)
    ok("closure_gate.ready", closure_readiness_gate.get("ready_for_closure") is True)
    ok("closure_gate.blockers", closure_readiness_gate.get("blockers") == [])

    ok("next_phase.final_decision", next_phase_recommendation.get("final_decision") == FINAL_DECISION)
    ok("next_phase.recommended_next_phase", next_phase_recommendation.get("recommended_next_phase") == NEXT_PHASE)

    for report_name, report in (
        ("no_runtime_boundary_report", no_runtime_boundary_report),
        ("no_write_boundary_report", no_write_boundary_report),
    ):
        ok(f"{report_name}.closure_scope", report.get("closure_scope") == "controlled_frame_input_closure_only")
        ok(f"{report_name}.closure_only", report.get("closure_only") is True)
        for key in (
            "no_runtime_executed",
            "no_new_runtime_enabled",
            "frame_to_ocr_requires_visual_focus",
            "frame_to_tracking_requires_visual_focus",
            "frame_to_world_observation_requires_policy",
            "dual_device_redundant_perception_placeholder_retained",
            "hardware_stage_deferred",
            "boundary_ok",
        ):
            ok(f"{report_name}.{key}", report.get(key) is True)
        for key in (
            "frame_content_loaded",
            "actual_image_read",
            "live_camera_allowed",
            "device_camera_allowed",
            "external_stream_allowed",
            "camera_invoked",
            "camera_opened",
            "video_capture_invoked",
            "visual_model_invoked",
            "map_api_invoked",
            "gaode_api_invoked",
            "gps_runtime_invoked",
            "ocr_provider_invoked",
            "ocrrequest_submitted",
            "tracking_runtime_invoked",
            "optical_flow_runtime_invoked",
            "supervision_invoked",
            "bytetrack_invoked",
            "ocsort_invoked",
            "dual_device_runtime_invoked",
            "dual_model_runtime_invoked",
            "failover_runtime_invoked",
            "multi_input_fusion_runtime_invoked",
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
            "entity_resolution_runtime_invoked",
            "fact_admission_runtime_invoked",
            "memory_consolidation_invoked",
            "library_experience_commit_invoked",
            "frame_to_navigation_action_allowed",
            "frame_to_speech_output_allowed",
            "frame_to_worldmodel_write_allowed",
            "frame_to_memory_write_allowed",
            "frame_to_fact_write_allowed",
        ):
            ok(f"{report_name}.{key}", report.get(key) is False)
        ok(f"{report_name}.violations", report.get("violations") == [])

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
    print(json.dumps({k: verifier_report[k] for k in ("verifier", "check_count", "passed_count", "failed_count", "final_decision", "recommended_next_phase")}, ensure_ascii=False))
    return 0 if verifier_report["verifier"] == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
