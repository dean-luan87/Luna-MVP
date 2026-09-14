#!/usr/bin/env python3
"""V2 final verifier for Field Role Dynamic Core contracts."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent

MD_REQ = {
    "cognitive_field_role_dynamic_core_v1.md": [
        "dynamic relational cognitive core", "Field", "Role", "Relationship", "Task", "Self", "Attention", "Drive", "Value",
        "Brain", "nested", "associated", "Physical Field", "Social Field", "Virtual Field", "Task Generated Field", "Relationship Field",
        "activated", "backgrounded", "suspended", "closed", "archived", "transferred", "Field sources", "Reality", "Social Relationship",
        "Virtual Interaction", "Memory Reconstruction", "Temporary Field", "Role Instance", "Field + Relationship + Task + Rule + Time",
        "Role Stack", "Organizer", "Participant", "Safety Observer", "Employee", "Priority Candidate", "Responsibility", "Constraint",
        "Attention Requirement", "Role Conflict Candidate", "Relationship Layer Stack", "Colleague", "Friend", "Historical Conflict",
        "Source Field", "Time", "Evidence", "Confidence", "History", "Boundary", "Task flow", "Goal → Task → Field Creation → Role Assignment → Capability Requirement",
        "Field State", "Drive", "Risk", "Attention Allocation", "Memory stores Field State", "Field Conflict Candidate", "Brain review",
        "Current Field State", "Simulation Field Candidate", "No Emotion Runtime", "automatic personality switching", "Social Decision",
        "Relationship Judgment", "B Runtime", "Prediction", "Action Runtime", "multi-agent", "hive behavior"
    ],
    "field_role_dynamic_whitebox_v1.md": [
        "Field Network", "Field State", "Role Stack", "Relationship Layer", "Task", "Self", "Drive", "Value", "Attention Allocation Candidate",
        "Who creates a Field", "Reality", "Social Relationship", "Virtual Interaction", "Memory Reconstruction", "Who activates or closes a Field",
        "Field Governance", "Who projects Role", "Field + Relationship + Task + Rule + Time", "Who composes Roles", "Role Conflict Candidate",
        "Who supplies Relationship", "Contextual history", "Who owns Goal and final Decision", "Brain", "Who owns Reality mutation", "Reality Reducer",
        "Field Network → Role Assignment Candidate", "Role Stack → Attention Candidate", "Relationship Layer → Memory Candidate", "Task → Field Creation Candidate",
        "Field/Role → Identity Mutation", "Relationship → Emotion Judgment", "Field → Decision", "Field → Action", "Simulation Field → Reality Write",
        "B Route", "placeholder only", "Emotion", "Planning Only", "automatic resolution"
    ],
    "field_role_dynamic_go_no_go_v1.md": [
        "Field Network", "Physical", "Social", "Virtual", "Task Generated", "Relationship Fields", "nested", "associated", "activated",
        "closed", "archived", "transferred", "Field Generation", "Reality", "Social Relationship", "Task", "Goal", "Virtual Interaction",
        "Memory Reconstruction", "Role Instance", "Field + Relationship + Task + Rule + Time", "Role Stack", "Priority", "Responsibility",
        "Constraint", "Attention Requirement", "Role Conflict Candidate", "auto-resolved", "Source Field", "Time", "Evidence", "Confidence",
        "History", "Boundary", "Unknown", "Attention", "Drive", "Value", "Task can create a Field", "Memory stores integrated",
        "Simulation Field Candidate", "No Emotion Runtime", "No automatic personality switching", "No Social Decision", "No Relationship Judgment",
        "No B Runtime", "No Prediction", "No Action Runtime", "No autonomous Multi-Agent", "No Hive", "directly modify Identity", "Reality",
        "Goal", "Decision", "Action", "WAITING_FOR_USER_TERMINAL_VERIFICATION"
    ]
}

JSON_REQ = {
    "field_network_schema_v1.json": [
        "Field Network Schema v1", "network_id", "nodes", "edges", "Physical Field", "Social Field", "Virtual Field", "Task Generated Field",
        "Relationship Field", "nested_fields", "associated_fields", "active_fields", "background_fields", "suspended_fields", "closed_fields",
        "archived_fields", "transferred_fields", "field_network_does_not_make_decision", "unknowns_are_preserved"
    ],
    "field_generation_contract_v1.json": [
        "Field Generation Contract v1", "field_source", "Reality", "Social Relationship", "Task", "Goal", "Virtual Interaction",
        "Memory Reconstruction", "source_reference", "field_type", "Physical", "Social", "Virtual", "Task Generated", "Relationship",
        "field_candidate", "temporary_field", "creation_evidence", "confidence", "unknowns", "field_close_candidate",
        "generation_does_not_modify_reality", "generation_does_not_make_decision", "unknowns_are_preserved"
    ],
    "field_transition_contract_v1.json": [
        "Field Transition Contract v1", "Created", "Active", "Background", "Suspended", "Closed", "Archived", "field_reference", "from_state",
        "to_state", "transition_reason", "source_field", "target_field", "continuity_context", "evidence", "confidence", "nested_or_associated",
        "transfer_candidate", "transition_does_not_modify_identity", "transition_does_not_make_decision", "unknowns_are_preserved"
    ],
    "role_projection_model_v1.json": [
        "Role Projection Model v1", "role_instance_id", "field_reference", "relationship_reference", "task_reference", "rule_reference",
        "time_reference", "role_candidate", "Organizer Candidate", "priority_candidate", "responsibility", "constraint", "attention_requirement",
        "role_instance_formula", "Field + Relationship + Task + Rule + Time", "role_does_not_modify_identity", "unknowns_are_preserved"
    ],
    "multi_role_composition_schema_v1.json": [
        "Multi Role Composition Schema v1", "role_stack_id", "field_reference", "active_roles", "Organizer", "Participant", "Safety Observer",
        "Employee", "background_roles", "suspended_roles", "role_priorities", "responsibilities", "constraints", "attention_requirements",
        "role_conflict_candidates", "composition_is_not_resolution", "identity_continuity_required", "unknowns_are_preserved"
    ],
    "relationship_layer_stack_v1.json": [
        "Relationship Layer Stack v1", "stack_id", "participant_a", "participant_b", "relationships", "Colleague", "Friend", "Historical Conflict",
        "source_field", "time", "evidence", "confidence", "history", "boundary", "unknowns", "relationship_is_contextual",
        "relationship_is_not_single_global_label", "unknowns_are_preserved"
    ],
    "field_conflict_candidate_schema_v1.json": [
        "Field Conflict Candidate Schema v1", "conflict_id", "fields", "Work Field", "Historical Relationship Field", "role_stack",
        "relationship_layer", "drive_reference", "value_reference", "risk", "evidence", "confidence", "unknowns", "brain_review_required",
        "automatic_resolution", "conflict_does_not_make_decision", "unknowns_are_preserved"
    ],
    "field_attention_interface_v1.json": [
        "Field Attention Interface v1", "field_state", "role_stack", "drive_reference", "value_reference", "risk", "attention_allocation_candidate",
        "role_attention_requirements", "field_does_not_allocate_attention_directly", "field_does_not_modify_goal", "field_does_not_modify_decision",
        "unknowns_are_preserved"
    ],
    "field_task_interface_v1.json": [
        "Field Task Interface v1", "goal_reference", "task_reference", "field_creation_candidate", "field_reference", "role_assignment_candidate",
        "capability_requirement", "task_can_create_temporary_field", "task_does_not_make_decision", "task_does_not_execute_action",
        "unknowns_are_preserved"
    ],
    "field_memory_interface_v1.json": [
        "Field Memory Interface v1", "field_state_reference", "role_stack_reference", "relationship_layer_reference", "task_reference",
        "outcome_reference", "experience_reference", "field_memory_candidate", "memory_stores_integrated_state", "memory_does_not_override_reality",
        "memory_does_not_make_decision", "unknowns_are_preserved"
    ],
    "field_brain_interface_v1.json": [
        "Field Brain Interface v1", "field_state", "role_stack", "relationship_layer", "field_conflict_candidate", "goal_reference",
        "decision_candidate_reference", "brain_review_required", "brain_retains_goal_authority", "brain_retains_final_decision_authority",
        "field_does_not_make_decision", "unknowns_are_preserved"
    ],
    "field_b_route_placeholder_v1.json": [
        "Field B Route Placeholder v1", "current_field_state", "simulation_field_candidate", "Role", "Rule", "Relationship", "Goal",
        "simulation_mode", "Placeholder", "reality_is_read_only", "b_runtime", "prediction", "simulation_does_not_modify_reality",
        "simulation_does_not_make_decision", "unknowns_are_preserved"
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
