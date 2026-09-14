#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Main Project Structure Migration Batch Preflight Harness Extraction Post-DryRun Review v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.main_project_structure_migration_batch_preflight_harness_extraction_post_dryrun_review_v1 import (
    run_main_project_structure_migration_batch_preflight_harness_extraction_post_dryrun_review_v1,
)

DEFAULT_OUTPUT_ROOT = (
    REPO_ROOT
    / "_eval_out"
    / "main_project_structure_migration_batch_preflight_harness_extraction_post_dryrun_review_v1_smoke_v0"
)
DEFAULT_DRYRUN_ROOT = (
    REPO_ROOT
    / "_eval_out"
    / "main_project_structure_migration_batch_preflight_harness_extraction_dryrun_v1_smoke_v0"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("batch_preflight_harness_extraction_post_dryrun_review_policy", "batch_preflight_harness_extraction_post_dryrun_review_policy_v1.json"),
    ("batch_preflight_harness_extraction_dryrun_input_review", "batch_preflight_harness_extraction_dryrun_input_review_v1.json"),
    ("reusable_preflight_check_inventory_review", "reusable_preflight_check_inventory_review_v1.json"),
    ("batch_config_schema_consumption_review", "batch_config_schema_consumption_review_v1.json"),
    ("batch_preflight_harness_interface_review", "batch_preflight_harness_interface_review_v1.json"),
    ("batch_preflight_output_contract_review", "batch_preflight_output_contract_review_v1.json"),
    ("batch_preflight_verifier_baseline_review", "batch_preflight_verifier_baseline_review_v1.json"),
    ("batch_specific_override_policy_review", "batch_specific_override_policy_review_v1.json"),
    ("b0_to_b7_harness_adoption_review", "b0_to_b7_harness_adoption_review_v1.json"),
    ("deprecated_repetitive_phase_pattern_review", "deprecated_repetitive_phase_pattern_review_v1.json"),
    ("migration_refactor_opportunity_scan_rule_review", "migration_refactor_opportunity_scan_rule_review_v1.json"),
    ("batch_preflight_harness_non_generation_review", "batch_preflight_harness_non_generation_review_v1.json"),
    ("batch_preflight_harness_extraction_non_claims_review", "batch_preflight_harness_extraction_non_claims_review_v1.json"),
    ("batch_preflight_harness_extraction_post_dryrun_review_readiness_decision", "batch_preflight_harness_extraction_post_dryrun_review_readiness_decision_v1.json"),
)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    p.add_argument("--batch-preflight-harness-extraction-dryrun-root", default=str(DEFAULT_DRYRUN_ROOT))
    return p.parse_args()


def main() -> int:
    args = parse_args()
    result = run_main_project_structure_migration_batch_preflight_harness_extraction_post_dryrun_review_v1(
        batch_preflight_harness_extraction_dryrun_root=args.batch_preflight_harness_extraction_dryrun_root,
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

