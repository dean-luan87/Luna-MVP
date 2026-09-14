#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Single-Chain Trial Validation Harness Extraction Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.single_chain_trial_validation_harness_extraction_planning_v1 import (
    run_single_chain_trial_validation_harness_extraction_planning_v1,
)

DEFAULT_OUTPUT_ROOT = REPO_ROOT / "_eval_out" / "single_chain_trial_validation_harness_extraction_planning_v1_smoke_v0"

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("single_chain_trial_validation_harness_extraction_policy", "single_chain_trial_validation_harness_extraction_policy_v1.json"),
    ("reusable_single_chain_trial_validation_contract", "reusable_single_chain_trial_validation_contract_v1.json"),
    ("chain_config_schema_planning", "chain_config_schema_planning_v1.json"),
    ("reusable_gate_library_planning", "reusable_gate_library_planning_v1.json"),
    ("reusable_stop_condition_library_planning", "reusable_stop_condition_library_planning_v1.json"),
    ("reusable_flow_contract_planning", "reusable_flow_contract_planning_v1.json"),
    ("reusable_candidate_output_contract_planning", "reusable_candidate_output_contract_planning_v1.json"),
    ("future_chain_adoption_matrix", "future_chain_adoption_matrix_v1.json"),
    ("anti_recursion_rules_for_single_chain_trials", "anti_recursion_rules_for_single_chain_trials_v1.json"),
    ("single_chain_harness_extraction_readiness_decision", "single_chain_harness_extraction_readiness_decision_v1.json"),
)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    p.add_argument("--vision-ocr-navigation-task-limited-runtime-trial-post-dryrun-review-root", required=True)
    p.add_argument("--vision-ocr-navigation-task-limited-runtime-trial-dryrun-root", default=None)
    p.add_argument("--vision-ocr-navigation-task-controlled-trial-plan-and-dryrun-root", default=None)
    args = p.parse_args()

    result = run_single_chain_trial_validation_harness_extraction_planning_v1(
        vision_ocr_navigation_task_limited_runtime_trial_post_dryrun_review_root=args.vision_ocr_navigation_task_limited_runtime_trial_post_dryrun_review_root,
        vision_ocr_navigation_task_limited_runtime_trial_dryrun_root=args.vision_ocr_navigation_task_limited_runtime_trial_dryrun_root,
        vision_ocr_navigation_task_controlled_trial_plan_and_dryrun_root=args.vision_ocr_navigation_task_controlled_trial_plan_and_dryrun_root,
    )
    out = Path(args.output_root)
    for key, fname in OUTPUT_FILES:
        _write_json(out / fname, result[key])
    s = result["summary"]
    print(json.dumps({"phase": s.get("phase"), "boundary_ok": s.get("boundary_ok"), "final_decision": s.get("final_decision")}, ensure_ascii=False))
    return 0 if s.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
