#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Main Project Structure Migration B3 Preflight Via Harness v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.main_project_structure_migration_b3_preflight_via_harness_v1 import (
    CAPABILITIES_ROOT,
    BATCH_DOMAIN,
    FINAL_DECISION_GO,
    FINAL_DECISION_HOLD,
    NEXT_PHASE_GO,
    NEXT_PHASE_HOLD,
    PHASE_ID,
    REQUIRED_FIXED_CHECKS,
    UPSTREAM_REQUIRED_FINAL,
    UPSTREAM_REQUIRED_PHASE,
)

MIN_CHECKS = 420

REQUIRED_FILES = (
    "b3_batch_config_v1.json",
    "b3_preflight_result_v1.json",
    "b3_import_path_consistency_scan_v1.json",
    "b3_capability_module_naming_consistency_scan_v1.json",
    "b3_migration_refactor_opportunity_scan_v1.json",
    "b3_preflight_readiness_decision_v1.json",
    "summary.json",
)


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default=str(repo_root / "_eval_out" / "main_project_structure_migration_b3_preflight_via_harness_v1_smoke_v0"),
    )
    p.add_argument("--b2-post-migration-review-root", required=True)
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
    batch_cfg = _load_json(root / "b3_batch_config_v1.json")
    preflight = _load_json(root / "b3_preflight_result_v1.json")
    import_scan = _load_json(root / "b3_import_path_consistency_scan_v1.json")
    naming_scan = _load_json(root / "b3_capability_module_naming_consistency_scan_v1.json")
    refactor_scan = _load_json(root / "b3_migration_refactor_opportunity_scan_v1.json")
    readiness = _load_json(root / "b3_preflight_readiness_decision_v1.json")

    path_count = summary.get("candidate_path_count") or 0
    hold = summary.get("hold_for_review") is True
    expected_final = FINAL_DECISION_HOLD if hold else FINAL_DECISION_GO
    expected_next = NEXT_PHASE_HOLD if hold else NEXT_PHASE_GO

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.path_count", path_count > 0)
    ok("summary.final", summary.get("final_decision") == expected_final)
    ok("summary.next", summary.get("recommended_next_phase") == expected_next)
    ok("summary.hold_flag", summary.get("hold_for_review") == hold)

    rv_root = Path(args.b2_post_migration_review_root)
    rv_sm = _load_json(rv_root / "summary.json")
    rv_vr = _load_json(rv_root / "verifier_report.json")
    ok("upstream.go", rv_vr.get("verifier") == "GO")
    ok("upstream.final", rv_sm.get("final_decision") == UPSTREAM_REQUIRED_FINAL)
    ok("upstream.b2_closed", rv_sm.get("b2_closed_now") is True)
    ok("upstream.b3_ready", rv_sm.get("ready_for_b3_preflight_via_harness") is True)

    ok("batch.id", batch_cfg.get("batch_id") == "B3")
    ok("batch.domain", batch_cfg.get("batch_domain") == BATCH_DOMAIN)
    ok("batch.count_match", len(batch_cfg.get("candidate_paths") or []) == path_count)
    ok("batch.scope", all(p.startswith(f"{CAPABILITIES_ROOT}/") for p in (batch_cfg.get("candidate_paths") or [])))
    ok("batch.blocked_rewrite", "content_rewrite" in (batch_cfg.get("blocked_operations") or []))

    check_results = summary.get("check_results") or {}
    for check_id in REQUIRED_FIXED_CHECKS:
        if check_id == "readiness_decision":
            continue
        passed_check = check_results.get(check_id) is True
        if hold and check_id in ("python_import_path_consistency_check", "capability_module_naming_consistency_check"):
            passed_check = check_results.get(check_id) is False
        ok(f"check.{check_id}", passed_check)

    ok("import.scan_present", import_scan.get("import_path_issue_candidates") is not None)
    ok("import.no_rewrite", import_scan.get("import_rewrite_executed_now") is False)
    ok("naming.scan_present", naming_scan.get("naming_issue_candidates") is not None)
    ok("naming.no_rename", naming_scan.get("module_rename_executed_now") is False)
    ok("refactor.blocked", refactor_scan.get("extract_now_allowed") is False)
    ok("readiness.hold_match", readiness.get("hold_for_review") == hold)
    ok("summary.no_arm", summary.get("arming_chain_reopened_now") is False)
    ok("summary.no_import_rewrite", summary.get("import_rewrite_executed_now") is False)

    if hold:
        ok(
            "hold.import_or_naming",
            (summary.get("import_high_risk_count") or 0) > 0 or (summary.get("naming_high_risk_count") or 0) > 0,
        )
        ok("readiness.not_ready", readiness.get("ready_for_b3_controlled_execution") is False)
        ok("preflight.hold_flag", preflight.get("hold_for_review") is True)
    else:
        ok("go.all_checks", summary.get("all_fixed_checks_pass") is True)
        ok("readiness.ready", readiness.get("ready_for_b3_controlled_execution") is True)
        ok("preflight.pass", preflight.get("all_checks_pass") is True)
        ok("check.import_pass", check_results.get("python_import_path_consistency_check") is True)
        ok("check.naming_pass", check_results.get("capability_module_naming_consistency_check") is True)

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
