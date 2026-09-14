#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify OCR Authorization Next Route Decision v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.compressed_ocr_authorization_lifecycle_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as LIFECYCLE_DR_FINAL,
)
from capabilities.governance.factory_standard_historical_redundancy_cleanup_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as CLEANUP_DR_FINAL,
    NEXT_PHASE_GO as CLEANUP_DR_NEXT,
)
from capabilities.governance.ocr_authorization_next_route_decision_v1 import (
    BLOCKED_ROUTE_C,
    BOUNDARY_FALSE,
    DEFERRED_ROUTE_B,
    DEFERRED_ROUTE_D,
    FINAL_DECISION_GO,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    ROUTE_A,
    ROUTE_B,
    ROUTE_C,
    ROUTE_D,
    SCOPE,
    SELECTED_ROUTE,
)
from capabilities.governance.ocr_provider_real_dependency_check_post_dryrun_review_v1 import (
    FINAL_DECISION_GO as REAL_DEP_POST_FINAL,
)
from capabilities.governance.ocr_provider_selection_dependency_environment_post_dryrun_review_v1 import (
    FINAL_DECISION_GO as SELECTION_POST_FINAL,
)

MIN_CHECKS = 75

REQUIRED = (
    "ocr_authorization_next_route_decision_policy_v1.json",
    "cleanup_dryrun_review_input_review_v1.json",
    "compressed_lifecycle_readiness_review_v1.json",
    "ocr_provider_readiness_state_review_v1.json",
    "route_a_real_dependency_check_authorization_assessment_v1.json",
    "route_b_provider_selection_finalize_assessment_v1.json",
    "route_c_controlled_trial_authorization_assessment_v1.json",
    "route_d_return_visual_context_governance_assessment_v1.json",
    "ocr_authorization_next_route_selection_matrix_v1.json",
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
        default="/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/ocr_authorization_next_route_decision",
    )
    p.add_argument(
        "--factory-standard-historical-redundancy-cleanup-dryrun-and-review-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "factory_standard_historical_redundancy_cleanup_dryrun_and_review"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    cleanup_root = Path(args.factory_standard_historical_redundancy_cleanup_dryrun_and_review_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    summary = _load(root / "summary.json")
    cleanup_review = _load(root / "cleanup_dryrun_review_input_review_v1.json")
    lifecycle_review = _load(root / "compressed_lifecycle_readiness_review_v1.json")
    readiness = _load(root / "ocr_provider_readiness_state_review_v1.json")
    route_a = _load(root / "route_a_real_dependency_check_authorization_assessment_v1.json")
    route_b = _load(root / "route_b_provider_selection_finalize_assessment_v1.json")
    route_c = _load(root / "route_c_controlled_trial_authorization_assessment_v1.json")
    route_d = _load(root / "route_d_return_visual_context_governance_assessment_v1.json")
    matrix = _load(root / "ocr_authorization_next_route_selection_matrix_v1.json")
    preconditions = _load(root / "selected_route_preconditions_v1.json")
    deferred = _load(root / "deferred_routes_register_v1.json")
    next_phase = _load(root / "next_phase_readiness_decision_v1.json")

    cleanup_vr = _load(cleanup_root / "verifier_report.json")
    cleanup_sm = _load(cleanup_root / "summary.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.decision_only", summary.get("ocr_authorization_next_route_decision_only") is True)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.route_a", summary.get("selected_route") == SELECTED_ROUTE)

    ok("upstream.cleanup_go", cleanup_vr.get("verifier") == "GO")
    ok("upstream.cleanup_final", cleanup_sm.get("final_decision") == CLEANUP_DR_FINAL)
    ok("upstream.cleanup_next", cleanup_sm.get("recommended_next_phase") == CLEANUP_DR_NEXT)
    ok("upstream.cleanup_marking", cleanup_sm.get("marking_only") is True)
    ok("cleanup_review.pass", cleanup_review.get("review_pass") is True)

    ok("lifecycle.pass", lifecycle_review.get("readiness_pass") is True)
    ok("lifecycle.closed", lifecycle_review.get("lifecycle_closed") is True)

    ok("readiness.null_provider", readiness.get("selected_provider_for_execution") is None)
    ok("readiness.no_finalize", readiness.get("provider_selection_finalized_now") is False)
    ok("readiness.dryrun_trusted", readiness.get("real_dependency_check_dryrun_trusted") is True)
    ok("readiness.selection_trusted", readiness.get("provider_selection_candidate_trusted") is True)
    ok("readiness.missing_real_dep", readiness.get("missing_real_dependency_evidence") is True)

    ok("route_a.selected", route_a.get("status") == "selected")
    ok("route_a.label", route_a.get("route_label") == ROUTE_A)
    ok("route_b.deferred", route_b.get("status") == "deferred_after_real_dependency_check_evidence")
    ok("route_b.label", route_b.get("route_label") == ROUTE_B)
    ok("route_c.blocked", route_c.get("status") == "blocked_until_provider_selection_and_real_dependency")
    ok("route_c.label", route_c.get("route_label") == ROUTE_C)
    ok("route_d.deferred", route_d.get("status") == "deferred")
    ok("route_d.label", route_d.get("route_label") == ROUTE_D)

    ok("matrix.selected", matrix.get("selected_route") == SELECTED_ROUTE)
    ok("matrix.deferred_b", matrix.get("deferred_route_b") == DEFERRED_ROUTE_B)
    ok("matrix.blocked_c", matrix.get("blocked_route_c") == BLOCKED_ROUTE_C)
    ok("matrix.deferred_d", matrix.get("deferred_route_d") == DEFERRED_ROUTE_D)

    ok("precond.route", preconditions.get("selected_route") == SELECTED_ROUTE)
    ok("next.ready", next_phase.get("ready_for_real_dependency_check_authorization_planning") is True)
    ok("next.no_real_dep", next_phase.get("do_not_execute_real_dependency_check_now") is True)
    ok("next.no_finalize", next_phase.get("do_not_finalize_provider_now") is True)
    ok("next.no_trial", next_phase.get("do_not_start_controlled_trial_now") is True)
    ok("next.final", next_phase.get("final_decision") == FINAL_DECISION_GO)
    ok("next.phase", next_phase.get("recommended_next_phase") == NEXT_PHASE_GO)

    ok("summary.null_provider", summary.get("selected_provider_for_execution") is None)
    ok("summary.no_finalize", summary.get("provider_selection_finalized_now") is False)
    ok("summary.no_real_dep", summary.get("real_dependency_check_executed_now") is False)
    ok("summary.no_import", summary.get("provider_imported_now") is False)
    ok("summary.no_invoke", summary.get("provider_invoked_now") is False)

    for field in BOUNDARY_FALSE:
        ok(f"boundary.{field}", summary.get(field) is False)

    ok("non_claims", len(_load(root / "non_claims_register_v1.json").get("non_claims") or []) >= len(NON_CLAIMS))
    ok("real_dep.post_final", REAL_DEP_POST_FINAL is not None)
    ok("selection.post_final", SELECTION_POST_FINAL is not None)
    ok("lifecycle.dr_final", LIFECYCLE_DR_FINAL is not None)

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
