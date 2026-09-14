#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Midplatform Module Gap and Roadmap Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.midplatform_module_gap_and_roadmap_planning_v1 import (
    run_midplatform_module_gap_and_roadmap_planning_v1,
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_module_gap_and_roadmap_planning"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("midplatform_module_gap_roadmap_policy", "midplatform_module_gap_roadmap_policy_v1.json"),
    ("midplatform_input_review", "midplatform_input_review_v1.json"),
    ("eight_layer_module_completeness_matrix", "eight_layer_module_completeness_matrix_v1.json"),
    ("existing_module_reuse_matrix", "existing_module_reuse_matrix_v1.json"),
    ("must_fill_module_gap_register", "must_fill_module_gap_register_v1.json"),
    ("optional_future_module_register", "optional_future_module_register_v1.json"),
    ("module_addition_priority_matrix", "module_addition_priority_matrix_v1.json"),
    ("midplatform_minimal_stabilization_roadmap", "midplatform_minimal_stabilization_roadmap_v1.json"),
    ("model_layer_optimization_handoff_plan", "model_layer_optimization_handoff_plan_v1.json"),
    ("task_response_candidate_defer_or_resume_decision", "task_response_candidate_defer_or_resume_decision_v1.json"),
    ("memory_library_map_defer_policy", "memory_library_map_defer_policy_v1.json"),
    ("midplatform_module_gap_non_claims_register", "midplatform_module_gap_non_claims_register_v1.json"),
    ("midplatform_module_gap_roadmap_decision", "midplatform_module_gap_roadmap_decision_v1.json"),
)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT_ROOT)
    p.add_argument("--midplatform-current-state-inventory-root", required=True)
    p.add_argument("--midplatform-backbone-definition-alignment-root", required=True)
    p.add_argument("--luna-validation-factory-consolidation-root", required=True)
    p.add_argument(
        "--vision-sample-frame-single-chain-controlled-trial-post-execution-review-root",
        required=True,
    )
    p.add_argument("--ocr-mock-result-single-chain-trial-via-validation-factory-root", required=True)
    p.add_argument(
        "--navigation-guidance-candidate-single-chain-trial-via-validation-factory-root",
        required=True,
    )
    p.add_argument("--midplatform-structure-cleanup-planning-root", default=None)
    args = p.parse_args()

    result = run_midplatform_module_gap_and_roadmap_planning_v1(
        midplatform_current_state_inventory_root=args.midplatform_current_state_inventory_root,
        midplatform_backbone_definition_alignment_root=args.midplatform_backbone_definition_alignment_root,
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
        midplatform_structure_cleanup_planning_root=args.midplatform_structure_cleanup_planning_root,
        output_root=args.output_root,
    )
    out = Path(args.output_root)
    for key, fname in OUTPUT_FILES:
        _write_json(out / fname, result[key])
    s = result["summary"]
    print(
        json.dumps(
            {
                "phase": s.get("phase"),
                "boundary_ok": s.get("boundary_ok"),
                "final_decision": s.get("final_decision"),
                "recommended_next_phase": s.get("recommended_next_phase"),
                "p0_gap_count": s.get("p0_gap_count"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if s.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
