#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Compressed OCR Authorization Roadmap Decision v1."""

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
    COMPRESSED_PATH,
    FINAL_DECISION_GO as FACTORY_DR_FINAL,
    NEXT_PHASE_GO as FACTORY_DR_NEXT,
)
from capabilities.governance.capability_factory_admission_and_operation_standard_planning_v1 import (
    MERGEABLE_OCR_AUTHORIZATION_PHASES,
    STANDARD_ID,
)
from capabilities.governance.compressed_ocr_authorization_roadmap_decision_v1 import (
    BLOCKED_ROUTE_B,
    BOUNDARY_FALSE,
    DEFERRED_ROUTE_C,
    DEFERRED_ROUTE_D,
    FACTORY_STANDARDS_REQUIRED,
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
from capabilities.governance.ocr_provider_authorization_formal_request_artifact_generation_planning_v1 import (
    FINAL_DECISION_GO as FORMAL_PLANNING_FINAL,
)
from capabilities.governance.ocr_provider_authorization_request_dryrun_v1 import (
    CURRENT_REQUEST_DRYRUN_STATE,
)
from capabilities.governance.ocr_provider_authorization_request_post_dryrun_review_v1 import (
    FINAL_DECISION_GO as REQUEST_POST_REVIEW_FINAL,
)

MIN_CHECKS = 75

REQUIRED = (
    "compressed_ocr_authorization_roadmap_policy_v1.json",
    "factory_standard_dryrun_review_input_review_v1.json",
    "compression_readiness_review_v1.json",
    "route_a_compressed_authorization_lifecycle_assessment_v1.json",
    "route_b_resume_formal_artifact_triple_chain_assessment_v1.json",
    "route_c_real_dependency_check_authorization_assessment_v1.json",
    "route_d_historical_redundancy_cleanup_assessment_v1.json",
    "compressed_ocr_authorization_route_selection_matrix_v1.json",
    "selected_route_preconditions_v1.json",
    "deferred_routes_register_v1.json",
    "compressed_authorization_execution_model_v1.json",
    "factory_standard_adoption_binding_v1.json",
    "non_claims_register_v1.json",
    "next_phase_readiness_decision_v1.json",
    "summary.json",
)


def _load(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default="/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/compressed_ocr_authorization_roadmap_decision",
    )
    p.add_argument(
        "--capability-factory-admission-and-operation-standard-dryrun-and-review-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "capability_factory_admission_and_operation_standard_dryrun_and_review"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    factory_dr_root = Path(args.capability_factory_admission_and_operation_standard_dryrun_and_review_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    summary = _load(root / "summary.json")
    input_review = _load(root / "factory_standard_dryrun_review_input_review_v1.json")
    compression_r = _load(root / "compression_readiness_review_v1.json")
    route_a = _load(root / "route_a_compressed_authorization_lifecycle_assessment_v1.json")
    route_b = _load(root / "route_b_resume_formal_artifact_triple_chain_assessment_v1.json")
    route_c = _load(root / "route_c_real_dependency_check_authorization_assessment_v1.json")
    route_d = _load(root / "route_d_historical_redundancy_cleanup_assessment_v1.json")
    matrix = _load(root / "compressed_ocr_authorization_route_selection_matrix_v1.json")
    preconditions = _load(root / "selected_route_preconditions_v1.json")
    deferred = _load(root / "deferred_routes_register_v1.json")
    exec_model = _load(root / "compressed_authorization_execution_model_v1.json")
    adoption = _load(root / "factory_standard_adoption_binding_v1.json")
    next_phase = _load(root / "next_phase_readiness_decision_v1.json")

    factory_dr_vr = _load(factory_dr_root / "verifier_report.json")
    factory_dr_sm = _load(factory_dr_root / "summary.json")
    readiness_dr = _load(factory_dr_root / "factory_standard_adoption_readiness_decision_v1.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.decision_only", summary.get("compressed_ocr_authorization_roadmap_decision_only") is True)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.route_a", summary.get("selected_route") == SELECTED_ROUTE)
    ok("summary.standard_id", summary.get("standard_id") == STANDARD_ID)

    ok("upstream.factory_dr_go", factory_dr_vr.get("verifier") == "GO")
    ok("upstream.factory_dr_final", factory_dr_sm.get("final_decision") == FACTORY_DR_FINAL)
    ok("upstream.factory_dr_next", factory_dr_sm.get("recommended_next_phase") == FACTORY_DR_NEXT)
    ok("upstream.nine", factory_dr_sm.get("nine_standards_validated") is True)
    ok("upstream.coverage", factory_dr_sm.get("ocr_chain_coverage") is True)
    ok("upstream.compression", factory_dr_sm.get("compression_validated") is True)
    ok("upstream.no_resume", readiness_dr.get("do_not_resume_formal_artifact_triple_chain") is True)
    ok("input.pass", input_review.get("review_pass") is True)

    ok("compression.pass", compression_r.get("compression_readiness_pass") is True)
    ok("compression.superseded", compression_r.get("superseded_by_factory_standard") is True)
    ok("compression.merge9", compression_r.get("mergeable_phase_count") == len(MERGEABLE_OCR_AUTHORIZATION_PHASES))

    ok("route_a.selected", route_a.get("status") == "selected")
    ok("route_a.label", route_a.get("route_label") == ROUTE_A)
    ok("route_b.blocked", route_b.get("status") == "blocked")
    ok("route_b.label", route_b.get("route_label") == ROUTE_B)
    ok("route_c.deferred", route_c.get("status") == "deferred_after_compressed_authorization_lifecycle")
    ok("route_c.label", route_c.get("route_label") == ROUTE_C)
    ok("route_d.deferred", route_d.get("status") == "deferred_next")
    ok("route_d.label", route_d.get("route_label") == ROUTE_D)

    ok("matrix.selected", matrix.get("selected_route") == SELECTED_ROUTE)
    ok("matrix.blocked_b", matrix.get("blocked_route_b") == BLOCKED_ROUTE_B)
    ok("matrix.deferred_c", matrix.get("deferred_route_c") == DEFERRED_ROUTE_C)
    ok("matrix.deferred_d", matrix.get("deferred_route_d") == DEFERRED_ROUTE_D)

    ok("precond.route", preconditions.get("selected_route") == SELECTED_ROUTE)
    ok("exec.path7", exec_model.get("step_count") == len(COMPRESSED_PATH))
    ok("exec.no_formal", exec_model.get("formal_request_artifact_generated_now") is False)
    ok("exec.no_sent", exec_model.get("request_sent_now") is False)
    ok("exec.no_grant", exec_model.get("grant_issued_now") is False)
    ok("exec.no_window", exec_model.get("execution_window_opened_now") is False)
    ok("exec.no_invoke", exec_model.get("provider_invoked_now") is False)
    ok("exec.no_real_dep", exec_model.get("real_dependency_check_executed_now") is False)

    ok("adoption.count9", adoption.get("standard_count") == len(FACTORY_STANDARDS_REQUIRED))
    ok("adoption.vf", adoption.get("validation_factory_pass_required_before_midplatform") is True)

    ok("next.ready", next_phase.get("ready_for_compressed_authorization_lifecycle_planning") is True)
    ok("next.no_resume", next_phase.get("do_not_resume_formal_artifact_triple_chain") is True)
    ok("next.no_formal", next_phase.get("do_not_generate_formal_artifact_now") is True)
    ok("next.no_send", next_phase.get("do_not_send_request_now") is True)
    ok("next.no_grant", next_phase.get("do_not_grant_authorization_now") is True)
    ok("next.no_real_dep", next_phase.get("do_not_execute_real_dependency_check_now") is True)
    ok("next.final", next_phase.get("final_decision") == FINAL_DECISION_GO)
    ok("next.phase", next_phase.get("recommended_next_phase") == NEXT_PHASE_GO)

    ok("summary.no_triple", summary.get("formal_artifact_triple_chain_resumed_now") is False)
    ok("summary.no_formal", summary.get("formal_request_artifact_generated_now") is False)
    ok("summary.no_sent", summary.get("authorization_request_sent_now") is False)
    ok("summary.no_grant", summary.get("grant_issued_now") is False)
    ok("summary.no_window", summary.get("execution_window_opened_now") is False)
    ok("summary.no_real_dep", summary.get("real_dependency_check_executed_now") is False)
    ok("summary.null_provider", summary.get("selected_provider_for_execution") is None)

    for field in BOUNDARY_FALSE:
        ok(f"boundary.{field}", summary.get(field) is False)

    ok("non_claims", len(_load(root / "non_claims_register_v1.json").get("non_claims") or []) >= len(NON_CLAIMS))
    ok("formal.planning_final", FORMAL_PLANNING_FINAL is not None)
    ok("req.post_final", REQUEST_POST_REVIEW_FINAL is not None)
    ok("lifecycle.state", CURRENT_REQUEST_DRYRUN_STATE == "request_artifact_candidate_ready")

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
