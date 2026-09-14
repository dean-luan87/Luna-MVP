#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Luna Midplatform Task Manager Core Orchestration Implementation Planning v1."""

from __future__ import annotations

import dataclasses
import json
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.task_manager_core_orchestration_implementation_planning_v1 import (
    DEFAULT_ORCHESTRATION_CONSOLIDATION_ROOT,
    DEFAULT_OUTPUT,
    run_task_manager_core_orchestration_implementation_planning_v1,
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("task_manager_core_orchestration_implementation_planning_report", "task_manager_core_orchestration_implementation_planning_report_v1.json"),
    ("implementation_planning_scope", "implementation_planning_scope_v1.json"),
    ("orchestration_functional_units", "orchestration_functional_units_v1.json"),
    ("orchestration_data_structure_plan", "orchestration_data_structure_plan_v1.json"),
    ("static_validator_plan", "static_validator_plan_v1.json"),
    ("implementation_file_plan", "implementation_file_plan_v1.json"),
    ("implementation_dependency_plan", "implementation_dependency_plan_v1.json"),
    ("non_execution_implementation_guard_plan", "non_execution_implementation_guard_plan_v1.json"),
    ("implementation_gap_register", "implementation_gap_register_v1.json"),
    ("next_route_decision", "next_route_decision_v1.json"),
    ("do_not_misclassify_rules", "do_not_misclassify_rules_v1.json"),
    ("file_size_governance_review", "file_size_governance_review_v1.json"),
    ("summary", "summary.json"),
)


def _default(obj: Any) -> Any:
    if dataclasses.is_dataclass(obj):
        return dataclasses.asdict(obj)
    if isinstance(obj, tuple):
        return list(obj)
    return str(obj)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, default=_default) + "\n", encoding="utf-8")


def main() -> int:
    parser = ArgumentParser()
    parser.add_argument("--orchestration-skeleton-consolidation-root", default=DEFAULT_ORCHESTRATION_CONSOLIDATION_ROOT)
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = run_task_manager_core_orchestration_implementation_planning_v1(
        orchestration_skeleton_consolidation_root=args.orchestration_skeleton_consolidation_root,
        output_root=args.output_root,
    )
    out = Path(args.output_root)
    for key, fname in OUTPUT_FILES:
        _write_json(out / fname, result[key])
    (out / "task_manager_core_orchestration_implementation_planning_report_v1.md").write_text(
        result["task_manager_core_orchestration_implementation_planning_report_md"] + "\n", encoding="utf-8",
    )
    summary = result["summary"]
    print(json.dumps({
        "output_root": str(out),
        "orchestration_implementation_planning_pass": summary.get("orchestration_implementation_planning_pass"),
        "selected_next_route": summary.get("selected_next_route"),
        "final_decision": summary.get("final_decision"),
        "recommended_next_phase": summary.get("recommended_next_phase"),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
