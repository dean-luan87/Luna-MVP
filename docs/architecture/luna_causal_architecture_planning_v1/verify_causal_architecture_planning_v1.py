#!/usr/bin/env python3
"""Read-only final phase verifier for Causal Architecture Planning v1."""

from __future__ import annotations

import ast
import json
import sys
from pathlib import Path
from typing import Any, Dict


BASE = Path(__file__).resolve().parent
READY = "LUNA_CAUSAL_ARCHITECTURE_PLANNING_READY"
REMEDIATION = "LUNA_CAUSAL_ARCHITECTURE_PLANNING_REMEDIATION_REQUIRED"

REQUIRED_FILES = {
    "causal_architecture_plan_v1.md",
    "causal_concept_boundary_matrix_v1.json",
    "causal_owner_boundary_candidate_v1.json",
    "causal_hypothesis_schema_candidate_v1.json",
    "causal_state_model_candidate_v1.json",
    "causal_formation_contract_candidate_v1.json",
    "causal_evidence_support_opposition_model_candidate_v1.json",
    "causal_multi_hypothesis_coexistence_model_candidate_v1.json",
    "causal_competition_alternative_explanation_model_candidate_v1.json",
    "causal_confounder_model_candidate_v1.json",
    "causal_temporal_ordering_boundary_candidate_v1.json",
    "causal_counterfactual_candidate_model_v1.json",
    "causal_uncertainty_confidence_boundary_candidate_v1.json",
    "causal_memory_prior_influence_boundary_candidate_v1.json",
    "causal_intent_influence_boundary_candidate_v1.json",
    "causal_field_context_influence_boundary_candidate_v1.json",
    "causal_provenance_trace_schema_candidate_v1.json",
    "causal_revision_suspension_revocation_model_candidate_v1.json",
    "causal_to_decision_handoff_contract_candidate_v1.json",
    "causal_negative_guards_v1.json",
    "causal_existing_asset_reuse_mapping_v1.json",
    "causal_minimum_scenario_suite_v1.json",
    "causal_open_questions_registry_v1.json",
    "causal_planning_change_manifest_v1.json",
    "phase_contract.json",
    "causal_architecture_planning_summary_v1.md",
    "verify_causal_architecture_planning_v1.py",
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

    owners = set()
    for name in [
        "causal_concept_boundary_matrix_v1.json",
        "causal_owner_boundary_candidate_v1.json",
        "causal_formation_contract_candidate_v1.json",
        "causal_state_model_candidate_v1.json",
    ]:
        doc = docs.get(name, {})
        if "canonical_owner" in doc:
            owners.add(str(doc.get("canonical_owner")))
        elif "owner" in doc:
            owners.add(str(doc.get("owner")))

    check(owners == {"Causal Governance"}, "owner_uniqueness")

    owner_boundary = docs.get("causal_owner_boundary_candidate_v1.json", {})
    aliases = owner_boundary.get("legacy_aliases", [])
    check(owner_boundary.get("unique_owner") is True, "owner_unique_true")
    check(
        all(item.get("creates_new_owner") is False for item in aliases),
        "no_parallel_causal_owner",
    )

    concept = docs.get("causal_concept_boundary_matrix_v1.json", {})
    neq = concept.get("non_equivalence_guards", {})
    check(
        neq.get("temporal_precedence_not_causality") is True,
        "temporal_not_causal_guard",
    )
    check(neq.get("correlation_not_causality") is True, "correlation_not_causal_guard")

    handoff = docs.get("causal_to_decision_handoff_contract_candidate_v1.json", {})
    forbidden = set(handoff.get("forbidden_output", []))
    check(
        {"final decision", "action instruction", "task"} <= forbidden,
        "no_decision_action_task_output",
    )
    guards = handoff.get("guards", {})
    check(guards.get("candidate_only") is True, "handoff_candidate_only")

    for influence_file in [
        "causal_intent_influence_boundary_candidate_v1.json",
        "causal_memory_prior_influence_boundary_candidate_v1.json",
        "causal_field_context_influence_boundary_candidate_v1.json",
    ]:
        data = docs.get(influence_file, {})
        text = " ".join(json.dumps(data, ensure_ascii=False).lower().split())
        check(
            "cross_write" in text or "mutates" in text,
            f"influence_boundary_present:{influence_file}",
        )

    multi = docs.get("causal_multi_hypothesis_coexistence_model_candidate_v1.json", {})
    check(
        "multiple hypothesis coexistence" in multi.get("supports", []),
        "multi_hypothesis_support",
    )

    confounder = docs.get("causal_confounder_model_candidate_v1.json", {})
    check(bool(confounder.get("required_fields")), "confounder_support")

    counterfactual = docs.get("causal_counterfactual_candidate_model_v1.json", {})
    cguards = counterfactual.get("guards", {})
    check(cguards.get("counterfactual_is_fact") is False, "counterfactual_support")

    uncertainty = docs.get(
        "causal_uncertainty_confidence_boundary_candidate_v1.json", {}
    )
    urules = set(uncertainty.get("rules", []))
    check("uncertainty_must_be_visible" in urules, "uncertainty_support")

    trace = docs.get("causal_provenance_trace_schema_candidate_v1.json", {})
    required_trace = set(trace.get("required", []))
    check(
        {"trace_id", "hypothesis_refs", "evidence_refs", "provenance"}
        <= required_trace,
        "provenance_completeness",
    )

    scenarios = docs.get("causal_minimum_scenario_suite_v1.json", {})
    check(scenarios.get("scenario_count") == 12, "minimum_scenario_count")
    check(len(scenarios.get("scenarios", [])) == 12, "minimum_scenario_coverage")

    manifest = docs.get("causal_planning_change_manifest_v1.json", {})
    check(
        manifest.get("modified_existing_files") == [], "no_existing_asset_modification"
    )

    phase = docs.get("phase_contract.json", {})
    check(phase.get("execution_mode") == "Planning Only", "phase_mode_planning_only")
    check(phase.get("planning_only") is True, "phase_planning_only_true")
    check(phase.get("runtime_executed") is False, "phase_runtime_false")
    check(phase.get("decision_executed") is False, "phase_no_decision")
    check(phase.get("action_triggered") is False, "phase_no_action")
    check(phase.get("task_created") is False, "phase_no_task")

    try:
        ast.parse(
            (BASE / "verify_causal_architecture_planning_v1.py").read_text(
                encoding="utf-8"
            )
        )
        check(True, "verifier_ast_parse")
    except SyntaxError:
        check(False, "verifier_ast_parse")

    emit(checks, failures)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
