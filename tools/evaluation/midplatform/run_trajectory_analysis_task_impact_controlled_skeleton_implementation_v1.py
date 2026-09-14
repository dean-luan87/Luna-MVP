#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Trajectory Analysis Task Impact Controlled Skeleton v1."""

from __future__ import annotations

import dataclasses
import json
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.trajectory_analysis_task_impact_controlled_skeleton_implementation_v1 import (
    DEFAULT_OUTPUT,
    run_trajectory_analysis_task_impact_controlled_skeleton_implementation_v1,
)
from capabilities.midplatform.trajectory_analysis_task_impact_planning_v1 import (
    DEFAULT_OUTPUT as DEFAULT_PLANNING_ROOT,
)

OUTPUT_FILES = (
    ("trajectory_analysis_task_impact_controlled_skeleton_report", "trajectory_analysis_task_impact_controlled_skeleton_report_v1.json"),
    ("trajectory_candidate_registry", "trajectory_candidate_registry_v1.json"),
    ("task_impact_analysis_candidate_registry", "task_impact_analysis_candidate_registry_v1.json"),
    ("risk_projection_candidate_registry", "risk_projection_candidate_registry_v1.json"),
    ("missing_information_candidate_registry", "missing_information_candidate_registry_v1.json"),
    ("trajectory_analysis_mock_case_results", "trajectory_analysis_mock_case_results_v1.json"),
    ("trajectory_status_validation_results", "trajectory_status_validation_results_v1.json"),
    ("non_execution_boundary_review", "non_execution_boundary_review_v1.json"),
    ("next_stage_split_plan", "next_stage_split_plan_v1.json"),
    ("prohibited_scope", "prohibited_scope_v1.json"),
    ("file_size_governance_review", "file_size_governance_review_v1.json"),
    ("summary", "summary.json"),
)


def _default(obj: Any) -> Any:
    if dataclasses.is_dataclass(obj):
        return dataclasses.asdict(obj)
    if isinstance(obj, tuple):
        return list(obj)
    return str(obj)


def main() -> int:
    parser = ArgumentParser()
    parser.add_argument("--planning-root", default=DEFAULT_PLANNING_ROOT)
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = run_trajectory_analysis_task_impact_controlled_skeleton_implementation_v1(
        planning_root=args.planning_root,
        output_root=args.output_root,
    )
    out = Path(args.output_root)
    out.mkdir(parents=True, exist_ok=True)
    for key, fname in OUTPUT_FILES:
        (out / fname).write_text(json.dumps(result[key], ensure_ascii=False, indent=2, default=_default) + "\n", encoding="utf-8")
    (out / "trajectory_analysis_task_impact_controlled_skeleton_report_v1.md").write_text(
        result["trajectory_analysis_task_impact_controlled_skeleton_report_md"] + "\n", encoding="utf-8",
    )
    s = result["summary"]
    print(json.dumps({
        "output_root": str(out),
        "trajectory_analysis_task_impact_controlled_skeleton_pass": s.get("trajectory_analysis_task_impact_controlled_skeleton_pass"),
        "all_four_field_first_skeletons_ready_for_core_logic": s.get("all_four_field_first_skeletons_ready_for_core_logic"),
        "final_decision": s.get("final_decision"),
        "recommended_next_phase": s.get("recommended_next_phase"),
        "mock_case_count": s.get("mock_case_count"),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
