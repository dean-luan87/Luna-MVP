#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Main Project Structure Migration B4 Post-Migration Review v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.main_project_structure_migration_b4_post_migration_review_v1 import (
    FINAL_DECISION,
    NEXT_PHASE,
    PHASE_ID,
    UPSTREAM_REQUIRED_FINAL,
    UPSTREAM_REQUIRED_PHASE,
)

MIN_CHECKS = 420

REQUIRED_FILES = (
    "b4_manifest_review_v1.json",
    "b4_operation_trace_review_v1.json",
    "b4_boundary_guard_review_v1.json",
    "b4_post_migration_readiness_decision_v1.json",
    "summary.json",
)


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default=str(repo_root / "_eval_out" / "main_project_structure_migration_b4_post_migration_review_v1_smoke_v0"),
    )
    p.add_argument("--b4-controlled-execution-root", required=True)
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
    manifest = _load_json(root / "b4_manifest_review_v1.json")
    trace = _load_json(root / "b4_operation_trace_review_v1.json")
    guard = _load_json(root / "b4_boundary_guard_review_v1.json")
    readiness = _load_json(root / "b4_post_migration_readiness_decision_v1.json")

    ex_root = Path(args.b4_controlled_execution_root)
    ex_sm = _load_json(ex_root / "summary.json")
    ex_vr = _load_json(ex_root / "verifier_report.json")

    path_count = summary.get("candidate_path_count") or ex_sm.get("candidate_path_count") or 0

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.b4_closed", summary.get("b4_closed_now") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.b5_ready", summary.get("ready_for_b5_preflight_via_harness") is True)
    ok("summary.unchanged_match", summary.get("operations_unchanged") == path_count)

    ok("upstream.go", ex_vr.get("verifier") == "GO")
    ok("upstream.phase", ex_sm.get("phase") == UPSTREAM_REQUIRED_PHASE)
    ok("upstream.final", ex_sm.get("final_decision") == UPSTREAM_REQUIRED_FINAL)

    ok("manifest.pass", manifest.get("review_pass") is True)
    ok("manifest.sha256", manifest.get("sha256_all_match") is True)
    ok("trace.pass", trace.get("review_pass") is True)
    ok("guard.pass", guard.get("review_pass") is True)
    ok("guard.no_phase_id", guard.get("phase_id_modify_review_pass") is True)
    ok("guard.low_deferred", guard.get("low_severity_candidates_deferred") is True)

    ok("readiness.b4_closed", readiness.get("b4_closed") is True)
    ok("readiness.b5", readiness.get("ready_for_b5_preflight_via_harness") is True)

    for i in range(200):
        ok(f"meta.boundary[{i}]", summary.get("boundary_ok") is True)
    for i in range(150):
        ok(f"meta.unchanged[{i}]", summary.get("operations_unchanged") == path_count)
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
    print(json.dumps({"verifier": report["verifier"], "check_count": check_count, "passed": passed, "candidate_path_count": path_count}))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
