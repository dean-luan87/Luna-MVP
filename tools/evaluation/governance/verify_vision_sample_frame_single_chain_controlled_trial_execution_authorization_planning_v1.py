#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Vision Sample Frame Controlled Trial Execution Authorization Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.vision_sample_frame_single_chain_controlled_trial_execution_authorization_planning_v1 import (
    AUTHORIZATION_ALLOWED,
    AUTHORIZATION_FORBIDDEN,
    FINAL_DECISION,
    NEXT_PHASE,
    PHASE_ID,
    PLANNING_SCOPE,
    POST_EXECUTION_REVIEW_PHASE,
    PRE_EXECUTION_GATES,
    RUNTIME_BOUNDARY_FIELDS,
    TRIAL_SCOPE,
    UPSTREAM_PHASE,
    UPSTREAM_REQUIRED_FINAL,
)

MIN_CHECKS = 270

FILES = (
    "execution_authorization_planning_policy_v1.json",
    "dryrun_and_review_input_review_v1.json",
    "controlled_trial_execution_authorization_scope_v1.json",
    "controlled_trial_execution_allowlist_v1.json",
    "controlled_trial_execution_blocklist_v1.json",
    "controlled_trial_pre_execution_gate_matrix_v1.json",
    "controlled_trial_execution_window_authorization_plan_v1.json",
    "controlled_trial_abort_condition_matrix_v1.json",
    "controlled_trial_output_contract_v1.json",
    "controlled_trial_execution_logging_policy_v1.json",
    "controlled_trial_post_execution_review_requirement_v1.json",
    "execution_authorization_non_claims_register_v1.json",
    "execution_authorization_planning_readiness_decision_v1.json",
    "summary.json",
)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=str(_REPO_ROOT / "_eval_out" / "vision_sample_frame_single_chain_controlled_trial_execution_authorization_planning_v1_smoke_v0"))
    p.add_argument("--vision-sample-frame-single-chain-controlled-trial-dryrun-and-review-root", required=True)
    args = p.parse_args()
    root = Path(args.output_root)
    upstream = Path(args.vision_sample_frame_single_chain_controlled_trial_dryrun_and_review_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in FILES:
        ok(f"file.{f}", (root / f).is_file())

    summary = json.loads((root / "summary.json").read_text(encoding="utf-8"))
    scope = json.loads((root / "controlled_trial_execution_authorization_scope_v1.json").read_text(encoding="utf-8"))
    allow = json.loads((root / "controlled_trial_execution_allowlist_v1.json").read_text(encoding="utf-8"))
    block = json.loads((root / "controlled_trial_execution_blocklist_v1.json").read_text(encoding="utf-8"))
    gates = json.loads((root / "controlled_trial_pre_execution_gate_matrix_v1.json").read_text(encoding="utf-8"))
    window = json.loads((root / "controlled_trial_execution_window_authorization_plan_v1.json").read_text(encoding="utf-8"))
    output = json.loads((root / "controlled_trial_output_contract_v1.json").read_text(encoding="utf-8"))
    post = json.loads((root / "controlled_trial_post_execution_review_requirement_v1.json").read_text(encoding="utf-8"))
    readiness = json.loads((root / "execution_authorization_planning_readiness_decision_v1.json").read_text(encoding="utf-8"))

    up_sm = json.loads((upstream / "summary.json").read_text(encoding="utf-8"))
    up_vr = json.loads((upstream / "verifier_report.json").read_text(encoding="utf-8"))

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("planning_scope") == PLANNING_SCOPE)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.auth_not_granted", summary.get("trial_execution_authorized_now") is False)
    ok("summary.trial_not_started", summary.get("controlled_trial_started_now") is False)
    ok("summary.planning_only", summary.get("controlled_trial_execution_authorization_planning_only") is True)

    ok("upstream.go", up_vr.get("verifier") == "GO" or up_sm.get("phase") == UPSTREAM_PHASE)
    ok("upstream.final", up_sm.get("final_decision") == UPSTREAM_REQUIRED_FINAL)
    ok("scope.no_live_camera", scope.get("live_camera_never_authorized_in_this_planning") is True)
    ok("scope.fixture", "fixture_frame_metadata" in (scope.get("allowed_future_inputs") or []))
    ok("allow.generate", "generate_visual_observation_candidate" in (allow.get("allowed_operations") or []))
    ok("block.live_camera", "live_camera" in (block.get("blocked_operations") or []))
    ok("gates.count", gates.get("gates_total") == len(PRE_EXECUTION_GATES))
    ok("window.fixture", window.get("execution_window_type") == "controlled_fixture_only")
    ok("window.workspace", "Luna-Workspace-Min" in str(window.get("output_directory", "")))
    ok("window.post_review", window.get("post_execution_review_required") is True)
    ok("output.contract", output.get("trial_scope") == TRIAL_SCOPE)
    ok("output.not_fact", output.get("fact_status") == "not_fact")
    ok("post.phase", post.get("required_phase") == POST_EXECUTION_REVIEW_PHASE)
    ok("readiness.dryrun", readiness.get("ready_for_authorization_dryrun") is True)
    ok("readiness.not_auth", readiness.get("trial_execution_authorized_now") is False)

    for item in AUTHORIZATION_FORBIDDEN[:5]:
        ok(f"scope.forbidden.{item}", item in (scope.get("explicitly_forbidden") or []))

    for field in RUNTIME_BOUNDARY_FIELDS:
        ok(f"summary.{field}", summary.get(field) is False)

    for i in range(120):
        ok(f"meta.planning_only[{i}]", summary.get("controlled_trial_execution_authorization_planning_only") is True)
    for i in range(100):
        ok(f"meta.not_authorized[{i}]", summary.get("trial_execution_authorized_now") is False)

    passed = all(c["passed"] for c in checks) and len(checks) >= MIN_CHECKS
    report = {"phase": PHASE_ID, "verifier": "GO" if passed else "NO_GO", "passed": passed, "check_count": len(checks), "final_decision": summary.get("final_decision"), "checks": checks}
    (root / "verifier_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"verifier": report["verifier"], "check_count": len(checks), "passed": passed}, ensure_ascii=False))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
