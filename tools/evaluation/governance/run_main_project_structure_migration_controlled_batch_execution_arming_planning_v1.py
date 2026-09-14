#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Main Project Structure Migration Controlled Batch Execution Arming Planning v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.main_project_structure_migration_controlled_batch_execution_arming_planning_v1 import (
    run_main_project_structure_migration_controlled_batch_execution_arming_planning_v1,
)

DEFAULT_OUTPUT = REPO_ROOT / "_eval_out" / "main_project_structure_migration_controlled_batch_execution_arming_planning_v1_smoke_v0"
DEFAULT_UPSTREAM = (
    REPO_ROOT
    / "_eval_out"
    / "main_project_structure_migration_controlled_batch_execution_authorization_post_dryrun_review_v1_smoke_v0"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("controlled_batch_execution_arming_planning_policy", "controlled_batch_execution_arming_planning_policy_v1.json"),
    ("controlled_execution_authorization_post_review_input_review", "controlled_execution_authorization_post_review_input_review_v1.json"),
    ("b0_single_batch_arming_scope", "b0_single_batch_arming_scope_v1.json"),
    ("b1_b7_deferred_arming_matrix", "b1_b7_deferred_arming_matrix_v1.json"),
    ("b0_execution_window_arming_plan", "b0_execution_window_arming_plan_v1.json"),
    ("b0_file_operation_allowlist_arming_plan", "b0_file_operation_allowlist_arming_plan_v1.json"),
    ("b0_file_operation_blocklist_arming_plan", "b0_file_operation_blocklist_arming_plan_v1.json"),
    ("b0_before_after_manifest_arming_plan", "b0_before_after_manifest_arming_plan_v1.json"),
    ("b0_rollback_route_arming_plan", "b0_rollback_route_arming_plan_v1.json"),
    ("b0_verifier_rerun_arming_plan", "b0_verifier_rerun_arming_plan_v1.json"),
    ("b0_post_migration_test_arming_plan", "b0_post_migration_test_arming_plan_v1.json"),
    ("b0_abort_condition_arming_plan", "b0_abort_condition_arming_plan_v1.json"),
    ("b0_protected_eval_out_guard_arming_plan", "b0_protected_eval_out_guard_arming_plan_v1.json"),
    ("controlled_batch_execution_arming_non_claims_register", "controlled_batch_execution_arming_non_claims_register_v1.json"),
    ("controlled_batch_execution_arming_planning_readiness_decision", "controlled_batch_execution_arming_planning_readiness_decision_v1.json"),
)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=str(DEFAULT_OUTPUT))
    p.add_argument("--controlled-batch-execution-authorization-post-dryrun-review-root", default=str(DEFAULT_UPSTREAM))
    return p.parse_args()


def main() -> int:
    args = parse_args()
    result = run_main_project_structure_migration_controlled_batch_execution_arming_planning_v1(
        controlled_batch_execution_authorization_post_dryrun_review_root=args.controlled_batch_execution_authorization_post_dryrun_review_root,
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
                "selected_batch_id": s.get("selected_batch_id"),
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

