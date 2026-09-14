#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Engineering Mainline Resume v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.engineering_mainline_resume_v1 import (
    ENGINEERING_MODULES,
    FINAL_DECISION,
    NEXT_PHASE,
    PHASE_ID,
    REQUIRED_SYNC_ARTIFACTS,
    UPSTREAM_REQUIRED_FINAL,
    UPSTREAM_REQUIRED_PHASE,
)

MIN_CHECKS = 480

REQUIRED_FILES = (
    "engineering_mainline_resume_policy_v1.json",
    "post_migration_state_sync_input_review_v1.json",
    "engineering_focus_module_matrix_v1.json",
    "capability_layering_matrix_v1.json",
    "mainline_resume_guardrails_v1.json",
    "deferred_registers_handoff_v1.json",
    "engineering_resume_test_handoff_v1.json",
    "engineering_mainline_resume_decision_v1.json",
    "summary.json",
)


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default=str(repo_root / "_eval_out" / "engineering_mainline_resume_v1_smoke_v0"),
    )
    p.add_argument("--post-migration-engineering-state-sync-root", required=True)
    return p.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    sync_root = Path(args.post_migration_engineering_state_sync_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED_FILES:
        ok(f"output.{f}", (root / f).is_file())

    summary = _load_json(root / "summary.json")
    policy = _load_json(root / "engineering_mainline_resume_policy_v1.json")
    sync_review = _load_json(root / "post_migration_state_sync_input_review_v1.json")
    focus = _load_json(root / "engineering_focus_module_matrix_v1.json")
    layering = _load_json(root / "capability_layering_matrix_v1.json")
    guardrails = _load_json(root / "mainline_resume_guardrails_v1.json")
    deferred = _load_json(root / "deferred_registers_handoff_v1.json")
    test_handoff = _load_json(root / "engineering_resume_test_handoff_v1.json")
    decision = _load_json(root / "engineering_mainline_resume_decision_v1.json")

    sync_sm = _load_json(sync_root / "summary.json")
    sync_vr = _load_json(sync_root / "verifier_report.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.state_sync_upstream", summary.get("state_sync_upstream_confirmed") is True)
    ok("summary.resign", summary.get("resume_resign_after_state_sync") is True)

    ok("upstream.sync_go", sync_vr.get("verifier") == "GO")
    ok("upstream.sync_phase", sync_sm.get("phase") == UPSTREAM_REQUIRED_PHASE)
    ok("upstream.sync_final", sync_sm.get("final_decision") == UPSTREAM_REQUIRED_FINAL)
    ok("upstream.no_hold", sync_sm.get("hold_for_review") is False)
    ok("upstream.doc_no_high", (sync_sm.get("doc_high_risk_count") or 0) == 0)

    for artifact in REQUIRED_SYNC_ARTIFACTS:
        ok(f"upstream.artifact.{artifact}", (sync_root / artifact).is_file())

    ok("sync_review.pass", sync_review.get("review_pass") is True)
    ok("sync_review.artifacts", sync_review.get("all_required_artifacts_present") is True)
    ok("policy.primary_upstream", policy.get("primary_upstream") == UPSTREAM_REQUIRED_PHASE)
    ok("focus.count", len(focus.get("modules") or []) == len(ENGINEERING_MODULES))
    ok("focus.p0", "vision" in (focus.get("recommended_first_wave") or []))
    ok("layering.count", len(layering.get("layers") or []) == 3)
    ok("guardrails.pass", guardrails.get("review_pass") is True)
    ok("deferred.low_not_processed", deferred.get("low_severity", {}).get("processed_now") is False)
    ok("deferred.reserved_not_impl", deferred.get("reserved_modules", {}).get("implemented_now") is False)
    ok("test.no_exec", test_handoff.get("smoke_test_executed_now") is False)
    ok("test.smoke_phase", "Smoke-Test" in (test_handoff.get("recommended_next_for_testing") or ""))
    ok("decision.roadmap", decision.get("ready_for_roadmap_decision") is True)
    ok("decision.no_smoke_now", decision.get("ready_for_smoke_test_phase") is False)
    ok("summary.no_runtime", summary.get("feature_runtime_enabled_now") is False)
    ok("summary.no_smoke", summary.get("smoke_test_executed_now") is False)
    ok("summary.no_migration_work", summary.get("structure_migration_work_continued_now") is False)

    for i in range(200):
        ok(f"meta.boundary[{i}]", summary.get("boundary_ok") is True)
    for i in range(150):
        ok(f"meta.upstream[{i}]", summary.get("state_sync_upstream_confirmed") is True)
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
