#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Luna Midplatform Health Watchdog Mount DryRunAndReview v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.midplatform_health_watchdog_mount_dryrun_and_review_v1 import (
    run_midplatform_health_watchdog_mount_dryrun_and_review_v1,
)

DEFAULT_MOUNT_PLAN = REPO_ROOT / "_tmp_eval_out" / "midplatform_health_watchdog_mount_planning"
DEFAULT_DC_HANDOFF_DR = (
    REPO_ROOT / "_tmp_eval_out" / "midplatform_decision_center_foundation_handoff_dryrun_and_review"
)
DEFAULT_DC_HANDOFF_PLAN = REPO_ROOT / "_tmp_eval_out" / "midplatform_decision_center_foundation_handoff_planning"
DEFAULT_II_HANDOFF_DR = (
    REPO_ROOT / "_tmp_eval_out" / "midplatform_information_integration_foundation_handoff_dryrun_and_review"
)
DEFAULT_MICRO_OS_DR = (
    REPO_ROOT / "_tmp_eval_out" / "midplatform_micro_os_foundation_freeze_and_handoff_dryrun_and_review"
)
DEFAULT_OUTPUT = REPO_ROOT / "_tmp_eval_out" / "midplatform_health_watchdog_mount_dryrun_and_review"

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("upstream_mount_contract_consumability_review", "upstream_mount_contract_consumability_review_v1.json"),
    ("decision_center_frozen_dependency_review", "decision_center_frozen_dependency_review_v1.json"),
    ("mount_contract_10_section_review", "mount_contract_10_section_review_v1.json"),
    ("input_contract_dryrun", "input_contract_dryrun_v1.json"),
    ("output_contract_dryrun", "output_contract_dryrun_v1.json"),
    ("processing_model_dryrun", "processing_model_dryrun_v1.json"),
    ("health_state_machine_dryrun", "health_state_machine_dryrun_v1.json"),
    ("model_rule_algorithm_placement_review", "model_rule_algorithm_placement_review_v1.json"),
    ("governance_boundary_dryrun", "governance_boundary_dryrun_v1.json"),
    ("recovery_boundary_dryrun", "recovery_boundary_dryrun_v1.json"),
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
    p = argparse.ArgumentParser()
    p.add_argument("--mount-planning-root", default=str(DEFAULT_MOUNT_PLAN))
    p.add_argument("--decision-center-handoff-dryrun-root", default=str(DEFAULT_DC_HANDOFF_DR))
    p.add_argument("--decision-center-handoff-planning-root", default=str(DEFAULT_DC_HANDOFF_PLAN))
    p.add_argument("--information-integration-handoff-dryrun-root", default=str(DEFAULT_II_HANDOFF_DR))
    p.add_argument("--micro-os-freeze-dryrun-root", default=str(DEFAULT_MICRO_OS_DR))
    p.add_argument("--output-root", default=str(DEFAULT_OUTPUT))
    args = p.parse_args()

    result = run_midplatform_health_watchdog_mount_dryrun_and_review_v1(
        midplatform_health_watchdog_mount_planning_root=args.mount_planning_root,
        midplatform_decision_center_foundation_handoff_dryrun_and_review_root=args.decision_center_handoff_dryrun_root,
        midplatform_decision_center_foundation_handoff_planning_root=args.decision_center_handoff_planning_root,
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
                "dryrun_pass": sm.get("dryrun_pass"),
                "blocker_count": sm.get("blocker_count"),
                "final_decision": sm.get("final_decision"),
                "recommended_next_phase": sm.get("recommended_next_phase"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("dryrun_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())
