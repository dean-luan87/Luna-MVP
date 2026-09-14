#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Main Project Structure Migration B0 Harness Adoption DryRun v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.main_project_structure_migration_b0_harness_adoption_dryrun_v1 import (
    run_main_project_structure_migration_b0_harness_adoption_dryrun_v1,
)

DEFAULT_OUTPUT_ROOT = (
    REPO_ROOT / "_eval_out" / "main_project_structure_migration_b0_harness_adoption_dryrun_v1_smoke_v0"
)
DEFAULT_PLANNING_ROOT = (
    REPO_ROOT / "_eval_out" / "main_project_structure_migration_b0_harness_adoption_planning_v1_smoke_v0"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("b0_harness_adoption_dryrun_policy", "b0_harness_adoption_dryrun_policy_v1.json"),
    ("b0_harness_adoption_planning_input_review", "b0_harness_adoption_planning_input_review_v1.json"),
    ("b0_batch_config_consumption_dryrun", "b0_batch_config_consumption_dryrun_v1.json"),
    ("b0_harness_preflight_check_binding_dryrun", "b0_harness_preflight_check_binding_dryrun_v1.json"),
    ("b0_scope_and_domain_isolation_dryrun", "b0_scope_and_domain_isolation_dryrun_v1.json"),
    ("b0_protected_eval_out_guard_dryrun", "b0_protected_eval_out_guard_dryrun_v1.json"),
    ("b0_file_operation_boundary_dryrun", "b0_file_operation_boundary_dryrun_v1.json"),
    ("b0_manifest_requirement_dryrun", "b0_manifest_requirement_dryrun_v1.json"),
    ("b0_rollback_requirement_dryrun", "b0_rollback_requirement_dryrun_v1.json"),
    ("b0_verifier_rerun_requirement_dryrun", "b0_verifier_rerun_requirement_dryrun_v1.json"),
    ("b0_post_migration_test_requirement_dryrun", "b0_post_migration_test_requirement_dryrun_v1.json"),
    ("b0_abort_condition_dryrun", "b0_abort_condition_dryrun_v1.json"),
    ("b0_migration_refactor_opportunity_scan_dryrun", "b0_migration_refactor_opportunity_scan_dryrun_v1.json"),
    ("b1_b7_harness_adoption_deferred_dryrun", "b1_b7_harness_adoption_deferred_dryrun_v1.json"),
    ("b0_harness_adoption_non_claims_dryrun", "b0_harness_adoption_non_claims_dryrun_v1.json"),
    ("b0_harness_adoption_dryrun_readiness_decision", "b0_harness_adoption_dryrun_readiness_decision_v1.json"),
)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    p.add_argument("--b0-harness-adoption-planning-root", default=str(DEFAULT_PLANNING_ROOT))
    return p.parse_args()


def main() -> int:
    args = parse_args()
    result = run_main_project_structure_migration_b0_harness_adoption_dryrun_v1(
        b0_harness_adoption_planning_root=args.b0_harness_adoption_planning_root,
    )
    out_root = Path(args.output_root)
    for key, filename in OUTPUT_FILES:
        _write_json(out_root / filename, result[key])

    summary = result["summary"]
    print(
        json.dumps(
            {
                "phase": summary.get("phase"),
                "boundary_ok": summary.get("boundary_ok"),
                "selected_batch_id": summary.get("selected_batch_id"),
                "final_decision": summary.get("final_decision"),
                "recommended_next_phase": summary.get("recommended_next_phase"),
                "violations": summary.get("violations"),
                "source_path_mode": summary.get("source_path_mode"),
                "standard_eval_out_write_pending_on_local_repro": summary.get("standard_eval_out_write_pending_on_local_repro"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())

