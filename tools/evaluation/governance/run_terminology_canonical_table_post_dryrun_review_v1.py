#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Terminology Canonical Table Post-DryRun Review v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.terminology_canonical_table_post_dryrun_review_v1 import (
    run_terminology_canonical_table_post_dryrun_review_v1,
)

DEFAULT_OUTPUT_ROOT = REPO_ROOT / "_eval_out" / "terminology_canonical_table_post_dryrun_review_v1_smoke_v0"
DEFAULT_DRYRUN_ROOT = REPO_ROOT / "_eval_out" / "terminology_canonical_table_dryrun_v1_smoke_v0"

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("input_root_matrix", "input_root_matrix.json"),
    (
        "terminology_canonical_table_post_dryrun_review_policy",
        "terminology_canonical_table_post_dryrun_review_policy_v1.json",
    ),
    ("terminology_dryrun_completeness_review", "terminology_dryrun_completeness_review_v1.json"),
    ("terminology_formal_table_non_generation_review", "terminology_formal_table_non_generation_review_v1.json"),
    ("terminology_entry_simulation_review", "terminology_entry_simulation_review_v1.json"),
    ("terminology_verifier_non_modification_review", "terminology_verifier_non_modification_review_v1.json"),
    (
        "terminology_forbidden_interpretation_non_enforcement_review",
        "terminology_forbidden_interpretation_non_enforcement_review_v1.json",
    ),
    ("terminology_required_fields_simulation_review", "terminology_required_fields_simulation_review_v1.json"),
    ("terminology_registry_write_review", "terminology_registry_write_review_v1.json"),
    ("terminology_success_claim_dependency_review", "terminology_success_claim_dependency_review_v1.json"),
    ("terminology_post_dryrun_review_non_claims_register", "terminology_post_dryrun_review_non_claims_register_v1.json"),
    (
        "terminology_canonical_table_post_dryrun_review_readiness_decision",
        "terminology_canonical_table_post_dryrun_review_readiness_decision_v1.json",
    ),
    ("next_phase_recommendation", "next_phase_recommendation.json"),
)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Terminology Canonical Table Post-DryRun Review v1")
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument(
        "--terminology-canonical-table-dryrun-root",
        default=str(DEFAULT_DRYRUN_ROOT),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_root = Path(args.output_root)
    result = run_terminology_canonical_table_post_dryrun_review_v1(
        terminology_canonical_table_dryrun_root=args.terminology_canonical_table_dryrun_root,
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
