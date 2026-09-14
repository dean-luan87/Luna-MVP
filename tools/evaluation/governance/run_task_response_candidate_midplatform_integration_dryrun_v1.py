#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Task Response Candidate Midplatform Integration DryRun v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.task_response_candidate_midplatform_integration_dryrun_v1 import (
    run_task_response_candidate_midplatform_integration_dryrun_v1,
)

WS = "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out"
DEFAULT_OUTPUT = f"{WS}/task_response_candidate_midplatform_integration_dryrun"

DEFAULT_INPUTS = {
    "task_response_candidate_midplatform_integration_planning_root": (
        f"{WS}/task_response_candidate_midplatform_integration_planning"
    ),
    "midplatform_minimal_backbone_post_dryrun_review_root": (
        f"{WS}/midplatform_minimal_backbone_post_dryrun_review"
    ),
    "midplatform_minimal_backbone_dryrun_root": f"{WS}/midplatform_minimal_backbone_dryrun",
    "vision_sample_frame_single_chain_controlled_trial_post_execution_review_root": (
        f"{WS}/vision_sample_frame_single_chain_controlled_trial_post_execution_review"
    ),
    "ocr_mock_result_single_chain_trial_via_validation_factory_root": (
        f"{WS}/ocr_mock_result_single_chain_trial_via_validation_factory"
    ),
    "navigation_guidance_candidate_single_chain_trial_via_validation_factory_root": (
        f"{WS}/navigation_guidance_candidate_single_chain_trial_via_validation_factory"
    ),
}


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    for key, default in DEFAULT_INPUTS.items():
        p.add_argument(f"--{key.replace('_', '-')}", default=default)
    args = p.parse_args()

    result = run_task_response_candidate_midplatform_integration_dryrun_v1(
        task_response_candidate_midplatform_integration_planning_root=(
            args.task_response_candidate_midplatform_integration_planning_root
        ),
        midplatform_minimal_backbone_post_dryrun_review_root=(
            args.midplatform_minimal_backbone_post_dryrun_review_root
        ),
        midplatform_minimal_backbone_dryrun_root=args.midplatform_minimal_backbone_dryrun_root,
        vision_sample_frame_single_chain_controlled_trial_post_execution_review_root=(
            args.vision_sample_frame_single_chain_controlled_trial_post_execution_review_root
        ),
        ocr_mock_result_single_chain_trial_via_validation_factory_root=(
            args.ocr_mock_result_single_chain_trial_via_validation_factory_root
        ),
        navigation_guidance_candidate_single_chain_trial_via_validation_factory_root=(
            args.navigation_guidance_candidate_single_chain_trial_via_validation_factory_root
        ),
        output_root=args.output_root,
    )

    out_root = Path(result["output_root"])
    for filename, payload in result["artifacts"].items():
        _write_json(out_root / filename, payload)

    sm = result["artifacts"]["summary.json"]
    print(
        json.dumps(
            {
                "output_root": str(out_root),
                "boundary_ok": sm.get("boundary_ok"),
                "final_decision": sm.get("final_decision"),
                "flows_all_pass": sm.get("flows_all_pass"),
                "candidates": sm.get("task_response_candidates_generated"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
