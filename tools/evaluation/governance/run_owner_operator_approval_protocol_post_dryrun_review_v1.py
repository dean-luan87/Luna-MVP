#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Owner/Operator Approval Protocol Post-DryRun Review v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.owner_operator_approval_protocol_post_dryrun_review_v1 import (
    run_owner_operator_approval_protocol_post_dryrun_review_v1,
)

DEFAULT_OUTPUT_ROOT = (
    REPO_ROOT / "_eval_out" / "owner_operator_approval_protocol_post_dryrun_review_v1_smoke_v0"
)
DEFAULT_DRYRUN_ROOT = REPO_ROOT / "_eval_out" / "owner_operator_approval_protocol_dryrun_v1_smoke_v0"

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("owner_operator_post_dryrun_review_policy", "owner_operator_post_dryrun_review_policy_v1.json"),
    ("owner_operator_dryrun_completeness_review", "owner_operator_dryrun_completeness_review_v1.json"),
    ("owner_approval_request_block_review", "owner_approval_request_block_review_v1.json"),
    ("operator_acknowledgement_request_block_review", "operator_acknowledgement_request_block_review_v1.json"),
    ("execution_window_block_review", "execution_window_block_review_v1.json"),
    ("abort_authority_block_review", "abort_authority_block_review_v1.json"),
    (
        "scope_boundary_acknowledgement_block_review",
        "scope_boundary_acknowledgement_block_review_v1.json",
    ),
    ("authorization_grant_block_review", "authorization_grant_block_review_v1.json"),
    ("evidence_authorization_link_block_review", "evidence_authorization_link_block_review_v1.json"),
    ("owner_operator_forbidden_shortcut_review", "owner_operator_forbidden_shortcut_review_v1.json"),
    (
        "owner_operator_verifier_non_modification_review",
        "owner_operator_verifier_non_modification_review_v1.json",
    ),
    ("owner_operator_non_claims_non_write_review", "owner_operator_non_claims_non_write_review_v1.json"),
    (
        "owner_operator_post_dryrun_review_readiness_decision",
        "owner_operator_post_dryrun_review_readiness_decision_v1.json",
    ),
)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Owner/Operator Approval Protocol Post-DryRun Review v1")
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument(
        "--owner-operator-approval-protocol-dryrun-root",
        default=str(DEFAULT_DRYRUN_ROOT),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_root = Path(args.output_root)
    result = run_owner_operator_approval_protocol_post_dryrun_review_v1(
        owner_operator_approval_protocol_dryrun_root=args.owner_operator_approval_protocol_dryrun_root,
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
