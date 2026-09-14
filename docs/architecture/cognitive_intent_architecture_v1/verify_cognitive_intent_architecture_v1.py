#!/usr/bin/env python3
"""V2 final verifier for Cognitive Intent architecture contracts.

Planning Only permits this file to be authored and statically checked by the
Agent. Final phase execution remains User Terminal only.
"""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent

MD_REQ = {
    "cognitive_intent_architecture_v1.md": [
        "Cognitive Intent Architecture v1", "Intent Layer", "Drive / Value", "Intent",
        "Goal", "Task", "Action Boundary", "Situation", "Intent Candidate", "Intent Expression",
        "Intent Context", "User Intent", "Self Intent", "Survival Intent", "Task Intent",
        "Field Requirement", "autonomous will", "automatic goal generation", "personality-driven intent",
        "Emotion Decision", "Action", "Intent is always context-bound", "Field reference",
        "Role and Relationship context", "Self state", "Situation reference", "Drive influence",
        "Value constraints", "Unknown is preserved", "Intent influences Attention", "Option",
        "Decision Candidate", "does not allocate Attention", "does not make a Decision",
        "Brain retains final Decision authority", "Intent Conflict Candidate", "Brain review",
        "Created → Qualified → ContextBound → Presented → Reviewed →", "Accepted", "Modified",
        "Rejected", "Deferred", "Expired", "Archived", "B Route", "Simulation Runtime",
        "Reality remains authoritative", "Provenance", "no Action Runtime", "no model invocation",
        "no hardware invocation"
    ],
    "intent_whitebox_v1.md": [
        "Who creates an Intent Candidate", "Who qualifies it", "Who binds it to a Field",
        "Who owns Goal and Task continuity", "Who allocates Attention", "Who evaluates options",
        "Who owns final Decision", "Who can request clarification", "Who can revoke an Intent",
        "Drive / Value + Source Evidence", "Intent Candidate", "Field / Role / Relationship / Self / Situation Binding",
        "Attention Influence + Option Relevance + Goal Alignment Candidate", "Brain Intent Review",
        "Provider → Intent", "Model → Intent", "Capability → Goal", "Intent → Goal mutation",
        "Intent → Decision", "Intent → Action", "Intent → Reality write", "Personality → automatic intent",
        "Emotion → Decision", "B Route Snapshot → live Intent mutation", "Intent Conflict Candidate",
        "Unknown", "Risk", "Constraint", "Confidence", "Provenance", "Field binding"
    ],
    "intent_go_no_go_v1.md": [
        "Intent Layer", "User Intent", "Self Intent", "Survival Intent", "Task Intent",
        "Field Requirement", "Intent Candidate", "Context", "Confidence", "Unknown", "Provenance",
        "Attention", "Option", "Decision Candidate", "Intent Conflict Candidate", "Brain review",
        "Existing Goal/Task contracts", "B Route", "Simulation Runtime", "No automatic goal generation",
        "no autonomous will", "no personality-driven intent", "no Emotion Decision", "no Action",
        "no Action Runtime", "no model or hardware invocation", "no Reality mutation",
        "no Provider-created Intent", "no silent Unknown completion", "no automatic conflict resolution",
        "V0 static checks", "V1", "V2 Final Phase Verification", "User Terminal Only", "V3",
        "WAITING_FOR_USER_TERMINAL_VERIFICATION"
    ]
}

JSON_REQ = {
    "intent_schema_v1.json": [
        "Intent Schema v1", "Intent Candidate", "intent_id", "intent_kind", "intent_expression",
        "intent_context", "situation_reference", "field_reference", "role_reference",
        "relationship_references", "self_reference", "goal_reference", "task_reference",
        "source_reference", "drive_influence", "value_constraints", "attention_influence_candidate",
        "option_relevance_candidate", "confidence", "unknowns", "risks", "constraints", "provenance",
        "intent_is_not_command", "intent_is_not_goal", "intent_is_not_task", "intent_is_not_decision",
        "intent_does_not_generate_goal_automatically", "intent_does_not_execute_action",
        "intent_does_not_modify_reality", "unknowns_are_preserved", "brain_retains_final_decision_authority"
    ],
    "intent_source_contract_v1.json": [
        "Intent Source Contract v1", "User Intent", "Self Intent", "Survival Intent", "Task Intent",
        "Field Requirement", "source_id", "source_type", "evidence", "provenance", "field_reference",
        "confidence", "unknowns", "provider_cannot_create_intent", "model_cannot_create_intent",
        "source_does_not_create_goal", "source_does_not_create_task", "source_does_not_make_decision",
        "conflicting_sources_create_intent_conflict_candidate", "unknowns_are_preserved"
    ],
    "intent_field_binding_v1.json": [
        "Intent Field Binding v1", "Intent Context Binding", "binding_request", "intent_candidate",
        "field_reference", "field_state_reference", "role_reference", "relationship_references",
        "self_state_reference", "situation_reference", "time_window", "provenance",
        "intent_is_field_bound", "intent_references_existing_field", "binding_does_not_create_field",
        "binding_does_not_mutate_field", "binding_does_not_mutate_role", "binding_does_not_mutate_relationship",
        "binding_does_not_mutate_self_identity", "reality_remains_authoritative", "unknowns_are_preserved",
        "same goal may produce different intent"
    ],
    "intent_goal_interface_v1.json": [
        "Intent Goal Interface v1", "Intent to Goal Alignment Candidate", "intent_candidate",
        "goal_reference", "goal_alignment_candidate", "drive_influence", "value_constraints",
        "field_reference", "provenance", "unknowns", "alignment_status", "goal_admission_request",
        "intent_does_not_generate_goal_automatically", "intent_does_not_modify_goal",
        "goal_owner_retains_authority", "brain_retains_goal_authority", "intent_is_not_goal",
        "unknowns_are_preserved"
    ],
    "intent_task_interface_v1.json": [
        "Intent Task Interface v1", "Intent to Task Reference", "intent_candidate", "task_reference",
        "goal_reference", "task_context", "field_reference", "provenance", "unknowns",
        "task_alignment_candidate", "task_intent_reference", "pending_information",
        "intent_references_existing_task", "intent_does_not_create_task", "intent_does_not_modify_task",
        "task_owner_retains_continuity", "intent_is_not_task", "unknowns_are_preserved"
    ],
    "intent_attention_interface_v1.json": [
        "Intent Attention Interface v1", "Intent Attention Influence Candidate", "intent_candidate",
        "field_context", "role_context", "task_context", "risk", "unknowns", "provenance",
        "attention_influence_candidate", "information_targets", "intent_influences_attention",
        "intent_does_not_allocate_attention", "attention_governance_retains_allocation",
        "intent_does_not_change_goal", "unknowns_are_preserved"
    ],
    "intent_conflict_schema_v1.json": [
        "Intent Conflict Candidate Schema v1", "Intent Conflict Candidate", "conflict_id",
        "intent_candidates", "source_conflict", "field_contexts", "role_contexts",
        "relationship_contexts", "goal_references", "task_references", "drive_influences",
        "value_constraints", "risk", "unknowns", "tradeoffs", "provenance", "resolution_status",
        "conflict_is_preserved", "conflict_requires_brain_review", "conflict_is_not_automatically_resolved",
        "conflict_does_not_make_decision", "unknowns_are_preserved"
    ],
    "intent_brain_interface_v1.json": [
        "Intent Brain Interface v1", "Brain Intent Review Package", "intent_candidate", "intent_expression",
        "intent_source", "field_context", "role_context", "relationship_context", "self_context",
        "situation", "goal_context", "task_context", "drive_state", "value_constraints",
        "attention_influence_candidate", "conflicts", "unknowns", "risks", "confidence", "provenance",
        "request_clarification", "request_more_information", "brain_retains_goal_authority",
        "brain_retains_final_decision_authority", "intent_does_not_make_decision", "intent_does_not_create_action",
        "intent_does_not_execute", "unknowns_are_preserved"
    ],
    "intent_lifecycle_contract_v1.json": [
        "Intent Lifecycle Contract v1", "Intent Candidate Lifecycle", "Created", "Qualified",
        "ContextBound", "Presented", "Reviewed", "Accepted", "Modified", "Rejected", "Deferred",
        "Expired", "Archived", "Created → Qualified", "Qualified → ContextBound", "ContextBound → Presented",
        "Presented → Reviewed", "candidate_based", "provenance_preserved", "expiry_is_contextual",
        "accepted_intent_does_not_generate_goal_automatically", "lifecycle_does_not_make_decision",
        "lifecycle_does_not_execute_action", "unknowns_are_preserved"
    ],
    "intent_governance_contract_v1.json": [
        "Intent Governance Contract v1", "Intent Admission and Authority Governance", "source permission",
        "field binding", "role and relationship context", "self capability and state", "situation compatibility",
        "goal/task compatibility", "drive/value constraints", "risk", "unknown", "provenance", "expiry",
        "intent_layer", "attention", "goal_owner", "task_owner", "brain", "provider", "model",
        "no_automatic_goal_generation", "no_autonomous_will", "no_personality_driven_intent",
        "no_emotion_decision", "no_action", "no_action_runtime", "no_model_invocation", "no_hardware_invocation",
        "no_reality_mutation", "no_provider_created_intent", "no_silent_unknown_completion",
        "no_automatic_conflict_resolution", "b_route_is_placeholder_only", "unknowns_are_preserved",
        "constitution_review_required", "protocol_version_required", "brain_boundary_review_required"
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
