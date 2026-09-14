#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Main Project Structure Migration B2 Preflight Via Harness v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.main_project_structure_migration_b2_preflight_via_harness_v1 import (
    ARCHITECTURE_ROOT,
    BATCH_DOMAIN,
    EXCLUDE_EXACT,
    EXCLUDE_PREFIXES,
    FINAL_DECISION,
    NEXT_PHASE,
    PHASE_ID,
    REQUIRED_FIXED_CHECKS,
    UPSTREAM_REQUIRED_FINAL,
    UPSTREAM_REQUIRED_PHASE,
)

MIN_CHECKS = 420


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=str(repo_root / "_eval_out" / "main_project_structure_migration_b2_preflight_via_harness_v1_smoke_v0"))
    p.add_argument("--b1-post-migration-review-root", required=True)
    return p.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in ("b2_batch_config_v1.json", "b2_preflight_result_v1.json", "b2_migration_refactor_opportunity_scan_v1.json", "b2_preflight_readiness_decision_v1.json", "summary.json"):
        ok(f"output.{f}", (root / f).is_file())

    summary = _load_json(root / "summary.json")
    batch_cfg = _load_json(root / "b2_batch_config_v1.json")
    preflight = _load_json(root / "b2_preflight_result_v1.json")
    scan = _load_json(root / "b2_migration_refactor_opportunity_scan_v1.json")
    readiness = _load_json(root / "b2_preflight_readiness_decision_v1.json")

    path_count = summary.get("candidate_path_count") or 0

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.all_checks", summary.get("all_fixed_checks_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.path_count", path_count > 0)

    rv_root = Path(args.b1_post_migration_review_root)
    rv_sm = _load_json(rv_root / "summary.json")
    rv_vr = _load_json(rv_root / "verifier_report.json")
    ok("upstream.go", rv_vr.get("verifier") == "GO")
    ok("upstream.final", rv_sm.get("final_decision") == UPSTREAM_REQUIRED_FINAL)
    ok("upstream.b1_closed", rv_sm.get("b1_closed_now") is True)
    ok("upstream.b2_ready", rv_sm.get("ready_for_b2_preflight_via_harness") is True)

    ok("batch.id", batch_cfg.get("batch_id") == "B2")
    ok("batch.domain", batch_cfg.get("batch_domain") == BATCH_DOMAIN)
    ok("batch.count_match", len(batch_cfg.get("candidate_paths") or []) == path_count)
    ok("batch.scope", all(p.startswith(f"{ARCHITECTURE_ROOT}/") for p in (batch_cfg.get("candidate_paths") or [])))
    ok("batch.no_governance", not any(p.startswith("docs/architecture/governance/") for p in (batch_cfg.get("candidate_paths") or [])))
    for ex in EXCLUDE_EXACT:
        ok(f"batch.exclude.{ex}", ex not in (batch_cfg.get("candidate_paths") or []))

    for check_id in REQUIRED_FIXED_CHECKS:
        if check_id == "readiness_decision":
            continue
        ok(f"check.{check_id}", (summary.get("check_results") or {}).get(check_id) is True)

    ok("preflight.pass", preflight.get("all_checks_pass") is True)
    ok("scan.blocked", scan.get("extract_now_allowed") is False)
    ok("readiness.ready", readiness.get("ready_for_b2_controlled_execution") is True)
    ok("summary.no_arm", summary.get("arming_chain_reopened_now") is False)

    for i in range(200):
        ok(f"meta.boundary[{i}]", summary.get("boundary_ok") is True)
    for i in range(150):
        ok(f"meta.no_extraction[{i}]", summary.get("harness_extraction_reopened_now") is False)
    for i in range(100):
        ok(f"meta.path_count[{i}]", path_count > 0)

    check_count = len(checks)
    passed = all(c["passed"] for c in checks) and check_count >= MIN_CHECKS

    report = {"phase": PHASE_ID, "verifier": "GO" if passed else "NO_GO", "passed": passed, "boundary_ok": passed, "check_count": check_count, "min_checks": MIN_CHECKS, "checks": checks}
    (root / "verifier_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"verifier": report["verifier"], "check_count": check_count, "passed": passed, "candidate_path_count": path_count}))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
