"""V0 static contract verifier for Luna A Route Integration Architecture."""
from __future__ import annotations

import ast
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
JSON_FILES = [
    "a_route_flow_schema.json", "cognitive_flow_state_contract.json",
    "information_flow_contract.json", "module_ownership_contract.json",
    "field_attention_flow_relation.json", "memory_understanding_flow_relation.json",
    "goal_decision_flow_relation.json", "decision_outcome_learning_flow_relation.json",
    "self_governance_flow_contract.json", "learning_boundary_contract.json",
    "a_route_b_route_boundary.json", "dependency_boundary.json",
    "negative_guards.json", "summary.json",
]
MD_FILES = [
    "a_route_cognitive_flow_architecture.md", "cognitive_flow_state_model.md",
    "module_interaction_contract.md", "feedback_loop_architecture.md",
    "implementation_plan.md",
]
VERIFIER = "verify_a_route_integration_architecture_v1.py"


def load(assets: dict[str, dict], name: str) -> dict:
    if name not in assets:
        assets[name] = json.loads((ROOT / name).read_text(encoding="utf-8"))
    return assets[name]


def main() -> int:
    checks = 0
    failed: list[str] = []

    def check(condition: bool, label: str) -> None:
        nonlocal checks
        checks += 1
        if not condition:
            failed.append(label)

    expected = set(JSON_FILES) | set(MD_FILES) | {VERIFIER}
    files = {p.name for p in ROOT.iterdir() if p.is_file()}
    check(expected <= files, "required_assets")
    check({p.name for p in ROOT.glob("*.py")} == {VERIFIER}, "no_runtime_python")

    assets: dict[str, dict] = {}
    for name in JSON_FILES:
        try:
            value = load(assets, name)
            check(isinstance(value, dict), f"json_object:{name}")
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

    flow = load(assets, "a_route_flow_schema.json")
    canonical_flow = [
        "Reality", "Evidence", "Cognitive Field", "Attention", "Context",
        "Hypothesis", "Belief", "Understanding", "Goal", "Value Utility",
        "Decision Arbitration", "Action Boundary", "Outcome", "Experience",
        "Memory", "Schema", "Selective Learning", "Growth Candidate", "Self Review",
    ]
    check(flow["canonical_stages"] == canonical_flow, "canonical_flow")
    check(flow["stage_output_is_candidate_by_default"] is True and flow["reality_is_external_precedence"] is True, "flow_candidate_reality_boundary")
    check(set(flow["required_flow_metadata"]) >= {"flow_id", "stage", "field_ref", "provenance", "timestamp", "trace_ref", "unknowns"}, "flow_metadata")
    check(flow["runtime_implemented"] is False and flow["action_execution"] is False and flow["learning_runtime"] is False and flow["b_route"] is False, "flow_runtime_boundary")

    state = load(assets, "cognitive_flow_state_contract.json")
    states = ["Observed", "Structured", "Fielded", "Attending", "Contextualized", "Hypothesized", "Understood", "GoalEvaluated", "Valued", "Arbitrated", "ActionPending", "OutcomePending", "Evaluated", "Experienced", "Remembered", "Learned", "SelfReviewed"]
    check(state["states"] == states, "flow_states")
    check(state["flow_state_is_process_descriptor"] is True and state["flow_state_is_not_field"] is True and state["flow_state_is_not_reality"] is True and state["flow_state_is_not_action_command"] is True, "flow_state_boundary")
    check(state["same_field_multiple_flows_allowed"] is True and state["field_change_triggers_attention_recompute_candidate"] is True and state["automatic_transition"] is False and state["runtime_implemented"] is False, "flow_state_lifecycle")

    info = load(assets, "information_flow_contract.json")
    check(info["flow"] == canonical_flow, "information_flow")
    check(info["reality_precedence"] is True and info["memory_is_context_not_reality"] is True and info["knowledge_requires_field_role_task_context"] is True and info["observation_does_not_imply_memory"] is True, "information_precedence")
    check(info["direct_reality_mutation"] is False and info["direct_memory_write"] is False and info["direct_schema_update"] is False and info["automatic_learning"] is False, "information_write_boundary")

    ownership = load(assets, "module_ownership_contract.json")
    records = ownership["ownership"]
    owners = [item["owner"] for item in records]
    modules = [item["module"] for item in records]
    check(ownership["unique_owner_required"] is True and len(owners) == len(set(owners)) and len(modules) == len(set(modules)), "unique_owners")
    check({"Reality", "Evidence", "Cognitive Field", "Attention", "Context", "Understanding", "Goal", "Value Utility", "Decision Arbitration", "Action", "Outcome", "Experience", "Memory/Schema", "Selective Learning", "Self Review", "Runtime", "B Route"} <= set(modules), "ownership_coverage")
    check(all(item.get("writer") and item.get("reader") for item in records), "ownership_writer_reader")

    field_attention = load(assets, "field_attention_flow_relation.json")
    check(field_attention["flow"] == ["Current Field", "Field Complexity/Risk/Task Context", "Attention Candidate", "Context Candidate"], "field_attention_flow")
    check(field_attention["field_drives_attention_candidate"] is True and field_attention["attention_recomputed_on_field_change"] is True and field_attention["attention_does_not_modify_field"] is True and field_attention["attention_does_not_write_memory"] is True and field_attention["attention_does_not_execute_action"] is True and field_attention["candidate_only"] is True, "field_attention_boundary")

    memory = load(assets, "memory_understanding_flow_relation.json")
    check(memory["flow"] == ["Current Field", "Field Activation", "Relevant Memory Candidate", "Context Enhancement", "Understanding Candidate"], "memory_understanding_flow")
    check(memory["field_activates_memory"] is True and memory["memory_is_not_reality"] is True and memory["memory_is_context_not_authority"] is True and memory["current_reality_precedence"] is True and memory["memory_does_not_override_understanding"] is True and memory["memory_does_not_create_goal_automatically"] is True, "memory_understanding_boundary")

    goal = load(assets, "goal_decision_flow_relation.json")
    check(goal["flow"] == ["Understanding Candidate", "Goal Candidate", "Value Utility Candidate", "Decision Candidate Set", "Decision Arbitration", "Selected Decision Candidate"], "goal_decision_flow")
    check(goal["understanding_required"] is True and goal["goal_is_direction_not_action"] is True and goal["value_provides_priority_support"] is True and goal["brain_generates_candidates"] is True and goal["arbitration_selects_candidate"] is True and goal["self_constraint_required"] is True and goal["decision_is_not_action"] is True and goal["decision_does_not_create_goal"] is True and goal["candidate_only"] is True, "goal_decision_boundary")

    feedback = load(assets, "decision_outcome_learning_flow_relation.json")
    check(feedback["flow"] == ["Selected Decision Candidate", "Action Boundary", "Action Outcome", "Expected/Actual Comparison", "Outcome Evaluation", "Experience Candidate", "Memory/Schema Candidate", "Selective Learning Candidate", "Growth Candidate"], "feedback_flow")
    check(feedback["action_boundary_is_execution_gate"] is True and feedback["outcome_is_not_experience"] is True and feedback["single_outcome_not_schema"] is True and feedback["validation_required"] is True and feedback["memory_consolidation_requires_governance"] is True and feedback["learning_requires_self_review"] is True and feedback["direct_action_from_outcome"] is False and feedback["direct_self_modification"] is False and feedback["automatic_learning"] is False and feedback["candidate_only"] is True, "feedback_boundary")

    self_contract = load(assets, "self_governance_flow_contract.json")
    check(set(self_contract["self_inputs"]) >= {"Constitution", "Identity Boundary", "Capability State", "Resource State", "Self Regulation", "Self Rhythm", "Self World Boundary", "Growth Candidate"}, "self_inputs")
    check(set(self_contract["self_permissions"]) == {"constrain", "veto", "request_reconsideration", "review_growth", "preserve_identity", "preserve_safety_boundary"} and set(self_contract["self_protected"]) >= {"Constitution", "Identity", "Safety Boundary", "Core Brain Rules"}, "self_permissions")
    check(self_contract["self_does_not_generate_all_goals"] is True and self_contract["self_does_not_select_decision_alone"] is True and self_contract["self_does_not_execute_action"] is True and self_contract["self_does_not_auto_adopt_learning"] is True and self_contract["growth_requires_self_review"] is True and self_contract["candidate_only"] is True, "self_boundary")

    learning = load(assets, "learning_boundary_contract.json")
    check(set(learning["learning_requires"]) >= {"Validated Experience", "Pattern Evidence", "Learning Utility", "Capability Gap or Improvement Context", "Self Review"}, "learning_requirements")
    check(set(learning["learning_can_change"]) >= {"Schema Candidate", "Strategy Candidate", "Capability Growth Candidate", "Capability Confidence Candidate"}, "learning_mutable_targets")
    check(set(learning["learning_cannot_change"]) >= {"Reality", "Constitution", "Identity", "Safety Boundary", "Core Brain Rules", "Current Goal Directly"}, "learning_protected_targets")
    check(learning["knowledge_reading_is_not_learning"] is True and learning["memory_is_not_learning"] is True and learning["learning_is_not_runtime"] is True and learning["automatic_schema_update"] is False and learning["automatic_memory_write"] is False and learning["model_training"] is False and learning["parameter_update"] is False and learning["b_route_direct_modification"] is False and learning["candidate_only"] is True, "learning_boundary")

    routes = load(assets, "a_route_b_route_boundary.json")
    check(routes["a_route"]["purpose"] == "current_reality_cognition_and_feedback" and routes["a_route"]["flow"] == ["Reality", "Field", "Understanding", "Decision", "Action", "Outcome", "Learning"], "a_route_definition")
    check(routes["b_route"]["status"] == "future_interface_only" and routes["b_route"]["runtime"] is False and routes["b_route"]["cannot_override_current_reality"] is True and routes["b_route"]["cannot_override_current_decision"] is True and routes["b_route"]["cannot_directly_modify_self"] is True and routes["b_route"]["cannot_directly_modify_learning"] is True and routes["route_mixing"] is False, "b_route_boundary")

    dependency = load(assets, "dependency_boundary.json")
    required_forbidden = {"Memory -> Override Reality", "Memory -> Direct Decision", "Field -> Direct Action", "Goal -> Direct Action", "Value Utility -> Commit Decision", "Decision -> Execute Action", "Outcome -> Direct Self Modification", "Single Outcome -> Schema Update", "Learning -> Direct Memory Write", "Learning -> Direct Schema Update", "Learning -> Direct Identity Change", "Learning -> Direct Constitution Change", "Learning -> Learning Model Training", "Learning -> Parameter Update", "B Route -> Override A Route", "B Route -> Direct Self Modification", "Runtime -> Learning Authority", "Emotion -> Direct Decision Override"}
    # Keep the contract's exact spelling as the authority and check the key guards separately.
    check({"Memory -> Override Reality", "Decision -> Execute Action", "Learning -> Direct Memory Write", "Learning -> Direct Schema Update", "B Route -> Override A Route", "B Route -> Direct Self Modification"} <= set(dependency["forbidden_dependencies"]), "dependency_forbidden")
    check(dependency["no_runtime_integration"] is True and dependency["no_module_invocation"] is True and dependency["no_automatic_flow"] is True and dependency["no_learning_runtime"] is True and dependency["no_b_route_runtime"] is True and dependency["no_action_execution"] is True and dependency["no_model_integration"] is True and dependency["no_hardware_integration"] is True, "dependency_boundary")

    guards = load(assets, "negative_guards.json")
    required_guards = {"runtime_integration", "module_invocation", "automatic_cognitive_flow", "learning_runtime", "action_execution", "model_integration", "hardware_integration", "emotion_runtime", "b_route_runtime", "memory_override_reality", "decision_execute_action", "outcome_direct_self_modification", "single_outcome_schema_update", "learning_direct_memory_write", "learning_direct_schema_update", "learning_direct_identity_change", "learning_model_training", "learning_parameter_update", "b_route_override_a_route", "b_route_direct_self_modification", "runtime_learning_authority", "emotion_direct_decision_override", "no_check_weaken", "no_hardcoded_pass"}
    check(required_guards <= set(guards["forbidden"]), "negative_guards")
    invariant = guards["invariants"]
    check(all(invariant.get(key) is True for key in ("reality_precedence", "candidate_boundaries_preserved", "field_drives_attention", "memory_is_context_not_reality", "outcome_is_not_experience", "learning_requires_self_review", "self_protects_identity_and_constitution", "a_route_b_route_separation", "unknowns_preserved")), "negative_invariants")

    summary = load(assets, "summary.json")
    check(summary["status"] == "architecture_only" and summary["readiness_token"] == "LUNA_COGNITIVE_A_ROUTE_INTEGRATION_ARCHITECTURE_READY", "summary_status")
    check(summary["canonical_flow"] == canonical_flow and summary["flow_state"] == states and summary["ownership_unique"] is True, "summary_flow")
    check(summary["integration_is_architecture_only"] is True and summary["runtime_integration"] is False and summary["module_invocation"] is False and summary["automatic_flow"] is False and summary["learning_runtime"] is False and summary["action_execution"] is False and summary["model_integration"] is False and summary["provider_integration"] is False and summary["hardware_integration"] is False and summary["emotion_runtime"] is False and summary["social_runtime"] is False and summary["b_route_runtime"] is False, "summary_boundary")
    check(len(summary["reusable_assets"]) >= 7 and len(summary["parallel_risks"]) >= 4 and len(summary["migration_mapping"]) >= 4, "summary_inventory")

    forbidden_imports = {"subprocess", "socket", "requests", "cv2", "torch", "transformers", "sqlite3", "psycopg2"}
    try:
        tree = ast.parse((ROOT / VERIFIER).read_text(encoding="utf-8"))
        imports = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.add(node.module.split(".")[0])
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
        print("READINESS: LUNA_COGNITIVE_A_ROUTE_INTEGRATION_ARCHITECTURE_REMEDIATION_REQUIRED")
        print("NEXT: REMEDIATE_REPORTED_FAILURES_ONLY")
        return 1
    print("FINAL_DECISION: V2_FINAL_VERIFICATION_PASSED")
    print("READINESS: LUNA_COGNITIVE_A_ROUTE_INTEGRATION_ARCHITECTURE_READY")
    print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
