#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Main Project Structure Migration Real Rollback Rehearsal Pre-Authorization DryRun v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.main_project_structure_migration_real_rollback_rehearsal_pre_authorization_dryrun_v1 import (
    run_main_project_structure_migration_real_rollback_rehearsal_pre_authorization_dryrun_v1,
)

DEFAULT_OUTPUT_ROOT = (
    REPO_ROOT
    / "_eval_out"
    / "main_project_structure_migration_real_rollback_rehearsal_pre_authorization_dryrun_v1_smoke_v0"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("input_root_matrix", "input_root_matrix.json"),
    (
        "real_rollback_rehearsal_pre_authorization_dryrun_policy",
        "real_rollback_rehearsal_pre_authorization_dryrun_policy_v1.json",
    ),
    ("owner_operator_approval_dryrun_evaluation", "owner_operator_approval_dryrun_evaluation_v1.json"),
    ("execution_window_dryrun_evaluation", "execution_window_dryrun_evaluation_v1.json"),
    ("sandbox_branch_authorization_dryrun_decision", "sandbox_branch_authorization_dryrun_decision_v1.json"),
    ("restore_map_authorization_dryrun_decision", "restore_map_authorization_dryrun_decision_v1.json"),
    ("restore_operation_boundary_dryrun_evaluation", "restore_operation_boundary_dryrun_evaluation_v1.json"),
    ("verifier_rerun_authorization_dryrun_evaluation", "verifier_rerun_authorization_dryrun_evaluation_v1.json"),
    ("evidence_generation_authorization_dryrun_evaluation", "evidence_generation_authorization_dryrun_evaluation_v1.json"),
    ("success_claim_gate_dryrun_evaluation", "success_claim_gate_dryrun_evaluation_v1.json"),
    (
        "real_rollback_rehearsal_pre_authorization_dryrun_readiness_decision",
        "real_rollback_rehearsal_pre_authorization_dryrun_readiness_decision_v1.json",
    ),
    ("next_phase_recommendation", "next_phase_recommendation.json"),
    ("no_file_move_boundary_report", "no_file_move_boundary_report.json"),
    ("no_delete_boundary_report", "no_delete_boundary_report.json"),
    ("no_runtime_boundary_report", "no_runtime_boundary_report.json"),
    ("no_write_boundary_report", "no_write_boundary_report.json"),
)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Real Rollback Rehearsal Pre-Authorization DryRun v1")
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument(
        "--pre-authorization-planning-root",
        default=str(
            REPO_ROOT
            / "_eval_out"
            / "main_project_structure_migration_real_rollback_rehearsal_pre_authorization_planning_v1_smoke_v0"
        ),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_root = Path(args.output_root)
    result = run_main_project_structure_migration_real_rollback_rehearsal_pre_authorization_dryrun_v1(
        pre_authorization_planning_root=args.pre_authorization_planning_root,
    )
    for key, filename in OUTPUT_FILES:
        _write_json(output_root / filename, result[key])

    summary = result["summary"]
    _write_json(
        output_root / "verifier_report.json",
        {
            "phase": summary.get("phase"),
            "verifier_status": "PENDING",
            "check_count": 0,
            "passed": None,
            "source_chain": summary.get("source_chain"),
        },
    )

    print(
        json.dumps(
            {
                "output_root": str(output_root),
                "final_decision": summary.get("final_decision"),
                "recommended_next_phase": summary.get("recommended_next_phase"),
                "boundary_ok": summary.get("boundary_ok"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())

