#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Luna Midplatform Task Manager Mount Planning v1."""

from __future__ import annotations

import json
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.midplatform_task_manager_mount_planning_v1 import (
    DEFAULT_DECISION_CENTER_HANDOFF_DRYRUN_ROOT,
    DEFAULT_HEALTH_WATCHDOG_HANDOFF_DRYRUN_ROOT,
    DEFAULT_II_HANDOFF_DRYRUN_ROOT,
    DEFAULT_MICRO_OS_FREEZE_DRYRUN_ROOT,
    DEFAULT_OUTPUT,
    run_midplatform_task_manager_mount_planning_v1,
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("task_manager_mount_scope", "task_manager_mount_scope_v1.json"),
    ("task_manager_mount_contract", "task_manager_mount_contract_v1.json"),
    ("task_manager_input_contract", "task_manager_input_contract_v1.json"),
    ("task_manager_output_contract", "task_manager_output_contract_v1.json"),
    ("task_manager_processing_model", "task_manager_processing_model_v1.json"),
    ("task_manager_task_state_machine", "task_manager_task_state_machine_v1.json"),
    ("task_manager_model_rule_algorithm_placement", "task_manager_model_rule_algorithm_placement_v1.json"),
    ("task_manager_governance_boundary", "task_manager_governance_boundary_v1.json"),
    ("task_manager_health_watchdog_dependency_boundary", "task_manager_health_watchdog_dependency_boundary_v1.json"),
    ("task_manager_decision_center_dependency_boundary", "task_manager_decision_center_dependency_boundary_v1.json"),
    ("task_manager_downstream_handoff_matrix", "task_manager_downstream_handoff_matrix_v1.json"),
    ("task_manager_sample_flow_plan", "task_manager_sample_flow_plan_v1.json"),
    ("task_manager_failure_route_matrix", "task_manager_failure_route_matrix_v1.json"),
    ("task_manager_mount_health_metric_scope", "task_manager_mount_health_metric_scope_v1.json"),
    ("task_manager_boundary_matrix", "task_manager_boundary_matrix_v1.json"),
    ("task_manager_mount_non_claims", "task_manager_mount_non_claims_v1.json"),
    ("task_manager_mount_readiness_decision", "task_manager_mount_readiness_decision_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = ArgumentParser()
    parser.add_argument("--health-watchdog-handoff-dryrun-root", default=DEFAULT_HEALTH_WATCHDOG_HANDOFF_DRYRUN_ROOT)
    parser.add_argument("--decision-center-handoff-dryrun-root", default=DEFAULT_DECISION_CENTER_HANDOFF_DRYRUN_ROOT)
    parser.add_argument("--information-integration-handoff-dryrun-root", default=DEFAULT_II_HANDOFF_DRYRUN_ROOT)
    parser.add_argument("--micro-os-freeze-dryrun-root", default=DEFAULT_MICRO_OS_FREEZE_DRYRUN_ROOT)
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    result = run_midplatform_task_manager_mount_planning_v1(
        health_watchdog_handoff_dryrun_root=args.health_watchdog_handoff_dryrun_root,
        decision_center_handoff_dryrun_root=args.decision_center_handoff_dryrun_root,
        information_integration_handoff_dryrun_root=args.information_integration_handoff_dryrun_root,
        micro_os_freeze_dryrun_root=args.micro_os_freeze_dryrun_root,
        output_root=args.output_root,
    )
    out = Path(args.output_root)
    for key, fname in OUTPUT_FILES:
        _write(out / fname, result[key])
    summary = result["summary"]
    print(
        json.dumps(
            {
                "output_root": str(out),
                "planning_pass": summary.get("planning_pass"),
                "blocker_count": summary.get("blocker_count"),
                "final_decision": summary.get("final_decision"),
                "recommended_next_phase": summary.get("recommended_next_phase"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("planning_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())
