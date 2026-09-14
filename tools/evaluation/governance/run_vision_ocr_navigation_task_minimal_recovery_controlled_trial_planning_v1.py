#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Vision / OCR / Navigation / Task Minimal Recovery Controlled Trial Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.vision_ocr_navigation_task_minimal_recovery_controlled_trial_planning_v1 import (
    run_vision_ocr_navigation_task_minimal_recovery_controlled_trial_planning_v1,
)

DEFAULT_OUTPUT_ROOT = (
    REPO_ROOT / "_eval_out" / "vision_ocr_navigation_task_minimal_recovery_controlled_trial_planning_v1_smoke_v0"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("controlled_trial_planning_policy", "controlled_trial_planning_policy_v1.json"),
    ("post_dryrun_review_input_review", "post_dryrun_review_input_review_v1.json"),
    ("controlled_trial_scope_matrix", "controlled_trial_scope_matrix_v1.json"),
    ("controlled_trial_input_source_policy", "controlled_trial_input_source_policy_v1.json"),
    ("controlled_trial_allowed_candidate_flow", "controlled_trial_allowed_candidate_flow_v1.json"),
    ("controlled_trial_gate_matrix", "controlled_trial_gate_matrix_v1.json"),
    ("controlled_trial_stop_condition_matrix", "controlled_trial_stop_condition_matrix_v1.json"),
    ("controlled_trial_observation_logging_plan", "controlled_trial_observation_logging_plan_v1.json"),
    ("controlled_trial_no_fact_write_policy", "controlled_trial_no_fact_write_policy_v1.json"),
    ("controlled_trial_fallback_plan", "controlled_trial_fallback_plan_v1.json"),
    ("controlled_trial_dryrun_plan", "controlled_trial_dryrun_plan_v1.json"),
    ("controlled_trial_non_claims_register", "controlled_trial_non_claims_register_v1.json"),
    ("controlled_trial_planning_readiness_decision", "controlled_trial_planning_readiness_decision_v1.json"),
)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    p.add_argument(
        "--vision-ocr-navigation-task-minimal-recovery-execution-post-dryrun-review-root",
        required=True,
    )
    return p.parse_args()


def main() -> int:
    args = parse_args()
    result = run_vision_ocr_navigation_task_minimal_recovery_controlled_trial_planning_v1(
        vision_ocr_navigation_task_minimal_recovery_execution_post_dryrun_review_root=(
            args.vision_ocr_navigation_task_minimal_recovery_execution_post_dryrun_review_root
        ),
        trial_output_root=args.output_root,
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
                "final_decision": summary.get("final_decision"),
                "recommended_next_phase": summary.get("recommended_next_phase"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
