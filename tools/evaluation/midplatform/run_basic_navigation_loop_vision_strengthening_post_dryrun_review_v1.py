#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Basic Navigation Loop Vision Strengthening Post-DryRun Review v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Dict

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.basic_navigation_loop_vision_strengthening_post_dryrun_review_v1 import (
    run_basic_navigation_loop_vision_strengthening_post_dryrun_review_v1,
)


DEFAULT_WORKSPACE_ROOT = Path("/Users/luanlei/Desktop/Luna-Workspace-Min")
DEFAULT_OUTPUT_ROOT = DEFAULT_WORKSPACE_ROOT / "_eval_out" / "basic_navigation_loop_vision_strengthening_post_dryrun_review_v1_smoke_v0"


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Basic Navigation Loop Vision Strengthening Post-DryRun Review v1")
    parser.add_argument("--workspace-root", default=str(DEFAULT_WORKSPACE_ROOT))
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument(
        "--dryrun-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "basic_navigation_loop_vision_strengthening_dryrun_v1_smoke_v0"),
    )
    parser.add_argument(
        "--visual-ocr-map-task-feedback-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "visual_ocr_map_task_feedback_dryrun_v1_smoke_v0"),
    )
    parser.add_argument(
        "--selective-tracking-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "selective_tracking_adapter_policy_v1_smoke_v0"),
    )
    parser.add_argument(
        "--world-observation-entity-feature-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "world_observation_and_entity_feature_policy_v1_smoke_v0"),
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
        "--basic-navigation-loop-stabilization-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "basic_navigation_guidance_loop_stabilization_test_v1_smoke_v0"),
    )
    parser.add_argument(
        "--safety-task-arbitration-policy-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "safety_task_arbitration_policy_v1_smoke_v0"),
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
        "--basic-navigation-guidance-loop-dryrun-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "basic_navigation_guidance_loop_dryrun_v1_smoke_v0"),
    )
    parser.add_argument(
        "--navigation-guidance-speech-adapter-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "navigation_guidance_speech_adapter_v1_smoke_v0"),
    )
    parser.add_argument(
        "--voice-interruption-governance-dryrun-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "voice_interruption_governance_dryrun_v1_smoke_v0"),
    )
    parser.add_argument(
        "--voice-command-ownership-gate-policy-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "voice_command_ownership_gate_policy_v1_smoke_v0"),
    )
    parser.add_argument(
        "--text-only-output-post-trial-review-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "minimal_runtime_integration_text_only_output_post_trial_review_v1_smoke_v0"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = run_basic_navigation_loop_vision_strengthening_post_dryrun_review_v1(
        dryrun_root=args.dryrun_root,
        visual_ocr_map_task_feedback_root=args.visual_ocr_map_task_feedback_root,
        selective_tracking_root=args.selective_tracking_root,
        world_observation_entity_feature_root=args.world_observation_entity_feature_root,
        task_aware_visual_focus_root=args.task_aware_visual_focus_root,
        midplatform_perception_orchestration_root=args.midplatform_perception_orchestration_root,
        basic_navigation_loop_stabilization_root=args.basic_navigation_loop_stabilization_root,
        safety_task_arbitration_policy_root=args.safety_task_arbitration_policy_root,
        minimal_runtime_integration_closure_root=args.minimal_runtime_integration_closure_root,
        ocr_final_closure_root=args.ocr_final_closure_root,
        basic_navigation_guidance_loop_dryrun_root=args.basic_navigation_guidance_loop_dryrun_root,
        navigation_guidance_speech_adapter_root=args.navigation_guidance_speech_adapter_root,
        voice_interruption_governance_dryrun_root=args.voice_interruption_governance_dryrun_root,
        voice_command_ownership_gate_policy_root=args.voice_command_ownership_gate_policy_root,
        text_only_output_post_trial_review_root=args.text_only_output_post_trial_review_root,
        workspace_root=args.workspace_root,
    )

    output_root = Path(args.output_root)
    output_root.mkdir(parents=True, exist_ok=True)

    for name in (
        "summary",
        "input_root_matrix",
        "dryrun_input_root_review",
        "scenario_coverage_review",
        "guidance_candidate_review",
        "safety_arbitration_bridge_review",
        "text_only_dry_output_review",
        "high_risk_scenario_review",
        "worldmodel_memory_library_boundary_review",
        "runtime_write_action_speech_boundary_review",
        "governance_debt_review",
        "closure_readiness_decision",
        "next_phase_recommendation",
        "no_runtime_boundary_report",
        "no_write_boundary_report",
    ):
        _write_json(output_root / f"{name}.json", result[name])

    print(
        json.dumps(
            {
                "output_root": str(output_root),
                "review_scope": result["summary"]["review_scope"],
                "final_decision": result["summary"]["final_decision"],
                "recommended_next_phase": result["summary"]["recommended_next_phase"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
