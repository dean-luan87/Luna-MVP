#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Vision Sample Frame Controlled Trial Execution Authorization Request Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.vision_sample_frame_single_chain_controlled_trial_execution_authorization_request_planning_v1 import (
    run_vision_sample_frame_single_chain_controlled_trial_execution_authorization_request_planning_v1,
)

DEFAULT_OUTPUT_ROOT = (
    REPO_ROOT
    / "_eval_out"
    / "vision_sample_frame_single_chain_controlled_trial_execution_authorization_request_planning_v1_smoke_v0"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("execution_authorization_request_planning_policy", "execution_authorization_request_planning_policy_v1.json"),
    ("authorization_dryrun_and_review_input_review", "authorization_dryrun_and_review_input_review_v1.json"),
    ("authorization_request_identity_schema", "authorization_request_identity_schema_v1.json"),
    ("authorization_request_scope_binding", "authorization_request_scope_binding_v1.json"),
    ("authorization_request_input_binding", "authorization_request_input_binding_v1.json"),
    ("authorization_request_execution_window_binding", "authorization_request_execution_window_binding_v1.json"),
    ("authorization_request_gate_binding", "authorization_request_gate_binding_v1.json"),
    ("authorization_request_abort_binding", "authorization_request_abort_binding_v1.json"),
    ("authorization_request_output_contract_binding", "authorization_request_output_contract_binding_v1.json"),
    ("authorization_request_post_execution_review_binding", "authorization_request_post_execution_review_binding_v1.json"),
    ("authorization_request_non_grant_statement", "authorization_request_non_grant_statement_v1.json"),
    ("authorization_request_lifecycle_plan", "authorization_request_lifecycle_plan_v1.json"),
    ("authorization_request_non_claims_register", "authorization_request_non_claims_register_v1.json"),
    ("authorization_request_planning_readiness_decision", "authorization_request_planning_readiness_decision_v1.json"),
)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    p.add_argument(
        "--vision-sample-frame-single-chain-controlled-trial-execution-authorization-dryrun-and-review-root",
        required=True,
    )
    args = p.parse_args()

    result = run_vision_sample_frame_single_chain_controlled_trial_execution_authorization_request_planning_v1(
        vision_sample_frame_single_chain_controlled_trial_execution_authorization_dryrun_and_review_root=(
            args.vision_sample_frame_single_chain_controlled_trial_execution_authorization_dryrun_and_review_root
        ),
        planning_output_root=args.output_root,
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
