"""V0 static verifier for architecture alignment migration validation planning."""
from __future__ import annotations

import ast
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parents[2]
JSON_FILES = [
    "migration_record_schema.json",
    "controlled_migration_contract.json",
    "architecture_integrity_check_contract.json",
    "asset_ownership_check_contract.json",
    "boundary_integrity_check_contract.json",
    "cognitive_chain_integrity_contract.json",
    "regression_capability_registry.json",
    "regression_check_contract.json",
    "migration_compatibility_matrix.json",
    "architecture_freeze_decision_contract.json",
    "stage_gate_registry.json",
    "owner_preservation_contract.json",
    "route_supersession_mapping.json",
    "phase_contract.json",
    "negative_guards.json",
    "summary.json",
]
MD_FILES = [
    "architecture_alignment_migration_strategy.md",
    "controlled_architecture_migration_plan.md",
    "migration_integrity_validation_architecture.md",
    "architecture_freeze_gate.md",
    "summary.md",
]
VERIFIER = "verify_architecture_alignment_migration_validation_planning_v1.py"
READY = "LUNA_DYNAMIC_COGNITIVE_ARCHITECTURE_ALIGNMENT_MIGRATION_VALIDATION_PLAN_READY"


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
    files = {path.name for path in ROOT.iterdir() if path.is_file()}
    check(expected <= files, "required_assets")
    check({path.name for path in ROOT.glob("*.py")} == {VERIFIER}, "no_runtime_python")

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

    record = load(assets, "migration_record_schema.json")
    check(set(record.get("required_fields", [])) >= {"migration_id", "old_module", "old_path", "old_owner", "new_position", "target_owner", "migration_type", "compatibility_checks", "before_evidence_refs", "after_evidence_refs", "rollback_plan", "legacy_compatibility", "status", "blockers", "trace_ref"}, "migration_record_fields")
    check(set(record.get("migration_types", [])) == {"keep", "boundary_update", "adapter", "rename_candidate", "move_candidate"}, "migration_types")
    check(set(record.get("compatibility_dimensions", [])) >= {"public_api", "schema", "owner", "dependency", "candidate_fact_semantics", "trace_replay", "behavior", "documentation", "import_path", "rollback"}, "compatibility_dimensions")
    check(record.get("rename_candidate_is_not_rename_authority") is True and record.get("move_candidate_is_not_move_authority") is True and record.get("single_owner_required") is True and record.get("before_after_evidence_required") is True and record.get("rollback_required") is True and record.get("candidate_only") is True, "migration_record_boundary")

    migration = load(assets, "controlled_migration_contract.json")
    check(set(migration.get("inputs", [])) >= {"Architecture v2 Candidate", "Existing Asset Mapping", "Canonical Owner Registry", "Module Baseline", "Compatibility Contract", "Rollback Plan", "Migration Authorization"}, "migration_inputs")
    check(migration.get("flow") == ["Resolve Asset", "Resolve Owner", "Select Migration Type", "Define Compatibility", "Define Rollback", "Authorize Separately", "Execute in Authorized Phase", "Collect Evidence", "Integrity Validation Handoff"], "migration_flow")
    check(migration.get("mapping_before_migration") is True and migration.get("owner_before_migration") is True and migration.get("compatibility_before_mutation") is True and migration.get("rollback_before_mutation") is True and migration.get("one_asset_slice_per_phase") is True and migration.get("parallel_mainline_forbidden") is True, "migration_principles")
    check(migration.get("current_phase_executes_migration") is False and migration.get("runtime") is False and migration.get("candidate_only") is True, "migration_boundary")

    architecture = load(assets, "architecture_integrity_check_contract.json")
    required_nodes = {"Field", "Personal Cognitive Network", "Role", "Relationship", "Experience", "Intent", "Causal", "Decision", "Action"}
    check(required_nodes == set(architecture.get("required_nodes", [])), "architecture_nodes")
    check(set(architecture.get("required_node_fields", [])) >= {"node_id", "canonical_owner", "status", "source_assets", "target_position", "dependency_contract", "compatibility_result"}, "architecture_node_fields")
    check(set(architecture.get("allowed_statuses", [])) == {"aligned", "preserved", "adapted", "blocked", "retired_candidate"}, "architecture_statuses")
    check(architecture.get("unassigned_owner_forbidden") is True and architecture.get("tbd_status_forbidden") is True and architecture.get("duplicate_node_owner_forbidden") is True and architecture.get("missing_node_blocks_freeze") is True and architecture.get("blocked_node_requires_resolution_or_governance_acceptance") is True and architecture.get("candidate_only") is True, "architecture_integrity_boundary")

    ownership = load(assets, "asset_ownership_check_contract.json")
    required_assets = {"Field State Reducer", "Observation Manager", "Cognitive Attention", "Self", "Role System", "Relationship System", "Memory System", "Intent Architecture", "Causality Architecture", "Experience Compression", "Decision Arbitration", "Task Manager", "Action Boundary/Runtime", "Model Manager", "OCR Pipeline", "Vision Pipeline", "Protocol Manager"}
    check(required_assets == set(ownership.get("required_assets", [])), "ownership_asset_coverage")
    assignments = ownership.get("canonical_assignments", {})
    check(set(assignments) == required_assets and assignments.get("Memory System") == "Memory System" and assignments.get("Task Manager") == "Task Manager" and assignments.get("Model Manager") == "Capability Governance" and assignments.get("Field State Reducer") == "Field System", "canonical_assignments")
    check(ownership.get("personal_network_owner_scope") == ["typed cross-object links", "activation projections", "network topology revisions"] and ownership.get("memory_projection_does_not_transfer_memory_ownership") is True, "projection_owner_boundary")
    check(ownership.get("no_asset_left_for_later") is True and ownership.get("unique_owner_required") is True and ownership.get("owner_change_requires_governance") is True, "ownership_integrity_boundary")

    boundary = load(assets, "boundary_integrity_check_contract.json")
    required_edges = {"Task Manager -> Causal Judgment", "Task Manager -> Action Execution", "Model Manager -> Cognitive Conclusion", "Model Manager -> Decision Authority", "OCR/Vision -> Direct Fact Promotion", "Memory -> Direct Cognitive Core Mutation", "Memory -> Reality Override", "Personal Cognitive Network -> Self Ownership", "Personal Cognitive Network -> Memory Ownership", "Intent -> Decision Execution", "Causal -> Fact Promotion", "Causal -> Action Execution", "Emotion -> Value Ownership", "B Route -> A Route State Mutation"}
    check(required_edges <= set(boundary.get("forbidden_authority_edges", [])), "boundary_forbidden_edges")
    check(set(boundary.get("required_boundaries", [])) >= {"candidate_fact_admission", "decision_action_separation", "memory_network_separation", "task_action_separation", "model_cognition_separation", "perceptual_cognitive_attention_separation", "a_b_route_separation"}, "required_boundaries")
    check(boundary.get("unique_owner_required") is True and boundary.get("boundary_violation_blocks_freeze") is True and boundary.get("runtime_authority_change_forbidden") is True and boundary.get("candidate_only") is True, "boundary_integrity")

    chain = load(assets, "cognitive_chain_integrity_contract.json")
    check(chain.get("required_chain") == ["Input", "Environment Understanding", "Field", "Intent", "Context Retrieval / Personal Cognitive Network Projection", "A/B Route Boundary", "Decision", "Action", "Feedback", "Experience"], "cognitive_chain")
    check(set(chain.get("required_edge_fields", [])) >= {"edge_id", "producer", "consumer", "contract_ref", "input_schema_ref", "output_schema_ref", "candidate_fact_semantics", "failure_behavior", "trace_ref", "compatibility_result"}, "chain_edge_fields")
    check(chain.get("all_edges_required") is True and chain.get("producer_consumer_required") is True and chain.get("candidate_fact_semantics_required") is True and chain.get("failure_behavior_required") is True and chain.get("trace_required") is True and chain.get("broken_edge_blocks_freeze") is True and chain.get("a_b_route_is_boundary_not_runtime") is True and chain.get("action_requires_action_boundary") is True, "chain_boundary")

    regression_registry = load(assets, "regression_capability_registry.json")
    capabilities = regression_registry.get("capabilities", [])
    capability_names = {item.get("capability") for item in capabilities}
    check(capability_names == {"Vision Pipeline", "OCR Pipeline", "Model Admission", "Task Manager", "Field State Reducer", "Protocol Manager"}, "regression_capabilities")
    check(all(item.get("owner") and item.get("baseline_ref") and item.get("checks") and item.get("required") is True for item in capabilities), "regression_registry_fields")
    check(all((REPO_ROOT / item.get("baseline_ref", "missing")).exists() for item in capabilities), "regression_baselines_exist")
    check(regression_registry.get("all_required") is True and regression_registry.get("baseline_evidence_required") is True and regression_registry.get("missing_regression_result_blocks_freeze") is True and regression_registry.get("current_phase_runs_regression") is False, "regression_registry_boundary")

    regression = load(assets, "regression_check_contract.json")
    check(set(regression.get("dimensions", [])) >= {"availability", "public_api", "schema", "behavior", "owner", "candidate_fact_boundary", "trace_replay", "dependency", "documentation"}, "regression_dimensions")
    check(set(regression.get("result_statuses", [])) == {"passed", "failed", "blocked", "not_run"}, "regression_statuses")
    check(regression.get("all_mandatory_results_must_be_passed") is True and regression.get("not_run_blocks_freeze") is True and regression.get("failed_blocks_freeze") is True and regression.get("baseline_mutation_forbidden") is True and regression.get("check_weakening_forbidden") is True and regression.get("current_phase_executes_checks") is False, "regression_boundary")

    matrix = load(assets, "migration_compatibility_matrix.json")
    rows = matrix.get("rows", [])
    row_names = {item.get("asset") for item in rows}
    check({"Field State Reducer", "Observation Manager", "Cognitive Attention", "Memory System", "Role System", "Relationship System", "Intent Architecture", "Causality Architecture", "Task Manager", "Model Manager", "OCR / Vision", "Protocol Manager"} == row_names, "compatibility_matrix_coverage")
    check(all(item.get("migration_type") in {"keep", "boundary_update", "adapter"} and item.get("new_position") and item.get("owner_preserved") is True and item.get("required_checks") for item in rows), "compatibility_matrix_fields")
    check(matrix.get("all_owner_preserved") is True and matrix.get("physical_moves_planned") is False and matrix.get("renames_planned") is False and matrix.get("current_phase_changes_assets") is False, "compatibility_matrix_boundary")

    freeze = load(assets, "architecture_freeze_decision_contract.json")
    check(set(freeze.get("inputs", [])) >= {"Closed Migration Records", "Architecture Integrity Result", "Asset Ownership Result", "Boundary Integrity Result", "Cognitive Chain Result", "Regression Results", "Documentation Consistency Result", "Rollback Evidence", "Unresolved Risk Registry"}, "freeze_inputs")
    check(set(freeze.get("mandatory_conditions", [])) >= {"all_required_nodes_present", "all_assets_assigned", "unique_owners", "no_dual_mainline", "all_chain_edges_closed", "all_boundary_checks_passed", "all_required_regressions_passed", "documentation_code_mapping_consistent", "rollback_verified", "unresolved_risks_governed"}, "freeze_conditions")
    check(set(freeze.get("allowed_decisions", [])) == {"freeze_candidate", "remediation_required", "blocked"} and freeze.get("freeze_does_not_modify_baseline") is True and freeze.get("freeze_does_not_start_next_phase") is True and freeze.get("integrity_validation_required") is True and freeze.get("user_v2_required") is True and freeze.get("chatgpt_v3_required") is True and freeze.get("candidate_only") is True, "freeze_boundary")

    gates = load(assets, "stage_gate_registry.json")
    stages = gates.get("stages", [])
    check([item.get("stage") for item in stages] == ["P0", "P1", "P2", "P3", "P4", "P5", "P6", "P7"], "stage_sequence")
    check(all(item.get("name") and item.get("exit_gate") and item.get("next") for item in stages), "stage_gate_fields")
    check(gates.get("no_stage_skip") is True and gates.get("p3_mandatory") is True and gates.get("p4_mandatory") is True and gates.get("next_stage_not_automatic") is True, "stage_gate_boundary")

    owner = load(assets, "owner_preservation_contract.json")
    invariants = owner.get("invariants", [])
    check(len(invariants) >= 7 and all(item.get("source") and item.get("projection") and item.get("target") and item.get("owner_after") and item.get("ownership_transfer") is False for item in invariants), "owner_preservation_records")
    check(owner.get("personal_network_is_projection_owner_only") is True and owner.get("task_manager_is_not_action_owner") is True and owner.get("model_manager_is_not_cognitive_owner") is True and owner.get("evidence_provider_is_not_fact_owner") is True and owner.get("owner_change_requires_explicit_governance") is True, "owner_preservation_boundary")

    supersession = load(assets, "route_supersession_mapping.json")
    check((REPO_ROOT / supersession.get("source_plan", "missing")).exists() and supersession.get("source_plan_preserved") is True and supersession.get("source_plan_modified") is False, "route_source_preserved")
    check(supersession.get("new_route") == ["Architecture Planning", "Asset Mapping", "Controlled Architecture Alignment Migration", "Migration Integrity Validation", "Architecture Freeze Decision", "Intent Planning", "Personal Cognitive Network Skeleton", "Causal Reasoning Skeleton"], "route_supersession")
    check(set(supersession.get("added_mandatory_gates", [])) == {"Migration Integrity Validation", "Architecture Freeze Decision"} and supersession.get("supersession_type") == "planning_amendment" and supersession.get("retroactive_asset_mutation") is False and supersession.get("next_phase_automatic") is False, "route_boundary")

    phase = load(assets, "phase_contract.json")
    required_phase_fields = {"Phase", "Stage", "Execution Mode", "Current Work Description", "Previous Phase", "Previous Phase Decision", "Input Assets", "Required Pre-Read", "Target Directory", "Scope", "Out Of Scope", "Required Final Files", "Implementation Principles", "Required Checks", "Negative Guards", "Verification Authority", "Allowed Agent Checks", "Allowed Agent Execution", "Prohibited Agent Execution", "Agent Stop Point", "User Terminal Commands", "Expected Success Decision", "Expected Next", "Expected Failure Decision", "Expected Failure Next", "Stop Condition", "Blocker Conditions", "Completion Report Format", "Current Status Contract"}
    check(required_phase_fields <= set(phase), "phase_required_fields")
    check(phase.get("Phase") == "Phase-Luna-Dynamic-Cognitive-Architecture-Alignment-Migration-Validation-Planning-v1-001" and phase.get("Execution Mode") == "Planning Only" and phase.get("Previous Phase Decision") == "LUNA_DYNAMIC_COGNITIVE_ARCHITECTURE_REALIGNMENT_PLAN_READY", "phase_identity")
    check(phase.get("Verification Authority") == {"V0": "Agent", "V1": "Not Authorized", "V2": "User Terminal Only", "V3": "ChatGPT Only"} and phase.get("Agent Stop Point") == "WAITING_FOR_USER_TERMINAL_VERIFICATION" and phase.get("Current Status Contract") == "WAITING_FOR_USER_TERMINAL_VERIFICATION", "phase_authority")
    check(phase.get("User Terminal Commands") == ["python3 docs/architecture/luna_dynamic_cognitive_architecture_alignment_migration_validation_planning_v1/verify_architecture_alignment_migration_validation_planning_v1.py"] and phase.get("Expected Success Decision") == "V2_FINAL_VERIFICATION_PASSED" and phase.get("Expected Next") == "RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT", "phase_terminal_contract")
    check(phase.get("Expected Failure Decision") == "BLOCKED_BY_VERIFIER_FAILURE" and phase.get("Expected Failure Next") == "REMEDIATE_REPORTED_FAILURES_ONLY" and "run final phase verifier" in phase.get("Prohibited Agent Execution", []), "phase_failure_boundary")

    guards = load(assets, "negative_guards.json")
    required_guards = {"migration_execution", "runtime", "code_change", "passed_asset_modification", "file_move", "file_rename", "file_delete", "baseline_activation", "architecture_freeze_activation", "regression_execution", "database_access", "network_call", "model_provider_call", "device_control", "stage_skip", "p2_to_p4_without_p3", "unassigned_asset", "tbd_owner", "dual_mainline", "projection_owner_transfer", "memory_owner_transfer", "task_manager_action_authority", "model_manager_cognitive_authority", "ocr_vision_direct_fact", "memory_direct_core_mutation", "intent_decision_execution", "causal_fact_promotion", "causal_action_execution", "check_weakening", "hardcoded_pass", "automatic_next_phase"}
    check(required_guards <= set(guards.get("forbidden", [])), "negative_guards")
    check(all(guards.get("invariants", {}).get(key) is True for key in ("planning_only", "alignment_not_replacement", "passed_assets_preserved", "migration_record_required", "compatibility_required", "rollback_required", "architecture_integrity_required", "ownership_integrity_required", "boundary_integrity_required", "cognitive_chain_integrity_required", "regression_integrity_required", "p3_mandatory", "p4_mandatory", "unique_owners_preserved", "unknowns_and_blockers_preserved")), "negative_invariants")

    summary = load(assets, "summary.json")
    check(summary.get("status") == "planning_only" and summary.get("readiness_token") == READY and summary.get("route_amended") is True, "summary_status")
    check(all(summary.get(key) is True for key in ("alignment_migration_defined", "migration_record_defined", "architecture_integrity_defined", "asset_ownership_integrity_defined", "boundary_integrity_defined", "cognitive_chain_integrity_defined", "regression_integrity_defined", "architecture_freeze_gate_defined", "p3_mandatory", "p4_mandatory", "personal_network_projection_owner_only", "memory_owner_preserved", "task_manager_orchestration_only", "action_owner_preserved", "model_manager_capability_owner_preserved", "evidence_fact_boundary_preserved")), "summary_model")
    check(all(summary.get(key) is False for key in ("runtime", "migration_execution", "regression_execution", "code_change", "passed_asset_modification", "file_move", "file_rename", "file_delete", "baseline_activation", "freeze_activation", "next_phase_automatic")), "summary_boundary")
    check(summary.get("planned_route") == ["P0 Architecture Planning", "P1 Asset Mapping", "P2 Controlled Alignment Migration", "P3 Migration Integrity Validation", "P4 Architecture Freeze Decision", "P5 Intent Planning", "P6 Personal Cognitive Network Skeleton", "P7 Causal Reasoning Skeleton"] and summary.get("future_immediate_phase_after_governance") == "Phase-Luna-Controlled-Architecture-Alignment-Migration-Planning-v1-001", "summary_route")

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
        print("READINESS: LUNA_DYNAMIC_COGNITIVE_ARCHITECTURE_ALIGNMENT_MIGRATION_VALIDATION_REMEDIATION_REQUIRED")
        print("NEXT: REMEDIATE_REPORTED_FAILURES_ONLY")
        return 1
    print("FINAL_DECISION: V2_FINAL_VERIFICATION_PASSED")
    print(f"READINESS: {READY}")
    print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
