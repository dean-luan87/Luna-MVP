#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Field Simulation Skeleton v1."""

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

from capabilities.midplatform.field_simulation_planning_v1 import DEFAULT_OUTPUT as DEFAULT_PLANNING_ROOT
from capabilities.midplatform.field_simulation_skeleton_v1 import (
    DEFAULT_OUTPUT,
    run_field_simulation_skeleton_v1,
)
from capabilities.midplatform.real_model_field_construction_success_path_hardening_v1 import (
    DEFAULT_OUTPUT as DEFAULT_HARDENING_ROOT,
)
from capabilities.midplatform.yolo_depth_controlled_real_model_dryrun_v1 import (
    DEFAULT_OUTPUT as DEFAULT_DRYRUN_ROOT,
)

OUTPUT_FILES = (
    ("field_simulation_skeleton_report", "field_simulation_skeleton_report_v1.json"),
    ("field_simulation_input_view_registry", "field_simulation_input_view_registry_v1.json"),
    ("simulation_eligibility_candidate_registry", "simulation_eligibility_candidate_registry_v1.json"),
    ("field_simulation_plan_candidate_registry", "field_simulation_plan_candidate_registry_v1.json"),
    ("field_simulation_candidate_registry", "field_simulation_candidate_registry_v1.json"),
    ("field_simulation_readiness_candidate_registry", "field_simulation_readiness_candidate_registry_v1.json"),
    ("field_simulation_skeleton_case_results", "field_simulation_skeleton_case_results_v1.json"),
    ("field_simulation_traceability_review", "field_simulation_traceability_review_v1.json"),
    ("no_action_no_fact_boundary_review", "no_action_no_fact_boundary_review_v1.json"),
    ("readiness_for_task_reasoning_planning_review", "readiness_for_task_reasoning_planning_review_v1.json"),
    ("non_execution_boundary_review", "non_execution_boundary_review_v1.json"),
    ("file_size_governance_review", "file_size_governance_review_v1.json"),
    ("prohibited_scope", "prohibited_scope_v1.json"),
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
    parser.add_argument("--hardening-root", default=DEFAULT_HARDENING_ROOT)
    parser.add_argument("--dryrun-root", default=DEFAULT_DRYRUN_ROOT)
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = run_field_simulation_skeleton_v1(
        planning_root=args.planning_root,
        hardening_root=args.hardening_root,
        dryrun_root=args.dryrun_root,
        output_root=args.output_root,
    )
    out = Path(args.output_root)
    out.mkdir(parents=True, exist_ok=True)
    for key, fname in OUTPUT_FILES:
        (out / fname).write_text(
            json.dumps(result[key], ensure_ascii=False, indent=2, default=_default) + "\n",
            encoding="utf-8",
        )
    (out / "field_simulation_skeleton_report_v1.md").write_text(
        result["field_simulation_skeleton_report_md"] + "\n",
        encoding="utf-8",
    )
    s = result["summary"]
    print(json.dumps({
        "output_root": str(out),
        "field_simulation_skeleton_pass": s.get("field_simulation_skeleton_pass"),
        "final_decision": s.get("final_decision"),
        "recommended_next_phase": s.get("recommended_next_phase"),
        "skeleton_case_count": s.get("skeleton_case_count"),
        "simulation_candidate_count": s.get("simulation_candidate_count"),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
