"""Static final-phase contract verifier for Cognitive Attention resources."""
from __future__ import annotations

import ast
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
JSON_FILES = [
    "attention_signal_schema.json",
    "attention_candidate_schema.json",
    "attention_value_contract.json",
    "attention_type_registry.json",
    "attention_allocation_contract.json",
    "attention_budget_contract.json",
    "attention_lifecycle_contract.json",
    "attention_memory_relation.json",
    "attention_schema_relation.json",
    "attention_belief_relation.json",
    "attention_uncertainty_relation.json",
    "self_attention_boundary.json",
    "ownership_registry.json",
    "dependency_boundary.json",
    "negative_guards.json",
    "summary.json",
]
MD_FILES = [
    "cognitive_attention_architecture.md",
    "attention_resource_allocation_model.md",
    "attention_governance_model.md",
    "implementation_plan.md",
]
VERIFIER = "verify_attention_resource_allocation_architecture_v1.py"


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

    signal = assets["attention_signal_schema.json"]
    required_signal = {"field_importance", "task_relevance", "safety_impact", "uncertainty", "belief_conflict", "memory_relevance", "schema_match", "self_budget"}
    check(required_signal <= set(signal["fields"]), "signal_fields")
    check(signal["perception_is_not_attention"] is True and signal["model_attention_is_not_cognitive_attention"] is True and signal["candidate_only"] is True and signal["decision_authority"] is False, "signal_boundary")

    candidate = assets["attention_candidate_schema.json"]
    check(candidate["candidate_only"] is True and candidate["self_approval_required"] is True and candidate["active_attention_is_admitted"] is False, "candidate_approval")
    check(candidate["direct_understanding"] is False and candidate["direct_action"] is False and candidate["unlimited_resource"] is False, "candidate_boundary")

    value = assets["attention_value_contract.json"]
    value_inputs = {"task_importance", "safety_impact", "decision_impact", "uncertainty_value", "conflict_value", "memory_relevance", "resource_cost"}
    check(set(value["inputs"]) == value_inputs, "value_inputs")
    check(value["algorithm_implemented"] is False and value["unknown_is_impact_weighted"] is True and value["candidate_only"] is True and value["decision_authority"] is False, "value_boundary")

    types = assets["attention_type_registry.json"]
    attention_types = {"Perceptual Attention", "Semantic Attention", "Context Attention", "Decision Attention", "Self Attention"}
    check(set(types["types"]) == attention_types, "attention_type_coverage")
    check(types["self_attention_is_neural_attention"] is False and types["model_attention_is_cognitive_attention"] is False and types["candidate_required"] is True and types["automatic_allocation"] is False, "attention_type_boundary")

    allocation = assets["attention_allocation_contract.json"]
    check(set(allocation["inputs"]) == {"current_field", "attention_signals", "attention_value_candidate", "self_budget", "cognitive_state", "self_rhythm_hint"}, "allocation_inputs")
    check(allocation["self_governance_required"] is True and allocation["active_attention_requires_approval"] is True and allocation["attention_produces_understanding"] is False and allocation["automatic_allocation"] is False and allocation["runtime_scheduling"] is False and allocation["candidate_only"] is True, "allocation_boundary")

    budget = assets["attention_budget_contract.json"]
    check(set(budget["resources"]) == {"CPU", "GPU/NPU", "Memory", "Battery", "Time", "Interaction Cost"}, "budget_resources")
    check(budget["self_has_final_resource_governance"] is True and budget["budget_is_candidate"] is True and budget["unlimited_attention"] is False and budget["direct_hardware_control"] is False and budget["runtime_control"] is False, "budget_boundary")

    lifecycle = assets["attention_lifecycle_contract.json"]
    lifecycle_states = {"Detected", "Candidate", "Evaluated", "Approved", "Active", "Reduced", "Suspended", "Archived"}
    check(set(lifecycle["states"]) == lifecycle_states, "lifecycle_states")
    check(lifecycle["automatic_transition"] is False and lifecycle["approval_required"] is True and lifecycle["active_is_runtime"] is False and lifecycle["candidate_only"] is True, "lifecycle_boundary")

    memory = assets["attention_memory_relation.json"]
    check(memory["flow"] == ["Current Field", "Attention", "Relevant Memory Activation", "Context Enhancement"], "memory_flow")
    check(memory["attention_activates_memory"] is True and memory["memory_forces_attention"] is False and memory["memory_direct_preemption"] is False and memory["context_required"] is True and memory["candidate_only"] is True, "memory_boundary")
    schema = assets["attention_schema_relation.json"]
    check(schema["flow"] == ["Schema", "Attention Prior", "Current Evidence", "Attention Update"], "schema_flow")
    check(schema["schema_provides_prior"] is True and schema["schema_determines_attention"] is False and schema["schema_overrides_reality"] is False and schema["current_evidence_precedence"] is True and schema["candidate_only"] is True, "schema_boundary")
    belief = assets["attention_belief_relation.json"]
    check(belief["belief_conflict_increases_attention"] is True and belief["belief_controls_attention"] is False and belief["reality_validation_link"] is True and belief["candidate_only"] is True, "belief_boundary")
    uncertainty = assets["attention_uncertainty_relation.json"]
    check(uncertainty["unknown_alone_is_not_priority"] is True and uncertainty["impact_weight_required"] is True and uncertainty["attention_executes_exploration"] is False and uncertainty["candidate_only"] is True, "uncertainty_boundary")

    self_boundary = assets["self_attention_boundary.json"]
    check(self_boundary["self_has_final_resource_governance"] is True and self_boundary["candidate_only"] is True, "self_boundary_owner")
    check(set(self_boundary["allowed"]) >= {"review_state", "review_resource", "review_task", "review_risk", "approve", "reject", "defer", "reduce"}, "self_allowed")
    check(set(self_boundary["forbidden"]) >= {"modify_identity", "modify_value", "modify_goal", "modify_constitution", "modify_brain_rules", "direct_model_switch", "direct_hardware_control", "direct_action", "scheduler_modification"}, "self_forbidden")

    ownership = assets["ownership_registry.json"]
    owners = [x["owner"] for x in ownership["ownership"]]
    required_owners = {"Evidence Layer", "Field", "Attention Layer", "Uncertainty", "Belief", "Memory", "Schema", "Self Regulation", "Brain", "Runtime"}
    check(ownership["unique_owner_required"] is True and len(owners) == len(set(owners)), "unique_owners")
    check(required_owners <= set(owners), "ownership_coverage")
    check(all(x.get("writer") for x in ownership["ownership"]), "writers_declared")

    dependency = assets["dependency_boundary.json"]
    check(dependency["no_parallel_attention_controller"] is True and dependency["no_model_attention_replacement"] is True and dependency["runtime"] is False and dependency["scheduler"] is False, "dependency_boundary")
    check(set(dependency["model_attention_boundary"]) == {"model_attention_is_capability_internal", "cognitive_attention_is_core_resource_allocation", "model_attention_cannot_replace_cognitive_attention"}, "model_attention_boundary")
    forbidden_dependencies = set(dependency["forbidden_dependencies"])
    check("Attention -> Direct Action" in forbidden_dependencies and "Attention -> Reality Mutation" in forbidden_dependencies and "Memory -> Force Attention" in forbidden_dependencies, "dependency_action_memory")
    check("Schema -> Override Reality" in forbidden_dependencies and "Model Attention -> Replace Cognitive Attention" in forbidden_dependencies and "Attention -> Unlimited Resource Usage" in forbidden_dependencies, "dependency_schema_model_budget")

    guards = assets["negative_guards.json"]
    required_guards = {"attention_runtime", "scheduler", "model_attention_modification", "automatic_resource_allocation", "runtime_integration", "action_execution", "attention_direct_action", "attention_modify_reality", "memory_force_attention", "schema_override_reality", "model_attention_replace_cognitive_attention", "attention_unlimited_resource_usage", "attention_model_switch", "attention_hardware_control", "attention_scheduler_modification", "parallel_attention_controller", "model_attention_replacement"}
    check(required_guards <= set(guards["forbidden"]), "negative_guards")
    check(guards["attention_is_not_perception"] is True and guards["attention_is_not_understanding"] is True and guards["attention_is_not_decision"] is True and guards["self_final_resource_governance"] is True and guards["candidate_only"] is True and guards["finite_resource_required"] is True, "negative_invariants")
    check(guards["no_check_weaken"] is True and guards["no_hardcoded_pass"] is True, "negative_verifier_guards")

    summary = assets["summary.json"]
    check(summary["status"] == "architecture_only", "summary_status")
    check(summary["readiness_token"] == "LUNA_COGNITIVE_ATTENTION_RESOURCE_ALLOCATION_ARCHITECTURE_READY", "summary_readiness")
    check(summary["attention_types"] == ["Perceptual Attention", "Semantic Attention", "Context Attention", "Decision Attention", "Self Attention"], "summary_types")
    check(summary["runtime"] is False and summary["scheduler"] is False and summary["automatic_allocation"] is False and summary["model_attention_modification"] is False and summary["action_execution"] is False, "summary_boundary")
    check(len(summary["reusable_attention_assets"]) >= 3 and len(summary["model_attention_assets"]) >= 2 and len(summary["parallel_risks"]) >= 2 and len(summary["migration_mapping"]) >= 1, "summary_inventory")

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
        print("READINESS: LUNA_COGNITIVE_ATTENTION_RESOURCE_ALLOCATION_ARCHITECTURE_REMEDIATION_REQUIRED")
        print("NEXT: REMEDIATE_REPORTED_FAILURES_ONLY")
        return 1
    print("FINAL_DECISION: V2_FINAL_VERIFICATION_PASSED")
    print("READINESS: LUNA_COGNITIVE_ATTENTION_RESOURCE_ALLOCATION_ARCHITECTURE_READY")
    print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
