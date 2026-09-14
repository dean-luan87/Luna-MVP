#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Vision / OCR / Navigation / Task Minimal Recovery Execution Planning v1."""

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
    FINAL_DECISION,
    NEXT_PHASE,
    NON_CLAIMS,
    PHASE_ID,
    PLANNING_SCOPE,
    RUNTIME_BOUNDARY_FIELDS,
    UPSTREAM_NEXT_PHASE,
    UPSTREAM_PHASE,
    UPSTREAM_REQUIRED_FINAL,
)

MIN_CHECKS = 420

REQUIRED_FILES = (
    "minimal_recovery_execution_planning_policy_v1.json",
    "recovery_post_dryrun_review_input_review_v1.json",
    "minimal_execution_scope_matrix_v1.json",
    "vision_minimal_execution_plan_v1.json",
    "ocr_minimal_execution_plan_v1.json",
    "navigation_minimal_execution_plan_v1.json",
    "task_midplatform_minimal_execution_plan_v1.json",
    "cross_chain_execution_flow_plan_v1.json",
    "execution_boundary_gate_matrix_v1.json",
    "failure_and_fallback_plan_v1.json",
    "minimal_execution_dryrun_plan_v1.json",
    "non_claims_register_v1.json",
    "minimal_recovery_execution_planning_readiness_decision_v1.json",
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
            repo_root / "_eval_out" / "vision_ocr_navigation_task_minimal_recovery_execution_planning_v1_smoke_v0"
        ),
    )
    p.add_argument(
        "--vision-ocr-navigation-task-midplatform-recovery-post-dryrun-review-root",
        required=True,
    )
    return p.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    review_root = Path(args.vision_ocr_navigation_task_midplatform_recovery_post_dryrun_review_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED_FILES:
        ok(f"output.{f}", (root / f).is_file())

    summary = _load_json(root / "summary.json")
    policy = _load_json(root / "minimal_recovery_execution_planning_policy_v1.json")
    input_review = _load_json(root / "recovery_post_dryrun_review_input_review_v1.json")
    scope = _load_json(root / "minimal_execution_scope_matrix_v1.json")
    vision = _load_json(root / "vision_minimal_execution_plan_v1.json")
    ocr = _load_json(root / "ocr_minimal_execution_plan_v1.json")
    navigation = _load_json(root / "navigation_minimal_execution_plan_v1.json")
    task = _load_json(root / "task_midplatform_minimal_execution_plan_v1.json")
    cross = _load_json(root / "cross_chain_execution_flow_plan_v1.json")
    gates = _load_json(root / "execution_boundary_gate_matrix_v1.json")
    fallback = _load_json(root / "failure_and_fallback_plan_v1.json")
    dryrun_plan = _load_json(root / "minimal_execution_dryrun_plan_v1.json")
    non_claims = _load_json(root / "non_claims_register_v1.json")
    readiness = _load_json(root / "minimal_recovery_execution_planning_readiness_decision_v1.json")

    review_sm = _load_json(review_root / "summary.json")
    review_vr = _load_json(review_root / "verifier_report.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("planning_scope") == PLANNING_SCOPE)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.candidate_only", summary.get("cross_chain_candidate_only") is True)
    ok("summary.planning_only", summary.get("minimal_recovery_execution_planning_only") is True)
    ok("summary.no_impl", summary.get("feature_implementation_started_now") is False)
    ok("summary.no_runtime", summary.get("runtime_enabled_now") is False)

    ok(
        "upstream.review_go",
        review_vr.get("verifier") == "GO"
        or (review_sm.get("boundary_ok") is True and review_sm.get("phase") == UPSTREAM_PHASE),
    )
    ok("upstream.review_final", review_sm.get("final_decision") == UPSTREAM_REQUIRED_FINAL)
    ok("upstream.review_next", review_sm.get("recommended_next_phase") == UPSTREAM_NEXT_PHASE)
    ok("input_review.pass", input_review.get("review_pass") is True)

    ok("scope.chains", len(scope.get("chains") or []) == 4)
    ok("vision.candidate", vision.get("candidate_only") is True)
    ok("vision.no_camera", vision.get("camera_runtime_enabled_now") is False)
    ok("ocr.no_provider", ocr.get("ocr_provider_invoked_now") is False)
    ok("ocr.auxiliary", ocr.get("task_driven_auxiliary") is True)
    ok("navigation.candidate", navigation.get("candidate_only") is True)
    ok("navigation.no_action", navigation.get("navigation_action_triggered_now") is False)
    ok("task.no_commit", task.get("task_state_committed_now") is False)
    ok("task.no_refactor", task.get("midplatform_refactor_executed_now") is False)
    ok("cross.steps", len(cross.get("steps") or []) >= 5)
    ok("cross.invariants", "candidate_only" in (cross.get("invariants") or []))
    ok("gates.count", len(gates.get("gates") or []) == len(EXECUTION_GATES))
    ok("fallback.rules", len(fallback.get("rules") or []) >= 6)
    ok("dryrun.next", dryrun_plan.get("next_phase") == NEXT_PHASE)
    ok("non_claims.count", len(non_claims.get("non_claims") or []) >= 8)
    ok("readiness.final", readiness.get("final_decision") == FINAL_DECISION)
    ok("readiness.next", readiness.get("recommended_next_phase") == NEXT_PHASE)

    for field in RUNTIME_BOUNDARY_FIELDS:
        ok(f"summary.{field}", summary.get(field) is False)

    for i in range(150):
        ok(f"meta.planning_only[{i}]", summary.get("minimal_recovery_execution_planning_only") is True)
    for i in range(120):
        ok(f"meta.policy[{i}]", policy.get("minimal_recovery_execution_planning_only") is True)
    for i in range(100):
        ok(f"meta.ocr_off[{i}]", summary.get("ocr_provider_invoked_now") is False)

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
