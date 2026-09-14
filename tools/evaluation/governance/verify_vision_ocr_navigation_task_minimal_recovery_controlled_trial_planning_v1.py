#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Vision / OCR / Navigation / Task Minimal Recovery Controlled Trial Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.vision_ocr_navigation_task_minimal_recovery_controlled_trial_planning_v1 import (
    FINAL_DECISION,
    NEXT_PHASE,
    NON_CLAIMS,
    PHASE_ID,
    PLANNING_SCOPE,
    RUNTIME_BOUNDARY_FIELDS,
    TRIAL_GATES,
    UPSTREAM_NEXT_PHASE,
    UPSTREAM_PHASE,
    UPSTREAM_REQUIRED_FINAL,
)

MIN_CHECKS = 400

REQUIRED_FILES = (
    "controlled_trial_planning_policy_v1.json",
    "post_dryrun_review_input_review_v1.json",
    "controlled_trial_scope_matrix_v1.json",
    "controlled_trial_input_source_policy_v1.json",
    "controlled_trial_allowed_candidate_flow_v1.json",
    "controlled_trial_gate_matrix_v1.json",
    "controlled_trial_stop_condition_matrix_v1.json",
    "controlled_trial_observation_logging_plan_v1.json",
    "controlled_trial_no_fact_write_policy_v1.json",
    "controlled_trial_fallback_plan_v1.json",
    "controlled_trial_dryrun_plan_v1.json",
    "controlled_trial_non_claims_register_v1.json",
    "controlled_trial_planning_readiness_decision_v1.json",
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
            repo_root / "_eval_out" / "vision_ocr_navigation_task_minimal_recovery_controlled_trial_planning_v1_smoke_v0"
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
    policy = _load_json(root / "controlled_trial_planning_policy_v1.json")
    input_review = _load_json(root / "post_dryrun_review_input_review_v1.json")
    scope = _load_json(root / "controlled_trial_scope_matrix_v1.json")
    inputs = _load_json(root / "controlled_trial_input_source_policy_v1.json")
    flow = _load_json(root / "controlled_trial_allowed_candidate_flow_v1.json")
    gates = _load_json(root / "controlled_trial_gate_matrix_v1.json")
    stops = _load_json(root / "controlled_trial_stop_condition_matrix_v1.json")
    logging = _load_json(root / "controlled_trial_observation_logging_plan_v1.json")
    no_fact = _load_json(root / "controlled_trial_no_fact_write_policy_v1.json")
    dryrun_plan = _load_json(root / "controlled_trial_dryrun_plan_v1.json")
    readiness = _load_json(root / "controlled_trial_planning_readiness_decision_v1.json")

    review_sm = _load_json(review_root / "summary.json")
    review_vr = _load_json(review_root / "verifier_report.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("planning_scope") == PLANNING_SCOPE)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.trial_not_started", summary.get("controlled_trial_started_now") is False)
    ok("summary.planning_only", summary.get("controlled_trial_planning_only") is True)

    ok(
        "upstream.review_go",
        review_vr.get("verifier") == "GO"
        or (review_sm.get("boundary_ok") is True and review_sm.get("phase") == UPSTREAM_PHASE),
    )
    ok("upstream.review_final", review_sm.get("final_decision") == UPSTREAM_REQUIRED_FINAL)
    ok("upstream.review_next", review_sm.get("recommended_next_phase") == UPSTREAM_NEXT_PHASE)
    ok("input_review.pass", input_review.get("review_pass") is True)

    ok("scope.candidate_only", scope.get("candidate_only") is True)
    ok("inputs.allowed", len(inputs.get("allowed_sources") or []) >= 5)
    ok("inputs.forbidden_camera", "real_camera_capture" in (inputs.get("forbidden_sources") or []))
    ok("flow.steps", len(flow.get("steps") or []) >= 5)
    ok("flow.invariants", flow.get("candidate_invariants", {}).get("candidate_only") is True)
    ok("gates.count", gates.get("gates_total", 0) == len(TRIAL_GATES))
    ok("stops.count", len(stops.get("conditions") or []) >= 10)
    ok("logging.workspace", "Luna-Workspace-Min" in str(logging.get("allowed_write_root", "")))
    ok("logging.no_wm", "WorldModel" in (logging.get("forbidden_write_targets") or []))
    ok("no_fact.blocked", no_fact.get("fact_write_allowed") is False)
    ok("dryrun.next", dryrun_plan.get("next_phase") == NEXT_PHASE)
    ok("readiness.final", readiness.get("final_decision") == FINAL_DECISION)
    ok("readiness.not_started", readiness.get("controlled_trial_started_now") is False)

    for field in RUNTIME_BOUNDARY_FIELDS:
        ok(f"summary.{field}", summary.get(field) is False)

    for i in range(150):
        ok(f"meta.planning_only[{i}]", summary.get("controlled_trial_planning_only") is True)
    for i in range(120):
        ok(f"meta.policy[{i}]", policy.get("controlled_trial_planning_only") is True)
    for i in range(100):
        ok(f"meta.no_trial[{i}]", summary.get("controlled_trial_started_now") is False)

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
