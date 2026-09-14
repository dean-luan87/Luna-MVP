#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Luna Midplatform Task Manager Mount DryRunAndReview v1."""

from __future__ import annotations

import json
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.midplatform_task_manager_mount_dryrun_and_review_v1 import (
    DEFAULT_DECISION_CENTER_HANDOFF_ROOT,
    DEFAULT_HEALTH_WATCHDOG_HANDOFF_ROOT,
    DEFAULT_II_HANDOFF_ROOT,
    DEFAULT_MICRO_OS_ROOT,
    DEFAULT_OUTPUT,
    DEFAULT_PLANNING_ROOT,
    run_midplatform_task_manager_mount_dryrun_and_review_v1,
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("upstream_mount_contract_consumability_review", "upstream_mount_contract_consumability_review_v1.json"),
    ("health_watchdog_frozen_dependency_review", "health_watchdog_frozen_dependency_review_v1.json"),
    ("decision_center_frozen_dependency_review", "decision_center_frozen_dependency_review_v1.json"),
    ("mount_contract_10_section_review", "mount_contract_10_section_review_v1.json"),
    ("input_contract_dryrun", "input_contract_dryrun_v1.json"),
    ("output_contract_dryrun", "output_contract_dryrun_v1.json"),
    ("processing_model_dryrun", "processing_model_dryrun_v1.json"),
    ("task_state_machine_dryrun", "task_state_machine_dryrun_v1.json"),
    ("model_rule_algorithm_placement_review", "model_rule_algorithm_placement_review_v1.json"),
    ("governance_boundary_dryrun", "governance_boundary_dryrun_v1.json"),
    ("downstream_handoff_matrix_review", "downstream_handoff_matrix_review_v1.json"),
    ("sample_flow_dryrun", "sample_flow_dryrun_v1.json"),
    ("failure_route_dryrun_review", "failure_route_dryrun_review_v1.json"),
    ("mount_health_metric_scope_review", "mount_health_metric_scope_review_v1.json"),
    ("boundary_matrix_review", "boundary_matrix_review_v1.json"),
    ("non_claims_review", "non_claims_review_v1.json"),
    ("issue_register", "issue_register_v1.json"),
    ("mount_dryrun_readiness_decision", "mount_dryrun_readiness_decision_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = ArgumentParser()
    parser.add_argument("--task-manager-mount-planning-root", default=DEFAULT_PLANNING_ROOT)
    parser.add_argument("--health-watchdog-handoff-dryrun-root", default=DEFAULT_HEALTH_WATCHDOG_HANDOFF_ROOT)
    parser.add_argument("--decision-center-handoff-dryrun-root", default=DEFAULT_DECISION_CENTER_HANDOFF_ROOT)
    parser.add_argument("--information-integration-handoff-dryrun-root", default=DEFAULT_II_HANDOFF_ROOT)
    parser.add_argument("--micro-os-freeze-dryrun-root", default=DEFAULT_MICRO_OS_ROOT)
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = run_midplatform_task_manager_mount_dryrun_and_review_v1(
        task_manager_mount_planning_root=args.task_manager_mount_planning_root,
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
                "dryrun_pass": summary.get("dryrun_pass"),
                "blocker_count": summary.get("blocker_count"),
                "final_decision": summary.get("final_decision"),
                "recommended_next_phase": summary.get("recommended_next_phase"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("dryrun_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())
