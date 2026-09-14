#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Vision Sample Frame Single-Chain Controlled Trial Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.vision_sample_frame_single_chain_controlled_trial_planning_v1 import (
    run_vision_sample_frame_single_chain_controlled_trial_planning_v1,
)

DEFAULT_OUTPUT_ROOT = REPO_ROOT / "_eval_out" / "vision_sample_frame_single_chain_controlled_trial_planning_v1_smoke_v0"

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("vision_sample_frame_controlled_trial_planning_policy", "vision_sample_frame_controlled_trial_planning_policy_v1.json"),
    ("harness_validation_input_review", "harness_validation_input_review_v1.json"),
    ("vision_plan_and_dryrun_input_review", "vision_plan_and_dryrun_input_review_v1.json"),
    ("controlled_trial_scope", "controlled_trial_scope_v1.json"),
    ("controlled_trial_input_allowlist", "controlled_trial_input_allowlist_v1.json"),
    ("controlled_trial_execution_window_policy", "controlled_trial_execution_window_policy_v1.json"),
    ("controlled_trial_gate_matrix", "controlled_trial_gate_matrix_v1.json"),
    ("controlled_trial_stop_condition_matrix", "controlled_trial_stop_condition_matrix_v1.json"),
    ("controlled_trial_success_criteria", "controlled_trial_success_criteria_v1.json"),
    ("controlled_trial_logging_policy", "controlled_trial_logging_policy_v1.json"),
    ("controlled_trial_abort_and_rollback_policy", "controlled_trial_abort_and_rollback_policy_v1.json"),
    ("controlled_trial_authorization_boundary", "controlled_trial_authorization_boundary_v1.json"),
    ("controlled_trial_non_claims_register", "controlled_trial_non_claims_register_v1.json"),
    ("controlled_trial_planning_readiness_decision", "controlled_trial_planning_readiness_decision_v1.json"),
)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    p.add_argument("--single-chain-trial-validation-harness-validation-closure-root", required=True)
    p.add_argument("--vision-sample-frame-single-chain-plan-and-dryrun-root", required=True)
    args = p.parse_args()

    result = run_vision_sample_frame_single_chain_controlled_trial_planning_v1(
        single_chain_trial_validation_harness_validation_closure_root=args.single_chain_trial_validation_harness_validation_closure_root,
        vision_sample_frame_single_chain_plan_and_dryrun_root=args.vision_sample_frame_single_chain_plan_and_dryrun_root,
        planning_output_root=args.output_root,
    )
    out = Path(args.output_root)
    for key, fname in OUTPUT_FILES:
        _write_json(out / fname, result[key])
    s = result["summary"]
    print(json.dumps({"phase": s.get("phase"), "boundary_ok": s.get("boundary_ok"), "final_decision": s.get("final_decision"), "recommended_next_phase": s.get("recommended_next_phase")}, ensure_ascii=False))
    return 0 if s.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
