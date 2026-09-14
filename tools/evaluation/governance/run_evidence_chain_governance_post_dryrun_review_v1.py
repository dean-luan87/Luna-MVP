#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Evidence Chain Governance Post-DryRun Review v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.evidence_chain_governance_post_dryrun_review_v1 import (
    run_evidence_chain_governance_post_dryrun_review_v1,
)

DEFAULT_OUTPUT_ROOT = REPO_ROOT / "_eval_out" / "evidence_chain_governance_post_dryrun_review_v1_smoke_v0"
DEFAULT_DRYRUN_ROOT = REPO_ROOT / "_eval_out" / "evidence_chain_governance_dryrun_v1_smoke_v0"

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("input_root_matrix", "input_root_matrix.json"),
    ("evidence_chain_post_dryrun_review_policy", "evidence_chain_post_dryrun_review_policy_v1.json"),
    ("evidence_dryrun_completeness_review", "evidence_dryrun_completeness_review_v1.json"),
    ("evidence_generation_block_review", "evidence_generation_block_review_v1.json"),
    ("evidence_success_claim_acceptance_block_review", "evidence_success_claim_acceptance_block_review_v1.json"),
    ("evidence_lifecycle_boundary_review", "evidence_lifecycle_boundary_review_v1.json"),
    ("evidence_acceptance_policy_review", "evidence_acceptance_policy_review_v1.json"),
    ("evidence_source_chain_standalone_review", "evidence_source_chain_standalone_review_v1.json"),
    ("evidence_usage_and_upgrade_block_review", "evidence_usage_and_upgrade_block_review_v1.json"),
    ("evidence_eligibility_review", "evidence_eligibility_review_v1.json"),
    ("evidence_verifier_non_modification_review", "evidence_verifier_non_modification_review_v1.json"),
    ("evidence_non_claims_non_write_review", "evidence_non_claims_non_write_review_v1.json"),
    (
        "evidence_chain_post_dryrun_review_readiness_decision",
        "evidence_chain_post_dryrun_review_readiness_decision_v1.json",
    ),
    ("next_phase_recommendation", "next_phase_recommendation.json"),
)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Evidence Chain Governance Post-DryRun Review v1")
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument(
        "--evidence-chain-governance-dryrun-root",
        default=str(DEFAULT_DRYRUN_ROOT),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_root = Path(args.output_root)
    result = run_evidence_chain_governance_post_dryrun_review_v1(
        evidence_chain_governance_dryrun_root=args.evidence_chain_governance_dryrun_root,
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
