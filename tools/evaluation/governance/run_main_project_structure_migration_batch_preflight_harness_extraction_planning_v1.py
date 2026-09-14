#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Main Project Structure Migration Batch Preflight Harness Extraction Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.main_project_structure_migration_batch_preflight_harness_extraction_planning_v1 import (
    run_main_project_structure_migration_batch_preflight_harness_extraction_planning_v1,
)

DEFAULT_OUTPUT_ROOT = (
    REPO_ROOT
    / "_eval_out"
    / "main_project_structure_migration_batch_preflight_harness_extraction_planning_v1_smoke_v0"
)

DEFAULT_AUTH_POST_REVIEW = (
    REPO_ROOT
    / "_eval_out"
    / "main_project_structure_migration_controlled_batch_execution_authorization_post_dryrun_review_v1_smoke_v0"
)
DEFAULT_ARMING_POST_REVIEW = (
    REPO_ROOT
    / "_eval_out"
    / "main_project_structure_migration_controlled_batch_execution_arming_post_dryrun_review_v1_smoke_v0"
)
DEFAULT_B0_REQUEST_PLANNING = (
    REPO_ROOT
    / "_eval_out"
    / "main_project_structure_migration_controlled_batch_execution_b0_arming_request_planning_v1_smoke_v0"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("batch_preflight_harness_extraction_policy", "batch_preflight_harness_extraction_policy_v1.json"),
    ("reusable_preflight_check_inventory", "reusable_preflight_check_inventory_v1.json"),
    ("batch_config_schema_planning", "batch_config_schema_planning_v1.json"),
    ("batch_preflight_harness_interface_planning", "batch_preflight_harness_interface_planning_v1.json"),
    ("batch_preflight_output_contract_planning", "batch_preflight_output_contract_planning_v1.json"),
    ("batch_preflight_verifier_baseline_planning", "batch_preflight_verifier_baseline_planning_v1.json"),
    ("batch_specific_override_policy", "batch_specific_override_policy_v1.json"),
    ("b0_to_b7_harness_adoption_matrix", "b0_to_b7_harness_adoption_matrix_v1.json"),
    ("deprecated_repetitive_phase_pattern_register", "deprecated_repetitive_phase_pattern_register_v1.json"),
    ("batch_preflight_harness_extraction_readiness_decision", "batch_preflight_harness_extraction_readiness_decision_v1.json"),
)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    p.add_argument("--controlled-batch-exec-auth-post-review-root", default=str(DEFAULT_AUTH_POST_REVIEW))
    p.add_argument("--controlled-batch-exec-arming-post-review-root", default=str(DEFAULT_ARMING_POST_REVIEW))
    p.add_argument("--b0-arming-request-planning-root", default=str(DEFAULT_B0_REQUEST_PLANNING))
    return p.parse_args()


def main() -> int:
    args = parse_args()
    result = run_main_project_structure_migration_batch_preflight_harness_extraction_planning_v1(
        controlled_batch_exec_auth_post_review_root=args.controlled_batch_exec_auth_post_review_root,
        controlled_batch_exec_arming_post_review_root=args.controlled_batch_exec_arming_post_review_root,
        b0_arming_request_planning_root=args.b0_arming_request_planning_root,
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

