#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Luna Midplatform Information Integration Mount DryRunAndReview v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.midplatform_information_integration_mount_dryrun_and_review_v1 import (
    run_midplatform_information_integration_mount_dryrun_and_review_v1,
)

DEFAULT_MOUNT_PLAN = REPO_ROOT / "_tmp_eval_out" / "midplatform_information_integration_mount_planning"
DEFAULT_FREEZE_DR = (
    REPO_ROOT / "_tmp_eval_out" / "midplatform_micro_os_foundation_freeze_and_handoff_dryrun_and_review"
)
DEFAULT_FREEZE_PLAN = REPO_ROOT / "_tmp_eval_out" / "midplatform_micro_os_foundation_freeze_and_handoff_planning"
DEFAULT_OUTPUT = REPO_ROOT / "_tmp_eval_out" / "midplatform_information_integration_mount_dryrun_and_review"

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("upstream_mount_contract_consumability_review", "upstream_mount_contract_consumability_review_v1.json"),
    ("frozen_interface_consumption_review", "frozen_interface_consumption_review_v1.json"),
    ("mount_contract_10_section_review", "mount_contract_10_section_review_v1.json"),
    ("input_contract_dryrun", "input_contract_dryrun_v1.json"),
    ("output_contract_dryrun", "output_contract_dryrun_v1.json"),
    ("processing_model_dryrun", "processing_model_dryrun_v1.json"),
    ("model_rule_algorithm_placement_review", "model_rule_algorithm_placement_review_v1.json"),
    ("governance_boundary_dryrun", "governance_boundary_dryrun_v1.json"),
    ("health_boundary_dryrun", "health_boundary_dryrun_v1.json"),
    ("worldmodel_memory_feedback_boundary_review", "worldmodel_memory_feedback_boundary_review_v1.json"),
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
    p.add_argument("--freeze-dryrun-root", default=str(DEFAULT_FREEZE_DR))
    p.add_argument("--freeze-planning-root", default=str(DEFAULT_FREEZE_PLAN))
    p.add_argument("--output-root", default=str(DEFAULT_OUTPUT))
    args = p.parse_args()

    result = run_midplatform_information_integration_mount_dryrun_and_review_v1(
        midplatform_information_integration_mount_planning_root=args.mount_planning_root,
        midplatform_micro_os_foundation_freeze_and_handoff_dryrun_and_review_root=args.freeze_dryrun_root,
        midplatform_micro_os_foundation_freeze_and_handoff_planning_root=args.freeze_planning_root,
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
