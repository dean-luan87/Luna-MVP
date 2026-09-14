#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Midplatform Constitution Governance Explanation DryRunAndReview v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.capability_factory_authorization_standard_extension_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as AUTH_EXT_DR_FINAL,
)
from capabilities.governance.midplatform_constitution_governance_explanation_dryrun_and_review_v1 import (
    AMENDMENT_CANDIDATE_STATES,
    AMENDMENT_TRIGGERS,
    AMENDMENT_WORKFLOW,
    BLOCKED_PATHS,
    BOUNDARY_FALSE,
    DECISION_TREE_QUESTIONS,
    FINAL_DECISION_GO,
    LAYER_PRIORITY,
    LOCAL_LUNA_MAY,
    LOCAL_LUNA_MAY_NOT,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    SCOPE,
    UPSTREAM_AUTH_EXT_DR_FINAL,
    UPSTREAM_EXPLANATION_PLANNING_FINAL,
    UPSTREAM_HIERARCHY_DR_FINAL,
    VIOLATION_ACTIONS,
    VIOLATION_EVIDENCE_FIELDS,
    VIOLATION_LEVELS,
    VIOLATION_TYPES,
)
from capabilities.governance.midplatform_constitution_governance_explanation_planning_v1 import (
    FINAL_DECISION_GO as EXPLAIN_PLANNING_FINAL,
)
from capabilities.governance.midplatform_constitution_governance_hierarchy_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as HIERARCHY_DR_FINAL,
)

MIN_CHECKS = 120

REQUIRED = (
    "constitution_governance_explanation_dryrun_and_review_policy_v1.json",
    "constitution_explanation_planning_input_review_v1.json",
    "constitution_layer_relationship_review_v1.json",
    "constitution_jurisdiction_conflict_review_v1.json",
    "constitution_generation_logic_review_v1.json",
    "constitution_amendment_logic_review_v1.json",
    "system_vs_personalized_constitution_review_v1.json",
    "hive_constitution_authority_review_v1.json",
    "local_luna_constitution_consumption_boundary_review_v1.json",
    "constitution_survival_mechanism_link_review_v1.json",
    "constitution_violation_alarm_penalty_review_v1.json",
    "constitution_change_candidate_lifecycle_review_v1.json",
    "constitution_governance_decision_tree_review_v1.json",
    "constitution_explanation_boundary_audit_v1.json",
    "constitution_explanation_blocked_path_result_v1.json",
    "constitution_explanation_closure_decision_v1.json",
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
            "midplatform_constitution_governance_explanation_dryrun_and_review"
        ),
    )
    p.add_argument(
        "--midplatform-constitution-governance-explanation-planning-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "midplatform_constitution_governance_explanation_planning"
        ),
    )
    p.add_argument(
        "--midplatform-constitution-governance-hierarchy-dryrun-and-review-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "midplatform_constitution_governance_hierarchy_dryrun_and_review"
        ),
    )
    p.add_argument(
        "--capability-factory-authorization-standard-extension-dryrun-and-review-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "capability_factory_authorization_standard_extension_dryrun_and_review"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    explain_root = Path(args.midplatform_constitution_governance_explanation_planning_root)
    hierarchy_root = Path(args.midplatform_constitution_governance_hierarchy_dryrun_and_review_root)
    auth_ext_root = Path(args.capability_factory_authorization_standard_extension_dryrun_and_review_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    summary = _load(root / "summary.json")
    policy = _load(root / "constitution_governance_explanation_dryrun_and_review_policy_v1.json")
    planning_review = _load(root / "constitution_explanation_planning_input_review_v1.json")
    layers = _load(root / "constitution_layer_relationship_review_v1.json")
    jurisdiction = _load(root / "constitution_jurisdiction_conflict_review_v1.json")
    generation = _load(root / "constitution_generation_logic_review_v1.json")
    amendment = _load(root / "constitution_amendment_logic_review_v1.json")
    sys_pers = _load(root / "system_vs_personalized_constitution_review_v1.json")
    hive = _load(root / "hive_constitution_authority_review_v1.json")
    local = _load(root / "local_luna_constitution_consumption_boundary_review_v1.json")
    survival = _load(root / "constitution_survival_mechanism_link_review_v1.json")
    violation = _load(root / "constitution_violation_alarm_penalty_review_v1.json")
    lifecycle = _load(root / "constitution_change_candidate_lifecycle_review_v1.json")
    tree = _load(root / "constitution_governance_decision_tree_review_v1.json")
    boundary = _load(root / "constitution_explanation_boundary_audit_v1.json")
    blocked = _load(root / "constitution_explanation_blocked_path_result_v1.json")
    closure = _load(root / "constitution_explanation_closure_decision_v1.json")
    next_route = _load(root / "next_route_readiness_decision_v1.json")
    non_claims = _load(root / "non_claims_register_v1.json")

    explain_vr = _load(explain_root / "verifier_report.json")
    explain_sm = _load(explain_root / "summary.json")
    hierarchy_vr = _load(hierarchy_root / "verifier_report.json")
    hierarchy_sm = _load(hierarchy_root / "summary.json")
    auth_ext_vr = _load(auth_ext_root / "verifier_report.json")
    auth_ext_sm = _load(auth_ext_root / "summary.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.pass", summary.get("dryrun_and_review_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.simulated", summary.get("simulated") is True)

    ok("policy.scope_only", policy.get("constitution_governance_explanation_dryrun_and_review_only") is True)

    ok("explain.vr_go", explain_vr.get("verifier") == "GO")
    ok("explain.final", explain_sm.get("final_decision") == EXPLAIN_PLANNING_FINAL)
    ok("explain.final_match", explain_sm.get("final_decision") == UPSTREAM_EXPLANATION_PLANNING_FINAL)
    ok("hierarchy.vr_go", hierarchy_vr.get("verifier") == "GO")
    ok("hierarchy.final", hierarchy_sm.get("final_decision") == HIERARCHY_DR_FINAL)
    ok("hierarchy.final_match", hierarchy_sm.get("final_decision") == UPSTREAM_HIERARCHY_DR_FINAL)
    ok("auth_ext.vr_go", auth_ext_vr.get("verifier") == "GO")
    ok("auth_ext.final", auth_ext_sm.get("final_decision") == AUTH_EXT_DR_FINAL)
    ok("auth_ext.final_match", auth_ext_sm.get("final_decision") == UPSTREAM_AUTH_EXT_DR_FINAL)
    ok("planning_review.pass", planning_review.get("review_pass") is True)
    ok("planning_review.three_layer", planning_review.get("three_layer_closed") is True)

    ok("layers.pass", layers.get("dryrun_and_review_pass") is True)
    ok("layers.general_highest", layers.get("general_constitution_highest") is True)
    ok("layers.personalized_overlay", layers.get("personalized_constitution_overlay_only") is True)
    ok("layers.phase_no_override", layers.get("phase_local_rule_cannot_override_upper") is True)
    ok("layers.priority6", len(layers.get("layer_priority") or []) == len(LAYER_PRIORITY))

    ok("jurisdiction.pass", jurisdiction.get("dryrun_and_review_pass") is True)
    ok("jurisdiction.upper_priority", jurisdiction.get("upper_rule_priority") is True)
    ok("jurisdiction.conflict8", jurisdiction.get("conflict_rules_count") == 8)

    ok("generation.pass", generation.get("dryrun_and_review_pass") is True)
    ok("generation.human", generation.get("initial_constitution_by_human") is True)
    ok("generation.candidate_only", generation.get("constitution_candidate_only") is True)
    ok("generation.no_local_submit", generation.get("local_auto_submit_forbidden") is True)

    ok("amendment.pass", amendment.get("dryrun_and_review_pass") is True)
    ok("amendment.triggers12", len(amendment.get("amendment_triggers") or []) == len(AMENDMENT_TRIGGERS))
    ok("amendment.workflow12", len(amendment.get("amendment_workflow") or []) == len(AMENDMENT_WORKFLOW))
    ok("amendment.not_committed", amendment.get("constitution_amendment_committed_now") is False)
    ok("amendment.hive_required", amendment.get("hive_review_required") is True)

    ok("sys_pers.pass", sys_pers.get("dryrun_and_review_pass") is True)
    ok("sys_pers.hive", sys_pers.get("system_constitution_hive_managed") is True)
    ok("sys_pers.overlay", sys_pers.get("personalized_overlay_only") is True)
    ok("sys_pers.not_generated", sys_pers.get("personalized_constitution_generated_now") is False)

    ok("hive.pass", hive.get("dryrun_and_review_pass") is True)
    ok("hive.highest", hive.get("hive_is_highest_management_end") is True)
    ok("hive.no_override", hive.get("local_override_of_general_constitution_allowed") is False)

    ok("local.pass", local.get("dryrun_and_review_pass") is True)
    ok("local.may9", len(local.get("local_may") or []) == len(LOCAL_LUNA_MAY))
    ok("local.may_not7", len(local.get("local_may_not") or []) == len(LOCAL_LUNA_MAY_NOT))

    ok("survival.pass", survival.get("dryrun_and_review_pass") is True)
    ok("survival.mechanism", survival.get("constitution_is_survival_mechanism") is True)
    ok("survival.hive_review", survival.get("all_amendments_require_hive_review") is True)

    ok("violation.pass", violation.get("dryrun_and_review_pass") is True)
    ok("violation.levels8", len(violation.get("violation_levels") or []) == len(VIOLATION_LEVELS))
    ok("violation.types10", len(violation.get("violation_types") or []) == len(VIOLATION_TYPES))
    ok("violation.actions11", len(violation.get("actions") or []) == len(VIOLATION_ACTIONS))
    ok("violation.evidence11", len(violation.get("evidence_fields") or []) == len(VIOLATION_EVIDENCE_FIELDS))
    ok("violation.not_executed", violation.get("violation_penalty_executed_now") is False)

    ok("lifecycle.pass", lifecycle.get("dryrun_and_review_pass") is True)
    ok("lifecycle.states13", len(lifecycle.get("states") or []) == len(AMENDMENT_CANDIDATE_STATES))
    ok("lifecycle.not_generated", lifecycle.get("amendment_candidate_generated_now") is False)
    ok("lifecycle.not_approved", lifecycle.get("approved_now") is False)

    ok("tree.pass", tree.get("dryrun_and_review_pass") is True)
    ok("tree.questions10", tree.get("question_count") == len(DECISION_TREE_QUESTIONS))

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
    ok("closure.consumable", closure.get("governance_explanation_consumable") is True)

    ok("next_route.ocr_planning", next_route.get("ready_for_ocr_real_dep_via_factory_standard_planning") is True)
    ok("next_route.no_real_dep", next_route.get("ready_for_real_dependency_check") is False)
    ok("next_route.domain_config", next_route.get("ocr_consumes_domain_config_only") is True)
    ok("next_route.next", next_route.get("recommended_next_phase") == NEXT_PHASE_GO)

    ok("non_claims", len(non_claims.get("non_claims") or []) >= len(NON_CLAIMS))

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
