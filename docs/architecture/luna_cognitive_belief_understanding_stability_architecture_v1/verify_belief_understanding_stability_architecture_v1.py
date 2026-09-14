"""Static final-phase contract verifier for Belief and Understanding stability."""
from __future__ import annotations

import ast
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
JSON_FILES = [
    "belief_schema.json",
    "belief_type_registry.json",
    "belief_evidence_relation_contract.json",
    "belief_confidence_contract.json",
    "belief_update_contract.json",
    "belief_validation_contract.json",
    "understanding_schema.json",
    "understanding_lifecycle_contract.json",
    "understanding_belief_relation.json",
    "belief_memory_relation.json",
    "belief_schema_relation.json",
    "belief_uncertainty_relation.json",
    "self_belief_boundary.json",
    "ownership_registry.json",
    "dependency_boundary.json",
    "negative_guards.json",
    "summary.json",
]
MD_FILES = [
    "cognitive_belief_architecture.md",
    "understanding_stability_model.md",
    "belief_update_model.md",
    "implementation_plan.md",
]
VERIFIER = "verify_belief_understanding_stability_architecture_v1.py"


def read_json(name: str) -> dict:
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def main() -> int:
    checks = 0
    failed: list[str] = []

    def check(condition: bool, label: str) -> None:
        nonlocal checks
        checks += 1
        if not condition:
            failed.append(label)

    files = {p.name for p in ROOT.iterdir() if p.is_file()}
    check(set(JSON_FILES) | set(MD_FILES) | {VERIFIER} <= files, "required_assets")
    check({p.name for p in ROOT.glob("*.py")} == {VERIFIER}, "no_runtime_python")
    assets = {name: read_json(name) for name in JSON_FILES}
    for name in JSON_FILES:
        check(isinstance(assets[name], dict), f"json_object:{name}")
    for name in MD_FILES:
        check((ROOT / name).read_text(encoding="utf-8").strip() != "", f"markdown_nonempty:{name}")
    try:
        ast.parse((ROOT / VERIFIER).read_text(encoding="utf-8"))
        check(True, "verifier_ast")
    except SyntaxError:
        check(False, "verifier_ast")

    belief = assets["belief_schema.json"]
    required_belief = {"source_evidence", "supporting_evidence", "contradicting_evidence", "confidence", "validity_range", "context", "field_ref", "related_schema", "related_memory", "uncertainty", "provenance"}
    check(required_belief <= set(belief["required_binding"]), "belief_bindings")
    check(belief["belief_is_reality"] is False and belief["belief_is_knowledge"] is False and belief["belief_is_memory"] is False and belief["candidate_only"] is True and belief["field_bound"] is True, "belief_boundary")

    type_registry = assets["belief_type_registry.json"]
    belief_types = {"Perceptual Belief", "Semantic Belief", "Context Belief", "Social Belief", "Self Belief", "Decision Belief"}
    check(set(type_registry["types"]) == belief_types, "belief_type_coverage")
    check(type_registry["candidate_required"] is True and type_registry["field_context_required"] is True and type_registry["reality_precedence"] is True and type_registry["truth_assertion"] is False, "belief_type_boundary")

    evidence = assets["belief_evidence_relation_contract.json"]
    check(evidence["source_required"] is True and evidence["supporting_and_contradicting_preserved"] is True and evidence["evidence_is_belief"] is False and evidence["reality_write"] is False and evidence["candidate_only"] is True, "evidence_relation")
    confidence = assets["belief_confidence_contract.json"]
    check(confidence["confidence_is_truth"] is False and confidence["truth_assertion"] is False and confidence["calculation_implemented"] is False and confidence["unknown_preserved"] is True and confidence["candidate_only"] is True, "confidence_boundary")

    update = assets["belief_update_contract.json"]
    update_types = {"Strengthen", "Weaken", "Replace", "Invalidate", "Suspend"}
    check(set(update["update_types"]) == update_types, "update_types")
    check(update["original_belief_preserved"] is True and update["automatic_update"] is False and update["reality_precedence"] is True and update["candidate_only"] is True, "update_boundary")

    validation = assets["belief_validation_contract.json"]
    results = {"Confirmed", "Supported", "Contradicted", "Unknown", "Expired"}
    check(set(validation["result_values"]) == results, "validation_results")
    check(validation["reality_precedence"] is True and validation["direct_belief_mutation"] is False and validation["direct_memory_mutation"] is False and validation["candidate_only"] is True, "validation_boundary")

    understanding = assets["understanding_schema.json"]
    required_understanding = {"belief_refs", "selected_evidence", "unknown_state", "conflict_state", "confidence", "provenance", "time"}
    check(required_understanding <= set(understanding["required_fields"]), "understanding_bindings")
    check(understanding["candidate_only"] is True and understanding["understanding_is_reality"] is False and understanding["understanding_is_world_model"] is False and understanding["current_reality_precedence"] is True and understanding["decision_authority"] is False, "understanding_boundary")

    lifecycle = assets["understanding_lifecycle_contract.json"]
    lifecycle_states = {"Candidate Understanding", "Supported Understanding", "Active Understanding", "Challenged Understanding", "Invalidated Understanding", "Archived Understanding"}
    check(set(lifecycle["states"]) == lifecycle_states, "understanding_lifecycle")
    check(set(lifecycle["required_conditions"]) == {"multiple_evidence_support", "context_stability", "decision_relevance"}, "understanding_conditions")
    check(lifecycle["automatic_transition"] is False and lifecycle["invalidated_is_deleted"] is False and lifecycle["unknown_allowed"] is True and lifecycle["candidate_only"] is True, "understanding_lifecycle_boundary")

    relation = assets["understanding_belief_relation.json"]
    check(relation["multiple_beliefs_allowed"] is True and relation["belief_is_not_fact"] is True and relation["schema_is_prior_not_decision"] is True and relation["memory_is_context_not_override"] is True and relation["candidate_only"] is True, "understanding_belief_relation")
    memory = assets["belief_memory_relation.json"]
    check(memory["flow"] == ["Memory", "Prior Experience", "Belief Candidate", "Reality Validation"], "belief_memory_flow")
    check(memory["memory_direct_belief_override"] is False and memory["memory_replaces_reality"] is False and memory["current_reality_precedence"] is True and memory["candidate_only"] is True, "belief_memory_boundary")
    schema = assets["belief_schema_relation.json"]
    check(schema["flow"] == ["Schema", "Prior", "Hypothesis", "Belief", "Understanding"], "belief_schema_flow")
    check(schema["schema_influences"] is True and schema["schema_determines"] is False and schema["forced_conclusion"] is False and schema["candidate_only"] is True, "belief_schema_boundary")
    uncertainty = assets["belief_uncertainty_relation.json"]
    check(uncertainty["multiple_beliefs_allowed"] is True and uncertainty["unknown_preserved"] is True and uncertainty["forced_resolution"] is False and uncertainty["confidence_is_truth"] is False and uncertainty["candidate_only"] is True, "belief_uncertainty_boundary")

    self_boundary = assets["self_belief_boundary.json"]
    check(self_boundary["direct_self_modification"] is False and self_boundary["identity_write"] is False and self_boundary["value_write"] is False and self_boundary["goal_write"] is False and self_boundary["candidate_only"] is True and self_boundary["governance_required"] is True, "self_belief_boundary")

    ownership = assets["ownership_registry.json"]
    owners = [x["owner"] for x in ownership["ownership"]]
    required_owners = {"Reality", "Evidence Layer", "Hypothesis", "Belief Layer", "Understanding", "Reality Validation", "Memory", "Schema", "Self", "Brain"}
    check(ownership["unique_owner_required"] is True and len(owners) == len(set(owners)), "unique_owners")
    check(required_owners <= set(owners), "ownership_coverage")
    check(all(x.get("writer") for x in ownership["ownership"]), "writers_declared")

    dependency = assets["dependency_boundary.json"]
    check(dependency["no_parallel_belief_store"] is True and dependency["no_independent_knowledge_judgment"] is True and dependency["brain_runtime_unchanged"] is True and dependency["decision_runtime_unchanged"] is True and dependency["runtime"] is False, "dependency_boundary")
    forbidden_dependencies = set(dependency["forbidden_dependencies"])
    check("Belief -> Reality Replacement" in forbidden_dependencies and "Memory -> Direct Belief Override" in forbidden_dependencies and "Schema -> Forced Conclusion" in forbidden_dependencies, "dependency_reality_memory_schema")
    check("Confidence -> Truth Assertion" in forbidden_dependencies and "Understanding -> Direct Action" in forbidden_dependencies, "dependency_confidence_action")

    guards = assets["negative_guards.json"]
    required_guards = {"belief_runtime", "confidence_engine", "automatic_reasoning", "model_calls", "knowledge_retrieval", "memory_modification", "decision_execution", "belief_reality_replacement", "memory_direct_belief_override", "schema_forced_conclusion", "confidence_truth_assertion", "understanding_direct_action", "parallel_belief_store", "independent_knowledge_judgment", "brain_runtime_modification", "decision_runtime_modification", "automatic_belief_update"}
    check(required_guards <= set(guards["forbidden"]), "negative_guards")
    check(guards["reality_highest_priority"] is True and guards["belief_is_best_current_explanation"] is True and guards["unknown_preserved"] is True and guards["candidate_only"] is True and guards["provenance_required"] is True, "negative_invariants")
    check(guards["no_check_weaken"] is True and guards["no_hardcoded_pass"] is True, "negative_verifier_guards")

    summary = assets["summary.json"]
    check(summary["status"] == "architecture_only", "summary_status")
    check(summary["readiness_token"] == "LUNA_COGNITIVE_BELIEF_UNDERSTANDING_STABILITY_ARCHITECTURE_READY", "summary_readiness")
    check(summary["belief_types"] == ["Perceptual Belief", "Semantic Belief", "Context Belief", "Social Belief", "Self Belief", "Decision Belief"], "summary_belief_types")
    check(summary["runtime"] is False and summary["confidence_engine"] is False and summary["automatic_reasoning"] is False and summary["memory_modification"] is False and summary["decision_execution"] is False, "summary_boundary")
    check(len(summary["reusable_assets"]) >= 5 and len(summary["existing_belief_understanding_assets"]) >= 4 and len(summary["parallel_risks"]) >= 3 and len(summary["migration_mapping"]) >= 1, "summary_inventory")

    forbidden_imports = {"subprocess", "socket", "requests", "cv2", "torch", "transformers", "sqlite3", "psycopg2"}
    try:
        tree = ast.parse((ROOT / VERIFIER).read_text(encoding="utf-8"))
        imports = {node.names[0].name.split(".")[0] for node in ast.walk(tree) if isinstance(node, ast.Import) and node.names}
        imports |= {node.module.split(".")[0] for node in ast.walk(tree) if isinstance(node, ast.ImportFrom) and node.module}
        check(not imports & forbidden_imports, "verifier_no_runtime_imports")
    except SyntaxError:
        check(False, "verifier_no_runtime_imports")

    blockers = len(failed)
    print(f"CHECKS: {checks}")
    print(f"FAILED_CHECKS: {failed}")
    print(f"PASSED_CHECK_COUNT: {checks - blockers}")
    print(f"FAILED_CHECK_COUNT: {blockers}")
    print(f"BLOCKER_COUNT: {blockers}")
    if blockers:
        print("FINAL_DECISION: BLOCKED_BY_VERIFIER_FAILURE")
        print("READINESS: LUNA_COGNITIVE_BELIEF_UNDERSTANDING_STABILITY_ARCHITECTURE_REMEDIATION_REQUIRED")
        print("NEXT: REMEDIATE_REPORTED_FAILURES_ONLY")
        return 1
    print("FINAL_DECISION: V2_FINAL_VERIFICATION_PASSED")
    print("READINESS: LUNA_COGNITIVE_BELIEF_UNDERSTANDING_STABILITY_ARCHITECTURE_READY")
    print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
