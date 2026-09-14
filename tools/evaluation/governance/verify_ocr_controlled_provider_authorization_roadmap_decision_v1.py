#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify OCR Controlled Provider Authorization Roadmap Decision v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.ocr_controlled_provider_dryrun_v1 import BLOCKED_PATHS
from capabilities.governance.ocr_controlled_provider_post_dryrun_review_v1 import (
    FINAL_DECISION_GO as POST_REVIEW_FINAL,
)
from capabilities.governance.ocr_controlled_provider_authorization_roadmap_decision_v1 import (
    BLOCKED_ROUTE_C,
    BOUNDARY_FALSE,
    DEFERRED_ROUTE_A,
    DEFERRED_ROUTE_D,
    FINAL_DECISION_GO,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    ROUTE_B,
    SCOPE,
    SELECTED_ROUTE,
)

MIN_CHECKS = 59

REQUIRED = (
    "ocr_authorization_roadmap_decision_policy_v1.json",
    "ocr_post_dryrun_review_input_review_v1.json",
    "route_a_provider_authorization_planning_assessment_v1.json",
    "route_b_provider_selection_dependency_environment_assessment_v1.json",
    "route_c_controlled_trial_planning_assessment_v1.json",
    "route_d_defer_ocr_provider_assessment_v1.json",
    "ocr_authorization_route_selection_matrix_v1.json",
    "selected_route_preconditions_v1.json",
    "deferred_routes_register_v1.json",
    "next_phase_readiness_decision_v1.json",
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
            "ocr_controlled_provider_authorization_roadmap_decision"
        ),
    )
    p.add_argument(
        "--ocr-controlled-provider-post-dryrun-review-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "ocr_controlled_provider_post_dryrun_review"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    post_root = Path(args.ocr_controlled_provider_post_dryrun_review_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    summary = _load(root / "summary.json")
    matrix = _load(root / "ocr_authorization_route_selection_matrix_v1.json")
    route_a = _load(root / "route_a_provider_authorization_planning_assessment_v1.json")
    route_b = _load(root / "route_b_provider_selection_dependency_environment_assessment_v1.json")
    route_c = _load(root / "route_c_controlled_trial_planning_assessment_v1.json")
    route_d = _load(root / "route_d_defer_ocr_provider_assessment_v1.json")
    next_phase = _load(root / "next_phase_readiness_decision_v1.json")
    input_review = _load(root / "ocr_post_dryrun_review_input_review_v1.json")

    post_sm = _load(post_root / "summary.json")
    post_vr = _load(post_root / "verifier_report.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.decision_only", summary.get("ocr_controlled_provider_authorization_roadmap_decision_only") is True)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.selected", summary.get("selected_route") == SELECTED_ROUTE)
    ok("summary.defer_a", summary.get("deferred_route_a") == DEFERRED_ROUTE_A)
    ok("summary.block_c", summary.get("blocked_route_c") == BLOCKED_ROUTE_C)

    ok("route_a.deferred", route_a.get("status") == "deferred")
    ok("route_b.selected", route_b.get("status") == "selected")
    ok("route_c.blocked", route_c.get("status") == "blocked_until_authorization")
    ok("route_d.deferred", route_d.get("status") == "deferred")
    ok("matrix.selected", matrix.get("selected_route") == SELECTED_ROUTE)

    ok("next.ready", next_phase.get("ready_for_provider_selection_dependency_environment_planning") is True)
    ok("next.no_auth", next_phase.get("do_not_authorize_provider_now") is True)
    ok("next.no_trial", next_phase.get("do_not_start_controlled_trial_now") is True)

    ok("input.pass", input_review.get("review_pass") is True)
    ok("input.closed", input_review.get("ocr_controlled_provider_dryrun_closed") is True)
    ok("input.trusted", input_review.get("ocr_candidate_chain_trusted") is True)
    ok("input.readiness4", input_review.get("readiness_count") == 4)
    ok("input.blocked15", input_review.get("blocked_paths_count") == len(BLOCKED_PATHS))

    ok("upstream.post_go", post_vr.get("verifier") == "GO")
    ok("upstream.final", post_sm.get("final_decision") == POST_REVIEW_FINAL)

    ok("summary.no_paddle", summary.get("paddleocr_invoked_now") is False)
    ok("summary.no_trial", summary.get("controlled_trial_started_now") is False)
    ok("summary.no_auth", summary.get("provider_authorization_started_now") is False)

    for field in BOUNDARY_FALSE:
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
