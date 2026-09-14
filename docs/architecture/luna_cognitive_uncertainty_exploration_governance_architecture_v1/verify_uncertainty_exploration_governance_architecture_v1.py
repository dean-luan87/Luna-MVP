"""Static final-phase contract verifier for uncertainty and exploration governance."""
from __future__ import annotations

import ast
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
JSON_FILES = [
    "uncertainty_type_registry.json",
    "uncertainty_schema.json",
    "uncertainty_impact_evaluation_contract.json",
    "exploration_candidate_schema.json",
    "exploration_strategy_registry.json",
    "exploration_budget_contract.json",
    "exploration_approval_contract.json",
    "exploration_state_schema.json",
    "exploration_stop_condition_contract.json",
    "uncertainty_attention_relation.json",
    "uncertainty_memory_relation.json",
    "uncertainty_knowledge_relation.json",
    "self_exploration_boundary.json",
    "ownership_registry.json",
    "dependency_boundary.json",
    "negative_guards.json",
    "summary.json",
]
MD_FILES = [
    "uncertainty_exploration_architecture.md",
    "uncertainty_taxonomy_model.md",
    "exploration_governance_model.md",
    "implementation_plan.md",
]
VERIFIER = "verify_uncertainty_exploration_governance_architecture_v1.py"


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

    type_registry = assets["uncertainty_type_registry.json"]
    uncertainty_types = {"Perception Uncertainty", "Semantic Uncertainty", "Field Uncertainty", "Causal Uncertainty", "Decision Uncertainty", "Capability Uncertainty"}
    check({x["type"] for x in type_registry["types"]} == uncertainty_types, "uncertainty_type_coverage")
    check(type_registry["unknown_is_first_class"] is True and type_registry["unknown_is_exploration"] is False and type_registry["candidate_only"] is True, "uncertainty_unknown_boundary")

    uncertainty = assets["uncertainty_schema.json"]
    check(set(uncertainty["type_values"]) == uncertainty_types, "uncertainty_schema_types")
    check(uncertainty["candidate_only"] is True and uncertainty["direct_action"] is False and uncertainty["forced_resolution"] is False and uncertainty["reality_replacement"] is False, "uncertainty_schema_boundary")

    impact = assets["uncertainty_impact_evaluation_contract.json"]
    impact_inputs = {"safety_impact", "decision_impact", "task_impact", "future_utility", "information_gain", "exploration_cost"}
    check(set(impact["inputs"]) == impact_inputs, "impact_inputs")
    check(set(impact["value_levels"]) == {"CRITICAL", "HIGH", "MEDIUM", "LOW", "IGNORE"}, "impact_levels")
    check(impact["calculation_implemented"] is False and impact["candidate_only"] is True and impact["self_approval_required"] is True and impact["direct_exploration"] is False, "impact_boundary")

    candidate = assets["exploration_candidate_schema.json"]
    check(set(candidate["required_refs"]) == {"uncertainty_ref", "strategy_ref", "field_ref", "provenance"}, "candidate_refs")
    check(candidate["candidate_only"] is True and candidate["self_approval_required"] is True and candidate["execution"] is False and candidate["unlimited_resources"] is False, "candidate_boundary")

    strategies = assets["exploration_strategy_registry.json"]
    strategy_types = {"Perception Exploration", "Interaction Exploration", "Environment Exploration", "Knowledge Exploration", "Experience Exploration"}
    check({x["strategy"] for x in strategies["strategies"]} == strategy_types, "strategy_coverage")
    check(strategies["automatic_execution"] is False and strategies["knowledge_auto_call"] is False and strategies["candidate_only"] is True and strategies["self_approval_required"] is True, "strategy_boundary")

    budget = assets["exploration_budget_contract.json"]
    check(set(budget["inputs"]) == {"compute", "energy", "time", "user_attention", "self_rhythm_hint", "cognitive_state"}, "budget_inputs")
    check(budget["budget_is_advisory"] is True and budget["unlimited_usage"] is False and budget["self_governance_required"] is True and budget["runtime_control"] is False and budget["hardware_control"] is False, "budget_boundary")

    approval = assets["exploration_approval_contract.json"]
    check(approval["owner"] == "Self Layer" and approval["controller"] == "Exploration Governance Controller", "approval_owner")
    check(set(approval["outputs"]) == {"Approved", "Rejected", "Deferred"} and set(approval["permissions"]) == {"priority_approval", "resource_budget", "exploration_depth", "stop_decision"}, "approval_scope")
    check(approval["direct_execution"] is False and approval["self_modification"] is False and approval["scheduler_modification"] is False and approval["model_switching"] is False and approval["candidate_only"] is True, "approval_boundary")

    state = assets["exploration_state_schema.json"]
    states = {"Detected", "Evaluated", "Candidate", "Approved", "Exploring", "Partial Result", "Completed", "Accepted Unknown", "Archived"}
    check(set(state["states"]) == states, "exploration_state_coverage")
    check(state["state_candidate"] is True and state["automatic_state_transition"] is False and state["accepted_unknown_is_valid"] is True and state["runtime"] is False and state["execution"] is False, "exploration_state_boundary")

    stop = assets["exploration_stop_condition_contract.json"]
    stop_conditions = {"Value Exhausted", "Budget Exhausted", "Information Ceiling", "Decision Sufficient", "Accept Unknown"}
    check(set(stop["conditions"]) == stop_conditions, "stop_conditions")
    check(stop["accept_unknown_allowed"] is True and stop["forced_resolution"] is False and stop["unlimited_exploration"] is False and stop["direct_action"] is False and stop["candidate_only"] is True, "stop_boundary")

    attention = assets["uncertainty_attention_relation.json"]
    check(attention["unknown_requests_attention"] is True and attention["attention_executes_exploration"] is False and attention["decision_authority"] is False and attention["candidate_only"] is True, "attention_boundary")
    memory = assets["uncertainty_memory_relation.json"]
    check(memory["flow"] == ["Exploration Result", "Information Lifecycle", "Experience Evaluation", "Memory Candidate", "Schema Candidate"], "memory_flow")
    check(memory["unresolved_unknown_can_be_retained"] is True and memory["automatic_memory"] is False and memory["memory_overrides_reality"] is False and memory["candidate_only"] is True, "memory_boundary")
    knowledge = assets["uncertainty_knowledge_relation.json"]
    check(knowledge["knowledge_auto_call"] is False and knowledge["knowledge_auto_injection"] is False and knowledge["field_role_context_required"] is True and knowledge["self_approval_required"] is True, "knowledge_boundary")

    self_boundary = assets["self_exploration_boundary.json"]
    check(set(self_boundary["allowed"]) >= {"priority_approval", "resource_budget", "exploration_depth", "stop_decision", "approve", "reject", "defer"}, "self_allowed")
    check(set(self_boundary["forbidden"]) >= {"modify_identity", "modify_value", "modify_goal", "modify_constitution", "modify_brain_rules", "automatic_model_switch", "hardware_control", "direct_action", "automatic_learning"}, "self_forbidden")
    check(self_boundary["cognitive_kernel_role"] == "propose_exploration" and self_boundary["runtime_role"] == "future_executor_only" and self_boundary["candidate_only"] is True, "self_boundary")

    ownership = assets["ownership_registry.json"]
    owners = [x["owner"] for x in ownership["ownership"]]
    required_owners = {"Cognitive Kernel", "Exploration Evaluation", "Self Layer", "Self Rhythm", "Cognitive State", "Knowledge", "Memory", "Schema", "Brain", "Runtime"}
    check(ownership["unique_owner_required"] is True and len(owners) == len(set(owners)), "unique_owners")
    check(required_owners <= set(owners), "ownership_coverage")
    check(all(x.get("writer") for x in ownership["ownership"]), "writers_declared")

    dependency = assets["dependency_boundary.json"]
    check(dependency["no_parallel_exploration_engine"] is True and dependency["runtime"] is False and dependency["scheduler"] is False and dependency["database_access"] is False, "dependency_boundary")
    forbidden_dependencies = set(dependency["forbidden_dependencies"])
    check("Uncertainty -> Direct Action" in forbidden_dependencies and "Exploration -> Direct Self Modification" in forbidden_dependencies, "dependency_action_self")
    check("Knowledge Retrieval -> Automatic Exploration" in forbidden_dependencies and "Unknown -> Forced Resolution" in forbidden_dependencies and "Memory -> Override Reality" in forbidden_dependencies, "dependency_unknown_memory")

    guards = assets["negative_guards.json"]
    required_guards = {"runtime", "exploration_engine", "scheduler", "automatic_exploration", "automatic_knowledge_call", "automatic_learning", "model_calls", "database_access", "uncertainty_direct_action", "exploration_direct_self_modification", "knowledge_retrieval_automatic_exploration", "exploration_unlimited_resource_usage", "unknown_forced_resolution", "memory_override_reality", "exploration_model_switch", "exploration_hardware_control", "exploration_b_route_runtime", "emotion_runtime"}
    check(required_guards <= set(guards["forbidden"]), "negative_guards")
    check(guards["unknown_is_not_exploration"] is True and guards["accept_unknown_allowed"] is True and guards["self_approval_required"] is True and guards["candidate_only"] is True, "negative_invariants")
    check(guards["no_check_weaken"] is True and guards["no_hardcoded_pass"] is True, "negative_verifier_guards")

    summary = assets["summary.json"]
    check(summary["status"] == "architecture_only", "summary_status")
    check(summary["readiness_token"] == "LUNA_COGNITIVE_UNCERTAINTY_EXPLORATION_GOVERNANCE_ARCHITECTURE_READY", "summary_readiness")
    check(summary["uncertainty_types"] == ["Perception Uncertainty", "Semantic Uncertainty", "Field Uncertainty", "Causal Uncertainty", "Decision Uncertainty", "Capability Uncertainty"], "summary_types")
    check(summary["exploration_strategies"] == ["Perception Exploration", "Interaction Exploration", "Environment Exploration", "Knowledge Exploration", "Experience Exploration"], "summary_strategies")
    check(summary["runtime"] is False and summary["scheduler"] is False and summary["automatic_exploration"] is False and summary["automatic_learning"] is False and summary["database_access"] is False, "summary_boundary")
    check(len(summary["reusable_assets"]) >= 6 and len(summary["exploration_assets"]) >= 2 and len(summary["self_governance_assets"]) >= 3 and len(summary["parallel_risks"]) >= 3 and len(summary["migration_mapping"]) >= 1, "summary_inventory")

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
        print("READINESS: LUNA_COGNITIVE_UNCERTAINTY_EXPLORATION_GOVERNANCE_ARCHITECTURE_REMEDIATION_REQUIRED")
        print("NEXT: REMEDIATE_REPORTED_FAILURES_ONLY")
        return 1
    print("FINAL_DECISION: V2_FINAL_VERIFICATION_PASSED")
    print("READINESS: LUNA_COGNITIVE_UNCERTAINTY_EXPLORATION_GOVERNANCE_ARCHITECTURE_READY")
    print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
