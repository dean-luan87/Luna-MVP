#!/usr/bin/env python3
"""Read-only final phase verifier for Decision Architecture Planning v1."""

from __future__ import annotations

import ast
import json
import sys
from pathlib import Path
from typing import Any, Dict


BASE = Path(__file__).resolve().parent
READY = "LUNA_DECISION_ARCHITECTURE_PLANNING_READY"
REMEDIATION = "LUNA_DECISION_ARCHITECTURE_PLANNING_REMEDIATION_REQUIRED"

REQUIRED_FILES = {
    "decision_architecture_plan_v1.md",
    "decision_concept_boundary_matrix_v1.json",
    "decision_owner_boundary_candidate_v1.json",
    "decision_candidate_schema_v1.json",
    "decision_state_model_candidate_v1.json",
    "decision_formation_contract_candidate_v1.json",
    "decision_option_model_candidate_v1.json",
    "decision_multi_candidate_coexistence_model_candidate_v1.json",
    "decision_selection_boundary_candidate_v1.json",
    "decision_risk_model_candidate_v1.json",
    "decision_utility_model_candidate_v1.json",
    "decision_constraint_model_candidate_v1.json",
    "decision_permission_safety_boundary_candidate_v1.json",
    "decision_role_influence_boundary_candidate_v1.json",
    "decision_intent_influence_boundary_candidate_v1.json",
    "decision_causal_influence_boundary_candidate_v1.json",
    "decision_defer_abstain_evidence_request_model_candidate_v1.json",
    "decision_reversibility_model_candidate_v1.json",
    "decision_human_confirmation_boundary_candidate_v1.json",
    "decision_resource_constraint_model_candidate_v1.json",
    "decision_provenance_trace_schema_candidate_v1.json",
    "decision_revision_suspension_revocation_model_candidate_v1.json",
    "decision_to_action_task_handoff_contract_candidate_v1.json",
    "decision_negative_guards_v1.json",
    "decision_existing_asset_reuse_mapping_v1.json",
    "decision_minimum_scenario_suite_v1.json",
    "decision_open_questions_registry_v1.json",
    "decision_planning_change_manifest_v1.json",
    "decision_architecture_planning_summary_v1.md",
    "phase_contract.json",
    "verify_decision_architecture_planning_v1.py",
}

JSON_FILES = {name for name in REQUIRED_FILES if name.endswith(".json")}


def load_json(path: Path) -> Dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"{path.name} must contain a JSON object")
    return value


def emit(checks: list[str], failures: list[str]) -> None:
    print("CHECKS")
    for item in checks:
        print(item)

    print("FAILED_CHECKS")
    for item in failures:
        print(item)

    print("PASSED_CHECK_COUNT")
    print(max(0, len(checks) - len(failures)))

    print("FAILED_CHECK_COUNT")
    print(len(failures))

    print("BLOCKER_COUNT")
    print(len(failures))

    print("FINAL_DECISION")
    print(READY if not failures else "BLOCKED_BY_VERIFIER_FAILURE")

    print("READINESS")
    print(READY if not failures else REMEDIATION)

    print("NEXT")
    print(
        "RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT"
        if not failures
        else "REMEDIATE_REPORTED_FAILURES_ONLY"
    )


def main() -> int:
    checks: list[str] = []
    failures: list[str] = []

    def check(condition: bool, check_id: str) -> None:
        checks.append(check_id)
        if not condition:
            failures.append(check_id)

    actual_files = {path.name for path in BASE.iterdir() if path.is_file()}
    check(actual_files == REQUIRED_FILES, "exact_required_file_set")

    docs: Dict[str, Dict[str, Any]] = {}
    for name in sorted(JSON_FILES):
        try:
            docs[name] = load_json(BASE / name)
            check(True, f"json_parse:{name}")
        except (OSError, TypeError, json.JSONDecodeError):
            docs[name] = {}
            check(False, f"json_parse:{name}")

    try:
        ast.parse(
            (BASE / "verify_decision_architecture_planning_v1.py").read_text(
                encoding="utf-8"
            )
        )
        check(True, "verifier_ast_parse")
    except SyntaxError:
        check(False, "verifier_ast_parse")

    owner = docs.get("decision_owner_boundary_candidate_v1.json", {})
    concept = docs.get("decision_concept_boundary_matrix_v1.json", {})
    check(owner.get("canonical_owner") == "Decision Governance", "canonical_owner")
    check(owner.get("unique_owner") is True, "canonical_owner_unique")
    aliases = owner.get("legacy_aliases", [])
    check(
        all(item.get("mutation_authority") is False for item in aliases),
        "legacy_alias_no_authority",
    )
    check(
        all(item.get("creates_new_owner") is False for item in aliases),
        "no_parallel_decision_owner",
    )

    neq = concept.get("non_equivalence_guards", {})
    check(neq.get("intent_not_decision") is True, "intent_not_decision")
    check(neq.get("causal_hypothesis_not_decision") is True, "causal_not_decision")
    check(neq.get("decision_candidate_not_action") is True, "decision_not_action")
    check(neq.get("decision_not_task") is True, "decision_not_task")

    multi = docs.get("decision_multi_candidate_coexistence_model_candidate_v1.json", {})
    supports = set(multi.get("supports", []))
    check("multiple candidate coexistence" in supports, "multi_candidate_support")

    dar = docs.get(
        "decision_defer_abstain_evidence_request_model_candidate_v1.json", {}
    )
    outcomes = set(dar.get("supported_outcomes", []))
    check("DEFER" in outcomes, "defer_support")
    check("ABSTAIN" in outcomes, "abstain_support")
    check("REQUEST_MORE_EVIDENCE" in outcomes, "request_more_evidence_support")

    utility = docs.get("decision_utility_model_candidate_v1.json", {})
    risk = docs.get("decision_risk_model_candidate_v1.json", {})
    constraint = docs.get("decision_constraint_model_candidate_v1.json", {})
    check(
        utility.get("utility_rules", {}).get("utility_not_permission") is True,
        "utility_permission_separation",
    )
    check(
        risk.get("risk_rules", {}).get("risk_not_safety_authority") is True,
        "risk_safety_separation",
    )
    check(
        constraint.get("constraint_rules", {}).get(
            "hard_constraints_before_soft_preferences"
        )
        is True,
        "hard_constraint_priority",
    )

    ps = docs.get("decision_permission_safety_boundary_candidate_v1.json", {})
    check(
        ps.get("permission_boundary", {}).get(
            "permission_can_veto_candidate_eligibility"
        )
        is True,
        "permission_boundary",
    )
    check(
        ps.get("safety_boundary", {}).get("safety_can_constrain_or_block") is True,
        "safety_boundary",
    )

    role_inf = docs.get("decision_role_influence_boundary_candidate_v1.json", {})
    intent_inf = docs.get("decision_intent_influence_boundary_candidate_v1.json", {})
    causal_inf = docs.get("decision_causal_influence_boundary_candidate_v1.json", {})
    check(
        role_inf.get("role_influence", {}).get("role_is_decision_owner") is False,
        "role_influence_only",
    )
    check(
        intent_inf.get("intent_influence", {}).get("intent_equals_decision") is False,
        "intent_influence_only",
    )
    check(
        causal_inf.get("causal_influence", {}).get("causal_candidate_equals_decision")
        is False,
        "causal_influence_only",
    )

    rev = docs.get("decision_reversibility_model_candidate_v1.json", {})
    levels = set(rev.get("reversibility_levels", []))
    check("IRREVERSIBLE" in levels, "reversibility_support")
    check(
        rev.get("irreversible_escalation_rules", {}).get(
            "confirmation_requirement_stronger"
        )
        is True,
        "irreversible_confirmation_requirement",
    )

    human = docs.get("decision_human_confirmation_boundary_candidate_v1.json", {})
    check(
        human.get("boundary_rules", {}).get(
            "decision_cannot_fabricate_human_confirmation"
        )
        is True,
        "human_confirmation_not_fabricated",
    )

    resource = docs.get("decision_resource_constraint_model_candidate_v1.json", {})
    r_support = set(resource.get("resource_degradation_support", []))
    check(
        "defer" in r_support and "abstain" in r_support, "resource_degradation_support"
    )

    trace = docs.get("decision_provenance_trace_schema_candidate_v1.json", {})
    req_trace = set(trace.get("required", []))
    check(
        {
            "trace_id",
            "intent_refs",
            "causal_refs",
            "evidence_refs",
            "constraint_refs",
            "risk_refs",
            "utility_refs",
            "permission_refs",
            "safety_refs",
            "resource_state_refs",
            "alternative_option_refs",
            "rejected_alternative_refs",
            "selection_or_nonselection_reason_refs",
            "state_transition_refs",
            "revision_lineage_refs",
            "provenance",
        }
        <= req_trace,
        "provenance_completeness",
    )

    handoff = docs.get("decision_to_action_task_handoff_contract_candidate_v1.json", {})
    hguards = handoff.get("guards", {})
    forbidden = set(handoff.get("forbidden_output", []))
    check(hguards.get("candidate_only") is True, "handoff_candidate_only")
    check(
        hguards.get("action_triggered") is False
        and hguards.get("task_created") is False,
        "handoff_no_action_task_execution",
    )
    check(
        "actual action execution" in forbidden and "task creation" in forbidden,
        "handoff_forbidden_outputs",
    )

    scenarios = docs.get("decision_minimum_scenario_suite_v1.json", {})
    check(scenarios.get("scenario_count", 0) >= 14, "minimum_scenario_count")
    scenario_ids = {item.get("scenario_id") for item in scenarios.get("scenarios", [])}
    required_ids = {
        "D01_LOW_RISK_SINGLE_CANDIDATE",
        "D02_TWO_CANDIDATE_COEXISTENCE",
        "D03_HIGH_UTILITY_PERMISSION_DENIED",
        "D04_HIGH_UTILITY_SAFETY_VETO",
        "D05_CAUSAL_UNCERTAINTY_DEFER",
        "D06_EVIDENCE_GAP_REQUEST_MORE",
        "D07_NO_ACCEPTABLE_OPTION_ABSTAIN",
        "D08_REVERSIBLE_CANDIDATE",
        "D09_IRREVERSIBLE_CONFIRMATION_REQUIRED",
        "D10_RESOURCE_CONSTRAINT_LOWER_COST",
        "D11_ROLE_CONSTRAINT_ELIGIBILITY_SHIFT",
        "D12_INTENT_PREFERENCE_NO_OVERRULE",
        "D13_COMPETING_CAUSAL_HYPOTHESES",
        "D14_DECISION_TO_ACTION_TASK_CANDIDATE_ONLY",
    }
    check(required_ids <= scenario_ids, "minimum_scenario_semantic_coverage")

    negative = docs.get("decision_negative_guards_v1.json", {})
    nset = set(negative.get("negative_guards", []))
    check(
        "intent != decision" in nset
        and "decision != action" in nset
        and "decision != task" in nset,
        "negative_guard_core",
    )

    phase = docs.get("phase_contract.json", {})
    check(phase.get("execution_mode") == "Planning Only", "phase_mode_planning_only")
    check(phase.get("planning_only") is True, "planning_only_true")
    check(phase.get("runtime_executed") is False, "runtime_executed_false")
    check(phase.get("decision_execution") is False, "decision_execution_false")
    check(phase.get("action_triggered") is False, "action_triggered_false")
    check(phase.get("task_created") is False, "task_created_false")
    check(phase.get("database_write") is False, "database_write_false")

    manifest = docs.get("decision_planning_change_manifest_v1.json", {})
    check(
        manifest.get("modified_existing_files") == [], "no_existing_asset_modification"
    )

    emit(checks, failures)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
