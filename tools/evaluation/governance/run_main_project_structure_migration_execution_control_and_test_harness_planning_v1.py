#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Main Project Structure Migration Execution Control and Test Harness Planning v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Dict

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.main_project_structure_migration_execution_control_and_test_harness_planning_v1 import (
    run_main_project_structure_migration_execution_control_and_test_harness_planning_v1,
)

DEFAULT_OUTPUT_ROOT = (
    REPO_ROOT
    / "_eval_out"
    / "main_project_structure_migration_execution_control_and_test_harness_planning_v1_smoke_v0"
)

OUTPUT_NAMES = (
    "summary",
    "input_root_matrix",
    "migration_execution_control_and_test_harness_planning_policy",
    "execution_control_gate",
    "batch_arming_policy",
    "abort_condition_policy",
    "pre_execution_checklist",
    "post_migration_test_harness",
    "post_migration_verifier_suite",
    "rollback_rehearsal_requirement",
    "failure_response_matrix",
    "execution_control_readiness_decision",
    "execution_non_claims_register",
    "governance_debt_register",
    "next_phase_recommendation",
    "no_file_move_boundary_report",
    "no_delete_boundary_report",
    "no_runtime_boundary_report",
    "no_write_boundary_report",
)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Execution Control and Test Harness Planning v1")
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument(
        "--guarded-roadmap-root",
        default=str(REPO_ROOT / "_eval_out" / "main_project_structure_migration_guarded_roadmap_decision_v1_smoke_v0"),
    )
    parser.add_argument(
        "--guarded-closure-root",
        default=str(REPO_ROOT / "_eval_out" / "main_project_structure_migration_guarded_closure_v1_smoke_v0"),
    )
    parser.add_argument(
        "--guarded-post-review-root",
        default=str(REPO_ROOT / "_eval_out" / "main_project_structure_migration_guarded_post_dryrun_review_v1_smoke_v0"),
    )
    parser.add_argument(
        "--guarded-dryrun-root",
        default=str(REPO_ROOT / "_eval_out" / "main_project_structure_migration_guarded_dryrun_v1_smoke_v0"),
    )
    parser.add_argument(
        "--guarded-planning-root",
        default=str(REPO_ROOT / "_eval_out" / "main_project_structure_migration_guarded_planning_v1_smoke_v0"),
    )
    parser.add_argument(
        "--readiness-root",
        default=str(REPO_ROOT / "_eval_out" / "main_project_structure_migration_readiness_and_test_plan_v1_smoke_v0"),
    )
    parser.add_argument(
        "--roadmap-decision-root",
        default=str(
            REPO_ROOT
            / "_eval_out"
            / "post_protected_asset_and_human_review_resolution_roadmap_decision_v1_smoke_v0"
        ),
    )
    parser.add_argument(
        "--pahr-closure-root",
        default=str(REPO_ROOT / "_eval_out" / "protected_asset_and_human_review_resolution_closure_v1_smoke_v0"),
    )
    parser.add_argument(
        "--consolidation-closure-root",
        default=str(REPO_ROOT / "_eval_out" / "luna_project_structure_consolidation_closure_v1_smoke_v0"),
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
    result = run_main_project_structure_migration_execution_control_and_test_harness_planning_v1(
        guarded_roadmap_root=args.guarded_roadmap_root,
        guarded_closure_root=args.guarded_closure_root,
        guarded_post_review_root=args.guarded_post_review_root,
        guarded_dryrun_root=args.guarded_dryrun_root,
        guarded_planning_root=args.guarded_planning_root,
        readiness_root=args.readiness_root,
        roadmap_decision_root=args.roadmap_decision_root,
        pahr_closure_root=args.pahr_closure_root,
        consolidation_closure_root=args.consolidation_closure_root,
        structure_map_root=args.structure_map_root,
        gate_taxonomy_root=args.gate_taxonomy_root,
    )

    output_root = Path(args.output_root).expanduser().resolve()
    output_root.mkdir(parents=True, exist_ok=True)

    for name in OUTPUT_NAMES:
        _write_json(output_root / f"{name}.json", result[name])

    _write_json(
        output_root / "verifier_report.json",
        {"verifier": "PENDING", "phase": result["summary"].get("phase"), "source_chain": result["summary"].get("source_chain")},
    )

    s = result["summary"]
    print(
        json.dumps(
            {
                "output_root": str(output_root),
                "post_migration_test_count": s.get("post_migration_test_count"),
                "abort_condition_count": s.get("abort_condition_count"),
                "ready_for_execution_control_dryrun": s.get("ready_for_execution_control_dryrun"),
                "final_decision": s.get("final_decision"),
                "boundary_ok": s.get("boundary_ok"),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
