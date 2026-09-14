#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Midplatform Minimal Backbone DryRun v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.midplatform_minimal_backbone_dryrun_v1 import (
    run_midplatform_minimal_backbone_dryrun_v1,
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_minimal_backbone_dryrun"
)

DEFAULT_INPUTS = {
    "midplatform_current_state_inventory_root": (
        "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_current_state_inventory"
    ),
    "midplatform_backbone_definition_alignment_root": (
        "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_backbone_definition_alignment"
    ),
    "midplatform_structure_cleanup_planning_root": (
        "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_structure_cleanup_planning"
    ),
    "midplatform_module_gap_and_roadmap_planning_root": (
        "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_module_gap_and_roadmap_planning"
    ),
    "luna_validation_factory_consolidation_root": (
        "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/luna_validation_factory_consolidation"
    ),
    "vision_sample_frame_single_chain_controlled_trial_post_execution_review_root": (
        "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
        "vision_sample_frame_single_chain_controlled_trial_post_execution_review"
    ),
    "ocr_mock_result_single_chain_trial_via_validation_factory_root": (
        "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
        "ocr_mock_result_single_chain_trial_via_validation_factory"
    ),
    "navigation_guidance_candidate_single_chain_trial_via_validation_factory_root": (
        "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
        "navigation_guidance_candidate_single_chain_trial_via_validation_factory"
    ),
}


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT_ROOT)
    for key, default in DEFAULT_INPUTS.items():
        p.add_argument(f"--{key.replace('_', '-')}", default=default)
    args = p.parse_args()

    result = run_midplatform_minimal_backbone_dryrun_v1(
        midplatform_current_state_inventory_root=args.midplatform_current_state_inventory_root,
        midplatform_backbone_definition_alignment_root=args.midplatform_backbone_definition_alignment_root,
        midplatform_structure_cleanup_planning_root=args.midplatform_structure_cleanup_planning_root,
        midplatform_module_gap_and_roadmap_planning_root=args.midplatform_module_gap_and_roadmap_planning_root,
        luna_validation_factory_consolidation_root=args.luna_validation_factory_consolidation_root,
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

    print(
        json.dumps(
            {
                "output_root": str(out_root),
                "dryrun_ok": result["dryrun_ok"],
                "final_decision": result["artifacts"]["summary.json"].get("final_decision"),
                "flows_all_pass": result["artifacts"]["summary.json"].get("flows_all_pass"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["artifacts"]["summary.json"].get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
