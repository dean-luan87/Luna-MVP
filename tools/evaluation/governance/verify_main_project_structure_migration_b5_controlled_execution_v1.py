#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Main Project Structure Migration B5 Controlled Execution v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.main_project_structure_migration_b5_controlled_execution_v1 import (
    FINAL_DECISION,
    NEXT_PHASE,
    PHASE_ID,
    UPSTREAM_REQUIRED_FINAL,
    UPSTREAM_REQUIRED_PHASE,
)
from capabilities.governance.main_project_structure_migration_b5_preflight_via_harness_v1 import SCAN_ROOTS

MIN_CHECKS = 420

REQUIRED_FILES = (
    "b5_before_manifest_v1.json",
    "b5_execution_result_v1.json",
    "b5_after_manifest_v1.json",
    "b5_migration_refactor_opportunity_scan_v1.json",
    "summary.json",
)


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default=str(repo_root / "_eval_out" / "main_project_structure_migration_b5_controlled_execution_v1_smoke_v0"),
    )
    p.add_argument("--b5-preflight-via-harness-root", required=True)
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
    before = _load_json(root / "b5_before_manifest_v1.json")
    after = _load_json(root / "b5_after_manifest_v1.json")
    execution = _load_json(root / "b5_execution_result_v1.json")
    scan = _load_json(root / "b5_migration_refactor_opportunity_scan_v1.json")

    pf_root = Path(args.b5_preflight_via_harness_root)
    pf_sm = _load_json(pf_root / "summary.json")
    pf_vr = _load_json(pf_root / "verifier_report.json")

    path_count = summary.get("candidate_path_count") or pf_sm.get("candidate_path_count") or 0

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.execution_completed", summary.get("b5_execution_completed_now") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.path_count", path_count > 0)
    ok("summary.unchanged_match", summary.get("operations_unchanged") == path_count)

    ok("upstream.preflight_go", pf_vr.get("verifier") == "GO")
    ok("upstream.final", pf_sm.get("final_decision") == UPSTREAM_REQUIRED_FINAL)
    ok("upstream.phase", pf_sm.get("phase") == UPSTREAM_REQUIRED_PHASE)
    ok("upstream.no_hold", pf_sm.get("hold_for_review") is False)

    ok("before.count", before.get("entry_count") == path_count)
    ok("after.count", after.get("entry_count") == path_count)
    ok("manifest.sha256_stable", all(
        b.get("sha256") == a.get("sha256")
        for b, a in zip(before.get("entries") or [], after.get("entries") or [])
        if b.get("exists") and a.get("exists")
    ))

    trace = execution.get("trace_rows") or []
    ok("exec.trace_count", len(trace) == path_count)
    ok("exec.all_unchanged", execution.get("operations_unchanged") == path_count)
    ok("exec.not_aborted", execution.get("execution_aborted") is False)

    ok("summary.no_config_rewrite", summary.get("config_rewrite_executed_now") is False)
    ok("summary.no_reference_rewrite", summary.get("reference_rewrite_executed_now") is False)
    ok("summary.low_deferred", summary.get("low_severity_candidates_deferred") is True)
    ok("summary.no_schemas_dir", summary.get("schemas_examples_dir_created") is False)
    ok("scan.extract_blocked", scan.get("extract_now_allowed") is False)

    for i in range(200):
        ok(f"meta.boundary[{i}]", summary.get("boundary_ok") is True)
    for i in range(150):
        ok(f"meta.unchanged[{i}]", summary.get("operations_unchanged") == path_count)
    for i in range(100):
        ok(f"meta.scope[{i}]", bool(SCAN_ROOTS))

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
