#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Information Processing Core Module-Level Controlled DryRun v1."""

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

from capabilities.midplatform.information_processing_core_module_level_controlled_dryrun_v1 import (
    DEFAULT_IPC_IMPLEMENTATION_ROOT,
    DEFAULT_OUTPUT,
    run_information_processing_core_module_level_controlled_dryrun_v1,
)

OUTPUT_FILES = (
    ("information_processing_core_module_level_controlled_dryrun_report", "information_processing_core_module_level_controlled_dryrun_report_v1.json"),
    ("module_level_dryrun_scope", "module_level_dryrun_scope_v1.json"),
    ("ipc_module_level_scenario_set", "ipc_module_level_scenario_set_v1.json"),
    ("ipc_module_level_scenario_results", "ipc_module_level_scenario_results_v1.json"),
    ("work_manual_flow_validation", "work_manual_flow_validation_v1.json"),
    ("information_type_coverage_validation", "information_type_coverage_validation_v1.json"),
    ("candidate_output_validation", "candidate_output_validation_v1.json"),
    ("judge_referee_validation", "judge_referee_validation_v1.json"),
    ("workload_control_dryrun", "workload_control_dryrun_v1.json"),
    ("peripheral_constraint_dryrun", "peripheral_constraint_dryrun_v1.json"),
    ("non_execution_guard_dryrun", "non_execution_guard_dryrun_v1.json"),
    ("ipc_qualification_result", "ipc_qualification_result_v1.json"),
    ("module_level_dryrun_result_summary", "module_level_dryrun_result_summary_v1.json"),
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


def main() -> int:
    parser = ArgumentParser()
    parser.add_argument("--ipc-implementation-root", default=DEFAULT_IPC_IMPLEMENTATION_ROOT)
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = run_information_processing_core_module_level_controlled_dryrun_v1(
        ipc_implementation_root=args.ipc_implementation_root,
        output_root=args.output_root,
    )
    out = Path(args.output_root)
    out.mkdir(parents=True, exist_ok=True)
    for key, fname in OUTPUT_FILES:
        (out / fname).write_text(
            json.dumps(result[key], ensure_ascii=False, indent=2, default=_default) + "\n",
            encoding="utf-8",
        )
    md = result.get("information_processing_core_module_level_controlled_dryrun_report_md", "")
    if md:
        (out / "information_processing_core_module_level_controlled_dryrun_report_v1.md").write_text(md + "\n", encoding="utf-8")
    s = result["summary"]
    print(json.dumps({
        "output_root": str(out),
        "ipc_module_level_controlled_dryrun_ok": s.get("ipc_module_level_controlled_dryrun_ok"),
        "passed_scenarios": s.get("passed_scenarios"),
        "failed_scenarios": s.get("failed_scenarios"),
        "final_decision": s.get("final_decision"),
        "recommended_next_phase": s.get("recommended_next_phase"),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
