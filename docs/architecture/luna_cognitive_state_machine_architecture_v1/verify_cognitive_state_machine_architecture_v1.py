"""V0 static contract verifier for Cognitive State Machine Architecture."""
from __future__ import annotations

import ast
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
JSON_FILES = [
    "cognitive_state_schema.json", "state_type_registry.json",
    "state_transition_contract.json", "state_entry_exit_contract.json",
    "state_attention_relation.json", "state_memory_relation.json",
    "state_decision_relation.json", "state_learning_relation.json",
    "state_self_boundary.json", "a_route_state_flow.json",
    "b_route_state_boundary.json", "ownership_registry.json",
    "dependency_boundary.json", "negative_guards.json", "summary.json",
]
MD_FILES = [
    "cognitive_state_machine_architecture.md", "state_transition_model.md",
    "state_attention_relation.md", "state_feedback_relation.md",
    "implementation_plan.md",
]
VERIFIER = "verify_cognitive_state_machine_architecture_v1.py"
STATES = ["Observation", "Understanding", "Decision", "Action", "Reflection", "Learning"]
CYCLE = ["Observation", "Understanding", "Decision", "Action", "Reflection", "Learning", "Observation"]


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

    schema = load(assets, "cognitive_state_schema.json")
    check(schema["states"] == STATES, "state_types")
    check(set(schema["required_fields"]) >= {"state_id", "state_type", "field_ref", "flow_ref", "entry_reason", "exit_conditions", "timestamp", "trace_ref", "unknowns"}, "state_fields")
    check(schema["state_is_cognitive_mode"] is True and schema["state_is_not_field"] is True and schema["state_is_not_flow"] is True and schema["state_is_not_runtime"] is True and schema["state_is_not_action_command"] is True and schema["candidate_only"] is True and schema["automatic_transition"] is False, "state_boundary")

    registry = load(assets, "state_type_registry.json")
    registered = [item["state"] for item in registry["types"]]
    check(registry["unique_state_types"] is True and registered == STATES, "registry_coverage")
    check(all(item.get("purpose") and item.get("attention_focus") for item in registry["types"]), "registry_descriptions")
    check(registry["emotion_is_not_state_owner"] is True and registry["b_route_state_is_separate"] is True, "registry_boundary")

    transition = load(assets, "state_transition_contract.json")
    check(transition["canonical_cycle"] == CYCLE, "transition_cycle")
    expected_transitions = [("Observation", "Understanding"), ("Understanding", "Decision"), ("Decision", "Action"), ("Action", "Reflection"), ("Reflection", "Learning"), ("Learning", "Observation")]
    check([(item["from"], item["to"]) for item in transition["transitions"]] == expected_transitions, "transition_edges")
    check(transition["transition_is_candidate"] is True and transition["automatic_transition"] is False and transition["scheduler"] is False and transition["runtime_implemented"] is False and transition["action_execution"] is False and transition["learning_runtime"] is False and transition["reconsideration_allowed"] is True and transition["unknowns_preserved"] is True, "transition_boundary")

    entry = load(assets, "state_entry_exit_contract.json")
    check(set(entry["entry_requirements"]) == set(STATES), "entry_coverage")
    check(all(entry["entry_requirements"][state] for state in STATES), "entry_requirements")
    check(entry["exit_is_candidate"] is True and entry["exit_requires_trace"] is True and entry["entry_does_not_execute"] is True and entry["entry_does_not_modify_reality"] is True and entry["exit_does_not_auto_write_memory"] is True and entry["exit_does_not_auto_update_schema"] is True and entry["self_review_required_for_learning_exit"] is True, "entry_exit_boundary")

    attention = load(assets, "state_attention_relation.json")
    check(set(attention["mapping"]) == set(STATES), "attention_mapping")
    check(attention["state_provides_attention_policy_candidate"] is True and attention["attention_does_not_own_state"] is True and attention["attention_does_not_switch_state"] is True and attention["attention_does_not_execute_action"] is True and attention["attention_does_not_write_memory"] is True and attention["self_rhythm_is_resource_hint"] is True and attention["candidate_only"] is True, "attention_boundary")

    memory = load(assets, "state_memory_relation.json")
    check(set(memory["mapping"]) == {"Observation", "Understanding", "Reflection", "Learning"}, "memory_mapping")
    check(memory["memory_is_not_state"] is True and memory["memory_is_not_reality"] is True and memory["current_reality_precedence"] is True and memory["single_outcome_not_memory"] is True and memory["state_does_not_auto_write_memory"] is True and memory["memory_does_not_switch_state"] is True and memory["candidate_only"] is True, "memory_boundary")

    decision = load(assets, "state_decision_relation.json")
    check(decision["flow"] == ["Understanding State", "Goal Candidate", "Value Utility Candidate", "Decision State", "Decision Arbitration Candidate", "Action State Candidate"], "decision_flow")
    check(set(decision["decision_state_inputs"]) >= {"Current Understanding", "Goal", "Value Utility", "Self Constraint", "Risk", "Unknowns"}, "decision_inputs")
    check(decision["brain_generates_candidates"] is True and decision["arbitration_selects_candidate"] is True and decision["state_does_not_execute"] is True and decision["decision_is_not_action"] is True and decision["self_has_veto_context"] is True and decision["automatic_state_to_action"] is False and decision["candidate_only"] is True, "decision_boundary")

    learning = load(assets, "state_learning_relation.json")
    check(learning["flow"] == ["Reflection State", "Outcome Evaluation", "Experience Candidate", "Pattern/Schema Candidate", "Learning State", "Growth Candidate", "Self Review", "Observation State"], "learning_flow")
    check(set(learning["learning_state_requires"]) >= {"validated_experience", "pattern_or_capability_gap", "learning_utility", "self_review"}, "learning_requirements")
    check(learning["learning_is_not_memory"] is True and learning["learning_is_not_runtime"] is True and learning["single_outcome_not_schema"] is True and learning["automatic_learning"] is False and learning["automatic_schema_update"] is False and learning["automatic_capability_update"] is False and learning["self_review_required"] is True and learning["candidate_only"] is True, "learning_boundary")

    self_boundary = load(assets, "state_self_boundary.json")
    check(set(self_boundary["self_inputs"]) >= {"Constitution", "Identity Boundary", "Capability State", "Resource State", "Self Regulation", "Self Rhythm", "Self World Boundary"}, "self_inputs")
    check(set(self_boundary["self_permissions"]) == {"constrain_state_candidate", "veto_unsafe_transition", "provide_resource_context", "request_reconsideration", "review_learning_exit"}, "self_permissions")
    check(set(self_boundary["self_protected"]) >= {"Constitution", "Identity", "Safety Boundary", "Core Brain Rules"} and set(self_boundary["self_rhythm_provides"]) >= {"resource_budget_hint", "cognitive_intensity_hint", "tick_frequency_hint"}, "self_protected")
    check(self_boundary["self_rhythm_does_not_switch_state"] is True and self_boundary["self_does_not_execute_action"] is True and self_boundary["self_does_not_auto_adopt_learning"] is True and self_boundary["state_does_not_modify_self"] is True and self_boundary["candidate_only"] is True, "self_boundary")

    a_route = load(assets, "a_route_state_flow.json")
    check(a_route["flow"] == CYCLE and a_route["purpose"] == "current_reality_cognitive_processing" and a_route["state_is_current_mode"] is True and a_route["field_is_context"] is True and a_route["flow_is_process"] is True and a_route["state_transition_is_candidate"] is True, "a_route_flow")
    check(a_route["runtime"] is False and a_route["scheduler"] is False and a_route["automatic_transition"] is False and a_route["action_execution"] is False and a_route["learning_runtime"] is False and a_route["emotion_runtime"] is False, "a_route_boundary")

    b_route = load(assets, "b_route_state_boundary.json")
    check(b_route["a_state"] == "current_reality_processing_state" and b_route["b_state"] == "future_simulation_state" and b_route["b_route_status"] == "future_interface_only", "b_route_states")
    check(b_route["b_route_runtime"] is False and b_route["b_route_cannot_override_a_state"] is True and b_route["b_route_cannot_override_reality"] is True and b_route["b_route_cannot_directly_modify_self"] is True and b_route["b_route_cannot_directly_modify_learning"] is True and b_route["b_route_cannot_execute_action"] is True and b_route["route_mixing"] is False, "b_route_boundary")

    ownership = load(assets, "ownership_registry.json")
    records = ownership["ownership"]
    owners = [item["owner"] for item in records]
    modules = [item["module"] for item in records]
    check(ownership["unique_owner_required"] is True and len(owners) == len(set(owners)) and len(modules) == len(set(modules)), "unique_owners")
    check({"Cognitive State", "Observation State", "Understanding State", "Decision State", "Action State", "Reflection State", "Learning State", "Attention", "Self Rhythm", "Self", "Runtime", "B Route"} <= set(modules), "ownership_coverage")
    check(all(item.get("writer") and item.get("reader") for item in records), "ownership_writer_reader")

    dependency = load(assets, "dependency_boundary.json")
    required_forbidden = {"State -> Scheduler", "State -> Execute Action", "State -> Direct Reality Mutation", "Attention -> Own State", "Attention -> Switch State", "Self Rhythm -> Switch State", "Learning -> Direct State Mutation", "Single Outcome -> Schema Update", "B Route -> Override A State", "B Route -> Direct Self Modification", "Runtime -> State Authority", "State -> Learning Runtime", "State -> B Route Runtime", "State -> Model Switching", "State -> Hardware Control"}
    check(required_forbidden <= set(dependency["forbidden_dependencies"]), "dependency_forbidden")
    check(dependency["no_state_runtime"] is True and dependency["no_scheduler"] is True and dependency["no_automatic_transition"] is True and dependency["no_action_execution"] is True and dependency["no_learning_runtime"] is True and dependency["no_emotion_runtime"] is True and dependency["no_b_route_runtime"] is True and dependency["no_model_integration"] is True and dependency["no_hardware_control"] is True, "dependency_boundary")

    guards = load(assets, "negative_guards.json")
    required_guards = {"state_runtime", "scheduler", "automatic_state_transition", "state_execute_action", "state_direct_reality_mutation", "attention_own_state", "attention_switch_state", "self_rhythm_switch_state", "emotion_own_state", "memory_switch_state", "learning_direct_state_mutation", "learning_direct_identity_change", "learning_direct_constitution_change", "single_outcome_schema_update", "b_route_override_a_state", "b_route_override_reality", "b_route_direct_self_modification", "runtime_state_authority", "state_learning_runtime", "state_b_route_runtime", "state_model_switching", "state_hardware_control", "action_execution", "learning_runtime", "emotion_runtime", "b_route_runtime", "model_calls", "provider_calls", "no_check_weaken", "no_hardcoded_pass"}
    check(required_guards <= set(guards["forbidden"]), "negative_guards")
    check(all(guards["invariants"].get(key) is True for key in ("six_state_model", "state_is_not_field", "state_is_not_flow", "transitions_are_candidates", "attention_is_not_state_owner", "self_rhythm_is_resource_hint", "self_review_required_for_learning", "a_route_b_route_separation", "unknowns_preserved")), "negative_invariants")

    summary = load(assets, "summary.json")
    check(summary["status"] == "architecture_only" and summary["readiness_token"] == "LUNA_COGNITIVE_STATE_MACHINE_ARCHITECTURE_READY", "summary_status")
    check(summary["states"] == STATES and summary["canonical_cycle"] == CYCLE and summary["state_is_not_field"] is True and summary["state_is_not_flow"] is True and summary["state_is_not_runtime"] is True and summary["transition_is_candidate"] is True and summary["ownership_unique"] is True, "summary_model")
    check(summary["runtime"] is False and summary["scheduler"] is False and summary["automatic_transition"] is False and summary["action_execution"] is False and summary["learning_runtime"] is False and summary["emotion_runtime"] is False and summary["b_route_runtime"] is False and summary["model_integration"] is False and summary["hardware_control"] is False, "summary_boundary")
    check(len(summary["reusable_assets"]) >= 6 and len(summary["parallel_risks"]) >= 4 and len(summary["future_extensions"]) >= 3, "summary_inventory")

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
        print("READINESS: LUNA_COGNITIVE_STATE_MACHINE_ARCHITECTURE_REMEDIATION_REQUIRED")
        print("NEXT: REMEDIATE_REPORTED_FAILURES_ONLY")
        return 1
    print("FINAL_DECISION: V2_FINAL_VERIFICATION_PASSED")
    print("READINESS: LUNA_COGNITIVE_STATE_MACHINE_ARCHITECTURE_READY")
    print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

