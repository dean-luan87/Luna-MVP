#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Main Project Structure Migration Stabilized Batch Authorization DryRun v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.main_project_structure_migration_stabilized_batch_authorization_dryrun_v1 import (
    run_main_project_structure_migration_stabilized_batch_authorization_dryrun_v1,
)

DEFAULT_OUTPUT = (
    REPO_ROOT
    / "_eval_out"
    / "main_project_structure_migration_stabilized_batch_authorization_dryrun_v1_smoke_v0"
)
DEFAULT_PLANNING = (
    REPO_ROOT
    / "_eval_out"
    / "main_project_structure_migration_stabilized_batch_authorization_planning_v1_smoke_v0"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("stabilized_batch_authorization_dryrun_policy", "stabilized_batch_authorization_dryrun_policy_v1.json"),
    ("batch_authorization_planning_input_review", "batch_authorization_planning_input_review_v1.json"),
    ("b0_b7_authorization_scope_dryrun", "b0_b7_authorization_scope_dryrun_v1.json"),
    ("batch_authorization_request_schema_dryrun", "batch_authorization_request_schema_dryrun_v1.json"),
    ("batch_authorization_grant_schema_dryrun", "batch_authorization_grant_schema_dryrun_v1.json"),
    ("batch_pre_authorization_gate_dryrun", "batch_pre_authorization_gate_dryrun_v1.json"),
    ("batch_execution_window_dryrun", "batch_execution_window_dryrun_v1.json"),
    ("batch_verifier_rerun_authorization_dryrun", "batch_verifier_rerun_authorization_dryrun_v1.json"),
    ("batch_rollback_authorization_dryrun", "batch_rollback_authorization_dryrun_v1.json"),
    ("batch_file_operation_permission_boundary_dryrun", "batch_file_operation_permission_boundary_dryrun_v1.json"),
    ("batch_protected_eval_out_guard_dryrun", "batch_protected_eval_out_guard_dryrun_v1.json"),
    ("batch_authorization_non_claims_dryrun", "batch_authorization_non_claims_dryrun_v1.json"),
    ("stabilized_batch_authorization_dryrun_readiness_decision", "stabilized_batch_authorization_dryrun_readiness_decision_v1.json"),
)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=str(DEFAULT_OUTPUT))
    p.add_argument("--stabilized-batch-authorization-planning-root", default=str(DEFAULT_PLANNING))
    return p.parse_args()


def main() -> int:
    args = parse_args()
    result = run_main_project_structure_migration_stabilized_batch_authorization_dryrun_v1(
        stabilized_batch_authorization_planning_root=args.stabilized_batch_authorization_planning_root,
    )
    root = Path(args.output_root)
    for key, filename in OUTPUT_FILES:
        _write_json(root / filename, result[key])
    s = result["summary"]
    print(
        json.dumps(
            {
                "phase": s.get("phase"),
                "boundary_ok": s.get("boundary_ok"),
                "final_decision": s.get("final_decision"),
                "recommended_next_phase": s.get("recommended_next_phase"),
                "violations": s.get("violations"),
                "source_path_mode": s.get("source_path_mode"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if s.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())

