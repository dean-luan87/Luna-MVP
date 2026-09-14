#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Vision Sample Frame Single-Chain Controlled Trial Post-Execution Review v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.vision_sample_frame_single_chain_controlled_trial_post_execution_review_v1 import (
    run_vision_sample_frame_single_chain_controlled_trial_post_execution_review_v1,
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "vision_sample_frame_single_chain_controlled_trial_post_execution_review"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("post_execution_review_policy", "post_execution_review_policy_v1.json"),
    ("controlled_trial_execution_input_review", "controlled_trial_execution_input_review_v1.json"),
    ("execution_result_completeness_review", "execution_result_completeness_review_v1.json"),
    ("visual_observation_candidate_contract_review", "visual_observation_candidate_contract_review_v1.json"),
    ("no_runtime_boundary_post_execution_review", "no_runtime_boundary_post_execution_review_v1.json"),
    ("abort_monitor_post_execution_review", "abort_monitor_post_execution_review_v1.json"),
    ("logging_path_compliance_review", "logging_path_compliance_review_v1.json"),
    ("side_effect_absence_review", "side_effect_absence_review_v1.json"),
    ("controlled_trial_closure_decision", "controlled_trial_closure_decision_v1.json"),
    ("next_chain_adoption_readiness", "next_chain_adoption_readiness_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT_ROOT)
    p.add_argument("--vision-sample-frame-single-chain-controlled-trial-execution-root", required=True)
    args = p.parse_args()

    result = run_vision_sample_frame_single_chain_controlled_trial_post_execution_review_v1(
        vision_sample_frame_single_chain_controlled_trial_execution_root=(
            args.vision_sample_frame_single_chain_controlled_trial_execution_root
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
