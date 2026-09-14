#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify OCR Provider Authorization Request Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.ocr_provider_authorization_dryrun_v1 import CURRENT_DRYRUN_STATE
from capabilities.governance.ocr_provider_authorization_planning_v1 import (
    AUTHORIZATION_SCOPE_COVERED,
    EVIDENCE_REQUIREMENTS,
)
from capabilities.governance.ocr_provider_authorization_post_dryrun_review_v1 import (
    FINAL_DECISION_GO as POST_REVIEW_FINAL,
    NEXT_PHASE_GO as POST_REVIEW_NEXT,
)
from capabilities.governance.ocr_provider_authorization_request_planning_v1 import (
    BLOCKED_PATHS,
    BOUNDARY_FALSE,
    CURRENT_LIFECYCLE_STATE,
    FINAL_DECISION_GO,
    LIFECYCLE_STATES,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    REQUEST_ARTIFACT_SCHEMA_STATE,
    SCOPE,
    SEND_BOUNDARY_CLAIMS,
    VALIDATION_RULES,
)

MIN_CHECKS = 75

REQUIRED = (
    "ocr_provider_authorization_request_planning_policy_v1.json",
    "authorization_post_dryrun_review_input_review_v1.json",
    "authorization_request_artifact_schema_v1.json",
    "authorization_request_generation_precondition_v1.json",
    "authorization_request_field_binding_plan_v1.json",
    "authorization_request_validation_rule_plan_v1.json",
    "authorization_request_owner_operator_approval_plan_v1.json",
    "authorization_request_send_boundary_plan_v1.json",
    "authorization_request_lifecycle_plan_v1.json",
    "authorization_request_evidence_binding_plan_v1.json",
    "authorization_request_blocked_path_matrix_v1.json",
    "authorization_request_dryrun_plan_v1.json",
    "non_claims_register_v1.json",
    "authorization_request_planning_decision_v1.json",
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
            "ocr_provider_authorization_request_planning"
        ),
    )
    p.add_argument(
        "--ocr-provider-authorization-post-dryrun-review-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "ocr_provider_authorization_post_dryrun_review"
        ),
    )
    p.add_argument(
        "--ocr-provider-authorization-dryrun-root",
        default="/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/ocr_provider_authorization_dryrun",
    )
    args = p.parse_args()
    root = Path(args.output_root)
    post_root = Path(args.ocr_provider_authorization_post_dryrun_review_root)
    dryrun_root = Path(args.ocr_provider_authorization_dryrun_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    summary = _load(root / "summary.json")
    input_review = _load(root / "authorization_post_dryrun_review_input_review_v1.json")
    schema = _load(root / "authorization_request_artifact_schema_v1.json")
    precond = _load(root / "authorization_request_generation_precondition_v1.json")
    bindings = _load(root / "authorization_request_field_binding_plan_v1.json")
    validation = _load(root / "authorization_request_validation_rule_plan_v1.json")
    approval = _load(root / "authorization_request_owner_operator_approval_plan_v1.json")
    send_boundary = _load(root / "authorization_request_send_boundary_plan_v1.json")
    lifecycle = _load(root / "authorization_request_lifecycle_plan_v1.json")
    evidence = _load(root / "authorization_request_evidence_binding_plan_v1.json")
    blocked = _load(root / "authorization_request_blocked_path_matrix_v1.json")
    dryrun_plan = _load(root / "authorization_request_dryrun_plan_v1.json")
    decision = _load(root / "authorization_request_planning_decision_v1.json")

    post_vr = _load(post_root / "verifier_report.json")
    post_sm = _load(post_root / "summary.json")
    post_closure = _load(post_root / "authorization_closure_decision_v1.json")
    dryrun_sm = _load(dryrun_root / "summary.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.planning_only", summary.get("ocr_provider_authorization_request_planning_only") is True)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.state", summary.get("current_lifecycle_state") == CURRENT_LIFECYCLE_STATE)
    ok("summary.null_provider", summary.get("selected_provider_for_execution") is None)

    ok("upstream.post_go", post_vr.get("verifier") == "GO")
    ok("upstream.post_final", post_sm.get("final_decision") == POST_REVIEW_FINAL)
    ok("upstream.post_next", post_sm.get("recommended_next_phase") == POST_REVIEW_NEXT)
    ok("upstream.post_closed", post_closure.get("ocr_provider_authorization_dryrun_closed") is True)
    ok("upstream.post_state", post_sm.get("current_lifecycle_state") == CURRENT_DRYRUN_STATE)
    ok("input.pass", input_review.get("review_pass") is True)

    ok("schema.type", schema.get("request_type") == "ocr_provider_authorization_request")
    ok("schema.lifecycle", schema.get("lifecycle_state") == REQUEST_ARTIFACT_SCHEMA_STATE)
    ok("schema.candidate_ref", bool(schema.get("related_authorization_request_candidate_ref")))
    ok("schema.scope5", len(schema.get("target_scope") or []) == len(AUTHORIZATION_SCOPE_COVERED))
    ok("schema.window_ref", bool(schema.get("requested_execution_window_ref")))
    ok("schema.sandbox_ref", bool(schema.get("sandbox_boundary_ref")))
    ok("schema.rollback_ref", bool(schema.get("rollback_plan_ref")))
    ok("schema.evidence_ref", bool(schema.get("evidence_requirement_ref")))
    ok("schema.owner", schema.get("owner_operator_approval_required") is True)
    ok("schema.verifier", schema.get("verifier_required") is True)
    ok("schema.post_review", schema.get("post_execution_review_required") is True)
    ok("schema.no_gen", schema.get("generated_now") is False)
    ok("schema.no_sent", schema.get("sent_now") is False)
    ok("schema.no_approved", schema.get("approved_now") is False)

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
    ok("precond.no_gen_now", precond.get("artifact_generation_allowed_now") is False)

    ok("bindings.count7", bindings.get("binding_count") == 7)
    ok("bindings.list7", len(bindings.get("bindings") or []) == 7)

    ok("validation.count8", validation.get("rule_count") == len(VALIDATION_RULES))
    ok("validation.rules8", len(validation.get("rules") or []) == len(VALIDATION_RULES))
    ok("validation.blocked", validation.get("artifact_generation_blocked_in_planning") is True)

    ok("approval.required", approval.get("owner_operator_approval_required") is True)
    ok("approval.not_collected", approval.get("approval_collected_now") is False)

    ok("send.claims5", len(send_boundary.get("send_boundary_claims") or []) == len(SEND_BOUNDARY_CLAIMS))
    ok("send.planned_not_gen", send_boundary.get("request_artifact_planned_not_generated") is True)
    ok("send.no_artifact", send_boundary.get("authorization_request_artifact_generated_now") is False)
    ok("send.no_sent", send_boundary.get("authorization_request_sent_now") is False)

    ok("lifecycle.current", lifecycle.get("current_state") == CURRENT_LIFECYCLE_STATE)
    ok("lifecycle.count11", len(lifecycle.get("states") or []) == len(LIFECYCLE_STATES))
    ok("lifecycle.prior", lifecycle.get("prior_authorization_state") == CURRENT_DRYRUN_STATE)

    ok("evidence.count11", evidence.get("artifact_count") == len(EVIDENCE_REQUIREMENTS))
    ok("evidence.required", evidence.get("evidence_package_required") is True)

    ok("blocked.count15", blocked.get("path_count") == len(BLOCKED_PATHS))
    ok("blocked.all", blocked.get("all_blocked") is True)

    ok("dryrun.next", dryrun_plan.get("next_phase") == NEXT_PHASE_GO)
    ok("decision.ready", decision.get("ready_for_dryrun") is True)
    ok("decision.final", decision.get("final_decision") == FINAL_DECISION_GO)

    ok("summary.no_artifact", summary.get("authorization_request_artifact_generated_now") is False)
    ok("summary.no_sent", summary.get("authorization_request_sent_now") is False)
    ok("summary.no_persist", summary.get("authorization_request_persisted_now") is False)
    ok("summary.no_approved", summary.get("authorization_request_approved_now") is False)
    ok("summary.no_grant", summary.get("grant_issued_now") is False)
    ok("summary.no_auth", summary.get("provider_authorization_granted_now") is False)
    ok("summary.no_window", summary.get("execution_window_opened_now") is False)
    ok("summary.no_real_dep", summary.get("real_dependency_check_executed_now") is False)

    for field in BOUNDARY_FALSE:
        ok(f"boundary.{field}", summary.get(field) is False)

    ok("non_claims", len(_load(root / "non_claims_register_v1.json").get("non_claims") or []) >= len(NON_CLAIMS))

    ok("upstream.dryrun_req_cand", dryrun_sm.get("authorization_request_candidate_generated_now") is True)

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
