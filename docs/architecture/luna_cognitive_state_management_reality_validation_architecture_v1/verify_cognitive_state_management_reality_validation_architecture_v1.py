"""Static final-phase contract verifier for state management and validation."""
from __future__ import annotations

import ast
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
JSON_FILES = [
    "cognitive_state_schema.json",
    "cognitive_state_transition_matrix.json",
    "cognitive_state_input_contract.json",
    "cognitive_state_output_contract.json",
    "validation_event_schema.json",
    "understanding_validation_contract.json",
    "hypothesis_update_candidate_schema.json",
    "reality_feedback_contract.json",
    "ownership_registry.json",
    "dependency_boundary.json",
    "negative_guards.json",
    "summary.json",
]
MD_FILES = [
    "cognitive_state_management_architecture.md",
    "reality_validation_loop_architecture.md",
    "implementation_plan.md",
    "state_validation_whitebox_v1.md",
    "state_validation_go_no_go_v1.md",
]
VERIFIER = "verify_cognitive_state_management_reality_validation_architecture_v1.py"


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

    state = assets["cognitive_state_schema.json"]
    states = {"NORMAL", "IDLE", "FOCUS", "PROTECTION", "DEGRADED", "RECOVERY"}
    check(set(state["states"]) == states, "state_vocabulary")
    check(state["candidate_only"] is True and state["automatic_transition"] is False, "state_candidate_boundary")
    check(state["runtime_state_machine"] is False and state["emotion_input"] is False, "state_no_runtime_emotion")

    matrix = assets["cognitive_state_transition_matrix.json"]
    transitions = {item["from"]: set(item["to"]) for item in matrix["allowed_transitions"]}
    check(set(transitions) == states, "transition_coverage")
    check(matrix["transition_is_candidate"] is True and matrix["transition_execution"] is False, "transition_candidate")
    check(matrix["scheduler_authority"] is False and matrix["model_switching"] is False and matrix["hardware_control"] is False, "transition_no_control")
    check(matrix["review_required"] is True, "transition_review")

    state_input = assets["cognitive_state_input_contract.json"]
    required_inputs = {"Self Regulation", "Resource Awareness", "Field Complexity", "Task Demand", "Capability Health", "Runtime Health"}
    check(set(state_input["inputs"]) == required_inputs, "state_inputs")
    check(state_input["self_regulation_role"] == "propose_state_adjustment_candidate", "self_regulation_candidate")
    check(state_input["self_rhythm_role"] == "provide_rhythm_context", "self_rhythm_context")
    check(state_input["automatic_transition"] is False and state_input["unknown_preserved"] is True, "state_input_boundary")

    state_output = assets["cognitive_state_output_contract.json"]
    check(state_output["candidate_only"] is True and state_output["decision_authority"] is False, "state_output_candidate")
    check(state_output["runtime_control"] is False and state_output["model_control"] is False and state_output["hardware_control"] is False, "state_output_no_control")
    check(state_output["consumer"] == "Cognitive Kernel", "state_kernel_consumer")

    validation_event = assets["validation_event_schema.json"]
    results = {"Confirmed", "Supported", "Contradicted", "Unknown", "Expired"}
    check(set(validation_event["result_values"]) == results, "validation_results")
    check(validation_event["original_hypothesis_preserved"] is True and validation_event["field_required"] is True and validation_event["time_required"] is True, "validation_context")
    check(validation_event["candidate_only"] is True, "validation_event_candidate")

    understanding = assets["understanding_validation_contract.json"]
    check(understanding["reality_precedence"] is True and understanding["understanding_adjustment_is_candidate"] is True, "validation_understanding_boundary")
    check(understanding["automatic_understanding_mutation"] is False and understanding["automatic_memory_mutation"] is False and understanding["automatic_self_mutation"] is False, "validation_no_mutation")
    check(understanding["brain_review_required"] is True, "validation_brain_review")

    hypothesis = assets["hypothesis_update_candidate_schema.json"]
    check(hypothesis["original_preserved"] is True and hypothesis["candidate_only"] is True, "hypothesis_preserved_candidate")
    check(set(hypothesis["proposed_status_values"]) >= {"supported", "contradicted", "unknown", "expired"}, "hypothesis_statuses")
    check(hypothesis["direct_belief_write"] is False and hypothesis["direct_memory_write"] is False, "hypothesis_no_write")

    feedback = assets["reality_feedback_contract.json"]
    check(feedback["feedback_is_reality"] is False and feedback["feedback_requires_evidence"] is True, "feedback_evidence_boundary")
    check(feedback["current_reality_precedence"] is True and feedback["memory_write"] is False and feedback["self_write"] is False and feedback["goal_write"] is False, "feedback_no_mutation")

    ownership = assets["ownership_registry.json"]
    owners = [item["owner"] for item in ownership["ownership"]]
    check(ownership["unique_owner_required"] is True and len(owners) == len(set(owners)), "unique_owners")
    check({"Self Regulation", "Self Rhythm Controller", "Cognitive Field", "Brain", "Runtime"} <= set(owners), "ownership_required_modules")
    check(all(item.get("writer") for item in ownership["ownership"]), "writers_declared")

    boundary = assets["dependency_boundary.json"]
    check(boundary["architecture_only"] is True, "dependency_architecture_only")
    forbidden = set(boundary["forbidden_dependencies"])
    check("Cognitive State -> Model Switch" in forbidden and "Validation -> Memory Direct Mutation" in forbidden, "dependency_no_model_memory")
    check("Validation -> Identity Rewrite" in forbidden and "Hypothesis -> Action Execution" in forbidden, "dependency_no_identity_action")

    guards = assets["negative_guards.json"]
    required_guards = {"runtime_implementation", "scheduler_implementation", "automatic_state_transition", "automatic_learning", "emotion_runtime", "b_route_runtime", "action_execution", "model_or_provider_integration", "hardware_control", "memory_mutation_from_validation", "self_mutation_from_validation", "identity_rewrite", "goal_rewrite"}
    check(required_guards <= set(guards["forbidden"]), "negative_guards")
    literal_guards = {"if_emotion_runtime_modify_state", "if_validation_modify_memory", "if_cognitive_state_switch_model", "if_hypothesis_execute_action"}
    check(literal_guards <= set(guards["forbidden"]), "negative_literal_guards")
    check(guards["state_output_must_be_candidate"] is True and guards["understanding_adjustment_must_be_candidate"] is True and guards["unknown_preserved"] is True, "negative_core_invariants")
    check(guards["no_check_weaken"] is True and guards["no_hardcoded_pass"] is True, "negative_verifier_guards")

    summary = assets["summary.json"]
    check(summary["status"] == "architecture_only", "summary_status")
    check(summary["readiness_token"] == "LUNA_COGNITIVE_STATE_MANAGEMENT_REALITY_VALIDATION_ARCHITECTURE_READY", "summary_readiness")
    check(summary["canonical_loop"] == ["Hypothesis", "Understanding", "Decision Candidate", "Reality Feedback", "Validation Result", "Understanding Adjustment Candidate"], "summary_loop")
    check(summary["runtime_active"] is False and summary["automatic_state_transition"] is False and summary["automatic_learning"] is False, "summary_boundaries")

    forbidden_imports = {"subprocess", "socket", "requests", "cv2", "torch", "transformers"}
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
        print("READINESS: LUNA_COGNITIVE_STATE_MANAGEMENT_REALITY_VALIDATION_ARCHITECTURE_REMEDIATION_REQUIRED")
        print("NEXT: REMEDIATE_REPORTED_FAILURES_ONLY")
        return 1
    print("FINAL_DECISION: V2_FINAL_VERIFICATION_PASSED")
    print("READINESS: LUNA_COGNITIVE_STATE_MANAGEMENT_REALITY_VALIDATION_ARCHITECTURE_READY")
    print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
