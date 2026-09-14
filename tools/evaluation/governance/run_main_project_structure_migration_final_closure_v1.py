#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Main Project Structure Migration Final Closure v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.main_project_structure_migration_final_closure_v1 import (
    run_main_project_structure_migration_final_closure_v1,
)

DEFAULT_OUTPUT_ROOT = REPO_ROOT / "_eval_out" / "main_project_structure_migration_final_closure_v1_smoke_v0"
DEFAULT_B7_REVIEW_ROOT = REPO_ROOT / "_eval_out" / "main_project_structure_migration_b7_final_closure_review_v1_smoke_v0"

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("main_structure_migration_final_closure_policy", "main_structure_migration_final_closure_policy_v1.json"),
    ("b0_b7_batch_closure_matrix", "b0_b7_batch_closure_matrix_v1.json"),
    ("reusable_harness_contract_final_review", "reusable_harness_contract_final_review_v1.json"),
    ("anti_recursion_rule_final_review", "anti_recursion_rule_final_review_v1.json"),
    ("migration_operation_boundary_final_review", "migration_operation_boundary_final_review_v1.json"),
    ("global_consistency_final_review", "global_consistency_final_review_v1.json"),
    ("low_severity_candidate_final_register", "low_severity_candidate_final_register_v1.json"),
    ("deferred_refactor_candidate_register", "deferred_refactor_candidate_register_v1.json"),
    ("post_migration_engineering_resume_readiness", "post_migration_engineering_resume_readiness_v1.json"),
    ("main_structure_migration_final_non_claims_register", "main_structure_migration_final_non_claims_register_v1.json"),
    ("main_structure_migration_final_closure_decision", "main_structure_migration_final_closure_decision_v1.json"),
)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    p.add_argument("--b7-final-closure-review-root", default=str(DEFAULT_B7_REVIEW_ROOT))
    p.add_argument("--eval-out-base", default=None)
    return p.parse_args()


def main() -> int:
    args = parse_args()
    b7_root = Path(args.b7_final_closure_review_root)
    eval_base = args.eval_out_base or str(b7_root.parent)
    result = run_main_project_structure_migration_final_closure_v1(
        b7_final_closure_review_root=args.b7_final_closure_review_root,
        eval_out_base=eval_base,
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
                "batch_closure_matrix_pass": summary.get("batch_closure_matrix_pass"),
                "migration_chain_closed_now": summary.get("migration_chain_closed_now"),
                "ready_to_resume_engineering_mainline": summary.get("ready_to_resume_engineering_mainline"),
                "final_decision": summary.get("final_decision"),
                "recommended_next_phase": summary.get("recommended_next_phase"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
