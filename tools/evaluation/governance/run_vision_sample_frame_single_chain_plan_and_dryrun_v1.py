#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Vision Sample Frame Single-Chain Plan+DryRun v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.vision_sample_frame_single_chain_plan_and_dryrun_v1 import (
    run_vision_sample_frame_single_chain_plan_and_dryrun_v1,
)

DEFAULT_OUTPUT_ROOT = REPO_ROOT / "_eval_out" / "vision_sample_frame_single_chain_plan_and_dryrun_v1_smoke_v0"

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("vision_sample_frame_plan_and_dryrun_policy", "vision_sample_frame_plan_and_dryrun_policy_v1.json"),
    ("input_review", "input_review_v1.json"),
    ("vision_sample_frame_scope_and_source_policy", "vision_sample_frame_scope_and_source_policy_v1.json"),
    ("visual_observation_candidate_schema", "visual_observation_candidate_schema_v1.json"),
    ("vision_sample_frame_fixture_input_matrix", "vision_sample_frame_fixture_input_matrix_v1.json"),
    ("vision_sample_frame_positive_flow_result", "vision_sample_frame_positive_flow_result_v1.json"),
    ("vision_sample_frame_blocked_flow_result", "vision_sample_frame_blocked_flow_result_v1.json"),
    ("vision_sample_frame_gate_result", "vision_sample_frame_gate_result_v1.json"),
    ("vision_sample_frame_stop_condition_result", "vision_sample_frame_stop_condition_result_v1.json"),
    ("no_runtime_boundary_audit", "no_runtime_boundary_audit_v1.json"),
    ("vision_sample_frame_next_step_readiness_decision", "vision_sample_frame_next_step_readiness_decision_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    p.add_argument("--vision-ocr-navigation-task-limited-runtime-trial-post-dryrun-review-root", required=True)
    args = p.parse_args()

    result = run_vision_sample_frame_single_chain_plan_and_dryrun_v1(
        vision_ocr_navigation_task_limited_runtime_trial_post_dryrun_review_root=args.vision_ocr_navigation_task_limited_runtime_trial_post_dryrun_review_root,
        output_root=args.output_root,
    )
    out = Path(args.output_root)
    for key, fname in OUTPUT_FILES:
        _write_json(out / fname, result[key])
    s = result["summary"]
    print(json.dumps({"phase": s.get("phase"), "boundary_ok": s.get("boundary_ok"), "final_decision": s.get("final_decision"), "recommended_next_phase": s.get("recommended_next_phase")}, ensure_ascii=False))
    return 0 if s.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
