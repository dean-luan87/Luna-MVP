"""Static final-phase contract verifier for Cognitive Schema Architecture."""
from __future__ import annotations

import ast
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
JSON_FILES = [
    "schema_type_registry.json",
    "field_schema_contract.json",
    "role_schema_contract.json",
    "social_schema_contract.json",
    "self_schema_contract.json",
    "schema_candidate_contract.json",
    "schema_validation_contract.json",
    "schema_activation_contract.json",
    "schema_lifecycle_contract.json",
    "memory_schema_relation_contract.json",
    "knowledge_schema_boundary.json",
    "field_schema_binding_contract.json",
    "role_schema_binding_contract.json",
    "ownership_registry.json",
    "dependency_boundary.json",
    "negative_guards.json",
    "summary.json",
]
MD_FILES = [
    "cognitive_schema_architecture.md",
    "schema_hierarchy_model.md",
    "schema_formation_and_validation.md",
    "implementation_plan.md",
]
VERIFIER = "verify_cognitive_schema_architecture_v1.py"


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

    registry = assets["schema_type_registry.json"]
    schema_types = {"Field Schema", "Role Schema", "Social Schema", "Self Schema"}
    check({x["type"] for x in registry["types"]} == schema_types, "schema_type_coverage")
    check(registry["candidate_required"] is True and registry["automatic_generation"] is False and registry["model_parameter"] is False, "schema_registry_boundary")

    field = assets["field_schema_contract.json"]
    role = assets["role_schema_contract.json"]
    social = assets["social_schema_contract.json"]
    self_schema = assets["self_schema_contract.json"]
    check(field["schema_type"] == "Field Schema" and field["field_bound"] is True and field["candidate_only"] is True, "field_schema_contract")
    check(field["reality_replacement"] is False and field["world_model"] is False and field["direct_decision"] is False, "field_schema_boundary")
    check(role["schema_type"] == "Role Schema" and role["role_bound"] is True and role["candidate_only"] is True, "role_schema_contract")
    check(role["direct_role_update"] is False and role["direct_role_activation"] is False and role["decision_authority"] is False, "role_schema_boundary")
    check(social["schema_type"] == "Social Schema" and social["social_bound"] is True and social["candidate_only"] is True, "social_schema_contract")
    check(social["direct_social_self_update"] is False and social["social_judgment"] is False and social["decision_authority"] is False, "social_schema_boundary")
    check(self_schema["schema_type"] == "Self Schema" and self_schema["self_bound"] is True and self_schema["candidate_only"] is True, "self_schema_contract")
    check(self_schema["direct_self_update"] is False and self_schema["identity_write"] is False and self_schema["value_write"] is False and self_schema["goal_write"] is False, "self_schema_boundary")

    candidate = assets["schema_candidate_contract.json"]
    check(set(candidate["required_sources"]) == {"memory_cluster", "pattern_candidate", "field_context", "validation_results"}, "candidate_sources")
    check(candidate["candidate_only"] is True and candidate["automatic_generation"] is False and candidate["automatic_admission"] is False and candidate["single_experience_to_schema"] is False, "candidate_boundary")

    validation = assets["schema_validation_contract.json"]
    dimensions = {"Repeatability", "Context Stability", "Prediction Support", "Contradiction"}
    check(set(validation["validation_dimensions"]) == dimensions, "validation_dimensions")
    check(validation["long_term_validation_required"] is True and validation["reality_precedence"] is True and validation["prediction_engine"] is False, "validation_boundary")
    check(validation["automatic_admission"] is False and validation["candidate_only"] is True, "validation_candidate")

    activation = assets["schema_activation_contract.json"]
    check(activation["activation_trigger"] == "current_field" and activation["flow"] == ["Current Field", "Schema Activation Candidate", "Context Enhancement Candidate", "Hypothesis", "Understanding"], "activation_flow")
    check(activation["autonomous_activation"] is False and activation["direct_decision_override"] is False and activation["reality_replacement"] is False, "activation_boundary")

    lifecycle = assets["schema_lifecycle_contract.json"]
    lifecycle_states = ["Observed", "Candidate", "Validated", "Active", "Reinforced", "Compressed", "Generalized", "Dormant", "Archived", "Removed"]
    check(lifecycle["states"] == lifecycle_states and lifecycle["removed_definition"] == "no_longer_in_current_cognitive_influence", "lifecycle_states")
    check(lifecycle["destructive_deletion"] is False and lifecycle["long_term_validation_required"] is True and lifecycle["automatic_transition"] is False and lifecycle["memory_lifecycle_reused"] is True, "lifecycle_boundary")

    memory_relation = assets["memory_schema_relation_contract.json"]
    check(memory_relation["flow"] == ["Memory", "Pattern", "Schema Candidate", "Schema Validation", "Schema Admission", "Understanding"], "memory_schema_flow")
    check(memory_relation["schema_deletes_memory"] is False and memory_relation["memory_direct_schema_activation"] is False and memory_relation["candidate_only"] is True, "memory_schema_boundary")

    knowledge = assets["knowledge_schema_boundary.json"]
    check(knowledge["required_flow"] == ["Knowledge", "Practice", "Experience", "Memory", "Pattern", "Schema Candidate"], "knowledge_schema_flow")
    check(knowledge["knowledge_direct_schema"] is False and knowledge["knowledge_auto_injection"] is False and knowledge["practice_required"] is True and knowledge["candidate_only"] is True, "knowledge_schema_boundary")

    field_binding = assets["field_schema_binding_contract.json"]
    role_binding = assets["role_schema_binding_contract.json"]
    check(field_binding["schema_context_only"] is True and field_binding["field_owns_schema"] is False and field_binding["reality_replacement"] is False, "field_binding_boundary")
    check(role_binding["role_owns_schema"] is False and role_binding["schema_creates_role"] is False and role_binding["schema_activates_role"] is False and role_binding["candidate_only"] is True, "role_binding_boundary")

    ownership = assets["ownership_registry.json"]
    owners = [x["owner"] for x in ownership["ownership"]]
    required_owners = {"Memory", "Experience", "Information Lifecycle", "Schema Layer", "Knowledge", "Field", "Role", "Self", "Brain"}
    check(ownership["unique_owner_required"] is True and len(owners) == len(set(owners)), "unique_owners")
    check(required_owners <= set(owners), "ownership_coverage")
    check(all(x.get("writer") for x in ownership["ownership"]), "writers_declared")

    dependency = assets["dependency_boundary.json"]
    check(dependency["no_parallel_memory"] is True and dependency["no_parallel_knowledge"] is True and dependency["runtime_implementation"] is False and dependency["schema_store"] is False, "dependency_no_parallel_runtime")
    forbidden_dependencies = set(dependency["forbidden_dependencies"])
    check("Memory -> Direct Schema Activation" in forbidden_dependencies and "Knowledge -> Automatic Schema Creation" in forbidden_dependencies, "dependency_memory_knowledge")
    check("Schema -> Direct Decision Override" in forbidden_dependencies and "Schema -> Reality Replacement" in forbidden_dependencies and "Schema -> Self Modification" in forbidden_dependencies, "dependency_schema_authority")

    guards = assets["negative_guards.json"]
    required_guards = {"runtime", "schema_store", "automatic_schema_generation", "automatic_pattern_mining", "automatic_learning", "model_training", "parameter_update", "knowledge_automatic_injection", "emotion_runtime", "b_route", "decision_override", "self_automatic_modification", "memory_direct_schema_activation", "knowledge_automatic_schema_creation", "schema_direct_decision_override", "schema_reality_replacement", "schema_self_modification", "parallel_memory", "parallel_knowledge", "database_access", "model_calls"}
    check(required_guards <= set(guards["forbidden"]), "negative_guards")
    check(guards["schema_is_not_memory"] is True and guards["schema_is_not_knowledge"] is True and guards["schema_is_not_model"] is True, "negative_schema_boundaries")
    check(guards["long_term_validation_required"] is True and guards["candidate_only"] is True and guards["unknown_preserved"] is True and guards["provenance_preserved"] is True, "negative_invariants")
    check(guards["no_check_weaken"] is True and guards["no_hardcoded_pass"] is True, "negative_verifier_guards")

    summary = assets["summary.json"]
    check(summary["status"] == "architecture_only", "summary_status")
    check(summary["readiness_token"] == "LUNA_COGNITIVE_SCHEMA_ARCHITECTURE_READY", "summary_readiness")
    check(summary["schema_types"] == ["Field Schema", "Role Schema", "Social Schema", "Self Schema"], "summary_schema_types")
    check(summary["runtime"] is False and summary["schema_store"] is False and summary["automatic_learning"] is False and summary["model_training"] is False and summary["database_access"] is False, "summary_boundary")
    check(len(summary["reusable_schema_assets"]) >= 3 and len(summary["memory_pattern_assets"]) >= 2 and len(summary["knowledge_assets"]) >= 2 and len(summary["parallel_risks"]) >= 3 and len(summary["migration_mapping"]) >= 1, "summary_inventory")

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
        print("READINESS: LUNA_COGNITIVE_SCHEMA_ARCHITECTURE_REMEDIATION_REQUIRED")
        print("NEXT: REMEDIATE_REPORTED_FAILURES_ONLY")
        return 1
    print("FINAL_DECISION: V2_FINAL_VERIFICATION_PASSED")
    print("READINESS: LUNA_COGNITIVE_SCHEMA_ARCHITECTURE_READY")
    print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
