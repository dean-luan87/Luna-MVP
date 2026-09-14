#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Midplatform Structure Cleanup Planning v1 (8-layer)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.midplatform_structure_cleanup_planning_v1 import (
    run_midplatform_structure_cleanup_planning_v1,
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_structure_cleanup_planning"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("midplatform_structure_cleanup_planning_policy", "midplatform_structure_cleanup_planning_policy_v1.json"),
    ("inventory_and_backbone_input_review", "inventory_and_backbone_input_review_v1.json"),
    ("midplatform_directory_role_decision", "midplatform_directory_role_decision_v1.json"),
    ("midplatform_8_layer_module_mapping", "midplatform_8_layer_module_mapping_v1.json"),
    ("midplatform_constitution_overlay_mapping", "midplatform_constitution_overlay_mapping_v1.json"),
    ("midplatform_input_output_layer_cleanup_plan", "midplatform_input_output_layer_cleanup_plan_v1.json"),
    ("midplatform_model_management_layer_cleanup_plan", "midplatform_model_management_layer_cleanup_plan_v1.json"),
    ("midplatform_health_management_layer_cleanup_plan", "midplatform_health_management_layer_cleanup_plan_v1.json"),
    ("midplatform_constitution_layer_cleanup_plan", "midplatform_constitution_layer_cleanup_plan_v1.json"),
    ("midplatform_task_layer_cleanup_plan", "midplatform_task_layer_cleanup_plan_v1.json"),
    ("midplatform_drive_layer_cleanup_plan", "midplatform_drive_layer_cleanup_plan_v1.json"),
    ("midplatform_local_memory_layer_cleanup_plan", "midplatform_local_memory_layer_cleanup_plan_v1.json"),
    ("midplatform_support_layer_cleanup_plan", "midplatform_support_layer_cleanup_plan_v1.json"),
    ("midplatform_runtime_bridge_plan", "midplatform_runtime_bridge_plan_v1.json"),
    ("midplatform_candidate_flow_contract", "midplatform_candidate_flow_contract_v1.json"),
    ("midplatform_minimal_backbone_dryrun_plan", "midplatform_minimal_backbone_dryrun_plan_v1.json"),
    ("midplatform_cleanup_route_matrix", "midplatform_cleanup_route_matrix_v1.json"),
    ("midplatform_gap_resolution_priority", "midplatform_gap_resolution_priority_v1.json"),
    ("midplatform_structure_cleanup_non_claims_register", "midplatform_structure_cleanup_non_claims_register_v1.json"),
    ("midplatform_structure_cleanup_planning_decision", "midplatform_structure_cleanup_planning_decision_v1.json"),
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
    args = p.parse_args()

    result = run_midplatform_structure_cleanup_planning_v1(
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
                "modules_mapped": s.get("modules_mapped"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if s.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
