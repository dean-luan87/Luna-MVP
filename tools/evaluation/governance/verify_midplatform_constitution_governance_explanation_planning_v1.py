#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Midplatform Constitution Governance Explanation Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.midplatform_constitution_governance_explanation_planning_v1 import (
    AMENDMENT_CANDIDATE_STATES,
    AMENDMENT_TRIGGERS,
    AMENDMENT_WORKFLOW,
    BOUNDARY_FALSE,
    CONFLICT_RULES,
    CONSTITUTION_LAYERS_EXPLAINED,
    DECISION_TREE_QUESTIONS,
    FINAL_DECISION_GO,
    GENERAL_JURISDICTION,
    LAYER_PRIORITY,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    SCOPE,
    UPSTREAM_HIERARCHY_DR_FINAL,
    VIOLATION_ACTIONS,
    VIOLATION_EVIDENCE_FIELDS,
    VIOLATION_LEVELS,
    VIOLATION_TYPES,
)
from capabilities.governance.midplatform_constitution_governance_hierarchy_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as HIERARCHY_DR_FINAL,
    OCR_REAL_DEP_AUTHORIZATION_CHAIN,
)
from capabilities.governance.midplatform_constitution_governance_hierarchy_planning_v1 import (
    DOMAIN_CONSTITUTIONS,
    DOMAIN_STANDARD_CATEGORIES,
    LUNA_GENERAL_CONSTITUTION_ARTICLES,
)

MIN_CHECKS = 95

REQUIRED = (
    "constitution_governance_explanation_planning_policy_v1.json",
    "constitution_hierarchy_input_review_v1.json",
    "constitution_layer_relationship_explanation_v1.json",
    "constitution_jurisdiction_and_conflict_rule_v1.json",
    "constitution_generation_logic_v1.json",
    "constitution_amendment_logic_v1.json",
    "system_vs_personalized_constitution_rule_v1.json",
    "hive_constitution_authority_rule_v1.json",
    "local_luna_constitution_consumption_boundary_v1.json",
    "constitution_survival_mechanism_link_v1.json",
    "constitution_violation_alarm_and_penalty_rule_v1.json",
    "constitution_change_candidate_lifecycle_v1.json",
    "constitution_governance_decision_tree_v1.json",
    "constitution_explanation_non_claims_register_v1.json",
    "constitution_governance_explanation_planning_decision_v1.json",
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
    args = p.parse_args()
    root = Path(args.output_root)
    hierarchy_root = Path(args.midplatform_constitution_governance_hierarchy_dryrun_and_review_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    summary = _load(root / "summary.json")
    policy = _load(root / "constitution_governance_explanation_planning_policy_v1.json")
    hierarchy_review = _load(root / "constitution_hierarchy_input_review_v1.json")
    layers = _load(root / "constitution_layer_relationship_explanation_v1.json")
    jurisdiction = _load(root / "constitution_jurisdiction_and_conflict_rule_v1.json")
    generation = _load(root / "constitution_generation_logic_v1.json")
    amendment = _load(root / "constitution_amendment_logic_v1.json")
    sys_vs_pers = _load(root / "system_vs_personalized_constitution_rule_v1.json")
    hive = _load(root / "hive_constitution_authority_rule_v1.json")
    local = _load(root / "local_luna_constitution_consumption_boundary_v1.json")
    survival = _load(root / "constitution_survival_mechanism_link_v1.json")
    violation = _load(root / "constitution_violation_alarm_and_penalty_rule_v1.json")
    lifecycle = _load(root / "constitution_change_candidate_lifecycle_v1.json")
    tree = _load(root / "constitution_governance_decision_tree_v1.json")
    decision = _load(root / "constitution_governance_explanation_planning_decision_v1.json")
    non_claims = _load(root / "constitution_explanation_non_claims_register_v1.json")

    hierarchy_vr = _load(hierarchy_root / "verifier_report.json")
    hierarchy_sm = _load(hierarchy_root / "summary.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)

    ok("policy.scope_only", policy.get("constitution_governance_explanation_planning_only") is True)
    ok("policy.phase", policy.get("phase") == PHASE_ID)

    ok("hierarchy.vr_go", hierarchy_vr.get("verifier") == "GO")
    ok("hierarchy.final", hierarchy_sm.get("final_decision") == HIERARCHY_DR_FINAL)
    ok("hierarchy.final_match", hierarchy_sm.get("final_decision") == UPSTREAM_HIERARCHY_DR_FINAL)
    ok("hierarchy_review.pass", hierarchy_review.get("review_pass") is True)
    ok("hierarchy_review.ocr_path", hierarchy_review.get("ocr_real_dep_path") == OCR_REAL_DEP_AUTHORIZATION_CHAIN)
    ok("hierarchy_review.vf_compliance", hierarchy_review.get("validation_factory_compliance_only") is True)

    ok("layers.count5", len(layers.get("layers") or []) == len(CONSTITUTION_LAYERS_EXPLAINED))
    ok("layers.priority6", len(layers.get("layer_priority") or []) == len(LAYER_PRIORITY))
    ok("layers.general6", len(layers.get("general_constitution_articles") or []) == len(LUNA_GENERAL_CONSTITUTION_ARTICLES))
    ok("layers.domain8", len(layers.get("domain_constitutions") or []) == len(DOMAIN_CONSTITUTIONS))
    ok("layers.std10", len(layers.get("domain_standard_categories") or []) == len(DOMAIN_STANDARD_CATEGORIES))

    ok("jurisdiction.general8", len(jurisdiction.get("general_constitution_jurisdiction") or []) >= len(GENERAL_JURISDICTION))
    ok("jurisdiction.conflict8", len(jurisdiction.get("conflict_rules") or []) == len(CONFLICT_RULES))
    ok("jurisdiction.non_overridable", len(jurisdiction.get("non_overridable_floors") or []) >= 5)

    ok("generation.human_initial", generation.get("initial_constitution", {}).get("created_by") == "human designers")
    ok("generation.not_final", generation.get("initial_constitution", {}).get("not_final_form") is True)
    ok("generation.candidate_only", generation.get("future_constitution_generation", {}).get("candidate_only") is True)
    ok("generation.no_local_submit", generation.get("future_constitution_generation", {}).get("local_auto_submit_forbidden") is True)
    ok("generation.goals5", len(generation.get("generation_goals") or []) >= 5)

    ok("amendment.triggers12", len(amendment.get("amendment_triggers") or []) == len(AMENDMENT_TRIGGERS))
    ok("amendment.workflow12", len(amendment.get("amendment_workflow") or []) == len(AMENDMENT_WORKFLOW))
    ok("amendment.not_committed", amendment.get("constitution_amendment_committed_now") is False)
    ok("amendment.no_local_auto", amendment.get("local_auto_amendment_allowed") is False)
    ok("amendment.hive_required", amendment.get("hive_review_required") is True)

    ok("sys_pers.hive_managed", sys_vs_pers.get("system_constitution", {}).get("managed_by") == "Hive")
    ok("sys_pers.local_forbidden", sys_vs_pers.get("system_constitution", {}).get("local_modification_forbidden") is True)
    ok("sys_pers.overlay", "overlay" in (sys_vs_pers.get("personalized_constitution", {}).get("status") or ""))

    ok("hive.authority", hive.get("hive_constitution_authority") is True)
    ok("hive.no_local_override", hive.get("local_override_of_general_constitution_allowed") is False)
    ok("hive.review_required", hive.get("hive_review_required_for_general_constitution_change") is True)

    ok("local.may8", len(local.get("local_may") or []) >= 8)
    ok("local.may_not7", len(local.get("local_may_not") or []) >= 7)

    ok("survival.not_limit_only", "生存机制" in (survival.get("core_principle") or ""))
    ok("survival.capabilities10", len(survival.get("supported_survival_capabilities") or []) >= 10)
    ok("survival.hive_review", survival.get("all_amendments_require_hive_review") is True)

    ok("violation.levels8", len(violation.get("violation_levels") or []) == len(VIOLATION_LEVELS))
    ok("violation.types10", len(violation.get("violation_types") or []) == len(VIOLATION_TYPES))
    ok("violation.actions11", len(violation.get("actions") or []) == len(VIOLATION_ACTIONS))
    ok("violation.evidence11", len(violation.get("evidence_fields") or []) == len(VIOLATION_EVIDENCE_FIELDS))

    ok("lifecycle.states13", len(lifecycle.get("states") or []) == len(AMENDMENT_CANDIDATE_STATES))
    ok("lifecycle.not_generated", lifecycle.get("amendment_candidate_generated_now") is False)
    ok("lifecycle.not_approved", lifecycle.get("approved_now") is False)
    ok("lifecycle.not_active", lifecycle.get("active_now") is False)

    ok("tree.questions10", len(tree.get("questions") or []) == len(DECISION_TREE_QUESTIONS))
    ok("tree.flow10", len(tree.get("rule_placement_flow") or []) == 10)

    ok("decision.pass", decision.get("planning_pass") is True)
    ok("decision.final", decision.get("final_decision") == FINAL_DECISION_GO)
    ok("decision.next", decision.get("recommended_next_phase") == NEXT_PHASE_GO)

    for field in BOUNDARY_FALSE:
        ok(f"boundary.{field}", summary.get(field) is False)

    ok("policy.hive_review", policy.get("hive_review_required") is True)
    ok("policy.no_local_auto", policy.get("local_auto_amendment_allowed") is False)
    ok("summary.layers5", summary.get("layer_count") == len(CONSTITUTION_LAYERS_EXPLAINED))
    ok("summary.tree10", summary.get("decision_tree_questions") == len(DECISION_TREE_QUESTIONS))
    ok("summary.triggers12", summary.get("amendment_trigger_count") == len(AMENDMENT_TRIGGERS))
    ok("summary.violation8", summary.get("violation_level_count") == len(VIOLATION_LEVELS))
    ok("hierarchy_review.three_layer", hierarchy_review.get("three_layer_validated") is True)

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
