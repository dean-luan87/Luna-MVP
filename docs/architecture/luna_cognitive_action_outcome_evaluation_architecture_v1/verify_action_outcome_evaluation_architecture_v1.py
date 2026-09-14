"""V0 static contract verifier for Action Outcome Evaluation Architecture."""
from __future__ import annotations

import ast
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
JSON_FILES = [
    "outcome_schema.json", "outcome_type_registry.json",
    "expected_actual_comparison_contract.json", "outcome_evaluation_contract.json",
    "failure_classification_contract.json", "outcome_experience_relation.json",
    "outcome_memory_relation.json", "outcome_schema_relation.json",
    "outcome_belief_update_relation.json", "outcome_self_boundary.json",
    "ownership_registry.json", "dependency_boundary.json",
    "negative_guards.json", "summary.json",
]
MD_FILES = [
    "action_outcome_architecture.md", "outcome_evaluation_model.md",
    "failure_classification_model.md", "experience_transition_model.md",
    "implementation_plan.md",
]
VERIFIER = "verify_action_outcome_evaluation_architecture_v1.py"


def load(name: str) -> dict:
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
    assets: dict[str, dict] = {}
    for name in JSON_FILES:
        try:
            assets[name] = load(name)
            check(isinstance(assets[name], dict), f"json_object:{name}")
        except (OSError, json.JSONDecodeError):
            check(False, f"json_parse:{name}")
    for name in MD_FILES:
        try:
            check((ROOT / name).read_text(encoding="utf-8").strip() != "", f"markdown_nonempty:{name}")
        except OSError:
            check(False, f"markdown_read:{name}")
    try:
        ast.parse((ROOT / VERIFIER).read_text(encoding="utf-8"))
        check(True, "verifier_ast")
    except (OSError, SyntaxError):
        check(False, "verifier_ast")

    schema = assets["outcome_schema.json"]
    required_fields = {"outcome_id", "action_ref", "expected_outcome", "actual_outcome", "outcome_type", "difference", "impact", "evidence", "field_ref", "provenance", "unknowns"}
    check(required_fields <= set(schema["required"]), "outcome_fields")
    check(schema["action_is_not_outcome"] is True and schema["outcome_is_not_experience"] is True and schema["actual_outcome_requires_reality_evidence"] is True and schema["candidate_only"] is True and schema["direct_reality_mutation"] is False and schema["automatic_memory_write"] is False, "outcome_boundary")

    types = assets["outcome_type_registry.json"]
    check(types["types"] == ["Expected Outcome", "Actual Outcome", "Outcome Difference", "Outcome Impact"], "outcome_types")
    check(types["states"] == ["Success", "Failure", "Partial Success", "Unexpected Outcome", "Unknown"], "outcome_states")
    check(types["expected_source"] == "Decision Candidate" and types["actual_source"] == "Reality Validation / Future Action Runtime" and types["difference_preserved"] is True and types["unknown_preserved"] is True and types["outcome_is_not_experience"] is True and types["candidate_only"] is True, "outcome_type_boundary")

    comparison = assets["expected_actual_comparison_contract.json"]
    check(set(comparison["inputs"]) == {"Expected Outcome", "Actual Outcome", "Decision Reference", "Reality Evidence", "Field Context", "Unknowns"}, "comparison_inputs")
    check(comparison["comparison"] == "Expected Outcome - Actual Outcome" and comparison["expected_source_required"] is True and comparison["actual_reality_evidence_required"] is True and comparison["prediction_error_preserved"] is True and comparison["comparison_is_not_reality_mutation"] is True and comparison["comparison_is_not_belief_mutation"] is True and comparison["candidate_only"] is True, "comparison_boundary")

    evaluation = assets["outcome_evaluation_contract.json"]
    check(set(evaluation["dimensions"]) == {"Goal Achievement", "Safety Result", "Resource Efficiency", "Prediction Accuracy", "User Impact"}, "evaluation_dimensions")
    check(set(evaluation["inputs"]) == {"Outcome", "Goal", "Expected Outcome", "Actual Outcome", "Outcome Difference", "Evidence", "Self State", "Field Context"}, "evaluation_inputs")
    check(set(evaluation["output"]) == {"Outcome Quality Candidate", "Learning Signal Candidate", "Experience Candidate", "Failure Classification Candidate"}, "evaluation_outputs")
    check(evaluation["calculation_implemented"] is False and evaluation["candidate_only"] is True and evaluation["failure_is_information"] is True and evaluation["evaluation_does_not_modify_reality"] is True and evaluation["evaluation_does_not_execute_action"] is True and evaluation["automatic_learning"] is False, "evaluation_boundary")

    failure = assets["failure_classification_contract.json"]
    failure_classes = {"Perception Failure", "Understanding Failure", "Decision Failure", "Execution Failure", "Environment Change"}
    check(set(failure["classes"]) == failure_classes, "failure_classes")
    check(failure["multi_causal"] is True and failure["unknown_classification_allowed"] is True and failure["single_outcome_schema_update"] is False and failure["classification_does_not_modify_self"] is True and failure["classification_does_not_modify_personality"] is True and failure["candidate_only"] is True, "failure_boundary")

    experience = assets["outcome_experience_relation.json"]
    check(experience["flow"] == ["Outcome", "Outcome Evaluation", "Experience Candidate", "Experience Validation", "Memory/Schema Candidate"], "experience_flow")
    check(experience["outcome_is_fact_candidate"] is True and experience["experience_requires_situated_context"] is True and experience["outcome_is_not_experience"] is True and experience["outcome_does_not_write_experience_directly"] is True and experience["repetition_or_impact_required_for_reinforcement"] is True and experience["automatic_learning"] is False, "experience_boundary")

    memory = assets["outcome_memory_relation.json"]
    check(memory["flow"] == ["Outcome", "Evaluation", "Experience Candidate", "Memory Candidate", "Information Lifecycle Consolidation"], "memory_flow")
    check(memory["information_lifecycle_required"] is True and memory["memory_candidate_only"] is True and memory["automatic_memory_write"] is False and memory["single_outcome_is_not_memory"] is True and memory["memory_does_not_override_reality"] is True and memory["current_reality_precedence"] is True, "memory_boundary")
    schema_relation = assets["outcome_schema_relation.json"]
    check(schema_relation["flow"] == ["Outcome Pattern Candidates", "Repetition/Impact Validation", "Schema Candidate", "Schema Governance"], "schema_flow")
    check(schema_relation["schema_requires_repeated_pattern"] is True and schema_relation["single_outcome_updates_schema"] is False and schema_relation["schema_candidate_only"] is True and schema_relation["automatic_schema_update"] is False and schema_relation["schema_is_not_reality"] is True and schema_relation["source_lineage_preserved"] is True, "schema_boundary")

    belief = assets["outcome_belief_update_relation.json"]
    check(belief["flow"] == ["Belief", "Prediction/Expectation", "Outcome", "Prediction Error", "Belief Update Candidate"], "belief_flow")
    check(belief["belief_update_is_candidate"] is True and belief["direct_belief_mutation"] is False and belief["reality_precedence"] is True and belief["prediction_error_preserved"] is True and belief["unknowns_preserved"] is True and belief["automatic_belief_update"] is False, "belief_boundary")

    self_boundary = assets["outcome_self_boundary.json"]
    check(set(self_boundary["self_outputs"]) == {"Capability Adjustment Candidate", "Degradation Candidate", "Recovery Candidate", "Self Governance Review Candidate"}, "self_outputs")
    check(self_boundary["self_governance_required"] is True and self_boundary["direct_self_modification"] is False and self_boundary["automatic_capability_change"] is False and self_boundary["personality_change"] is False and self_boundary["identity_change"] is False and self_boundary["goal_change"] is False and self_boundary["outcome_does_not_modify_self_directly"] is True and self_boundary["candidate_only"] is True, "self_boundary")

    ownership = assets["ownership_registry.json"]
    owners = [x["owner"] for x in ownership["ownership"]]
    required_owners = {"Action Runtime", "Outcome Layer", "Reality Validation", "Decision", "Experience", "Memory", "Schema", "Belief", "Self", "Information Lifecycle", "Learning"}
    check(ownership["unique_owner_required"] is True and len(owners) == len(set(owners)), "unique_owners")
    check(required_owners <= set(owners), "ownership_coverage")
    check(all(x.get("writer") and x.get("reader") for x in ownership["ownership"]), "ownership_writer_reader")

    dependency = assets["dependency_boundary.json"]
    required_forbidden = {"Outcome -> Direct Self Modification", "Failure -> Direct Personality Change", "Single Outcome -> Immediate Schema Update", "Memory -> Override Reality", "Outcome Evaluation -> Direct Action", "Outcome Evaluation -> Direct Memory Write", "Outcome Evaluation -> Direct Belief Mutation", "Outcome Evaluation -> Direct Goal Mutation", "Outcome Evaluation -> Execute Learning", "B Route -> Override Actual Outcome"}
    check(required_forbidden <= set(dependency["forbidden_dependencies"]), "dependency_forbidden")
    check(dependency["no_action_runtime"] is True and dependency["no_outcome_collector"] is True and dependency["no_learning_runtime"] is True and dependency["no_automatic_memory_write"] is True and dependency["no_automatic_schema_update"] is True and dependency["no_emotion_runtime"] is True and dependency["no_b_route_runtime"] is True, "dependency_boundary")

    guards = assets["negative_guards.json"]
    required_guards = {"action_runtime", "outcome_collector", "learning_runtime", "automatic_memory_write", "automatic_schema_update", "automatic_belief_update", "automatic_learning", "emotion_runtime", "b_route_runtime", "action_outcome_direct_self_modification", "failure_direct_personality_change", "single_outcome_immediate_schema_update", "memory_override_reality", "outcome_evaluation_direct_action", "outcome_evaluation_direct_memory", "outcome_evaluation_direct_belief", "outcome_evaluation_direct_goal", "outcome_evaluation_direct_value", "model_calls", "provider_calls", "hardware_control", "no_check_weaken", "no_hardcoded_pass"}
    check(required_guards <= set(guards["forbidden"]), "negative_guards")
    check(guards["action_is_not_outcome"] is True and guards["outcome_is_not_experience"] is True and guards["failure_is_information"] is True and guards["single_outcome_is_not_schema"] is True and guards["reality_precedence"] is True and guards["candidate_only"] is True and guards["unknowns_preserved"] is True, "negative_invariants")

    summary = assets["summary.json"]
    check(summary["status"] == "architecture_only" and summary["readiness_token"] == "LUNA_COGNITIVE_ACTION_OUTCOME_EVALUATION_ARCHITECTURE_READY", "summary_status")
    check(summary["outcome_types"] == ["Expected Outcome", "Actual Outcome", "Outcome Difference", "Outcome Impact"] and summary["outcome_states"] == ["Success", "Failure", "Partial Success", "Unexpected Outcome", "Unknown"], "summary_types")
    check(summary["failure_classes"] == ["Perception Failure", "Understanding Failure", "Decision Failure", "Execution Failure", "Environment Change"] and summary["evaluation_dimensions"] == ["Goal Achievement", "Safety Result", "Resource Efficiency", "Prediction Accuracy", "User Impact"], "summary_evaluation")
    check(summary["runtime"] is False and summary["action_runtime"] is False and summary["outcome_collector"] is False and summary["learning_runtime"] is False and summary["automatic_memory_write"] is False and summary["automatic_schema_update"] is False and summary["emotion_runtime"] is False and summary["b_route_runtime"] is False, "summary_boundary")
    check(len(summary["reusable_assets"]) >= 6 and len(summary["parallel_risks"]) >= 3 and len(summary["migration_mapping"]) >= 3, "summary_inventory")

    forbidden_imports = {"subprocess", "socket", "requests", "cv2", "torch", "transformers", "sqlite3", "psycopg2"}
    try:
        tree = ast.parse((ROOT / VERIFIER).read_text(encoding="utf-8"))
        imports = {n.names[0].name.split(".")[0] for n in ast.walk(tree) if isinstance(n, ast.Import) and n.names}
        imports |= {n.module.split(".")[0] for n in ast.walk(tree) if isinstance(n, ast.ImportFrom) and n.module}
        check(not imports & forbidden_imports, "verifier_no_runtime_imports")
    except (OSError, SyntaxError):
        check(False, "verifier_no_runtime_imports")

    blockers = len(failed)
    print(f"CHECKS: {checks}")
    print(f"FAILED_CHECKS: {failed}")
    print(f"PASSED_CHECK_COUNT: {checks - blockers}")
    print(f"FAILED_CHECK_COUNT: {blockers}")
    print(f"BLOCKER_COUNT: {blockers}")
    if blockers:
        print("FINAL_DECISION: BLOCKED_BY_VERIFIER_FAILURE")
        print("READINESS: LUNA_COGNITIVE_ACTION_OUTCOME_EVALUATION_ARCHITECTURE_REMEDIATION_REQUIRED")
        print("NEXT: REMEDIATE_REPORTED_FAILURES_ONLY")
        return 1
    print("FINAL_DECISION: V2_FINAL_VERIFICATION_PASSED")
    print("READINESS: LUNA_COGNITIVE_ACTION_OUTCOME_EVALUATION_ARCHITECTURE_READY")
    print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
