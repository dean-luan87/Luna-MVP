#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Governance Constraint Module Branch Closure v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.governance_constraint_module_branch_closure_v1 import (
    run_governance_constraint_module_branch_closure_v1,
)

DEFAULT_OUTPUT_ROOT = REPO_ROOT / "_eval_out" / "governance_constraint_module_branch_closure_v1_smoke_v0"
DEFAULT_UPSTREAM_ROOT = (
    REPO_ROOT
    / "_eval_out"
    / "governance_constraint_module_generation_authorization_request_roadmap_decision_v1_smoke_v0"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    (
        "governance_constraint_module_branch_closure_policy",
        "governance_constraint_module_branch_closure_policy_v1.json",
    ),
    (
        "completed_governance_constraint_module_branch_chain_review",
        "completed_governance_constraint_module_branch_chain_review_v1.json",
    ),
    ("deferred_capability_register", "deferred_capability_register_v1.json"),
    ("source_pack_register", "source_pack_register_v1.json"),
    (
        "recursive_expansion_stop_decision",
        "recursive_expansion_stop_decision_v1.json",
    ),
    (
        "mainline_return_readiness_matrix",
        "mainline_return_readiness_matrix_v1.json",
    ),
    ("branch_non_release_matrix", "branch_non_release_matrix_v1.json"),
    (
        "branch_closure_non_claims_register",
        "branch_closure_non_claims_register_v1.json",
    ),
    (
        "governance_constraint_module_branch_closure_readiness_decision",
        "governance_constraint_module_branch_closure_readiness_decision_v1.json",
    ),
)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Governance Constraint Module Branch Closure v1")
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument(
        "--governance-constraint-module-generation-authorization-request-roadmap-decision-root",
        default=str(DEFAULT_UPSTREAM_ROOT),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_root = Path(args.output_root)
    result = run_governance_constraint_module_branch_closure_v1(
        governance_constraint_module_generation_authorization_request_roadmap_decision_root=args.governance_constraint_module_generation_authorization_request_roadmap_decision_root,
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
                "branch_closed_for_current_mainline": summary.get("branch_closed_for_current_mainline"),
                "artifact_generation_planning_continued_now": summary.get("artifact_generation_planning_continued_now"),
                "violations": summary.get("violations"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
