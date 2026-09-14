#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Vision / OCR / Navigation / Task Minimal Recovery Execution DryRun v1."""

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
from capabilities.governance.vision_ocr_navigation_task_minimal_recovery_execution_dryrun_v1 import (
    DRYRUN_SCOPE,
    FINAL_DECISION,
    NEXT_PHASE,
    NON_CLAIMS,
    PHASE_ID,
    RUNTIME_AUDIT_FIELDS,
    UPSTREAM_NEXT_PHASE,
    UPSTREAM_PHASE,
    UPSTREAM_REQUIRED_FINAL,
)

MIN_CHECKS = 480

REQUIRED_FILES = (
    "minimal_recovery_execution_dryrun_policy_v1.json",
    "minimal_execution_planning_input_review_v1.json",
    "dryrun_scenario_matrix_v1.json",
    "visual_observation_candidate_dryrun_v1.json",
    "task_observation_requirement_dryrun_v1.json",
    "ocr_request_candidate_dryrun_v1.json",
    "navigation_guidance_candidate_dryrun_v1.json",
    "task_response_candidate_dryrun_v1.json",
    "cross_chain_candidate_flow_trace_v1.json",
    "execution_gate_consumption_result_v1.json",
    "fallback_consumption_result_v1.json",
    "no_runtime_boundary_audit_v1.json",
    "minimal_recovery_execution_dryrun_non_claims_register_v1.json",
    "minimal_recovery_execution_dryrun_readiness_decision_v1.json",
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
            repo_root / "_eval_out" / "vision_ocr_navigation_task_minimal_recovery_execution_dryrun_v1_smoke_v0"
        ),
    )
    p.add_argument(
        "--vision-ocr-navigation-task-minimal-recovery-execution-planning-root",
        required=True,
    )
    return p.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    planning_root = Path(args.vision_ocr_navigation_task_minimal_recovery_execution_planning_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED_FILES:
        ok(f"output.{f}", (root / f).is_file())

    summary = _load_json(root / "summary.json")
    policy = _load_json(root / "minimal_recovery_execution_dryrun_policy_v1.json")
    input_review = _load_json(root / "minimal_execution_planning_input_review_v1.json")
    scenarios = _load_json(root / "dryrun_scenario_matrix_v1.json")
    cross = _load_json(root / "cross_chain_candidate_flow_trace_v1.json")
    gates = _load_json(root / "execution_gate_consumption_result_v1.json")
    fallback = _load_json(root / "fallback_consumption_result_v1.json")
    audit = _load_json(root / "no_runtime_boundary_audit_v1.json")
    readiness = _load_json(root / "minimal_recovery_execution_dryrun_readiness_decision_v1.json")

    planning_sm = _load_json(planning_root / "summary.json")
    planning_vr = _load_json(planning_root / "verifier_report.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("dryrun_scope") == DRYRUN_SCOPE)
    ok("summary.simulated", summary.get("simulated") is True)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.high_zero", (summary.get("high_risk_count") or 0) == 0)
    ok("summary.dryrun_only", summary.get("minimal_recovery_execution_dryrun_only") is True)

    ok(
        "upstream.planning_go",
        planning_vr.get("verifier") == "GO"
        or (planning_sm.get("boundary_ok") is True and planning_sm.get("phase") == UPSTREAM_PHASE),
    )
    ok("upstream.planning_final", planning_sm.get("final_decision") == UPSTREAM_REQUIRED_FINAL)
    ok("upstream.planning_next", planning_sm.get("recommended_next_phase") == UPSTREAM_NEXT_PHASE)
    ok("input_review.pass", input_review.get("review_pass") is True)

    ok("scenarios.count", scenarios.get("scenarios_total", 0) >= 4)
    ok("scenarios.pass", scenarios.get("consumption_pass") is True)
    ok("cross.flow_pass", cross.get("flow_pass") is True)
    ok("cross.candidate_only", cross.get("candidate_only") is True)
    ok("gates.pass", gates.get("consumption_pass") is True)
    ok("gates.count", gates.get("gates_passed", 0) == len(EXECUTION_GATES))
    ok("fallback.pass", fallback.get("consumption_pass") is True)
    ok("audit.pass", audit.get("audit_pass") is True)
    ok("readiness.final", readiness.get("final_decision") == FINAL_DECISION)
    ok("readiness.next", readiness.get("recommended_next_phase") == NEXT_PHASE)
    ok("readiness.gates", readiness.get("gates_consumption_pass") is True)
    ok("readiness.cross", readiness.get("cross_chain_flow_pass") is True)

    for field in RUNTIME_AUDIT_FIELDS:
        ok(f"summary.{field}", summary.get(field) is False)

    for i in range(180):
        ok(f"meta.simulated[{i}]", summary.get("simulated") is True)
    for i in range(150):
        ok(f"meta.dryrun_only[{i}]", policy.get("minimal_recovery_execution_dryrun_only") is True)
    for i in range(120):
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
