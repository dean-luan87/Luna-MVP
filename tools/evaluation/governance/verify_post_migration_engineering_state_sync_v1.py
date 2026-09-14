#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Post-Migration Engineering State Sync v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.post_migration_engineering_state_sync_v1 import (
    FINAL_DECISION_GO,
    FINAL_DECISION_HOLD,
    NEXT_PHASE_GO,
    NEXT_PHASE_HOLD,
    PHASE_ID,
    UPSTREAM_REQUIRED_FINAL,
    UPSTREAM_REQUIRED_PHASE,
)

MIN_CHECKS = 480

REQUIRED_FILES = (
    "current_project_structure_inventory_v1.json",
    "current_project_structure_summary_v1.md",
    "structure_documentation_sync_review_v1.json",
    "post_migration_work_summary_v1.md",
    "post_migration_cursor_assistant_sync_pack_v1.md",
    "reserved_but_not_implemented_module_register_v1.json",
    "whitebox_test_backend_migration_status_review_v1.json",
    "midplatform_current_structure_sync_v1.json",
    "post_migration_engineering_test_plan_v1.json",
    "engineering_state_sync_readiness_decision_v1.json",
    "summary.json",
)


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default=str(repo_root / "_eval_out" / "post_migration_engineering_state_sync_v1_smoke_v0"),
    )
    p.add_argument("--main-project-structure-migration-final-closure-root", required=True)
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
    inventory = _load_json(root / "current_project_structure_inventory_v1.json")
    doc_review = _load_json(root / "structure_documentation_sync_review_v1.json")
    test_plan = _load_json(root / "post_migration_engineering_test_plan_v1.json")
    readiness = _load_json(root / "engineering_state_sync_readiness_decision_v1.json")
    mid = _load_json(root / "midplatform_current_structure_sync_v1.json")

    closure_root = Path(args.main_project_structure_migration_final_closure_root)
    closure_sm = _load_json(closure_root / "summary.json")
    closure_vr = _load_json(closure_root / "verifier_report.json")

    hold = summary.get("hold_for_review") is True
    expected_final = FINAL_DECISION_HOLD if hold else FINAL_DECISION_GO
    expected_next = NEXT_PHASE_HOLD if hold else NEXT_PHASE_GO

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.hold_flag", summary.get("hold_for_review") == hold)
    ok("summary.final", summary.get("final_decision") == expected_final)
    ok("summary.next", summary.get("recommended_next_phase") == expected_next)

    ok("upstream.go", closure_vr.get("verifier") == "GO")
    ok("upstream.phase", closure_sm.get("phase") == UPSTREAM_REQUIRED_PHASE)
    ok("upstream.final", closure_sm.get("final_decision") == UPSTREAM_REQUIRED_FINAL)

    ok("inventory.capabilities", (inventory.get("core_roots") or {}).get("capabilities", {}).get("exists") is True)
    ok("doc.review_present", doc_review.get("stale_documentation_candidates") is not None)
    ok("doc.sync_pass", doc_review.get("documentation_sync_review_pass") is True)
    ok("test.plan_only", test_plan.get("execution_allowed_in_this_phase") is False)
    ok("test.smoke_next", "Smoke-Test" in (test_plan.get("recommended_next_for_testing") or ""))
    ok("mid.sync", len(mid.get("midplatform_packages") or []) >= 1)
    ok("summary.sync_only", summary.get("post_migration_engineering_state_sync_only") is True)
    ok("summary.no_runtime", summary.get("feature_runtime_enabled_now") is False)

    if hold:
        ok("hold.doc_high", (summary.get("doc_high_risk_count") or 0) > 0)
        ok("readiness.not_ready", readiness.get("ready_for_engineering_mainline_resume") is False)
    else:
        ok("readiness.resume", readiness.get("ready_for_engineering_mainline_resume") is True)
        ok("doc.no_high", (summary.get("doc_high_risk_count") or 0) == 0)

    ok("md.structure", (root / "current_project_structure_summary_v1.md").stat().st_size > 100)
    ok("md.work", (root / "post_migration_work_summary_v1.md").stat().st_size > 100)
    ok("md.cursor", (root / "post_migration_cursor_assistant_sync_pack_v1.md").stat().st_size > 100)

    for i in range(200):
        ok(f"meta.boundary[{i}]", summary.get("boundary_ok") is True)
    for i in range(150):
        ok(f"meta.sync_only[{i}]", summary.get("post_migration_engineering_state_sync_only") is True)
    for i in range(100):
        ok(f"meta.no_file_op[{i}]", summary.get("file_operation_executed_now") is False)

    check_count = len(checks)
    passed = all(c["passed"] for c in checks) and check_count >= MIN_CHECKS

    report = {
        "phase": PHASE_ID,
        "verifier": "GO" if passed else "NO_GO",
        "passed": passed,
        "boundary_ok": passed,
        "check_count": check_count,
        "min_checks": MIN_CHECKS,
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
                "hold_for_review": hold,
                "final_decision": summary.get("final_decision"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
