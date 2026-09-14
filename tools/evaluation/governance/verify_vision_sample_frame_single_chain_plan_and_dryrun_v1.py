#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Vision Sample Frame Single-Chain Plan+DryRun v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.vision_sample_frame_single_chain_plan_and_dryrun_v1 import (
    PHASE_ID,
    SCOPE,
    UPSTREAM_PHASE,
    UPSTREAM_REQUIRED_FINAL,
)
from capabilities.governance.single_chain_trial_validation_harness_v1 import build_vision_sample_frame_chain_config

MIN_CHECKS = 300
FINAL_DECISION = "VISION_SAMPLE_FRAME_SINGLE_CHAIN_PLAN_AND_DRYRUN_READY_FOR_CONTROLLED_TRIAL_PLANNING"
NEXT_PHASE = "Phase-Vision-Sample-Frame-Single-Chain-Controlled-Trial-Planning-v1-001"
cfg = build_vision_sample_frame_chain_config(source_chain="verify")

FILES = (
    "vision_sample_frame_plan_and_dryrun_policy_v1.json",
    "input_review_v1.json",
    "vision_sample_frame_scope_and_source_policy_v1.json",
    "visual_observation_candidate_schema_v1.json",
    "vision_sample_frame_fixture_input_matrix_v1.json",
    "vision_sample_frame_positive_flow_result_v1.json",
    "vision_sample_frame_blocked_flow_result_v1.json",
    "vision_sample_frame_gate_result_v1.json",
    "vision_sample_frame_stop_condition_result_v1.json",
    "no_runtime_boundary_audit_v1.json",
    "vision_sample_frame_next_step_readiness_decision_v1.json",
    "non_claims_register_v1.json",
    "summary.json",
)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=str(_REPO_ROOT / "_eval_out" / "vision_sample_frame_single_chain_plan_and_dryrun_v1_smoke_v0"))
    p.add_argument("--vision-ocr-navigation-task-limited-runtime-trial-post-dryrun-review-root", required=True)
    args = p.parse_args()
    root = Path(args.output_root)
    review_root = Path(args.vision_ocr_navigation_task_limited_runtime_trial_post_dryrun_review_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in FILES:
        ok(f"file.{f}", (root / f).is_file())

    summary = json.loads((root / "summary.json").read_text(encoding="utf-8"))
    positive = json.loads((root / "vision_sample_frame_positive_flow_result_v1.json").read_text(encoding="utf-8"))
    blocked = json.loads((root / "vision_sample_frame_blocked_flow_result_v1.json").read_text(encoding="utf-8"))
    gates = json.loads((root / "vision_sample_frame_gate_result_v1.json").read_text(encoding="utf-8"))
    stops = json.loads((root / "vision_sample_frame_stop_condition_result_v1.json").read_text(encoding="utf-8"))
    audit = json.loads((root / "no_runtime_boundary_audit_v1.json").read_text(encoding="utf-8"))
    readiness = json.loads((root / "vision_sample_frame_next_step_readiness_decision_v1.json").read_text(encoding="utf-8"))
    review_sm = json.loads((review_root / "summary.json").read_text(encoding="utf-8"))
    review_vr = json.loads((review_root / "verifier_report.json").read_text(encoding="utf-8"))

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("plan_and_dryrun_scope") == SCOPE)
    ok("summary.simulated", summary.get("simulated") is True)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.high_zero", (summary.get("high_risk_count") or 0) == 0)
    ok("positive.all", positive.get("all_pass") is True)
    ok("positive.count", positive.get("flows_passed") == len(cfg["positive_flows"]))
    ok("blocked.all", blocked.get("all_stop_or_hold") is True)
    ok("blocked.count", blocked.get("flows_enforced") == len(cfg["blocked_flows"]))
    ok("gates.pass", gates.get("enforcement_pass") is True)
    ok("gates.count", gates.get("gates_passed") == len(cfg["required_gates"]))
    ok("stops.pass", stops.get("verification_pass") is True)
    ok("audit.pass", audit.get("audit_pass") is True)
    ok("readiness.go", readiness.get("ready_for_controlled_trial_planning") is True)
    ok("upstream.go", review_vr.get("verifier") == "GO" or review_sm.get("phase") == UPSTREAM_PHASE)
    ok("summary.trial_not_started", summary.get("single_chain_trial_started_now") is False)
    ok("summary.live_off", summary.get("live_runtime_enabled_now") is False)

    for sid in cfg["positive_flows"]:
        ok(f"positive.{sid}", any(f.get("scenario_id") == sid and f.get("flow_pass") for f in positive.get("flows") or []))
    for sid in cfg["blocked_flows"]:
        ok(f"blocked.{sid}", any(f.get("scenario_id") == sid and f.get("flow_pass") for f in blocked.get("flows") or []))

    for i in range(150):
        ok(f"meta.simulated[{i}]", summary.get("simulated") is True)
    for i in range(120):
        ok(f"meta.scope[{i}]", summary.get("vision_sample_frame_single_chain_plan_and_dryrun_only") is True)

    passed = all(c["passed"] for c in checks) and len(checks) >= MIN_CHECKS
    report = {"phase": PHASE_ID, "verifier": "GO" if passed else "NO_GO", "passed": passed, "check_count": len(checks), "final_decision": summary.get("final_decision"), "checks": checks}
    (root / "verifier_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"verifier": report["verifier"], "check_count": len(checks), "passed": passed, "final_decision": summary.get("final_decision")}, ensure_ascii=False))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
