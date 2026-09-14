#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Owner/Operator Approval Protocol Planning v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.owner_operator_approval_protocol_planning_v1 import (
    run_owner_operator_approval_protocol_planning_v1,
)

DEFAULT_OUTPUT_ROOT = REPO_ROOT / "_eval_out" / "owner_operator_approval_protocol_planning_v1_smoke_v0"
DEFAULT_ROADMAP_ROOT = (
    REPO_ROOT / "_eval_out" / "evidence_chain_governance_roadmap_decision_v1_smoke_v0"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    (
        "owner_operator_approval_protocol_planning_policy",
        "owner_operator_approval_protocol_planning_policy_v1.json",
    ),
    ("owner_approval_identity_planning_matrix", "owner_approval_identity_planning_matrix_v1.json"),
    ("operator_acknowledgement_planning_matrix", "operator_acknowledgement_planning_matrix_v1.json"),
    ("execution_window_planning_matrix", "execution_window_planning_matrix_v1.json"),
    ("abort_authority_planning_matrix", "abort_authority_planning_matrix_v1.json"),
    (
        "scope_boundary_acknowledgement_planning_matrix",
        "scope_boundary_acknowledgement_planning_matrix_v1.json",
    ),
    (
        "authorization_dependency_planning_matrix",
        "authorization_dependency_planning_matrix_v1.json",
    ),
    ("owner_operator_forbidden_shortcut_matrix", "owner_operator_forbidden_shortcut_matrix_v1.json"),
    (
        "owner_operator_evidence_authorization_link_matrix",
        "owner_operator_evidence_authorization_link_matrix_v1.json",
    ),
    (
        "owner_operator_verifier_usage_planning_matrix",
        "owner_operator_verifier_usage_planning_matrix_v1.json",
    ),
    ("owner_operator_non_claims_planning_matrix", "owner_operator_non_claims_planning_matrix_v1.json"),
    ("owner_operator_protocol_output_plan", "owner_operator_protocol_output_plan_v1.json"),
    (
        "owner_operator_approval_protocol_planning_readiness_decision",
        "owner_operator_approval_protocol_planning_readiness_decision_v1.json",
    ),
)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Owner/Operator Approval Protocol Planning v1")
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument(
        "--evidence-chain-governance-roadmap-decision-root",
        default=str(DEFAULT_ROADMAP_ROOT),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_root = Path(args.output_root)
    result = run_owner_operator_approval_protocol_planning_v1(
        evidence_chain_governance_roadmap_decision_root=args.evidence_chain_governance_roadmap_decision_root,
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
