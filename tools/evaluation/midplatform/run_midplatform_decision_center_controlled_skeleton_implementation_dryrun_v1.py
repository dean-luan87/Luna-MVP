#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Luna Midplatform Decision Center Controlled Skeleton Implementation DryRun v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.midplatform_decision_center_controlled_skeleton_implementation_dryrun_v1 import (
    run_midplatform_decision_center_controlled_skeleton_implementation_dryrun_v1,
)

DEFAULT_SK_PLAN = (
    REPO_ROOT
    / "_tmp_eval_out"
    / "midplatform_decision_center_controlled_skeleton_implementation_planning"
)
DEFAULT_MOUNT_DR = REPO_ROOT / "_tmp_eval_out" / "midplatform_decision_center_mount_dryrun_and_review"
DEFAULT_HANDOFF_DR = (
    REPO_ROOT
    / "_tmp_eval_out"
    / "midplatform_information_integration_foundation_handoff_dryrun_and_review"
)
DEFAULT_OUTPUT = (
    REPO_ROOT
    / "_tmp_eval_out"
    / "midplatform_decision_center_controlled_skeleton_implementation_dryrun"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    (
        "decision_center_skeleton_implementation_scope_report",
        "decision_center_skeleton_implementation_scope_report_v1.json",
    ),
    (
        "decision_center_skeleton_file_creation_report",
        "decision_center_skeleton_file_creation_report_v1.json",
    ),
    (
        "decision_center_type_contract_validation",
        "decision_center_type_contract_validation_v1.json",
    ),
    (
        "decision_center_function_static_validation",
        "decision_center_function_static_validation_v1.json",
    ),
    (
        "decision_center_static_validator_review",
        "decision_center_static_validator_review_v1.json",
    ),
    (
        "decision_center_processing_chain_dryrun",
        "decision_center_processing_chain_dryrun_v1.json",
    ),
    (
        "decision_center_governance_guard_dryrun",
        "decision_center_governance_guard_dryrun_v1.json",
    ),
    ("decision_center_health_guard_dryrun", "decision_center_health_guard_dryrun_v1.json"),
    (
        "decision_center_information_integration_dependency_dryrun",
        "decision_center_information_integration_dependency_dryrun_v1.json",
    ),
    ("decision_center_sample_dryrun", "decision_center_sample_dryrun_v1.json"),
    ("decision_center_boundary_matrix", "decision_center_boundary_matrix_v1.json"),
    ("decision_center_issue_register", "decision_center_issue_register_v1.json"),
    (
        "decision_center_skeleton_implementation_dryrun_readiness_decision",
        "decision_center_skeleton_implementation_dryrun_readiness_decision_v1.json",
    ),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--skeleton-planning-root", default=str(DEFAULT_SK_PLAN))
    p.add_argument("--mount-dryrun-root", default=str(DEFAULT_MOUNT_DR))
    p.add_argument("--handoff-dryrun-root", default=str(DEFAULT_HANDOFF_DR))
    p.add_argument("--output-root", default=str(DEFAULT_OUTPUT))
    args = p.parse_args()

    result = run_midplatform_decision_center_controlled_skeleton_implementation_dryrun_v1(
        midplatform_decision_center_controlled_skeleton_implementation_planning_root=args.skeleton_planning_root,
        midplatform_decision_center_mount_dryrun_and_review_root=args.mount_dryrun_root,
        midplatform_information_integration_foundation_handoff_dryrun_and_review_root=args.handoff_dryrun_root,
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
                "decision_center_files_created_now": sm.get("decision_center_files_created_now"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("dryrun_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())
