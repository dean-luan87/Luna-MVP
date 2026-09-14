"""Fail-closed verifier for the full E2E cognitive-logic regression."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict


PHASE = "Phase-P1-Luna-Full-End-To-End-Cognitive-Logic-Conformance-Regression-v1-001"
REQUIRED_ASSERTIONS = {
    "role_changes_attention",
    "role_changes_relation_interpretation",
    "role_changes_evidence_relevance",
    "task_changes_information_need",
    "task_changes_sufficiency_threshold",
    "task_changes_stop_condition",
    "role_task_change_can_change_hypothesis",
    "role_task_change_can_change_current_world_candidate",
    "role_task_change_can_change_decision_candidate",
    "physical_field_not_mutated_by_role_change",
    "physical_field_not_mutated_by_task_change",
    "same_evidence_can_have_different_relevance",
    "irrelevant_change_does_not_change_field_cognition",
    "evidence_not_promoted_to_fact",
    "hypothesis_not_promoted_to_truth",
    "current_world_candidate_not_promoted_to_world_truth",
    "conflicting_evidence_preserved",
    "missing_information_produces_gap",
    "material_new_evidence_can_trigger_revision",
    "sufficient_information_produces_stop",
    "no_premature_stop",
    "no_post_sufficiency_over_observation",
}


def _check(check_id: str, passed: bool, observed: Any = None) -> Dict[str, Any]:
    return {"check_id": check_id, "passed": bool(passed), "observed": observed}


def _find(results: list[Dict[str, Any]], contrast_id: str) -> Dict[str, Any]:
    return next((item for item in results if item.get("contrast_id") == contrast_id), {})


def _pair(summary: Dict[str, Any], left: str, right: str) -> Dict[str, Any]:
    return next(
        (item for item in summary.get("contrast_case_results") or ()
         if item.get("left") == left and item.get("right") == right),
        {},
    )


def _cognitive_checks(summary: Dict[str, Any]) -> list[Dict[str, Any]]:
    results = summary.get("contrast_results") or []
    role = _pair(summary, "role-owner", "role-visitor")
    task = _pair(summary, "task-document", "task-exit")
    both = _pair(summary, "role-task-owner", "role-task-visitor")
    goal = _pair(summary, "goal-locate", "goal-operational-state")
    irrelevant = _pair(summary, "task-document", "irrelevant-clutter")
    owner = _find(results, "role-owner")
    visitor = _find(results, "role-visitor")
    document = _find(results, "task-document")
    exit_case = _find(results, "task-exit")
    locate = _find(results, "goal-locate")
    operational = _find(results, "goal-operational-state")
    missing = _find(results, "missing-evidence")
    conflict = _find(results, "conflicting-evidence")
    task_changed = bool(task.get("changed_semantic_fields"))
    goal_sufficiency_changed = locate.get("semantic_snapshot", {}).get("sufficiency_status") != operational.get("semantic_snapshot", {}).get("sufficiency_status")
    goal_relevance_changed = "attention_relevance_score_candidate" in goal.get("changed_semantic_fields", []) or "attention_priority_candidate" in goal.get("changed_semantic_fields", [])
    checks = [
        _check("role_changes_attention", "attention_priority_candidate" in role.get("changed_semantic_fields", []) or "selected_attention_count" in role.get("changed_semantic_fields", []), role),
        _check("role_changes_relation_interpretation", "relation_interpretation_candidates" in role.get("changed_semantic_fields", []), role),
        _check("role_changes_evidence_relevance", "conditioned_evidence_relevance" in role.get("changed_semantic_fields", []), role),
        _check("task_changes_information_need", task_changed, task),
        _check("task_changes_sufficiency_threshold", "sufficiency_status" in task.get("changed_semantic_fields", []), task),
        _check("task_changes_stop_condition", "stop_present" in task.get("changed_semantic_fields", []), task),
        _check("role_task_change_can_change_hypothesis", "hypothesis_state" in both.get("changed_semantic_fields", []) or "hypothesis_statement_candidate" in both.get("changed_semantic_fields", []), both),
        _check("role_task_change_can_change_current_world_candidate", "current_world_kind_candidate" in both.get("changed_semantic_fields", []), both),
        _check("role_task_change_can_change_decision_candidate", "decision_candidate_semantic_projection" in both.get("changed_semantic_fields", []), both),
        _check("physical_field_not_mutated_by_role_change", owner.get("input_semantics", {}).get("field_refs") == visitor.get("input_semantics", {}).get("field_refs") and owner.get("field_output_refs") == visitor.get("field_output_refs"), {"left": owner.get("field_output_refs"), "right": visitor.get("field_output_refs")}),
        _check("physical_field_not_mutated_by_task_change", document.get("input_semantics", {}).get("field_refs") == exit_case.get("input_semantics", {}).get("field_refs") and document.get("field_output_refs") == exit_case.get("field_output_refs"), {"left": document.get("field_output_refs"), "right": exit_case.get("field_output_refs")}),
        _check("same_evidence_can_have_different_relevance", goal.get("same_evidence") is True and goal_relevance_changed, {"same_evidence": goal.get("same_evidence"), "sufficiency_changed": goal_sufficiency_changed, "relevance_changed": goal_relevance_changed}),
        _check("irrelevant_change_does_not_change_field_cognition", irrelevant.get("same_evidence") is True and not irrelevant.get("changed_semantic_fields"), irrelevant),
        _check("evidence_not_promoted_to_fact", owner.get("semantic_snapshot", {}).get("candidate_only") is True),
        _check("hypothesis_not_promoted_to_truth", owner.get("semantic_snapshot", {}).get("causal_truth") is False),
        _check("current_world_candidate_not_promoted_to_world_truth", owner.get("semantic_snapshot", {}).get("world_truth_declared") is False),
        _check("conflicting_evidence_preserved", bool(conflict.get("semantic_snapshot", {}).get("conflict_refs")) and conflict.get("semantic_snapshot", {}).get("hypothesis_state") == "CONTESTED" and conflict.get("semantic_snapshot", {}).get("causal_truth") is False, conflict.get("semantic_snapshot")),
        _check("missing_information_produces_gap", missing.get("semantic_snapshot", {}).get("sufficiency_status") == "INSUFFICIENT" and missing.get("information_gap_ref")),
        _check("material_new_evidence_can_trigger_revision", bool((summary.get("operational_source", {}).get("cases") or [{}])[1].get("source_case", {}).get("task_case", {}).get("decision_case", {}).get("cognitive_case", {}).get("cognitive_proofs", [{}])[-1].get("hypothesis_revision_ref")), "existing verified Case B proof"),
        _check("sufficient_information_produces_stop", owner.get("semantic_snapshot", {}).get("sufficiency_status") == "SUFFICIENT" and owner.get("stop_ref")),
        _check("no_premature_stop", missing.get("stop_ref") is None),
        _check("no_post_sufficiency_over_observation", owner.get("reobservation_ref") is None),
    ]
    return checks


def verify_summary_v1(summary: Dict[str, Any]) -> Dict[str, Any]:
    operational = summary.get("operational") or {}
    operational_checks = [
        _check("phase_present", summary.get("phase") == PHASE),
        _check("operational_e2e_pass", operational.get("result") == "PASS", operational),
        _check("operational_two_cases", operational.get("case_count") == 2),
        _check("no_forbidden_behavior", all(value is False for value in (summary.get("forbidden_behaviors") or {}).values()), summary.get("forbidden_behaviors")),
    ]
    cognitive_checks = _cognitive_checks(summary)
    capability_gaps = summary.get("capability_gaps") or []
    observed_assertion_ids = {item.get("check_id") for item in cognitive_checks}
    cognitive_checks.insert(
        0,
        _check(
            "required_assertion_inventory_complete",
            observed_assertion_ids == REQUIRED_ASSERTIONS,
            {"missing": sorted(REQUIRED_ASSERTIONS - observed_assertion_ids), "unexpected": sorted(observed_assertion_ids - REQUIRED_ASSERTIONS)},
        ),
    )
    cognitive_pass = not capability_gaps and all(item["passed"] for item in cognitive_checks)
    operational_pass = all(item["passed"] for item in operational_checks)
    all_checks = operational_checks + cognitive_checks
    return {
        "phase": PHASE,
        "operational_result": "PASS" if operational_pass else "FAIL",
        "cognitive_logic_result": "PASS" if cognitive_pass else "FAIL",
        "cognitive_logic_assertions": cognitive_checks,
        "capability_gaps": capability_gaps,
        "contrast_case_results": summary.get("contrast_case_results") or [],
        "final_decision": "GO" if operational_pass and cognitive_pass else "NOT_GO",
        "checks": all_checks,
        "failed_checks": [item["check_id"] for item in all_checks if not item["passed"]],
        "all_checks_passed": operational_pass and cognitive_pass,
        "status": "WAITING_FOR_USER_TERMINAL_VERIFICATION",
    }


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: python -m capabilities.evaluation.full_end_to_end_cognitive_logic_conformance_regression.verifier_v1 <runner_summary.json>")
    summary = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    result = verify_summary_v1(summary)
    print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
    return 0 if result["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
