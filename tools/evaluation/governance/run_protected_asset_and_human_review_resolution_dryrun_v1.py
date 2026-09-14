#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Protected Asset and Human Review Resolution DryRun v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Dict

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.protected_asset_and_human_review_resolution_dryrun_v1 import (
    run_protected_asset_and_human_review_resolution_dryrun_v1,
)

DEFAULT_OUTPUT_ROOT = REPO_ROOT / "_eval_out" / "protected_asset_and_human_review_resolution_dryrun_v1_smoke_v0"


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Protected Asset and Human Review Resolution DryRun v1")
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument(
        "--planning-root",
        default=str(REPO_ROOT / "_eval_out" / "protected_asset_and_human_review_resolution_planning_v1_smoke_v0"),
    )
    parser.add_argument(
        "--roadmap-decision-root",
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
        "--consolidation-dryrun-root",
        default=str(REPO_ROOT / "_eval_out" / "luna_project_structure_consolidation_dryrun_v1_smoke_v0"),
    )
    parser.add_argument(
        "--consolidation-planning-root",
        default=str(REPO_ROOT / "_eval_out" / "luna_project_structure_consolidation_planning_v1_smoke_v0"),
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
    result = run_protected_asset_and_human_review_resolution_dryrun_v1(
        planning_root=args.planning_root,
        roadmap_decision_root=args.roadmap_decision_root,
        consolidation_closure_root=args.consolidation_closure_root,
        consolidation_post_review_root=args.consolidation_post_review_root,
        consolidation_dryrun_root=args.consolidation_dryrun_root,
        consolidation_planning_root=args.consolidation_planning_root,
        structure_map_dryrun_root=args.structure_map_dryrun_root,
        gate_taxonomy_planning_root=args.gate_taxonomy_planning_root,
    )

    output_root = Path(args.output_root).expanduser().resolve()
    output_root.mkdir(parents=True, exist_ok=True)

    for name in (
        "summary",
        "input_root_matrix",
        "resolution_dryrun_execution_plan",
        "human_review_dryrun_cases",
        "permanent_dnae_dryrun_cases",
        "owner_assignment_dryrun_results",
        "review_decision_dryrun_results",
        "review_state_machine_dryrun_traces",
        "audit_trace_dryrun_results",
        "rollback_dryrun_results",
        "resolution_dryrun_summary_matrix",
        "resolution_dryrun_readiness_decision",
        "forbidden_decision_block_report",
        "forbidden_state_absence_report",
        "governance_debt_register",
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
                "human_review_case_count": s.get("human_review_case_count"),
                "permanent_dnae_case_count": s.get("permanent_dnae_case_count"),
                "high_risk_merge_case_count": s.get("high_risk_merge_case_count"),
                "future_placeholder_current_code_case_count": s.get("future_placeholder_current_code_case_count"),
                "target_module_unclear_case_count": s.get("target_module_unclear_case_count"),
                "audit_trace_generated_count": s.get("audit_trace_generated_count"),
                "final_decision": s.get("final_decision"),
                "recommended_next_phase": s.get("recommended_next_phase"),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
