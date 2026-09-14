#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Vision / OCR / Navigation / Task Minimal Recovery Execution Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.vision_ocr_navigation_task_minimal_recovery_execution_planning_v1 import (
    run_vision_ocr_navigation_task_minimal_recovery_execution_planning_v1,
)

DEFAULT_OUTPUT_ROOT = (
    REPO_ROOT / "_eval_out" / "vision_ocr_navigation_task_minimal_recovery_execution_planning_v1_smoke_v0"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("minimal_recovery_execution_planning_policy", "minimal_recovery_execution_planning_policy_v1.json"),
    ("recovery_post_dryrun_review_input_review", "recovery_post_dryrun_review_input_review_v1.json"),
    ("minimal_execution_scope_matrix", "minimal_execution_scope_matrix_v1.json"),
    ("vision_minimal_execution_plan", "vision_minimal_execution_plan_v1.json"),
    ("ocr_minimal_execution_plan", "ocr_minimal_execution_plan_v1.json"),
    ("navigation_minimal_execution_plan", "navigation_minimal_execution_plan_v1.json"),
    ("task_midplatform_minimal_execution_plan", "task_midplatform_minimal_execution_plan_v1.json"),
    ("cross_chain_execution_flow_plan", "cross_chain_execution_flow_plan_v1.json"),
    ("execution_boundary_gate_matrix", "execution_boundary_gate_matrix_v1.json"),
    ("failure_and_fallback_plan", "failure_and_fallback_plan_v1.json"),
    ("minimal_execution_dryrun_plan", "minimal_execution_dryrun_plan_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
    ("minimal_recovery_execution_planning_readiness_decision", "minimal_recovery_execution_planning_readiness_decision_v1.json"),
)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    p.add_argument(
        "--vision-ocr-navigation-task-midplatform-recovery-post-dryrun-review-root",
        required=True,
    )
    return p.parse_args()


def main() -> int:
    args = parse_args()
    result = run_vision_ocr_navigation_task_minimal_recovery_execution_planning_v1(
        vision_ocr_navigation_task_midplatform_recovery_post_dryrun_review_root=(
            args.vision_ocr_navigation_task_midplatform_recovery_post_dryrun_review_root
        ),
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
