#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Main Project Structure Migration B0 Harness Adoption Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.main_project_structure_migration_b0_harness_adoption_planning_v1 import (
    run_main_project_structure_migration_b0_harness_adoption_planning_v1,
)

DEFAULT_OUTPUT_ROOT = (
    REPO_ROOT / "_eval_out" / "main_project_structure_migration_b0_harness_adoption_planning_v1_smoke_v0"
)
DEFAULT_POST_REVIEW_ROOT = (
    REPO_ROOT
    / "_eval_out"
    / "main_project_structure_migration_batch_preflight_harness_extraction_post_dryrun_review_v1_smoke_v0"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("b0_harness_adoption_planning_policy", "b0_harness_adoption_planning_policy_v1.json"),
    ("batch_preflight_harness_post_review_input_review", "batch_preflight_harness_post_review_input_review_v1.json"),
    ("b0_batch_config_planning", "b0_batch_config_planning_v1.json"),
    ("b0_harness_preflight_check_binding", "b0_harness_preflight_check_binding_v1.json"),
    ("b0_scope_and_domain_isolation_planning", "b0_scope_and_domain_isolation_planning_v1.json"),
    ("b0_protected_eval_out_guard_planning", "b0_protected_eval_out_guard_planning_v1.json"),
    ("b0_file_operation_boundary_planning", "b0_file_operation_boundary_planning_v1.json"),
    ("b0_manifest_requirement_planning", "b0_manifest_requirement_planning_v1.json"),
    ("b0_rollback_requirement_planning", "b0_rollback_requirement_planning_v1.json"),
    ("b0_verifier_rerun_requirement_planning", "b0_verifier_rerun_requirement_planning_v1.json"),
    ("b0_post_migration_test_requirement_planning", "b0_post_migration_test_requirement_planning_v1.json"),
    ("b0_abort_condition_planning", "b0_abort_condition_planning_v1.json"),
    ("b0_migration_refactor_opportunity_scan_planning", "b0_migration_refactor_opportunity_scan_planning_v1.json"),
    ("b1_b7_harness_adoption_deferred_matrix", "b1_b7_harness_adoption_deferred_matrix_v1.json"),
    ("b0_harness_adoption_non_claims_register", "b0_harness_adoption_non_claims_register_v1.json"),
    ("b0_harness_adoption_planning_readiness_decision", "b0_harness_adoption_planning_readiness_decision_v1.json"),
)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    p.add_argument("--batch-preflight-harness-extraction-post-review-root", default=str(DEFAULT_POST_REVIEW_ROOT))
    return p.parse_args()


def main() -> int:
    args = parse_args()
    result = run_main_project_structure_migration_b0_harness_adoption_planning_v1(
        batch_preflight_harness_extraction_post_review_root=args.batch_preflight_harness_extraction_post_review_root,
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

