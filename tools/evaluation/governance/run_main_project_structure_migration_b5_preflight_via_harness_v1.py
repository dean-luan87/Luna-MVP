#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Main Project Structure Migration B5 Preflight Via Harness v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.main_project_structure_migration_b5_preflight_via_harness_v1 import (
    run_main_project_structure_migration_b5_preflight_via_harness_v1,
)

DEFAULT_OUTPUT_ROOT = REPO_ROOT / "_eval_out" / "main_project_structure_migration_b5_preflight_via_harness_v1_smoke_v0"
DEFAULT_B4_REVIEW_ROOT = REPO_ROOT / "_eval_out" / "main_project_structure_migration_b4_post_migration_review_v1_smoke_v0"

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("b5_batch_config", "b5_batch_config_v1.json"),
    ("b5_preflight_result", "b5_preflight_result_v1.json"),
    ("b5_schema_path_reference_consistency_scan", "b5_schema_path_reference_consistency_scan_v1.json"),
    ("b5_config_reference_consistency_scan", "b5_config_reference_consistency_scan_v1.json"),
    ("b5_migration_refactor_opportunity_scan", "b5_migration_refactor_opportunity_scan_v1.json"),
    ("b5_preflight_readiness_decision", "b5_preflight_readiness_decision_v1.json"),
)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    p.add_argument("--b4-post-migration-review-root", default=str(DEFAULT_B4_REVIEW_ROOT))
    p.add_argument("--repo-root", default=str(REPO_ROOT))
    return p.parse_args()


def main() -> int:
    args = parse_args()
    result = run_main_project_structure_migration_b5_preflight_via_harness_v1(
        b4_post_migration_review_root=args.b4_post_migration_review_root,
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
                "candidate_path_count": summary.get("candidate_path_count"),
                "configs_count": summary.get("configs_count"),
                "all_fixed_checks_pass": summary.get("all_fixed_checks_pass"),
                "hold_for_review": summary.get("hold_for_review"),
                "final_decision": summary.get("final_decision"),
                "recommended_next_phase": summary.get("recommended_next_phase"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
