#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Luna Midplatform Health Watchdog Mount Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.midplatform_health_watchdog_mount_planning_v1 import (
    run_midplatform_health_watchdog_mount_planning_v1,
)

DEFAULT_DC_HANDOFF_DR = (
    REPO_ROOT / "_tmp_eval_out" / "midplatform_decision_center_foundation_handoff_dryrun_and_review"
)
DEFAULT_DC_HANDOFF_PLAN = REPO_ROOT / "_tmp_eval_out" / "midplatform_decision_center_foundation_handoff_planning"
DEFAULT_DC_POST_DR = (
    REPO_ROOT / "_tmp_eval_out" / "midplatform_decision_center_controlled_skeleton_implementation_post_dryrun_review"
)
DEFAULT_II_HANDOFF_DR = (
    REPO_ROOT / "_tmp_eval_out" / "midplatform_information_integration_foundation_handoff_dryrun_and_review"
)
DEFAULT_MICRO_OS_DR = (
    REPO_ROOT / "_tmp_eval_out" / "midplatform_micro_os_foundation_freeze_and_handoff_dryrun_and_review"
)
DEFAULT_OUTPUT = REPO_ROOT / "_tmp_eval_out" / "midplatform_health_watchdog_mount_planning"

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("health_watchdog_mount_scope", "health_watchdog_mount_scope_v1.json"),
    ("health_watchdog_mount_contract", "health_watchdog_mount_contract_v1.json"),
    ("health_watchdog_input_contract", "health_watchdog_input_contract_v1.json"),
    ("health_watchdog_output_contract", "health_watchdog_output_contract_v1.json"),
    ("health_watchdog_processing_model", "health_watchdog_processing_model_v1.json"),
    ("health_watchdog_health_state_machine", "health_watchdog_health_state_machine_v1.json"),
    ("health_watchdog_model_rule_algorithm_placement", "health_watchdog_model_rule_algorithm_placement_v1.json"),
    ("health_watchdog_governance_boundary", "health_watchdog_governance_boundary_v1.json"),
    ("health_watchdog_recovery_boundary", "health_watchdog_recovery_boundary_v1.json"),
    ("health_watchdog_decision_center_dependency_boundary", "health_watchdog_decision_center_dependency_boundary_v1.json"),
    ("health_watchdog_downstream_handoff_matrix", "health_watchdog_downstream_handoff_matrix_v1.json"),
    ("health_watchdog_sample_flow_plan", "health_watchdog_sample_flow_plan_v1.json"),
    ("health_watchdog_failure_route_matrix", "health_watchdog_failure_route_matrix_v1.json"),
    ("health_watchdog_mount_health_metric_scope", "health_watchdog_mount_health_metric_scope_v1.json"),
    ("health_watchdog_boundary_matrix", "health_watchdog_boundary_matrix_v1.json"),
    ("health_watchdog_mount_non_claims", "health_watchdog_mount_non_claims_v1.json"),
    ("health_watchdog_mount_readiness_decision", "health_watchdog_mount_readiness_decision_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--decision-center-handoff-dryrun-root", default=str(DEFAULT_DC_HANDOFF_DR))
    p.add_argument("--decision-center-handoff-planning-root", default=str(DEFAULT_DC_HANDOFF_PLAN))
    p.add_argument("--decision-center-post-dryrun-root", default=str(DEFAULT_DC_POST_DR))
    p.add_argument("--information-integration-handoff-dryrun-root", default=str(DEFAULT_II_HANDOFF_DR))
    p.add_argument("--micro-os-freeze-dryrun-root", default=str(DEFAULT_MICRO_OS_DR))
    p.add_argument("--output-root", default=str(DEFAULT_OUTPUT))
    args = p.parse_args()

    result = run_midplatform_health_watchdog_mount_planning_v1(
        midplatform_decision_center_foundation_handoff_dryrun_and_review_root=args.decision_center_handoff_dryrun_root,
        midplatform_decision_center_foundation_handoff_planning_root=args.decision_center_handoff_planning_root,
        midplatform_decision_center_controlled_skeleton_implementation_post_dryrun_review_root=args.decision_center_post_dryrun_root,
        midplatform_information_integration_foundation_handoff_dryrun_and_review_root=args.information_integration_handoff_dryrun_root,
        midplatform_micro_os_foundation_freeze_and_handoff_dryrun_and_review_root=args.micro_os_freeze_dryrun_root,
        output_root=args.output_root,
    )
    out = Path(args.output_root)
    for key, fname in OUTPUT_FILES:
        _write(out / fname, result[key])

    sm = result["summary"]
    print(
        json.dumps(
            {
                "output_root": str(out),
                "planning_pass": sm.get("planning_pass"),
                "final_decision": sm.get("final_decision"),
                "recommended_next_phase": sm.get("recommended_next_phase"),
                "foundation_id": sm.get("foundation_id"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("planning_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())
