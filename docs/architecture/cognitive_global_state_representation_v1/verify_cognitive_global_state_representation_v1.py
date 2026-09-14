#!/usr/bin/env python3
"""V2 final verifier for Global Cognitive State representation contracts."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent

MD_REQ = {
    "cognitive_global_state_architecture_v1.md": [
        "Cognitive Global State Representation Architecture v1", "Global Cognitive State", "Module State", "Brain Context",
        "not a database", "not Memory", "not Decision", "not Reality", "Reality State", "Field State", "Self State",
        "Role State", "Relationship State", "Situation State", "Intent State", "Goal State", "Task State", "Workspace State",
        "Attention State", "Drive State", "Value State", "Hypothesis State", "Belief State", "Expectation State",
        "Memory Context", "Learning Context", "Capability State", "Unknown State", "source versions", "Conflicts", "Provenance",
        "Unknown or Stale Candidate", "read-only Global Cognitive State Package", "does not infer a new Reality",
        "does not resolve a Hypothesis", "does not update a Belief", "does not change an Expectation",
        "does not allocate Attention", "does not create a Decision", "Brain receives a Global Cognitive State Package",
        "Brain retains", "final Decision authority", "current Reality", "State Transition Candidate", "Snapshots are immutable",
        "Memory may retain important State Transition records", "Simulation State placeholder", "B Runtime",
        "Decision", "Prediction", "World Model", "automatic learning", "Action", "Runtime execution", "model invocation",
        "hardware invocation", "Emotion Runtime", "state mutation"
    ],
    "state_whitebox_v1.md": [
        "Who owns each component", "Who composes Global Cognitive State", "Who validates freshness", "Who owns Unknown State",
        "Who consumes the package", "Who owns final Decision", "Who updates modules", "Who stores history",
        "Field / Self / Workspace / Attention / Hypothesis / Expectation / Memory /", "Global Cognitive State Snapshot",
        "Global Cognitive State Package", "Brain", "Global State → Reality write", "Global State → Field mutation",
        "Global State → Self Identity mutation", "Global State → Goal or Task mutation", "Global State → Attention allocation",
        "Global State → Hypothesis or Belief resolution", "Global State → Expectation update", "Global State → Decision",
        "Global State → Action", "Global State → Prediction Runtime", "Global State → World Model", "Global State → B Runtime",
        "Global State → automatic learning", "Identity reference", "Confidence", "Unknown State", "Conflict State", "Risk",
        "Constraints", "Provenance", "fabricates a complete state"
    ],
    "state_go_no_go_v1.md": [
        "Global Cognitive State", "representation layer", "Reality", "Field", "Self", "Role", "Relationship", "Situation",
        "Intent", "Goal", "Task", "Workspace", "Attention", "Drive", "Value", "Hypothesis", "Belief", "Expectation",
        "Memory", "Learning", "Capability", "Unknown State", "Global Cognitive State Snapshot", "Global Cognitive State Package",
        "Brain", "final Decision authority", "State Transition", "Memory", "B Route", "snapshot-copy placeholder",
        "No Decision", "No Prediction", "No World Model", "No B Runtime", "No automatic learning", "No Action",
        "No Runtime execution", "No model invocation", "No hardware invocation", "No Reality mutation", "No Goal/Task mutation",
        "No Identity mutation", "No fabricated Unknown completion", "V0 static checks", "V1", "V2 Final Phase Verification",
        "User Terminal Only", "V3", "WAITING_FOR_USER_TERMINAL_VERIFICATION"
    ]
}

JSON_REQ = {
    "global_state_schema_v1.json": [
        "Global Cognitive State Schema v1", "Global Cognitive State Snapshot", "snapshot_id", "snapshot_time", "source_versions",
        "reality_state", "field_state", "self_state", "role_state", "relationship_state", "situation_state", "intent_state",
        "goal_state", "task_state", "workspace_state", "attention_state", "drive_state", "value_state", "hypothesis_state",
        "belief_state", "expectation_state", "memory_context", "learning_context", "capability_state", "unknown_state",
        "risk", "conflicts", "confidence", "provenance", "state_is_not_reality", "state_is_not_decision",
        "state_does_not_mutate_sources", "unknowns_are_preserved"
    ],
    "state_composition_contract_v1.json": [
        "Global State Composition Contract v1", "Read-only State Composition", "Reality State", "Field State", "Self State",
        "Role State", "Relationship State", "Situation State", "Intent State", "Goal State", "Task State", "Workspace State",
        "Attention State", "Drive State", "Value State", "Hypothesis State", "Belief State", "Expectation State", "Memory Context",
        "Learning Context", "Capability State", "Unknown State", "read owner state", "validate source version", "preserve conflicts and Unknown State",
        "compose Global Cognitive State Snapshot", "publish Global Cognitive State Package", "composer_is_read_only",
        "composer_does_not_create_reality", "composer_does_not_resolve_hypothesis", "composer_does_not_update_belief",
        "composer_does_not_update_expectation", "composer_does_not_allocate_attention", "composer_does_not_make_decision",
        "unknowns_are_preserved"
    ],
    "field_state_interface_v1.json": [
        "Global State Field State Interface v1", "Field State Projection", "field_reference", "field_state", "field_version",
        "field_context", "unknowns", "provenance", "field_state_reference", "active_field_context", "field_dynamics", "field_unknowns",
        "global_state_references_field_only", "global_state_does_not_create_field", "global_state_does_not_mutate_field",
        "field_owner_retains_authority", "unknowns_are_preserved"
    ],
    "self_state_interface_v1.json": [
        "Global State Self State Interface v1", "Self State Projection", "identity_reference", "capability_state", "dynamic_self_state",
        "self_version", "unknowns", "provenance", "self_state_reference", "capability_reference", "state_reference",
        "global_state_does_not_modify_identity", "global_state_does_not_modify_capability", "global_state_does_not_modify_self_state",
        "self_owner_retains_authority", "unknowns_are_preserved"
    ],
    "workspace_state_interface_v1.json": [
        "Global State Workspace State Interface v1", "Workspace State Projection", "workspace_reference", "workspace_state",
        "active_field", "active_task", "workspace_version", "unknowns", "provenance", "workspace_state_reference", "current_focus",
        "known_state", "unknown_state", "conflict_state", "global_state_references_workspace_only", "global_state_does_not_create_workspace",
        "global_state_does_not_mutate_workspace", "workspace_owner_retains_authority", "unknowns_are_preserved"
    ],
    "attention_state_interface_v1.json": [
        "Global State Attention State Interface v1", "Attention State Projection", "attention_state", "allocation_reference", "resource_state",
        "attention_version", "risk", "unknowns", "provenance", "attention_state_reference", "current_allocations", "competition_state",
        "preemption_state", "resource_summary", "global_state_does_not_allocate_attention", "global_state_does_not_preempt_attention",
        "attention_owner_retains_authority", "attention_state_is_reference_only", "unknowns_are_preserved"
    ],
    "belief_expectation_state_interface_v1.json": [
        "Global State Belief Expectation Interface v1", "Belief and Expectation State Projection", "hypothesis_state", "belief_state",
        "expectation_state", "feedback_state", "field_context", "confidence", "unknowns", "provenance", "hypothesis_state_reference",
        "belief_state_reference", "expectation_state_reference", "feedback_status", "conflict_state", "global_state_does_not_resolve_hypothesis",
        "global_state_does_not_modify_belief", "global_state_does_not_modify_expectation", "reality_and_feedback_remain_authoritative",
        "unknowns_are_preserved"
    ],
    "memory_context_interface_v1.json": [
        "Global State Memory Context Interface v1", "Relevant Memory Context Projection", "memory_query_reference", "current_field",
        "current_situation", "current_task", "attention_context", "provenance", "unknowns", "memory_context", "relevant_memory_candidates",
        "state_transition_records", "memory_conflicts", "global_state_does_not_store_all_memory", "memory_context_is_retrieval_candidate",
        "memory_does_not_override_reality", "global_state_does_not_modify_memory", "unknowns_are_preserved"
    ],
    "learning_context_interface_v1.json": [
        "Global State Learning Context Interface v1", "Learning Context Projection", "experience_candidates", "feedback_candidates",
        "state_transition_records", "pattern_candidates", "learning_version", "provenance", "unknowns", "learning_context",
        "future_adjustment_candidates", "learning_signals", "global_state_does_not_execute_learning", "learning_context_is_candidate_only",
        "learning_does_not_mutate_global_state", "learning_does_not_modify_reality", "unknowns_are_preserved"
    ],
    "capability_state_interface_v1.json": [
        "Global State Capability State Interface v1", "Capability State Projection", "capability_references", "capability_states",
        "confidence", "hardware_state_reference", "capability_version", "provenance", "unknowns", "capability_state", "availability",
        "degradation", "confidence_summary", "global_state_does_not_invoke_capability", "global_state_does_not_select_provider",
        "capability_owner_retains_authority", "capability_state_is_reference_only", "unknowns_are_preserved"
    ],
    "unknown_state_contract_v1.json": [
        "Global Unknown State Contract v1", "Unknown and Conflict State Preservation", "unknown_state", "unknown_id", "source_reference",
        "reason", "confidence", "provenance", "time_context", "conflict_state", "conflict_id", "source_references", "candidate_values",
        "unknown_is_first_class", "unknown_is_not_silently_completed", "unknown_affects_brain_context", "unknown_affects_attention_candidate",
        "conflict_is_preserved", "composer_does_not_resolve_unknown", "unknowns_are_preserved"
    ],
    "brain_state_package_contract_v1.json": [
        "Brain Global State Package Contract v1", "Global Cognitive State Package for Brain", "global_cognitive_state_snapshot",
        "reality_state", "field_state", "self_state", "role_state", "relationship_state", "situation_state", "intent_state", "goal_state",
        "task_state", "workspace_state", "attention_state", "drive_state", "value_state", "hypothesis_state", "belief_state",
        "expectation_state", "memory_context", "learning_context", "capability_state", "unknown_state", "risk", "conflicts", "confidence",
        "provenance", "brain_receives_global_cognitive_state_package", "brain_retains_reasoning_authority", "brain_retains_goal_authority",
        "brain_retains_final_decision_authority", "global_state_is_not_decision", "global_state_does_not_execute_action",
        "unknowns_are_preserved"
    ],
    "state_snapshot_lifecycle_v1.json": [
        "Global State Snapshot Lifecycle v1", "Immutable State Snapshot and Transition", "Created", "Composed", "Published", "Superseded",
        "Archived", "Created → Composed", "Composed → Published", "Published → Superseded", "Superseded → Archived",
        "snapshot_is_immutable", "new_composition_creates_new_snapshot", "source_versions_are_preserved", "state_transition_candidate_is_separate",
        "memory_stores_selected_state_transitions_only", "snapshot_does_not_make_decision", "snapshot_does_not_modify_reality",
        "unknowns_are_preserved"
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
