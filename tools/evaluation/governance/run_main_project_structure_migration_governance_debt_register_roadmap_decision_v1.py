#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Main Project Structure Migration Governance Debt Register Roadmap Decision v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.main_project_structure_migration_governance_debt_register_roadmap_decision_v1 import (
    run_main_project_structure_migration_governance_debt_register_roadmap_decision_v1,
)

DEFAULT_OUTPUT_ROOT = (
    REPO_ROOT
    / "_eval_out"
    / "main_project_structure_migration_governance_debt_register_roadmap_decision_v1_smoke_v0"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("input_root_matrix", "input_root_matrix.json"),
    (
        "governance_debt_register_roadmap_decision_policy",
        "governance_debt_register_roadmap_decision_policy_v1.json",
    ),
    (
        "governance_debt_roadmap_route_candidate_matrix",
        "governance_debt_roadmap_route_candidate_matrix_v1.json",
    ),
    ("governance_debt_priority_decision_matrix", "governance_debt_priority_decision_matrix_v1.json"),
    (
        "selected_governance_debt_roadmap_route_decision",
        "selected_governance_debt_roadmap_route_decision_v1.json",
    ),
    ("permission_semantics_planning_scope", "permission_semantics_planning_scope_v1.json"),
    ("future_development_norms_planning_scope", "future_development_norms_planning_scope_v1.json"),
    ("forbidden_state_combination_planning", "forbidden_state_combination_planning_v1.json"),
    ("canonical_semantics_output_plan", "canonical_semantics_output_plan_v1.json"),
    (
        "governance_roadmap_decision_non_claims_register",
        "governance_roadmap_decision_non_claims_register_v1.json",
    ),
    (
        "governance_debt_register_roadmap_readiness_decision",
        "governance_debt_register_roadmap_readiness_decision_v1.json",
    ),
    ("next_phase_recommendation", "next_phase_recommendation.json"),
)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Governance Debt Register Roadmap Decision v1")
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument(
        "--governance-debt-register-post-review-root",
        default=str(
            REPO_ROOT
            / "_eval_out"
            / "main_project_structure_migration_governance_debt_register_post_review_v1_smoke_v0"
        ),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_root = Path(args.output_root)
    result = run_main_project_structure_migration_governance_debt_register_roadmap_decision_v1(
        governance_debt_register_post_review_root=args.governance_debt_register_post_review_root,
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
                "selected_route": summary.get("selected_route"),
                "boundary_ok": summary.get("boundary_ok"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
