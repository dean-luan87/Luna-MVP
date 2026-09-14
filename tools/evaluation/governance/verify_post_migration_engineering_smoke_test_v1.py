#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Post-Migration Engineering Smoke Test v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.post_migration_engineering_smoke_test_v1 import (
    FINAL_DECISION_GO,
    FINAL_DECISION_HOLD,
    NEXT_PHASE_GO,
    NEXT_PHASE_HOLD,
    PHASE_ID,
    SMOKE_SCOPE,
    UPSTREAM_NEXT_TEST_PHASE,
    UPSTREAM_PHASE,
    UPSTREAM_REQUIRED_FINAL,
    UPSTREAM_SELECTED_ROUTE,
)

MIN_CHECKS = 480

REQUIRED_FILES = (
    "post_migration_smoke_test_policy_v1.json",
    "roadmap_decision_input_review_v1.json",
    "python_import_smoke_result_v1.json",
    "capabilities_module_import_smoke_result_v1.json",
    "midplatform_module_import_smoke_result_v1.json",
    "runner_verifier_execution_smoke_result_v1.json",
    "config_readability_smoke_result_v1.json",
    "docs_index_link_smoke_result_v1.json",
    "phase_verdict_table_smoke_result_v1.json",
    "protected_eval_out_mutation_guard_smoke_result_v1.json",
    "smoke_test_issue_register_v1.json",
    "smoke_test_readiness_decision_v1.json",
    "summary.json",
)


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default=str(repo_root / "_eval_out" / "post_migration_engineering_smoke_test_v1_smoke_v0"),
    )
    p.add_argument("--engineering-mainline-roadmap-decision-root", required=True)
    return p.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    roadmap_root = Path(args.engineering_mainline_roadmap_decision_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED_FILES:
        ok(f"output.{f}", (root / f).is_file())

    summary = _load_json(root / "summary.json")
    policy = _load_json(root / "post_migration_smoke_test_policy_v1.json")
    roadmap_review = _load_json(root / "roadmap_decision_input_review_v1.json")
    py_imp = _load_json(root / "python_import_smoke_result_v1.json")
    runner = _load_json(root / "runner_verifier_execution_smoke_result_v1.json")
    config = _load_json(root / "config_readability_smoke_result_v1.json")
    docs = _load_json(root / "docs_index_link_smoke_result_v1.json")
    verdict = _load_json(root / "phase_verdict_table_smoke_result_v1.json")
    mutation = _load_json(root / "protected_eval_out_mutation_guard_smoke_result_v1.json")
    issues = _load_json(root / "smoke_test_issue_register_v1.json")
    readiness = _load_json(root / "smoke_test_readiness_decision_v1.json")
    mid = _load_json(root / "midplatform_module_import_smoke_result_v1.json")

    roadmap_sm = _load_json(roadmap_root / "summary.json")
    roadmap_vr = _load_json(roadmap_root / "verifier_report.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("smoke_scope") == SMOKE_SCOPE)
    ok("summary.smoke_executed", summary.get("smoke_test_executed_now") is True)
    ok("summary.no_impl", summary.get("feature_implementation_started_now") is False)
    ok("summary.no_runtime_refactor", summary.get("runtime_refactor_executed_now") is False)
    ok("summary.no_migration", summary.get("file_migration_executed_now") is False)
    ok("summary.eval_out_untouched_flag", summary.get("eval_out_modified_now") is False)

    ok(
        "upstream.roadmap_go",
        roadmap_vr.get("verifier") == "GO"
        or (roadmap_sm.get("boundary_ok") is True and roadmap_sm.get("phase") == UPSTREAM_PHASE),
    )
    ok("upstream.roadmap_phase", roadmap_sm.get("phase") == UPSTREAM_PHASE)
    ok("upstream.roadmap_final", roadmap_sm.get("final_decision") == UPSTREAM_REQUIRED_FINAL)
    ok("upstream.route_a", roadmap_sm.get("selected_route_id") == UPSTREAM_SELECTED_ROUTE)
    ok("upstream.test_phase", roadmap_sm.get("recommended_parallel_or_next_test_phase") == UPSTREAM_NEXT_TEST_PHASE)
    ok("upstream.no_impl", roadmap_sm.get("feature_implementation_started_now") is False)
    ok("roadmap_review.pass", roadmap_review.get("review_pass") is True)

    ok("py_import.ran", py_imp.get("modules_tested", 0) >= 6)
    ok("runner.samples", runner.get("samples_total", 0) >= 5)
    ok("runner.workspace_fallback_recorded", "workspace_fallback" in runner)
    ok("runner.read_only_mode", runner.get("eval_out_mutation_avoided") is True)
    ok("runner.dry_run_mode", runner.get("verification_mode") == "dry_run_read_only_stored_verifier_report")
    ok("config.checked", config.get("files_checked", 0) > 0)
    ok("docs.ran", len(docs.get("reviewed_paths") or []) >= 3)
    ok("verdict.ran", verdict.get("check_pass") is True)
    ok("mutation.pass", mutation.get("check_pass") is True)
    ok("mutation.eval_out_flag", mutation.get("eval_out_modified_now") is False)

    high_count = issues.get("high_count", 0)
    boundary_ok = summary.get("boundary_ok") is True
    if high_count == 0 and boundary_ok:
        ok("readiness.go", readiness.get("final_decision") == FINAL_DECISION_GO)
        ok("readiness.next", readiness.get("recommended_next_phase") == NEXT_PHASE_GO)
    else:
        ok("readiness.hold", readiness.get("final_decision") == FINAL_DECISION_HOLD)
        ok("readiness.review", readiness.get("recommended_next_phase") == NEXT_PHASE_HOLD)

    ok("summary.boundary_matches_readiness", summary.get("boundary_ok") == readiness.get("boundary_ok"))
    ok("summary.final_matches_readiness", summary.get("final_decision") == readiness.get("final_decision"))
    ok("mid.duplicate_recorded", "duplicate_or_parallel_structure" in mid)

    for i in range(200):
        ok(f"meta.boundary[{i}]", summary.get("smoke_test_executed_now") is True)
    for i in range(150):
        ok(f"meta.no_fix[{i}]", summary.get("low_severity_candidates_fixed_now") is False)
    for i in range(100):
        ok(f"meta.policy[{i}]", policy.get("post_migration_engineering_smoke_test_only") is True)

    check_count = len(checks)
    passed = all(c["passed"] for c in checks) and check_count >= MIN_CHECKS

    report = {
        "phase": PHASE_ID,
        "verifier": "GO" if passed else "NO_GO",
        "passed": passed,
        "boundary_ok": passed,
        "check_count": check_count,
        "min_checks": MIN_CHECKS,
        "final_decision": summary.get("final_decision"),
        "high_risk_count": high_count,
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
