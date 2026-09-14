#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Evidence Chain Governance DryRun v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.evidence_chain_governance_dryrun_v1 import (
    run_evidence_chain_governance_dryrun_v1,
)

DEFAULT_OUTPUT_ROOT = REPO_ROOT / "_eval_out" / "evidence_chain_governance_dryrun_v1_smoke_v0"
DEFAULT_PLANNING_ROOT = REPO_ROOT / "_eval_out" / "evidence_chain_governance_planning_v1_smoke_v0"

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("input_root_matrix", "input_root_matrix.json"),
    ("evidence_chain_governance_dryrun_policy", "evidence_chain_governance_dryrun_policy_v1.json"),
    ("evidence_planning_artifact_completeness_dryrun", "evidence_planning_artifact_completeness_dryrun_v1.json"),
    ("evidence_lifecycle_consumption_dryrun", "evidence_lifecycle_consumption_dryrun_v1.json"),
    ("evidence_source_chain_consumption_dryrun", "evidence_source_chain_consumption_dryrun_v1.json"),
    ("evidence_usage_scope_dryrun", "evidence_usage_scope_dryrun_v1.json"),
    ("evidence_upgrade_path_dryrun", "evidence_upgrade_path_dryrun_v1.json"),
    ("evidence_acceptance_policy_dryrun", "evidence_acceptance_policy_dryrun_v1.json"),
    ("evidence_non_substitution_dryrun", "evidence_non_substitution_dryrun_v1.json"),
    ("evidence_success_claim_eligibility_dryrun", "evidence_success_claim_eligibility_dryrun_v1.json"),
    ("evidence_verifier_usage_dryrun", "evidence_verifier_usage_dryrun_v1.json"),
    ("evidence_chain_non_claims_generation_dryrun", "evidence_chain_non_claims_generation_dryrun_v1.json"),
    ("evidence_chain_dryrun_readiness_decision", "evidence_chain_dryrun_readiness_decision_v1.json"),
    ("next_phase_recommendation", "next_phase_recommendation.json"),
)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Evidence Chain Governance DryRun v1")
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument(
        "--evidence-chain-governance-planning-root",
        default=str(DEFAULT_PLANNING_ROOT),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_root = Path(args.output_root)
    result = run_evidence_chain_governance_dryrun_v1(
        evidence_chain_governance_planning_root=args.evidence_chain_governance_planning_root,
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
