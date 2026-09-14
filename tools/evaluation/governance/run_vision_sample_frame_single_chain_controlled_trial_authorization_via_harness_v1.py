#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Vision Sample Frame Controlled Trial Authorization Via Harness v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.vision_sample_frame_single_chain_controlled_trial_authorization_via_harness_v1 import (
    run_vision_sample_frame_single_chain_controlled_trial_authorization_via_harness_v1,
)

DEFAULT_OUTPUT_ROOT = (
    REPO_ROOT / "_eval_out" / "vision_sample_frame_single_chain_controlled_trial_authorization_via_harness_v1_smoke_v0"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("vision_sample_frame_authorization_via_harness_policy", "vision_sample_frame_authorization_via_harness_policy_v1.json"),
    ("harness_validation_closure_input_review", "harness_validation_closure_input_review_v1.json"),
    ("authorization_config_snapshot", "authorization_config_snapshot_v1.json"),
    ("authorization_validation_result", "authorization_validation_result_v1.json"),
    ("request_lifecycle_result", "request_lifecycle_result_v1.json"),
    ("grant_lifecycle_result", "grant_lifecycle_result_v1.json"),
    ("controlled_trial_execution_readiness_decision", "controlled_trial_execution_readiness_decision_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    p.add_argument("--controlled-trial-authorization-harness-validation-closure-root", required=True)
    p.add_argument("--vision-sample-frame-single-chain-plan-and-dryrun-root", default=None)
    p.add_argument("--vision-sample-frame-single-chain-controlled-trial-dryrun-and-review-root", default=None)
    args = p.parse_args()

    result = run_vision_sample_frame_single_chain_controlled_trial_authorization_via_harness_v1(
        controlled_trial_authorization_harness_validation_closure_root=args.controlled_trial_authorization_harness_validation_closure_root,
        vision_sample_frame_single_chain_plan_and_dryrun_root=args.vision_sample_frame_single_chain_plan_and_dryrun_root,
        vision_sample_frame_single_chain_controlled_trial_dryrun_and_review_root=(
            args.vision_sample_frame_single_chain_controlled_trial_dryrun_and_review_root
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
