#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Main Project Structure Migration Rollback Rehearsal Execution DryRun v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.main_project_structure_migration_rollback_rehearsal_execution_dryrun_v1 import (
    run_main_project_structure_migration_rollback_rehearsal_execution_dryrun_v1,
)

DEFAULT_OUTPUT_ROOT = (
    REPO_ROOT
    / "_eval_out"
    / "main_project_structure_migration_rollback_rehearsal_execution_dryrun_v1_smoke_v0"
)

# (result_key, output_filename)
OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("input_root_matrix", "input_root_matrix.json"),
    ("rollback_rehearsal_execution_dryrun_policy", "rollback_rehearsal_execution_dryrun_policy_v1.json"),
    ("dryrun_gate_evaluation_matrix", "dryrun_gate_evaluation_matrix_v1.json"),
    ("sandbox_branch_creation_dryrun_decision", "sandbox_branch_creation_dryrun_decision_v1.json"),
    ("restore_map_generation_dryrun_decision", "restore_map_generation_dryrun_decision_v1.json"),
    ("restore_operation_dryrun_blocker_matrix", "restore_operation_dryrun_blocker_matrix_v1.json"),
    ("verifier_rerun_dryrun_plan", "verifier_rerun_dryrun_plan_v1.json"),
    ("evidence_generation_dryrun_plan", "evidence_generation_dryrun_plan_v1.json"),
    ("rollback_failure_response_dryrun_trace", "rollback_failure_response_dryrun_trace_v1.json"),
    ("rollback_success_claim_dryrun_gate", "rollback_success_claim_dryrun_gate_v1.json"),
    (
        "rollback_rehearsal_execution_dryrun_readiness_decision",
        "rollback_rehearsal_execution_dryrun_readiness_decision_v1.json",
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
    parser = argparse.ArgumentParser(description="Run Rollback Rehearsal Execution DryRun v1")
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument(
        "--execution-planning-root",
        default=str(
            REPO_ROOT
            / "_eval_out"
            / "main_project_structure_migration_rollback_rehearsal_execution_planning_v1_smoke_v0"
        ),
    )
    parser.add_argument(
        "--rollback-rehearsal-closure-root",
        default=str(
            REPO_ROOT
            / "_eval_out"
            / "main_project_structure_migration_rollback_rehearsal_closure_v1_smoke_v0"
        ),
    )
    parser.add_argument(
        "--rollback-rehearsal-roadmap-root",
        default=str(
            REPO_ROOT
            / "_eval_out"
            / "main_project_structure_migration_rollback_rehearsal_roadmap_decision_v1_smoke_v0"
        ),
    )
    parser.add_argument(
        "--pre-authorization-closure-root",
        default=str(
            REPO_ROOT
            / "_eval_out"
            / "main_project_structure_migration_pre_authorization_and_rollback_rehearsal_closure_v1_smoke_v0"
        ),
    )
    parser.add_argument(
        "--controlled-execution-closure-root",
        default=str(
            REPO_ROOT
            / "_eval_out"
            / "main_project_structure_migration_controlled_execution_closure_v1_smoke_v0"
        ),
    )
    parser.add_argument(
        "--controlled-execution-planning-root",
        default=str(
            REPO_ROOT
            / "_eval_out"
            / "main_project_structure_migration_controlled_execution_planning_v1_smoke_v0"
        ),
    )
    parser.add_argument(
        "--execution-control-closure-root",
        default=str(
            REPO_ROOT
            / "_eval_out"
            / "main_project_structure_migration_execution_control_and_test_harness_closure_v1_smoke_v0"
        ),
    )
    parser.add_argument(
        "--guarded-closure-root",
        default=str(REPO_ROOT / "_eval_out" / "main_project_structure_migration_guarded_closure_v1_smoke_v0"),
    )
    parser.add_argument(
        "--readiness-root",
        default=str(REPO_ROOT / "_eval_out" / "main_project_structure_migration_readiness_and_test_plan_v1_smoke_v0"),
    )
    parser.add_argument(
        "--pahr-closure-root",
        default=str(REPO_ROOT / "_eval_out" / "protected_asset_and_human_review_resolution_closure_v1_smoke_v0"),
    )
    parser.add_argument(
        "--structure-map-root",
        default=str(
            REPO_ROOT / "_eval_out" / "luna_project_module_inventory_and_structure_map_dryrun_v1_smoke_v0"
        ),
    )
    parser.add_argument(
        "--gate-taxonomy-root",
        default=str(REPO_ROOT / "_eval_out" / "gate_taxonomy_and_requirement_framework_planning_v1_smoke_v0"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_root = Path(args.output_root)
    result = run_main_project_structure_migration_rollback_rehearsal_execution_dryrun_v1(
        execution_planning_root=args.execution_planning_root,
        rollback_rehearsal_closure_root=args.rollback_rehearsal_closure_root,
        rollback_rehearsal_roadmap_root=args.rollback_rehearsal_roadmap_root,
        pre_authorization_closure_root=args.pre_authorization_closure_root,
        controlled_execution_closure_root=args.controlled_execution_closure_root,
        controlled_execution_planning_root=args.controlled_execution_planning_root,
        execution_control_closure_root=args.execution_control_closure_root,
        guarded_closure_root=args.guarded_closure_root,
        readiness_root=args.readiness_root,
        pahr_closure_root=args.pahr_closure_root,
        structure_map_root=args.structure_map_root,
        gate_taxonomy_root=args.gate_taxonomy_root,
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
                "boundary_ok": summary.get("boundary_ok"),
                "ready_for_post_dryrun_review": summary.get("ready_for_post_dryrun_review"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
