#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify OCR Provider Authorization Request Post-DryRun Review v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.ocr_provider_authorization_request_dryrun_v1 import (
    CURRENT_REQUEST_DRYRUN_STATE,
    DRYRUN_BLOCKED_PATHS,
    EVIDENCE_REQUIREMENTS,
    FINAL_DECISION_GO as REQUEST_DRYRUN_FINAL,
    LIFECYCLE_STATES,
    NEXT_PHASE_GO as REQUEST_DRYRUN_NEXT,
    SEND_BOUNDARY_DRYRUN_CLAIMS,
    VALIDATION_RULE_IDS,
)
from capabilities.governance.ocr_provider_authorization_request_planning_v1 import (
    CURRENT_LIFECYCLE_STATE as REQUEST_PLANNING_STATE,
)
from capabilities.governance.ocr_provider_authorization_request_post_dryrun_review_v1 import (
    BOUNDARY_FALSE_REVIEW,
    FINAL_DECISION_GO,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    REVIEW_SCOPE,
)

MIN_CHECKS = 85

REQUIRED = (
    "authorization_request_dryrun_input_review_v1.json",
    "request_artifact_candidate_review_v1.json",
    "request_artifact_schema_validation_review_v1.json",
    "generation_precondition_review_v1.json",
    "field_binding_review_v1.json",
    "validation_rule_review_v1.json",
    "send_boundary_review_v1.json",
    "request_lifecycle_review_v1.json",
    "request_evidence_binding_review_v1.json",
    "request_blocked_path_review_v1.json",
    "request_no_artifact_no_send_review_v1.json",
    "authorization_request_closure_decision_v1.json",
    "next_route_readiness_decision_v1.json",
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
            "ocr_provider_authorization_request_post_dryrun_review"
        ),
    )
    p.add_argument(
        "--ocr-provider-authorization-request-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "ocr_provider_authorization_request_dryrun"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    dryrun_root = Path(args.ocr_provider_authorization_request_dryrun_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    summary = _load(root / "summary.json")
    input_review = _load(root / "authorization_request_dryrun_input_review_v1.json")
    candidate_r = _load(root / "request_artifact_candidate_review_v1.json")
    schema_r = _load(root / "request_artifact_schema_validation_review_v1.json")
    precond_r = _load(root / "generation_precondition_review_v1.json")
    binding_r = _load(root / "field_binding_review_v1.json")
    validation_r = _load(root / "validation_rule_review_v1.json")
    send_r = _load(root / "send_boundary_review_v1.json")
    lifecycle_r = _load(root / "request_lifecycle_review_v1.json")
    evidence_r = _load(root / "request_evidence_binding_review_v1.json")
    blocked_r = _load(root / "request_blocked_path_review_v1.json")
    audit_r = _load(root / "request_no_artifact_no_send_review_v1.json")
    closure = _load(root / "authorization_request_closure_decision_v1.json")
    next_route = _load(root / "next_route_readiness_decision_v1.json")

    dryrun_vr = _load(dryrun_root / "verifier_report.json")
    dryrun_sm = _load(dryrun_root / "summary.json")
    candidate = _load(dryrun_root / "request_artifact_candidate_v1.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("review_scope") == REVIEW_SCOPE)
    ok("summary.review_only", summary.get("review_only") is True)
    ok("summary.post_review_only", summary.get("ocr_provider_authorization_request_post_dryrun_review_only") is True)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.closed", summary.get("ocr_provider_authorization_request_dryrun_closed") is True)
    ok("summary.state", summary.get("current_lifecycle_state") == CURRENT_REQUEST_DRYRUN_STATE)

    ok("upstream.dryrun_go", dryrun_vr.get("verifier") == "GO")
    ok("upstream.dryrun_final", dryrun_sm.get("final_decision") == REQUEST_DRYRUN_FINAL)
    ok("upstream.dryrun_next", dryrun_sm.get("recommended_next_phase") == REQUEST_DRYRUN_NEXT)
    ok("upstream.candidate_gen", dryrun_sm.get("request_artifact_candidate_generated_now") is True)
    ok("upstream.candidate_file", (dryrun_root / "request_artifact_candidate_v1.json").is_file())

    ok("input.pass", input_review.get("review_pass") is True)

    ok("candidate.pass", candidate_r.get("review_pass") is True)
    ok("candidate.candidate_only", candidate.get("candidate_only") is True)
    ok("candidate.no_formal", candidate.get("formal_artifact_generated_now") is False)

    ok("schema.pass", schema_r.get("review_pass") is True)
    ok("schema.count8", schema_r.get("check_count") == 8)

    ok("precond.pass", precond_r.get("review_pass") is True)
    ok("binding.pass", binding_r.get("review_pass") is True)
    ok("binding.count7", binding_r.get("binding_count") == 7)
    ok("validation.pass", validation_r.get("review_pass") is True)
    ok("validation.count8", validation_r.get("rule_count") == len(VALIDATION_RULE_IDS))
    ok("send.pass", send_r.get("review_pass") is True)
    ok("lifecycle.pass", lifecycle_r.get("review_pass") is True)
    ok("lifecycle.prior", lifecycle_r.get("prior_state") == REQUEST_PLANNING_STATE)
    ok("lifecycle.current", lifecycle_r.get("current_state") == CURRENT_REQUEST_DRYRUN_STATE)
    ok("lifecycle.count11", lifecycle_r.get("state_count") == len(LIFECYCLE_STATES))
    ok("evidence.pass", evidence_r.get("review_pass") is True)
    ok("evidence.count11", evidence_r.get("artifact_count") == len(EVIDENCE_REQUIREMENTS))
    ok("blocked.pass", blocked_r.get("review_pass") is True)
    ok("blocked.count17", blocked_r.get("paths_total") == len(DRYRUN_BLOCKED_PATHS))
    ok("audit.pass", audit_r.get("review_pass") is True)

    ok("closure.closed", closure.get("ocr_provider_authorization_request_dryrun_closed") is True)
    ok("closure.candidate_trusted", closure.get("request_artifact_candidate_trusted") is True)
    ok("closure.formal_planning", closure.get("ready_for_formal_request_artifact_generation_planning") is True)
    ok("closure.final", closure.get("final_decision") == FINAL_DECISION_GO)

    ok("next.ready", next_route.get("ready_for_formal_request_artifact_generation_planning") is True)
    ok("next.no_formal", next_route.get("do_not_generate_formal_request_artifact_now") is True)
    ok("next.no_persist", next_route.get("do_not_persist_request_now") is True)
    ok("next.no_send", next_route.get("do_not_send_request_now") is True)
    ok("next.no_approval", next_route.get("do_not_collect_approval_now") is True)
    ok("next.no_grant", next_route.get("do_not_grant_authorization_now") is True)
    ok("next.no_window", next_route.get("do_not_open_execution_window_now") is True)
    ok("next.no_real_dep", next_route.get("do_not_execute_real_dependency_check_now") is True)

    ok("summary.no_new_candidate", summary.get("new_request_artifact_candidate_generated_now") is False)
    ok("summary.no_artifact", summary.get("authorization_request_artifact_generated_now") is False)
    ok("summary.no_persist", summary.get("authorization_request_persisted_now") is False)
    ok("summary.no_sent", summary.get("authorization_request_sent_now") is False)
    ok("summary.no_approved", summary.get("authorization_request_approved_now") is False)
    ok("summary.no_grant", summary.get("grant_issued_now") is False)
    ok("summary.null_provider", summary.get("selected_provider_for_execution") is None)

    for field in BOUNDARY_FALSE_REVIEW:
        ok(f"boundary.{field}", summary.get(field) is False)

    ok("non_claims", len(_load(root / "non_claims_register_v1.json").get("non_claims") or []) >= len(NON_CLAIMS))
    ok("send.claims5", len(SEND_BOUNDARY_DRYRUN_CLAIMS) == 5)

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
