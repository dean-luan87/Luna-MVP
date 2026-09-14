#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Luna Midplatform Task Manager Core Orchestration Module-Level Controlled DryRun v1."""

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

from capabilities.midplatform.task_manager_core_orchestration_module_level_controlled_dryrun_v1 import (
    DEFAULT_CONTROLLED_SKELETON_ROOT,
    DEFAULT_OUTPUT,
    run_task_manager_core_orchestration_module_level_controlled_dryrun_v1,
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("module_level_controlled_dryrun_report", "module_level_controlled_dryrun_report_v1.json"),
    ("controlled_dryrun_scope", "controlled_dryrun_scope_v1.json"),
    ("controlled_dryrun_scenario_set", "controlled_dryrun_scenario_set_v1.json"),
    ("controlled_dryrun_scenario_results", "controlled_dryrun_scenario_results_v1.json"),
    ("module_level_flow_validation", "module_level_flow_validation_v1.json"),
    ("candidate_output_validation", "candidate_output_validation_v1.json"),
    ("non_execution_guard_dryrun", "non_execution_guard_dryrun_v1.json"),
    ("error_blocker_defer_handling_validation", "error_blocker_defer_handling_validation_v1.json"),
    ("module_level_dryrun_result_summary", "module_level_dryrun_result_summary_v1.json"),
    ("integration_readiness_positioning", "integration_readiness_positioning_v1.json"),
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
    parser.add_argument("--controlled-skeleton-implementation-root", default=DEFAULT_CONTROLLED_SKELETON_ROOT)
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = run_task_manager_core_orchestration_module_level_controlled_dryrun_v1(
        controlled_skeleton_implementation_root=args.controlled_skeleton_implementation_root,
        output_root=args.output_root,
    )
    out = Path(args.output_root)
    for key, fname in OUTPUT_FILES:
        _write_json(out / fname, result[key])
    (out / "module_level_controlled_dryrun_report_v1.md").write_text(
        result["module_level_controlled_dryrun_report_md"] + "\n", encoding="utf-8",
    )
    summary = result["summary"]
    print(json.dumps({
        "output_root": str(out),
        "orchestration_module_level_controlled_dryrun_pass": summary.get("orchestration_module_level_controlled_dryrun_pass"),
        "module_level_controlled_dryrun_ok": summary.get("module_level_controlled_dryrun_ok"),
        "passed_scenarios": summary.get("passed_scenarios"),
        "failed_scenarios": summary.get("failed_scenarios"),
        "selected_next_route": summary.get("selected_next_route"),
        "final_decision": summary.get("final_decision"),
        "recommended_next_phase": summary.get("recommended_next_phase"),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
