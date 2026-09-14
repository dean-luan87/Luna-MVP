#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Governance Constraint Module Generation Authorization Request Planning v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.governance_constraint_module_generation_authorization_request_planning_v1 import (
    run_governance_constraint_module_generation_authorization_request_planning_v1,
)

DEFAULT_OUTPUT_ROOT = (
    REPO_ROOT / "_eval_out" / "governance_constraint_module_generation_authorization_request_planning_v1_smoke_v0"
)
DEFAULT_ROADMAP_ROOT = (
    REPO_ROOT / "_eval_out" / "governance_constraint_module_generation_authorization_roadmap_decision_v1_smoke_v0"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("authorization_request_planning_policy", "authorization_request_planning_policy_v1.json"),
    ("authorization_request_identity_planning", "authorization_request_identity_planning_v1.json"),
    (
        "authorization_request_source_set_binding_planning",
        "authorization_request_source_set_binding_planning_v1.json",
    ),
    (
        "authorization_request_domain_preservation_binding_planning",
        "authorization_request_domain_preservation_binding_planning_v1.json",
    ),
    (
        "authorization_request_scope_and_exclusion_planning",
        "authorization_request_scope_and_exclusion_planning_v1.json",
    ),
    (
        "authorization_request_non_grant_and_non_generation_statement_planning",
        "authorization_request_non_grant_and_non_generation_statement_planning_v1.json",
    ),
    ("authorization_request_lifecycle_planning", "authorization_request_lifecycle_planning_v1.json"),
    (
        "authorization_request_review_requirement_planning",
        "authorization_request_review_requirement_planning_v1.json",
    ),
    (
        "authorization_request_abort_revoke_linkage_planning",
        "authorization_request_abort_revoke_linkage_planning_v1.json",
    ),
    ("authorization_request_verifier_usage_planning", "authorization_request_verifier_usage_planning_v1.json"),
    (
        "authorization_request_planning_non_claims_planning",
        "authorization_request_planning_non_claims_planning_v1.json",
    ),
    (
        "authorization_request_planning_readiness_decision",
        "authorization_request_planning_readiness_decision_v1.json",
    ),
)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run Governance Constraint Module Generation Authorization Request Planning v1"
    )
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument(
        "--governance-constraint-module-generation-authorization-roadmap-decision-root",
        default=str(DEFAULT_ROADMAP_ROOT),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_root = Path(args.output_root)
    result = run_governance_constraint_module_generation_authorization_request_planning_v1(
        governance_constraint_module_generation_authorization_roadmap_decision_root=args.governance_constraint_module_generation_authorization_roadmap_decision_root,
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
