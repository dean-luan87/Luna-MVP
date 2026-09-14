#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Trajectory Analysis & Task Impact Planning v1."""

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

from capabilities.midplatform.field_continuity_detection_controlled_skeleton_implementation_v1 import (
    DEFAULT_OUTPUT as DEFAULT_CONTINUITY_SKELETON_ROOT,
)
from capabilities.midplatform.field_scene_small_range_construction_core_definition_v1 import (
    DEFAULT_OUTPUT as DEFAULT_FIELD_SCENE_ROOT,
)
from capabilities.midplatform.static_dynamic_target_locking_tracking_controlled_skeleton_implementation_v1 import (
    DEFAULT_OUTPUT as DEFAULT_TARGET_LOCKING_SKELETON_ROOT,
)
from capabilities.midplatform.trajectory_analysis_task_impact_planning_v1 import (
    DEFAULT_OUTPUT,
    run_trajectory_analysis_task_impact_planning_v1,
)

OUTPUT_FILES = (
    ("trajectory_analysis_task_impact_planning_report", "trajectory_analysis_task_impact_planning_report_v1.json"),
    ("trajectory_status_registry", "trajectory_status_registry_v1.json"),
    ("task_impact_type_registry", "task_impact_type_registry_v1.json"),
    ("trajectory_candidate_model", "trajectory_candidate_model_v1.json"),
    ("task_impact_analysis_candidate_model", "task_impact_analysis_candidate_model_v1.json"),
    ("risk_projection_candidate_model", "risk_projection_candidate_model_v1.json"),
    ("missing_information_candidate_model", "missing_information_candidate_model_v1.json"),
    ("trajectory_task_impact_rule_registry", "trajectory_task_impact_rule_registry_v1.json"),
    ("trajectory_task_impact_mock_case_registry", "trajectory_task_impact_mock_case_registry_v1.json"),
    ("trajectory_task_impact_mock_case_expected_results", "trajectory_task_impact_mock_case_expected_results_v1.json"),
    ("trajectory_task_impact_input_output_contract", "trajectory_task_impact_input_output_contract_v1.json"),
    ("trajectory_task_impact_next_implementation_plan", "trajectory_task_impact_next_implementation_plan_v1.json"),
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
    parser.add_argument("--target-locking-skeleton-root", default=DEFAULT_TARGET_LOCKING_SKELETON_ROOT)
    parser.add_argument("--continuity-skeleton-root", default=DEFAULT_CONTINUITY_SKELETON_ROOT)
    parser.add_argument("--field-scene-root", default=DEFAULT_FIELD_SCENE_ROOT)
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = run_trajectory_analysis_task_impact_planning_v1(
        target_locking_skeleton_root=args.target_locking_skeleton_root,
        continuity_skeleton_root=args.continuity_skeleton_root,
        field_scene_root=args.field_scene_root,
        output_root=args.output_root,
    )
    out = Path(args.output_root)
    out.mkdir(parents=True, exist_ok=True)
    for key, fname in OUTPUT_FILES:
        (out / fname).write_text(json.dumps(result[key], ensure_ascii=False, indent=2, default=_default) + "\n", encoding="utf-8")
    (out / "trajectory_analysis_task_impact_planning_report_v1.md").write_text(
        result["trajectory_analysis_task_impact_planning_report_md"] + "\n", encoding="utf-8",
    )
    s = result["summary"]
    print(json.dumps({
        "output_root": str(out),
        "trajectory_analysis_task_impact_planning_pass": s.get("trajectory_analysis_task_impact_planning_pass"),
        "final_decision": s.get("final_decision"),
        "recommended_next_phase": s.get("recommended_next_phase"),
        "mock_case_count": s.get("mock_case_count"),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
