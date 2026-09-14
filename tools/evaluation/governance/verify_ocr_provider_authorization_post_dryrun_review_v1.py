#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify OCR Provider Authorization Post-DryRun Review v1."""

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
    CURRENT_DRYRUN_STATE,
    DRYRUN_BLOCKED_PATHS,
    EVIDENCE_REQUIREMENTS,
    FINAL_DECISION_GO as DRYRUN_FINAL,
    NEXT_PHASE_GO as DRYRUN_NEXT,
)
from capabilities.governance.ocr_provider_authorization_planning_v1 import (
    CURRENT_LIFECYCLE_STATE as PLANNING_LIFECYCLE_STATE,
)
from capabilities.governance.ocr_provider_authorization_post_dryrun_review_v1 import (
    BOUNDARY_FALSE_REVIEW,
    FINAL_DECISION_GO,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    REVIEW_SCOPE,
)

MIN_CHECKS = 75

REQUIRED = (
    "ocr_provider_authorization_dryrun_input_review_v1.json",
    "authorization_request_candidate_review_v1.json",
    "grant_candidate_review_v1.json",
    "execution_window_candidate_review_v1.json",
    "sandbox_boundary_candidate_review_v1.json",
    "rollback_candidate_review_v1.json",
    "evidence_requirement_candidate_review_v1.json",
    "owner_operator_approval_review_v1.json",
    "provider_selection_binding_review_v1.json",
    "authorization_lifecycle_review_v1.json",
    "authorization_boundary_guard_review_v1.json",
    "authorization_blocked_path_review_v1.json",
    "authorization_closure_decision_v1.json",
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
            "ocr_provider_authorization_post_dryrun_review"
        ),
    )
    p.add_argument(
        "--ocr-provider-authorization-dryrun-root",
        default="/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/ocr_provider_authorization_dryrun",
    )
    args = p.parse_args()
    root = Path(args.output_root)
    dryrun_root = Path(args.ocr_provider_authorization_dryrun_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    summary = _load(root / "summary.json")
    input_review = _load(root / "ocr_provider_authorization_dryrun_input_review_v1.json")
    request_r = _load(root / "authorization_request_candidate_review_v1.json")
    grant_r = _load(root / "grant_candidate_review_v1.json")
    window_r = _load(root / "execution_window_candidate_review_v1.json")
    sandbox_r = _load(root / "sandbox_boundary_candidate_review_v1.json")
    rollback_r = _load(root / "rollback_candidate_review_v1.json")
    evidence_r = _load(root / "evidence_requirement_candidate_review_v1.json")
    owner_r = _load(root / "owner_operator_approval_review_v1.json")
    selection_r = _load(root / "provider_selection_binding_review_v1.json")
    lifecycle_r = _load(root / "authorization_lifecycle_review_v1.json")
    boundary_r = _load(root / "authorization_boundary_guard_review_v1.json")
    blocked_r = _load(root / "authorization_blocked_path_review_v1.json")
    closure = _load(root / "authorization_closure_decision_v1.json")
    next_route = _load(root / "next_route_readiness_decision_v1.json")

    dryrun_vr = _load(dryrun_root / "verifier_report.json")
    dryrun_sm = _load(dryrun_root / "summary.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("review_scope") == REVIEW_SCOPE)
    ok("summary.review_only", summary.get("review_only") is True)
    ok("summary.post_review_only", summary.get("ocr_provider_authorization_post_dryrun_review_only") is True)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.closed", summary.get("ocr_provider_authorization_dryrun_closed") is True)
    ok("summary.state", summary.get("current_lifecycle_state") == CURRENT_DRYRUN_STATE)

    ok("upstream.dryrun_go", dryrun_vr.get("verifier") == "GO")
    ok("upstream.dryrun_final", dryrun_sm.get("final_decision") == DRYRUN_FINAL)
    ok("upstream.dryrun_next", dryrun_sm.get("recommended_next_phase") == DRYRUN_NEXT)
    ok("upstream.req_cand", dryrun_sm.get("authorization_request_candidate_generated_now") is True)
    ok("upstream.grant_cand", dryrun_sm.get("grant_candidate_generated_now") is True)

    ok("input.pass", input_review.get("review_pass") is True)

    ok("request.pass", request_r.get("review_pass") is True)
    ok("grant.pass", grant_r.get("review_pass") is True)
    ok("window.pass", window_r.get("review_pass") is True)
    ok("sandbox.pass", sandbox_r.get("review_pass") is True)
    ok("rollback.pass", rollback_r.get("review_pass") is True)
    ok("evidence.pass", evidence_r.get("review_pass") is True)
    ok("evidence.count11", evidence_r.get("artifact_count") == len(EVIDENCE_REQUIREMENTS))
    ok("owner.pass", owner_r.get("review_pass") is True)
    ok("selection.pass", selection_r.get("review_pass") is True)
    ok("lifecycle.pass", lifecycle_r.get("review_pass") is True)
    ok("lifecycle.prior", lifecycle_r.get("prior_state") == PLANNING_LIFECYCLE_STATE)
    ok("lifecycle.current", lifecycle_r.get("current_state") == CURRENT_DRYRUN_STATE)
    ok("boundary.pass", boundary_r.get("review_pass") is True)
    ok("boundary.count15", boundary_r.get("path_count") == len(DRYRUN_BLOCKED_PATHS))
    ok("blocked.pass", blocked_r.get("review_pass") is True)
    ok("blocked.count15", blocked_r.get("paths_total") == len(DRYRUN_BLOCKED_PATHS))

    ok("closure.closed", closure.get("ocr_provider_authorization_dryrun_closed") is True)
    ok("closure.request_trusted", closure.get("authorization_request_candidate_trusted") is True)
    ok("closure.grant_trusted", closure.get("grant_candidate_trusted") is True)
    ok("closure.request_planning", closure.get("ready_for_authorization_request_planning") is True)
    ok("closure.final", closure.get("final_decision") == FINAL_DECISION_GO)

    ok("next.ready", next_route.get("ready_for_authorization_request_planning") is True)
    ok("next.no_artifact", next_route.get("do_not_generate_request_artifact_now") is True)
    ok("next.no_send", next_route.get("do_not_send_request_now") is True)
    ok("next.no_grant", next_route.get("do_not_grant_authorization_now") is True)
    ok("next.no_window", next_route.get("do_not_open_execution_window_now") is True)
    ok("next.no_real_dep", next_route.get("do_not_execute_real_dependency_check_now") is True)

    ok("summary.no_new_request", summary.get("new_authorization_request_candidate_generated_now") is False)
    ok("summary.no_new_grant", summary.get("new_grant_candidate_generated_now") is False)
    ok("summary.no_artifact", summary.get("authorization_request_artifact_generated_now") is False)
    ok("summary.no_grant", summary.get("provider_authorization_granted_now") is False)
    ok("summary.null_provider", summary.get("selected_provider_for_execution") is None)

    for field in BOUNDARY_FALSE_REVIEW:
        ok(f"boundary.{field}", summary.get(field) is False)

    ok("non_claims", len(_load(root / "non_claims_register_v1.json").get("non_claims") or []) >= len(NON_CLAIMS))

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
