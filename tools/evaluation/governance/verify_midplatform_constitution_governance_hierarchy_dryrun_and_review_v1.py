#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Midplatform Constitution Governance Hierarchy DryRunAndReview v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.capability_factory_admission_and_operation_standard_planning_v1 import (
    STANDARD_ID as FACTORY_STANDARD_ID,
)
from capabilities.governance.capability_factory_authorization_standard_extension_planning_v1 import (
    AUTHORIZATION_STANDARD_ID,
    AUTHORIZATION_SUBCOMPONENTS,
    NINE_STANDARDS,
)
from capabilities.governance.midplatform_constitution_governance_hierarchy_dryrun_and_review_v1 import (
    BLOCKED_PATHS,
    BOUNDARY_FALSE,
    DOMAIN_CONSTITUTIONS,
    DOMAIN_STANDARD_CATEGORIES,
    FINAL_DECISION_GO,
    GENERAL_CONSTITUTION_ARTICLES,
    HIERARCHY_ANALOGY,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    OCR_DOMAIN_STANDARDS,
    OCR_REAL_DEP_AUTHORIZATION_CHAIN,
    PHASE_ID,
    RULE_CLASSIFICATION_QUESTIONS,
    SCOPE,
    UPSTREAM_HIERARCHY_PLANNING_FINAL,
)
from capabilities.governance.midplatform_constitution_governance_hierarchy_planning_v1 import (
    FINAL_DECISION_GO as HIERARCHY_PLANNING_FINAL,
)

MIN_CHECKS = 120

REQUIRED = (
    "midplatform_constitution_hierarchy_dryrun_and_review_policy_v1.json",
    "constitution_hierarchy_planning_input_review_v1.json",
    "general_constitution_dryrun_review_v1.json",
    "domain_constitution_dryrun_review_v1.json",
    "domain_standard_dryrun_review_v1.json",
    "factory_standard_constitution_mapping_review_v1.json",
    "factory_authorization_standard_mapping_review_v1.json",
    "controlled_provider_harness_mapping_review_v1.json",
    "validation_factory_role_mapping_review_v1.json",
    "ocr_constitution_and_standard_mapping_review_v1.json",
    "vision_voice_future_constitution_mapping_review_v1.json",
    "rule_placement_decision_tree_dryrun_result_v1.json",
    "ocr_real_dep_authorization_governance_path_review_v1.json",
    "constitution_hierarchy_boundary_audit_v1.json",
    "constitution_hierarchy_blocked_path_result_v1.json",
    "constitution_hierarchy_closure_decision_v1.json",
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
            "midplatform_constitution_governance_hierarchy_dryrun_and_review"
        ),
    )
    p.add_argument(
        "--midplatform-constitution-governance-hierarchy-planning-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "midplatform_constitution_governance_hierarchy_planning"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    plan_root = Path(args.midplatform_constitution_governance_hierarchy_planning_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    summary = _load(root / "summary.json")
    policy = _load(root / "midplatform_constitution_hierarchy_dryrun_and_review_policy_v1.json")
    planning_review = _load(root / "constitution_hierarchy_planning_input_review_v1.json")
    general = _load(root / "general_constitution_dryrun_review_v1.json")
    domain = _load(root / "domain_constitution_dryrun_review_v1.json")
    domain_std = _load(root / "domain_standard_dryrun_review_v1.json")
    factory_map = _load(root / "factory_standard_constitution_mapping_review_v1.json")
    auth_map = _load(root / "factory_authorization_standard_mapping_review_v1.json")
    harness_map = _load(root / "controlled_provider_harness_mapping_review_v1.json")
    vf_map = _load(root / "validation_factory_role_mapping_review_v1.json")
    ocr_map = _load(root / "ocr_constitution_and_standard_mapping_review_v1.json")
    vv_map = _load(root / "vision_voice_future_constitution_mapping_review_v1.json")
    tree = _load(root / "rule_placement_decision_tree_dryrun_result_v1.json")
    ocr_path = _load(root / "ocr_real_dep_authorization_governance_path_review_v1.json")
    boundary = _load(root / "constitution_hierarchy_boundary_audit_v1.json")
    blocked = _load(root / "constitution_hierarchy_blocked_path_result_v1.json")
    closure = _load(root / "constitution_hierarchy_closure_decision_v1.json")
    next_route = _load(root / "next_route_readiness_decision_v1.json")
    non_claims = _load(root / "non_claims_register_v1.json")

    plan_vr = _load(plan_root / "verifier_report.json")
    plan_sm = _load(plan_root / "summary.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.pass", summary.get("dryrun_and_review_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.simulated", summary.get("simulated") is True)

    ok("policy.scope_only", policy.get("midplatform_constitution_governance_hierarchy_dryrun_and_review_only") is True)
    ok("policy.phase", policy.get("phase") == PHASE_ID)

    ok("planning.vr_go", plan_vr.get("verifier") == "GO")
    ok("planning.final", plan_sm.get("final_decision") == HIERARCHY_PLANNING_FINAL)
    ok("planning.final_match", plan_sm.get("final_decision") == UPSTREAM_HIERARCHY_PLANNING_FINAL)
    ok("planning_review.pass", planning_review.get("review_pass") is True)

    ok("general.pass", general.get("dryrun_and_review_pass") is True)
    ok("general.articles6", general.get("article_count") == len(GENERAL_CONSTITUTION_ARTICLES))
    ok("general.overlays", general.get("overlays_all_domains") is True)
    ok("general.no_domain_override", general.get("cannot_be_overridden_by_domain_standard") is True)
    ok("general.no_provider_override", general.get("cannot_be_overridden_by_provider") is True)
    ok("general.no_user_task_override", general.get("cannot_be_overridden_by_user_task") is True)
    for article_id, _ in GENERAL_CONSTITUTION_ARTICLES:
        ok(f"general.{article_id}", any(a.get("article_id") == article_id for a in (general.get("articles") or [])))

    ok("domain.pass", domain.get("dryrun_and_review_pass") is True)
    ok("domain.count8", domain.get("domain_count") == len(DOMAIN_CONSTITUTIONS))
    ok("domain.ocr_active", domain.get("ocr_constitution_active_for_mapping") is True)
    ok("domain.vision_planned", domain.get("vision_constitution_planned") is True)
    ok("domain.voice_planned", domain.get("voice_constitution_planned") is True)
    ok("domain.future_only", domain.get("map_library_hive_memory_future_only") is True)

    ok("domain_std.pass", domain_std.get("dryrun_and_review_pass") is True)
    ok("domain_std.count10", domain_std.get("category_count") == len(DOMAIN_STANDARD_CATEGORIES))

    ok("factory.pass", factory_map.get("dryrun_and_review_pass") is True)
    ok("factory.root", factory_map.get("factory_standard_id") == FACTORY_STANDARD_ID)
    ok("factory.not_isolated", factory_map.get("not_isolated_outside_constitution") is True)
    ok("factory.categories9", len(factory_map.get("category_mappings") or []) == len(NINE_STANDARDS))

    ok("auth.pass", auth_map.get("dryrun_and_review_pass") is True)
    ok("auth.std", auth_map.get("authorization_standard_id") == AUTHORIZATION_STANDARD_ID)
    ok("auth.distinct", auth_map.get("approval_grant_distinct_from_authorization") is True)
    ok("auth.ocr_domain_config", auth_map.get("ocr_domain_config_only") is True)
    ok("auth.subs8", len(auth_map.get("subcomponent_mappings") or []) == len(AUTHORIZATION_SUBCOMPONENTS))

    ok("harness.pass", harness_map.get("dryrun_and_review_pass") is True)
    ok("harness.no_constitution", harness_map.get("writes_constitution") is False)
    ok("harness.consumers7", len(harness_map.get("consumers") or []) == 7)

    ok("vf.pass", vf_map.get("dryrun_and_review_pass") is True)
    ok("vf.no_rules", vf_map.get("writes_constitution_rules") is False)
    ok("vf.before_midplatform", vf_map.get("pass_required_before_midplatform_consumption") is True)

    ok("ocr.pass", ocr_map.get("dryrun_and_review_pass") is True)
    ok("ocr.standards8", ocr_map.get("standard_count") == len(OCR_DOMAIN_STANDARDS))

    ok("vv.pass", vv_map.get("dryrun_and_review_pass") is True)
    ok("vv.planned", vv_map.get("status") == "planned_not_instantiated")

    ok("tree.pass", tree.get("dryrun_and_review_pass") is True)
    ok("tree.questions4", len(tree.get("questions") or []) == len(RULE_CLASSIFICATION_QUESTIONS))

    ok("ocr_path.pass", ocr_path.get("dryrun_and_review_pass") is True)
    ok("ocr_path.chain", ocr_path.get("authorization_chain") == OCR_REAL_DEP_AUTHORIZATION_CHAIN)
    ok("ocr_path.domain_config", ocr_path.get("using_ocr_domain_config_only") is True)
    ok("ocr_path.no_repeat", ocr_path.get("no_repeated_request_grant_window_rules_in_ocr_phase") is True)

    ok("boundary.pass", boundary.get("dryrun_and_review_pass") is True)
    ok("boundary.all_false", boundary.get("all_boundary_false") is True)
    for field in BOUNDARY_FALSE:
        ok(f"boundary.{field}", summary.get(field) is False)

    ok("blocked.all", blocked.get("all_blocked") is True)
    ok("blocked.count13", blocked.get("blocked_count") == len(BLOCKED_PATHS))
    for bp in BLOCKED_PATHS:
        ok(f"blocked.{bp}", any(
            b.get("blocked_path") == bp and b.get("blocked") is True
            for b in (blocked.get("blocked_paths") or [])
        ))

    ok("closure.pass", closure.get("dryrun_and_review_pass") is True)
    ok("closure.final", closure.get("final_decision") == FINAL_DECISION_GO)
    ok("closure.next", closure.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("closure.no_high_risk", closure.get("high_risk") is False)

    ok("next_route.auth_ext", next_route.get("ready_for_auth_extension_dryrun_review") is True)
    ok("next_route.no_ocr_real_dep", next_route.get("ready_for_ocr_real_dep_authorization") is False)
    ok("next_route.next", next_route.get("recommended_next_phase") == NEXT_PHASE_GO)

    ok("non_claims.count", len(non_claims.get("non_claims") or []) >= len(NON_CLAIMS))
    ok("analogy", summary.get("hierarchy_analogy") == HIERARCHY_ANALOGY)

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
