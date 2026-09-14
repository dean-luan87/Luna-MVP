#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Post Crossing Decision Roadmap Decision v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Dict

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.post_crossing_decision_roadmap_decision_v1 import (
    run_post_crossing_decision_roadmap_decision_v1,
)

DEFAULT_WORKSPACE_ROOT = Path("/Users/luanlei/Desktop/Luna-Workspace-Min")
DEFAULT_OUTPUT_ROOT = DEFAULT_WORKSPACE_ROOT / "_eval_out" / "post_crossing_decision_roadmap_decision_v1_smoke_v0"


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Post Crossing Decision Roadmap Decision v1")
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument(
        "--crossing-decision-closure-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "crossing_decision_closure_v1_smoke_v0"),
    )
    parser.add_argument(
        "--crossing-decision-post-review-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "crossing_decision_post_dryrun_review_v1_smoke_v0"),
    )
    parser.add_argument(
        "--crossing-decision-dryrun-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "crossing_decision_dryrun_v1_smoke_v0"),
    )
    parser.add_argument(
        "--crossing-safety-governance-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "crossing_decision_safety_governance_policy_v1_smoke_v0"),
    )
    parser.add_argument(
        "--safety-constitution-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "luna_safety_constitution_policy_v1_smoke_v0"),
    )
    parser.add_argument(
        "--post-controlled-frame-roadmap-decision-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "post_controlled_frame_input_roadmap_decision_v1_smoke_v0"),
    )
    parser.add_argument(
        "--controlled-frame-input-closure-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "controlled_frame_input_closure_v1_smoke_v0"),
    )
    parser.add_argument(
        "--map-location-readonly-context-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "map_location_readonly_context_policy_v1_smoke_v0"),
    )
    parser.add_argument(
        "--vision-strengthening-closure-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "basic_navigation_loop_vision_strengthening_closure_v1_smoke_v0"),
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
        "--safety-task-arbitration-policy-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "safety_task_arbitration_policy_v1_smoke_v0"),
    )
    parser.add_argument(
        "--task-aware-visual-focus-policy-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "task_aware_visual_focus_policy_v1_smoke_v0"),
    )
    parser.add_argument(
        "--selective-tracking-adapter-policy-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "selective_tracking_adapter_policy_v1_smoke_v0"),
    )
    parser.add_argument(
        "--visual-ocr-map-task-feedback-dryrun-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "visual_ocr_map_task_feedback_dryrun_v1_smoke_v0"),
    )
    parser.add_argument(
        "--minimal-runtime-controlled-output-definition-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "minimal_runtime_integration_controlled_output_definition_v1_smoke_v0"),
    )
    parser.add_argument(
        "--minimal-runtime-text-only-output-post-review-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "minimal_runtime_integration_text_only_output_post_trial_review_v1_smoke_v0"),
    )
    parser.add_argument(
        "--voice-command-ownership-gate-policy-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "voice_command_ownership_gate_policy_v1_smoke_v0"),
    )
    parser.add_argument(
        "--voice-interruption-governance-dryrun-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "voice_interruption_governance_dryrun_v1_smoke_v0"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = run_post_crossing_decision_roadmap_decision_v1(
        crossing_decision_closure_root=args.crossing_decision_closure_root,
        crossing_decision_post_review_root=args.crossing_decision_post_review_root,
        crossing_decision_dryrun_root=args.crossing_decision_dryrun_root,
        crossing_safety_governance_root=args.crossing_safety_governance_root,
        safety_constitution_root=args.safety_constitution_root,
        post_controlled_frame_roadmap_decision_root=args.post_controlled_frame_roadmap_decision_root,
        controlled_frame_input_closure_root=args.controlled_frame_input_closure_root,
        map_location_readonly_context_root=args.map_location_readonly_context_root,
        vision_strengthening_closure_root=args.vision_strengthening_closure_root,
        minimal_runtime_integration_closure_root=args.minimal_runtime_integration_closure_root,
        ocr_final_closure_root=args.ocr_final_closure_root,
        safety_task_arbitration_policy_root=args.safety_task_arbitration_policy_root,
        task_aware_visual_focus_policy_root=args.task_aware_visual_focus_policy_root,
        selective_tracking_adapter_policy_root=args.selective_tracking_adapter_policy_root,
        visual_ocr_map_task_feedback_dryrun_root=args.visual_ocr_map_task_feedback_dryrun_root,
        minimal_runtime_controlled_output_definition_root=args.minimal_runtime_controlled_output_definition_root,
        minimal_runtime_text_only_output_post_review_root=args.minimal_runtime_text_only_output_post_review_root,
        voice_command_ownership_gate_policy_root=args.voice_command_ownership_gate_policy_root,
        voice_interruption_governance_dryrun_root=args.voice_interruption_governance_dryrun_root,
    )
    output_root = Path(args.output_root)
    for name in (
        "summary",
        "input_root_matrix",
        "post_crossing_decision_roadmap_decision",
        "current_crossing_decision_status_summary",
        "completed_capability_summary",
        "route_option_matrix",
        "priority_ranking",
        "recommended_next_phase_decision",
        "deferred_gate_taxonomy_register",
        "deferred_resilience_distributed_midplatform_register",
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
                "selected_route": result["route_option_matrix"]["selected_route_id"],
                "final_decision": result["summary"]["final_decision"],
                "recommended_next_phase": result["summary"]["recommended_next_phase"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
