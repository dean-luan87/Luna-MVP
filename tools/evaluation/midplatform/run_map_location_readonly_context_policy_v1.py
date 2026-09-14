#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Map Location ReadOnly Context Policy v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Dict

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.map_location_readonly_context_policy_v1 import (
    run_map_location_readonly_context_policy_v1,
)


DEFAULT_WORKSPACE_ROOT = Path("/Users/luanlei/Desktop/Luna-Workspace-Min")
DEFAULT_OUTPUT_ROOT = DEFAULT_WORKSPACE_ROOT / "_eval_out" / "map_location_readonly_context_policy_v1_smoke_v0"


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Map Location ReadOnly Context Policy v1")
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument("--post-vision-strengthening-roadmap-decision-root", default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "post_vision_strengthening_roadmap_decision_v1_smoke_v0"))
    parser.add_argument("--vision-strengthening-closure-root", default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "basic_navigation_loop_vision_strengthening_closure_v1_smoke_v0"))
    parser.add_argument("--post-dryrun-review-root", default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "basic_navigation_loop_vision_strengthening_post_dryrun_review_v1_smoke_v0"))
    parser.add_argument("--dryrun-root", default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "basic_navigation_loop_vision_strengthening_dryrun_v1_smoke_v0"))
    parser.add_argument("--visual-ocr-map-task-feedback-root", default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "visual_ocr_map_task_feedback_dryrun_v1_smoke_v0"))
    parser.add_argument("--selective-tracking-root", default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "selective_tracking_adapter_policy_v1_smoke_v0"))
    parser.add_argument("--world-observation-entity-feature-root", default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "world_observation_and_entity_feature_policy_v1_smoke_v0"))
    parser.add_argument("--task-aware-visual-focus-root", default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "task_aware_visual_focus_policy_v1_smoke_v0"))
    parser.add_argument("--midplatform-perception-orchestration-root", default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "midplatform_perception_orchestration_policy_v1_smoke_v0"))
    parser.add_argument("--minimal-runtime-integration-closure-root", default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "minimal_runtime_integration_closure_v1_smoke_v0"))
    parser.add_argument("--ocr-final-closure-root", default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "ocr_mainline_final_closure_v1_smoke_v0"))
    parser.add_argument("--map-anchor-context-output-root", default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "map_anchor_context_output_v1_smoke_v0"))
    parser.add_argument("--gps-route-context-output-root", default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "gps_route_context_output_v1_smoke_v0"))
    parser.add_argument("--route-context-preplan-root", default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "map_route_location_context_preplan_v1"))
    parser.add_argument("--basic-navigation-guidance-loop-output-root", default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "basic_navigation_guidance_loop_dryrun_v1_smoke_v0"))
    parser.add_argument("--basic-navigation-loop-stabilization-root", default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "basic_navigation_guidance_loop_stabilization_test_v1_smoke_v0"))
    parser.add_argument("--safety-task-arbitration-policy-root", default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "safety_task_arbitration_policy_v1_smoke_v0"))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = run_map_location_readonly_context_policy_v1(
        post_vision_strengthening_roadmap_decision_root=args.post_vision_strengthening_roadmap_decision_root,
        vision_strengthening_closure_root=args.vision_strengthening_closure_root,
        post_dryrun_review_root=args.post_dryrun_review_root,
        dryrun_root=args.dryrun_root,
        visual_ocr_map_task_feedback_root=args.visual_ocr_map_task_feedback_root,
        selective_tracking_root=args.selective_tracking_root,
        world_observation_entity_feature_root=args.world_observation_entity_feature_root,
        task_aware_visual_focus_root=args.task_aware_visual_focus_root,
        midplatform_perception_orchestration_root=args.midplatform_perception_orchestration_root,
        minimal_runtime_integration_closure_root=args.minimal_runtime_integration_closure_root,
        ocr_final_closure_root=args.ocr_final_closure_root,
        map_anchor_context_output_root=args.map_anchor_context_output_root,
        gps_route_context_output_root=args.gps_route_context_output_root,
        route_context_preplan_root=args.route_context_preplan_root,
        basic_navigation_guidance_loop_output_root=args.basic_navigation_guidance_loop_output_root,
        basic_navigation_loop_stabilization_root=args.basic_navigation_loop_stabilization_root,
        safety_task_arbitration_policy_root=args.safety_task_arbitration_policy_root,
    )
    output_root = Path(args.output_root)
    for name in (
        "summary",
        "input_root_matrix",
        "map_location_readonly_context_policy",
        "map_location_context_candidate_schema",
        "route_stage_hint_candidate_schema",
        "target_proximity_hint_candidate_schema",
        "side_orientation_hint_candidate_schema",
        "entrance_intersection_hint_candidate_schema",
        "map_visual_memory_conflict_policy",
        "map_location_to_visual_focus_binding_policy",
        "map_location_to_ocr_activation_hint_policy",
        "map_location_feedback_policy",
        "map_location_readonly_context_scenario_matrix",
        "map_location_boundary_matrix",
        "governance_debt_register",
        "next_phase_recommendation",
        "no_runtime_boundary_report",
        "no_write_boundary_report",
    ):
        _write_json(output_root / f"{name}.json", result[name])
    print(json.dumps({"output_root": str(output_root), "final_decision": result["summary"]["final_decision"], "recommended_next_phase": result["summary"]["recommended_next_phase"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
