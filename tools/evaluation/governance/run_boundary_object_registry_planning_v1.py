#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Boundary Object Registry Planning v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.boundary_object_registry_planning_v1 import (
    run_boundary_object_registry_planning_v1,
)

DEFAULT_OUTPUT_ROOT = REPO_ROOT / "_eval_out" / "boundary_object_registry_planning_v1_smoke_v0"
DEFAULT_ROADMAP_ROOT = (
    REPO_ROOT / "_eval_out" / "owner_operator_approval_protocol_roadmap_decision_v1_smoke_v0"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("boundary_object_registry_planning_policy", "boundary_object_registry_planning_policy_v1.json"),
    ("boundary_object_category_planning_matrix", "boundary_object_category_planning_matrix_v1.json"),
    (
        "boundary_object_read_write_policy_planning_matrix",
        "boundary_object_read_write_policy_planning_matrix_v1.json",
    ),
    (
        "boundary_object_migration_policy_planning_matrix",
        "boundary_object_migration_policy_planning_matrix_v1.json",
    ),
    (
        "boundary_object_evidence_policy_planning_matrix",
        "boundary_object_evidence_policy_planning_matrix_v1.json",
    ),
    (
        "boundary_object_rollback_policy_planning_matrix",
        "boundary_object_rollback_policy_planning_matrix_v1.json",
    ),
    (
        "protected_and_blocked_object_planning_matrix",
        "protected_and_blocked_object_planning_matrix_v1.json",
    ),
    (
        "boundary_object_owner_operator_dependency_matrix",
        "boundary_object_owner_operator_dependency_matrix_v1.json",
    ),
    (
        "boundary_object_file_operation_policy_planning_matrix",
        "boundary_object_file_operation_policy_planning_matrix_v1.json",
    ),
    ("boundary_object_forbidden_shortcut_matrix", "boundary_object_forbidden_shortcut_matrix_v1.json"),
    (
        "boundary_object_verifier_usage_planning_matrix",
        "boundary_object_verifier_usage_planning_matrix_v1.json",
    ),
    ("boundary_object_non_claims_planning_matrix", "boundary_object_non_claims_planning_matrix_v1.json"),
    ("boundary_object_registry_output_plan", "boundary_object_registry_output_plan_v1.json"),
    (
        "boundary_object_registry_planning_readiness_decision",
        "boundary_object_registry_planning_readiness_decision_v1.json",
    ),
)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Boundary Object Registry Planning v1")
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument(
        "--owner-operator-approval-protocol-roadmap-decision-root",
        default=str(DEFAULT_ROADMAP_ROOT),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_root = Path(args.output_root)
    result = run_boundary_object_registry_planning_v1(
        owner_operator_approval_protocol_roadmap_decision_root=args.owner_operator_approval_protocol_roadmap_decision_root,
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
