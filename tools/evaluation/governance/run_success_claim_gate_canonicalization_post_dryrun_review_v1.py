#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Success Claim Gate Canonicalization Post-DryRun Review v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.success_claim_gate_canonicalization_post_dryrun_review_v1 import (
    run_success_claim_gate_canonicalization_post_dryrun_review_v1,
)

DEFAULT_OUTPUT_ROOT = REPO_ROOT / "_eval_out" / "success_claim_gate_canonicalization_post_dryrun_review_v1_smoke_v0"
DEFAULT_DRYRUN_ROOT = REPO_ROOT / "_eval_out" / "success_claim_gate_canonicalization_dryrun_v1_smoke_v0"

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("input_root_matrix", "input_root_matrix.json"),
    (
        "success_claim_gate_post_dryrun_review_policy",
        "success_claim_gate_post_dryrun_review_policy_v1.json",
    ),
    ("success_claim_dryrun_completeness_review", "success_claim_dryrun_completeness_review_v1.json"),
    ("success_claim_gate_non_generation_review", "success_claim_gate_non_generation_review_v1.json"),
    ("success_claim_allowance_block_review", "success_claim_allowance_block_review_v1.json"),
    ("success_claim_evidence_boundary_review", "success_claim_evidence_boundary_review_v1.json"),
    ("success_claim_authorization_dependency_review", "success_claim_authorization_dependency_review_v1.json"),
    ("success_claim_forbidden_interpretation_review", "success_claim_forbidden_interpretation_review_v1.json"),
    ("success_claim_verifier_non_modification_review", "success_claim_verifier_non_modification_review_v1.json"),
    ("success_claim_non_claims_non_write_review", "success_claim_non_claims_non_write_review_v1.json"),
    ("success_claim_cross_artifact_consistency_review", "success_claim_cross_artifact_consistency_review_v1.json"),
    (
        "success_claim_gate_post_dryrun_review_readiness_decision",
        "success_claim_gate_post_dryrun_review_readiness_decision_v1.json",
    ),
    ("next_phase_recommendation", "next_phase_recommendation.json"),
)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Success Claim Gate Canonicalization Post-DryRun Review v1")
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument(
        "--success-claim-gate-canonicalization-dryrun-root",
        default=str(DEFAULT_DRYRUN_ROOT),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_root = Path(args.output_root)
    result = run_success_claim_gate_canonicalization_post_dryrun_review_v1(
        success_claim_gate_canonicalization_dryrun_root=args.success_claim_gate_canonicalization_dryrun_root,
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
