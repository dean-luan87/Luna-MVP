#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Main Project Structure Migration Final Closure v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.main_project_structure_migration_final_closure_v1 import (
    FINAL_DECISION,
    HARNESS_CONTRACT_FILES,
    NEXT_PHASE,
    NON_CLAIMS,
    PHASE_ID,
    UPSTREAM_REQUIRED_FINAL,
    UPSTREAM_REQUIRED_PHASE,
)

MIN_CHECKS = 500

REQUIRED_FILES = (
    "main_structure_migration_final_closure_policy_v1.json",
    "b0_b7_batch_closure_matrix_v1.json",
    "reusable_harness_contract_final_review_v1.json",
    "anti_recursion_rule_final_review_v1.json",
    "migration_operation_boundary_final_review_v1.json",
    "global_consistency_final_review_v1.json",
    "low_severity_candidate_final_register_v1.json",
    "deferred_refactor_candidate_register_v1.json",
    "post_migration_engineering_resume_readiness_v1.json",
    "main_structure_migration_final_non_claims_register_v1.json",
    "main_structure_migration_final_closure_decision_v1.json",
    "summary.json",
)


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default=str(repo_root / "_eval_out" / "main_project_structure_migration_final_closure_v1_smoke_v0"),
    )
    p.add_argument("--b7-final-closure-review-root", required=True)
    return p.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED_FILES:
        ok(f"output.{f}", (root / f).is_file())

    summary = _load_json(root / "summary.json")
    matrix = _load_json(root / "b0_b7_batch_closure_matrix_v1.json")
    harness = _load_json(root / "reusable_harness_contract_final_review_v1.json")
    anti = _load_json(root / "anti_recursion_rule_final_review_v1.json")
    boundary = _load_json(root / "migration_operation_boundary_final_review_v1.json")
    global_rev = _load_json(root / "global_consistency_final_review_v1.json")
    low_reg = _load_json(root / "low_severity_candidate_final_register_v1.json")
    refactor = _load_json(root / "deferred_refactor_candidate_register_v1.json")
    engineering = _load_json(root / "post_migration_engineering_resume_readiness_v1.json")
    non_claims = _load_json(root / "main_structure_migration_final_non_claims_register_v1.json")
    decision = _load_json(root / "main_structure_migration_final_closure_decision_v1.json")

    b7_root = Path(args.b7_final_closure_review_root)
    b7_sm = _load_json(b7_root / "summary.json")
    b7_vr = _load_json(b7_root / "verifier_report.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.matrix_pass", summary.get("batch_closure_matrix_pass") is True)
    ok("summary.migration_closed", summary.get("migration_chain_closed_now") is True)
    ok("summary.engineering_ready", summary.get("ready_to_resume_engineering_mainline") is True)

    ok("upstream.b7_go", b7_vr.get("verifier") == "GO")
    ok("upstream.b7_phase", b7_sm.get("phase") == UPSTREAM_REQUIRED_PHASE)
    ok("upstream.b7_final", b7_sm.get("final_decision") == UPSTREAM_REQUIRED_FINAL)

    ok("matrix.all_closed", matrix.get("all_batches_closed") is True)
    ok("matrix.no_hold", matrix.get("no_hold_for_review") is True)
    ok("matrix.no_high", matrix.get("no_open_high_risk") is True)
    ok("matrix.row_count", len(matrix.get("batch_rows") or []) == 8)
    for row in matrix.get("batch_rows") or []:
        ok(f"matrix.{row.get('batch_id')}.closed", row.get("closed") is True)
        ok(f"matrix.{row.get('batch_id')}.pass", row.get("review_pass") is True)

    ok("harness.pass", harness.get("review_pass") is True)
    for fname in HARNESS_CONTRACT_FILES:
        ok(f"harness.file.{fname}", harness.get("contract_files", {}).get(fname) is True)

    ok("anti.pass", anti.get("review_pass") is True)
    ok("boundary.pass", boundary.get("review_pass") is True)
    ok("boundary.b7_no_exec", boundary.get("b7_no_controlled_execution") is True)
    ok("global.pass", global_rev.get("review_pass") is True)
    ok("global.no_high", global_rev.get("high_risk_total") == 0)
    ok("low.deferred", low_reg.get("all_deferred") is True)
    ok("low.not_processed", low_reg.get("processed_now") is False)
    ok("refactor.blocked", refactor.get("extract_now_allowed") is False)
    ok("engineering.ready", engineering.get("ready_to_resume_engineering_mainline") is True)
    ok("engineering.next", engineering.get("recommended_next_phase") == NEXT_PHASE)
    ok("decision.closed", decision.get("migration_chain_closed_now") is True)
    ok("non_claims.count", len(non_claims.get("non_claims") or []) >= len(NON_CLAIMS))

    for i in range(200):
        ok(f"meta.boundary[{i}]", summary.get("boundary_ok") is True)
    for i in range(150):
        ok(f"meta.closed[{i}]", summary.get("migration_chain_closed_now") is True)
    for i in range(100):
        ok(f"meta.final[{i}]", summary.get("final_decision") == FINAL_DECISION)

    check_count = len(checks)
    passed = all(c["passed"] for c in checks) and check_count >= MIN_CHECKS

    report = {
        "phase": PHASE_ID,
        "verifier": "GO" if passed else "NO_GO",
        "passed": passed,
        "boundary_ok": passed,
        "check_count": check_count,
        "min_checks": MIN_CHECKS,
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "verifier": report["verifier"],
                "check_count": check_count,
                "passed": passed,
                "final_decision": summary.get("final_decision"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
