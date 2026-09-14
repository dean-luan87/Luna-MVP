#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Vision / OCR / Navigation / Task Midplatform Recovery Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.vision_ocr_navigation_task_midplatform_recovery_planning_v1 import (
    run_vision_ocr_navigation_task_midplatform_recovery_planning_v1,
)

DEFAULT_OUTPUT_ROOT = (
    REPO_ROOT / "_eval_out" / "vision_ocr_navigation_task_midplatform_recovery_planning_v1_smoke_v0"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("recovery_planning_policy", "recovery_planning_policy_v1.json"),
    ("smoke_test_input_review", "smoke_test_input_review_v1.json"),
    ("p0_function_chain_inventory", "p0_function_chain_inventory_v1.json"),
    ("vision_recovery_scope_planning", "vision_recovery_scope_planning_v1.json"),
    ("ocr_recovery_scope_planning", "ocr_recovery_scope_planning_v1.json"),
    ("navigation_recovery_scope_planning", "navigation_recovery_scope_planning_v1.json"),
    ("task_midplatform_recovery_scope_planning", "task_midplatform_recovery_scope_planning_v1.json"),
    ("vision_ocr_navigation_task_dependency_matrix", "vision_ocr_navigation_task_dependency_matrix_v1.json"),
    ("recovery_runtime_boundary_matrix", "recovery_runtime_boundary_matrix_v1.json"),
    ("midplatform_structure_risk_register", "midplatform_structure_risk_register_v1.json"),
    ("recovery_phase_sequence_plan", "recovery_phase_sequence_plan_v1.json"),
    ("recovery_non_claims_register", "recovery_non_claims_register_v1.json"),
    ("recovery_planning_readiness_decision", "recovery_planning_readiness_decision_v1.json"),
)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--repo-root", default=str(REPO_ROOT))
    p.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    p.add_argument("--post-migration-engineering-smoke-test-root", required=True)
    return p.parse_args()


def main() -> int:
    args = parse_args()
    result = run_vision_ocr_navigation_task_midplatform_recovery_planning_v1(
        repo_root=args.repo_root,
        post_migration_engineering_smoke_test_root=args.post_migration_engineering_smoke_test_root,
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
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
