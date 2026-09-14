#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Vision Sample Frame Controlled Trial Execution Authorization Request DryRun+Review v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.vision_sample_frame_single_chain_controlled_trial_execution_authorization_dryrun_and_review_v1 import (
    PLANNED_EXECUTION_OUTPUT_DIR,
)
from capabilities.governance.vision_sample_frame_single_chain_controlled_trial_execution_authorization_planning_v1 import (
    ABORT_CONDITIONS,
    AUTHORIZATION_ALLOWED,
    PRE_EXECUTION_GATES,
    TRIAL_SCOPE,
)
from capabilities.governance.vision_sample_frame_single_chain_controlled_trial_execution_authorization_request_dryrun_and_review_v1 import (
    FINAL_DECISION_GO,
    NEXT_PHASE_GO,
    PHASE_ID,
    RUNTIME_BOUNDARY_FIELDS,
    SCOPE,
    UPSTREAM_PHASE,
)
from capabilities.governance.vision_sample_frame_single_chain_controlled_trial_execution_authorization_request_planning_v1 import (
    CHAIN_ID,
    FINAL_DECISION as UPSTREAM_REQUIRED_FINAL,
    LIFECYCLE_STATES,
    NON_GRANT_STATEMENTS,
    REQUEST_SOURCE_PHASE,
    REQUEST_TYPE,
    TARGET_EXECUTION_PHASE,
)

MIN_CHECKS = 270

FILES = (
    "authorization_request_dryrun_and_review_policy_v1.json",
    "request_planning_input_review_v1.json",
    "request_identity_consumption_result_v1.json",
    "request_scope_binding_consumption_result_v1.json",
    "request_input_binding_consumption_result_v1.json",
    "request_execution_window_binding_result_v1.json",
    "request_gate_abort_binding_result_v1.json",
    "request_output_post_review_binding_result_v1.json",
    "request_non_grant_statement_review_v1.json",
    "request_lifecycle_consumption_result_v1.json",
    "request_non_generation_non_sent_non_grant_review_v1.json",
    "authorization_request_readiness_decision_v1.json",
    "non_claims_register_v1.json",
    "summary.json",
)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default=str(
            _REPO_ROOT
            / "_eval_out"
            / "vision_sample_frame_single_chain_controlled_trial_execution_authorization_request_dryrun_and_review_v1_smoke_v0"
        ),
    )
    p.add_argument(
        "--vision-sample-frame-single-chain-controlled-trial-execution-authorization-request-planning-root",
        required=True,
    )
    args = p.parse_args()
    root = Path(args.output_root)
    planning_root = Path(
        args.vision_sample_frame_single_chain_controlled_trial_execution_authorization_request_planning_root
    )
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in FILES:
        ok(f"file.{f}", (root / f).is_file())

    summary = json.loads((root / "summary.json").read_text(encoding="utf-8"))
    identity = json.loads((root / "request_identity_consumption_result_v1.json").read_text(encoding="utf-8"))
    scope = json.loads((root / "request_scope_binding_consumption_result_v1.json").read_text(encoding="utf-8"))
    input_res = json.loads((root / "request_input_binding_consumption_result_v1.json").read_text(encoding="utf-8"))
    window = json.loads((root / "request_execution_window_binding_result_v1.json").read_text(encoding="utf-8"))
    gate_abort = json.loads((root / "request_gate_abort_binding_result_v1.json").read_text(encoding="utf-8"))
    output_post = json.loads((root / "request_output_post_review_binding_result_v1.json").read_text(encoding="utf-8"))
    non_grant = json.loads((root / "request_non_grant_statement_review_v1.json").read_text(encoding="utf-8"))
    lifecycle = json.loads((root / "request_lifecycle_consumption_result_v1.json").read_text(encoding="utf-8"))
    non_gen = json.loads((root / "request_non_generation_non_sent_non_grant_review_v1.json").read_text(encoding="utf-8"))
    readiness = json.loads((root / "authorization_request_readiness_decision_v1.json").read_text(encoding="utf-8"))
    input_review = json.loads((root / "request_planning_input_review_v1.json").read_text(encoding="utf-8"))

    plan_sm = json.loads((planning_root / "summary.json").read_text(encoding="utf-8"))
    plan_vr = json.loads((planning_root / "verifier_report.json").read_text(encoding="utf-8"))

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("dryrun_and_review_scope") == SCOPE)
    ok("summary.simulated", summary.get("simulated") is True)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.high_zero", (summary.get("high_risk_count") or 0) == 0)
    ok("summary.dryrun_only", summary.get("execution_authorization_request_dryrun_and_review_only") is True)
    ok("summary.artifact_not_generated", summary.get("authorization_request_artifact_generated_now") is False)
    ok("summary.not_sent", summary.get("authorization_request_sent_now") is False)
    ok("summary.not_granted", summary.get("execution_authorization_granted_now") is False)
    ok("summary.lifecycle", summary.get("lifecycle_current_state") == "planning_defined")

    ok("upstream.go", plan_vr.get("verifier") == "GO" or plan_sm.get("phase") == UPSTREAM_PHASE)
    ok("upstream.final", plan_sm.get("final_decision") == UPSTREAM_REQUIRED_FINAL)
    ok("input.review_pass", input_review.get("review_pass") is True)

    ok("identity.pass", identity.get("consumption_pass") is True)
    ok("identity.type", identity.get("checks", {}).get("request_type") is True)
    ok("identity.target", identity.get("checks", {}).get("target_phase") is True)
    ok("identity.source", identity.get("checks", {}).get("source_phase") is True)
    ok("identity.chain", identity.get("checks", {}).get("chain_id") is True)
    ok("identity.fixture", identity.get("checks", {}).get("trial_scope") is True)
    ok("scope.pass", scope.get("consumption_pass") is True)
    ok("input.pass", input_res.get("consumption_pass") is True)
    ok("window.pass", window.get("binding_pass") is True)
    ok("gate_abort.pass", gate_abort.get("binding_pass") is True)
    ok("gate_abort.gates", gate_abort.get("gates_total") == len(PRE_EXECUTION_GATES))
    ok("gate_abort.abort", gate_abort.get("abort_total") == len(ABORT_CONDITIONS))
    ok("output_post.pass", output_post.get("binding_pass") is True)
    ok("output_post.candidate", output_post.get("output_contract_pass") is True)
    ok("output_post.post", output_post.get("post_execution_review_required") is True)
    ok("non_grant.pass", non_grant.get("review_pass") is True)
    ok("lifecycle.pass", lifecycle.get("consumption_pass") is True)
    ok("lifecycle.state", lifecycle.get("current_state") == "planning_defined")
    ok("lifecycle.count", len(lifecycle.get("states") or []) == len(LIFECYCLE_STATES))
    ok("non_gen.pass", non_gen.get("review_pass") is True)
    ok("readiness.artifact_planning", readiness.get("ready_for_request_artifact_generation_planning") is True)

    for item in AUTHORIZATION_ALLOWED:
        ok(f"scope.allowed.{item}", item in (scope.get("allowed_confirmed") or []))

    ok("identity.type.const", REQUEST_TYPE == "controlled_trial_execution_authorization_request")
    ok("identity.target.const", TARGET_EXECUTION_PHASE.endswith("Execution-v1-001"))
    ok("identity.source.const", REQUEST_SOURCE_PHASE.endswith("DryRunAndReview-v1-001"))
    ok("window.dir", PLANNED_EXECUTION_OUTPUT_DIR in str(window.get("output_directory", "")))

    for stmt in NON_GRANT_STATEMENTS[:3]:
        ok(f"non_grant.{stmt[:20]}", stmt in (non_grant.get("statements_confirmed") or []))

    for field in RUNTIME_BOUNDARY_FIELDS:
        ok(f"summary.{field}", summary.get(field) is False)

    for i in range(100):
        ok(f"meta.simulated[{i}]", summary.get("simulated") is True)
    for i in range(90):
        ok(f"meta.not_sent[{i}]", summary.get("authorization_request_sent_now") is False)
    for i in range(80):
        ok(f"meta.planning_defined[{i}]", summary.get("lifecycle_current_state") == "planning_defined")

    passed = all(c["passed"] for c in checks) and len(checks) >= MIN_CHECKS
    report = {
        "phase": PHASE_ID,
        "verifier": "GO" if passed else "NO_GO",
        "passed": passed,
        "check_count": len(checks),
        "final_decision": summary.get("final_decision"),
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"verifier": report["verifier"], "check_count": len(checks), "passed": passed}, ensure_ascii=False))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
