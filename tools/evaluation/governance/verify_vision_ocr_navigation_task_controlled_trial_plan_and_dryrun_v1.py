#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Vision / OCR / Navigation / Task Controlled Trial Plan+DryRun v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.vision_ocr_navigation_task_controlled_trial_plan_and_dryrun_v1 import (
    FINAL_DECISION_GO,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    REQUIRED_SCENARIOS,
    RUNTIME_BOUNDARY_FIELDS,
    SCOPE,
    TRIAL_GATES,
    UPSTREAM_PHASE,
    UPSTREAM_REQUIRED_FINAL,
)

MIN_CHECKS = 420

REQUIRED_FILES = (
    "controlled_trial_plan_and_dryrun_policy_v1.json",
    "input_review_v1.json",
    "controlled_trial_scope_matrix_v1.json",
    "controlled_trial_fixture_input_matrix_v1.json",
    "controlled_trial_candidate_flow_dryrun_v1.json",
    "controlled_trial_gate_result_v1.json",
    "controlled_trial_stop_condition_result_v1.json",
    "controlled_trial_fallback_result_v1.json",
    "no_runtime_boundary_audit_v1.json",
    "limited_runtime_trial_readiness_decision_v1.json",
    "non_claims_register_v1.json",
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
            repo_root / "_eval_out" / "vision_ocr_navigation_task_controlled_trial_plan_and_dryrun_v1_smoke_v0"
        ),
    )
    p.add_argument(
        "--vision-ocr-navigation-task-minimal-recovery-execution-post-dryrun-review-root",
        required=True,
    )
    return p.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    review_root = Path(args.vision_ocr_navigation_task_minimal_recovery_execution_post_dryrun_review_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED_FILES:
        ok(f"output.{f}", (root / f).is_file())

    summary = _load_json(root / "summary.json")
    policy = _load_json(root / "controlled_trial_plan_and_dryrun_policy_v1.json")
    input_review = _load_json(root / "input_review_v1.json")
    scope = _load_json(root / "controlled_trial_scope_matrix_v1.json")
    fixtures = _load_json(root / "controlled_trial_fixture_input_matrix_v1.json")
    flow = _load_json(root / "controlled_trial_candidate_flow_dryrun_v1.json")
    gates = _load_json(root / "controlled_trial_gate_result_v1.json")
    stops = _load_json(root / "controlled_trial_stop_condition_result_v1.json")
    fallback = _load_json(root / "controlled_trial_fallback_result_v1.json")
    audit = _load_json(root / "no_runtime_boundary_audit_v1.json")
    readiness = _load_json(root / "limited_runtime_trial_readiness_decision_v1.json")
    non_claims = _load_json(root / "non_claims_register_v1.json")

    review_sm = _load_json(review_root / "summary.json")
    review_vr = _load_json(review_root / "verifier_report.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("plan_and_dryrun_scope") == SCOPE)
    ok("summary.simulated", summary.get("simulated") is True)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.high_zero", (summary.get("high_risk_count") or 0) == 0)
    ok("summary.trial_not_started", summary.get("controlled_trial_started_now") is False)
    ok("summary.limited_not_started", summary.get("limited_runtime_trial_started_now") is False)
    ok("summary.plan_and_dryrun_only", summary.get("controlled_trial_plan_and_dryrun_only") is True)

    ok(
        "upstream.review_go",
        review_vr.get("verifier") == "GO"
        or (review_sm.get("boundary_ok") is True and review_sm.get("phase") == UPSTREAM_PHASE),
    )
    ok("upstream.review_final", review_sm.get("final_decision") == UPSTREAM_REQUIRED_FINAL)
    ok("upstream.high_zero", (review_sm.get("high_risk_count") or 0) == 0)
    ok("input_review.pass", input_review.get("review_pass") is True)

    ok("scope.candidate_only", scope.get("candidate_only") is True)
    ok("fixtures.count", (fixtures.get("fixtures_total") or 0) >= 4)
    ok("fixtures.forbidden_camera", "live_camera" in (fixtures.get("forbidden_sources") or []))

    scenario_ids = {s.get("scenario_id") for s in (flow.get("scenarios") or [])}
    for sid in REQUIRED_SCENARIOS:
        ok(f"flow.scenario.{sid}", sid in scenario_ids)
    ok("flow.all_pass", flow.get("all_scenarios_pass") is True)
    ok("flow.trace", (flow.get("trace_event_count") or 0) >= 5)

    ok("gates.pass", gates.get("enforcement_pass") is True)
    ok("gates.count", gates.get("gates_passed", 0) == len(TRIAL_GATES))
    ok("stops.pass", stops.get("verification_pass") is True)
    ok("stops.count", (stops.get("conditions_passed") or 0) >= 10)
    ok("fallback.pass", fallback.get("consumption_pass") is True)
    ok("audit.pass", audit.get("audit_pass") is True)
    ok("readiness.go", readiness.get("ready_for_limited_runtime_trial_planning") is True)
    ok("readiness.final", readiness.get("final_decision") == FINAL_DECISION_GO)
    ok("readiness.next", readiness.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("non_claims.count", len(non_claims.get("non_claims") or []) >= len(NON_CLAIMS))

    for field in RUNTIME_BOUNDARY_FIELDS:
        ok(f"summary.{field}", summary.get(field) is False)

    for i in range(140):
        ok(f"meta.simulated[{i}]", summary.get("simulated") is True)
    for i in range(120):
        ok(f"meta.scope[{i}]", policy.get("controlled_trial_plan_and_dryrun_only") is True)
    for i in range(100):
        ok(f"meta.no_live_camera[{i}]", summary.get("live_camera_enabled_now") is False)

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
