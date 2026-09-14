#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Single-Chain Trial Validation Harness Validation Closure v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.single_chain_trial_validation_harness_validation_closure_v1 import (
    run_single_chain_trial_validation_harness_validation_closure_v1,
)

DEFAULT_OUTPUT_ROOT = REPO_ROOT / "_eval_out" / "single_chain_trial_validation_harness_validation_closure_v1_smoke_v0"

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("single_chain_harness_validation_closure_policy", "single_chain_harness_validation_closure_policy_v1.json"),
    ("harness_contract_consumption_review", "harness_contract_consumption_review_v1.json"),
    ("harness_module_presence_review", "harness_module_presence_review_v1.json"),
    ("vision_first_consumer_review", "vision_first_consumer_review_v1.json"),
    ("reusable_chain_config_schema_closure", "reusable_chain_config_schema_closure_v1.json"),
    ("anti_recursion_rule_closure", "anti_recursion_rule_closure_v1.json"),
    ("future_single_chain_usage_guide", "future_single_chain_usage_guide_v1.json"),
    ("single_chain_harness_validation_closure_decision", "single_chain_harness_validation_closure_decision_v1.json"),
)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    p.add_argument("--single-chain-trial-validation-harness-extraction-planning-root", required=True)
    p.add_argument("--vision-sample-frame-single-chain-plan-and-dryrun-root", required=True)
    p.add_argument("--repo-root", default=str(REPO_ROOT))
    args = p.parse_args()

    result = run_single_chain_trial_validation_harness_validation_closure_v1(
        single_chain_trial_validation_harness_extraction_planning_root=args.single_chain_trial_validation_harness_extraction_planning_root,
        vision_sample_frame_single_chain_plan_and_dryrun_root=args.vision_sample_frame_single_chain_plan_and_dryrun_root,
        repo_root=args.repo_root,
        closure_output_root=args.output_root,
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
            },
            ensure_ascii=False,
        )
    )
    return 0 if s.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
