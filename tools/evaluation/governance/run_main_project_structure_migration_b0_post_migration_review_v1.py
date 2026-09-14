#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Main Project Structure Migration B0 Post-Migration Review v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.main_project_structure_migration_b0_post_migration_review_v1 import (
    run_main_project_structure_migration_b0_post_migration_review_v1,
)

DEFAULT_OUTPUT_ROOT = REPO_ROOT / "_eval_out" / "main_project_structure_migration_b0_post_migration_review_v1_smoke_v0"
DEFAULT_EXECUTION_ROOT = REPO_ROOT / "_eval_out" / "main_project_structure_migration_b0_controlled_execution_v1_smoke_v0"

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("b0_post_migration_review_policy", "b0_post_migration_review_policy_v1.json"),
    ("b0_controlled_execution_input_review", "b0_controlled_execution_input_review_v1.json"),
    ("b0_before_after_manifest_review", "b0_before_after_manifest_review_v1.json"),
    ("b0_operation_trace_review", "b0_operation_trace_review_v1.json"),
    ("b0_stable_placement_review", "b0_stable_placement_review_v1.json"),
    ("b0_forbidden_operation_review", "b0_forbidden_operation_review_v1.json"),
    ("b0_protected_eval_out_guard_review", "b0_protected_eval_out_guard_review_v1.json"),
    ("b0_runtime_refactor_non_execution_review", "b0_runtime_refactor_non_execution_review_v1.json"),
    ("b0_content_rewrite_non_execution_review", "b0_content_rewrite_non_execution_review_v1.json"),
    ("b0_rollback_readiness_review", "b0_rollback_readiness_review_v1.json"),
    ("b0_post_migration_non_claims_register", "b0_post_migration_non_claims_register_v1.json"),
    ("b0_post_migration_review_readiness_decision", "b0_post_migration_review_readiness_decision_v1.json"),
)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    p.add_argument("--b0-controlled-execution-root", default=str(DEFAULT_EXECUTION_ROOT))
    return p.parse_args()


def main() -> int:
    args = parse_args()
    result = run_main_project_structure_migration_b0_post_migration_review_v1(
        b0_controlled_execution_root=args.b0_controlled_execution_root,
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
                "b0_closed_now": summary.get("b0_closed_now"),
                "ready_for_b1_preflight_via_harness": summary.get("ready_for_b1_preflight_via_harness"),
                "final_decision": summary.get("final_decision"),
                "recommended_next_phase": summary.get("recommended_next_phase"),
                "violations": summary.get("violations"),
                "source_path_mode": summary.get("source_path_mode"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
