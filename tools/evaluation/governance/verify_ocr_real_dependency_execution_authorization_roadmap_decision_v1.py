#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify OCR Real Dependency Execution Authorization Roadmap Decision v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.midplatform_validation_engineering_separation_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as VALIDATION_SEP_DR_FINAL,
)
from capabilities.governance.ocr_provider_real_dependency_check_authorization_via_factory_standard_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as OCR_VIA_FACTORY_DR_FINAL,
)
from capabilities.governance.ocr_real_dependency_execution_authorization_roadmap_decision_v1 import (
    BOUNDARY_FALSE,
    DEFERRED_ROUTE_B,
    DEFERRED_ROUTE_C,
    DEFERRED_ROUTE_D,
    DEFERRED_ROUTE_E,
    FINAL_DECISION_GO,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    ROUTE_A,
    SCOPE,
    SELECTED_ROUTE,
)

MIN_CHECKS = 72

REQUIRED = (
    "ocr_real_dependency_execution_authorization_roadmap_policy_v1.json",
    "validation_engineering_separation_input_review_v1.json",
    "ocr_real_dep_via_factory_standard_input_review_v1.json",
    "execution_authorization_readiness_review_v1.json",
    "route_a_execution_authorization_planning_assessment_v1.json",
    "route_b_provider_selection_finalize_assessment_v1.json",
    "route_c_validation_runtime_activation_assessment_v1.json",
    "route_d_health_readiness_baseline_assessment_v1.json",
    "route_e_return_visual_context_governance_assessment_v1.json",
    "ocr_real_dependency_execution_authorization_route_selection_matrix_v1.json",
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
            "ocr_real_dependency_execution_authorization_roadmap_decision"
        ),
    )
    p.add_argument(
        "--midplatform-validation-engineering-separation-dryrun-and-review-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "midplatform_validation_engineering_separation_dryrun_and_review"
        ),
    )
    p.add_argument(
        "--ocr-real-dependency-authorization-via-factory-standard-dryrun-and-review-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "ocr_real_dependency_authorization_via_factory_standard_dryrun_and_review"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    val_root = Path(args.midplatform_validation_engineering_separation_dryrun_and_review_root)
    ocr_dr_root = Path(args.ocr_real_dependency_authorization_via_factory_standard_dryrun_and_review_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    val_vr = _load(val_root / "verifier_report.json")
    val_sm = _load(val_root / "summary.json")
    val_model = _load(val_root / "validation_engineering_model_candidate_v1.json")
    ocr_vr = _load(ocr_dr_root / "verifier_report.json")
    ocr_sm = _load(ocr_dr_root / "summary.json")
    ocr_cfg = _load(ocr_dr_root / "ocr_real_dependency_domain_config_candidate_v1.json")

    summary = _load(root / "summary.json")
    policy = _load(root / "ocr_real_dependency_execution_authorization_roadmap_policy_v1.json")
    val_input = _load(root / "validation_engineering_separation_input_review_v1.json")
    ocr_input = _load(root / "ocr_real_dep_via_factory_standard_input_review_v1.json")
    readiness = _load(root / "execution_authorization_readiness_review_v1.json")
    route_a = _load(root / "route_a_execution_authorization_planning_assessment_v1.json")
    route_b = _load(root / "route_b_provider_selection_finalize_assessment_v1.json")
    route_c = _load(root / "route_c_validation_runtime_activation_assessment_v1.json")
    route_d = _load(root / "route_d_health_readiness_baseline_assessment_v1.json")
    route_e = _load(root / "route_e_return_visual_context_governance_assessment_v1.json")
    matrix = _load(
        root / "ocr_real_dependency_execution_authorization_route_selection_matrix_v1.json"
    )
    next_phase = _load(root / "next_phase_readiness_decision_v1.json")
    non_claims = _load(root / "non_claims_register_v1.json")

    ok("upstream.val_dr_go", val_vr.get("verifier") == "GO")
    ok("upstream.val_dr_final", val_sm.get("final_decision") == VALIDATION_SEP_DR_FINAL)
    ok("upstream.ocr_dr_go", ocr_vr.get("verifier") == "GO")
    ok("upstream.ocr_dr_final", ocr_sm.get("final_decision") == OCR_VIA_FACTORY_DR_FINAL)
    ok("upstream.domain_config", bool(ocr_cfg.get("candidate_id")))
    ok("upstream.candidate_only", ocr_cfg.get("candidate_only") is True)
    ok("upstream.not_activated", ocr_cfg.get("activated_now") is False)
    ok("upstream.model_candidate", val_model.get("model_id") == "validation_engineering_model_v1")
    ok("upstream.runtime_false", val_model.get("runtime_enabled_now") is False)

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.decision_only", summary.get("ocr_real_dependency_execution_authorization_roadmap_decision_only") is True)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.selected", summary.get("selected_route") == SELECTED_ROUTE)
    ok("summary.defer_b", summary.get("deferred_route_b") == DEFERRED_ROUTE_B)
    ok("summary.defer_c", summary.get("deferred_route_c") == DEFERRED_ROUTE_C)
    ok("summary.defer_d", summary.get("deferred_route_d") == DEFERRED_ROUTE_D)
    ok("summary.defer_e", summary.get("deferred_route_e") == DEFERRED_ROUTE_E)
    ok("summary.provider_null", summary.get("selected_provider_for_execution") is None)

    ok("policy.scope", policy.get("scope") == SCOPE)
    ok("val_input.pass", val_input.get("review_pass") is True)
    ok("ocr_input.pass", ocr_input.get("review_pass") is True)
    ok("readiness.pass", readiness.get("readiness_pass") is True)

    ok("route_a.selected", route_a.get("status") == "selected")
    ok("route_b.deferred", route_b.get("status") == "deferred_after_real_dependency_evidence")
    ok("route_c.deferred", route_c.get("status") == "deferred")
    ok("route_d.deferred_hw", route_d.get("status") == "deferred_until_hardware_runtime_ready")
    ok("route_e.deferred", route_e.get("status") == "deferred")
    ok("matrix.selected", matrix.get("selected_route") == SELECTED_ROUTE)

    ok("next.ready_planning", next_phase.get("ready_for_execution_authorization_planning") is True)
    ok("next.no_real_dep", next_phase.get("ready_for_real_dependency_check_execution") is False)
    ok("next.no_grant", next_phase.get("do_not_grant_now") is True)
    ok("next.no_window", next_phase.get("do_not_open_execution_window_now") is True)
    ok("next.no_exec", next_phase.get("do_not_execute_real_dep_now") is True)

    for field in BOUNDARY_FALSE:
        ok(f"boundary_false.{field}", summary.get(field) is False)

    ok("non_claims.count", len(non_claims.get("non_claims") or []) >= len(NON_CLAIMS))

    passed = sum(1 for c in checks if c["passed"])
    total = len(checks)
    boundary_ok = summary.get("boundary_ok") is True
    go = passed >= MIN_CHECKS and boundary_ok and passed == total

    report = {
        "phase": PHASE_ID,
        "verifier": "GO" if go else "NO_GO",
        "checks_passed": passed,
        "checks_total": total,
        "min_checks_required": MIN_CHECKS,
        "boundary_ok": boundary_ok,
        "final_decision": summary.get("final_decision"),
        "recommended_next_phase": summary.get("recommended_next_phase"),
        "selected_route": summary.get("selected_route"),
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"verifier": report["verifier"], "checks_passed": passed, "checks_total": total}, ensure_ascii=False))
    return 0 if go else 1


if __name__ == "__main__":
    raise SystemExit(main())
