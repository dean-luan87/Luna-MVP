#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Main Project Structure Migration Stabilized Execution Planning v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.main_project_structure_migration_stabilized_execution_planning_v1 import (
    run_main_project_structure_migration_stabilized_execution_planning_v1,
)

DEFAULT_OUTPUT = (
    REPO_ROOT / "_eval_out" / "main_project_structure_migration_stabilized_execution_planning_v1_smoke_v0"
)
DEFAULT_RESUME = (
    REPO_ROOT / "_eval_out" / "main_project_structure_migration_stabilized_resume_planning_v1_smoke_v0"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("stabilized_execution_planning_policy", "stabilized_execution_planning_policy_v1.json"),
    ("resume_planning_input_review", "resume_planning_input_review_v1.json"),
    ("b0_b7_execution_batch_plan", "b0_b7_execution_batch_plan_v1.json"),
    ("batch_pre_gate_matrix", "batch_pre_gate_matrix_v1.json"),
    ("batch_before_after_manifest_plan", "batch_before_after_manifest_plan_v1.json"),
    ("batch_rollback_route_plan", "batch_rollback_route_plan_v1.json"),
    ("batch_verifier_rerun_plan", "batch_verifier_rerun_plan_v1.json"),
    ("batch_protected_asset_guard_matrix", "batch_protected_asset_guard_matrix_v1.json"),
    ("batch_eval_out_readonly_guard", "batch_eval_out_readonly_guard_v1.json"),
    ("batch_domain_isolation_matrix", "batch_domain_isolation_matrix_v1.json"),
    ("batch_abort_condition_matrix", "batch_abort_condition_matrix_v1.json"),
    ("stabilized_execution_planning_readiness_decision", "stabilized_execution_planning_readiness_decision_v1.json"),
)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=str(DEFAULT_OUTPUT))
    p.add_argument("--stabilized-resume-planning-root", default=str(DEFAULT_RESUME))
    return p.parse_args()


def main() -> int:
    args = parse_args()
    result = run_main_project_structure_migration_stabilized_execution_planning_v1(
        stabilized_resume_planning_root=args.stabilized_resume_planning_root,
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
                "final_decision": s.get("final_decision"),
                "recommended_next_phase": s.get("recommended_next_phase"),
                "violations": s.get("violations"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if s.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
