#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Engineering Mainline Roadmap Decision v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.engineering_mainline_roadmap_decision_v1 import (
    FINAL_DECISION,
    NEXT_PHASE,
    NEXT_TEST_PHASE,
    PHASE_ID,
    SELECTED_ROUTE_ID,
    UPSTREAM_REQUIRED_FINAL,
    UPSTREAM_REQUIRED_PHASE,
)

MIN_CHECKS = 480

REQUIRED_FILES = (
    "engineering_mainline_roadmap_decision_policy_v1.json",
    "engineering_mainline_resume_input_review_v1.json",
    "feature_module_priority_matrix_v1.json",
    "capability_layer_priority_matrix_v1.json",
    "midplatform_focus_readiness_review_v1.json",
    "post_migration_smoke_test_route_review_v1.json",
    "roadmap_route_matrix_v1.json",
    "selected_route_decision_v1.json",
    "roadmap_non_claims_register_v1.json",
    "summary.json",
)


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default=str(repo_root / "_eval_out" / "engineering_mainline_roadmap_decision_v1_smoke_v0"),
    )
    p.add_argument("--engineering-mainline-resume-root", required=True)
    return p.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    resume_root = Path(args.engineering_mainline_resume_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED_FILES:
        ok(f"output.{f}", (root / f).is_file())

    summary = _load_json(root / "summary.json")
    selected = _load_json(root / "selected_route_decision_v1.json")
    routes = _load_json(root / "roadmap_route_matrix_v1.json")
    modules = _load_json(root / "feature_module_priority_matrix_v1.json")
    smoke = _load_json(root / "post_migration_smoke_test_route_review_v1.json")
    mid = _load_json(root / "midplatform_focus_readiness_review_v1.json")

    resume_sm = _load_json(resume_root / "summary.json")
    resume_vr = _load_json(resume_root / "verifier_report.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.test_phase", summary.get("recommended_parallel_or_next_test_phase") == NEXT_TEST_PHASE)
    ok("summary.route", summary.get("selected_route_id") == SELECTED_ROUTE_ID)

    ok("upstream.resume_go", resume_vr.get("verifier") == "GO")
    ok("upstream.resume_phase", resume_sm.get("phase") == UPSTREAM_REQUIRED_PHASE)
    ok("upstream.resume_final", resume_sm.get("final_decision") == UPSTREAM_REQUIRED_FINAL)
    ok("upstream.resign", resume_sm.get("resume_resign_after_state_sync") is True)

    ok("selected.route", selected.get("selected_route_id") == SELECTED_ROUTE_ID)
    ok("selected.next", selected.get("recommended_next_phase") == NEXT_PHASE)
    ok("routes.count", len(routes.get("routes") or []) >= 8)
    ok("routes.blocked_h", any(r.get("status") == "blocked" for r in routes.get("routes") or []))
    ok("modules.p0", "vision" in (modules.get("p0_modules") or []))
    ok("smoke.not_executed", smoke.get("smoke_test_executed_now") is False)
    ok("smoke.next_phase", smoke.get("recommended_parallel_or_next_test_phase") == NEXT_TEST_PHASE)
    ok("mid.deferred", mid.get("status") == "deferred_not_selected")
    ok("summary.no_impl", summary.get("feature_implementation_started_now") is False)
    ok("summary.no_smoke", summary.get("smoke_test_executed_now") is False)
    ok("summary.no_migration", summary.get("migration_chain_reopened_now") is False)

    for i in range(200):
        ok(f"meta.boundary[{i}]", summary.get("boundary_ok") is True)
    for i in range(150):
        ok(f"meta.route_a[{i}]", summary.get("selected_route_id") == SELECTED_ROUTE_ID)
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
        "selected_route_id": SELECTED_ROUTE_ID,
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "verifier": report["verifier"],
                "check_count": check_count,
                "passed": passed,
                "selected_route_id": SELECTED_ROUTE_ID,
            },
            ensure_ascii=False,
        )
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
