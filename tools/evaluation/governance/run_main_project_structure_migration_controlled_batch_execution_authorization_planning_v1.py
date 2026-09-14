#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Main Project Structure Migration Controlled Batch Execution Authorization Planning v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.main_project_structure_migration_controlled_batch_execution_authorization_planning_v1 import (
    run_main_project_structure_migration_controlled_batch_execution_authorization_planning_v1,
)

DEFAULT_OUTPUT = (
    REPO_ROOT
    / "_eval_out"
    / "main_project_structure_migration_controlled_batch_execution_authorization_planning_v1_smoke_v0"
)
DEFAULT_UPSTREAM = (
    REPO_ROOT
    / "_eval_out"
    / "main_project_structure_migration_stabilized_batch_authorization_post_dryrun_review_v1_smoke_v0"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("controlled_batch_execution_authorization_planning_policy", "controlled_batch_execution_authorization_planning_policy_v1.json"),
    ("batch_authorization_post_dryrun_review_input_review", "batch_authorization_post_dryrun_review_input_review_v1.json"),
    ("b0_b7_controlled_execution_authorization_scope_matrix", "b0_b7_controlled_execution_authorization_scope_matrix_v1.json"),
    ("controlled_execution_authorization_request_schema_planning", "controlled_execution_authorization_request_schema_planning_v1.json"),
    ("controlled_execution_authorization_grant_schema_planning", "controlled_execution_authorization_grant_schema_planning_v1.json"),
    ("controlled_execution_precondition_gate_matrix", "controlled_execution_precondition_gate_matrix_v1.json"),
    ("controlled_execution_window_planning", "controlled_execution_window_planning_v1.json"),
    ("controlled_execution_file_operation_allowlist_planning", "controlled_execution_file_operation_allowlist_planning_v1.json"),
    ("controlled_execution_file_operation_blocklist_planning", "controlled_execution_file_operation_blocklist_planning_v1.json"),
    ("controlled_execution_verifier_rerun_plan", "controlled_execution_verifier_rerun_plan_v1.json"),
    ("controlled_execution_rollback_rehearsal_requirement", "controlled_execution_rollback_rehearsal_requirement_v1.json"),
    ("controlled_execution_abort_condition_matrix", "controlled_execution_abort_condition_matrix_v1.json"),
    ("controlled_execution_post_migration_test_plan", "controlled_execution_post_migration_test_plan_v1.json"),
    ("controlled_execution_non_claims_register", "controlled_execution_non_claims_register_v1.json"),
    ("controlled_batch_execution_authorization_planning_readiness_decision", "controlled_batch_execution_authorization_planning_readiness_decision_v1.json"),
)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=str(DEFAULT_OUTPUT))
    p.add_argument("--stabilized-batch-authorization-post-dryrun-review-root", default=str(DEFAULT_UPSTREAM))
    return p.parse_args()


def main() -> int:
    args = parse_args()
    result = run_main_project_structure_migration_controlled_batch_execution_authorization_planning_v1(
        stabilized_batch_authorization_post_dryrun_review_root=args.stabilized_batch_authorization_post_dryrun_review_root,
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

