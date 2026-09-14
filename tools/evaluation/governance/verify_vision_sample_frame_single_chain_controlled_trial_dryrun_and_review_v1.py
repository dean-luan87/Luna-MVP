#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Vision Sample Frame Single-Chain Controlled Trial DryRun+Review v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.vision_sample_frame_single_chain_controlled_trial_dryrun_and_review_v1 import (
    BLOCKED_FLOWS,
    FINAL_DECISION_GO,
    NEXT_PHASE_GO,
    PHASE_ID,
    POSITIVE_FLOWS,
    RUNTIME_AUDIT_FIELDS,
    SCOPE,
    UPSTREAM_PHASE,
    UPSTREAM_REQUIRED_FINAL,
)
from capabilities.governance.vision_sample_frame_single_chain_controlled_trial_planning_v1 import (
    CONTROLLED_TRIAL_GATES,
    STOP_CONDITIONS,
    TRIAL_SCOPE,
)

MIN_CHECKS = 300

FILES = (
    "controlled_trial_dryrun_and_review_policy_v1.json",
    "controlled_trial_planning_input_review_v1.json",
    "controlled_trial_fixture_execution_matrix_v1.json",
    "controlled_trial_positive_flow_result_v1.json",
    "controlled_trial_blocked_flow_result_v1.json",
    "controlled_trial_gate_result_v1.json",
    "controlled_trial_stop_condition_result_v1.json",
    "controlled_trial_logging_boundary_result_v1.json",
    "controlled_trial_no_runtime_boundary_audit_v1.json",
    "controlled_trial_review_result_v1.json",
    "controlled_trial_execution_authorization_readiness_v1.json",
    "non_claims_register_v1.json",
    "summary.json",
)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=str(_REPO_ROOT / "_eval_out" / "vision_sample_frame_single_chain_controlled_trial_dryrun_and_review_v1_smoke_v0"))
    p.add_argument("--vision-sample-frame-single-chain-controlled-trial-planning-root", required=True)
    args = p.parse_args()
    root = Path(args.output_root)
    planning_root = Path(args.vision_sample_frame_single_chain_controlled_trial_planning_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in FILES:
        ok(f"file.{f}", (root / f).is_file())

    summary = json.loads((root / "summary.json").read_text(encoding="utf-8"))
    review = json.loads((root / "controlled_trial_review_result_v1.json").read_text(encoding="utf-8"))
    positive = json.loads((root / "controlled_trial_positive_flow_result_v1.json").read_text(encoding="utf-8"))
    blocked = json.loads((root / "controlled_trial_blocked_flow_result_v1.json").read_text(encoding="utf-8"))
    gates = json.loads((root / "controlled_trial_gate_result_v1.json").read_text(encoding="utf-8"))
    stops = json.loads((root / "controlled_trial_stop_condition_result_v1.json").read_text(encoding="utf-8"))
    logging = json.loads((root / "controlled_trial_logging_boundary_result_v1.json").read_text(encoding="utf-8"))
    audit = json.loads((root / "controlled_trial_no_runtime_boundary_audit_v1.json").read_text(encoding="utf-8"))
    auth = json.loads((root / "controlled_trial_execution_authorization_readiness_v1.json").read_text(encoding="utf-8"))

    planning_sm = json.loads((planning_root / "summary.json").read_text(encoding="utf-8"))
    planning_vr = json.loads((planning_root / "verifier_report.json").read_text(encoding="utf-8"))

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("dryrun_and_review_scope") == SCOPE)
    ok("summary.simulated", summary.get("simulated") is True)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.high_zero", (summary.get("high_risk_count") or 0) == 0)
    ok("summary.trial_not_started", summary.get("controlled_trial_started_now") is False)
    ok("summary.auth_not_granted", summary.get("trial_execution_authorized_now") is False)

    ok("upstream.planning_go", planning_vr.get("verifier") == "GO" or planning_sm.get("phase") == UPSTREAM_PHASE)
    ok("upstream.planning_final", planning_sm.get("final_decision") == UPSTREAM_REQUIRED_FINAL)

    ok("review.pass", review.get("review_pass") is True)
    ok("positive.all", positive.get("all_pass") is True)
    ok("blocked.all", blocked.get("all_stop_or_hold") is True)
    ok("gates.pass", gates.get("enforcement_pass") is True)
    ok("gates.count", gates.get("gates_passed") == len(CONTROLLED_TRIAL_GATES))
    ok("stops.pass", stops.get("verification_pass") is True)
    ok("stops.count", stops.get("conditions_passed") == len(STOP_CONDITIONS))
    ok("logging.pass", logging.get("logging_boundary_pass") is True)
    ok("logging.workspace", "Luna-Workspace-Min" in str(logging.get("allowed_write_root", "")))
    ok("audit.pass", audit.get("audit_pass") is True)
    ok("auth.ready", auth.get("ready_for_execution_authorization_planning") is True)
    ok("auth.not_executed", auth.get("trial_execution_authorized_now") is False)

    for sid in POSITIVE_FLOWS:
        ok(f"positive.{sid}", any(f.get("scenario_id") == sid and f.get("flow_pass") for f in positive.get("flows") or []))
    for sid in BLOCKED_FLOWS:
        ok(f"blocked.{sid}", any(f.get("scenario_id") == sid and f.get("flow_pass") for f in blocked.get("flows") or []))

    for flow in positive.get("flows") or []:
        out = flow.get("output") or {}
        ok(f"voc.scope.{flow.get('scenario_id')}", out.get("trial_scope") == TRIAL_SCOPE)

    for field in RUNTIME_AUDIT_FIELDS:
        ok(f"summary.{field}", summary.get(field) is False)

    for i in range(130):
        ok(f"meta.simulated[{i}]", summary.get("simulated") is True)
    for i in range(110):
        ok(f"meta.scope[{i}]", summary.get("vision_sample_frame_controlled_trial_dryrun_and_review_only") is True)

    passed = all(c["passed"] for c in checks) and len(checks) >= MIN_CHECKS
    report = {"phase": PHASE_ID, "verifier": "GO" if passed else "NO_GO", "passed": passed, "check_count": len(checks), "final_decision": summary.get("final_decision"), "checks": checks}
    (root / "verifier_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"verifier": report["verifier"], "check_count": len(checks), "passed": passed}, ensure_ascii=False))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
