#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Governance Constraint Module Generation Authorization Request Roadmap Decision v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.governance_constraint_module_generation_authorization_request_roadmap_decision_v1 import (
    run_governance_constraint_module_generation_authorization_request_roadmap_decision_v1,
)

DEFAULT_OUTPUT_ROOT = (
    REPO_ROOT
    / "_eval_out"
    / "governance_constraint_module_generation_authorization_request_roadmap_decision_v1_smoke_v0"
)
DEFAULT_POST_REVIEW_ROOT = (
    REPO_ROOT
    / "_eval_out"
    / "governance_constraint_module_generation_authorization_request_post_dryrun_review_v1_smoke_v0"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    (
        "authorization_request_roadmap_decision_policy",
        "authorization_request_roadmap_decision_policy_v1.json",
    ),
    (
        "completed_authorization_request_chain_review",
        "completed_authorization_request_chain_review_v1.json",
    ),
    (
        "authorization_request_roadmap_route_candidate_matrix",
        "authorization_request_roadmap_route_candidate_matrix_v1.json",
    ),
    (
        "authorization_request_artifact_generation_planning_dependency_matrix",
        "authorization_request_artifact_generation_planning_dependency_matrix_v1.json",
    ),
    (
        "authorization_request_artifact_generation_planning_scope",
        "authorization_request_artifact_generation_planning_scope_v1.json",
    ),
    (
        "authorization_request_roadmap_non_release_matrix",
        "authorization_request_roadmap_non_release_matrix_v1.json",
    ),
    (
        "authorization_request_artifact_entry_readiness_risk_matrix",
        "authorization_request_artifact_entry_readiness_risk_matrix_v1.json",
    ),
    (
        "authorization_request_roadmap_decision_non_claims_register",
        "authorization_request_roadmap_decision_non_claims_register_v1.json",
    ),
    (
        "authorization_request_roadmap_readiness_decision",
        "authorization_request_roadmap_readiness_decision_v1.json",
    ),
)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run Governance Constraint Module Generation Authorization Request Roadmap Decision v1"
    )
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument(
        "--governance-constraint-module-generation-authorization-request-post-dryrun-review-root",
        default=str(DEFAULT_POST_REVIEW_ROOT),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_root = Path(args.output_root)
    result = run_governance_constraint_module_generation_authorization_request_roadmap_decision_v1(
        governance_constraint_module_generation_authorization_request_post_dryrun_review_root=args.governance_constraint_module_generation_authorization_request_post_dryrun_review_root,
    )
    for key, filename in OUTPUT_FILES:
        _write_json(output_root / filename, result[key])

    summary = result["summary"]
    print(
        json.dumps(
            {
                "phase": summary.get("phase"),
                "boundary_ok": summary.get("boundary_ok"),
                "selected_route": summary.get("selected_route"),
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
