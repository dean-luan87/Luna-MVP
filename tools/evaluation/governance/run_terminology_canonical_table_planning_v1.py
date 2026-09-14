#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Terminology Canonical Table Planning v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.terminology_canonical_table_planning_v1 import (
    run_terminology_canonical_table_planning_v1,
)

DEFAULT_OUTPUT_ROOT = REPO_ROOT / "_eval_out" / "terminology_canonical_table_planning_v1_smoke_v0"
DEFAULT_ROADMAP_ROOT = REPO_ROOT / "_eval_out" / "permission_semantics_canonicalization_roadmap_decision_v1_smoke_v0"

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("input_root_matrix", "input_root_matrix.json"),
    ("terminology_canonical_table_planning_policy", "terminology_canonical_table_planning_policy_v1.json"),
    ("terminology_scope_intake_matrix", "terminology_scope_intake_matrix_v1.json"),
    ("terminology_canonical_entry_plan", "terminology_canonical_entry_plan_v1.json"),
    ("terminology_high_risk_misread_matrix", "terminology_high_risk_misread_matrix_v1.json"),
    ("terminology_required_fields_planning_matrix", "terminology_required_fields_planning_matrix_v1.json"),
    ("terminology_verifier_usage_planning_matrix", "terminology_verifier_usage_planning_matrix_v1.json"),
    ("terminology_forbidden_interpretation_planning_matrix", "terminology_forbidden_interpretation_planning_matrix_v1.json"),
    ("terminology_success_claim_dependency_matrix", "terminology_success_claim_dependency_matrix_v1.json"),
    ("terminology_table_output_plan", "terminology_table_output_plan_v1.json"),
    ("terminology_canonical_table_planning_readiness_decision", "terminology_canonical_table_planning_readiness_decision_v1.json"),
    ("next_phase_recommendation", "next_phase_recommendation.json"),
)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Terminology Canonical Table Planning v1")
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument(
        "--permission-semantics-canonicalization-roadmap-decision-root",
        default=str(DEFAULT_ROADMAP_ROOT),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_root = Path(args.output_root)
    result = run_terminology_canonical_table_planning_v1(
        permission_semantics_canonicalization_roadmap_decision_root=args.permission_semantics_canonicalization_roadmap_decision_root,
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
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
