#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Return To Registry Generation Authorization Planning v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.return_to_registry_generation_authorization_planning_v1 import (
    run_return_to_registry_generation_authorization_planning_v1,
)

DEFAULT_OUTPUT_ROOT = REPO_ROOT / "_eval_out" / "return_to_registry_generation_authorization_planning_v1_smoke_v0"
DEFAULT_UPSTREAM_ROOT = REPO_ROOT / "_eval_out" / "governance_constraint_module_branch_closure_v1_smoke_v0"

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    (
        "return_to_registry_generation_authorization_planning_policy",
        "return_to_registry_generation_authorization_planning_policy_v1.json",
    ),
    ("branch_closure_input_review", "branch_closure_input_review_v1.json"),
    (
        "deferred_governance_constraint_module_source_pack_reference",
        "deferred_governance_constraint_module_source_pack_reference_v1.json",
    ),
    ("mainline_resume_target_binding", "mainline_resume_target_binding_v1.json"),
    ("return_non_release_matrix", "return_non_release_matrix_v1.json"),
    (
        "registry_generation_authorization_planning_reentry_scope",
        "registry_generation_authorization_planning_reentry_scope_v1.json",
    ),
    (
        "return_to_mainline_non_claims_register",
        "return_to_mainline_non_claims_register_v1.json",
    ),
    (
        "return_to_registry_generation_authorization_planning_readiness_decision",
        "return_to_registry_generation_authorization_planning_readiness_decision_v1.json",
    ),
)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run Return To Registry Generation Authorization Planning v1"
    )
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument(
        "--governance-constraint-module-branch-closure-root",
        default=str(DEFAULT_UPSTREAM_ROOT),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_root = Path(args.output_root)
    result = run_return_to_registry_generation_authorization_planning_v1(
        governance_constraint_module_branch_closure_root=args.governance_constraint_module_branch_closure_root,
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
                "mainline_resume_target": summary.get("mainline_resume_target"),
                "violations": summary.get("violations"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
