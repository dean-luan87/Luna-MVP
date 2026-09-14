#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Main Project Structure Migration Controlled Execution Roadmap Decision v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Dict

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.main_project_structure_migration_controlled_execution_roadmap_decision_v1 import (
    run_main_project_structure_migration_controlled_execution_roadmap_decision_v1,
)

DEFAULT_OUTPUT_ROOT = (
    REPO_ROOT
    / "_eval_out"
    / "main_project_structure_migration_controlled_execution_roadmap_decision_v1_smoke_v0"
)

OUTPUT_NAMES = (
    "summary",
    "input_root_matrix",
    "controlled_execution_closure_status_summary",
    "route_option_matrix",
    "priority_ranking",
    "recommended_next_phase_decision",
    "pre_authorization_rollback_rehearsal_route_decision",
    "deferred_real_migration_execution_trial_register",
    "deferred_batch_arming_trial_register",
    "deferred_post_migration_test_harness_execution_register",
    "deferred_whitebox_test_center_register",
    "deferred_developer_backend_architecture_register",
    "deferred_future_reserved_module_register",
    "boundary_freeze",
    "governance_debt_roadmap_register",
    "non_claims_register",
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
    parser = argparse.ArgumentParser(description="Run Controlled Execution Roadmap Decision v1")
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument(
        "--controlled-execution-closure-root",
        default=str(
            REPO_ROOT
            / "_eval_out"
            / "main_project_structure_migration_controlled_execution_closure_v1_smoke_v0"
        ),
    )
    parser.add_argument(
        "--controlled-execution-post-review-root",
        default=str(
            REPO_ROOT
            / "_eval_out"
            / "main_project_structure_migration_controlled_execution_post_dryrun_review_v1_smoke_v0"
        ),
    )
    parser.add_argument(
        "--controlled-execution-dryrun-root",
        default=str(
            REPO_ROOT
            / "_eval_out"
            / "main_project_structure_migration_controlled_execution_dryrun_v1_smoke_v0"
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
        "--execution-control-roadmap-root",
        default=str(
            REPO_ROOT
            / "_eval_out"
            / "main_project_structure_migration_execution_control_and_test_harness_roadmap_decision_v1_smoke_v0"
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
    output_root = Path(args.output_root)
    result = run_main_project_structure_migration_controlled_execution_roadmap_decision_v1(
        controlled_execution_closure_root=args.controlled_execution_closure_root,
        controlled_execution_post_review_root=args.controlled_execution_post_review_root,
        controlled_execution_dryrun_root=args.controlled_execution_dryrun_root,
        controlled_execution_planning_root=args.controlled_execution_planning_root,
        execution_control_roadmap_root=args.execution_control_roadmap_root,
        execution_control_closure_root=args.execution_control_closure_root,
        guarded_closure_root=args.guarded_closure_root,
        readiness_root=args.readiness_root,
        pahr_closure_root=args.pahr_closure_root,
        consolidation_closure_root=args.consolidation_closure_root,
        structure_map_root=args.structure_map_root,
        gate_taxonomy_root=args.gate_taxonomy_root,
    )
    for name in OUTPUT_NAMES:
        _write_json(output_root / f"{name}.json", result[name])

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
                "selected_route": summary.get("selected_route"),
                "final_decision": summary.get("final_decision"),
                "boundary_ok": summary.get("boundary_ok"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
