#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Post Protected Asset and Human Review Resolution Roadmap Decision v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Dict

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.post_protected_asset_and_human_review_resolution_roadmap_decision_v1 import (
    run_post_protected_asset_and_human_review_resolution_roadmap_decision_v1,
)

DEFAULT_OUTPUT_ROOT = REPO_ROOT / "_eval_out" / "post_protected_asset_and_human_review_resolution_roadmap_decision_v1_smoke_v0"


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run Post Protected Asset and Human Review Resolution Roadmap Decision v1"
    )
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument(
        "--protected-asset-resolution-closure-root",
        default=str(REPO_ROOT / "_eval_out" / "protected_asset_and_human_review_resolution_closure_v1_smoke_v0"),
    )
    parser.add_argument(
        "--protected-asset-resolution-post-review-root",
        default=str(REPO_ROOT / "_eval_out" / "protected_asset_and_human_review_resolution_post_dryrun_review_v1_smoke_v0"),
    )
    parser.add_argument(
        "--protected-asset-resolution-dryrun-root",
        default=str(REPO_ROOT / "_eval_out" / "protected_asset_and_human_review_resolution_dryrun_v1_smoke_v0"),
    )
    parser.add_argument(
        "--protected-asset-resolution-planning-root",
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
        default=str(REPO_ROOT / "_eval_out" / "luna_project_structure_consolidation_post_dryrun_review_v1_smoke_v0"),
    )
    parser.add_argument(
        "--structure-map-dryrun-root",
        default=str(REPO_ROOT / "_eval_out" / "luna_project_module_inventory_and_structure_map_dryrun_v1_smoke_v0"),
    )
    parser.add_argument(
        "--gate-taxonomy-planning-root",
        default=str(REPO_ROOT / "_eval_out" / "gate_taxonomy_and_requirement_framework_planning_v1_smoke_v0"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = run_post_protected_asset_and_human_review_resolution_roadmap_decision_v1(
        protected_asset_resolution_closure_root=args.protected_asset_resolution_closure_root,
        protected_asset_resolution_post_review_root=args.protected_asset_resolution_post_review_root,
        protected_asset_resolution_dryrun_root=args.protected_asset_resolution_dryrun_root,
        protected_asset_resolution_planning_root=args.protected_asset_resolution_planning_root,
        consolidation_roadmap_root=args.consolidation_roadmap_root,
        consolidation_closure_root=args.consolidation_closure_root,
        consolidation_post_review_root=args.consolidation_post_review_root,
        structure_map_dryrun_root=args.structure_map_dryrun_root,
        gate_taxonomy_planning_root=args.gate_taxonomy_planning_root,
    )

    output_root = Path(args.output_root).expanduser().resolve()
    output_root.mkdir(parents=True, exist_ok=True)

    for name in (
        "summary",
        "input_root_matrix",
        "protected_asset_resolution_closure_status_summary",
        "route_option_matrix",
        "priority_ranking",
        "recommended_next_phase_decision",
        "main_project_migration_readiness_route_decision",
        "whitebox_test_center_route_decision",
        "deferred_whitebox_test_center_structure_optimization_register",
        "deferred_developer_backend_architecture_register",
        "deferred_docs_reorganization_register",
        "deferred_human_review_execution_register",
        "deferred_real_migration_register",
        "future_reserved_module_discussion_register",
        "boundary_freeze",
        "governance_debt_roadmap_register",
        "non_claims_register",
        "next_phase_recommendation",
        "no_file_move_boundary_report",
        "no_delete_boundary_report",
        "no_runtime_boundary_report",
        "no_write_boundary_report",
        "verifier_report",
    ):
        _write_json(output_root / f"{name}.json", result[name])

    s = result["summary"]
    print(
        json.dumps(
            {
                "output_root": str(output_root),
                "selected_route": s.get("selected_route"),
                "protected_asset_resolution_closed": s.get("protected_asset_resolution_closed"),
                "main_project_migration_readiness_selected": s.get("main_project_migration_readiness_selected"),
                "whitebox_test_center_structure_optimization_deferred": s.get("whitebox_test_center_structure_optimization_deferred"),
                "test_after_main_project_migration_required": s.get("test_after_main_project_migration_required"),
                "final_decision": s.get("final_decision"),
                "recommended_next_phase": s.get("recommended_next_phase"),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
