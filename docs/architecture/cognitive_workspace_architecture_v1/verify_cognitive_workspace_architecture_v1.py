#!/usr/bin/env python3
"""V2 final verifier for Cognitive Workspace architecture contracts."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent

MD_REQ = {
    "cognitive_workspace_architecture_v1.md": [
        "Cognitive Workspace", "current cognitive operating window", "Field", "Role", "Relationship", "Task", "Self",
        "Attention", "Drive", "Value", "Memory", "Brain", "Reality", "world facts", "historical experience",
        "current cognitive focus", "Active Field Context", "Active Role Context", "Active Relationship Context",
        "Active Task Context", "Active Goal Context", "Attention State", "Current Unknown", "Current Risk",
        "Relevant Memory", "Drive Influence", "Value Constraint", "Known State", "Unknown State", "Conflict State",
        "Workspace references an existing Field", "does not create or mutate a Field", "Attention selects what enters",
        "Memory contributes retrieval candidates", "Brain retains reasoning", "Goal authority", "final Decision authority",
        "Created → Active → Updated → Background → Closed", "Primary Workspace", "Background Workspace", "not multiple consciousnesses",
        "Unknown is first-class", "Known State, Unknown State, and Conflict State", "Workspace Package", "Workspace Snapshot",
        "No Decision", "No Reasoning", "No Planning", "No Emotion Runtime", "No B Route Runtime", "No automatic learning",
        "No Memory modification", "No Action Runtime", "No model training", "No hardware calls", "cannot modify Reality",
        "cannot modify Goal", "cannot modify Identity", "cannot modify Decision"
    ],
    "workspace_whitebox_v1.md": [
        "Reality / Field / Role / Relationship / Task / Self / Memory", "Attention Arbitration", "Cognitive Workspace State",
        "Brain Input Package", "Who creates a Workspace", "Workspace Governance", "Who activates a Workspace",
        "Activation Contract", "Who updates a Workspace", "Update Contract", "Who selects content", "Who supplies historical context",
        "Memory Retrieval Candidate", "Who owns Goal and final Decision", "Brain", "Reality Reducer", "Field, Role, Relationship, and Task definitions",
        "Primary and Background Workspaces", "Attention → Workspace admission", "Memory → Workspace retrieval", "Field → Workspace context projection",
        "Workspace → Decision", "Workspace → Reality Write", "Workspace → Goal Mutation", "Workspace → Identity Mutation", "Workspace → Action",
        "Workspace → Model/Hardware Invocation", "Unknown", "Risk", "Conflict", "Provenance", "B Route is a placeholder only",
        "no Simulation Runtime"
    ],
    "workspace_go_no_go_v1.md": [
        "Workspace schema", "Active Field", "Role", "Relationship", "Task", "Goal", "Attention", "Unknown", "Risk", "Memory", "Drive", "Value",
        "references Field", "does not create or mutate Field", "Attention controls admission", "Memory enters through a retrieval candidate",
        "cannot override Reality", "Brain receives", "Cognitive Workspace Package", "Decision authority", "Known, Unknown, and Conflict states",
        "Created", "Active", "Updated", "Background", "Closed", "Multiple Workspaces", "Primary", "Background contexts", "Snapshot placeholder",
        "No Decision", "No Reasoning", "No Planning", "No Emotion Runtime", "No B Route Runtime", "No automatic learning", "No Memory modification",
        "No Action Runtime", "No model training", "No hardware calls", "cannot modify Reality", "Goal", "Identity", "Decision", "WAITING_FOR_USER_TERMINAL_VERIFICATION"
    ]
}

JSON_REQ = {
    "cognitive_workspace_schema_v1.json": [
        "Cognitive Workspace Schema v1", "workspace_id", "workspace_kind", "Primary Workspace", "status", "Active", "active_field_context",
        "active_role_context", "active_relationship_context", "active_task_context", "active_goal_context", "attention_state",
        "current_unknown", "current_risk", "relevant_memory", "drive_influence", "value_constraint", "known_state", "unknown_state",
        "conflict_state", "provenance", "workspace_does_not_make_decision", "workspace_does_not_modify_reality", "workspace_does_not_modify_identity",
        "multiple_workspaces_are_isolated"
    ],
    "workspace_state_model_v1.json": [
        "Workspace State Model v1", "Created", "Active", "Updated", "Background", "Closed", "Primary Workspace", "Background Workspace",
        "state_owner", "state_transition_is_candidate_based", "closed_workspace_releases_focus_only", "closed_workspace_does_not_delete_memory",
        "unknowns_are_preserved"
    ],
    "workspace_activation_contract_v1.json": [
        "Workspace Activation Contract v1", "activation_request", "source_field", "source_role", "source_relationship", "source_task",
        "source_goal", "attention_admission_candidate", "resource_constraints", "unknowns", "provenance", "activation_does_not_create_field",
        "activation_does_not_make_decision", "activation_does_not_modify_reality", "unknowns_are_preserved"
    ],
    "workspace_update_contract_v1.json": [
        "Workspace Update Contract v1", "update_candidate", "active_field_context_delta", "active_role_context_delta", "active_relationship_context_delta",
        "active_task_context_delta", "attention_state_delta", "known_state_delta", "unknown_state_delta", "conflict_state_delta", "provenance",
        "update_is_not_decision", "update_does_not_modify_reality", "update_does_not_modify_memory", "unknowns_are_preserved"
    ],
    "workspace_field_interface_v1.json": [
        "Workspace Field Interface v1", "field_reference", "active_field_context", "field_state", "field_provenance", "field_unknowns",
        "workspace_references_field_only", "workspace_does_not_create_field", "workspace_does_not_close_field", "field_does_not_make_decision",
        "unknowns_are_preserved"
    ],
    "workspace_role_interface_v1.json": [
        "Workspace Role Interface v1", "role_reference", "active_role_context", "supporting_role_context", "role_stack_reference",
        "role_provenance", "workspace_stores_role_reference_only", "workspace_does_not_define_role", "workspace_does_not_modify_identity",
        "role_conflicts_are_preserved", "unknowns_are_preserved"
    ],
    "workspace_task_interface_v1.json": [
        "Workspace Task Interface v1", "task_reference", "active_task_context", "goal_reference", "progress_reference",
        "completion_condition_reference", "pending_information", "next_requirement", "workspace_does_not_create_task", "task_does_not_make_decision",
        "task_context_is_current_focus_only", "unknowns_are_preserved"
    ],
    "workspace_attention_interface_v1.json": [
        "Workspace Attention Interface v1", "attention_admission", "field_state", "role_context", "task_context", "drive_influence",
        "value_constraint", "risk", "attention_selection_candidate", "attention_decides_workspace_content", "workspace_does_not_allocate_attention",
        "workspace_does_not_change_goal", "unknowns_are_preserved"
    ],
    "workspace_memory_interface_v1.json": [
        "Workspace Memory Interface v1", "current_context", "memory_retrieval_request", "relevant_memory_candidate", "Working Memory",
        "Episodic Memory", "Field Memory", "Semantic Memory", "Self Memory", "memory_provenance", "memory_enters_workspace_as_candidate",
        "memory_does_not_override_reality", "workspace_does_not_modify_memory", "unknowns_are_preserved"
    ],
    "workspace_brain_interface_v1.json": [
        "Workspace Brain Interface v1", "cognitive_workspace_package", "field_context", "role_context", "relationship_context", "task_context",
        "goal_context", "attention_state", "unknowns", "risks", "memory_candidates", "drive_state", "value_constraints",
        "brain_receives_workspace_package", "brain_retains_reasoning_authority", "brain_retains_goal_authority", "brain_retains_final_decision_authority",
        "workspace_does_not_make_decision", "unknowns_are_preserved"
    ],
    "workspace_unknown_contract_v1.json": [
        "Workspace Unknown Contract v1", "known_state", "unknown_state", "conflict_state", "unknown_id", "source_reference", "confidence",
        "provenance", "unknown_is_first_class", "unknown_is_not_silently_completed", "unknown_affects_attention", "unknowns_are_preserved"
    ],
    "workspace_lifecycle_contract_v1.json": [
        "Workspace Lifecycle Contract v1", "Created", "Active", "Updated", "Background", "Closed", "Created → Active", "Active → Updated",
        "Updated → Background", "Background → Active", "Active → Closed", "Background → Closed", "Primary Workspace", "Background Workspace",
        "workspace_isolation", "closed_workspace_does_not_delete_memory", "lifecycle_does_not_make_decision", "unknowns_are_preserved"
    ]
}


def main():
    failures = []
    checks = 0
    for name, terms in MD_REQ.items():
        checks += 1
        path = BASE / name
        if not path.is_file():
            failures.append(f"missing required file: {name}")
            continue
        text = path.read_text()
        for term in terms:
            checks += 1
            if term not in text:
                failures.append(f"missing required contract term: {term} in {name}")
    for name, terms in JSON_REQ.items():
        checks += 1
        path = BASE / name
        try:
            text = path.read_text()
            json.loads(text)
        except Exception as exc:
            failures.append(f"JSON parse failure: {name}: {type(exc).__name__}")
            text = ""
        for term in terms:
            checks += 1
            if term not in text:
                failures.append(f"missing required JSON contract term: {term} in {name}")
    print(f"CHECKS: {checks}")
    print(f"FAILED_CHECKS: {failures}")
    print(f"PASSED_CHECK_COUNT: {checks - len(failures)}")
    print(f"FAILED_CHECK_COUNT: {len(failures)}")
    print(f"BLOCKER_COUNT: {len(failures)}")
    if failures:
        print("FINAL_DECISION: BLOCKED_BY_VERIFIER_FAILURE")
        print("NEXT: REMEDIATE_REPORTED_FAILURES_ONLY")
        return 1
    print("FINAL_DECISION: V2_FINAL_VERIFICATION_PASSED")
    print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
