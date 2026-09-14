#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Luna Midplatform Task Manager Controlled Skeleton Implementation Planning v1."""

from __future__ import annotations

import json
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.midplatform_task_manager_controlled_skeleton_implementation_planning_v1 import (
    DEFAULT_DECISION_CENTER_HANDOFF_ROOT,
    DEFAULT_HEALTH_WATCHDOG_HANDOFF_ROOT,
    DEFAULT_MOUNT_DRYRUN_ROOT,
    DEFAULT_MOUNT_PLANNING_ROOT,
    DEFAULT_OUTPUT,
    run_midplatform_task_manager_controlled_skeleton_implementation_planning_v1,
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("task_manager_skeleton_scope", "task_manager_skeleton_scope_v1.json"),
    ("task_manager_skeleton_file_plan", "task_manager_skeleton_file_plan_v1.json"),
    ("task_manager_type_contract", "task_manager_type_contract_v1.json"),
    ("task_manager_function_contract", "task_manager_function_contract_v1.json"),
    ("task_manager_static_validator_contract", "task_manager_static_validator_contract_v1.json"),
    ("task_manager_processing_chain_contract", "task_manager_processing_chain_contract_v1.json"),
    ("task_manager_governance_guard_plan", "task_manager_governance_guard_plan_v1.json"),
    ("task_manager_execution_guard_plan", "task_manager_execution_guard_plan_v1.json"),
    ("task_manager_health_watchdog_dependency_guard_plan", "task_manager_health_watchdog_dependency_guard_plan_v1.json"),
    ("task_manager_decision_center_dependency_guard_plan", "task_manager_decision_center_dependency_guard_plan_v1.json"),
    ("task_manager_sample_plan", "task_manager_sample_plan_v1.json"),
    ("task_manager_test_plan", "task_manager_test_plan_v1.json"),
    ("task_manager_skeleton_boundary_matrix", "task_manager_skeleton_boundary_matrix_v1.json"),
    ("task_manager_skeleton_non_claims", "task_manager_skeleton_non_claims_v1.json"),
    ("task_manager_skeleton_planning_readiness_decision", "task_manager_skeleton_planning_readiness_decision_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = ArgumentParser()
    parser.add_argument("--task-manager-mount-dryrun-root", default=DEFAULT_MOUNT_DRYRUN_ROOT)
    parser.add_argument("--task-manager-mount-planning-root", default=DEFAULT_MOUNT_PLANNING_ROOT)
    parser.add_argument("--health-watchdog-handoff-dryrun-root", default=DEFAULT_HEALTH_WATCHDOG_HANDOFF_ROOT)
    parser.add_argument("--decision-center-handoff-dryrun-root", default=DEFAULT_DECISION_CENTER_HANDOFF_ROOT)
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = run_midplatform_task_manager_controlled_skeleton_implementation_planning_v1(
        task_manager_mount_dryrun_root=args.task_manager_mount_dryrun_root,
        task_manager_mount_planning_root=args.task_manager_mount_planning_root,
        health_watchdog_handoff_dryrun_root=args.health_watchdog_handoff_dryrun_root,
        decision_center_handoff_dryrun_root=args.decision_center_handoff_dryrun_root,
        output_root=args.output_root,
    )
    out = Path(args.output_root)
    for key, fname in OUTPUT_FILES:
        _write(out / fname, result[key])
    summary = result["summary"]
    print(json.dumps({
        "output_root": str(out),
        "planning_pass": summary.get("planning_pass"),
        "blocker_count": summary.get("blocker_count"),
        "final_decision": summary.get("final_decision"),
        "recommended_next_phase": summary.get("recommended_next_phase"),
        "task_manager_files_created_now": summary.get("task_manager_files_created_now"),
    }, ensure_ascii=False))
    return 0 if summary.get("planning_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())
