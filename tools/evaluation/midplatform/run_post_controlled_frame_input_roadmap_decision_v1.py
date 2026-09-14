#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Post Controlled Frame Input Roadmap Decision v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Dict

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.post_controlled_frame_input_roadmap_decision_v1 import (
    run_post_controlled_frame_input_roadmap_decision_v1,
)


DEFAULT_WORKSPACE_ROOT = Path("/Users/luanlei/Desktop/Luna-Workspace-Min")
DEFAULT_OUTPUT_ROOT = DEFAULT_WORKSPACE_ROOT / "_eval_out" / "post_controlled_frame_input_roadmap_decision_v1_smoke_v0"


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Post Controlled Frame Input Roadmap Decision v1")
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument(
        "--controlled-frame-input-closure-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "controlled_frame_input_closure_v1_smoke_v0"),
    )
    parser.add_argument(
        "--controlled-frame-input-post-review-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "controlled_frame_input_post_dryrun_review_v1_smoke_v0"),
    )
    parser.add_argument(
        "--controlled-frame-input-dryrun-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "controlled_frame_input_dryrun_v1_smoke_v0"),
    )
    parser.add_argument(
        "--controlled-frame-input-planning-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "controlled_frame_input_planning_v1_smoke_v0"),
    )
    parser.add_argument(
        "--map-location-readonly-context-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "map_location_readonly_context_policy_v1_smoke_v0"),
    )
    parser.add_argument(
        "--post-vision-strengthening-roadmap-decision-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "post_vision_strengthening_roadmap_decision_v1_smoke_v0"),
    )
    parser.add_argument(
        "--vision-strengthening-closure-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "basic_navigation_loop_vision_strengthening_closure_v1_smoke_v0"),
    )
    parser.add_argument(
        "--task-aware-visual-focus-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "task_aware_visual_focus_policy_v1_smoke_v0"),
    )
    parser.add_argument(
        "--midplatform-perception-orchestration-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "midplatform_perception_orchestration_policy_v1_smoke_v0"),
    )
    parser.add_argument(
        "--minimal-runtime-integration-closure-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "minimal_runtime_integration_closure_v1_smoke_v0"),
    )
    parser.add_argument(
        "--ocr-final-closure-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "ocr_mainline_final_closure_v1_smoke_v0"),
    )
    parser.add_argument(
        "--hardware-profile-capability-registry-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "hardware_profile_capability_registry_v1_smoke_v0"),
    )
    parser.add_argument(
        "--system-health-center-governance-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "system_health_center_governance_v0"),
    )
    parser.add_argument(
        "--vision-frame-trace-stream-registry-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "vision_frame_trace_stream_registry_smoke_v0"),
    )
    parser.add_argument(
        "--vision-frame-input-governance-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "vision_frame_input_governance_smoke_v0"),
    )
    parser.add_argument(
        "--safety-task-arbitration-policy-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "safety_task_arbitration_policy_v1_smoke_v0"),
    )
    parser.add_argument(
        "--crossing-decision-safety-governance-policy-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "crossing_decision_safety_governance_policy_v1_smoke_v0"),
    )
    parser.add_argument(
        "--traffic-safety-semantics-stub-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "traffic_safety_semantics_stub_v0"),
    )
    parser.add_argument(
        "--midplatform-function-governance-consolidation-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "midplatform_function_governance_consolidation_v1_smoke_v0"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = run_post_controlled_frame_input_roadmap_decision_v1(
        controlled_frame_input_closure_root=args.controlled_frame_input_closure_root,
        controlled_frame_input_post_review_root=args.controlled_frame_input_post_review_root,
        controlled_frame_input_dryrun_root=args.controlled_frame_input_dryrun_root,
        controlled_frame_input_planning_root=args.controlled_frame_input_planning_root,
        map_location_readonly_context_root=args.map_location_readonly_context_root,
        post_vision_strengthening_roadmap_decision_root=args.post_vision_strengthening_roadmap_decision_root,
        vision_strengthening_closure_root=args.vision_strengthening_closure_root,
        task_aware_visual_focus_root=args.task_aware_visual_focus_root,
        midplatform_perception_orchestration_root=args.midplatform_perception_orchestration_root,
        minimal_runtime_integration_closure_root=args.minimal_runtime_integration_closure_root,
        ocr_final_closure_root=args.ocr_final_closure_root,
        hardware_profile_capability_registry_root=args.hardware_profile_capability_registry_root,
        system_health_center_governance_root=args.system_health_center_governance_root,
        vision_frame_trace_stream_registry_root=args.vision_frame_trace_stream_registry_root,
        vision_frame_input_governance_root=args.vision_frame_input_governance_root,
        safety_task_arbitration_policy_root=args.safety_task_arbitration_policy_root,
        crossing_decision_safety_governance_policy_root=args.crossing_decision_safety_governance_policy_root,
        traffic_safety_semantics_stub_root=args.traffic_safety_semantics_stub_root,
        midplatform_function_governance_consolidation_root=args.midplatform_function_governance_consolidation_root,
    )
    output_root = Path(args.output_root)
    for name in (
        "summary",
        "input_root_matrix",
        "post_controlled_frame_input_roadmap_decision",
        "current_controlled_frame_input_status_summary",
        "completed_capability_summary",
        "route_option_matrix",
        "priority_ranking",
        "recommended_next_phase_decision",
        "deferred_resilience_distributed_midplatform_register",
        "deferred_exploration_drive_register",
        "deferred_worldmodel_memory_library_emotion_register",
        "boundary_freeze",
        "governance_debt_roadmap_register",
        "non_claims_register",
        "next_phase_recommendation",
        "no_runtime_boundary_report",
        "no_write_boundary_report",
    ):
        _write_json(output_root / f"{name}.json", result[name])
    print(
        json.dumps(
            {
                "output_root": str(output_root),
                "decision_scope": result["summary"]["decision_scope"],
                "final_decision": result["summary"]["final_decision"],
                "recommended_next_phase": result["summary"]["recommended_next_phase"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
