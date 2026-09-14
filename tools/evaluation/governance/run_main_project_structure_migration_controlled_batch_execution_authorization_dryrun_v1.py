#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Main Project Structure Migration Controlled Batch Execution Authorization DryRun v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.main_project_structure_migration_controlled_batch_execution_authorization_dryrun_v1 import (
    run_main_project_structure_migration_controlled_batch_execution_authorization_dryrun_v1,
)

DEFAULT_OUTPUT = (
    REPO_ROOT
    / "_eval_out"
    / "main_project_structure_migration_controlled_batch_execution_authorization_dryrun_v1_smoke_v0"
)
DEFAULT_PLANNING = (
    REPO_ROOT
    / "_eval_out"
    / "main_project_structure_migration_controlled_batch_execution_authorization_planning_v1_smoke_v0"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("controlled_batch_execution_authorization_dryrun_policy", "controlled_batch_execution_authorization_dryrun_policy_v1.json"),
    ("controlled_batch_execution_authorization_planning_input_review", "controlled_batch_execution_authorization_planning_input_review_v1.json"),
    ("b0_b7_controlled_execution_authorization_scope_dryrun", "b0_b7_controlled_execution_authorization_scope_dryrun_v1.json"),
    ("controlled_execution_authorization_request_schema_dryrun", "controlled_execution_authorization_request_schema_dryrun_v1.json"),
    ("controlled_execution_authorization_grant_schema_dryrun", "controlled_execution_authorization_grant_schema_dryrun_v1.json"),
    ("controlled_execution_precondition_gate_dryrun", "controlled_execution_precondition_gate_dryrun_v1.json"),
    ("controlled_execution_window_dryrun", "controlled_execution_window_dryrun_v1.json"),
    ("controlled_execution_file_operation_allowlist_dryrun", "controlled_execution_file_operation_allowlist_dryrun_v1.json"),
    ("controlled_execution_file_operation_blocklist_dryrun", "controlled_execution_file_operation_blocklist_dryrun_v1.json"),
    ("controlled_execution_verifier_rerun_plan_dryrun", "controlled_execution_verifier_rerun_plan_dryrun_v1.json"),
    ("controlled_execution_rollback_rehearsal_requirement_dryrun", "controlled_execution_rollback_rehearsal_requirement_dryrun_v1.json"),
    ("controlled_execution_abort_condition_dryrun", "controlled_execution_abort_condition_dryrun_v1.json"),
    ("controlled_execution_post_migration_test_plan_dryrun", "controlled_execution_post_migration_test_plan_dryrun_v1.json"),
    ("controlled_execution_non_claims_dryrun", "controlled_execution_non_claims_dryrun_v1.json"),
    ("controlled_batch_execution_authorization_dryrun_readiness_decision", "controlled_batch_execution_authorization_dryrun_readiness_decision_v1.json"),
)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=str(DEFAULT_OUTPUT))
    p.add_argument("--controlled-batch-execution-authorization-planning-root", default=str(DEFAULT_PLANNING))
    return p.parse_args()


def main() -> int:
    args = parse_args()
    result = run_main_project_structure_migration_controlled_batch_execution_authorization_dryrun_v1(
        controlled_batch_execution_authorization_planning_root=args.controlled_batch_execution_authorization_planning_root,
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
                "standard_eval_out_write_pending_on_local_repro": s.get("standard_eval_out_write_pending_on_local_repro"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if s.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())

