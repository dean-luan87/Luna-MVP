#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Controlled Trial Authorization Harness Extraction Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.controlled_trial_authorization_harness_extraction_planning_v1 import (
    run_controlled_trial_authorization_harness_extraction_planning_v1,
)

DEFAULT_OUTPUT_ROOT = REPO_ROOT / "_eval_out" / "controlled_trial_authorization_harness_extraction_planning_v1_smoke_v0"

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("controlled_trial_authorization_harness_extraction_policy", "controlled_trial_authorization_harness_extraction_policy_v1.json"),
    ("reusable_authorization_lifecycle_contract", "reusable_authorization_lifecycle_contract_v1.json"),
    ("authorization_config_schema_planning", "authorization_config_schema_planning_v1.json"),
    ("authorization_scope_contract_planning", "authorization_scope_contract_planning_v1.json"),
    ("allowlist_blocklist_contract_planning", "allowlist_blocklist_contract_planning_v1.json"),
    ("pre_execution_gate_contract_planning", "pre_execution_gate_contract_planning_v1.json"),
    ("execution_window_contract_planning", "execution_window_contract_planning_v1.json"),
    ("abort_condition_contract_planning", "abort_condition_contract_planning_v1.json"),
    ("output_contract_binding_planning", "output_contract_binding_planning_v1.json"),
    ("request_lifecycle_contract_planning", "request_lifecycle_contract_planning_v1.json"),
    ("grant_lifecycle_contract_planning", "grant_lifecycle_contract_planning_v1.json"),
    ("post_execution_review_contract_planning", "post_execution_review_contract_planning_v1.json"),
    ("future_trial_authorization_adoption_matrix", "future_trial_authorization_adoption_matrix_v1.json"),
    ("anti_recursion_rules_for_authorization_trials", "anti_recursion_rules_for_authorization_trials_v1.json"),
    ("controlled_trial_authorization_harness_readiness_decision", "controlled_trial_authorization_harness_readiness_decision_v1.json"),
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
    p.add_argument(
        "--vision-sample-frame-single-chain-controlled-trial-execution-authorization-dryrun-and-review-root",
        required=True,
    )
    p.add_argument(
        "--vision-sample-frame-single-chain-controlled-trial-execution-authorization-request-planning-root",
        required=True,
    )
    args = p.parse_args()

    result = run_controlled_trial_authorization_harness_extraction_planning_v1(
        vision_sample_frame_single_chain_controlled_trial_execution_authorization_planning_root=(
            args.vision_sample_frame_single_chain_controlled_trial_execution_authorization_planning_root
        ),
        vision_sample_frame_single_chain_controlled_trial_execution_authorization_dryrun_and_review_root=(
            args.vision_sample_frame_single_chain_controlled_trial_execution_authorization_dryrun_and_review_root
        ),
        vision_sample_frame_single_chain_controlled_trial_execution_authorization_request_planning_root=(
            args.vision_sample_frame_single_chain_controlled_trial_execution_authorization_request_planning_root
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
