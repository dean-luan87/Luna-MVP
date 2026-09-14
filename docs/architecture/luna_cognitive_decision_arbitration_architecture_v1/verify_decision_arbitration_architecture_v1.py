"""V0 static contract verifier for Decision Arbitration Architecture."""
from __future__ import annotations

import ast
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
JSON_FILES = [
    "decision_candidate_schema.json", "decision_input_contract.json",
    "decision_arbitration_contract.json", "decision_constraint_contract.json",
    "decision_priority_contract.json", "decision_lifecycle_contract.json",
    "decision_goal_relation.json", "decision_value_relation.json",
    "decision_utility_relation.json", "decision_self_boundary.json",
    "decision_reconsideration_contract.json", "ownership_registry.json",
    "dependency_boundary.json", "negative_guards.json", "summary.json",
]
MD_FILES = [
    "cognitive_decision_arbitration_architecture.md", "decision_candidate_model.md",
    "decision_selection_model.md", "decision_governance_model.md",
    "implementation_plan.md",
]
VERIFIER = "verify_decision_arbitration_architecture_v1.py"


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

    schema = assets["decision_candidate_schema.json"]
    required_fields = {"candidate_id", "goal_reference", "expected_outcome", "utility_candidate", "risk", "confidence", "required_capability", "resource_cost", "reversibility", "unknowns", "provenance"}
    check(required_fields <= set(schema["required"]), "candidate_fields")
    check(schema["candidate_only"] is True and schema["decision_is_not_action"] is True and schema["decision_is_not_command"] is True and schema["decision_does_not_execute"] is True and schema["current_understanding_required"] is True, "candidate_boundary")

    inputs = assets["decision_input_contract.json"]
    expected_inputs = {"Current Understanding", "Current Reality", "Goal", "Value", "Utility", "Self State", "Risk", "Unknowns", "Candidate Set"}
    check(set(inputs["inputs"]) == expected_inputs and inputs["candidate_source"] == "Brain", "input_coverage")
    check(inputs["memory_is_context_not_authority"] is True and inputs["current_reality_precedence"] is True and inputs["self_constraint_required"] is True and inputs["candidate_only"] is True and inputs["action_execution"] is False and inputs["planner"] is False and inputs["b_route"] is False, "input_boundary")

    arbitration = assets["decision_arbitration_contract.json"]
    check(arbitration["flow"] == ["Candidate Set", "Hard Constraint Filter", "Utility Evaluation", "Priority Ranking", "Decision Selection"], "arbitration_flow")
    check(set(arbitration["outputs"]) == {"Selected Decision Candidate", "Rejected Candidate", "Deferred Candidate", "Reconsideration Candidate"}, "arbitration_outputs")
    check(arbitration["hard_constraint_filter_first"] is True and arbitration["selected_output_is_candidate"] is True and arbitration["decision_commitment"] is False and arbitration["action_execution"] is False and arbitration["planner"] is False and arbitration["automatic_arbitration"] is False and arbitration["brain_generates_candidates"] is True and arbitration["arbitration_selects_candidate"] is True, "arbitration_boundary")

    constraint = assets["decision_constraint_contract.json"]
    check(set(constraint["hard_constraints"]) == {"Constitution", "Safety", "Self Preservation", "Capability Feasibility", "Irreversible Impact Boundary"}, "constraint_coverage")
    check(constraint["hard_violation_rejects"] is True and constraint["hard_constraints_are_non_compensatory"] is True and constraint["self_has_veto_context"] is True and constraint["constraint_does_not_execute"] is True and constraint["candidate_only"] is True, "constraint_boundary")

    priority = assets["decision_priority_contract.json"]
    check(set(priority["inputs"]) == {"Utility Candidate", "Value Dimensions", "Goal Priority Candidate", "Risk Candidate", "Resource Cost Candidate", "Confidence", "Reversibility"}, "priority_inputs")
    check(set(priority["outputs"]) == {"Priority Candidate", "Tradeoff Candidate", "Sensitivity Candidate"} and priority["constraint_filter_precedes_priority"] is True and priority["priority_is_not_decision"] is True and priority["priority_is_not_action"] is True and priority["automatic_ranking"] is False and priority["brain_review_required"] is True, "priority_boundary")

    lifecycle = assets["decision_lifecycle_contract.json"]
    check(lifecycle["states"] == ["Proposed", "Evaluated", "Approved", "Active", "Invalidated", "Reconsidered"], "lifecycle_states")
    check(lifecycle["automatic_transition"] is False and lifecycle["selected_state_is_candidate"] is True and lifecycle["runtime_implemented"] is False and lifecycle["action_execution"] is False, "lifecycle_boundary")
    check(set(lifecycle["invalidating_events"]) >= {"Reality Change", "Field Change", "Understanding Contradiction", "Risk Increase", "Capability Failure", "Self State Change"}, "invalidation_events")

    goal = assets["decision_goal_relation.json"]
    check(goal["flow"] == ["Goal", "Decision Candidate Set", "Decision Arbitration", "Selected Decision Candidate"], "goal_flow")
    check(goal["decision_creates_goal"] is False and goal["decision_modifies_goal"] is False and goal["goal_overrides_constitution"] is False and goal["goal_reference_required"] is True and goal["candidate_only"] is True, "goal_boundary")
    value = assets["decision_value_relation.json"]
    check(value["flow"] == ["Value Constraints", "Utility Candidate", "Priority Candidate", "Decision Arbitration"], "value_flow")
    check(value["value_is_not_decision_authority"] is True and value["value_does_not_create_candidate"] is True and value["value_does_not_execute"] is True and value["hard_constraint_precedence"] is True and value["candidate_only"] is True, "value_boundary")
    utility = assets["decision_utility_relation.json"]
    check(set(utility["inputs"]) == {"Expected Benefit", "Importance", "Probability", "Resource Cost", "Risk Factor"}, "utility_inputs")
    check(utility["utility_is_candidate"] is True and utility["utility_does_not_decide_alone"] is True and utility["utility_does_not_execute"] is True and utility["hard_constraint_precedes_utility"] is True and utility["scalar_score_is_not_authority"] is True and utility["candidate_only"] is True, "utility_boundary")

    self_boundary = assets["decision_self_boundary.json"]
    check(set(self_boundary["self_inputs"]) == {"Capability State", "Resource State", "Health State", "Self Rhythm Hint", "Self Preservation Constraint", "Identity Boundary"}, "self_inputs")
    check(set(self_boundary["self_permissions"]) == {"constrain_candidate", "veto_candidate", "request_reconsideration", "provide_constraint_context"} and self_boundary["self_has_veto_context"] is True and self_boundary["self_does_not_select_alone"] is True and self_boundary["candidate_only"] is True and self_boundary["action_execution"] is False, "self_boundary")
    reconsider = assets["decision_reconsideration_contract.json"]
    check(set(reconsider["triggers"]) >= {"Reality Change", "Field Change", "New Evidence", "Understanding Contradiction", "Risk Increase", "Capability Failure", "Self State Change"}, "reconsideration_triggers")
    check(reconsider["output"] == "Reconsideration Candidate" and reconsider["automatic_reconsideration"] is False and reconsider["reconsideration_does_not_execute"] is True and reconsider["reconsideration_does_not_modify_reality"] is True and reconsider["brain_review_required"] is True and reconsider["candidate_only"] is True, "reconsideration_boundary")

    ownership = assets["ownership_registry.json"]
    owners = [x["owner"] for x in ownership["ownership"]]
    required_owners = {"Brain", "Decision Arbitration", "Self", "Constitution", "Value Utility", "Goal", "Action Boundary", "Runtime", "Field", "Memory", "B Route"}
    check(ownership["unique_owner_required"] is True and len(owners) == len(set(owners)), "unique_owners")
    check(required_owners <= set(owners), "ownership_coverage")
    check(all(x.get("writer") and x.get("reader") for x in ownership["ownership"]), "ownership_writer_reader")

    dependency = assets["dependency_boundary.json"]
    required_forbidden = {"Brain -> Execute Action", "Decision Arbitration -> Execute Action", "Decision Candidate -> Action Command", "Decision -> Direct Reality Mutation", "Decision Arbitration -> Create Goal", "Memory -> Override Current Reality", "B Route -> Override Current Decision", "External Algorithm -> Commit Decision", "Runtime -> Generate Decision", "Decision Arbitration -> Run Planner"}
    check(required_forbidden <= set(dependency["forbidden_dependencies"]), "dependency_forbidden")
    check(dependency["brain_is_candidate_owner"] is True and dependency["arbitration_is_selection_owner"] is True and dependency["action_boundary_is_execution_owner"] is True and dependency["no_planner"] is True and dependency["no_decision_runtime"] is True and dependency["no_action_execution"] is True and dependency["no_b_route_runtime"] is True and dependency["no_emotion_runtime"] is True, "dependency_boundary")

    guards = assets["negative_guards.json"]
    required_guards = {"decision_runtime", "action_execution", "planner", "automatic_execution", "emotion_runtime", "b_route_runtime", "model_calls", "provider_calls", "hardware_control", "brain_execute_action", "arbitration_execute_action", "candidate_action_command", "decision_modify_reality", "arbitration_create_goal", "arbitration_modify_value", "arbitration_rewrite_constitution", "memory_override_reality", "b_route_override_decision", "external_algorithm_commit_decision", "runtime_generate_decision", "automatic_reconsideration", "parallel_brain", "parallel_decision_owner", "no_check_weaken", "no_hardcoded_pass"}
    check(required_guards <= set(guards["forbidden"]), "negative_guards")
    check(guards["decision_is_not_action"] is True and guards["selected_output_is_candidate"] is True and guards["hard_constraint_precedence"] is True and guards["self_veto_context_required"] is True and guards["current_reality_precedence"] is True and guards["unknowns_preserved"] is True, "negative_invariants")

    summary = assets["summary.json"]
    check(summary["status"] == "architecture_only" and summary["readiness_token"] == "LUNA_COGNITIVE_DECISION_ARBITRATION_ARCHITECTURE_READY", "summary_status")
    check(summary["canonical_flow"] == ["Understanding", "Goal", "Value Utility", "Decision Candidate Generation", "Decision Arbitration", "Selected Decision Candidate", "Action Boundary"], "summary_flow")
    check(summary["lifecycle"] == ["Proposed", "Evaluated", "Approved", "Active", "Invalidated", "Reconsidered"], "summary_lifecycle")
    check(summary["runtime"] is False and summary["decision_runtime"] is False and summary["action_execution"] is False and summary["planner"] is False and summary["automatic_execution"] is False and summary["emotion_runtime"] is False and summary["b_route_runtime"] is False and summary["model_integration"] is False, "summary_boundary")
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
        print("READINESS: LUNA_COGNITIVE_DECISION_ARBITRATION_ARCHITECTURE_REMEDIATION_REQUIRED")
        print("NEXT: REMEDIATE_REPORTED_FAILURES_ONLY")
        return 1
    print("FINAL_DECISION: V2_FINAL_VERIFICATION_PASSED")
    print("READINESS: LUNA_COGNITIVE_DECISION_ARBITRATION_ARCHITECTURE_READY")
    print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
