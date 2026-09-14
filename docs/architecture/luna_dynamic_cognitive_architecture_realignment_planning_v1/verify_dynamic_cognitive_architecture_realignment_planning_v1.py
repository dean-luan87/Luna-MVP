"""V0 static verifier for Dynamic Cognitive Architecture Realignment Planning."""
from __future__ import annotations

import ast
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parents[2]
JSON_FILES = [
    "existing_asset_mapping.json",
    "canonical_component_registry_v2.json",
    "personal_cognitive_network_boundary.json",
    "intent_and_gate_boundary.json",
    "causal_network_boundary.json",
    "field_activation_contract.json",
    "experience_evolution_boundary.json",
    "ownership_alignment.json",
    "duplicate_owner_risk_registry.json",
    "architecture_change_impact_registry.json",
    "migration_sequence.json",
    "phase_contract.json",
    "negative_guards.json",
    "summary.json",
]
MD_FILES = ["architecture_v2.md", "module_boundary_update.md", "migration_plan.md", "summary.md"]
VERIFIER = "verify_dynamic_cognitive_architecture_realignment_planning_v1.py"
READY = "LUNA_DYNAMIC_COGNITIVE_ARCHITECTURE_REALIGNMENT_PLAN_READY"


def load(assets: dict[str, dict], name: str) -> dict:
    if name not in assets:
        try:
            value = json.loads((ROOT / name).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            value = {}
        assets[name] = value if isinstance(value, dict) else {}
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
        value = load(assets, name)
        check(isinstance(value, dict) and bool(value), f"json_parse:{name}")
    for name in MD_FILES:
        try:
            check(bool((ROOT / name).read_text(encoding="utf-8").strip()), f"markdown_nonempty:{name}")
        except OSError:
            check(False, f"markdown_read:{name}")
    try:
        ast.parse((ROOT / VERIFIER).read_text(encoding="utf-8"))
        check(True, "verifier_ast")
    except (OSError, SyntaxError):
        check(False, "verifier_ast")

    mapping = load(assets, "existing_asset_mapping.json")
    records = mapping.get("mappings", [])
    by_asset = {item.get("asset"): item for item in records}
    check(mapping.get("scan_mode") == "baseline_first_targeted_read_only" and len(mapping.get("baseline_refs", [])) >= 7, "baseline_first_scan")
    check(all((REPO_ROOT / ref).exists() for ref in mapping.get("baseline_refs", [])), "baseline_refs_exist")
    check(len(records) >= 16 and all(item.get("current_location") and item.get("current_owner") and item.get("current_status") and item.get("v2_position") and item.get("disposition") and isinstance(item.get("migration_needed"), bool) and isinstance(item.get("rewrite_required"), bool) and item.get("reason") for item in records), "mapping_fields")
    check({"Field State Reducer", "Observation Manager", "Cognitive Attention", "Self and Social Self", "Role System", "Relationship System", "Memory System", "Cognitive Intent Architecture", "Cognitive Causality Model", "Luna V2 Cognitive Object Model", "Cognitive Experience Compression", "Emotion Context", "Decision Arbitration", "Task Manager", "Model Manager", "Action Boundary and Runtime"} <= set(by_asset), "mapping_coverage")
    check(by_asset.get("Cognitive Intent Architecture", {}).get("disposition") == "reuse_and_align" and by_asset.get("Cognitive Causality Model", {}).get("disposition") == "reuse_and_extend" and by_asset.get("Cognitive Experience Compression", {}).get("disposition") == "reuse_and_align", "existing_architecture_reuse")
    check(by_asset.get("Task Manager", {}).get("v2_position") == "Task lifecycle and capability-routing orchestration" and by_asset.get("Model Manager", {}).get("current_owner") == "Capability Governance", "task_model_boundaries")
    check(mapping.get("new_integration_constructs") == ["Personal Cognitive Network"] and set(mapping.get("existing_architecture_to_align", [])) == {"Intent Processing", "Causal Network", "Experience Compression"}, "new_vs_existing")
    check(mapping.get("qualitative_reuse_estimate") == 0.8 and mapping.get("estimate_is_not_inventory_count") is True and mapping.get("read_only") is True and mapping.get("no_move") is True and mapping.get("no_delete") is True and mapping.get("no_code_change") is True, "mapping_boundary")

    registry = load(assets, "canonical_component_registry_v2.json")
    components = registry.get("components", [])
    ids = [item.get("id") for item in components]
    check(registry.get("status") == "canonical_freeze_candidate" and len(components) >= 19 and len(ids) == len(set(ids)), "component_registry")
    check(all(item.get("owner") and item.get("responsibility") and isinstance(item.get("candidate_only"), bool) for item in components), "component_fields")
    check({"personal_cognitive_network", "causal_network", "intent_processing", "intent_evaluation_gate", "decision_arbitration", "task_manager", "action", "experience_compression", "emotion_context", "value_utility", "model_manager"} <= set(ids), "component_coverage")
    check(registry.get("unique_owner_per_responsibility") is True and registry.get("active_baseline_replacement") is False and registry.get("runtime_activation") is False, "registry_boundary")

    network = load(assets, "personal_cognitive_network_boundary.json")
    check(network.get("owner") == "Personal Cognitive Network Governance" and set(network.get("owns", [])) >= {"typed link candidates", "activation weight candidates", "context projection candidates", "network topology revisions", "network trace and provenance"}, "personal_network_owner")
    check(set(network.get("does_not_own", [])) >= {"Self Identity", "Role Lifecycle", "Relationship Truth", "Memory Persistence", "Emotion State", "Value Evaluation", "Intent", "Decision", "Action", "Reality"}, "personal_network_non_owners")
    check(set(network.get("required_fields", [])) >= {"network_object_id", "source_object_refs", "edge_type", "field_scope", "perspective_scope", "temporal_validity", "activation_weight", "evidence_refs", "counter_evidence_refs", "confidence", "candidate_only", "not_fact", "revision", "revoked", "trace_refs", "unresolved_fields"}, "personal_network_fields")
    check(network.get("source_owner_precedence") is True and network.get("field_activation_required") is True and network.get("candidate_only") is True and network.get("not_fact") is True and network.get("direct_memory_write") is False and network.get("direct_self_write") is False and network.get("automatic_evolution") is False and network.get("runtime") is False, "personal_network_boundary")

    intent = load(assets, "intent_and_gate_boundary.json")
    check(intent.get("intent_owner") == "Intent Governance" and intent.get("gate_owner") == "Cognitive Routing Governance" and intent.get("reused_architecture") == "docs/architecture/cognitive_intent_architecture_v1/", "intent_gate_owners")
    check(set(intent.get("intent_outputs", [])) >= {"Intent Candidate", "Intent Conflict Candidate", "Clarification Candidate", "Goal Alignment Candidate"} and set(intent.get("gate_outputs", [])) >= {"Direct Response Candidate", "Cognitive Expansion Candidate", "Clarification Candidate", "Defer Candidate", "Reject Candidate"}, "intent_gate_outputs")
    check(intent.get("direct_response_is_not_action") is True and intent.get("cognitive_expansion_is_not_b_route_execution") is True and intent.get("gate_is_not_decision_owner") is True and intent.get("intent_is_not_goal_owner") is True and intent.get("intent_is_not_task_owner") is True and intent.get("candidate_only") is True and intent.get("automatic_goal_generation") is False and intent.get("runtime") is False, "intent_gate_boundary")

    causal = load(assets, "causal_network_boundary.json")
    check(causal.get("owner") == "Causal Reasoning Governance" and len(causal.get("reused_assets", [])) >= 3 and set(causal.get("node_types", [])) >= {"Person", "Event", "Role", "Relationship", "State", "Goal", "Field", "Experience"}, "causal_network_model")
    check(set(causal.get("edge_types", [])) >= {"Influence", "Temporal", "Benefit", "Cost", "Condition", "Counter Evidence", "Role Projection"} and set(causal.get("outputs", [])) >= {"Causal Candidate", "Causal Projection Candidate", "Future State Candidate", "Decision Evaluation Candidate", "Unknown Candidate"}, "causal_network_contract")
    check(causal.get("evidence_required") is True and causal.get("counter_evidence_preserved") is True and causal.get("temporal_validity_required") is True and causal.get("candidate_only") is True and causal.get("not_fact") is True and causal.get("not_knowledge_base") is True and causal.get("not_rule_engine") is True and causal.get("graph_execution") is False and causal.get("simulation_runtime") is False and causal.get("decision_authority") is False and causal.get("action_authority") is False, "causal_boundary")

    field = load(assets, "field_activation_contract.json")
    check(field.get("field_owner") == "Field System" and field.get("network_owner") == "Personal Cognitive Network Governance" and set(field.get("outputs", [])) >= {"Field Context Projection Candidate", "Network Activation Candidate", "Related Field Candidate", "Unknown Activation Candidate"}, "field_activation")
    check(field.get("field_state_reducer_mainline_preserved") is True and field.get("field_is_not_location_only") is True and field.get("activation_does_not_modify_source_objects") is True and field.get("activation_does_not_write_memory") is True and field.get("activation_does_not_create_intent") is True and field.get("candidate_only") is True and field.get("runtime") is False, "field_activation_boundary")

    experience = load(assets, "experience_evolution_boundary.json")
    check(experience.get("experience_owner") == "Experience Governance" and experience.get("memory_owner") == "Memory System" and experience.get("network_owner") == "Personal Cognitive Network Governance" and experience.get("learning_owner") == "Learning Governance / Self Review", "experience_owners")
    check(experience.get("flow") == ["Feedback", "Reality Validation", "Outcome Evaluation", "Experience Candidate", "Experience Compression Candidate", "Memory Candidate", "Network Evolution Candidate", "Self Review", "Admission", "Future Application"], "experience_flow")
    check(experience.get("single_outcome_is_not_network_evolution") is True and experience.get("repeated_evidence_required") is True and experience.get("memory_admission_required") is True and experience.get("self_review_required") is True and experience.get("direct_memory_write") is False and experience.get("direct_network_mutation") is False and experience.get("automatic_learning") is False and experience.get("model_training") is False and experience.get("candidate_only") is True and experience.get("runtime") is False, "experience_boundary")

    ownership = load(assets, "ownership_alignment.json")
    owner_records = ownership.get("records", [])
    responsibilities = [item.get("responsibility") for item in owner_records]
    check(ownership.get("unique_owner_required") is True and len(owner_records) >= 17 and len(responsibilities) == len(set(responsibilities)) and all(item.get("owner") and item.get("consumers") for item in owner_records), "ownership_alignment")
    check(ownership.get("personal_network_does_not_absorb_source_owners") is True and ownership.get("task_manager_is_not_action_owner") is True and ownership.get("emotion_is_not_value_owner") is True and ownership.get("intent_is_not_decision_owner") is True, "ownership_boundaries")

    risks = load(assets, "duplicate_owner_risk_registry.json")
    risk_ids = {item.get("risk_id") for item in risks.get("risks", [])}
    check({"personal_network_vs_self", "personal_network_vs_memory", "intent_engine_duplicate", "causal_engine_duplicate", "observation_attention_vs_cognitive_attention", "task_manager_vs_action", "emotion_vs_value", "intent_gate_vs_decision", "field_adapter_vs_reducer"} <= risk_ids, "duplicate_risk_coverage")
    check(all(item.get("canonical_owner") and item.get("resolution") and item.get("severity") for item in risks.get("risks", [])) and risks.get("delete_or_merge_authorized") is False and risks.get("owner_change_authorized") is False and risks.get("runtime_change_authorized") is False, "duplicate_risk_boundary")

    impact = load(assets, "architecture_change_impact_registry.json")
    check(len(impact.get("impacts", [])) >= 11 and all(item.get("area") and item.get("impact") and item.get("current_phase_action") and item.get("risk") for item in impact.get("impacts", [])), "impact_registry")
    check(impact.get("existing_documents_modified") is False and impact.get("existing_code_modified") is False and impact.get("future_change_control_required") is True, "impact_boundary")

    migration = load(assets, "migration_sequence.json")
    stages = migration.get("stages", [])
    check([item.get("priority") for item in stages] == ["P0", "P1", "P2", "P3", "P4"] and all(item.get("name") and item.get("deliverables") for item in stages), "migration_sequence")
    check(migration.get("order_fixed") is True and migration.get("mapping_before_migration") is True and migration.get("adapter_before_rewrite") is True and migration.get("owner_before_implementation") is True and migration.get("current_phase_executes_migration") is False, "migration_boundary")

    phase = load(assets, "phase_contract.json")
    required_phase_fields = {"Phase", "Stage", "Execution Mode", "Current Work Description", "Previous Phase", "Previous Phase Decision", "Input Assets", "Required Pre-Read", "Target Directory", "Scope", "Out Of Scope", "Required Final Files", "Implementation Principles", "Required Checks", "Negative Guards", "Verification Authority", "Allowed Agent Checks", "Allowed Agent Execution", "Prohibited Agent Execution", "Agent Stop Point", "User Terminal Commands", "Expected Success Decision", "Expected Next", "Expected Failure Decision", "Expected Failure Next", "Stop Condition", "Blocker Conditions", "Completion Report Format", "Current Status Contract"}
    check(required_phase_fields <= set(phase), "phase_required_fields")
    check(phase.get("Phase") == "Phase-Luna-Dynamic-Cognitive-Architecture-Realignment-Planning-v1-001" and phase.get("Execution Mode") == "Planning Only" and phase.get("Previous Phase Decision") == "LUNA_SELF_REGULATION_FUNCTION_ENHANCEMENT_READY", "phase_identity")
    check(phase.get("Verification Authority") == {"V0": "Agent", "V1": "Not Authorized", "V2": "User Terminal Only", "V3": "ChatGPT Only"} and phase.get("Agent Stop Point") == "WAITING_FOR_USER_TERMINAL_VERIFICATION" and phase.get("Current Status Contract") == "WAITING_FOR_USER_TERMINAL_VERIFICATION", "phase_authority")
    check(phase.get("User Terminal Commands") == ["python3 docs/architecture/luna_dynamic_cognitive_architecture_realignment_planning_v1/verify_dynamic_cognitive_architecture_realignment_planning_v1.py"] and phase.get("Expected Success Decision") == "V2_FINAL_VERIFICATION_PASSED" and phase.get("Expected Next") == "RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT", "phase_terminal_contract")
    check(phase.get("Expected Failure Decision") == "BLOCKED_BY_VERIFIER_FAILURE" and phase.get("Expected Failure Next") == "REMEDIATE_REPORTED_FAILURES_ONLY" and "run final phase verifier" in phase.get("Prohibited Agent Execution", []), "phase_failure_boundary")

    guards = load(assets, "negative_guards.json")
    required_guards = {"runtime", "code_change", "existing_document_rewrite", "file_move", "file_rename", "file_delete", "database_selection", "network_call", "model_provider_integration", "automatic_learning", "automatic_network_evolution", "causal_graph_execution", "emotion_runtime", "b_route_runtime", "decision_execution", "action_execution", "personal_network_self_ownership", "personal_network_memory_ownership", "intent_duplicate_owner", "causal_duplicate_owner", "task_manager_action_ownership", "emotion_value_ownership", "intent_gate_decision_ownership", "causal_candidate_fact_promotion", "no_check_weaken", "no_hardcoded_pass"}
    check(required_guards <= set(guards.get("forbidden", [])), "negative_guards")
    check(all(guards.get("invariants", {}).get(key) is True for key in ("planning_only", "baseline_first", "passed_assets_preserved", "unique_owner_per_responsibility", "personal_network_is_projection_owner", "intent_architecture_reused", "causality_architecture_reused", "memory_owner_preserved", "task_manager_is_not_action_executor", "emotion_is_not_value_owner", "candidate_fact_boundary_preserved", "unknowns_preserved")), "negative_invariants")

    summary = load(assets, "summary.json")
    check(summary.get("status") == "planning_only" and summary.get("readiness_token") == READY and summary.get("architecture_v2_candidate") is True and summary.get("active_baseline_replaced") is False, "summary_status")
    check(all(summary.get(key) is True for key in ("existing_asset_mapping_complete", "module_boundary_update_complete", "migration_plan_complete", "unique_owner_alignment_complete", "personal_cognitive_network_positioned", "intent_existing_asset_reused", "causality_existing_assets_reused", "experience_compression_existing_asset_reused", "field_reducer_mainline_preserved", "observation_manager_mainline_preserved", "task_manager_mainline_preserved", "model_manager_mainline_preserved", "memory_owner_preserved", "decision_owner_preserved", "action_owner_preserved")), "summary_model")
    check(summary.get("qualitative_reuse_estimate") == 0.8 and all(summary.get(key) is False for key in ("runtime", "code_change", "existing_document_modification", "file_move", "file_delete", "automatic_learning", "automatic_network_evolution", "causal_graph_execution", "emotion_runtime", "b_route_runtime", "decision_execution", "action_execution")), "summary_boundary")
    check(summary.get("recommended_next_phase") == "Phase-Luna-Intent-Processing-And-Evaluation-Gate-Alignment-Planning-v1-001" and summary.get("next_phase_is_not_automatic") is True, "summary_next")

    forbidden_imports = {"subprocess", "socket", "requests", "cv2", "torch", "transformers", "sqlite3", "psycopg2"}
    try:
        tree = ast.parse((ROOT / VERIFIER).read_text(encoding="utf-8"))
        imports: set[str] = set()
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
        print("READINESS: LUNA_DYNAMIC_COGNITIVE_ARCHITECTURE_REALIGNMENT_REMEDIATION_REQUIRED")
        print("NEXT: REMEDIATE_REPORTED_FAILURES_ONLY")
        return 1
    print("FINAL_DECISION: V2_FINAL_VERIFICATION_PASSED")
    print(f"READINESS: {READY}")
    print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
