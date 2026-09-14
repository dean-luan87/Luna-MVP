"""V0 static contract verifier for Selective Learning Architecture."""
from __future__ import annotations

import ast
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
JSON_FILES = [
    "learning_candidate_schema.json", "learning_source_registry.json",
    "learning_utility_contract.json", "learning_admission_contract.json",
    "experience_learning_relation.json", "knowledge_learning_relation.json",
    "memory_learning_relation.json", "schema_learning_relation.json",
    "capability_growth_contract.json", "self_evolution_boundary.json",
    "learning_lifecycle_contract.json", "ownership_registry.json",
    "dependency_boundary.json", "negative_guards.json", "summary.json",
]
MD_FILES = [
    "selective_learning_architecture.md", "learning_candidate_model.md",
    "learning_governance_model.md", "capability_growth_model.md",
    "implementation_plan.md",
]
VERIFIER = "verify_selective_learning_architecture_v1.py"


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

    candidate = assets["learning_candidate_schema.json"]
    required_fields = {"candidate_id", "source", "field_ref", "role_ref", "task_ref", "gap", "evidence", "expected_capability_gain", "future_decision_improvement", "learning_cost", "risk", "utility_candidate", "target_level", "provenance", "unknowns"}
    check(required_fields <= set(candidate["required"]), "candidate_fields")
    check(candidate["candidate_only"] is True and candidate["self_review_required"] is True and candidate["automatic_learning"] is False and candidate["model_training"] is False and candidate["parameter_update"] is False and candidate["automatic_memory_write"] is False and candidate["automatic_schema_update"] is False, "candidate_boundary")

    source = assets["learning_source_registry.json"]
    sources = ["Experience Learning", "Knowledge Assimilation", "Social Learning", "Self Reflection Learning"]
    check(source["sources"] == sources and source["source_is_provenance_not_authority"] is True and source["field_context_required"] is True and source["experience_or_application_required"] is True and source["knowledge_reading_alone_is_learning"] is False and source["candidate_only"] is True, "source_boundary")

    utility = assets["learning_utility_contract.json"]
    check(set(utility["inputs"]) == {"Expected Capability Gain", "Future Decision Improvement", "Learning Cost", "Risk", "Evidence Quality", "Reversibility", "Unknowns"}, "utility_inputs")
    check(utility["formula"] == "Expected Capability Gain + Future Decision Improvement - Learning Cost - Risk" and utility["hard_constraint_check_required"] is True and utility["calculation_implemented"] is False and utility["candidate_only"] is True and utility["utility_does_not_admit_learning"] is True and utility["utility_does_not_modify_capability"] is True, "utility_boundary")

    admission = assets["learning_admission_contract.json"]
    review = {"Evidence Quality", "Utility", "Cost", "Risk", "Reversibility", "Capability Relevance", "Constitution Compliance", "Self Boundary", "Unknown Preservation"}
    check(set(admission["review_criteria"]) == review and set(admission["outputs"]) == {"Approved Growth Candidate", "Rejected Learning Candidate", "Deferred Learning Candidate", "Revised Learning Candidate"}, "admission_scope")
    check(admission["admission_required"] is True and admission["self_review_required"] is True and admission["capability_governance_required"] is True and admission["automatic_admission"] is False and admission["automatic_learning"] is False and admission["revocation_supported"] is True and admission["candidate_only"] is True, "admission_boundary")

    experience = assets["experience_learning_relation.json"]
    check(experience["flow"] == ["Reality Outcome", "Experience", "Pattern Detection", "Learning Candidate", "Utility Evaluation", "Self Approval"], "experience_flow")
    check(experience["experience_is_learning"] is False and experience["experience_is_source"] is True and experience["repetition_or_impact_required"] is True and experience["outcome_evidence_required"] is True and experience["single_event_auto_learning"] is False and experience["candidate_only"] is True, "experience_boundary")

    knowledge = assets["knowledge_learning_relation.json"]
    check(knowledge["flow"] == ["Admitted Knowledge", "Field Contextualization", "Role/Task Application", "Interaction", "Outcome Evidence", "Experience Candidate", "Learning Candidate"], "knowledge_flow")
    check(knowledge["knowledge_is_learning"] is False and knowledge["reading_alone_is_insufficient"] is True and knowledge["knowledge_admission_required"] is True and knowledge["field_role_task_required"] is True and knowledge["application_or_interaction_required"] is True and knowledge["knowledge_does_not_modify_capability_directly"] is True and knowledge["candidate_only"] is True, "knowledge_boundary")

    memory = assets["memory_learning_relation.json"]
    check(memory["flow"] == ["Memory", "Pattern", "Schema", "Learning Candidate", "Self Review"], "memory_flow")
    check(memory["memory_is_learning"] is False and memory["memory_creates_learning_automatically"] is False and memory["memory_direct_capability_change"] is False and memory["memory_direct_self_change"] is False and memory["current_reality_precedence"] is True and memory["candidate_only"] is True, "memory_boundary")
    schema = assets["schema_learning_relation.json"]
    check(schema["flow"] == ["Schema", "Capability Gap Context", "Learning Candidate", "Self Review"], "schema_flow")
    check(schema["schema_is_learning"] is False and schema["schema_creates_learning_automatically"] is False and schema["schema_direct_capability_change"] is False and schema["schema_direct_goal_change"] is False and schema["repeated_pattern_required"] is True and schema["candidate_only"] is True, "schema_boundary")

    growth = assets["capability_growth_contract.json"]
    levels = ["Level 0 Temporary Information", "Level 1 Experience Pattern", "Level 2 Capability Improvement", "Level 3 Self Evolution Candidate"]
    check(growth["growth_levels"] == levels and set(growth["mutable_targets"]) == {"Capability", "Strategy", "Schema", "Capability Confidence"} and set(growth["protected_targets"]) == {"Constitution", "Identity", "Safety Boundary", "Core Brain Rules"}, "growth_scope")
    check(growth["automatic_capability_change"] is False and growth["parameter_update"] is False and growth["model_training"] is False and growth["capability_governance_required"] is True and growth["candidate_only"] is True, "growth_boundary")

    evolution = assets["self_evolution_boundary.json"]
    check(evolution["self_evolution_role"] == "review and govern long-term growth candidates" and set(evolution["protected"]) == {"Constitution", "Identity", "Safety Boundary"}, "evolution_owner")
    check(evolution["self_review_required"] is True and evolution["automatic_self_modification"] is False and evolution["direct_identity_change"] is False and evolution["direct_constitution_change"] is False and evolution["emotion_runtime"] is False and evolution["candidate_only"] is True, "evolution_boundary")

    lifecycle = assets["learning_lifecycle_contract.json"]
    states = ["Detected", "Candidate", "Evaluated", "Admitted", "Applied Candidate", "Validated", "Growth Candidate", "Rejected", "Deferred", "Archived"]
    check(lifecycle["states"] == states and lifecycle["automatic_transition"] is False and lifecycle["admission_required"] is True and lifecycle["validation_required"] is True and lifecycle["revocation_supported"] is True and lifecycle["rollback_supported"] is True and lifecycle["learning_runtime"] is False and lifecycle["automatic_learning"] is False and lifecycle["candidate_only"] is True, "lifecycle_boundary")

    ownership = assets["ownership_registry.json"]
    owners = [x["owner"] for x in ownership["ownership"]]
    required_owners = {"Experience", "Knowledge", "Memory", "Schema", "Learning", "Self", "Self Evolution", "Capability Governance", "Value Utility", "Constitution", "Field", "Social Self"}
    check(ownership["unique_owner_required"] is True and len(owners) == len(set(owners)), "unique_owners")
    check(required_owners <= set(owners), "ownership_coverage")
    check(all(x.get("writer") and x.get("reader") for x in ownership["ownership"]), "ownership_writer_reader")

    dependency = assets["dependency_boundary.json"]
    required_forbidden = {"Knowledge -> Direct Capability Change", "Memory -> Automatic Learning", "Schema -> Automatic Learning", "Experience -> Automatic Self Modification", "Learning -> Direct Memory Write", "Learning -> Direct Schema Update", "Learning -> Direct Identity Change", "Learning -> Direct Constitution Change", "Learning -> Model Parameter Update", "Learning -> Model Training", "Learning -> Execute Action", "B Route -> Direct Self Modification", "Emotion -> Direct Learning Adoption", "Provider -> Learning Authority"}
    check(required_forbidden <= set(dependency["forbidden_dependencies"]), "dependency_forbidden")
    check(dependency["no_learning_runtime"] is True and dependency["no_automatic_learning"] is True and dependency["no_model_training"] is True and dependency["no_parameter_update"] is True and dependency["no_automatic_memory_write"] is True and dependency["no_automatic_schema_update"] is True and dependency["no_emotion_runtime"] is True and dependency["no_b_route_runtime"] is True, "dependency_boundary")

    guards = assets["negative_guards.json"]
    required_guards = {"learning_runtime", "automatic_learning", "model_training", "parameter_update", "automatic_memory_write", "automatic_schema_update", "emotion_runtime", "b_route_runtime", "knowledge_direct_capability_change", "knowledge_direct_self_modification", "memory_automatic_learning", "schema_automatic_learning", "experience_automatic_self_modification", "learning_direct_memory_write", "learning_direct_schema_update", "learning_direct_identity_change", "learning_direct_constitution_change", "learning_direct_goal_change", "learning_model_parameter_update", "learning_execute_action", "b_route_direct_self_modification", "emotion_direct_learning_adoption", "provider_learning_authority", "runtime_learning_authority", "model_calls", "provider_calls", "hardware_control", "no_check_weaken", "no_hardcoded_pass"}
    check(required_guards <= set(guards["forbidden"]), "negative_guards")
    check(guards["knowledge_is_not_learning"] is True and guards["memory_is_not_learning"] is True and guards["experience_is_not_learning"] is True and guards["candidate_only"] is True and guards["self_review_required"] is True and guards["hard_constraints_preserved"] is True and guards["unknowns_preserved"] is True, "negative_invariants")

    summary = assets["summary.json"]
    check(summary["status"] == "architecture_only" and summary["readiness_token"] == "LUNA_COGNITIVE_SELECTIVE_LEARNING_ARCHITECTURE_READY", "summary_status")
    check(summary["canonical_flow"] == ["Reality", "Experience", "Pattern Detection", "Learning Candidate", "Utility Evaluation", "Self Approval", "Schema Update", "Capability Growth"], "summary_flow")
    check(summary["sources"] == sources and summary["levels"] == levels, "summary_taxonomy")
    check(summary["runtime"] is False and summary["learning_runtime"] is False and summary["automatic_learning"] is False and summary["model_training"] is False and summary["parameter_update"] is False and summary["automatic_memory_write"] is False and summary["automatic_schema_update"] is False and summary["emotion_runtime"] is False and summary["b_route_runtime"] is False, "summary_boundary")
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
        print("READINESS: LUNA_COGNITIVE_SELECTIVE_LEARNING_ARCHITECTURE_REMEDIATION_REQUIRED")
        print("NEXT: REMEDIATE_REPORTED_FAILURES_ONLY")
        return 1
    print("FINAL_DECISION: V2_FINAL_VERIFICATION_PASSED")
    print("READINESS: LUNA_COGNITIVE_SELECTIVE_LEARNING_ARCHITECTURE_READY")
    print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
