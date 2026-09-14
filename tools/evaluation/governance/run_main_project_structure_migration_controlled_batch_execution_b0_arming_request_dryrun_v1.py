#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Main Project Structure Migration Controlled Batch Execution B0 Arming Request DryRun v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.main_project_structure_migration_controlled_batch_execution_b0_arming_request_dryrun_v1 import (
    run_main_project_structure_migration_controlled_batch_execution_b0_arming_request_dryrun_v1,
)

DEFAULT_OUTPUT = (
    REPO_ROOT
    / "_eval_out"
    / "main_project_structure_migration_controlled_batch_execution_b0_arming_request_dryrun_v1_smoke_v0"
)
DEFAULT_PLANNING = (
    REPO_ROOT
    / "_eval_out"
    / "main_project_structure_migration_controlled_batch_execution_b0_arming_request_planning_v1_smoke_v0"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("b0_arming_request_dryrun_policy", "b0_arming_request_dryrun_policy_v1.json"),
    ("b0_arming_request_planning_input_review", "b0_arming_request_planning_input_review_v1.json"),
    ("b0_arming_request_identity_dryrun", "b0_arming_request_identity_dryrun_v1.json"),
    ("b0_arming_request_scope_dryrun", "b0_arming_request_scope_dryrun_v1.json"),
    ("b0_arming_request_precondition_gate_dryrun", "b0_arming_request_precondition_gate_dryrun_v1.json"),
    ("b0_arming_request_forbidden_scope_dryrun", "b0_arming_request_forbidden_scope_dryrun_v1.json"),
    ("b0_arming_request_manifest_requirement_dryrun", "b0_arming_request_manifest_requirement_dryrun_v1.json"),
    ("b0_arming_request_rollback_requirement_dryrun", "b0_arming_request_rollback_requirement_dryrun_v1.json"),
    ("b0_arming_request_verifier_rerun_requirement_dryrun", "b0_arming_request_verifier_rerun_requirement_dryrun_v1.json"),
    ("b0_arming_request_post_migration_test_requirement_dryrun", "b0_arming_request_post_migration_test_requirement_dryrun_v1.json"),
    ("b0_arming_request_abort_revoke_dryrun", "b0_arming_request_abort_revoke_dryrun_v1.json"),
    ("b0_arming_request_non_claims_dryrun", "b0_arming_request_non_claims_dryrun_v1.json"),
    ("b0_arming_request_dryrun_readiness_decision", "b0_arming_request_dryrun_readiness_decision_v1.json"),
)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=str(DEFAULT_OUTPUT))
    p.add_argument("--b0-arming-request-planning-root", default=str(DEFAULT_PLANNING))
    return p.parse_args()


def main() -> int:
    args = parse_args()
    result = run_main_project_structure_migration_controlled_batch_execution_b0_arming_request_dryrun_v1(
        b0_arming_request_planning_root=args.b0_arming_request_planning_root,
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

