#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Midplatform Current State Inventory v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.midplatform_current_state_inventory_v1 import (
    run_midplatform_current_state_inventory_v1,
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_current_state_inventory"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("midplatform_inventory_policy", "midplatform_inventory_policy_v1.json"),
    ("validation_factory_and_candidate_chain_input_review", "validation_factory_and_candidate_chain_input_review_v1.json"),
    ("midplatform_directory_structure_inventory", "midplatform_directory_structure_inventory_v1.json"),
    ("midplatform_parallel_directory_review", "midplatform_parallel_directory_review_v1.json"),
    ("midplatform_module_inventory", "midplatform_module_inventory_v1.json"),
    ("midplatform_documentation_inventory", "midplatform_documentation_inventory_v1.json"),
    ("midplatform_runner_verifier_inventory", "midplatform_runner_verifier_inventory_v1.json"),
    ("midplatform_candidate_handoff_inventory", "midplatform_candidate_handoff_inventory_v1.json"),
    ("midplatform_task_state_related_inventory", "midplatform_task_state_related_inventory_v1.json"),
    ("midplatform_runtime_boundary_inventory", "midplatform_runtime_boundary_inventory_v1.json"),
    ("midplatform_stub_placeholder_register", "midplatform_stub_placeholder_register_v1.json"),
    ("midplatform_gap_and_duplication_register", "midplatform_gap_and_duplication_register_v1.json"),
    ("midplatform_next_work_recommendation", "midplatform_next_work_recommendation_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT_ROOT)
    p.add_argument("--luna-core-root", default=str(REPO_ROOT))
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
    p.add_argument("--post-migration-engineering-state-sync-root", required=True)
    args = p.parse_args()

    result = run_midplatform_current_state_inventory_v1(
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
        post_migration_engineering_state_sync_root=args.post_migration_engineering_state_sync_root,
        luna_core_root=args.luna_core_root,
        output_root=args.output_root,
    )
    out = Path(args.output_root)
    for key, fname in OUTPUT_FILES:
        _write_json(out / fname, result[key])
    (out / "midplatform_inventory_summary_v1.md").write_text(
        result["midplatform_inventory_summary_v1_md"], encoding="utf-8"
    )
    s = result["summary"]
    print(
        json.dumps(
            {
                "phase": s.get("phase"),
                "boundary_ok": s.get("boundary_ok"),
                "final_decision": s.get("final_decision"),
                "recommended_next_phase": s.get("recommended_next_phase"),
                "midplatform_py": s.get("midplatform_py_count"),
                "mid_platform_py": s.get("mid_platform_py_count"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if s.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
