"""V0 static verifier for Luna Cognitive Self Model Architecture.

Planning Only: validates the self-state, awareness, resource, context,
boundary, interface, lifecycle, and dependency contracts. It does not import
or execute runtime, learning, model, hardware, emotion, social, or action code.
"""

from __future__ import annotations

import ast
import json
import sys
from pathlib import Path


BASE = Path(__file__).resolve().parent
JSON_ASSETS = (
    "self_state_schema_v1.json",
    "self_capability_awareness_contract_v1.json",
    "self_limitation_awareness_contract_v1.json",
    "self_resource_awareness_contract_v1.json",
    "self_context_awareness_contract_v1.json",
    "self_boundary_awareness_contract_v1.json",
    "self_history_reference_contract_v1.json",
    "self_model_update_contract_v1.json",
    "self_model_lifecycle_v1.json",
    "self_model_memory_interface_v1.json",
    "self_model_learning_interface_v1.json",
    "self_model_brain_interface_v1.json",
    "self_model_action_interface_v1.json",
    "self_model_dependency_boundary_v1.json",
)
MD_ASSETS = (
    "luna_cognitive_self_model_architecture_v1.md",
    "self_model_whitebox_v1.md",
    "self_model_go_no_go_v1.md",
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

    state = data.get("self_state_schema_v1.json", {})
    capability = data.get("self_capability_awareness_contract_v1.json", {})
    limitation = data.get("self_limitation_awareness_contract_v1.json", {})
    resource = data.get("self_resource_awareness_contract_v1.json", {})
    context = data.get("self_context_awareness_contract_v1.json", {})
    boundary = data.get("self_boundary_awareness_contract_v1.json", {})
    history = data.get("self_history_reference_contract_v1.json", {})
    update = data.get("self_model_update_contract_v1.json", {})
    lifecycle = data.get("self_model_lifecycle_v1.json", {})
    memory = data.get("self_model_memory_interface_v1.json", {})
    learning = data.get("self_model_learning_interface_v1.json", {})
    brain = data.get("self_model_brain_interface_v1.json", {})
    action = data.get("self_model_action_interface_v1.json", {})
    dependency = data.get("self_model_dependency_boundary_v1.json", {})

    check({"self_state_id", "timestamp", "current_context", "active_task", "runtime_status", "confidence"}.issubset(set(state.get("schema", []))), "self_state_schema")
    check(state.get("rules", {}).get("state_is_dynamic") is True, "self_state_dynamic")
    check(state.get("rules", {}).get("identity_separate") is True, "self_state_identity_boundary")
    check(state.get("rules", {}).get("unknown_preserved") is True, "self_state_unknown")

    check({"Self Capability Profile", "Capability State", "Performance Evidence", "Field Context", "Condition"}.issubset(set(capability.get("inputs", []))), "capability_awareness_inputs")
    check(capability.get("output") == "Current Capability Awareness", "capability_awareness_output")
    check({"capability", "context", "condition", "availability", "confidence", "limitation", "unknown"}.issubset(set(capability.get("schema", []))), "capability_awareness_schema")
    check(capability.get("rules", {}).get("context_bound") is True, "capability_awareness_context")
    check(capability.get("rules", {}).get("provider_not_authority") is True, "capability_provider_boundary")
    check(capability.get("rules", {}).get("decision_reference_only") is True, "capability_reference_only")

    check({"limitation", "boundary", "confidence", "affected_area", "Unknown"}.issubset(set(limitation.get("inputs", []))), "limitation_inputs")
    check(limitation.get("output") == "Current Limitation Awareness", "limitation_output")
    check({"limitation", "boundary", "confidence", "affected_area", "condition", "unknown"}.issubset(set(limitation.get("schema", []))), "limitation_schema")
    check(limitation.get("rules", {}).get("limitation_not_identity") is True, "limitation_identity_boundary")
    check(limitation.get("rules", {}).get("boundary_explicit") is True, "limitation_boundary_explicit")
    check(limitation.get("rules", {}).get("permission_not_inferred") is True, "limitation_no_permission_inference")

    check({"Compute", "Energy", "Communication", "Perception"}.issubset(set(resource.get("resource_domains", []))), "resource_domains")
    check({"Resource State", "Hardware Capability State", "Runtime Resource Snapshot"}.issubset(set(resource.get("inputs", []))), "resource_inputs")
    check({"resource", "available", "usage", "constraint", "timestamp", "confidence"}.issubset(set(resource.get("schema", []))), "resource_schema")
    check(resource.get("rules", {}).get("read_only_context") is True, "resource_read_only")
    check(resource.get("rules", {}).get("constraint_explicit") is True, "resource_constraint")

    check({"Field", "Workspace", "Intent", "Goal", "Task"}.issubset(set(context.get("inputs", []))), "context_inputs")
    check(context.get("output") == "Current Self Context", "context_output")
    check(context.get("rules", {}).get("does_not_create_field") is True, "context_no_field_creation")
    check(context.get("rules", {}).get("does_not_create_goal") is True, "context_no_goal_creation")
    check(context.get("rules", {}).get("role_context_only") is True, "context_role_reference")

    check({"Safety Boundary", "Permission Boundary", "Capability Boundary", "Knowledge Boundary"}.issubset(set(boundary.get("boundary_types", []))), "boundary_types")
    check({"Constitution Boundary Reference", "Authority Context", "Capability Limitation", "Unknown"}.issubset(set(boundary.get("inputs", []))), "boundary_inputs")
    check(boundary.get("rules", {}).get("does_not_modify_constitution") is True, "boundary_no_constitution_write")
    check(boundary.get("rules", {}).get("does_not_grant_permission") is True, "boundary_no_permission_grant")
    check(boundary.get("rules", {}).get("action_boundary_consumes") is True, "boundary_action_consumer")

    check({"Memory", "Self Experience", "Current Task", "Current Context"}.issubset(set(history.get("inputs", []))), "history_inputs")
    check(history.get("output") == "Relevant Self History Reference", "history_output")
    check(history.get("rules", {}).get("relevant_subset_only") is True, "history_relevant_subset")
    check(history.get("rules", {}).get("memory_remains_owner") is True, "history_memory_owner")
    check(history.get("rules", {}).get("current_reality_priority") is True, "history_reality_priority")

    check({"Growth Candidate", "Validation Evidence", "Capability Profile", "Limitation Evidence", "Review Decision"}.issubset(set(update.get("inputs", []))), "update_inputs")
    check(update.get("output") == "Self Model Update Candidate", "update_output")
    check(update.get("rules", {}).get("evidence_required") is True, "update_evidence")
    check(update.get("rules", {}).get("review_required") is True, "update_review")
    check(update.get("rules", {}).get("candidate_before_write") is True, "update_candidate_boundary")
    check(update.get("rules", {}).get("identity_rewrite_forbidden") is True, "update_identity_guard")
    check(update.get("rules", {}).get("value_rewrite_forbidden") is True, "update_value_guard")
    check(update.get("rules", {}).get("goal_creation_forbidden") is True, "update_goal_guard")

    check({"Created", "Composed", "Validated", "Active", "Updated", "Stale", "Superseded", "Archived"}.issubset(set(lifecycle.get("states", []))), "lifecycle_states")
    check({"self_model_id", "state", "snapshot_version", "created_at", "updated_at", "owner", "source_trace"}.issubset(set(lifecycle.get("schema", []))), "lifecycle_schema")
    check(len(lifecycle.get("transitions", [])) >= 6, "lifecycle_transitions")
    check(lifecycle.get("rules", {}).get("stale_not_deleted") is True, "lifecycle_stale_preserved")
    check(lifecycle.get("rules", {}).get("identity_continuity_preserved") is True, "lifecycle_identity_continuity")

    check("Current Task" in memory.get("inputs", []), "memory_interface_task")
    check({"Relevant Self History Reference", "Capability History Reference"}.issubset(set(memory.get("outputs", []))), "memory_interface_outputs")
    check(memory.get("rules", {}).get("memory_owns_records") is True, "memory_interface_owner")
    check(memory.get("rules", {}).get("memory_not_overwritten") is True, "memory_interface_no_overwrite")

    check({"Learning Signal", "Capability Growth Candidate", "Limitation Candidate", "Validation Result"}.issubset(set(learning.get("inputs", []))), "learning_interface_inputs")
    check("Self Model Update Candidate" in learning.get("outputs", []), "learning_interface_output")
    check(learning.get("rules", {}).get("no_automatic_update") is True, "learning_no_auto_update")
    check(learning.get("rules", {}).get("model_training_forbidden") is True, "learning_no_model_training")
    check(learning.get("rules", {}).get("evidence_and_review_required") is True, "learning_review")

    check({"Global Cognitive State", "Self State", "Capability Awareness", "Limitation Awareness", "Resource Awareness", "Boundary Awareness", "Self Context"}.issubset(set(brain.get("inputs", []))), "brain_interface_inputs")
    check({"Self Context Package", "Decision Confidence Context", "Risk Eligibility Context"}.issubset(set(brain.get("outputs", []))), "brain_interface_outputs")
    check(brain.get("rules", {}).get("brain_retains_judgment") is True, "brain_authority")
    check(brain.get("rules", {}).get("context_not_decision") is True, "brain_context_only")
    check(brain.get("rules", {}).get("self_model_does_not_create_goal") is True, "brain_no_goal_creation")

    check({"Action Request Candidate", "Capability Awareness", "Limitation Awareness", "Resource Awareness", "Permission Boundary", "Safety Boundary"}.issubset(set(action.get("inputs", []))), "action_interface_inputs")
    check({"Action Eligibility Context", "Capability Constraint Candidate", "Alternative Required Candidate"}.issubset(set(action.get("outputs", []))), "action_interface_outputs")
    check(action.get("rules", {}).get("action_boundary_owns_execution_gate") is True, "action_boundary_owner")
    check(action.get("rules", {}).get("self_model_does_not_execute") is True, "action_no_execute")
    check(action.get("rules", {}).get("self_model_does_not_authorize") is True, "action_no_authorize")
    check(action.get("rules", {}).get("no_direct_reality_write") is True, "action_no_reality_write")

    forbidden = set(dependency.get("forbidden", []))
    for item in (
        "Self Model → Constitution",
        "Self Model → Value Rewrite",
        "Self Model → Personality",
        "Self Model → Emotion Runtime",
        "Self Model → Social Identity",
        "Self Model → Automatic Goal Creation",
        "Self Model → Identity Rewrite",
        "Self Model → Direct Action",
        "Self Model → Direct Reality Mutation",
        "Self Model → Model Training",
        "Self Model → Runtime Learning",
    ):
        check(item in forbidden, f"dependency_guard:{item}")
    check(len(dependency.get("allowed", [])) >= 6, "dependency_allowed_edges")
    check(dependency.get("rules", {}).get("identity_boundary") is True, "dependency_identity_boundary")
    check(dependency.get("rules", {}).get("emotion_boundary") is True, "dependency_emotion_boundary")
    check(dependency.get("rules", {}).get("candidate_update_boundary") is True, "dependency_candidate_update")
    check(dependency.get("rules", {}).get("brain_authority_preserved") is True, "dependency_brain_authority")
    check(dependency.get("rules", {}).get("action_boundary_preserved") is True, "dependency_action_authority")
    check(dependency.get("rules", {}).get("no_runtime_execution") is True, "dependency_no_runtime")

    verifier_text = Path(__file__).read_text(encoding="utf-8")
    verifier_ast = ast.parse(verifier_text, filename=str(Path(__file__)))
    imports: set[str] = set()
    for node in ast.walk(verifier_ast):
        if isinstance(node, ast.Import):
            imports.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module.split(".")[0])
    check(not imports.intersection({"subprocess", "socket", "requests", "cv2", "torch"}), "planning_no_runtime_import")
    check(not any(name in {"runtime_learning", "online_learning", "model_training", "parameter_update"} for name in imports), "planning_no_learning_import")
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
        print("READINESS: LUNA_COGNITIVE_SELF_MODEL_REMEDIATION_REQUIRED")
        print("NEXT: REMEDIATE_REPORTED_FAILURES_ONLY")
        return 1
    print("FINAL_DECISION: V2_FINAL_VERIFICATION_PASSED")
    print("READINESS: LUNA_COGNITIVE_SELF_MODEL_ARCHITECTURE_READY")
    print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT")
    return 0


if __name__ == "__main__":
    sys.exit(main())
