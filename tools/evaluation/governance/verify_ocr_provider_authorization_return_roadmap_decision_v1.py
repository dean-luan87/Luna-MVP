#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify OCR Provider Authorization Return Roadmap Decision v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.controlled_provider_readiness_harness_factory_registration_dryrun_v1 import (
    NEW_FACTORY_MODULE_ID,
)
from capabilities.governance.controlled_provider_readiness_harness_factory_registration_planning_v1 import (
    EXISTING_FACTORY_MODULE_COUNT,
    FUTURE_CONSUMER_DOMAINS,
)
from capabilities.governance.controlled_provider_readiness_harness_factory_registration_post_dryrun_review_v1 import (
    FINAL_DECISION_GO as FACTORY_POST_FINAL,
    NEXT_PHASE_GO as FACTORY_POST_NEXT,
)
from capabilities.governance.ocr_provider_authorization_return_roadmap_decision_v1 import (
    BOUNDARY_FALSE,
    DEFERRED_ROUTE_B,
    DEFERRED_ROUTE_C,
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

MIN_CHECKS = 65

REQUIRED = (
    "ocr_authorization_return_roadmap_policy_v1.json",
    "factory_registration_post_review_input_review_v1.json",
    "ocr_provider_chain_readiness_review_v1.json",
    "route_a_ocr_provider_authorization_planning_assessment_v1.json",
    "route_b_real_dependency_check_authorization_assessment_v1.json",
    "route_c_provider_selection_finalize_assessment_v1.json",
    "route_d_return_to_visual_context_governance_assessment_v1.json",
    "ocr_authorization_return_route_selection_matrix_v1.json",
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
            "ocr_provider_authorization_return_roadmap_decision"
        ),
    )
    p.add_argument(
        "--controlled-provider-readiness-harness-factory-registration-post-dryrun-review-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "controlled_provider_readiness_harness_factory_registration_post_dryrun_review"
        ),
    )
    p.add_argument(
        "--controlled-provider-readiness-harness-factory-registration-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "controlled_provider_readiness_harness_factory_registration_dryrun"
        ),
    )
    p.add_argument(
        "--ocr-provider-real-dependency-check-post-dryrun-review-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "ocr_provider_real_dependency_check_post_dryrun_review"
        ),
    )
    p.add_argument(
        "--ocr-provider-selection-dependency-environment-post-dryrun-review-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "ocr_provider_selection_dependency_environment_post_dryrun_review"
        ),
    )
    p.add_argument(
        "--ocr-controlled-provider-post-dryrun-review-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/ocr_controlled_provider_post_dryrun_review"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    factory_post_root = Path(
        args.controlled_provider_readiness_harness_factory_registration_post_dryrun_review_root
    )
    dryrun_root = Path(args.controlled_provider_readiness_harness_factory_registration_dryrun_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    summary = _load(root / "summary.json")
    input_review = _load(root / "factory_registration_post_review_input_review_v1.json")
    chain = _load(root / "ocr_provider_chain_readiness_review_v1.json")
    route_a = _load(root / "route_a_ocr_provider_authorization_planning_assessment_v1.json")
    route_b = _load(root / "route_b_real_dependency_check_authorization_assessment_v1.json")
    route_c = _load(root / "route_c_provider_selection_finalize_assessment_v1.json")
    route_d = _load(root / "route_d_return_to_visual_context_governance_assessment_v1.json")
    matrix = _load(root / "ocr_authorization_return_route_selection_matrix_v1.json")
    next_phase = _load(root / "next_phase_readiness_decision_v1.json")

    factory_post_vr = _load(factory_post_root / "verifier_report.json")
    factory_post_sm = _load(factory_post_root / "summary.json")
    dryrun_sm = _load(dryrun_root / "summary.json")
    real_post_vr = _load(Path(args.ocr_provider_real_dependency_check_post_dryrun_review_root) / "verifier_report.json")
    sel_post_vr = _load(
        Path(args.ocr_provider_selection_dependency_environment_post_dryrun_review_root) / "verifier_report.json"
    )
    ocr_post_vr = _load(Path(args.ocr_controlled_provider_post_dryrun_review_root) / "verifier_report.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.decision_only", summary.get("ocr_provider_authorization_return_roadmap_decision_only") is True)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.selected", summary.get("selected_route") == SELECTED_ROUTE)
    ok("summary.null_provider", summary.get("selected_provider_for_execution") is None)

    ok("upstream.factory_post_go", factory_post_vr.get("verifier") == "GO")
    ok("upstream.factory_post_final", factory_post_sm.get("final_decision") == FACTORY_POST_FINAL)
    ok("upstream.factory_post_next", factory_post_sm.get("recommended_next_phase") == FACTORY_POST_NEXT)
    ok("upstream.candidate_gen", dryrun_sm.get("validation_factory_registry_candidate_generated_now") is True)
    ok("upstream.not_updated", dryrun_sm.get("validation_factory_registry_updated_now") is False)

    ok("upstream.real_go", real_post_vr.get("verifier") == "GO")
    ok("upstream.sel_go", sel_post_vr.get("verifier") == "GO")
    ok("upstream.ocr_go", ocr_post_vr.get("verifier") == "GO")

    ok("input.pass", input_review.get("review_pass") is True)
    ok("input.modules7", input_review.get("registry_candidate_module_count") == EXISTING_FACTORY_MODULE_COUNT + 1)
    ok("input.seventh", input_review.get("seventh_module_id") == NEW_FACTORY_MODULE_ID)

    ok("chain.pass", chain.get("chain_readiness_pass") is True)
    ok("chain.ocr_validated", chain.get("ocr_first_consumer_validated") is True)
    ok("chain.vision_voice", chain.get("vision_voice_validated") is True)
    ok("chain.null_provider", chain.get("selected_provider_for_execution") is None)

    ok("route_a.selected", route_a.get("status") == "selected")
    ok("route_b.deferred", route_b.get("status") == "deferred_after_authorization_planning")
    ok("route_c.deferred", route_c.get("status") == "deferred")
    ok("route_d.deferred", route_d.get("status") == "deferred")

    ok("matrix.selected", matrix.get("selected_route") == SELECTED_ROUTE)
    ok("matrix.defer_b", matrix.get("deferred_route_b") == DEFERRED_ROUTE_B)
    ok("matrix.defer_c", matrix.get("deferred_route_c") == DEFERRED_ROUTE_C)
    ok("matrix.defer_d", matrix.get("deferred_route_d") == DEFERRED_ROUTE_D)

    ok("next.ready", next_phase.get("ready_for_ocr_provider_authorization_planning") is True)
    ok("next.no_grant", next_phase.get("do_not_grant_authorization_now") is True)
    ok("next.no_real_dep", next_phase.get("do_not_execute_real_dependency_check_now") is True)
    ok("next.no_finalize", next_phase.get("do_not_finalize_provider_selection_now") is True)
    ok("next.no_import", next_phase.get("do_not_import_install_invoke_now") is True)

    ok("route_a.label", route_a.get("route_label") == ROUTE_A)
    ok("route_b.label", route_b.get("route_label") == ROUTE_B)
    ok("route_c.label", route_c.get("route_label") == ROUTE_C)
    ok("route_d.label", route_d.get("route_label") == ROUTE_D)

    ok("summary.no_auth_plan", summary.get("ocr_authorization_planning_started_now") is False)
    ok("summary.no_grant", summary.get("provider_authorization_granted_now") is False)
    ok("summary.no_finalize", summary.get("provider_selection_finalized_now") is False)

    for domain in FUTURE_CONSUMER_DOMAINS:
        ok(f"future.{domain}", domain in FUTURE_CONSUMER_DOMAINS)

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
