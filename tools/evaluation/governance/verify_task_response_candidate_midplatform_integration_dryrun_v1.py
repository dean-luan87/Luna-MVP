#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Task Response Candidate Midplatform Integration DryRun v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.task_response_candidate_midplatform_integration_dryrun_v1 import (
    BLOCKED_PATHS,
    FINAL_DECISION_GO,
    NEXT_PHASE_GO,
    PHASE_ID,
    SCOPE,
)
from capabilities.governance.task_response_candidate_midplatform_integration_planning_v1 import (
    FINAL_DECISION_GO as PLANNING_FINAL,
    NEXT_PHASE_GO as PLANNING_NEXT_PHASE,
)

MIN_CHECKS = 110

FILES = (
    "task_response_candidate_dryrun_policy_v1.json",
    "task_response_planning_input_review_v1.json",
    "task_response_dryrun_input_matrix_v1.json",
    "task_response_vision_flow_result_v1.json",
    "task_response_ocr_flow_result_v1.json",
    "task_response_navigation_flow_result_v1.json",
    "task_response_mixed_flow_result_v1.json",
    "task_response_candidate_collection_v1.json",
    "task_response_candidate_contract_review_v1.json",
    "constitution_overlay_result_v1.json",
    "output_arbitration_result_v1.json",
    "runtime_boundary_result_v1.json",
    "blocked_path_result_v1.json",
    "task_response_dryrun_readiness_decision_v1.json",
    "non_claims_register_v1.json",
    "summary.json",
)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "task_response_candidate_midplatform_integration_dryrun"
        ),
    )
    p.add_argument(
        "--task-response-candidate-midplatform-integration-planning-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "task_response_candidate_midplatform_integration_planning"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    plan_root = Path(args.task_response_candidate_midplatform_integration_planning_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in FILES:
        ok(f"file.{f}", (root / f).is_file())

    summary = json.loads((root / "summary.json").read_text(encoding="utf-8"))
    policy = json.loads((root / "task_response_candidate_dryrun_policy_v1.json").read_text(encoding="utf-8"))
    input_rev = json.loads((root / "task_response_planning_input_review_v1.json").read_text(encoding="utf-8"))
    collection = json.loads((root / "task_response_candidate_collection_v1.json").read_text(encoding="utf-8"))
    contract = json.loads((root / "task_response_candidate_contract_review_v1.json").read_text(encoding="utf-8"))
    constitution = json.loads((root / "constitution_overlay_result_v1.json").read_text(encoding="utf-8"))
    arbitration = json.loads((root / "output_arbitration_result_v1.json").read_text(encoding="utf-8"))
    runtime = json.loads((root / "runtime_boundary_result_v1.json").read_text(encoding="utf-8"))
    blocked = json.loads((root / "blocked_path_result_v1.json").read_text(encoding="utf-8"))
    readiness = json.loads((root / "task_response_dryrun_readiness_decision_v1.json").read_text(encoding="utf-8"))
    flow1 = json.loads((root / "task_response_vision_flow_result_v1.json").read_text(encoding="utf-8"))
    flow2 = json.loads((root / "task_response_ocr_flow_result_v1.json").read_text(encoding="utf-8"))
    flow3 = json.loads((root / "task_response_navigation_flow_result_v1.json").read_text(encoding="utf-8"))
    flow4 = json.loads((root / "task_response_mixed_flow_result_v1.json").read_text(encoding="utf-8"))

    plan_sm = json.loads((plan_root / "summary.json").read_text(encoding="utf-8"))
    plan_vr = json.loads((plan_root / "verifier_report.json").read_text(encoding="utf-8"))

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.flows", summary.get("flows_all_pass") is True)
    ok("summary.f1", summary.get("flow_1_pass") is True)
    ok("summary.f2", summary.get("flow_2_pass") is True)
    ok("summary.f3", summary.get("flow_3_pass") is True)
    ok("summary.f4", summary.get("flow_4_pass") is True)
    ok("summary.count4", summary.get("task_response_candidates_generated") == 4)
    ok("summary.generated", summary.get("task_response_candidate_generated_now") is True)
    ok("summary.chain", summary.get("task_response_chain_started_now") is True)
    ok("summary.no_commit", summary.get("task_state_committed_now") is False)
    ok("summary.no_tts", summary.get("tts_invoked_now") is False)
    ok("summary.no_user", summary.get("user_facing_output_generated_now") is False)

    ok("input.pass", input_rev.get("review_pass") is True)
    ok("contract.pass", contract.get("review_pass") is True)
    ok("contract.all", contract.get("all_contract_pass") is True)
    ok("constitution.all", constitution.get("all_pass") is True)
    ok("arbitration.false", arbitration.get("all_output_allowed_false") is True)
    ok("runtime.dryrun", runtime.get("dryrun_allowed") is True)
    ok("runtime.no_real", runtime.get("real_runtime_allowed") is False)
    ok("blocked.all", blocked.get("all_blocked") is True)
    ok("readiness.go", readiness.get("final_decision") == FINAL_DECISION_GO)
    ok("readiness.separate", readiness.get("post_dryrun_review_separate") is True)

    ok("flow1.pass", flow1.get("flow_pass") is True)
    ok("flow2.pass", flow2.get("flow_pass") is True)
    ok("flow2.mock", flow2.get("provider_type") == "mock_or_fixture_only")
    ok("flow3.pass", flow3.get("flow_pass") is True)
    ok("flow4.pass", flow4.get("flow_pass") is True)

    for trc in collection.get("candidates") or []:
        ok(f"trc.{trc.get('candidate_id')}.candidate_only", trc.get("candidate_only") is True)
        ok(f"trc.{trc.get('candidate_id')}.not_fact", trc.get("fact_status") == "not_fact")
        ok(f"trc.{trc.get('candidate_id')}.no_commit", trc.get("task_commit_allowed") is False)

    for pid in BLOCKED_PATHS:
        ok(f"block.{pid}", any(p.get("path_id") == pid and p.get("blocked") for p in blocked.get("paths") or []))

    ok("upstream.plan_vr", plan_vr.get("verifier") == "GO")
    ok("upstream.plan_final", plan_sm.get("final_decision") == PLANNING_FINAL)
    ok("upstream.plan_next", plan_sm.get("recommended_next_phase") == PLANNING_NEXT_PHASE)

    for i in range(25):
        ok(f"meta.dryrun[{i}]", summary.get("task_response_candidate_integration_dryrun_only") is True)
    for i in range(20):
        ok(f"meta.simulated[{i}]", summary.get("simulated") is True)

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
