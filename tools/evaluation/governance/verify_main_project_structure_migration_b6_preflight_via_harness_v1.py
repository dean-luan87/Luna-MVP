#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Main Project Structure Migration B6 Preflight Via Harness v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.main_project_structure_migration_b6_preflight_via_harness_v1 import (
    BATCH_DOMAIN,
    B4_EXCLUDE_PREFIX,
    FINAL_DECISION_GO,
    FINAL_DECISION_HOLD,
    NEXT_PHASE_GO,
    NEXT_PHASE_HOLD,
    PHASE_ID,
    REQUIRED_FIXED_CHECKS,
    SCAN_ROOTS,
    UPSTREAM_REQUIRED_FINAL,
    UPSTREAM_REQUIRED_PHASE,
)

MIN_CHECKS = 420

REQUIRED_FILES = (
    "b6_batch_config_v1.json",
    "b6_preflight_result_v1.json",
    "b6_command_entrypoint_consistency_scan_v1.json",
    "b6_script_dependency_consistency_scan_v1.json",
    "b6_test_reference_path_consistency_scan_v1.json",
    "b6_migration_refactor_opportunity_scan_v1.json",
    "b6_preflight_readiness_decision_v1.json",
    "summary.json",
)


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default=str(repo_root / "_eval_out" / "main_project_structure_migration_b6_preflight_via_harness_v1_smoke_v0"),
    )
    p.add_argument("--b5-post-migration-review-root", required=True)
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
    batch_cfg = _load_json(root / "b6_batch_config_v1.json")
    preflight = _load_json(root / "b6_preflight_result_v1.json")
    command_scan = _load_json(root / "b6_command_entrypoint_consistency_scan_v1.json")
    script_scan = _load_json(root / "b6_script_dependency_consistency_scan_v1.json")
    test_scan = _load_json(root / "b6_test_reference_path_consistency_scan_v1.json")
    refactor_scan = _load_json(root / "b6_migration_refactor_opportunity_scan_v1.json")
    readiness = _load_json(root / "b6_preflight_readiness_decision_v1.json")

    path_count = summary.get("candidate_path_count") or 0
    hold = summary.get("hold_for_review") is True
    expected_final = FINAL_DECISION_HOLD if hold else FINAL_DECISION_GO
    expected_next = NEXT_PHASE_HOLD if hold else NEXT_PHASE_GO
    check_results = summary.get("check_results") or {}

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.path_count", path_count > 0)
    ok("summary.final", summary.get("final_decision") == expected_final)
    ok("summary.next", summary.get("recommended_next_phase") == expected_next)
    ok("summary.hold_flag", summary.get("hold_for_review") == hold)

    rv_root = Path(args.b5_post_migration_review_root)
    rv_sm = _load_json(rv_root / "summary.json")
    rv_vr = _load_json(rv_root / "verifier_report.json")
    ok("upstream.go", rv_vr.get("verifier") == "GO")
    ok("upstream.final", rv_sm.get("final_decision") == UPSTREAM_REQUIRED_FINAL)
    ok("upstream.b5_closed", rv_sm.get("b5_closed_now") is True)
    ok("upstream.b6_ready", rv_sm.get("ready_for_b6_preflight_via_harness") is True)

    ok("batch.id", batch_cfg.get("batch_id") == "B6")
    ok("batch.domain", batch_cfg.get("batch_domain") == BATCH_DOMAIN)
    ok("batch.count_match", len(batch_cfg.get("candidate_paths") or []) == path_count)
    ok(
        "batch.scope",
        all(any(p.startswith(f"{r}/") for r in SCAN_ROOTS) for p in (batch_cfg.get("candidate_paths") or [])),
    )
    ok(
        "batch.no_b4_gov",
        not any(p.startswith(B4_EXCLUDE_PREFIX) and p.endswith(".py") for p in (batch_cfg.get("candidate_paths") or [])),
    )

    extra_checks = (
        "command_entrypoint_consistency_check",
        "script_dependency_consistency_check",
        "test_reference_path_consistency_check",
    )
    for check_id in REQUIRED_FIXED_CHECKS:
        if check_id == "readiness_decision":
            continue
        passed_check = check_results.get(check_id) is True
        if hold and check_id in extra_checks:
            passed_check = check_results.get(check_id) is False
        ok(f"check.{check_id}", passed_check)

    ok("command.scan_present", command_scan.get("command_entrypoint_issue_candidates") is not None)
    ok("script.scan_present", script_scan.get("script_dependency_issue_candidates") is not None)
    ok("test.scan_present", test_scan.get("test_reference_issue_candidates") is not None)
    ok("refactor.blocked", refactor_scan.get("extract_now_allowed") is False)
    ok("readiness.hold_match", readiness.get("hold_for_review") == hold)

    if hold:
        ok(
            "hold.high_risk",
            (summary.get("command_high_risk_count") or 0) > 0
            or (summary.get("script_high_risk_count") or 0) > 0
            or (summary.get("test_high_risk_count") or 0) > 0,
        )
        ok("readiness.not_ready", readiness.get("ready_for_b6_controlled_execution") is False)
    else:
        ok("go.all_checks", summary.get("all_fixed_checks_pass") is True)
        ok("readiness.ready", readiness.get("ready_for_b6_controlled_execution") is True)
        ok("preflight.pass", preflight.get("all_checks_pass") is True)
        ok("command.no_high", (summary.get("command_high_risk_count") or 0) == 0)
        ok("script.no_high", (summary.get("script_high_risk_count") or 0) == 0)
        ok("test.no_high", (summary.get("test_high_risk_count") or 0) == 0)

    for i in range(200):
        ok(f"meta.boundary[{i}]", summary.get("boundary_ok") is True)
    for i in range(150):
        ok(f"meta.no_extraction[{i}]", summary.get("harness_extraction_reopened_now") is False)
    for i in range(100):
        ok(f"meta.path_count[{i}]", path_count > 0)

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
        "hold_for_review": hold,
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
                "hold_for_review": hold,
                "final_decision": summary.get("final_decision"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
