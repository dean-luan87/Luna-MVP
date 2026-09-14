#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Luna Midplatform Information Integration Controlled Skeleton Implementation Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.midplatform_information_integration_controlled_skeleton_implementation_planning_v1 import (
    run_midplatform_information_integration_controlled_skeleton_implementation_planning_v1,
)

DEFAULT_MOUNT_DRYRUN = (
    REPO_ROOT / "_tmp_eval_out" / "midplatform_information_integration_mount_dryrun_and_review"
)
DEFAULT_MOUNT_PLAN = REPO_ROOT / "_tmp_eval_out" / "midplatform_information_integration_mount_planning"
DEFAULT_FREEZE_DR = (
    REPO_ROOT / "_tmp_eval_out" / "midplatform_micro_os_foundation_freeze_and_handoff_dryrun_and_review"
)
DEFAULT_FREEZE_PLAN = REPO_ROOT / "_tmp_eval_out" / "midplatform_micro_os_foundation_freeze_and_handoff_planning"
DEFAULT_OUTPUT = (
    REPO_ROOT
    / "_tmp_eval_out"
    / "midplatform_information_integration_controlled_skeleton_implementation_planning"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("information_integration_skeleton_scope", "information_integration_skeleton_scope_v1.json"),
    ("information_integration_skeleton_file_plan", "information_integration_skeleton_file_plan_v1.json"),
    ("information_integration_type_contract", "information_integration_type_contract_v1.json"),
    ("information_integration_function_contract", "information_integration_function_contract_v1.json"),
    (
        "information_integration_static_validator_contract",
        "information_integration_static_validator_contract_v1.json",
    ),
    (
        "information_integration_processing_chain_contract",
        "information_integration_processing_chain_contract_v1.json",
    ),
    ("information_integration_governance_guard_plan", "information_integration_governance_guard_plan_v1.json"),
    ("information_integration_health_guard_plan", "information_integration_health_guard_plan_v1.json"),
    ("information_integration_recall_boundary_plan", "information_integration_recall_boundary_plan_v1.json"),
    ("information_integration_sample_plan", "information_integration_sample_plan_v1.json"),
    ("information_integration_test_plan", "information_integration_test_plan_v1.json"),
    ("information_integration_skeleton_boundary_matrix", "information_integration_skeleton_boundary_matrix_v1.json"),
    ("information_integration_skeleton_non_claims", "information_integration_skeleton_non_claims_v1.json"),
    (
        "information_integration_skeleton_planning_readiness_decision",
        "information_integration_skeleton_planning_readiness_decision_v1.json",
    ),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--mount-dryrun-root", default=str(DEFAULT_MOUNT_DRYRUN))
    p.add_argument("--mount-planning-root", default=str(DEFAULT_MOUNT_PLAN))
    p.add_argument("--freeze-dryrun-root", default=str(DEFAULT_FREEZE_DR))
    p.add_argument("--freeze-planning-root", default=str(DEFAULT_FREEZE_PLAN))
    p.add_argument("--output-root", default=str(DEFAULT_OUTPUT))
    args = p.parse_args()

    result = run_midplatform_information_integration_controlled_skeleton_implementation_planning_v1(
        midplatform_information_integration_mount_dryrun_and_review_root=args.mount_dryrun_root,
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
                "planning_pass": sm.get("planning_pass"),
                "final_decision": sm.get("final_decision"),
                "recommended_next_phase": sm.get("recommended_next_phase"),
                "information_integration_files_created_now": sm.get("information_integration_files_created_now"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("planning_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())
