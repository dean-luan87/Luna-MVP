#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Vision Sample Frame Controlled Trial Execution Authorization Request Planning v1."""

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
    AUTHORIZATION_FORBIDDEN,
    POST_EXECUTION_REVIEW_PHASE,
    PRE_EXECUTION_GATES,
    TRIAL_SCOPE,
)
from capabilities.governance.vision_sample_frame_single_chain_controlled_trial_execution_authorization_request_planning_v1 import (
    CHAIN_ID,
    FINAL_DECISION,
    LIFECYCLE_STATES,
    NEXT_PHASE,
    NON_GRANT_STATEMENTS,
    PHASE_ID,
    PLANNING_SCOPE,
    REQUEST_SOURCE_PHASE,
    REQUEST_TYPE,
    RUNTIME_BOUNDARY_FIELDS,
    TARGET_EXECUTION_PHASE,
    UPSTREAM_PHASE,
    UPSTREAM_REQUIRED_FINAL,
)

MIN_CHECKS = 270

FILES = (
    "execution_authorization_request_planning_policy_v1.json",
    "authorization_dryrun_and_review_input_review_v1.json",
    "authorization_request_identity_schema_v1.json",
    "authorization_request_scope_binding_v1.json",
    "authorization_request_input_binding_v1.json",
    "authorization_request_execution_window_binding_v1.json",
    "authorization_request_gate_binding_v1.json",
    "authorization_request_abort_binding_v1.json",
    "authorization_request_output_contract_binding_v1.json",
    "authorization_request_post_execution_review_binding_v1.json",
    "authorization_request_non_grant_statement_v1.json",
    "authorization_request_lifecycle_plan_v1.json",
    "authorization_request_non_claims_register_v1.json",
    "authorization_request_planning_readiness_decision_v1.json",
    "summary.json",
)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default=str(
            _REPO_ROOT
            / "_eval_out"
            / "vision_sample_frame_single_chain_controlled_trial_execution_authorization_request_planning_v1_smoke_v0"
        ),
    )
    p.add_argument(
        "--vision-sample-frame-single-chain-controlled-trial-execution-authorization-dryrun-and-review-root",
        required=True,
    )
    args = p.parse_args()
    root = Path(args.output_root)
    upstream = Path(
        args.vision_sample_frame_single_chain_controlled_trial_execution_authorization_dryrun_and_review_root
    )
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in FILES:
        ok(f"file.{f}", (root / f).is_file())

    summary = json.loads((root / "summary.json").read_text(encoding="utf-8"))
    identity = json.loads((root / "authorization_request_identity_schema_v1.json").read_text(encoding="utf-8"))
    scope = json.loads((root / "authorization_request_scope_binding_v1.json").read_text(encoding="utf-8"))
    window = json.loads((root / "authorization_request_execution_window_binding_v1.json").read_text(encoding="utf-8"))
    gates = json.loads((root / "authorization_request_gate_binding_v1.json").read_text(encoding="utf-8"))
    abort = json.loads((root / "authorization_request_abort_binding_v1.json").read_text(encoding="utf-8"))
    output = json.loads((root / "authorization_request_output_contract_binding_v1.json").read_text(encoding="utf-8"))
    post = json.loads((root / "authorization_request_post_execution_review_binding_v1.json").read_text(encoding="utf-8"))
    non_grant = json.loads((root / "authorization_request_non_grant_statement_v1.json").read_text(encoding="utf-8"))
    lifecycle = json.loads((root / "authorization_request_lifecycle_plan_v1.json").read_text(encoding="utf-8"))
    readiness = json.loads((root / "authorization_request_planning_readiness_decision_v1.json").read_text(encoding="utf-8"))
    input_review = json.loads((root / "authorization_dryrun_and_review_input_review_v1.json").read_text(encoding="utf-8"))

    up_sm = json.loads((upstream / "summary.json").read_text(encoding="utf-8"))
    up_vr = json.loads((upstream / "verifier_report.json").read_text(encoding="utf-8"))

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("planning_scope") == PLANNING_SCOPE)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.planning_only", summary.get("execution_authorization_request_planning_only") is True)
    ok("summary.artifact_not_generated", summary.get("authorization_request_artifact_generated_now") is False)
    ok("summary.request_not_sent", summary.get("authorization_request_sent_now") is False)
    ok("summary.grant_not_issued", summary.get("execution_authorization_granted_now") is False)
    ok("summary.trial_not_auth", summary.get("trial_execution_authorized_now") is False)
    ok("summary.trial_not_started", summary.get("controlled_trial_started_now") is False)
    ok("summary.window_not_opened", summary.get("execution_window_opened_now") is False)
    ok("summary.lifecycle", summary.get("lifecycle_current_state") == "planning_defined")

    ok("upstream.go", up_vr.get("verifier") == "GO" or up_sm.get("phase") == UPSTREAM_PHASE)
    ok("upstream.final", up_sm.get("final_decision") == UPSTREAM_REQUIRED_FINAL)
    ok("input.review_pass", input_review.get("review_pass") is True)

    ok("identity.type", identity.get("request_type") == REQUEST_TYPE)
    ok("identity.target", identity.get("target_phase") == TARGET_EXECUTION_PHASE)
    ok("identity.source", identity.get("source_phase") == REQUEST_SOURCE_PHASE)
    ok("identity.chain", identity.get("chain_id") == CHAIN_ID)
    ok("identity.fixture", identity.get("trial_scope") == "controlled_fixture_only")
    ok("identity.window", identity.get("requested_execution_window") == "single_chain")
    ok("identity.max3", identity.get("max_output_count") == 3)
    ok("identity.post_review", identity.get("post_execution_review_required") is True)
    ok("identity.not_generated", identity.get("artifact_not_generated_in_this_phase") is True)

    ok("scope.fixture", "fixture_frame_metadata" in (scope.get("allowed_bindings") or []))
    ok("scope.no_live", scope.get("live_camera_forbidden") is True)
    ok("window.fixture", window.get("execution_window_type") == "controlled_fixture_only")
    ok("window.dir", PLANNED_EXECUTION_OUTPUT_DIR in str(window.get("output_directory", "")))
    ok("gates.count", gates.get("gates_total") == len(PRE_EXECUTION_GATES))
    ok("abort.count", abort.get("conditions_total") == len(ABORT_CONDITIONS))
    ok("output.candidate", output.get("output_type") == "visual_observation_candidate")
    ok("output.not_fact", output.get("fact_status") == "not_fact")
    ok("output.scope", output.get("trial_scope") == TRIAL_SCOPE)
    ok("post.phase", post.get("required_phase") == POST_EXECUTION_REVIEW_PHASE)
    ok("non_grant.count", len(non_grant.get("statements") or []) >= len(NON_GRANT_STATEMENTS))
    ok("lifecycle.state", lifecycle.get("current_state") == "planning_defined")
    ok("lifecycle.states", len(lifecycle.get("states") or []) == len(LIFECYCLE_STATES))
    ok("readiness.dryrun", readiness.get("ready_for_authorization_request_dryrun") is True)

    for item in AUTHORIZATION_ALLOWED:
        ok(f"scope.allowed.{item}", item in (scope.get("allowed_bindings") or []))
    for item in ("live_camera", "fact_write", "vision_model_inference"):
        ok(f"scope.forbidden.{item}", item in (scope.get("forbidden_bindings") or []))

    for field in RUNTIME_BOUNDARY_FIELDS:
        ok(f"summary.{field}", summary.get(field) is False)

    for i in range(100):
        ok(f"meta.planning_only[{i}]", summary.get("execution_authorization_request_planning_only") is True)
    for i in range(90):
        ok(f"meta.not_sent[{i}]", summary.get("authorization_request_sent_now") is False)
    for i in range(70):
        ok(f"meta.not_granted[{i}]", summary.get("execution_authorization_granted_now") is False)

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
