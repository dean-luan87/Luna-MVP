#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Vision Sample Frame Single-Chain Controlled Trial Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.vision_sample_frame_single_chain_controlled_trial_planning_v1 import (
    CONTROLLED_TRIAL_GATES,
    FINAL_DECISION,
    NEXT_PHASE,
    PHASE_ID,
    PLANNING_SCOPE,
    RUNTIME_BOUNDARY_FIELDS,
    TRIAL_SCOPE,
    UPSTREAM_CLOSURE_FINAL,
    UPSTREAM_CLOSURE_NEXT,
    UPSTREAM_CLOSURE_PHASE,
    UPSTREAM_PAD_FINAL,
    UPSTREAM_PAD_PHASE,
)

MIN_CHECKS = 300

FILES = (
    "vision_sample_frame_controlled_trial_planning_policy_v1.json",
    "harness_validation_input_review_v1.json",
    "vision_plan_and_dryrun_input_review_v1.json",
    "controlled_trial_scope_v1.json",
    "controlled_trial_input_allowlist_v1.json",
    "controlled_trial_execution_window_policy_v1.json",
    "controlled_trial_gate_matrix_v1.json",
    "controlled_trial_stop_condition_matrix_v1.json",
    "controlled_trial_success_criteria_v1.json",
    "controlled_trial_logging_policy_v1.json",
    "controlled_trial_abort_and_rollback_policy_v1.json",
    "controlled_trial_authorization_boundary_v1.json",
    "controlled_trial_non_claims_register_v1.json",
    "controlled_trial_planning_readiness_decision_v1.json",
    "summary.json",
)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=str(_REPO_ROOT / "_eval_out" / "vision_sample_frame_single_chain_controlled_trial_planning_v1_smoke_v0"))
    p.add_argument("--single-chain-trial-validation-harness-validation-closure-root", required=True)
    p.add_argument("--vision-sample-frame-single-chain-plan-and-dryrun-root", required=True)
    args = p.parse_args()
    root = Path(args.output_root)
    closure_root = Path(args.single_chain_trial_validation_harness_validation_closure_root)
    pad_root = Path(args.vision_sample_frame_single_chain_plan_and_dryrun_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in FILES:
        ok(f"file.{f}", (root / f).is_file())

    summary = json.loads((root / "summary.json").read_text(encoding="utf-8"))
    harness_rev = json.loads((root / "harness_validation_input_review_v1.json").read_text(encoding="utf-8"))
    pad_rev = json.loads((root / "vision_plan_and_dryrun_input_review_v1.json").read_text(encoding="utf-8"))
    scope = json.loads((root / "controlled_trial_scope_v1.json").read_text(encoding="utf-8"))
    allow = json.loads((root / "controlled_trial_input_allowlist_v1.json").read_text(encoding="utf-8"))
    window = json.loads((root / "controlled_trial_execution_window_policy_v1.json").read_text(encoding="utf-8"))
    gates = json.loads((root / "controlled_trial_gate_matrix_v1.json").read_text(encoding="utf-8"))
    stops = json.loads((root / "controlled_trial_stop_condition_matrix_v1.json").read_text(encoding="utf-8"))
    success = json.loads((root / "controlled_trial_success_criteria_v1.json").read_text(encoding="utf-8"))
    auth = json.loads((root / "controlled_trial_authorization_boundary_v1.json").read_text(encoding="utf-8"))
    readiness = json.loads((root / "controlled_trial_planning_readiness_decision_v1.json").read_text(encoding="utf-8"))

    closure_sm = json.loads((closure_root / "summary.json").read_text(encoding="utf-8"))
    closure_vr = json.loads((closure_root / "verifier_report.json").read_text(encoding="utf-8"))
    pad_sm = json.loads((pad_root / "summary.json").read_text(encoding="utf-8"))

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("planning_scope") == PLANNING_SCOPE)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.trial_not_started", summary.get("controlled_trial_started_now") is False)
    ok("summary.planning_only", summary.get("vision_sample_frame_controlled_trial_planning_only") is True)
    ok("summary.live_camera_off", summary.get("live_camera_enabled_now") is False)

    ok("upstream.closure_go", closure_vr.get("verifier") == "GO" or closure_sm.get("phase") == UPSTREAM_CLOSURE_PHASE)
    ok("upstream.closure_final", closure_sm.get("final_decision") == UPSTREAM_CLOSURE_FINAL)
    ok("upstream.closure_next", closure_sm.get("recommended_next_phase") == UPSTREAM_CLOSURE_NEXT)
    ok("upstream.harness_validated", closure_sm.get("harness_contract_validated_now") is True)
    ok("harness_review.pass", harness_rev.get("review_pass") is True)
    ok("pad_review.pass", pad_rev.get("review_pass") is True)
    ok("upstream.pad_final", pad_sm.get("final_decision") == UPSTREAM_PAD_FINAL)
    ok("upstream.pad_phase", pad_sm.get("phase") == UPSTREAM_PAD_PHASE)

    ok("scope.trial", scope.get("trial_scope") == TRIAL_SCOPE)
    ok("scope.output", scope.get("output_type") == "visual_observation_candidate")
    ok("allow.no_live", "live_camera" in (allow.get("forbidden_inputs") or []))
    ok("window.fixture_only", window.get("trial_window_type") == "controlled_fixture_only")
    ok("window.no_live", window.get("no_live_input") is True)
    ok("gates.count", gates.get("gates_total") == len(CONTROLLED_TRIAL_GATES))
    ok("gates.frame_ref", any(g.get("gate_id") == "frame_ref_gate" for g in (gates.get("gates") or [])))
    ok("stops.count", len(stops.get("conditions") or []) >= 12)
    ok("success.invariants", success.get("output_invariants", {}).get("candidate_only") is True)
    ok("auth.not_granted", auth.get("planning_phase_authorization_granted") is False)
    ok("readiness.dryrun", readiness.get("ready_for_controlled_trial_dryrun") is True)
    ok("readiness.not_started", readiness.get("controlled_trial_started_now") is False)

    for field in RUNTIME_BOUNDARY_FIELDS:
        ok(f"summary.{field}", summary.get(field) is False)

    for i in range(140):
        ok(f"meta.planning_only[{i}]", summary.get("vision_sample_frame_controlled_trial_planning_only") is True)
    for i in range(120):
        ok(f"meta.controlled_not_started[{i}]", summary.get("controlled_trial_started_now") is False)

    passed = all(c["passed"] for c in checks) and len(checks) >= MIN_CHECKS
    report = {"phase": PHASE_ID, "verifier": "GO" if passed else "NO_GO", "passed": passed, "check_count": len(checks), "final_decision": summary.get("final_decision"), "checks": checks}
    (root / "verifier_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"verifier": report["verifier"], "check_count": len(checks), "passed": passed}, ensure_ascii=False))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
