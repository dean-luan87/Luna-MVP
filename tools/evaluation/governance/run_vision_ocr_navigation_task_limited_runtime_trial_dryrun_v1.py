#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Vision / OCR / Navigation / Task Limited Runtime Trial DryRun v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.vision_ocr_navigation_task_limited_runtime_trial_dryrun_v1 import (
    run_vision_ocr_navigation_task_limited_runtime_trial_dryrun_v1,
)

DEFAULT_OUTPUT_ROOT = (
    REPO_ROOT / "_eval_out" / "vision_ocr_navigation_task_limited_runtime_trial_dryrun_v1_smoke_v0"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("limited_runtime_trial_dryrun_policy", "limited_runtime_trial_dryrun_policy_v1.json"),
    ("limited_runtime_trial_planning_input_review", "limited_runtime_trial_planning_input_review_v1.json"),
    ("limited_runtime_fixture_input_matrix", "limited_runtime_fixture_input_matrix_v1.json"),
    ("vision_sample_frame_candidate_dryrun", "vision_sample_frame_candidate_dryrun_v1.json"),
    ("mock_ocr_result_candidate_dryrun", "mock_ocr_result_candidate_dryrun_v1.json"),
    ("synthetic_navigation_guidance_candidate_dryrun", "synthetic_navigation_guidance_candidate_dryrun_v1.json"),
    ("task_state_candidate_dryrun", "task_state_candidate_dryrun_v1.json"),
    ("limited_runtime_candidate_flow_trace", "limited_runtime_candidate_flow_trace_v1.json"),
    ("limited_runtime_gate_consumption_result", "limited_runtime_gate_consumption_result_v1.json"),
    ("limited_runtime_stop_condition_result", "limited_runtime_stop_condition_result_v1.json"),
    ("limited_runtime_no_runtime_boundary_audit", "limited_runtime_no_runtime_boundary_audit_v1.json"),
    ("limited_runtime_trial_dryrun_non_claims_register", "limited_runtime_trial_dryrun_non_claims_register_v1.json"),
    ("limited_runtime_trial_dryrun_readiness_decision", "limited_runtime_trial_dryrun_readiness_decision_v1.json"),
)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    p.add_argument(
        "--vision-ocr-navigation-task-limited-runtime-trial-planning-root",
        required=True,
    )
    return p.parse_args()


def main() -> int:
    args = parse_args()
    result = run_vision_ocr_navigation_task_limited_runtime_trial_dryrun_v1(
        vision_ocr_navigation_task_limited_runtime_trial_planning_root=(
            args.vision_ocr_navigation_task_limited_runtime_trial_planning_root
        ),
        dryrun_output_root=args.output_root,
    )
    out_root = Path(args.output_root)
    for key, filename in OUTPUT_FILES:
        _write_json(out_root / filename, result[key])

    summary = result["summary"]
    print(
        json.dumps(
            {
                "phase": summary.get("phase"),
                "boundary_ok": summary.get("boundary_ok"),
                "high_risk_count": summary.get("high_risk_count"),
                "final_decision": summary.get("final_decision"),
                "recommended_next_phase": summary.get("recommended_next_phase"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
