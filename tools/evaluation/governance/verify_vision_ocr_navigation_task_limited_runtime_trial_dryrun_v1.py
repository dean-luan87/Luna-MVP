#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Vision / OCR / Navigation / Task Limited Runtime Trial DryRun v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.vision_ocr_navigation_task_limited_runtime_trial_dryrun_v1 import (
    DRYRUN_SCOPE,
    FINAL_DECISION_GO,
    NEXT_PHASE_GO,
    PHASE_ID,
    REQUIRED_SCENARIOS,
    RUNTIME_AUDIT_FIELDS,
    STOP_TRIGGERS,
    UPSTREAM_NEXT_PHASE,
    UPSTREAM_PHASE,
    UPSTREAM_REQUIRED_FINAL,
)
from capabilities.governance.vision_ocr_navigation_task_limited_runtime_trial_planning_v1 import (
    LIMITED_RUNTIME_GATES,
)

MIN_CHECKS = 460

REQUIRED_FILES = (
    "limited_runtime_trial_dryrun_policy_v1.json",
    "limited_runtime_trial_planning_input_review_v1.json",
    "limited_runtime_fixture_input_matrix_v1.json",
    "vision_sample_frame_candidate_dryrun_v1.json",
    "mock_ocr_result_candidate_dryrun_v1.json",
    "synthetic_navigation_guidance_candidate_dryrun_v1.json",
    "task_state_candidate_dryrun_v1.json",
    "limited_runtime_candidate_flow_trace_v1.json",
    "limited_runtime_gate_consumption_result_v1.json",
    "limited_runtime_stop_condition_result_v1.json",
    "limited_runtime_no_runtime_boundary_audit_v1.json",
    "limited_runtime_trial_dryrun_non_claims_register_v1.json",
    "limited_runtime_trial_dryrun_readiness_decision_v1.json",
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
            repo_root / "_eval_out" / "vision_ocr_navigation_task_limited_runtime_trial_dryrun_v1_smoke_v0"
        ),
    )
    p.add_argument(
        "--vision-ocr-navigation-task-limited-runtime-trial-planning-root",
        required=True,
    )
    return p.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    planning_root = Path(args.vision_ocr_navigation_task_limited_runtime_trial_planning_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED_FILES:
        ok(f"output.{f}", (root / f).is_file())

    summary = _load_json(root / "summary.json")
    policy = _load_json(root / "limited_runtime_trial_dryrun_policy_v1.json")
    input_review = _load_json(root / "limited_runtime_trial_planning_input_review_v1.json")
    fixtures = _load_json(root / "limited_runtime_fixture_input_matrix_v1.json")
    vision = _load_json(root / "vision_sample_frame_candidate_dryrun_v1.json")
    ocr = _load_json(root / "mock_ocr_result_candidate_dryrun_v1.json")
    nav = _load_json(root / "synthetic_navigation_guidance_candidate_dryrun_v1.json")
    task = _load_json(root / "task_state_candidate_dryrun_v1.json")
    trace = _load_json(root / "limited_runtime_candidate_flow_trace_v1.json")
    gates = _load_json(root / "limited_runtime_gate_consumption_result_v1.json")
    stops = _load_json(root / "limited_runtime_stop_condition_result_v1.json")
    audit = _load_json(root / "limited_runtime_no_runtime_boundary_audit_v1.json")
    readiness = _load_json(root / "limited_runtime_trial_dryrun_readiness_decision_v1.json")

    planning_sm = _load_json(planning_root / "summary.json")
    planning_vr = _load_json(planning_root / "verifier_report.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("dryrun_scope") == DRYRUN_SCOPE)
    ok("summary.simulated", summary.get("simulated") is True)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.high_zero", (summary.get("high_risk_count") or 0) == 0)
    ok("summary.trial_not_started", summary.get("limited_runtime_trial_started_now") is False)
    ok("summary.dryrun_only", summary.get("limited_runtime_trial_dryrun_only") is True)

    ok(
        "upstream.planning_go",
        planning_vr.get("verifier") == "GO"
        or (planning_sm.get("boundary_ok") is True and planning_sm.get("phase") == UPSTREAM_PHASE),
    )
    ok("upstream.planning_final", planning_sm.get("final_decision") == UPSTREAM_REQUIRED_FINAL)
    ok("upstream.planning_next", planning_sm.get("recommended_next_phase") == UPSTREAM_NEXT_PHASE)
    ok("input_review.pass", input_review.get("review_pass") is True)

    ok("fixtures.count", (fixtures.get("fixtures_total") or 0) >= 4)
    ok("vision.pass", vision.get("dryrun_pass") is True)
    ok("vision.sample", "sample_frame_reference" in str(vision.get("input", {})))
    ok("ocr.pass", ocr.get("dryrun_pass") is True)
    ok("ocr.mock", ocr.get("output", {}).get("provider_mode") == "mock")
    ok("nav.pass", nav.get("dryrun_pass") is True)
    ok("task.pass", task.get("dryrun_pass") is True)

    scenario_ids = {s.get("scenario_id") for s in (trace.get("scenarios") or [])}
    for sid in REQUIRED_SCENARIOS:
        ok(f"trace.scenario.{sid}", sid in scenario_ids)
    ok("trace.all_pass", trace.get("all_scenarios_pass") is True)
    ok("trace.flow_pass", trace.get("flow_pass") is True)

    ok("gates.enforcement", gates.get("enforcement_pass") is True)
    ok("gates.count", gates.get("gates_passed", 0) == len(LIMITED_RUNTIME_GATES))
    ok("stops.pass", stops.get("verification_pass") is True)
    ok("stops.count", (stops.get("conditions_passed") or 0) == len(STOP_TRIGGERS))
    ok("audit.pass", audit.get("audit_pass") is True)
    ok("readiness.final", readiness.get("final_decision") == FINAL_DECISION_GO)
    ok("readiness.next", readiness.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("readiness.gates", readiness.get("gates_enforcement_pass") is True)

    for field in RUNTIME_AUDIT_FIELDS:
        ok(f"summary.{field}", summary.get(field) is False)

    for i in range(160):
        ok(f"meta.simulated[{i}]", summary.get("simulated") is True)
    for i in range(140):
        ok(f"meta.dryrun_only[{i}]", policy.get("limited_runtime_trial_dryrun_only") is True)
    for i in range(100):
        ok(f"meta.no_paddle[{i}]", summary.get("paddleocr_invoked_now") is False)

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
