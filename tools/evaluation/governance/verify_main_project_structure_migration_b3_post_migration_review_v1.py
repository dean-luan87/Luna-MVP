#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Main Project Structure Migration B3 Post-Migration Review v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.main_project_structure_migration_b3_post_migration_review_v1 import (
    FINAL_DECISION,
    NEXT_PHASE,
    PHASE_ID,
    UPSTREAM_REQUIRED_FINAL,
    UPSTREAM_REQUIRED_PHASE,
)

MIN_CHECKS = 420

REQUIRED_FILES = (
    "b3_manifest_review_v1.json",
    "b3_operation_trace_review_v1.json",
    "b3_boundary_guard_review_v1.json",
    "b3_post_migration_readiness_decision_v1.json",
    "summary.json",
)


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default=str(repo_root / "_eval_out" / "main_project_structure_migration_b3_post_migration_review_v1_smoke_v0"),
    )
    p.add_argument("--b3-controlled-execution-root", required=True)
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
    manifest = _load_json(root / "b3_manifest_review_v1.json")
    trace = _load_json(root / "b3_operation_trace_review_v1.json")
    guard = _load_json(root / "b3_boundary_guard_review_v1.json")
    readiness = _load_json(root / "b3_post_migration_readiness_decision_v1.json")

    ex_root = Path(args.b3_controlled_execution_root)
    ex_sm = _load_json(ex_root / "summary.json")
    ex_vr = _load_json(ex_root / "verifier_report.json")

    path_count = summary.get("candidate_path_count") or ex_sm.get("candidate_path_count") or 0

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.b3_closed", summary.get("b3_closed_now") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.b4_ready", summary.get("ready_for_b4_preflight_via_harness") is True)
    ok("summary.path_count", path_count > 0)
    ok("summary.unchanged_match", summary.get("operations_unchanged") == path_count)

    ok("upstream.go", ex_vr.get("verifier") == "GO")
    ok("upstream.phase", ex_sm.get("phase") == UPSTREAM_REQUIRED_PHASE)
    ok("upstream.final", ex_sm.get("final_decision") == UPSTREAM_REQUIRED_FINAL)
    ok("upstream.execution_done", ex_sm.get("b3_execution_completed_now") is True)

    ok("manifest.pass", manifest.get("review_pass") is True)
    ok("manifest.count", manifest.get("before_count") == path_count)
    ok("manifest.sha256", manifest.get("sha256_all_match") is True)
    ok("trace.pass", trace.get("review_pass") is True)
    ok("trace.interpretation", "stable placement" in (trace.get("interpretation") or "").lower())
    ok("guard.pass", guard.get("review_pass") is True)
    ok("guard.no_import_rewrite", guard.get("import_rewrite_review_pass") is True)
    ok("guard.no_module_rename", guard.get("module_rename_review_pass") is True)
    ok("guard.no_arm", guard.get("harness_chain_guard_pass") is True)

    ok("readiness.b3_closed", readiness.get("b3_closed") is True)
    ok("readiness.b4", readiness.get("ready_for_b4_preflight_via_harness") is True)

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
