#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Task-Aware Visual Focus Policy v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Dict

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.vision.task_aware_visual_focus_policy_v1 import (
    run_task_aware_visual_focus_policy_v1,
)


DEFAULT_WORKSPACE_ROOT = Path("/Users/luanlei/Desktop/Luna-Workspace-Min")
DEFAULT_OUTPUT_ROOT = DEFAULT_WORKSPACE_ROOT / "_eval_out" / "task_aware_visual_focus_policy_v1_smoke_v0"


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Task-Aware Visual Focus Policy v1")
    parser.add_argument("--workspace-root", default=str(DEFAULT_WORKSPACE_ROOT))
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument(
        "--midplatform-perception-orchestration-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "midplatform_perception_orchestration_policy_v1_smoke_v0"),
    )
    parser.add_argument(
        "--return-to-vision-planning-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "return_to_vision_mainline_planning_v1_smoke_v0"),
    )
    parser.add_argument(
        "--preplan-input-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "return_to_vision_mainline_preplan_v1"),
    )
    parser.add_argument(
        "--ocr-final-closure-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "ocr_mainline_final_closure_v1_smoke_v0"),
    )
    parser.add_argument(
        "--minimal-runtime-integration-closure-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "minimal_runtime_integration_closure_v1_smoke_v0"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = run_task_aware_visual_focus_policy_v1(
        midplatform_perception_orchestration_root=args.midplatform_perception_orchestration_root,
        return_to_vision_planning_root=args.return_to_vision_planning_root,
        preplan_input_root=args.preplan_input_root,
        ocr_final_closure_root=args.ocr_final_closure_root,
        minimal_runtime_integration_closure_root=args.minimal_runtime_integration_closure_root,
        workspace_root=args.workspace_root,
    )

    output_root = Path(args.output_root)
    output_root.mkdir(parents=True, exist_ok=True)

    for name in (
        "summary",
        "input_root_matrix",
        "scene_sketch_candidate_schema",
        "visual_focus_plan_schema",
        "visual_focus_slot_schema",
        "view_quality_candidate_schema",
        "active_view_adjustment_candidate_schema",
        "visual_observation_lifecycle_policy",
        "focus_to_ocr_activation_policy",
        "focus_to_tracking_request_policy",
        "visual_focus_feedback_policy",
        "deferred_worldmodel_memory_library_boundary",
        "task_aware_visual_focus_scenario_matrix",
        "visual_focus_boundary_matrix",
        "governance_debt_register",
        "next_phase_recommendation",
        "no_runtime_boundary_report",
        "no_write_boundary_report",
    ):
        _write_json(output_root / f"{name}.json", result[name])

    print(
        json.dumps(
            {
                "output_root": str(output_root),
                "policy_scope": result["summary"]["policy_scope"],
                "final_decision": result["summary"]["final_decision"],
                "recommended_next_phase": result["summary"]["recommended_next_phase"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
