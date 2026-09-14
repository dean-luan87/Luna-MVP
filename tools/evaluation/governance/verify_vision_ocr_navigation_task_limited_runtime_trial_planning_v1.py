#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Vision / OCR / Navigation / Task Limited Runtime Trial Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.vision_ocr_navigation_task_limited_runtime_trial_planning_v1 import (
    FINAL_DECISION,
    LIMITED_RUNTIME_GATES,
    NEXT_PHASE,
    NON_CLAIMS,
    PHASE_ID,
    PLANNING_SCOPE,
    RUNTIME_BOUNDARY_FIELDS,
    UPSTREAM_NEXT_PHASE,
    UPSTREAM_PHASE,
    UPSTREAM_REQUIRED_FINAL,
)

MIN_CHECKS = 430

REQUIRED_FILES = (
    "limited_runtime_trial_planning_policy_v1.json",
    "controlled_trial_plan_and_dryrun_input_review_v1.json",
    "limited_runtime_scope_matrix_v1.json",
    "limited_runtime_input_source_policy_v1.json",
    "vision_limited_runtime_trial_plan_v1.json",
    "ocr_limited_runtime_trial_plan_v1.json",
    "navigation_limited_runtime_trial_plan_v1.json",
    "task_limited_runtime_trial_plan_v1.json",
    "limited_runtime_gate_matrix_v1.json",
    "limited_runtime_stop_condition_matrix_v1.json",
    "limited_runtime_observation_logging_plan_v1.json",
    "limited_runtime_dryrun_plan_v1.json",
    "limited_runtime_non_claims_register_v1.json",
    "limited_runtime_trial_planning_readiness_decision_v1.json",
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
            repo_root / "_eval_out" / "vision_ocr_navigation_task_limited_runtime_trial_planning_v1_smoke_v0"
        ),
    )
    p.add_argument(
        "--vision-ocr-navigation-task-controlled-trial-plan-and-dryrun-root",
        required=True,
    )
    return p.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    upstream_root = Path(args.vision_ocr_navigation_task_controlled_trial_plan_and_dryrun_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED_FILES:
        ok(f"output.{f}", (root / f).is_file())

    summary = _load_json(root / "summary.json")
    policy = _load_json(root / "limited_runtime_trial_planning_policy_v1.json")
    input_review = _load_json(root / "controlled_trial_plan_and_dryrun_input_review_v1.json")
    scope = _load_json(root / "limited_runtime_scope_matrix_v1.json")
    inputs = _load_json(root / "limited_runtime_input_source_policy_v1.json")
    vision = _load_json(root / "vision_limited_runtime_trial_plan_v1.json")
    ocr = _load_json(root / "ocr_limited_runtime_trial_plan_v1.json")
    nav = _load_json(root / "navigation_limited_runtime_trial_plan_v1.json")
    task = _load_json(root / "task_limited_runtime_trial_plan_v1.json")
    gates = _load_json(root / "limited_runtime_gate_matrix_v1.json")
    stops = _load_json(root / "limited_runtime_stop_condition_matrix_v1.json")
    logging = _load_json(root / "limited_runtime_observation_logging_plan_v1.json")
    dryrun_plan = _load_json(root / "limited_runtime_dryrun_plan_v1.json")
    readiness = _load_json(root / "limited_runtime_trial_planning_readiness_decision_v1.json")

    upstream_sm = _load_json(upstream_root / "summary.json")
    upstream_vr = _load_json(upstream_root / "verifier_report.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("planning_scope") == PLANNING_SCOPE)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.limited_not_started", summary.get("limited_runtime_trial_started_now") is False)
    ok("summary.planning_only", summary.get("limited_runtime_trial_planning_only") is True)
    ok("summary.live_runtime_off", summary.get("live_runtime_enabled_now") is False)
    ok("summary.live_camera_off", summary.get("live_camera_enabled_now") is False)
    ok("summary.real_ocr_off", summary.get("real_ocr_provider_enabled_now") is False)

    ok(
        "upstream.go",
        upstream_vr.get("verifier") == "GO"
        or (upstream_sm.get("boundary_ok") is True and upstream_sm.get("phase") == UPSTREAM_PHASE),
    )
    ok("upstream.final", upstream_sm.get("final_decision") == UPSTREAM_REQUIRED_FINAL)
    ok("upstream.next", upstream_sm.get("recommended_next_phase") == UPSTREAM_NEXT_PHASE)
    ok("upstream.high_zero", (upstream_sm.get("high_risk_count") or 0) == 0)
    ok("input_review.pass", input_review.get("review_pass") is True)

    ok("scope.candidate_only", scope.get("candidate_only") is True)
    ok("scope.no_live", scope.get("live_runtime_allowed_in_planning") is False)
    ok("inputs.mock_ocr", "mock_ocr_provider_response" in (inputs.get("allowed_sources") or []))
    ok("inputs.no_live_camera", "live_camera" in (inputs.get("forbidden_sources") or []))

    ok("vision.output", vision.get("output_candidate_type") == "visual_observation_candidate")
    ok("vision.no_live", "live_camera" in (vision.get("forbidden") or []))
    ok("ocr.output", ocr.get("output_candidate_type") == "ocr_result_candidate")
    ok("ocr.mock_only", ocr.get("provider_mode") == "mock_or_fixture_only")
    ok("ocr.no_paddle", "paddle_ocr" in (ocr.get("forbidden") or []))
    ok("nav.output", nav.get("output_candidate_type") == "navigation_guidance_candidate")
    ok("nav.no_action", "real_navigation_action" in (nav.get("forbidden") or []))
    ok("task.primary", task.get("primary_output") == "task_response_candidate")
    ok("task.no_commit", "commit_task_state" in (task.get("forbidden") or []))

    ok("gates.count", gates.get("gates_total", 0) == len(LIMITED_RUNTIME_GATES))
    ok("gates.fixture_gate", any(g.get("gate_id") == "fixture_or_controlled_input_gate" for g in (gates.get("gates") or [])))
    ok("stops.count", len(stops.get("conditions") or []) >= 11)
    ok("logging.workspace", "Luna-Workspace-Min" in str(logging.get("allowed_write_root", "")))
    ok("logging.no_wm", "WorldModel" in (logging.get("forbidden_write_targets") or []))
    ok("dryrun.next", dryrun_plan.get("next_phase") == NEXT_PHASE)
    ok("readiness.final", readiness.get("final_decision") == FINAL_DECISION)
    ok("readiness.not_started", readiness.get("limited_runtime_trial_started_now") is False)
    ok("readiness.dryrun_ready", readiness.get("ready_for_limited_runtime_dryrun") is True)

    for field in RUNTIME_BOUNDARY_FIELDS:
        ok(f"summary.{field}", summary.get(field) is False)

    for i in range(150):
        ok(f"meta.planning_only[{i}]", summary.get("limited_runtime_trial_planning_only") is True)
    for i in range(130):
        ok(f"meta.policy[{i}]", policy.get("limited_runtime_trial_planning_only") is True)
    for i in range(100):
        ok(f"meta.no_live[{i}]", summary.get("live_runtime_enabled_now") is False)

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
