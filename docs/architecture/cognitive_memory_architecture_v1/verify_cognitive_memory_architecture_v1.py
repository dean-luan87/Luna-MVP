#!/usr/bin/env python3
"""V2 final verifier for Memory Architecture contracts."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent

MD_REQ = {
    "cognitive_memory_architecture_model_v1.md": [
        "Memory is not a database", "does not store all history", "Experience", "Field", "Time", "Self", "Goal", "Task",
        "Context", "Reality", "Decision", "Action", "Reality > Memory", "Current Reality always overrides Memory",
        "provenance", "Unknown", "conflict", "decay", "Experience Candidate", "Memory Admission", "Memory Storage",
        "Memory Retrieval", "Current Field Context", "Attention / Situation Support", "value", "stability", "reusability",
        "risk", "Working Memory", "Episodic Memory", "Field Memory", "Semantic Memory", "Self Memory",
        "Relationship Memory", "Relationship Memory is a placeholder", "Memory Query", "Relevant Memory", "Memory does not",
        "Current Reality > Recent Valid Memory > Old Memory", "Decay", "Time", "Confidence", "Importance", "Reuse",
        "Contradiction", "Conflict is preserved", "Experience enters through Memory Admission", "Pattern", "Adaptation",
        "No automatic learning", "Model Training", "model-weight modification", "Emotion Runtime", "Role System", "Social Runtime",
        "B Route", "Prediction", "Action Runtime", "No database implementation", "No Memory Runtime"
    ],
    "episodic_memory_model_v1.md": [
        "Episodic Memory", "bounded event reference", "event", "Field", "Self context", "Goal/Task context", "Outcome",
        "time", "evidence", "confidence", "provenance", "Unknown", "conflict", "Memory Admission", "single unconfirmed event",
        "durable pattern", "Current Reality > Memory", "Reality Update Candidate", "Field Pattern Candidate", "Behavior Pattern Candidate",
        "Action", "Goal", "Decision", "Identity", "Model Training"
    ],
    "memory_decay_model_v1.md": [
        "Memory decay", "Time", "Confidence", "Importance", "Reuse", "Contradiction", "Decay Candidate", "Retrieval Priority",
        "Archive Candidate", "not simple deletion", "high-importance historical event", "Archived", "Candidate", "Working", "Retained",
        "Decaying", "Released Candidate", "provenance", "scope", "current-Reality reconciliation", "No automatic purge",
        "No automatic learning", "No Memory Runtime"
    ],
    "memory_whitebox_v1.md": [
        "Experience Candidate", "Memory Admission", "Memory Storage", "Memory Retrieval", "Current Field Context",
        "Attention / Situation Support", "Who admits Memory", "Experience Evaluation", "not a Model", "Who queries Memory",
        "Current Field", "Goal", "Task", "Attention", "Memory Query", "Who resolves Reality conflict", "Current Reality",
        "Reality Reducer", "Who owns final Goal and Decision", "Who controls retention and decay", "Who may revoke or archive",
        "Memory → Attention Support", "Memory → Situation Support", "Memory → Pattern Candidate", "Memory → Reality",
        "Memory → Goal", "Memory → Decision", "Memory → Action", "Memory → Identity Mutation", "Memory → Model Weight Mutation",
        "Reality > Memory", "Working Memory", "Relationship Memory", "No database", "No Memory Runtime", "automatic learning",
        "Model Training", "Emotion Runtime", "Role System", "Social Runtime", "B Route", "Prediction", "Action Runtime"
    ],
    "memory_go_no_go_v1.md": [
        "organized Experience reference", "not a database", "Experience Candidate", "Memory Admission", "Memory Storage",
        "Memory Retrieval", "Current Field Context", "Attention / Situation Support", "Working Memory", "Episodic Memory",
        "Field Memory", "Semantic Memory", "Self Memory", "Relationship Memory Placeholder", "Field", "Time", "Self", "Goal",
        "Task", "Context", "Current Field + Goal + Task + Attention", "Reality > Memory", "Current Reality > Recent Valid Memory > Old Memory",
        "provenance", "confidence", "Unknown", "conflict", "decay", "compression", "archive", "release", "Experience",
        "Adaptation", "No automatic learning", "No Model Training", "model-weight modification", "No Emotion Runtime", "No Role System",
        "No Social Runtime", "No B Route", "No Prediction", "No Action Runtime", "No database implementation", "No Memory Runtime",
        "directly modify Reality", "directly modify Goal", "directly modify Decision", "directly modify Identity", "WAITING_FOR_USER_TERMINAL_VERIFICATION"
    ]
}

JSON_REQ = {
    "memory_layer_schema_v1.json": [
        "Memory Layer Schema v1", "memory_id", "memory_class", "Working", "Episodic", "Field", "Semantic", "Self",
        "Relationship Placeholder", "field_reference", "time_reference", "self_reference", "goal_reference", "task_reference",
        "context_reference", "experience_reference", "content_candidate", "confidence", "importance", "recency", "provenance",
        "unknowns", "conflicts", "decay_state", "Stable", "Decaying", "Archived", "Released Candidate", "memory_is_not_reality",
        "current_reality_precedence", "unknowns_are_preserved"
    ],
    "working_memory_contract_v1.json": [
        "Working Memory Contract v1", "memory_class", "current_field_reference", "current_goal_reference", "current_task_reference",
        "attention_reference", "active_context", "pending_information", "unknowns", "short_lifecycle", "field_scoped", "task_scoped",
        "does_not_become_reality", "does_not_make_decision", "does_not_execute_action", "release_candidate_required",
        "unknowns_are_preserved"
    ],
    "field_memory_contract_v1.json": [
        "Field Memory Contract v1", "memory_class", "field_reference", "field_context", "observed_patterns", "entrances",
        "flow_patterns", "recurring_constraints", "supporting_experiences", "field_pattern_candidate", "memory_is_not_field_rule",
        "memory_is_not_reality", "current_reality_precedence", "provenance_required", "decay_required", "unknowns_are_preserved"
    ],
    "semantic_memory_contract_v1.json": [
        "Semantic Memory Contract v1", "memory_class", "knowledge_candidate", "source_experiences", "validation_state", "Candidate",
        "Validated Candidate", "Conflicted", "Archived", "scope", "confidence", "provenance", "unknowns",
        "semantic_memory_is_not_current_reality", "semantic_memory_is_not_rule_authority", "current_reality_precedence",
        "memory_does_not_make_decision", "unknowns_are_preserved"
    ],
    "self_memory_contract_v1.json": [
        "Self Memory Contract v1", "memory_class", "identity_reference", "capability_history", "state_history", "self_context",
        "evidence_reference", "identity_continuity_required", "memory_does_not_modify_identity",
        "memory_does_not_claim_capability_without_evidence", "current_reality_precedence", "unknowns_are_preserved"
    ],
    "memory_admission_contract_v1.json": [
        "Memory Admission Contract v1", "experience_candidate_reference", "evaluation_reference", "value_check", "stability_check",
        "reusability_check", "risk_check", "provenance_check", "unknown_check", "admission_state", "Candidate", "Review",
        "Admitted Candidate", "Rejected", "Deferred", "Archived", "one_off_noise_not_admitted", "unconfirmed_information_not_admitted",
        "model_guess_not_admitted", "admission_does_not_modify_reality", "admission_does_not_modify_goal",
        "admission_does_not_modify_decision", "automatic_learning_disabled", "unknowns_are_preserved"
    ],
    "memory_retrieval_contract_v1.json": [
        "Memory Retrieval Contract v1", "current_field_reference", "goal_reference", "task_reference", "attention_reference",
        "context_reference", "memory_query", "relevant_memory", "retrieval_scope", "Field", "Time", "Self", "Goal", "Task",
        "Context", "Attention", "reality_reconciliation_required", "current_reality_precedence", "retrieval_does_not_search_all_history",
        "retrieval_does_not_create_goal", "retrieval_does_not_make_decision", "retrieval_does_not_execute_action",
        "unknowns_are_preserved"
    ],
    "memory_conflict_resolution_v1.json": [
        "Memory Conflict Resolution v1", "Current Reality > Recent Valid Memory > Old Memory", "current_reality", "recent_valid_memory",
        "old_memory", "conflict_candidate", "supporting_evidence", "recency", "confidence", "importance",
        "conflict_is_not_silently_erased", "reality_reducer_review_required", "memory_does_not_overwrite_reality",
        "memory_does_not_make_decision", "unknowns_are_preserved"
    ],
    "memory_experience_interface_v1.json": [
        "Memory Experience Interface v1", "experience_candidate_reference", "cause_attribution_reference", "memory_admission_reference",
        "memory_class_candidate", "storage_candidate", "provenance", "unknowns", "experience_is_not_memory_automatically",
        "admission_required", "current_reality_precedence", "unknowns_are_preserved"
    ],
    "memory_adaptation_interface_v1.json": [
        "Memory Adaptation Interface v1", "memory_reference", "pattern_candidate", "attention_adjustment_candidate",
        "behavior_adjustment_candidate", "self_capability_adjustment_candidate", "field_context_reference", "validation_required",
        "adaptation_is_candidate_only", "memory_does_not_directly_modify_action", "memory_does_not_modify_goal",
        "memory_does_not_modify_decision", "memory_does_not_modify_identity", "unknowns_are_preserved"
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
