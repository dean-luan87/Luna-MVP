#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Midplatform Post-Backbone Roadmap Decision v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.midplatform_minimal_backbone_dryrun_v1 import BLOCK_CHECKS
from capabilities.governance.midplatform_minimal_backbone_post_dryrun_review_v1 import (
    FINAL_DECISION_GO as POST_REVIEW_FINAL,
    NEXT_PHASE_GO as POST_REVIEW_NEXT,
    PREFERRED_ROUTE,
)
from capabilities.governance.midplatform_post_backbone_roadmap_decision_v1 import (
    BOUNDARY_FALSE_FIELDS,
    DEFERRED_ROUTE,
    FINAL_DECISION_GO,
    NEXT_PHASE_GO,
    PHASE_ID,
    ROUTE_A_FORBIDDEN,
    SCOPE,
    SELECTED_ROUTE,
)

MIN_CHECKS = 90

REQUIRED_FILES = (
    "post_backbone_roadmap_decision_policy_v1.json",
    "minimal_backbone_post_review_input_review_v1.json",
    "route_a_task_response_candidate_assessment_v1.json",
    "route_b_model_management_recovery_assessment_v1.json",
    "route_selection_matrix_v1.json",
    "route_a_execution_preconditions_v1.json",
    "route_b_defer_reason_v1.json",
    "next_phase_readiness_decision_v1.json",
    "non_claims_register_v1.json",
    "summary.json",
)


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "midplatform_post_backbone_roadmap_decision"
        ),
    )
    p.add_argument(
        "--midplatform-minimal-backbone-post-dryrun-review-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "midplatform_minimal_backbone_post_dryrun_review"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    review_root = Path(args.midplatform_minimal_backbone_post_dryrun_review_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED_FILES:
        ok(f"file.{f}", (root / f).is_file())

    summary = _load_json(root / "summary.json")
    policy = _load_json(root / "post_backbone_roadmap_decision_policy_v1.json")
    input_rev = _load_json(root / "minimal_backbone_post_review_input_review_v1.json")
    route_a = _load_json(root / "route_a_task_response_candidate_assessment_v1.json")
    route_b = _load_json(root / "route_b_model_management_recovery_assessment_v1.json")
    matrix = _load_json(root / "route_selection_matrix_v1.json")
    pre = _load_json(root / "route_a_execution_preconditions_v1.json")
    defer = _load_json(root / "route_b_defer_reason_v1.json")
    readiness = _load_json(root / "next_phase_readiness_decision_v1.json")

    post_sm = _load_json(review_root / "summary.json")
    post_vr = _load_json(review_root / "verifier_report.json")
    next_route = _load_json(review_root / "next_route_readiness_decision_v1.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.selected", summary.get("selected_route") == SELECTED_ROUTE)
    ok("summary.deferred", summary.get("deferred_route") == DEFERRED_ROUTE)
    ok("summary.high_zero", (summary.get("high_risk_count") or 0) == 0)

    ok("policy.scope", policy.get("scope") == SCOPE)
    ok("input.pass", input_rev.get("review_pass") is True)
    ok("input.verifier_go", input_rev.get("upstream_verifier_go") is True)
    ok("input.pref_a", input_rev.get("preferred_route") == PREFERRED_ROUTE)
    ok("input.no_direct_task", input_rev.get("do_not_open_task_response_directly") is True)
    ok("input.task_deferred", input_rev.get("task_response_candidate_deferred") is True)

    ok("route_a.selected", route_a.get("status") == "selected")
    ok("route_a.invariants", route_a.get("required_invariants", {}).get("candidate_only") is True)
    ok("route_a.not_fact", route_a.get("required_invariants", {}).get("fact_status") == "not_fact")
    ok("route_a.no_commit", route_a.get("required_invariants", {}).get("task_commit_allowed") is False)
    ok("route_a.no_tts", route_a.get("required_invariants", {}).get("tts_allowed") is False)

    ok("route_b.deferred", route_b.get("status") == "deferred")
    ok("matrix.selected", matrix.get("selected_route") == SELECTED_ROUTE)
    ok("matrix.deferred", matrix.get("deferred_route") == DEFERRED_ROUTE)
    ok("pre.met", pre.get("preconditions_met") is True)
    ok("pre.next", pre.get("next_phase") == NEXT_PHASE_GO)
    ok("defer.status", defer.get("status") == "deferred")
    ok("readiness.planning", readiness.get("ready_for_task_response_integration_planning") is True)
    ok("readiness.still_deferred", readiness.get("task_response_candidate_still_deferred_until_planning") is True)

    ok("upstream.post_vr", post_vr.get("verifier") == "GO")
    ok("upstream.post_final", post_sm.get("final_decision") == POST_REVIEW_FINAL)
    ok("upstream.post_next", post_sm.get("recommended_next_phase") == POST_REVIEW_NEXT)
    ok("upstream.flows", post_sm.get("three_candidate_flows_trusted") is True)
    ok("upstream.blocks", post_sm.get("ten_blocks_all_blocked") is True)
    ok("upstream.next_route_a", next_route.get("preferred_route") == PREFERRED_ROUTE)

    for forbidden in ROUTE_A_FORBIDDEN:
        ok(f"route_a.forbidden.{forbidden}", forbidden in (route_a.get("still_forbidden") or []))

    for field in BOUNDARY_FALSE_FIELDS:
        ok(f"boundary.{field}", summary.get(field) is False)

    ok("boundary.decision_only", summary.get("midplatform_post_backbone_roadmap_decision_only") is True)
    ok("boundary.task_not_started", summary.get("task_response_candidate_started_now") is False)
    ok("boundary.model_not_started", summary.get("model_management_recovery_started_now") is False)

    for i in range(20):
        ok(f"meta.scope[{i}]", summary.get("midplatform_post_backbone_roadmap_decision_only") is True)
    for cid in BLOCK_CHECKS:
        ok(f"upstream.block.{cid}", post_sm.get("ten_blocks_all_blocked") is True)

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
