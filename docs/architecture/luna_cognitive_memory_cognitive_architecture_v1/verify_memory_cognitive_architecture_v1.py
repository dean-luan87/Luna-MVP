"""Static final-phase contract verifier for Cognitive Memory Architecture."""
from __future__ import annotations

import ast
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
JSON_FILES = [
    "memory_type_registry.json",
    "episode_memory_schema.json",
    "experience_memory_schema.json",
    "principle_memory_schema.json",
    "memory_importance_evaluation_contract.json",
    "memory_activation_contract.json",
    "memory_consolidation_contract.json",
    "memory_folding_contract.json",
    "memory_decay_contract.json",
    "self_memory_boundary.json",
    "social_memory_boundary.json",
    "role_memory_boundary.json",
    "field_memory_relation.json",
    "knowledge_memory_boundary.json",
    "ownership_registry.json",
    "dependency_boundary.json",
    "negative_guards.json",
    "summary.json",
]
MD_FILES = [
    "memory_cognitive_architecture.md",
    "memory_hierarchy_model.md",
    "memory_consolidation_model.md",
    "implementation_plan.md",
]
VERIFIER = "verify_memory_cognitive_architecture_v1.py"


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

    types = assets["memory_type_registry.json"]
    memory_types = {"Episode Memory", "Experience Memory", "Principle Memory"}
    check({x["type"] for x in types["types"]} == memory_types, "memory_hierarchy_types")
    check(types["candidate_required"] is True and types["raw_observation_auto_memory"] is False and types["knowledge_auto_memory"] is False, "memory_type_boundary")

    episode = assets["episode_memory_schema.json"]
    required_episode = {"time", "space", "field_ref", "role_ref", "task_ref", "event_sequence", "outcome"}
    check(required_episode <= set(episode["required_binding"]), "episode_bindings")
    check(episode["experience_evaluation_required"] is True and episode["observation_auto_admission"] is False and episode["candidate_only"] is True, "episode_validation")

    experience = assets["experience_memory_schema.json"]
    check(experience["multiple_episodes_required"] is True and experience["minimum_episode_refs"] >= 2 and experience["pattern_candidate_required"] is True, "experience_multiple_episodes")
    check(experience["candidate_only"] is True and experience["direct_role_update"] is False and experience["direct_self_update"] is False, "experience_boundary")

    principle = assets["principle_memory_schema.json"]
    check(principle["long_term_validation_required"] is True and principle["multi_context_validation_required"] is True and principle["rare_generation"] is True, "principle_validation")
    check(principle["candidate_only"] is True and principle["direct_value_update"] is False and principle["fact_assertion"] is False, "principle_boundary")

    importance = assets["memory_importance_evaluation_contract.json"]
    dimensions = {"Field Impact", "Self Impact", "Social Impact", "Role Impact", "Frequency", "Validation Result", "Future Utility"}
    check(set(importance["evaluation_dimensions"]) == dimensions, "importance_dimensions")
    check(importance["candidate_only"] is True and importance["automatic_admission"] is False and importance["unknown_preserved"] is True, "importance_candidate")

    activation = assets["memory_activation_contract.json"]
    check(activation["activation_trigger"] == "current_field_context" and activation["field_activates_memory"] is True, "activation_field_trigger")
    check(activation["autonomous_recall"] is False and activation["context_required"] is True and activation["current_reality_precedence"] is True, "activation_boundary")

    consolidation = assets["memory_consolidation_contract.json"]
    stages = {"experience_evaluation", "validation", "admission", "reinforcement", "decay", "compression", "folding"}
    check(set(consolidation["stages"]) == stages, "consolidation_stages")
    check(set(consolidation["source_required"]) == {"provenance", "time", "field", "confidence", "unknowns"}, "consolidation_provenance")
    check(consolidation["automatic_consolidation"] is False and consolidation["store_before_validation"] is False and consolidation["governance_admission_required"] is True, "consolidation_boundary")

    folding = assets["memory_folding_contract.json"]
    check(folding["minimum_episode_count"] >= 2 and folding["provenance_preserved"] is True and folding["unknown_preserved"] is True, "folding_provenance")
    check(folding["automatic_folding"] is False and folding["fact_assertion"] is False, "folding_boundary")

    decay = assets["memory_decay_contract.json"]
    check(set(decay["factors"]) == {"time_decay", "reinforcement", "context_match", "current_relevance", "validation_status"}, "decay_factors")
    check(decay["decay_reduces_influence"] is True and decay["removed_is_not_deleted"] is True and decay["automatic_deletion"] is False, "decay_boundary")

    self_boundary = assets["self_memory_boundary.json"]
    social_boundary = assets["social_memory_boundary.json"]
    role_boundary = assets["role_memory_boundary.json"]
    check(self_boundary["memory_scope"] == "Self Memory" and self_boundary["direct_self_modification"] is False and self_boundary["identity_write"] is False, "self_memory_boundary")
    check(social_boundary["memory_scope"] == "Social Memory" and social_boundary["direct_social_self_modification"] is False and social_boundary["role_write"] is False, "social_memory_boundary")
    check(role_boundary["memory_scope"] == "Role Memory" and role_boundary["direct_role_activation"] is False and role_boundary["repetition_not_automatic_role"] is True, "role_memory_boundary")

    field_relation = assets["field_memory_relation.json"]
    check(field_relation["field_role"] == "current_reality_context" and field_relation["memory_role"] == "historical_field_experience", "field_memory_roles")
    check(field_relation["memory_overwrites_reality"] is False and field_relation["field_owns_memory"] is False and field_relation["current_reality_precedence"] is True, "field_memory_boundary")

    knowledge = assets["knowledge_memory_boundary.json"]
    check(knowledge["knowledge_is"] == "external_information" and knowledge["memory_is"] == "validated_subject_experience", "knowledge_memory_definition")
    check(knowledge["required_flow"] == ["Knowledge", "Field", "Role", "Task", "Practice", "Experience", "Memory Candidate"], "knowledge_memory_flow")
    check(knowledge["reading_is_experience"] is False and knowledge["knowledge_auto_memory"] is False and knowledge["admission_required"] is True, "knowledge_memory_boundary")

    ownership = assets["ownership_registry.json"]
    owners = [x["owner"] for x in ownership["ownership"]]
    required_owners = {"Information Lifecycle", "Experience Layer", "Memory System", "Self Layer", "Social Self Layer", "Role", "Field", "Knowledge", "Brain", "Runtime"}
    check(ownership["unique_owner_required"] is True and len(owners) == len(set(owners)), "unique_owners")
    check(required_owners <= set(owners), "ownership_coverage")
    check(all(x.get("writer") for x in ownership["ownership"]), "writers_declared")

    dependency = assets["dependency_boundary.json"]
    check(dependency["no_parallel_memory_system"] is True and dependency["runtime_implementation"] is False and dependency["store_implementation"] is False, "dependency_no_parallel_runtime")
    forbidden_dependencies = set(dependency["forbidden_dependencies"])
    check("Memory -> Direct Self Modification" in forbidden_dependencies and "Memory -> Direct Decision Override" in forbidden_dependencies, "dependency_self_decision")
    check("Knowledge -> Automatic Memory" in forbidden_dependencies and "Retrieval -> Reality Replacement" in forbidden_dependencies if "Retrieval -> Reality Replacement" in forbidden_dependencies else "Memory Retrieval -> Reality Replacement" in forbidden_dependencies, "dependency_knowledge_reality")
    check("Pattern -> Fact Assertion" in forbidden_dependencies and "Memory -> Direct Action" in forbidden_dependencies, "dependency_pattern_action")

    guards = assets["negative_guards.json"]
    required_guards = {"memory_runtime", "memory_store", "automatic_compression", "automatic_folding", "model_calls", "database_access", "automatic_learning", "direct_self_modification", "direct_social_self_modification", "direct_role_modification", "direct_decision_override", "knowledge_automatic_memory", "experience_automatic_growth", "retrieval_replaces_reality", "pattern_asserts_fact", "parallel_memory_system"}
    check(required_guards <= set(guards["forbidden"]), "negative_guards")
    check(guards["memory_is_not_database"] is True and guards["memory_is_not_reality"] is True and guards["memory_is_not_decision"] is True, "negative_memory_boundaries")
    check(guards["candidate_only"] is True and guards["current_reality_precedence"] is True and guards["unknown_preserved"] is True and guards["provenance_preserved"] is True, "negative_invariants")
    check(guards["no_check_weaken"] is True and guards["no_hardcoded_pass"] is True, "negative_verifier_guards")

    summary = assets["summary.json"]
    check(summary["status"] == "architecture_only", "summary_status")
    check(summary["readiness_token"] == "LUNA_COGNITIVE_MEMORY_COGNITIVE_ARCHITECTURE_READY", "summary_readiness")
    check(summary["memory_hierarchy"] == ["Episode Memory", "Experience Memory", "Principle Memory"], "summary_hierarchy")
    check(summary["runtime_active"] is False and summary["memory_store"] is False and summary["automatic_learning"] is False and summary["database_access"] is False, "summary_boundary")
    check(len(summary["reusable_assets"]) >= 5 and len(summary["existing_memory_capabilities"]) >= 5 and len(summary["duplicate_risks"]) >= 3 and len(summary["migration_mapping"]) >= 1, "summary_inventory")

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
        print("READINESS: LUNA_COGNITIVE_MEMORY_COGNITIVE_ARCHITECTURE_REMEDIATION_REQUIRED")
        print("NEXT: REMEDIATE_REPORTED_FAILURES_ONLY")
        return 1
    print("FINAL_DECISION: V2_FINAL_VERIFICATION_PASSED")
    print("READINESS: LUNA_COGNITIVE_MEMORY_COGNITIVE_ARCHITECTURE_READY")
    print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
