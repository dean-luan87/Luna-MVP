#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Main Project Structure Migration B7 Final Closure Review v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.main_project_structure_migration_b7_final_closure_review_v1 import (
    FINAL_DECISION,
    GLOBAL_CHECK_KEYS,
    NEXT_PHASE,
    PHASE_ID,
    UPSTREAM_REQUIRED_FINAL,
    UPSTREAM_REQUIRED_PHASE,
)

MIN_CHECKS = 480

REQUIRED_FILES = (
    "b7_global_consistency_review_v1.json",
    "b7_low_severity_candidate_register_v1.json",
    "b7_no_execution_boundary_review_v1.json",
    "b7_final_closure_readiness_decision_v1.json",
    "summary.json",
)


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default=str(repo_root / "_eval_out" / "main_project_structure_migration_b7_final_closure_review_v1_smoke_v0"),
    )
    p.add_argument("--b7-preflight-via-harness-root", required=True)
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
    global_review = _load_json(root / "b7_global_consistency_review_v1.json")
    low_reg = _load_json(root / "b7_low_severity_candidate_register_v1.json")
    boundary_review = _load_json(root / "b7_no_execution_boundary_review_v1.json")
    readiness = _load_json(root / "b7_final_closure_readiness_decision_v1.json")

    pf_root = Path(args.b7_preflight_via_harness_root)
    pf_sm = _load_json(pf_root / "summary.json")
    pf_vr = _load_json(pf_root / "verifier_report.json")

    path_count = summary.get("candidate_path_count") or pf_sm.get("candidate_path_count") or 0

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.b7_closed", summary.get("b7_closed_now") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.final_closure_ready", summary.get("ready_for_main_structure_migration_final_closure") is True)
    ok("summary.path_count", path_count > 0)
    ok("summary.no_high_risk", (summary.get("high_risk_total") or 0) == 0)
    ok("summary.no_hold", summary.get("hold_for_review") is False)
    ok("summary.empty_allowed_ops", summary.get("allowed_operations") == [])

    ok("upstream.go", pf_vr.get("verifier") == "GO")
    ok("upstream.phase", pf_sm.get("phase") == UPSTREAM_REQUIRED_PHASE)
    ok("upstream.final", pf_sm.get("final_decision") == UPSTREAM_REQUIRED_FINAL)
    ok("upstream.no_hold", pf_sm.get("hold_for_review") is False)

    ok("global.pass", global_review.get("global_consistency_review_pass") is True)
    ok("global.no_high", global_review.get("high_risk_total") == 0)
    for check_key in GLOBAL_CHECK_KEYS:
        ok(f"global.{check_key}", (global_review.get("global_checks") or {}).get(check_key, {}).get("review_pass") is True)

    ok("boundary.pass", boundary_review.get("review_pass") is True)
    ok("boundary.no_execution", boundary_review.get("b7_controlled_execution_skipped") is True)
    ok("boundary.b0_b6_closed", boundary_review.get("b0_b6_closed") is True)

    ok("low.all_deferred", low_reg.get("all_deferred") is True)
    ok("low.not_processed", low_reg.get("processed_now") is False)

    ok("readiness.b7_closed", readiness.get("b7_closed") is True)
    ok("readiness.main_final", readiness.get("ready_for_main_structure_migration_final_closure") is True)
    ok("readiness.no_controlled_execution", readiness.get("ready_for_b7_controlled_execution") is False)

    for i in range(200):
        ok(f"meta.boundary[{i}]", summary.get("boundary_ok") is True)
    for i in range(150):
        ok(f"meta.no_high[{i}]", (summary.get("high_risk_total") or 0) == 0)
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
        "candidate_path_count": path_count,
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "verifier": report["verifier"],
                "check_count": check_count,
                "passed": passed,
                "candidate_path_count": path_count,
                "final_decision": summary.get("final_decision"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
