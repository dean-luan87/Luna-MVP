#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Luna Project Structure Consolidation DryRun v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Dict

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.luna_project_structure_consolidation_dryrun_v1 import (
    run_luna_project_structure_consolidation_dryrun_v1,
)

DEFAULT_OUTPUT_ROOT = REPO_ROOT / "_eval_out" / "luna_project_structure_consolidation_dryrun_v1_smoke_v0"


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Luna Project Structure Consolidation DryRun v1")
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument("--repo-root", default=str(REPO_ROOT))
    parser.add_argument(
        "--consolidation-planning-root",
        default=str(REPO_ROOT / "_eval_out" / "luna_project_structure_consolidation_planning_v1_smoke_v0"),
    )
    parser.add_argument(
        "--structure-map-dryrun-root",
        default=str(REPO_ROOT / "_eval_out" / "luna_project_module_inventory_and_structure_map_dryrun_v1_smoke_v0"),
    )
    parser.add_argument(
        "--project-structure-governance-planning-root",
        default=str(REPO_ROOT / "_eval_out" / "luna_project_structure_governance_and_modularization_planning_v1_smoke_v0"),
    )
    parser.add_argument(
        "--gate-taxonomy-planning-root",
        default=str(REPO_ROOT / "_eval_out" / "gate_taxonomy_and_requirement_framework_planning_v1_smoke_v0"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = run_luna_project_structure_consolidation_dryrun_v1(
        repo_root=args.repo_root,
        consolidation_planning_root=args.consolidation_planning_root,
        structure_map_dryrun_root=args.structure_map_dryrun_root,
        project_structure_governance_planning_root=args.project_structure_governance_planning_root,
        gate_taxonomy_planning_root=args.gate_taxonomy_planning_root,
    )

    output_root = Path(args.output_root).expanduser().resolve()
    output_root.mkdir(parents=True, exist_ok=True)

    for name in (
        "summary",
        "input_root_matrix",
        "consolidation_dryrun_execution_plan",
        "batch_dryrun_results",
        "consolidation_conflict_report",
        "dependency_break_simulation",
        "boundary_integrity_review",
        "human_review_required_register",
        "do_not_auto_execute_register",
        "rollback_simulation_plan",
        "consolidation_dryrun_readiness_decision",
        "life_system_consolidation_dryrun_matrix",
        "developer_backend_boundary_dryrun",
        "client_boundary_dryrun",
        "midplatform_boundary_dryrun",
        "cognition_placeholder_boundary_dryrun",
        "historical_test_asset_dryrun_review",
        "no_file_move_boundary_report",
        "no_delete_boundary_report",
        "no_runtime_boundary_report",
        "no_write_boundary_report",
        "no_action_boundary_report",
        "next_phase_recommendation",
    ):
        _write_json(output_root / f"{name}.json", result[name])

    _write_json(
        output_root / "verifier_report.json",
        {"verifier": "PENDING", "phase": "dryrun", "source_chain": result["summary"].get("source_chain")},
    )

    s = result["summary"]
    print(
        json.dumps(
            {
                "output_root": str(output_root),
                "conflict_count": s.get("conflict_count"),
                "human_review_count": s.get("human_review_required_register_count"),
                "do_not_auto_execute_count": s.get("do_not_auto_execute_register_count"),
                "final_decision": s.get("final_decision"),
                "recommended_next_phase": s.get("recommended_next_phase"),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
