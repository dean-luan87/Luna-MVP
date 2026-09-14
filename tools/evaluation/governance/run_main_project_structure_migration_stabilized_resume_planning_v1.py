#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Main Project Structure Migration Stabilized Resume Planning v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.main_project_structure_migration_stabilized_resume_planning_v1 import (
    run_main_project_structure_migration_stabilized_resume_planning_v1,
)

DEFAULT_OUTPUT = REPO_ROOT / "_eval_out" / "main_project_structure_migration_stabilized_resume_planning_v1_smoke_v0"
DEFAULT_RETURN = REPO_ROOT / "_eval_out" / "return_to_registry_generation_authorization_planning_v1_smoke_v0"
DEFAULT_CLOSURE = REPO_ROOT / "_eval_out" / "governance_constraint_module_branch_closure_v1_smoke_v0"

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("stabilized_resume_policy", "stabilized_resume_policy_v1.json"),
    ("governance_branch_closure_input_review", "governance_branch_closure_input_review_v1.json"),
    ("main_structure_migration_chain_status_review", "main_structure_migration_chain_status_review_v1.json"),
    ("target_project_structure_stability_policy", "target_project_structure_stability_policy_v1.json"),
    ("migration_batch_resume_matrix", "migration_batch_resume_matrix_v1.json"),
    ("protected_asset_and_forbidden_operation_matrix", "protected_asset_and_forbidden_operation_matrix_v1.json"),
    ("test_and_verifier_resume_plan", "test_and_verifier_resume_plan_v1.json"),
    ("rollback_rehearsal_resume_requirement", "rollback_rehearsal_resume_requirement_v1.json"),
    ("minimized_future_phase_template_policy", "minimized_future_phase_template_policy_v1.json"),
    ("stabilized_resume_readiness_decision", "stabilized_resume_readiness_decision_v1.json"),
)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=str(DEFAULT_OUTPUT))
    p.add_argument("--return-to-registry-generation-authorization-planning-root", default=str(DEFAULT_RETURN))
    p.add_argument("--governance-constraint-module-branch-closure-root", default=str(DEFAULT_CLOSURE))
    return p.parse_args()


def main() -> int:
    args = parse_args()
    result = run_main_project_structure_migration_stabilized_resume_planning_v1(
        return_to_registry_generation_authorization_planning_root=args.return_to_registry_generation_authorization_planning_root,
        governance_constraint_module_branch_closure_root=args.governance_constraint_module_branch_closure_root,
    )
    root = Path(args.output_root)
    for key, filename in OUTPUT_FILES:
        _write_json(root / filename, result[key])
    s = result["summary"]
    print(json.dumps({"phase": s.get("phase"), "boundary_ok": s.get("boundary_ok"), "final_decision": s.get("final_decision"), "recommended_next_phase": s.get("recommended_next_phase"), "violations": s.get("violations")}, ensure_ascii=False))
    return 0 if s.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
