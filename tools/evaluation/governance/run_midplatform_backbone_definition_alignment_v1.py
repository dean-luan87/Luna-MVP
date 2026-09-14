#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Midplatform Backbone Definition Alignment v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.midplatform_backbone_definition_alignment_v1 import (
    run_midplatform_backbone_definition_alignment_v1,
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_backbone_definition_alignment"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("midplatform_backbone_definition_policy", "midplatform_backbone_definition_policy_v1.json"),
    ("midplatform_inventory_input_review", "midplatform_inventory_input_review_v1.json"),
    ("luna_midplatform_8_layer_architecture", "luna_midplatform_8_layer_architecture_v1.json"),
    ("midplatform_layer_responsibility_matrix", "midplatform_layer_responsibility_matrix_v1.json"),
    ("midplatform_layer_authority_matrix", "midplatform_layer_authority_matrix_v1.json"),
    ("midplatform_old_new_layer_mapping", "midplatform_old_new_layer_mapping_v1.json"),
    ("input_output_layer_contract", "input_output_layer_contract_v1.json"),
    ("model_management_layer_contract", "model_management_layer_contract_v1.json"),
    ("health_management_layer_contract", "health_management_layer_contract_v1.json"),
    ("constitution_layer_contract", "constitution_layer_contract_v1.json"),
    ("task_layer_contract", "task_layer_contract_v1.json"),
    ("drive_layer_contract", "drive_layer_contract_v1.json"),
    ("local_memory_layer_contract", "local_memory_layer_contract_v1.json"),
    ("support_layer_contract", "support_layer_contract_v1.json"),
    ("active_passive_task_relation", "active_passive_task_relation_v1.json"),
    ("survival_drive_candidate_contract", "survival_drive_candidate_contract_v1.json"),
    ("midplatform_cross_layer_flow_examples", "midplatform_cross_layer_flow_examples_v1.json"),
    ("midplatform_missing_concern_register", "midplatform_missing_concern_register_v1.json"),
    ("midplatform_backbone_definition_non_claims_register", "midplatform_backbone_definition_non_claims_register_v1.json"),
    ("midplatform_backbone_definition_alignment_decision", "midplatform_backbone_definition_alignment_decision_v1.json"),
)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT_ROOT)
    p.add_argument("--midplatform-current-state-inventory-root", required=True)
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

    result = run_midplatform_backbone_definition_alignment_v1(
        midplatform_current_state_inventory_root=args.midplatform_current_state_inventory_root,
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
                "layer_count": s.get("layer_count"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if s.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
