#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Vision Sample Frame Controlled Trial Execution Authorization Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.vision_sample_frame_single_chain_controlled_trial_execution_authorization_planning_v1 import (
    run_vision_sample_frame_single_chain_controlled_trial_execution_authorization_planning_v1,
)

DEFAULT_OUTPUT_ROOT = (
    REPO_ROOT / "_eval_out" / "vision_sample_frame_single_chain_controlled_trial_execution_authorization_planning_v1_smoke_v0"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("execution_authorization_planning_policy", "execution_authorization_planning_policy_v1.json"),
    ("dryrun_and_review_input_review", "dryrun_and_review_input_review_v1.json"),
    ("controlled_trial_execution_authorization_scope", "controlled_trial_execution_authorization_scope_v1.json"),
    ("controlled_trial_execution_allowlist", "controlled_trial_execution_allowlist_v1.json"),
    ("controlled_trial_execution_blocklist", "controlled_trial_execution_blocklist_v1.json"),
    ("controlled_trial_pre_execution_gate_matrix", "controlled_trial_pre_execution_gate_matrix_v1.json"),
    ("controlled_trial_execution_window_authorization_plan", "controlled_trial_execution_window_authorization_plan_v1.json"),
    ("controlled_trial_abort_condition_matrix", "controlled_trial_abort_condition_matrix_v1.json"),
    ("controlled_trial_output_contract", "controlled_trial_output_contract_v1.json"),
    ("controlled_trial_execution_logging_policy", "controlled_trial_execution_logging_policy_v1.json"),
    ("controlled_trial_post_execution_review_requirement", "controlled_trial_post_execution_review_requirement_v1.json"),
    ("execution_authorization_non_claims_register", "execution_authorization_non_claims_register_v1.json"),
    ("execution_authorization_planning_readiness_decision", "execution_authorization_planning_readiness_decision_v1.json"),
)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    p.add_argument("--vision-sample-frame-single-chain-controlled-trial-dryrun-and-review-root", required=True)
    args = p.parse_args()

    result = run_vision_sample_frame_single_chain_controlled_trial_execution_authorization_planning_v1(
        vision_sample_frame_single_chain_controlled_trial_dryrun_and_review_root=(
            args.vision_sample_frame_single_chain_controlled_trial_dryrun_and_review_root
        ),
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
