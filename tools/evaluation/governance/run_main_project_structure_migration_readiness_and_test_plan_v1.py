#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Main Project Structure Migration Readiness and Test Plan v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Dict

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.main_project_structure_migration_readiness_and_test_plan_v1 import (
    run_main_project_structure_migration_readiness_and_test_plan_v1,
)

PHASE_ID = "Phase-Main-Project-Structure-Migration-Readiness-and-Test-Plan-v1-001"

DEFAULT_OUTPUT_ROOT = (
    REPO_ROOT / "_eval_out" / "main_project_structure_migration_readiness_and_test_plan_v1_smoke_v0"
)

OUTPUT_NAMES = (
    "summary",
    "input_root_matrix",
    "main_project_migration_readiness_policy",
    "migration_readiness_gate",
    "migration_allowed_scope",
    "migration_forbidden_scope",
    "pre_migration_checklist",
    "post_migration_test_plan",
    "migration_rollback_requirement",
    "whitebox_test_center_deferment_policy",
    "future_reserved_module_constraint",
    "migration_readiness_decision",
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
    parser = argparse.ArgumentParser(
        description="Run Main Project Structure Migration Readiness and Test Plan v1"
    )
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
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
        default=str(
            REPO_ROOT / "_eval_out" / "protected_asset_and_human_review_resolution_closure_v1_smoke_v0"
        ),
    )
    parser.add_argument(
        "--pahr-post-review-root",
        default=str(
            REPO_ROOT
            / "_eval_out"
            / "protected_asset_and_human_review_resolution_post_dryrun_review_v1_smoke_v0"
        ),
    )
    parser.add_argument(
        "--pahr-dryrun-root",
        default=str(REPO_ROOT / "_eval_out" / "protected_asset_and_human_review_resolution_dryrun_v1_smoke_v0"),
    )
    parser.add_argument(
        "--pahr-planning-root",
        default=str(REPO_ROOT / "_eval_out" / "protected_asset_and_human_review_resolution_planning_v1_smoke_v0"),
    )
    parser.add_argument(
        "--consolidation-roadmap-root",
        default=str(REPO_ROOT / "_eval_out" / "luna_project_structure_consolidation_roadmap_decision_v1_smoke_v0"),
    )
    parser.add_argument(
        "--consolidation-closure-root",
        default=str(REPO_ROOT / "_eval_out" / "luna_project_structure_consolidation_closure_v1_smoke_v0"),
    )
    parser.add_argument(
        "--consolidation-post-review-root",
        default=str(
            REPO_ROOT / "_eval_out" / "luna_project_structure_consolidation_post_dryrun_review_v1_smoke_v0"
        ),
    )
    parser.add_argument(
        "--consolidation-dryrun-root",
        default=str(REPO_ROOT / "_eval_out" / "luna_project_structure_consolidation_dryrun_v1_smoke_v0"),
    )
    parser.add_argument(
        "--consolidation-planning-root",
        default=str(REPO_ROOT / "_eval_out" / "luna_project_structure_consolidation_planning_v1_smoke_v0"),
    )
    parser.add_argument(
        "--structure-map-root",
        default=str(
            REPO_ROOT
            / "_eval_out"
            / "luna_project_module_inventory_and_structure_map_dryrun_v1_smoke_v0"
        ),
    )
    parser.add_argument(
        "--structure-governance-root",
        default=str(
            REPO_ROOT
            / "_eval_out"
            / "luna_project_structure_governance_and_modularization_planning_v1_smoke_v0"
        ),
    )
    parser.add_argument(
        "--gate-taxonomy-root",
        default=str(REPO_ROOT / "_eval_out" / "gate_taxonomy_and_requirement_framework_planning_v1_smoke_v0"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = run_main_project_structure_migration_readiness_and_test_plan_v1(
        roadmap_decision_root=args.roadmap_decision_root,
        pahr_closure_root=args.pahr_closure_root,
        pahr_post_review_root=args.pahr_post_review_root,
        pahr_dryrun_root=args.pahr_dryrun_root,
        pahr_planning_root=args.pahr_planning_root,
        consolidation_roadmap_root=args.consolidation_roadmap_root,
        consolidation_closure_root=args.consolidation_closure_root,
        consolidation_post_review_root=args.consolidation_post_review_root,
        consolidation_dryrun_root=args.consolidation_dryrun_root,
        consolidation_planning_root=args.consolidation_planning_root,
        structure_map_root=args.structure_map_root,
        structure_governance_root=args.structure_governance_root,
        gate_taxonomy_root=args.gate_taxonomy_root,
    )

    output_root = Path(args.output_root).expanduser().resolve()
    output_root.mkdir(parents=True, exist_ok=True)

    for name in OUTPUT_NAMES:
        _write_json(output_root / f"{name}.json", result[name])

    _write_json(
        output_root / "verifier_report.json",
        {"verifier": "PENDING", "phase": PHASE_ID, "source_chain": result["summary"].get("source_chain")},
    )

    s = result["summary"]
    print(
        json.dumps(
            {
                "output_root": str(output_root),
                "inventory_entry_count": s.get("inventory_entry_count"),
                "post_migration_test_group_count": s.get("post_migration_test_group_count"),
                "forbidden_scope_count": s.get("forbidden_scope_count"),
                "final_decision": s.get("final_decision"),
                "recommended_next_phase": s.get("recommended_next_phase"),
                "boundary_ok": s.get("boundary_ok"),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
