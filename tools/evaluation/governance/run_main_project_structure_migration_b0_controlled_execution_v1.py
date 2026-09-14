#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Main Project Structure Migration B0 Controlled Execution v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.main_project_structure_migration_b0_controlled_execution_v1 import (
    run_main_project_structure_migration_b0_controlled_execution_v1,
)

DEFAULT_OUTPUT_ROOT = REPO_ROOT / "_eval_out" / "main_project_structure_migration_b0_controlled_execution_v1_smoke_v0"
DEFAULT_PREFLIGHT_ROOT = REPO_ROOT / "_eval_out" / "main_project_structure_migration_b0_preflight_via_harness_v1_smoke_v0"

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("b0_controlled_execution_policy", "b0_controlled_execution_policy_v1.json"),
    ("b0_preflight_input_review", "b0_preflight_input_review_v1.json"),
    ("b0_before_manifest", "b0_before_manifest_v1.json"),
    ("b0_execution_operation_plan", "b0_execution_operation_plan_v1.json"),
    ("b0_execution_operation_trace", "b0_execution_operation_trace_v1.json"),
    ("b0_after_manifest", "b0_after_manifest_v1.json"),
    ("b0_path_mapping_result", "b0_path_mapping_result_v1.json"),
    ("b0_blocked_operation_assertion", "b0_blocked_operation_assertion_v1.json"),
    ("b0_protected_eval_out_guard_execution_result", "b0_protected_eval_out_guard_execution_result_v1.json"),
    ("b0_runtime_refactor_block_execution_result", "b0_runtime_refactor_block_execution_result_v1.json"),
    ("b0_execution_abort_check_result", "b0_execution_abort_check_result_v1.json"),
    ("b0_execution_readiness_for_post_migration_review", "b0_execution_readiness_for_post_migration_review_v1.json"),
)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    p.add_argument("--b0-preflight-via-harness-root", default=str(DEFAULT_PREFLIGHT_ROOT))
    p.add_argument("--repo-root", default=str(REPO_ROOT))
    return p.parse_args()


def main() -> int:
    args = parse_args()
    result = run_main_project_structure_migration_b0_controlled_execution_v1(
        b0_preflight_via_harness_root=args.b0_preflight_via_harness_root,
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
                "b0_execution_completed_now": summary.get("b0_execution_completed_now"),
                "operations_unchanged": summary.get("operations_unchanged"),
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
