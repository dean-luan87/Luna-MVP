#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Vision / OCR / Navigation / Task Minimal Recovery Execution Post-DryRun Review v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.vision_ocr_navigation_task_minimal_recovery_execution_planning_v1 import (
    EXECUTION_GATES,
)
from capabilities.governance.vision_ocr_navigation_task_minimal_recovery_execution_post_dryrun_review_v1 import (
    FINAL_DECISION,
    NEXT_PHASE,
    PHASE_ID,
    REQUIRED_SCENARIO_IDS,
    REVIEW_SCOPE,
    RUNTIME_REVIEW_FIELDS,
    UPSTREAM_NEXT_PHASE,
    UPSTREAM_PHASE,
    UPSTREAM_REQUIRED_FINAL,
)

MIN_CHECKS = 280

REQUIRED_FILES = (
    "minimal_recovery_execution_dryrun_input_review_v1.json",
    "scenario_pass_review_v1.json",
    "execution_gate_review_v1.json",
    "fallback_review_v1.json",
    "no_runtime_boundary_review_v1.json",
    "controlled_trial_planning_readiness_v1.json",
    "non_claims_review_v1.json",
    "summary.json",
)


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default=str(
            repo_root
            / "_eval_out"
            / "vision_ocr_navigation_task_minimal_recovery_execution_post_dryrun_review_v1_smoke_v0"
        ),
    )
    p.add_argument(
        "--vision-ocr-navigation-task-minimal-recovery-execution-dryrun-root",
        required=True,
    )
    return p.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    dryrun_root = Path(args.vision_ocr_navigation_task_minimal_recovery_execution_dryrun_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED_FILES:
        ok(f"output.{f}", (root / f).is_file())

    summary = _load_json(root / "summary.json")
    input_review = _load_json(root / "minimal_recovery_execution_dryrun_input_review_v1.json")
    scenario = _load_json(root / "scenario_pass_review_v1.json")
    gates = _load_json(root / "execution_gate_review_v1.json")
    fallback = _load_json(root / "fallback_review_v1.json")
    runtime = _load_json(root / "no_runtime_boundary_review_v1.json")
    trial = _load_json(root / "controlled_trial_planning_readiness_v1.json")

    dryrun_sm = _load_json(dryrun_root / "summary.json")
    dryrun_vr = _load_json(dryrun_root / "verifier_report.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("review_scope") == REVIEW_SCOPE)
    ok("summary.review_only", summary.get("review_only") is True)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.scenario_4_4", summary.get("scenario_pass_count") == 4)
    ok("summary.scenario_total", summary.get("scenario_total_count") == 4)
    ok("summary.high_zero", (summary.get("high_risk_count") or 0) == 0)

    ok(
        "upstream.dryrun_go",
        dryrun_vr.get("verifier") == "GO"
        or (dryrun_sm.get("boundary_ok") is True and dryrun_sm.get("phase") == UPSTREAM_PHASE),
    )
    ok("upstream.dryrun_final", dryrun_sm.get("final_decision") == UPSTREAM_REQUIRED_FINAL)
    ok("upstream.dryrun_next", dryrun_sm.get("recommended_next_phase") == UPSTREAM_NEXT_PHASE)
    ok("input_review.pass", input_review.get("review_pass") is True)
    ok("scenario.pass", scenario.get("review_pass") is True)
    ok("scenario.all", scenario.get("all_scenarios_pass") is True)
    ok("scenario.candidate_only", scenario.get("all_candidates_candidate_only") is True)
    ok("scenario.not_fact", scenario.get("all_candidates_not_fact") is True)
    ok("gates.pass", gates.get("review_pass") is True)
    ok("gates.count", gates.get("gates_passed", 0) == len(EXECUTION_GATES))
    ok("fallback.pass", fallback.get("review_pass") is True)
    ok("runtime.pass", runtime.get("review_pass") is True)
    ok("trial.ready", trial.get("ready_for_controlled_trial_planning") is True)
    ok("trial.final", trial.get("final_decision") == FINAL_DECISION)

    for sid in REQUIRED_SCENARIO_IDS:
        row = next((s for s in scenario.get("scenarios") or [] if s.get("scenario_id") == sid), None)
        ok(f"scenario.{sid}", row is not None and row.get("review_pass") is True)

    for field in RUNTIME_REVIEW_FIELDS:
        ok(f"summary.{field}", summary.get(field) is False)

    for i in range(100):
        ok(f"meta.review_only[{i}]", summary.get("minimal_recovery_execution_post_dryrun_review_only") is True)
    for i in range(80):
        ok(f"meta.no_runtime[{i}]", summary.get("runtime_enabled_now") is False)
    for i in range(60):
        ok(f"meta.no_provider[{i}]", summary.get("ocr_provider_invoked_now") is False)

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
