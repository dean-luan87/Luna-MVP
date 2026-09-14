#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Governance Constraint Module Generation Authorization Post-DryRun Review v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.governance_constraint_module_generation_authorization_post_dryrun_review_v1 import (
    run_governance_constraint_module_generation_authorization_post_dryrun_review_v1,
)

DEFAULT_OUTPUT_ROOT = (
    REPO_ROOT
    / "_eval_out"
    / "governance_constraint_module_generation_authorization_post_dryrun_review_v1_smoke_v0"
)
DEFAULT_DRYRUN_ROOT = (
    REPO_ROOT / "_eval_out" / "governance_constraint_module_generation_authorization_dryrun_v1_smoke_v0"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    (
        "governance_constraint_module_generation_authorization_post_dryrun_review_policy",
        "governance_constraint_module_generation_authorization_post_dryrun_review_policy_v1.json",
    ),
    ("authorization_dryrun_completeness_review", "authorization_dryrun_completeness_review_v1.json"),
    ("authorization_request_non_sent_review", "authorization_request_non_sent_review_v1.json"),
    ("authorization_grant_non_issued_review", "authorization_grant_non_issued_review_v1.json"),
    (
        "source_set_final_approval_non_execution_review",
        "source_set_final_approval_non_execution_review_v1.json",
    ),
    ("domain_preservation_non_approval_review", "domain_preservation_non_approval_review_v1.json"),
    ("generation_authority_non_release_review", "generation_authority_non_release_review_v1.json"),
    (
        "future_integration_boundary_non_confirmation_review",
        "future_integration_boundary_non_confirmation_review_v1.json",
    ),
    (
        "post_generation_review_non_execution_review",
        "post_generation_review_non_execution_review_v1.json",
    ),
    (
        "abort_rollback_authority_non_confirmation_review",
        "abort_rollback_authority_non_confirmation_review_v1.json",
    ),
    ("authorization_non_claims_review", "authorization_non_claims_review_v1.json"),
    (
        "governance_constraint_module_generation_authorization_post_dryrun_review_readiness_decision",
        "governance_constraint_module_generation_authorization_post_dryrun_review_readiness_decision_v1.json",
    ),
)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run Governance Constraint Module Generation Authorization Post-DryRun Review v1"
    )
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument(
        "--governance-constraint-module-generation-authorization-dryrun-root",
        default=str(DEFAULT_DRYRUN_ROOT),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_root = Path(args.output_root)
    result = run_governance_constraint_module_generation_authorization_post_dryrun_review_v1(
        governance_constraint_module_generation_authorization_dryrun_root=args.governance_constraint_module_generation_authorization_dryrun_root,
    )
    for key, filename in OUTPUT_FILES:
        _write_json(output_root / filename, result[key])

    summary = result["summary"]
    print(
        json.dumps(
            {
                "phase": summary.get("phase"),
                "boundary_ok": summary.get("boundary_ok"),
                "final_decision": summary.get("final_decision"),
                "recommended_next_phase": summary.get("recommended_next_phase"),
                "violations": summary.get("violations"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
