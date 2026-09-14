#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Main Project Structure Migration B0 Preflight Via Harness v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.main_project_structure_migration_b0_preflight_via_harness_v1 import (
    run_main_project_structure_migration_b0_preflight_via_harness_v1,
)

DEFAULT_OUTPUT_ROOT = (
    REPO_ROOT / "_eval_out" / "main_project_structure_migration_b0_preflight_via_harness_v1_smoke_v0"
)
DEFAULT_CLOSURE_ROOT = (
    REPO_ROOT
    / "_eval_out"
    / "main_project_structure_migration_b0_harness_adoption_and_reusable_contract_closure_v1_smoke_v0"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("b0_preflight_via_harness_policy", "b0_preflight_via_harness_policy_v1.json"),
    ("reusable_harness_contract_input_review", "reusable_harness_contract_input_review_v1.json"),
    ("b0_batch_config_instance", "b0_batch_config_instance_v1.json"),
    ("b0_preflight_scope_check_result", "b0_preflight_scope_check_result_v1.json"),
    ("b0_preflight_domain_isolation_check_result", "b0_preflight_domain_isolation_check_result_v1.json"),
    ("b0_preflight_protected_guard_check_result", "b0_preflight_protected_guard_check_result_v1.json"),
    ("b0_preflight_eval_out_readonly_check_result", "b0_preflight_eval_out_readonly_check_result_v1.json"),
    ("b0_preflight_file_operation_boundary_check_result", "b0_preflight_file_operation_boundary_check_result_v1.json"),
    ("b0_preflight_manifest_requirement_check_result", "b0_preflight_manifest_requirement_check_result_v1.json"),
    ("b0_preflight_rollback_requirement_check_result", "b0_preflight_rollback_requirement_check_result_v1.json"),
    ("b0_preflight_verifier_rerun_requirement_check_result", "b0_preflight_verifier_rerun_requirement_check_result_v1.json"),
    ("b0_preflight_post_migration_test_requirement_check_result", "b0_preflight_post_migration_test_requirement_check_result_v1.json"),
    ("b0_preflight_abort_condition_check_result", "b0_preflight_abort_condition_check_result_v1.json"),
    ("b0_preflight_workspace_fallback_check_result", "b0_preflight_workspace_fallback_check_result_v1.json"),
    ("b0_preflight_non_claims_check_result", "b0_preflight_non_claims_check_result_v1.json"),
    ("b0_preflight_migration_refactor_opportunity_scan", "b0_preflight_migration_refactor_opportunity_scan_v1.json"),
    ("b0_preflight_result", "b0_preflight_result_v1.json"),
    ("b0_preflight_via_harness_readiness_decision", "b0_preflight_via_harness_readiness_decision_v1.json"),
)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    p.add_argument(
        "--b0-harness-adoption-and-reusable-contract-closure-root",
        default=str(DEFAULT_CLOSURE_ROOT),
    )
    p.add_argument("--repo-root", default=str(REPO_ROOT))
    return p.parse_args()


def main() -> int:
    args = parse_args()
    result = run_main_project_structure_migration_b0_preflight_via_harness_v1(
        b0_harness_adoption_and_reusable_contract_closure_root=args.b0_harness_adoption_and_reusable_contract_closure_root,
        repo_root=args.repo_root,
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
                "all_fixed_checks_pass": summary.get("all_fixed_checks_pass"),
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
