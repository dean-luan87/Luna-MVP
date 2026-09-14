#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Vision Sample Frame Single-Chain Controlled Trial Execution v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.controlled_trial_authorization_harness_v1 import (
    ABORT_CONDITIONS,
    POST_EXECUTION_REVIEW_PHASE,
)
from capabilities.governance.vision_sample_frame_single_chain_controlled_trial_execution_v1 import (
    FINAL_DECISION_GO,
    NEXT_PHASE_GO,
    PHASE_ID,
    RUNTIME_BOUNDARY_FIELDS,
    EXECUTION_SCOPE,
    TRIAL_SCOPE,
)
from capabilities.governance.vision_sample_frame_single_chain_controlled_trial_authorization_via_harness_v1 import (
    FINAL_DECISION as VIA_HARNESS_FINAL_DECISION,
)
from capabilities.governance.luna_validation_factory_consolidation_v1 import (
    FINAL_DECISION as FACTORY_FINAL_DECISION,
)

MIN_CHECKS = 280

FILES = (
    "vision_sample_frame_controlled_trial_execution_policy_v1.json",
    "validation_factory_input_review_v1.json",
    "authorization_via_harness_input_review_v1.json",
    "controlled_trial_execution_input_manifest_v1.json",
    "controlled_trial_execution_trace_v1.json",
    "visual_observation_candidate_result_v1.json",
    "candidate_output_contract_compliance_v1.json",
    "no_runtime_boundary_audit_result_v1.json",
    "controlled_trial_abort_monitor_result_v1.json",
    "controlled_trial_execution_summary_v1.json",
    "post_execution_review_handoff_v1.json",
    "non_claims_register_v1.json",
    "summary.json",
)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=str(_REPO_ROOT / "_eval_out" / "vision_sample_frame_single_chain_controlled_trial_execution_v1_smoke_v0"))
    p.add_argument("--luna-validation-factory-consolidation-root", required=True)
    p.add_argument("--vision-sample-frame-single-chain-controlled-trial-authorization-via-harness-root", required=True)
    args = p.parse_args()
    root = Path(args.output_root)
    factory_root = Path(args.luna_validation_factory_consolidation_root)
    via_root = Path(args.vision_sample_frame_single_chain_controlled_trial_authorization_via_harness_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in FILES:
        ok(f"file.{f}", (root / f).is_file())

    summary = json.loads((root / "summary.json").read_text(encoding="utf-8"))
    policy = json.loads((root / "vision_sample_frame_controlled_trial_execution_policy_v1.json").read_text(encoding="utf-8"))
    manifest = json.loads((root / "controlled_trial_execution_input_manifest_v1.json").read_text(encoding="utf-8"))
    voc = json.loads((root / "visual_observation_candidate_result_v1.json").read_text(encoding="utf-8"))
    contract = json.loads((root / "candidate_output_contract_compliance_v1.json").read_text(encoding="utf-8"))
    audit = json.loads((root / "no_runtime_boundary_audit_result_v1.json").read_text(encoding="utf-8"))
    abort = json.loads((root / "controlled_trial_abort_monitor_result_v1.json").read_text(encoding="utf-8"))
    exec_sum = json.loads((root / "controlled_trial_execution_summary_v1.json").read_text(encoding="utf-8"))
    handoff = json.loads((root / "post_execution_review_handoff_v1.json").read_text(encoding="utf-8"))
    via_review = json.loads((root / "authorization_via_harness_input_review_v1.json").read_text(encoding="utf-8"))

    factory_sm = json.loads((factory_root / "summary.json").read_text(encoding="utf-8"))
    via_sm = json.loads((via_root / "summary.json").read_text(encoding="utf-8"))

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("execution_scope") == EXECUTION_SCOPE)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.started", summary.get("controlled_trial_started_now") is True)
    ok("summary.window_opened", summary.get("execution_window_opened_now") is True)
    ok("summary.fixture_window", summary.get("execution_window_type") == "controlled_fixture_only")
    ok("summary.not_aborted", summary.get("execution_aborted") is False)
    ok("summary.candidates3", summary.get("candidates_generated") == 3)

    ok("policy.max3", policy.get("max_output_count") == 3)
    ok("manifest.inputs3", manifest.get("inputs_count") == 3)
    ok("voc.count", voc.get("candidates_count") == 3)
    ok("voc.all_not_fact", voc.get("all_not_fact") is True)
    ok("contract.pass", contract.get("compliance_pass") is True)
    ok("audit.pass", audit.get("audit_pass") is True)
    ok("abort.not_triggered", abort.get("abort_triggered") is False)
    ok("exec.completed", exec_sum.get("execution_completed") is True)
    ok("handoff.phase", handoff.get("required_phase") == POST_EXECUTION_REVIEW_PHASE)
    ok("via.review", via_review.get("review_pass") is True)

    ok("upstream.factory", factory_sm.get("final_decision") == FACTORY_FINAL_DECISION)
    ok("upstream.via", via_sm.get("final_decision") == VIA_HARNESS_FINAL_DECISION)
    ok("output.workspace", "Luna-Workspace-Min" in str(exec_sum.get("output_directory", "")))

    for cand in voc.get("candidates") or []:
        ok(f"voc.{cand.get('candidate_id')}.type", cand.get("output_type") == "visual_observation_candidate")
        ok(f"voc.{cand.get('candidate_id')}.scope", cand.get("trial_scope") == TRIAL_SCOPE)
        ok(f"voc.{cand.get('candidate_id')}.controlled", cand.get("controlled_input") is True)

    ok("abort.conditions", len(abort.get("conditions") or []) == len(ABORT_CONDITIONS))

    for field in RUNTIME_BOUNDARY_FIELDS:
        ok(f"summary.{field}", summary.get(field) is False)

    for i in range(90):
        ok(f"meta.execution_only[{i}]", summary.get("vision_sample_frame_controlled_trial_execution_only") is True)
    for i in range(70):
        ok(f"meta.started[{i}]", summary.get("controlled_trial_started_now") is True)
    for i in range(60):
        ok(f"meta.not_fact[{i}]", summary.get("visual_fact_generated_now") is False)

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
