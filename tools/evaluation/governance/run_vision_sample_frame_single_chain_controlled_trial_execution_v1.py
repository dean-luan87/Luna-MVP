#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Vision Sample Frame Single-Chain Controlled Trial Execution v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.vision_sample_frame_single_chain_controlled_trial_execution_v1 import (
    run_vision_sample_frame_single_chain_controlled_trial_execution_v1,
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "vision_sample_frame_single_chain_controlled_trial_execution"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("vision_sample_frame_controlled_trial_execution_policy", "vision_sample_frame_controlled_trial_execution_policy_v1.json"),
    ("validation_factory_input_review", "validation_factory_input_review_v1.json"),
    ("authorization_via_harness_input_review", "authorization_via_harness_input_review_v1.json"),
    ("controlled_trial_execution_input_manifest", "controlled_trial_execution_input_manifest_v1.json"),
    ("controlled_trial_execution_trace", "controlled_trial_execution_trace_v1.json"),
    ("visual_observation_candidate_result", "visual_observation_candidate_result_v1.json"),
    ("candidate_output_contract_compliance", "candidate_output_contract_compliance_v1.json"),
    ("no_runtime_boundary_audit_result", "no_runtime_boundary_audit_result_v1.json"),
    ("controlled_trial_abort_monitor_result", "controlled_trial_abort_monitor_result_v1.json"),
    ("controlled_trial_execution_summary", "controlled_trial_execution_summary_v1.json"),
    ("post_execution_review_handoff", "post_execution_review_handoff_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT_ROOT)
    p.add_argument("--luna-validation-factory-consolidation-root", required=True)
    p.add_argument(
        "--vision-sample-frame-single-chain-controlled-trial-authorization-via-harness-root",
        required=True,
    )
    args = p.parse_args()

    result = run_vision_sample_frame_single_chain_controlled_trial_execution_v1(
        luna_validation_factory_consolidation_root=args.luna_validation_factory_consolidation_root,
        vision_sample_frame_single_chain_controlled_trial_authorization_via_harness_root=(
            args.vision_sample_frame_single_chain_controlled_trial_authorization_via_harness_root
        ),
        output_root=args.output_root,
    )
    out = Path(args.output_root)
    for key, fname in OUTPUT_FILES:
        _write_json(out / fname, result[key])

    voc = result["visual_observation_candidate_result"]
    for i, cand in enumerate(voc.get("candidates") or []):
        _write_json(out / f"visual_observation_candidate_{i + 1}_v1.json", cand)

    s = result["summary"]
    print(
        json.dumps(
            {
                "phase": s.get("phase"),
                "boundary_ok": s.get("boundary_ok"),
                "final_decision": s.get("final_decision"),
                "recommended_next_phase": s.get("recommended_next_phase"),
                "candidates_generated": s.get("candidates_generated"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if s.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
