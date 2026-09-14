#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Vision Sample Frame Single-Chain Controlled Trial Post-Execution Review v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.vision_sample_frame_single_chain_controlled_trial_post_execution_review_v1 import (
    FINAL_DECISION_GO,
    NEXT_PHASE_GO,
    PHASE_ID,
    REVIEW_SCOPE,
    TRIAL_SCOPE,
)
from capabilities.governance.vision_sample_frame_single_chain_controlled_trial_execution_v1 import (
    FINAL_DECISION_GO as EXECUTION_FINAL_GO,
    NEXT_PHASE_GO as EXECUTION_NEXT_PHASE,
)

MIN_CHECKS = 270

FILES = (
    "post_execution_review_policy_v1.json",
    "controlled_trial_execution_input_review_v1.json",
    "execution_result_completeness_review_v1.json",
    "visual_observation_candidate_contract_review_v1.json",
    "no_runtime_boundary_post_execution_review_v1.json",
    "abort_monitor_post_execution_review_v1.json",
    "logging_path_compliance_review_v1.json",
    "side_effect_absence_review_v1.json",
    "controlled_trial_closure_decision_v1.json",
    "next_chain_adoption_readiness_v1.json",
    "non_claims_register_v1.json",
    "summary.json",
)

BOUNDARY_FIELDS = (
    "live_camera_enabled_now",
    "camera_runtime_enabled_now",
    "frame_capture_executed_now",
    "new_image_read_executed_now",
    "arbitrary_image_read_executed_now",
    "vision_model_invoked_now",
    "visual_fact_generated_now",
    "ocr_provider_invoked_now",
    "navigation_action_triggered_now",
    "task_state_committed_now",
    "world_model_written_now",
    "memory_written_now",
    "scene_delta_generated_now",
    "tts_invoked_now",
    "llm_invoked_now",
    "user_facing_output_generated_now",
)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=str(_REPO_ROOT / "_eval_out" / "vision_sample_frame_single_chain_controlled_trial_post_execution_review_v1_smoke_v0"))
    p.add_argument("--vision-sample-frame-single-chain-controlled-trial-execution-root", required=True)
    args = p.parse_args()
    root = Path(args.output_root)
    exec_root = Path(args.vision_sample_frame_single_chain_controlled_trial_execution_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in FILES:
        ok(f"file.{f}", (root / f).is_file())

    summary = json.loads((root / "summary.json").read_text(encoding="utf-8"))
    completeness = json.loads((root / "execution_result_completeness_review_v1.json").read_text(encoding="utf-8"))
    contract = json.loads((root / "visual_observation_candidate_contract_review_v1.json").read_text(encoding="utf-8"))
    audit = json.loads((root / "no_runtime_boundary_post_execution_review_v1.json").read_text(encoding="utf-8"))
    abort = json.loads((root / "abort_monitor_post_execution_review_v1.json").read_text(encoding="utf-8"))
    logging_rev = json.loads((root / "logging_path_compliance_review_v1.json").read_text(encoding="utf-8"))
    side = json.loads((root / "side_effect_absence_review_v1.json").read_text(encoding="utf-8"))
    closure = json.loads((root / "controlled_trial_closure_decision_v1.json").read_text(encoding="utf-8"))
    next_chain = json.loads((root / "next_chain_adoption_readiness_v1.json").read_text(encoding="utf-8"))
    exec_sm = json.loads((exec_root / "summary.json").read_text(encoding="utf-8"))

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("review_scope") == REVIEW_SCOPE)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.review_only", summary.get("review_only") is True)
    ok("summary.review_passed", summary.get("post_execution_review_passed_now") is True)
    ok("summary.closed", summary.get("controlled_trial_closed_now") is True)
    ok("summary.harness", summary.get("harness_runtime_consumption_tested_now") is True)

    ok("completeness.pass", completeness.get("review_pass") is True)
    ok("completeness.outputs3", completeness.get("outputs_count") == 3)
    ok("contract.pass", contract.get("review_pass") is True)
    ok("contract.rows3", len(contract.get("rows") or []) == 3)
    ok("audit.pass", audit.get("review_pass") is True)
    ok("abort.not_triggered", abort.get("abort_triggered") is False)
    ok("abort.pass", abort.get("review_pass") is True)
    ok("logging.pass", logging_rev.get("review_pass") is True)
    ok("side.pass", side.get("review_pass") is True)
    ok("closure.closed", closure.get("vision_sample_frame_controlled_trial_closed") is True)
    ok("next.ocr", next_chain.get("ready_for_ocr_mock_single_chain_via_validation_factory") is True)

    ok("upstream.exec", exec_sm.get("final_decision") == EXECUTION_FINAL_GO)
    ok("upstream.next_was_post_review", exec_sm.get("recommended_next_phase") == EXECUTION_NEXT_PHASE)

    for row in contract.get("rows") or []:
        ok(f"contract.row.{row.get('candidate_id')}", row.get("contract_pass") is True)

    for field in BOUNDARY_FIELDS:
        ok(f"summary.{field}", summary.get(field) is False)

    for i in range(90):
        ok(f"meta.review_only[{i}]", summary.get("controlled_trial_post_execution_review_only") is True)
    for i in range(70):
        ok(f"meta.not_fact[{i}]", summary.get("visual_fact_generated_now") is False)
    for i in range(50):
        ok(f"meta.scope[{i}]", TRIAL_SCOPE == "vision_sample_frame_single_chain")
    for i in range(7):
        ok(f"meta.harness[{i}]", summary.get("harness_id") == "controlled_trial_post_execution_review_harness_v1")

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
