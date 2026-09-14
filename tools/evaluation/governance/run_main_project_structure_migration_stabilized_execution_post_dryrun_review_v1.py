#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Main Project Structure Migration Stabilized Execution Post-DryRun Review v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.main_project_structure_migration_stabilized_execution_post_dryrun_review_v1 import (
    run_main_project_structure_migration_stabilized_execution_post_dryrun_review_v1,
)

DEFAULT_OUTPUT = (
    REPO_ROOT
    / "_eval_out"
    / "main_project_structure_migration_stabilized_execution_post_dryrun_review_v1_smoke_v0"
)
DEFAULT_DRYRUN = REPO_ROOT / "_eval_out" / "main_project_structure_migration_stabilized_execution_dryrun_v1_smoke_v0"

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("stabilized_execution_post_dryrun_review_policy", "stabilized_execution_post_dryrun_review_policy_v1.json"),
    ("execution_dryrun_input_review", "execution_dryrun_input_review_v1.json"),
    ("b0_b7_batch_trace_completeness_review", "b0_b7_batch_trace_completeness_review_v1.json"),
    ("batch_pre_gate_review", "batch_pre_gate_review_v1.json"),
    ("batch_manifest_review", "batch_manifest_review_v1.json"),
    ("batch_rollback_route_review", "batch_rollback_route_review_v1.json"),
    ("batch_verifier_rerun_non_execution_review", "batch_verifier_rerun_non_execution_review_v1.json"),
    ("batch_protected_asset_guard_review", "batch_protected_asset_guard_review_v1.json"),
    ("batch_eval_out_readonly_guard_review", "batch_eval_out_readonly_guard_review_v1.json"),
    ("batch_domain_isolation_review", "batch_domain_isolation_review_v1.json"),
    ("batch_abort_condition_review", "batch_abort_condition_review_v1.json"),
    ("file_operation_non_execution_review", "file_operation_non_execution_review_v1.json"),
    ("stabilized_execution_post_dryrun_review_readiness_decision", "stabilized_execution_post_dryrun_review_readiness_decision_v1.json"),
)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=str(DEFAULT_OUTPUT))
    p.add_argument("--stabilized-execution-dryrun-root", default=str(DEFAULT_DRYRUN))
    return p.parse_args()


def main() -> int:
    args = parse_args()
    result = run_main_project_structure_migration_stabilized_execution_post_dryrun_review_v1(
        stabilized_execution_dryrun_root=args.stabilized_execution_dryrun_root,
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
            },
            ensure_ascii=False,
        )
    )
    return 0 if s.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())

