"""V0 static verifier for Luna Cognitive Self Evolution Architecture.

Planning Only: validates contracts and boundary declarations. It does not
execute Runtime Learning, model training, parameter updates, Emotion Runtime,
Action Runtime, or provider code.
"""

from __future__ import annotations

import ast
import json
import sys
from pathlib import Path


BASE = Path(__file__).resolve().parent
JSON_ASSETS = (
    "experience_consolidation_contract_v1.json",
    "pattern_extraction_contract_v1.json",
    "strategy_evolution_contract_v1.json",
    "capability_growth_contract_v1.json",
    "self_capability_profile_v1.json",
    "limitation_awareness_contract_v1.json",
    "behavior_adaptation_contract_v1.json",
    "evolution_governance_contract_v1.json",
    "experience_lifecycle_v1.json",
    "growth_candidate_schema_v1.json",
    "self_evolution_memory_interface_v1.json",
    "self_evolution_learning_interface_v1.json",
    "self_evolution_capability_interface_v1.json",
    "self_evolution_dependency_boundary_v1.json",
)
MD_ASSETS = (
    "luna_self_evolution_architecture_v1.md",
    "self_evolution_whitebox_v1.md",
    "self_evolution_go_no_go_v1.md",
)


def main() -> int:
    failures: list[str] = []
    checks = 0

    def check(condition: bool, name: str) -> None:
        nonlocal checks
        checks += 1
        if not condition:
            failures.append(name)

    data: dict[str, dict] = {}
    for name in JSON_ASSETS:
        path = BASE / name
        check(path.is_file(), f"missing_json:{name}")
        if path.is_file():
            try:
                data[name] = json.loads(path.read_text(encoding="utf-8"))
                check(True, f"json_parse:{name}")
            except (OSError, json.JSONDecodeError):
                check(False, f"json_parse:{name}")
    for name in MD_ASSETS:
        path = BASE / name
        check(path.is_file(), f"missing_md:{name}")
        if path.is_file():
            check(bool(path.read_text(encoding="utf-8", errors="replace").strip()), f"nonempty_md:{name}")

    consolidation = data.get("experience_consolidation_contract_v1.json", {})
    pattern = data.get("pattern_extraction_contract_v1.json", {})
    strategy = data.get("strategy_evolution_contract_v1.json", {})
    growth = data.get("capability_growth_contract_v1.json", {})
    profile = data.get("self_capability_profile_v1.json", {})
    limitation = data.get("limitation_awareness_contract_v1.json", {})
    behavior = data.get("behavior_adaptation_contract_v1.json", {})
    governance = data.get("evolution_governance_contract_v1.json", {})
    lifecycle = data.get("experience_lifecycle_v1.json", {})
    candidate = data.get("growth_candidate_schema_v1.json", {})
    memory = data.get("self_evolution_memory_interface_v1.json", {})
    learning = data.get("self_evolution_learning_interface_v1.json", {})
    capability = data.get("self_evolution_capability_interface_v1.json", {})
    boundary = data.get("self_evolution_dependency_boundary_v1.json", {})

    check({"Action Outcome", "Expectation Difference", "Feedback"}.issubset(set(consolidation.get("inputs", []))), "consolidation_inputs")
    check(consolidation.get("output") == "Experience Candidate", "consolidation_output")
    check({"experience_id", "context", "task", "outcome", "difference", "confidence", "reuse_candidate"}.issubset(set(consolidation.get("schema", []))), "consolidation_schema")
    check(consolidation.get("rules", {}).get("experience_is_not_fact") is True, "experience_not_fact")
    check(consolidation.get("rules", {}).get("candidate_only") is True, "experience_candidate_only")

    check("Repeated Evidence" in pattern.get("inputs", []), "pattern_repeated_evidence")
    check(pattern.get("output") == "Pattern Candidate", "pattern_output")
    check(pattern.get("rules", {}).get("single_episode_not_sufficient") is True, "pattern_not_single_episode")
    check(pattern.get("rules", {}).get("pattern_is_not_rule") is True, "pattern_not_rule")
    check(pattern.get("rules", {}).get("candidate_only") is True, "pattern_candidate_only")

    check(pattern.get("output") in strategy.get("inputs", []), "pattern_strategy_link")
    check(strategy.get("output") == "Strategy Candidate", "strategy_output")
    check(strategy.get("rules", {}).get("automatic_behavior_forbidden") is True, "strategy_no_automatic_behavior")
    check(strategy.get("rules", {}).get("review_required_before_adoption") is True, "strategy_review")

    check({"Performance Evidence", "Outcome Evidence", "Failure Attribution"}.issubset(set(growth.get("inputs", []))), "growth_inputs")
    check(growth.get("output") == "Capability Growth Candidate", "growth_output")
    check(growth.get("rules", {}).get("context_bound") is True, "growth_context_bound")
    check(growth.get("rules", {}).get("no_model_parameter_update") is True, "growth_no_parameter_update")
    check(growth.get("rules", {}).get("no_automatic_upgrade") is True, "growth_no_auto_upgrade")

    check({"Perception", "Field Understanding", "Task Execution", "Adaptation", "Information Seeking", "Reliability"}.issubset(set(profile.get("dimensions", []))), "profile_dimensions")
    check({"capability", "context", "condition", "experience_count", "success_rate", "confidence", "limitation", "growth_direction"}.issubset(set(profile.get("schema", []))), "profile_schema")
    check(profile.get("profile_rules", {}).get("context_bound") is True, "profile_context_bound")
    check(profile.get("profile_rules", {}).get("no_single_global_score") is True, "profile_no_single_score")
    check(profile.get("profile_rules", {}).get("identity_separate") is True, "profile_identity_separate")
    check(profile.get("profile_rules", {}).get("unknown_first_class") is True, "profile_unknown")

    check({"Unknown", "Failure Pattern", "Low Confidence", "Boundary"}.issubset(set(limitation.get("inputs", []))), "limitation_inputs")
    check(limitation.get("rules", {}).get("limitation_not_identity") is True, "limitation_not_identity")
    check(limitation.get("rules", {}).get("uncertainty_is_explicit") is True, "limitation_uncertainty")
    check(limitation.get("rules", {}).get("review_required") is True, "limitation_review")

    check("Strategy Candidate" in behavior.get("inputs", []), "behavior_strategy_input")
    check(behavior.get("output") == "Behavior Adaptation Candidate", "behavior_output")
    check(behavior.get("rules", {}).get("strategy_not_action") is True, "behavior_not_action")
    check(behavior.get("rules", {}).get("personality_change_forbidden") is True, "behavior_no_personality_change")
    check(behavior.get("rules", {}).get("action_runtime_not_invoked") is True, "behavior_no_action_runtime")

    check(governance.get("adoption_pipeline") == ["Candidate", "Evidence", "Confidence", "Review", "Adoption"], "governance_pipeline")
    forbidden_targets = set(governance.get("forbidden_targets", []))
    check({"Constitution", "Value", "Identity", "Goal", "Reality", "Emotion Runtime", "Model Parameters"}.issubset(forbidden_targets), "governance_forbidden_targets")
    check(governance.get("rules", {}).get("candidate_admission_required") is True, "governance_admission")
    check(governance.get("rules", {}).get("automatic_adoption_forbidden") is True, "governance_no_auto_adoption")
    check(governance.get("rules", {}).get("revocation_supported") is True, "governance_revocation")

    states = set(lifecycle.get("states", []))
    check({"Observed", "Candidate", "Evaluated", "Retained", "Pattern Linked", "Contradicted", "Deprecated", "Archived"}.issubset(states), "experience_lifecycle_states")
    check({"experience_id", "state", "created_at", "updated_at", "source_trace", "owner", "confidence"}.issubset(set(lifecycle.get("schema", []))), "experience_lifecycle_schema")
    check(len(lifecycle.get("transitions", [])) >= 6, "experience_lifecycle_transitions")
    check(lifecycle.get("rules", {}).get("current_reality_can_contradict") is True, "experience_reality_contradiction")
    check(lifecycle.get("rules", {}).get("history_preserved") is True, "experience_history_preserved")

    check({"Pattern", "Strategy", "Capability Growth", "Limitation Awareness", "Behavior Adaptation", "Attention Adjustment"}.issubset(set(candidate.get("candidate_types", []))), "candidate_types")
    check({"Candidate", "Under Review", "Admitted", "Rejected", "Revoked", "Archived"}.issubset(set(candidate.get("review_statuses", []))), "candidate_statuses")
    check(candidate.get("rules", {}).get("candidate_is_not_adoption") is True, "candidate_not_adoption")
    check(candidate.get("rules", {}).get("reversible_required") is True, "candidate_reversible")

    check("Retained Experience" in memory.get("inputs", []), "memory_input")
    check("Pattern Candidate" in memory.get("outputs", []), "memory_output")
    check(memory.get("rules", {}).get("memory_remains_owner_of_records") is True, "memory_owner")
    check(memory.get("rules", {}).get("self_evolution_does_not_rewrite_memory") is True, "memory_no_rewrite")

    check("Learning Signal" in learning.get("inputs", []), "learning_signal_input")
    check({"Strategy Candidate", "Capability Growth Candidate", "Behavior Adaptation Candidate"}.issubset(set(learning.get("outputs", []))), "learning_outputs")
    check(learning.get("rules", {}).get("learning_does_not_auto_adopt") is True, "learning_no_auto_adopt")
    check(learning.get("rules", {}).get("parameter_update_forbidden") is True, "learning_no_parameters")

    check("Performance Evidence" in capability.get("inputs", []), "capability_performance_input")
    check("Capability Growth Candidate" in capability.get("outputs", []), "capability_growth_output")
    check(capability.get("rules", {}).get("provider_is_evidence_source_only") is True, "capability_provider_boundary")
    check(capability.get("rules", {}).get("profile_update_requires_admission") is True, "capability_profile_admission")
    check(capability.get("rules", {}).get("identity_is_not_modified") is True, "capability_identity_boundary")

    forbidden = set(boundary.get("forbidden", []))
    for item in (
        "Self Evolution → Constitution",
        "Self Evolution → Value Rewrite",
        "Self Evolution → Identity Rewrite",
        "Self Evolution → Goal Rewrite",
        "Self Evolution → Automatic Model Training",
        "Self Evolution → Model Parameter Update",
        "Self Evolution → Emotion Control",
        "Self Evolution → Direct Reality Mutation",
        "Self Evolution → Direct Action",
    ):
        check(item in forbidden, f"dependency_guard:{item}")
    check(len(boundary.get("allowed", [])) >= 6, "dependency_allowed_edges")
    check(boundary.get("rules", {}).get("candidate_review_boundary") is True, "dependency_review_boundary")
    check(boundary.get("rules", {}).get("reality_priority") is True, "dependency_reality_priority")
    check(boundary.get("rules", {}).get("no_runtime_learning") is True, "dependency_no_runtime_learning")
    check(boundary.get("rules", {}).get("no_emotion_runtime") is True, "dependency_no_emotion_runtime")

    verifier_text = Path(__file__).read_text(encoding="utf-8")
    verifier_ast = ast.parse(verifier_text, filename=str(Path(__file__)))
    imports: set[str] = set()
    for node in ast.walk(verifier_ast):
        if isinstance(node, ast.Import):
            imports.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module.split(".")[0])
    check(not imports.intersection({"subprocess", "socket", "requests", "cv2", "torch"}), "planning_no_runtime_import")
    forbidden_runtime_modules = {"runtime_learning", "online_learning", "model_training", "parameter_update"}
    check(not any(name in forbidden_runtime_modules for name in imports), "verifier_no_runtime_learning_import")
    compile(verifier_text, str(Path(__file__)), "exec")
    check(True, "planning_verifier_compile")

    passed = checks - len(failures)
    print(f"CHECKS: {checks}")
    print(f"FAILED_CHECKS: {failures}")
    print(f"PASSED_CHECK_COUNT: {passed}")
    print(f"FAILED_CHECK_COUNT: {len(failures)}")
    print(f"BLOCKER_COUNT: {len(failures)}")
    if failures:
        print("FINAL_DECISION: BLOCKED_BY_VERIFIER_FAILURE")
        print("READINESS: LUNA_SELF_EVOLUTION_REMEDIATION_REQUIRED")
        print("NEXT: REMEDIATE_REPORTED_FAILURES_ONLY")
        return 1
    print("FINAL_DECISION: V2_FINAL_VERIFICATION_PASSED")
    print("READINESS: LUNA_SELF_EVOLUTION_ARCHITECTURE_READY")
    print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT")
    return 0


if __name__ == "__main__":
    sys.exit(main())
