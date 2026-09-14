#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify OCR Provider Authorization Request DryRun v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.ocr_provider_authorization_dryrun_v1 import (
    CURRENT_DRYRUN_STATE as AUTH_DRYRUN_STATE,
    EVIDENCE_REQUIREMENTS,
)
from capabilities.governance.ocr_provider_authorization_request_dryrun_v1 import (
    BOUNDARY_FALSE,
    CURRENT_REQUEST_DRYRUN_STATE,
    DRYRUN_BLOCKED_PATHS,
    FINAL_DECISION_GO,
    LIFECYCLE_STATES,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    SCOPE,
    SEND_BOUNDARY_DRYRUN_CLAIMS,
    VALIDATION_RULE_IDS,
)
from capabilities.governance.ocr_provider_authorization_request_planning_v1 import (
    BLOCKED_PATHS as PLANNING_BLOCKED_PATHS,
    CURRENT_LIFECYCLE_STATE as PLANNING_LIFECYCLE_STATE,
    FINAL_DECISION_GO as PLANNING_FINAL,
    NEXT_PHASE_GO as PLANNING_NEXT,
)

MIN_CHECKS = 85

REQUIRED = (
    "ocr_provider_authorization_request_dryrun_policy_v1.json",
    "authorization_request_planning_input_review_v1.json",
    "request_artifact_candidate_v1.json",
    "request_artifact_schema_validation_result_v1.json",
    "generation_precondition_dryrun_result_v1.json",
    "field_binding_dryrun_result_v1.json",
    "validation_rule_dryrun_result_v1.json",
    "send_boundary_dryrun_result_v1.json",
    "request_lifecycle_dryrun_result_v1.json",
    "request_evidence_binding_dryrun_result_v1.json",
    "request_blocked_path_result_v1.json",
    "request_no_artifact_no_send_audit_v1.json",
    "request_dryrun_readiness_decision_v1.json",
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
            "ocr_provider_authorization_request_dryrun"
        ),
    )
    p.add_argument(
        "--ocr-provider-authorization-request-planning-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "ocr_provider_authorization_request_planning"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    planning_root = Path(args.ocr_provider_authorization_request_planning_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    summary = _load(root / "summary.json")
    input_review = _load(root / "authorization_request_planning_input_review_v1.json")
    candidate = _load(root / "request_artifact_candidate_v1.json")
    schema_val = _load(root / "request_artifact_schema_validation_result_v1.json")
    precond = _load(root / "generation_precondition_dryrun_result_v1.json")
    bindings = _load(root / "field_binding_dryrun_result_v1.json")
    validation = _load(root / "validation_rule_dryrun_result_v1.json")
    send_boundary = _load(root / "send_boundary_dryrun_result_v1.json")
    lifecycle = _load(root / "request_lifecycle_dryrun_result_v1.json")
    evidence = _load(root / "request_evidence_binding_dryrun_result_v1.json")
    blocked = _load(root / "request_blocked_path_result_v1.json")
    audit = _load(root / "request_no_artifact_no_send_audit_v1.json")
    readiness = _load(root / "request_dryrun_readiness_decision_v1.json")

    plan_vr = _load(planning_root / "verifier_report.json")
    plan_sm = _load(planning_root / "summary.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.dryrun_only", summary.get("ocr_provider_authorization_request_dryrun_only") is True)
    ok("summary.simulated", summary.get("simulated") is True)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.state", summary.get("current_lifecycle_state") == CURRENT_REQUEST_DRYRUN_STATE)
    ok("summary.candidate_gen", summary.get("request_artifact_candidate_generated_now") is True)

    ok("upstream.plan_go", plan_vr.get("verifier") == "GO")
    ok("upstream.plan_final", plan_sm.get("final_decision") == PLANNING_FINAL)
    ok("upstream.plan_next", plan_sm.get("recommended_next_phase") == PLANNING_NEXT)
    ok("upstream.plan_state", plan_sm.get("current_lifecycle_state") == PLANNING_LIFECYCLE_STATE)
    ok("input.pass", input_review.get("review_pass") is True)
    ok("input.schema", input_review.get("schema_planned") is True)
    ok("input.precond", input_review.get("preconditions_planned") is True)
    ok("input.bindings", input_review.get("bindings_planned") is True)

    ok("candidate.type", candidate.get("request_type") == "ocr_provider_authorization_request")
    ok("candidate.lifecycle", candidate.get("lifecycle_state") == CURRENT_REQUEST_DRYRUN_STATE)
    ok("candidate.candidate_only", candidate.get("candidate_only") is True)
    ok("candidate.no_formal", candidate.get("formal_artifact_generated_now") is False)
    ok("candidate.no_persist", candidate.get("persisted_now") is False)
    ok("candidate.no_sent", candidate.get("sent_now") is False)
    ok("candidate.no_approved", candidate.get("approved_now") is False)
    ok("candidate.owner", candidate.get("owner_operator_approval_required") is True)
    ok("candidate.verifier", candidate.get("verifier_required") is True)
    ok("candidate.post_review", candidate.get("post_execution_review_required") is True)
    ok("candidate.ref", bool(candidate.get("related_authorization_request_candidate_ref")))
    ok("candidate.window_ref", bool(candidate.get("requested_execution_window_ref")))
    ok("candidate.sandbox_ref", bool(candidate.get("sandbox_boundary_ref")))
    ok("candidate.rollback_ref", bool(candidate.get("rollback_plan_ref")))
    ok("candidate.evidence_ref", bool(candidate.get("evidence_requirement_ref")))

    ok("schema_val.all", schema_val.get("all_pass") is True)

    ok("precond.pass", precond.get("dryrun_pass") is True)
    ok("precond.post_go", precond.get("authorization_post_dryrun_review_go") is True)
    ok("precond.req_ready", precond.get("request_candidate_ready") is True)
    ok("precond.grant", precond.get("grant_candidate_available") is True)
    ok("precond.window", precond.get("execution_window_candidate_available") is True)
    ok("precond.sandbox", precond.get("sandbox_boundary_candidate_available") is True)
    ok("precond.rollback", precond.get("rollback_candidate_available") is True)
    ok("precond.evidence", precond.get("evidence_requirement_candidate_available") is True)
    ok("precond.null_provider", precond.get("selected_provider_for_execution") is None)
    ok("precond.not_final", precond.get("provider_selection_finalized") is False)
    ok("precond.all_blocked", precond.get("all_boundary_paths_blocked") is True)

    ok("bindings.count7", bindings.get("binding_count") == 7)
    ok("bindings.all", bindings.get("all_pass") is True)

    ok("validation.count8", validation.get("rule_count") == len(VALIDATION_RULE_IDS))
    ok("validation.all", validation.get("all_pass") is True)

    ok("send.claims5", len(send_boundary.get("send_boundary_claims") or []) == len(SEND_BOUNDARY_DRYRUN_CLAIMS))
    ok("send.pass", send_boundary.get("dryrun_pass") is True)

    ok("lifecycle.prior", lifecycle.get("prior_state") == PLANNING_LIFECYCLE_STATE)
    ok("lifecycle.current", lifecycle.get("current_state") == CURRENT_REQUEST_DRYRUN_STATE)
    ok("lifecycle.count11", len(lifecycle.get("states") or []) == len(LIFECYCLE_STATES))
    ok("lifecycle.no_formal", lifecycle.get("formal_artifact_generated_now") is False)
    ok("lifecycle.no_sent", lifecycle.get("request_sent_now") is False)
    ok("lifecycle.no_grant", lifecycle.get("grant_issued_now") is False)
    ok("lifecycle.no_window", lifecycle.get("execution_window_opened_now") is False)
    ok("lifecycle.pass", lifecycle.get("lifecycle_dryrun_pass") is True)

    ok("evidence.count11", evidence.get("artifact_count") == len(EVIDENCE_REQUIREMENTS))
    ok("evidence.pass", evidence.get("dryrun_pass") is True)

    ok("blocked.count17", blocked.get("path_count") == len(DRYRUN_BLOCKED_PATHS))
    ok("blocked.all", blocked.get("all_blocked") is True)

    ok("audit.pass", audit.get("audit_pass") is True)
    ok("audit.no_formal", audit.get("no_formal_request_artifact") is True)
    ok("audit.no_persist", audit.get("no_persistence") is True)
    ok("audit.no_send", audit.get("no_send") is True)
    ok("audit.no_approval", audit.get("no_approval") is True)
    ok("audit.no_grant", audit.get("no_grant") is True)
    ok("audit.no_window", audit.get("no_execution_window") is True)
    ok("audit.no_provider", audit.get("no_provider_action") is True)
    ok("audit.no_ocr", audit.get("no_ocr_action") is True)

    ok("readiness.all", readiness.get("all_pass") is True)
    ok("readiness.final", readiness.get("final_decision") == FINAL_DECISION_GO)
    ok("readiness.next", readiness.get("recommended_next_phase") == NEXT_PHASE_GO)

    ok("summary.no_artifact", summary.get("authorization_request_artifact_generated_now") is False)
    ok("summary.no_persist", summary.get("authorization_request_persisted_now") is False)
    ok("summary.no_sent", summary.get("authorization_request_sent_now") is False)
    ok("summary.no_approved", summary.get("authorization_request_approved_now") is False)
    ok("summary.no_grant", summary.get("grant_issued_now") is False)
    ok("summary.no_window", summary.get("execution_window_opened_now") is False)
    ok("summary.no_real_dep", summary.get("real_dependency_check_executed_now") is False)
    ok("summary.null_provider", summary.get("selected_provider_for_execution") is None)

    for field in BOUNDARY_FALSE:
        ok(f"boundary.{field}", summary.get(field) is False)

    ok("non_claims", len(_load(root / "non_claims_register_v1.json").get("non_claims") or []) >= len(NON_CLAIMS))

    ok("planning.blocked15", len(PLANNING_BLOCKED_PATHS) == 15)
    ok("auth_dryrun.state", AUTH_DRYRUN_STATE == "request_candidate_ready")

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
