#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Luna Midplatform Task Manager Controlled Skeleton Implementation DryRun v1."""

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

from capabilities.midplatform.midplatform_task_manager_controlled_skeleton_implementation_dryrun_v1 import (
    DEFAULT_DECISION_CENTER_HANDOFF_ROOT,
    DEFAULT_HEALTH_WATCHDOG_HANDOFF_ROOT,
    DEFAULT_MOUNT_DRYRUN_ROOT,
    DEFAULT_OUTPUT,
    DEFAULT_PLANNING_ROOT,
    run_midplatform_task_manager_controlled_skeleton_implementation_dryrun_v1,
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("task_manager_skeleton_implementation_scope_report", "task_manager_skeleton_implementation_scope_report_v1.json"),
    ("task_manager_skeleton_file_creation_report", "task_manager_skeleton_file_creation_report_v1.json"),
    ("task_manager_type_contract_validation", "task_manager_type_contract_validation_v1.json"),
    ("task_manager_function_static_validation", "task_manager_function_static_validation_v1.json"),
    ("task_manager_static_validator_review", "task_manager_static_validator_review_v1.json"),
    ("task_manager_processing_chain_dryrun", "task_manager_processing_chain_dryrun_v1.json"),
    ("task_manager_governance_guard_dryrun", "task_manager_governance_guard_dryrun_v1.json"),
    ("task_manager_execution_guard_dryrun", "task_manager_execution_guard_dryrun_v1.json"),
    ("task_manager_health_watchdog_dependency_dryrun", "task_manager_health_watchdog_dependency_dryrun_v1.json"),
    ("task_manager_decision_center_dependency_dryrun", "task_manager_decision_center_dependency_dryrun_v1.json"),
    ("task_manager_sample_dryrun", "task_manager_sample_dryrun_v1.json"),
    ("task_manager_boundary_matrix", "task_manager_boundary_matrix_v1.json"),
    ("task_manager_issue_register", "task_manager_issue_register_v1.json"),
    ("task_manager_skeleton_implementation_dryrun_readiness_decision", "task_manager_skeleton_implementation_dryrun_readiness_decision_v1.json"),
)


def _default(obj: Any) -> Any:
    if dataclasses.is_dataclass(obj):
        return dataclasses.asdict(obj)
    if isinstance(obj, tuple):
        return list(obj)
    return str(obj)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, default=_default) + "\n", encoding="utf-8")


def main() -> int:
    p = ArgumentParser()
    p.add_argument("--planning-root", default=DEFAULT_PLANNING_ROOT)
    p.add_argument("--mount-dryrun-root", default=DEFAULT_MOUNT_DRYRUN_ROOT)
    p.add_argument("--health-watchdog-handoff-root", default=DEFAULT_HEALTH_WATCHDOG_HANDOFF_ROOT)
    p.add_argument("--decision-center-handoff-root", default=DEFAULT_DECISION_CENTER_HANDOFF_ROOT)
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    args = p.parse_args()
    result = run_midplatform_task_manager_controlled_skeleton_implementation_dryrun_v1(
        planning_root=args.planning_root,
        mount_dryrun_root=args.mount_dryrun_root,
        health_watchdog_handoff_root=args.health_watchdog_handoff_root,
        decision_center_handoff_root=args.decision_center_handoff_root,
        output_root=args.output_root,
    )
    out = Path(args.output_root)
    for key, fname in OUTPUT_FILES:
        _write(out / fname, result[key])
    summary = result["summary"]
    print(json.dumps({"output_root": str(out), "dryrun_pass": summary.get("dryrun_pass"), "blocker_count": summary.get("blocker_count"), "final_decision": summary.get("final_decision"), "recommended_next_phase": summary.get("recommended_next_phase"), "task_manager_files_created_now": summary.get("task_manager_files_created_now")}, ensure_ascii=False))
    return 0 if summary.get("dryrun_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())
