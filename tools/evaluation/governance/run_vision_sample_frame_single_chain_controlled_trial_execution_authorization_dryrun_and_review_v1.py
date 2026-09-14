#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Vision Sample Frame Controlled Trial Execution Authorization DryRun+Review v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.vision_sample_frame_single_chain_controlled_trial_execution_authorization_dryrun_and_review_v1 import (
    run_vision_sample_frame_single_chain_controlled_trial_execution_authorization_dryrun_and_review_v1,
)

DEFAULT_OUTPUT_ROOT = (
    REPO_ROOT
    / "_eval_out"
    / "vision_sample_frame_single_chain_controlled_trial_execution_authorization_dryrun_and_review_v1_smoke_v0"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("execution_authorization_dryrun_and_review_policy", "execution_authorization_dryrun_and_review_policy_v1.json"),
    ("authorization_planning_input_review", "authorization_planning_input_review_v1.json"),
    ("authorization_scope_consumption_result", "authorization_scope_consumption_result_v1.json"),
    ("execution_allowlist_blocklist_review", "execution_allowlist_blocklist_review_v1.json"),
    ("pre_execution_gate_consumption_result", "pre_execution_gate_consumption_result_v1.json"),
    ("execution_window_dryrun_result", "execution_window_dryrun_result_v1.json"),
    ("abort_condition_consumption_result", "abort_condition_consumption_result_v1.json"),
    ("output_contract_review", "output_contract_review_v1.json"),
    ("logging_policy_review", "logging_policy_review_v1.json"),
    ("post_execution_review_requirement_result", "post_execution_review_requirement_result_v1.json"),
    ("authorization_non_release_review", "authorization_non_release_review_v1.json"),
    ("trial_execution_readiness_decision", "trial_execution_readiness_decision_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    p.add_argument(
        "--vision-sample-frame-single-chain-controlled-trial-execution-authorization-planning-root",
        required=True,
    )
    args = p.parse_args()

    result = run_vision_sample_frame_single_chain_controlled_trial_execution_authorization_dryrun_and_review_v1(
        vision_sample_frame_single_chain_controlled_trial_execution_authorization_planning_root=(
            args.vision_sample_frame_single_chain_controlled_trial_execution_authorization_planning_root
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
            },
            ensure_ascii=False,
        )
    )
    return 0 if s.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
