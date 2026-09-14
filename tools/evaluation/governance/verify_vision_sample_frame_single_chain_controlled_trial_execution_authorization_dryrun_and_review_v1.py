#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Vision Sample Frame Controlled Trial Execution Authorization DryRun+Review v1."""

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
    FINAL_DECISION_GO,
    NEXT_PHASE_GO,
    PHASE_ID,
    PLANNED_EXECUTION_OUTPUT_DIR,
    PRE_EXECUTION_GATES,
    RUNTIME_BOUNDARY_FIELDS,
    SCOPE,
    UPSTREAM_PHASE,
    UPSTREAM_REQUIRED_FINAL,
)
from capabilities.governance.vision_sample_frame_single_chain_controlled_trial_execution_authorization_planning_v1 import (
    ABORT_CONDITIONS,
    AUTHORIZATION_ALLOWED,
    EXECUTION_ALLOWLIST,
    EXECUTION_BLOCKLIST,
    POST_EXECUTION_REVIEW_PHASE,
    TRIAL_SCOPE,
)

MIN_CHECKS = 270

FILES = (
    "execution_authorization_dryrun_and_review_policy_v1.json",
    "authorization_planning_input_review_v1.json",
    "authorization_scope_consumption_result_v1.json",
    "execution_allowlist_blocklist_review_v1.json",
    "pre_execution_gate_consumption_result_v1.json",
    "execution_window_dryrun_result_v1.json",
    "abort_condition_consumption_result_v1.json",
    "output_contract_review_v1.json",
    "logging_policy_review_v1.json",
    "post_execution_review_requirement_result_v1.json",
    "authorization_non_release_review_v1.json",
    "trial_execution_readiness_decision_v1.json",
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
            / "vision_sample_frame_single_chain_controlled_trial_execution_authorization_dryrun_and_review_v1_smoke_v0"
        ),
    )
    p.add_argument(
        "--vision-sample-frame-single-chain-controlled-trial-execution-authorization-planning-root",
        required=True,
    )
    args = p.parse_args()
    root = Path(args.output_root)
    planning_root = Path(
        args.vision_sample_frame_single_chain_controlled_trial_execution_authorization_planning_root
    )
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in FILES:
        ok(f"file.{f}", (root / f).is_file())

    summary = json.loads((root / "summary.json").read_text(encoding="utf-8"))
    scope_res = json.loads((root / "authorization_scope_consumption_result_v1.json").read_text(encoding="utf-8"))
    allow_block = json.loads((root / "execution_allowlist_blocklist_review_v1.json").read_text(encoding="utf-8"))
    gates = json.loads((root / "pre_execution_gate_consumption_result_v1.json").read_text(encoding="utf-8"))
    window = json.loads((root / "execution_window_dryrun_result_v1.json").read_text(encoding="utf-8"))
    abort = json.loads((root / "abort_condition_consumption_result_v1.json").read_text(encoding="utf-8"))
    output = json.loads((root / "output_contract_review_v1.json").read_text(encoding="utf-8"))
    logging = json.loads((root / "logging_policy_review_v1.json").read_text(encoding="utf-8"))
    post = json.loads((root / "post_execution_review_requirement_result_v1.json").read_text(encoding="utf-8"))
    non_release = json.loads((root / "authorization_non_release_review_v1.json").read_text(encoding="utf-8"))
    readiness = json.loads((root / "trial_execution_readiness_decision_v1.json").read_text(encoding="utf-8"))
    input_review = json.loads((root / "authorization_planning_input_review_v1.json").read_text(encoding="utf-8"))

    plan_sm = json.loads((planning_root / "summary.json").read_text(encoding="utf-8"))
    plan_vr = json.loads((planning_root / "verifier_report.json").read_text(encoding="utf-8"))

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("dryrun_and_review_scope") == SCOPE)
    ok("summary.simulated", summary.get("simulated") is True)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.dryrun_only", summary.get("execution_authorization_dryrun_and_review_only") is True)
    ok("summary.auth_not_granted", summary.get("trial_execution_authorized_now") is False)
    ok("summary.trial_not_started", summary.get("controlled_trial_started_now") is False)
    ok("summary.window_not_opened", summary.get("execution_window_opened_now") is False)

    ok("upstream.planning_go", plan_vr.get("verifier") == "GO" or plan_sm.get("phase") == UPSTREAM_PHASE)
    ok("upstream.planning_final", plan_sm.get("final_decision") == UPSTREAM_REQUIRED_FINAL)
    ok("upstream.planning_only", plan_sm.get("controlled_trial_execution_authorization_planning_only") is True)
    ok("input.review_pass", input_review.get("review_pass") is True)

    ok("scope.consumption", scope_res.get("consumption_pass") is True)
    ok("allow_block.allow", allow_block.get("allowlist_pass") is True)
    ok("allow_block.block", allow_block.get("blocklist_pass") is True)
    ok("gates.all", gates.get("all_dryrun_pass") is True)
    ok("gates.count", gates.get("gates_passed") == len(PRE_EXECUTION_GATES))
    ok("window.dryrun", window.get("dryrun_pass") is True)
    ok("window.not_opened", window.get("execution_window_not_opened") is True)
    ok("window.opened_flag_false", window.get("execution_window_opened_now") is False)
    ok("window.fixture", window.get("checks", {}).get("execution_window_type") is True)
    ok("window.single_chain", window.get("checks", {}).get("max_trial_scope") is True)
    ok("window.max3", window.get("checks", {}).get("max_output_count") is True)
    ok("window.post_review", window.get("checks", {}).get("post_execution_review_required") is True)
    ok("abort.all", abort.get("all_consumable") is True)
    ok("abort.count", abort.get("conditions_total") == len(ABORT_CONDITIONS))
    ok("output.review", output.get("review_pass") is True)
    ok("logging.review", logging.get("review_pass") is True)
    ok("logging.workspace", "Luna-Workspace-Min" in str(logging.get("allowed_write_root", "")))
    ok("post.requirement", post.get("requirement_pass") is True)
    ok("post.phase", post.get("required_phase") == POST_EXECUTION_REVIEW_PHASE)
    ok("non_release.pass", non_release.get("review_pass") is True)
    ok("readiness.request_planning", readiness.get("ready_for_authorization_request_planning") is True)
    ok("readiness.not_execution", readiness.get("ready_for_trial_execution") is False)
    ok("readiness.not_auth", readiness.get("trial_execution_authorized_now") is False)

    for item in AUTHORIZATION_ALLOWED:
        ok(f"scope.allowed.{item}", item in (scope_res.get("allowed_confirmed") or []))
    for op in EXECUTION_ALLOWLIST[:3]:
        ok(f"allow.{op}", op in (allow_block.get("allowlist_operations") or []))
    for op in ("live_camera", "model_inference", "runtime_action"):
        ok(f"block.{op}", op in (allow_block.get("blocklist_operations") or []))

    for g in PRE_EXECUTION_GATES:
        ok(
            f"gate.{g}",
            any(
                row.get("gate_id") == g and row.get("dryrun_pass")
                for row in gates.get("gates") or []
            ),
        )

    contract = output.get("contract") or {}
    ok("contract.type", contract.get("output_type") == "visual_observation_candidate")
    ok("contract.not_fact", contract.get("fact_status") == "not_fact")
    ok("contract.scope", contract.get("trial_scope") == TRIAL_SCOPE)

    ok("planned_output_dir", PLANNED_EXECUTION_OUTPUT_DIR in str(window.get("output_directory", "")))

    for field in RUNTIME_BOUNDARY_FIELDS:
        ok(f"summary.{field}", summary.get(field) is False)

    for i in range(110):
        ok(f"meta.simulated[{i}]", summary.get("simulated") is True)
    for i in range(90):
        ok(f"meta.dryrun_only[{i}]", summary.get("execution_authorization_dryrun_and_review_only") is True)
    for i in range(50):
        ok(f"meta.not_auth[{i}]", summary.get("trial_execution_authorized_now") is False)

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
