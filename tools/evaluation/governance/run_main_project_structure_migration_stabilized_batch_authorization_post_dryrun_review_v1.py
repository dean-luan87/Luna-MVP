#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Main Project Structure Migration Stabilized Batch Authorization Post-DryRun Review v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.main_project_structure_migration_stabilized_batch_authorization_post_dryrun_review_v1 import (
    run_main_project_structure_migration_stabilized_batch_authorization_post_dryrun_review_v1,
)

DEFAULT_OUTPUT = (
    REPO_ROOT
    / "_eval_out"
    / "main_project_structure_migration_stabilized_batch_authorization_post_dryrun_review_v1_smoke_v0"
)
DEFAULT_DRYRUN = (
    REPO_ROOT
    / "_eval_out"
    / "main_project_structure_migration_stabilized_batch_authorization_dryrun_v1_smoke_v0"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("stabilized_batch_authorization_post_dryrun_review_policy", "stabilized_batch_authorization_post_dryrun_review_policy_v1.json"),
    ("batch_authorization_dryrun_input_review", "batch_authorization_dryrun_input_review_v1.json"),
    ("b0_b7_authorization_scope_review", "b0_b7_authorization_scope_review_v1.json"),
    ("batch_authorization_request_non_sent_review", "batch_authorization_request_non_sent_review_v1.json"),
    ("batch_authorization_grant_non_issued_review", "batch_authorization_grant_non_issued_review_v1.json"),
    ("batch_arming_non_execution_review", "batch_arming_non_execution_review_v1.json"),
    ("batch_execution_window_non_open_review", "batch_execution_window_non_open_review_v1.json"),
    ("batch_verifier_rerun_non_execution_review", "batch_verifier_rerun_non_execution_review_v1.json"),
    ("batch_rollback_non_execution_review", "batch_rollback_non_execution_review_v1.json"),
    ("batch_file_operation_non_execution_review", "batch_file_operation_non_execution_review_v1.json"),
    ("batch_protected_eval_out_guard_review", "batch_protected_eval_out_guard_review_v1.json"),
    ("batch_authorization_non_claims_review", "batch_authorization_non_claims_review_v1.json"),
    ("stabilized_batch_authorization_post_dryrun_review_readiness_decision", "stabilized_batch_authorization_post_dryrun_review_readiness_decision_v1.json"),
)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=str(DEFAULT_OUTPUT))
    p.add_argument("--stabilized-batch-authorization-dryrun-root", default=str(DEFAULT_DRYRUN))
    return p.parse_args()


def main() -> int:
    args = parse_args()
    result = run_main_project_structure_migration_stabilized_batch_authorization_post_dryrun_review_v1(
        stabilized_batch_authorization_dryrun_root=args.stabilized_batch_authorization_dryrun_root,
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

