#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Success Claim Gate Canonicalization Planning v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.success_claim_gate_canonicalization_planning_v1 import (
    run_success_claim_gate_canonicalization_planning_v1,
)

DEFAULT_OUTPUT_ROOT = REPO_ROOT / "_eval_out" / "success_claim_gate_canonicalization_planning_v1_smoke_v0"
DEFAULT_ROADMAP_ROOT = REPO_ROOT / "_eval_out" / "terminology_canonical_table_roadmap_decision_v1_smoke_v0"

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("input_root_matrix", "input_root_matrix.json"),
    (
        "success_claim_gate_canonicalization_planning_policy",
        "success_claim_gate_canonicalization_planning_policy_v1.json",
    ),
    ("success_claim_gate_condition_scope", "success_claim_gate_condition_scope_v1.json"),
    ("success_claim_forbidden_interpretation_matrix", "success_claim_forbidden_interpretation_matrix_v1.json"),
    (
        "success_claim_required_evidence_planning_matrix",
        "success_claim_required_evidence_planning_matrix_v1.json",
    ),
    (
        "success_claim_runtime_vs_audit_evidence_boundary",
        "success_claim_runtime_vs_audit_evidence_boundary_v1.json",
    ),
    (
        "success_claim_authorization_dependency_matrix",
        "success_claim_authorization_dependency_matrix_v1.json",
    ),
    ("success_claim_non_claims_planning_matrix", "success_claim_non_claims_planning_matrix_v1.json"),
    ("success_claim_verifier_usage_planning_matrix", "success_claim_verifier_usage_planning_matrix_v1.json"),
    ("success_claim_gate_output_plan", "success_claim_gate_output_plan_v1.json"),
    (
        "success_claim_gate_canonicalization_planning_readiness_decision",
        "success_claim_gate_canonicalization_planning_readiness_decision_v1.json",
    ),
    ("next_phase_recommendation", "next_phase_recommendation.json"),
)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Success Claim Gate Canonicalization Planning v1")
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument(
        "--terminology-canonical-table-roadmap-decision-root",
        default=str(DEFAULT_ROADMAP_ROOT),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_root = Path(args.output_root)
    result = run_success_claim_gate_canonicalization_planning_v1(
        terminology_canonical_table_roadmap_decision_root=args.terminology_canonical_table_roadmap_decision_root,
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
