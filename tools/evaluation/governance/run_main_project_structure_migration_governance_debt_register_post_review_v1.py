#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Main Project Structure Migration Governance Debt Register Post-Review v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.main_project_structure_migration_governance_debt_register_post_review_v1 import (
    run_main_project_structure_migration_governance_debt_register_post_review_v1,
)

DEFAULT_OUTPUT_ROOT = (
    REPO_ROOT
    / "_eval_out"
    / "main_project_structure_migration_governance_debt_register_post_review_v1_smoke_v0"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("input_root_matrix", "input_root_matrix.json"),
    ("governance_debt_register_post_review_policy", "governance_debt_register_post_review_policy_v1.json"),
    ("governance_debt_register_completeness_review", "governance_debt_register_completeness_review_v1.json"),
    ("governance_debt_severity_review_matrix", "governance_debt_severity_review_matrix_v1.json"),
    ("governance_debt_source_mapping_review", "governance_debt_source_mapping_review_v1.json"),
    ("blocked_progression_rules_review", "blocked_progression_rules_review_v1.json"),
    ("future_phase_mapping_review", "future_phase_mapping_review_v1.json"),
    ("verifier_addition_plan_review", "verifier_addition_plan_review_v1.json"),
    ("terminology_canonical_table_review", "terminology_canonical_table_review_v1.json"),
    ("register_non_fix_non_claims_review", "register_non_fix_non_claims_review_v1.json"),
    (
        "governance_debt_register_post_review_readiness_decision",
        "governance_debt_register_post_review_readiness_decision_v1.json",
    ),
    ("next_phase_recommendation", "next_phase_recommendation.json"),
)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Governance Debt Register Post-Review v1")
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument(
        "--governance-debt-register-root",
        default=str(
            REPO_ROOT / "_eval_out" / "main_project_structure_migration_governance_debt_register_v1_smoke_v0"
        ),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_root = Path(args.output_root)
    result = run_main_project_structure_migration_governance_debt_register_post_review_v1(
        governance_debt_register_root=args.governance_debt_register_root,
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
