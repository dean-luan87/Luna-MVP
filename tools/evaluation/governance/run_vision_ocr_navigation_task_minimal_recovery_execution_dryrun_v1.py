#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Vision / OCR / Navigation / Task Minimal Recovery Execution DryRun v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.vision_ocr_navigation_task_minimal_recovery_execution_dryrun_v1 import (
    run_vision_ocr_navigation_task_minimal_recovery_execution_dryrun_v1,
)

DEFAULT_OUTPUT_ROOT = (
    REPO_ROOT / "_eval_out" / "vision_ocr_navigation_task_minimal_recovery_execution_dryrun_v1_smoke_v0"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("minimal_recovery_execution_dryrun_policy", "minimal_recovery_execution_dryrun_policy_v1.json"),
    ("minimal_execution_planning_input_review", "minimal_execution_planning_input_review_v1.json"),
    ("dryrun_scenario_matrix", "dryrun_scenario_matrix_v1.json"),
    ("visual_observation_candidate_dryrun", "visual_observation_candidate_dryrun_v1.json"),
    ("task_observation_requirement_dryrun", "task_observation_requirement_dryrun_v1.json"),
    ("ocr_request_candidate_dryrun", "ocr_request_candidate_dryrun_v1.json"),
    ("navigation_guidance_candidate_dryrun", "navigation_guidance_candidate_dryrun_v1.json"),
    ("task_response_candidate_dryrun", "task_response_candidate_dryrun_v1.json"),
    ("cross_chain_candidate_flow_trace", "cross_chain_candidate_flow_trace_v1.json"),
    ("execution_gate_consumption_result", "execution_gate_consumption_result_v1.json"),
    ("fallback_consumption_result", "fallback_consumption_result_v1.json"),
    ("no_runtime_boundary_audit", "no_runtime_boundary_audit_v1.json"),
    ("minimal_recovery_execution_dryrun_non_claims_register", "minimal_recovery_execution_dryrun_non_claims_register_v1.json"),
    ("minimal_recovery_execution_dryrun_readiness_decision", "minimal_recovery_execution_dryrun_readiness_decision_v1.json"),
)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    p.add_argument(
        "--vision-ocr-navigation-task-minimal-recovery-execution-planning-root",
        required=True,
    )
    return p.parse_args()


def main() -> int:
    args = parse_args()
    result = run_vision_ocr_navigation_task_minimal_recovery_execution_dryrun_v1(
        vision_ocr_navigation_task_minimal_recovery_execution_planning_root=(
            args.vision_ocr_navigation_task_minimal_recovery_execution_planning_root
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
                "high_risk_count": summary.get("high_risk_count"),
                "scenarios_passed": summary.get("scenarios_passed"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
