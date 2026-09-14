#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Registry Generation Authorization Planning v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.registry_generation_authorization_planning_v1 import (
    run_registry_generation_authorization_planning_v1,
)

DEFAULT_OUTPUT_ROOT = REPO_ROOT / "_eval_out" / "registry_generation_authorization_planning_v1_smoke_v0"
DEFAULT_RETURN_ROOT = REPO_ROOT / "_eval_out" / "return_to_registry_generation_authorization_planning_v1_smoke_v0"
DEFAULT_REGISTRY_ROADMAP_ROOT = (
    REPO_ROOT / "_eval_out" / "boundary_object_registry_generation_roadmap_decision_v1_smoke_v0"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    (
        "registry_generation_authorization_planning_policy",
        "registry_generation_authorization_planning_policy_v1.json",
    ),
    ("mainline_return_input_review", "mainline_return_input_review_v1.json"),
    (
        "registry_generation_authorization_request_schema_planning",
        "registry_generation_authorization_request_schema_planning_v1.json",
    ),
    (
        "registry_generation_authorization_grant_schema_planning",
        "registry_generation_authorization_grant_schema_planning_v1.json",
    ),
    (
        "registry_source_final_approval_authority_planning",
        "registry_source_final_approval_authority_planning_v1.json",
    ),
    (
        "registry_contamination_final_check_authority_planning",
        "registry_contamination_final_check_authority_planning_v1.json",
    ),
    (
        "registry_generation_authority_planning_matrix",
        "registry_generation_authority_planning_matrix_v1.json",
    ),
    (
        "registry_entry_generation_boundary_planning",
        "registry_entry_generation_boundary_planning_v1.json",
    ),
    (
        "registry_owner_operator_dependency_planning",
        "registry_owner_operator_dependency_planning_v1.json",
    ),
    ("registry_file_operation_block_planning", "registry_file_operation_block_planning_v1.json"),
    (
        "registry_generation_authorization_verifier_usage_planning",
        "registry_generation_authorization_verifier_usage_planning_v1.json",
    ),
    (
        "registry_generation_authorization_non_claims_planning",
        "registry_generation_authorization_non_claims_planning_v1.json",
    ),
    (
        "registry_generation_authorization_planning_readiness_decision",
        "registry_generation_authorization_planning_readiness_decision_v1.json",
    ),
)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Registry Generation Authorization Planning v1")
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument(
        "--return-to-registry-generation-authorization-planning-root",
        default=str(DEFAULT_RETURN_ROOT),
    )
    parser.add_argument(
        "--boundary-object-registry-generation-roadmap-decision-root",
        default=str(DEFAULT_REGISTRY_ROADMAP_ROOT),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_root = Path(args.output_root)
    result = run_registry_generation_authorization_planning_v1(
        return_to_registry_generation_authorization_planning_root=args.return_to_registry_generation_authorization_planning_root,
        boundary_object_registry_generation_roadmap_decision_root=args.boundary_object_registry_generation_roadmap_decision_root,
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
