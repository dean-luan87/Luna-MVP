#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Compressed OCR Authorization Lifecycle DryRunAndReview v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.capability_factory_admission_and_operation_standard_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as FACTORY_DR_FINAL,
)
from capabilities.governance.capability_factory_admission_and_operation_standard_planning_v1 import (
    COMPRESSED_PATH,
    STANDARD_ID,
)
from capabilities.governance.compressed_ocr_authorization_lifecycle_dryrun_and_review_v1 import (
    BLOCKED_PATHS,
    BOUNDARY_FALSE,
    BOUNDARY_TRUE,
    EVIDENCE_FIELDS,
    FACTORY_STANDARDS_REQUIRED,
    FINAL_DECISION_GO,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    SCOPE,
    STAGE_IDS,
)
from capabilities.governance.compressed_ocr_authorization_lifecycle_planning_v1 import (
    CURRENT_STATE as PLANNING_CURRENT_STATE,
    FINAL_DECISION_GO as PLANNING_FINAL,
    NEXT_PHASE_GO as PLANNING_NEXT,
)
from capabilities.governance.ocr_provider_authorization_request_dryrun_v1 import (
    CURRENT_REQUEST_DRYRUN_STATE,
)

MIN_CHECKS = 100

REQUIRED = (
    "compressed_lifecycle_dryrun_and_review_policy_v1.json",
    "compressed_lifecycle_planning_input_review_v1.json",
    "compressed_lifecycle_candidate_v1.json",
    "request_stage_candidate_dryrun_review_v1.json",
    "formal_artifact_stage_candidate_dryrun_review_v1.json",
    "send_stage_candidate_dryrun_review_v1.json",
    "grant_stage_candidate_dryrun_review_v1.json",
    "execution_window_stage_candidate_dryrun_review_v1.json",
    "review_stage_candidate_dryrun_review_v1.json",
    "factory_standard_consumption_matrix_v1.json",
    "validation_factory_binding_review_v1.json",
    "compressed_lifecycle_evidence_binding_review_v1.json",
    "compressed_lifecycle_approval_grant_review_v1.json",
    "compressed_lifecycle_sandbox_rollback_review_v1.json",
    "compressed_lifecycle_boundary_audit_v1.json",
    "compressed_lifecycle_blocked_path_result_v1.json",
    "compressed_lifecycle_closure_decision_v1.json",
    "non_claims_register_v1.json",
    "summary.json",
)


def _load(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "compressed_ocr_authorization_lifecycle_dryrun_and_review"
        ),
    )
    p.add_argument(
        "--compressed-ocr-authorization-lifecycle-planning-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "compressed_ocr_authorization_lifecycle_planning"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    plan_root = Path(args.compressed_ocr_authorization_lifecycle_planning_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    summary = _load(root / "summary.json")
    planning_review = _load(root / "compressed_lifecycle_planning_input_review_v1.json")
    candidate = _load(root / "compressed_lifecycle_candidate_v1.json")
    req_review = _load(root / "request_stage_candidate_dryrun_review_v1.json")
    formal_review = _load(root / "formal_artifact_stage_candidate_dryrun_review_v1.json")
    send_review = _load(root / "send_stage_candidate_dryrun_review_v1.json")
    grant_review = _load(root / "grant_stage_candidate_dryrun_review_v1.json")
    window_review = _load(root / "execution_window_stage_candidate_dryrun_review_v1.json")
    review_review = _load(root / "review_stage_candidate_dryrun_review_v1.json")
    consumption = _load(root / "factory_standard_consumption_matrix_v1.json")
    vf_binding = _load(root / "validation_factory_binding_review_v1.json")
    evidence = _load(root / "compressed_lifecycle_evidence_binding_review_v1.json")
    approval = _load(root / "compressed_lifecycle_approval_grant_review_v1.json")
    sandbox = _load(root / "compressed_lifecycle_sandbox_rollback_review_v1.json")
    boundary_audit = _load(root / "compressed_lifecycle_boundary_audit_v1.json")
    blocked = _load(root / "compressed_lifecycle_blocked_path_result_v1.json")
    closure = _load(root / "compressed_lifecycle_closure_decision_v1.json")

    plan_vr = _load(plan_root / "verifier_report.json")
    plan_sm = _load(plan_root / "summary.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.dryrun_only", summary.get("compressed_ocr_authorization_lifecycle_dryrun_and_review_only") is True)
    ok("summary.simulated", summary.get("simulated") is True)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.standard_id", summary.get("standard_id") == STANDARD_ID)

    ok("upstream.plan_go", plan_vr.get("verifier") == "GO")
    ok("upstream.plan_final", plan_sm.get("final_decision") == PLANNING_FINAL)
    ok("upstream.plan_next", plan_sm.get("recommended_next_phase") == PLANNING_NEXT)
    ok("upstream.plan_state", plan_sm.get("current_state") == PLANNING_CURRENT_STATE)
    ok("planning_review.pass", planning_review.get("review_pass") is True)

    ok("candidate.stages7", candidate.get("stage_count") == 7)
    ok("candidate.path7", len(candidate.get("compressed_path") or []) == len(COMPRESSED_PATH))
    stages = candidate.get("stages") or []
    for i, sid in enumerate(STAGE_IDS):
        ok(f"candidate.stage.{sid}", stages[i].get("stage_id") == sid if i < len(stages) else False)
        if i < len(stages):
            ok(f"candidate.{sid}.evidence", stages[i].get("evidence_required") is True)
            ok(f"candidate.{sid}.boundary", stages[i].get("boundary_required") is True)
            ok(f"candidate.{sid}.not_exec", stages[i].get("current_executed_now") is False)
            ok(f"candidate.{sid}.future", stages[i].get("promotion_requires_future_phase") is True)

    ok("req_review.pass", req_review.get("dryrun_and_review_pass") is True)
    ok("formal_review.pass", formal_review.get("dryrun_and_review_pass") is True)
    ok("send_review.pass", send_review.get("dryrun_and_review_pass") is True)
    ok("grant_review.pass", grant_review.get("dryrun_and_review_pass") is True)
    ok("window_review.pass", window_review.get("dryrun_and_review_pass") is True)
    ok("review_review.pass", review_review.get("dryrun_and_review_pass") is True)

    ok("consumption.count9", consumption.get("standard_count") == len(FACTORY_STANDARDS_REQUIRED))
    ok("consumption.all", consumption.get("all_consumed") is True)
    for std in FACTORY_STANDARDS_REQUIRED:
        row = next((r for r in (consumption.get("standards") or []) if r.get("standard") == std), None)
        ok(f"consumption.{std}", row is not None and row.get("consumed") is True)

    ok("vf.pass", vf_binding.get("dryrun_and_review_pass") is True)
    ok("vf.harness", vf_binding.get("controlled_provider_readiness_harness_factory_module_candidate") is True)
    ok("vf.midplatform_blocked", vf_binding.get("midplatform_consumption_blocked_now") is True)

    ok("evidence.count", len(evidence.get("required_fields") or []) == len(EVIDENCE_FIELDS))
    ok("evidence.bound", evidence.get("all_bound") is True)

    ok("approval.pass", approval.get("dryrun_and_review_pass") is True)
    ok("sandbox.pass", sandbox.get("dryrun_and_review_pass") is True)
    ok("boundary_audit.pass", boundary_audit.get("audit_pass") is True)
    ok("blocked.path_count", blocked.get("path_count") == len(BLOCKED_PATHS))
    ok("blocked.all", blocked.get("all_blocked") is True)
    for bp in BLOCKED_PATHS:
        row = next((r for r in (blocked.get("blocked_paths") or []) if r.get("path_id") == bp), None)
        ok(f"blocked.{bp}", row is not None and row.get("status") == "blocked")

    ok("closure.pass", closure.get("closure_pass") is True)
    ok("closure.final", closure.get("final_decision") == FINAL_DECISION_GO)
    ok("closure.next", closure.get("recommended_next_phase") == NEXT_PHASE_GO)

    for field in BOUNDARY_TRUE:
        ok(f"boundary_true.{field}", summary.get(field) is True)

    for field in BOUNDARY_FALSE:
        ok(f"boundary_false.{field}", summary.get(field) is False)

    ok("summary.candidate_gen", summary.get("compressed_lifecycle_candidate_generated_now") is True)
    ok("summary.no_exec", summary.get("compressed_lifecycle_executed_now") is False)
    ok("summary.no_formal", summary.get("formal_request_artifact_generated_now") is False)
    ok("summary.no_sent", summary.get("authorization_request_sent_now") is False)
    ok("summary.no_grant", summary.get("grant_issued_now") is False)
    ok("summary.no_window", summary.get("execution_window_opened_now") is False)
    ok("summary.no_real_dep", summary.get("real_dependency_check_executed_now") is False)
    ok("summary.null_provider", summary.get("selected_provider_for_execution") is None)

    ok("non_claims", len(_load(root / "non_claims_register_v1.json").get("non_claims") or []) >= len(NON_CLAIMS))
    ok("factory_dr_final", FACTORY_DR_FINAL is not None)
    ok("lifecycle.upstream", CURRENT_REQUEST_DRYRUN_STATE == "request_artifact_candidate_ready")

    passed = all(c["passed"] for c in checks) and len(checks) >= MIN_CHECKS
    report = {
        "phase": PHASE_ID,
        "verifier": "GO" if passed else "NO_GO",
        "passed": passed,
        "check_count": len(checks),
        "final_decision": summary.get("final_decision"),
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({"verifier": report["verifier"], "check_count": len(checks), "passed": passed}, ensure_ascii=False))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
