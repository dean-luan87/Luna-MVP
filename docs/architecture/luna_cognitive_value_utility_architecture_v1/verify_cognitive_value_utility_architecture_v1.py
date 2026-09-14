"""V0 static contract verifier for Cognitive Value & Utility Architecture."""
from __future__ import annotations

import ast
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
JSON_FILES = [
    "value_schema.json", "value_type_registry.json", "value_hierarchy_contract.json",
    "utility_score_contract.json", "benefit_evaluation_contract.json",
    "cost_evaluation_contract.json", "risk_evaluation_contract.json",
    "priority_ranking_contract.json", "value_goal_relation.json",
    "value_exploration_relation.json", "value_decision_relation.json",
    "value_self_boundary.json", "value_memory_relation.json",
    "value_schema_relation.json", "ownership_registry.json",
    "dependency_boundary.json", "negative_guards.json", "summary.json",
]
MD_FILES = [
    "cognitive_value_utility_architecture.md", "value_hierarchy_model.md",
    "utility_evaluation_model.md", "value_governance_model.md",
    "implementation_plan.md",
]
VERIFIER = "verify_cognitive_value_utility_architecture_v1.py"


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

    schema = assets["value_schema.json"]
    check({"value_id", "value_type", "field_ref", "goal_ref", "importance_candidate", "provenance", "unknowns"} <= set(schema["required"]), "schema_fields")
    check(schema["candidate_only"] is True and schema["value_is_not_decision"] is True and schema["value_is_not_goal_authority"] is True and schema["value_does_not_execute"] is True and schema["automatic_scoring"] is False, "schema_boundary")

    types = assets["value_type_registry.json"]
    hierarchy = ["Survival Value", "Safety Value", "Integrity Value", "Mission Value", "Relationship Value", "Growth Value"]
    check(types["types"] == hierarchy and types["hierarchy_order"] == hierarchy, "value_type_coverage")
    check(types["contextual_evaluation"] is True and types["fixed_weight_table"] is False and types["hard_constraint_check_required"] is True and types["candidate_only"] is True, "value_type_boundary")

    hierarchy_contract = assets["value_hierarchy_contract.json"]
    check([x["name"] for x in hierarchy_contract["hierarchy"]] == hierarchy and [x["rank"] for x in hierarchy_contract["hierarchy"]] == [0, 1, 2, 3, 4, 5], "hierarchy_contract")
    check(hierarchy_contract["higher_constraint_can_reject_lower_candidate"] is True and hierarchy_contract["hierarchy_is_not_action_authority"] is True and hierarchy_contract["value_does_not_create_goal"] is True and hierarchy_contract["current_field_context_required"] is True, "hierarchy_boundary")

    utility = assets["utility_score_contract.json"]
    check(set(utility["inputs"]) == {"Expected Benefit", "Importance", "Probability", "Resource Cost", "Risk Factor"}, "utility_inputs")
    check(utility["formula"] == "(Expected Benefit × Importance × Probability) - (Resource Cost × Risk Factor)" and utility["calculation_implemented"] is False and utility["candidate_only"] is True and utility["hard_constraint_check_required"] is True and utility["utility_does_not_decide"] is True and utility["utility_does_not_execute"] is True, "utility_boundary")

    benefit = assets["benefit_evaluation_contract.json"]
    check(set(benefit["benefit_sources"]) == {"Safety Improvement", "Task Completion", "Knowledge Gain", "Capability Gain", "Relationship Support", "System Stability"}, "benefit_sources")
    check(set(benefit["inputs"]) == {"Goal Candidate", "Field Context", "Evidence", "Belief", "Capability State", "Experience Context"} and benefit["calculation_implemented"] is False and benefit["benefit_is_not_fact"] is True and benefit["benefit_does_not_create_goal"] is True, "benefit_boundary")

    cost = assets["cost_evaluation_contract.json"]
    check(set(cost["cost_domains"]) == {"Compute", "Time", "Battery", "Memory", "User Attention", "Device Wear", "Network"}, "cost_domains")
    check(set(cost["inputs"]) == {"Goal Candidate", "Capability Requirement", "Self Resource State", "Self Rhythm Hint", "Task Context"} and cost["calculation_implemented"] is False and cost["self_provides_resource_context"] is True and cost["cost_does_not_control_runtime"] is True and cost["cost_does_not_switch_model"] is True, "cost_boundary")

    risk = assets["risk_evaluation_contract.json"]
    check(set(risk["risk_domains"]) == {"Safety Risk", "System Risk", "Irreversible Impact Risk", "Capability Risk", "Privacy Risk", "Unknown Risk"}, "risk_domains")
    check(set(risk["inputs"]) == {"Goal Candidate", "Field Context", "Evidence", "Unknowns", "Capability State", "Constitution Constraints"} and risk["calculation_implemented"] is False and risk["hard_constraint_precedence"] is True and risk["risk_does_not_execute"] is True, "risk_boundary")

    ranking = assets["priority_ranking_contract.json"]
    check(set(ranking["inputs"]) == {"Value Candidate", "Utility Candidate", "Hard Constraint Result", "Goal Priority Candidate", "Self Resource State", "Field Context"}, "ranking_inputs")
    check(set(ranking["outputs"]) == {"Priority Candidate", "Utility Level Candidate", "Accept Candidate", "Reject Candidate", "Defer Candidate"} and ranking["constraint_check_precedes_ranking"] is True and ranking["ranking_is_not_decision"] is True and ranking["ranking_is_not_action"] is True and ranking["automatic_ranking"] is False and ranking["brain_review_required"] is True, "ranking_boundary")

    goal_relation = assets["value_goal_relation.json"]
    check(goal_relation["flow"] == ["Goal Candidate", "Value Evaluation Candidate", "Utility Candidate", "Goal Priority Candidate"], "goal_flow")
    check(goal_relation["goal_creates_value"] is False and goal_relation["value_creates_goal"] is False and goal_relation["value_modifies_goal"] is False and goal_relation["goal_priority_is_candidate"] is True and goal_relation["candidate_only"] is True, "goal_boundary")

    exploration = assets["value_exploration_relation.json"]
    check(set(exploration["inputs"]) == {"Expected Information Gain", "Exploration Cost", "Safety Impact", "Decision Impact", "Unknowns"}, "exploration_inputs")
    check(exploration["formula"] == "Expected Information Gain - Exploration Cost" and exploration["exploration_is_investment"] is True and exploration["calculation_implemented"] is False and exploration["value_does_not_start_exploration"] is True and exploration["self_approval_required"] is True and exploration["exploration_execution"] is False, "exploration_boundary")

    decision = assets["value_decision_relation.json"]
    check(decision["flow"] == ["Value Evaluation", "Utility Calculation Candidate", "Priority Ranking Candidate", "Brain / Decision Arbitration Review"], "decision_flow")
    check(decision["value_is_not_decision_authority"] is True and decision["brain_retains_judgment"] is True and decision["decision_arbitration_future_only"] is True and decision["action_execution"] is False and decision["candidate_only"] is True, "decision_boundary")

    self_boundary = assets["value_self_boundary.json"]
    check(set(self_boundary["self_provides"]) == {"Current Resource State", "Health State", "Self Rhythm Hint", "Capability Boundary", "Stability Constraint"}, "self_inputs")
    check(self_boundary["self_has_hard_boundary_authority"] is True and self_boundary["value_does_not_control_resource"] is True and self_boundary["value_does_not_control_runtime"] is True and self_boundary["candidate_only"] is True, "self_boundary")

    memory = assets["value_memory_relation.json"]
    check(set(memory["memory_provides"]) == {"Historical Outcome", "Experience Context", "Capability Reliability", "Past Cost Context"}, "memory_context")
    check(memory["memory_creates_value_automatically"] is False and memory["memory_overrides_current_reality"] is False and memory["current_evidence_precedence"] is True and memory["memory_does_not_rank_directly"] is True and memory["candidate_only"] is True, "memory_boundary")
    schema_relation = assets["value_schema_relation.json"]
    check(set(schema_relation["schema_provides"]) == {"Pattern Context", "Regularity Context", "Prior Context"}, "schema_context")
    check(schema_relation["schema_creates_value_automatically"] is False and schema_relation["schema_overrides_current_evidence"] is False and schema_relation["current_evidence_precedence"] is True and schema_relation["schema_does_not_decide"] is True and schema_relation["candidate_only"] is True, "schema_boundary")

    ownership = assets["ownership_registry.json"]
    owners = [x["owner"] for x in ownership["ownership"]]
    required_owners = {"Constitution", "Value Layer", "Self Layer", "Goal Layer", "Exploration Governance", "Brain", "Decision Arbitration", "Memory", "Schema", "Field"}
    check(ownership["unique_owner_required"] is True and len(owners) == len(set(owners)), "unique_owners")
    check(required_owners <= set(owners), "ownership_coverage")
    check(all(x.get("writer") and x.get("reader") for x in ownership["ownership"]), "ownership_writer_reader")

    dependency = assets["dependency_boundary.json"]
    required_forbidden = {"Value -> Create Goal", "Value -> Direct Action", "Value -> Modify Reality", "Value -> Rewrite Constitution", "Value -> Modify Itself", "Utility -> Execute Action", "Priority -> Execute Action", "Emotion -> Modify Value"}
    check(required_forbidden <= set(dependency["forbidden_dependencies"]), "dependency_forbidden")
    check(dependency["no_parallel_value_manager"] is True and dependency["no_parallel_utility_engine"] is True and dependency["utility_runtime"] is False and dependency["automatic_scoring"] is False and dependency["decision_arbitration_runtime"] is False and dependency["action_execution"] is False and dependency["emotion_integration"] is False and dependency["learning"] is False, "dependency_boundary")

    guards = assets["negative_guards.json"]
    required_guards = {"utility_runtime", "automatic_scoring", "automatic_priority_ranking", "value_create_goal", "value_modify_goal", "value_direct_action", "value_modify_reality", "value_modify_identity", "value_rewrite_constitution", "value_modify_itself", "utility_execute_action", "priority_execute_action", "emotion_modify_value", "emotion_runtime", "learning", "model_calls", "provider_calls", "hardware_control", "decision_execution", "parallel_value_manager", "parallel_utility_engine"}
    check(required_guards <= set(guards["forbidden"]), "negative_guards")
    check(guards["value_is_not_decision"] is True and guards["value_is_not_goal_authority"] is True and guards["value_is_not_action"] is True and guards["candidate_only"] is True and guards["hard_constraint_precedence"] is True and guards["unknowns_preserved"] is True and guards["no_check_weaken"] is True and guards["no_hardcoded_pass"] is True, "negative_invariants")

    summary = assets["summary.json"]
    check(summary["status"] == "architecture_only" and summary["readiness_token"] == "LUNA_COGNITIVE_VALUE_UTILITY_ARCHITECTURE_READY", "summary_status")
    check(summary["value_hierarchy"] == hierarchy and summary["utility_formula"] == "(Expected Benefit × Importance × Probability) - (Resource Cost × Risk Factor)" and summary["exploration_formula"] == "Expected Information Gain - Exploration Cost", "summary_models")
    check(summary["runtime"] is False and summary["utility_runtime"] is False and summary["automatic_scoring"] is False and summary["automatic_priority_ranking"] is False and summary["decision_execution"] is False and summary["emotion_integration"] is False and summary["learning"] is False, "summary_boundary")
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
        print("READINESS: LUNA_COGNITIVE_VALUE_UTILITY_ARCHITECTURE_REMEDIATION_REQUIRED")
        print("NEXT: REMEDIATE_REPORTED_FAILURES_ONLY")
        return 1
    print("FINAL_DECISION: V2_FINAL_VERIFICATION_PASSED")
    print("READINESS: LUNA_COGNITIVE_VALUE_UTILITY_ARCHITECTURE_READY")
    print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
