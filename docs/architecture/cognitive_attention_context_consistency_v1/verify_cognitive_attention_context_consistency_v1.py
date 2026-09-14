#!/usr/bin/env python3
"""V2 static verifier for Attention Context Consistency."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent

MD_REQ = {
    "cognitive_attention_context_consistency_model_v1.md": [
        "Attention Pattern", "Field Context", "Condition", "Valid Scope", "Pattern Isolation",
        "Attention Transfer", "Attention Conflict Candidate", "Self Identity", "Role Runtime",
        "Emotion Runtime", "Social Field", "B Runtime", "automatic learning", "automatic personality modification",
        "Action", "Decision", "Goal"
    ],
    "attention_pattern_isolation_model_v1.md": [
        "Attention Pattern", "Field Context", "Condition", "Self Capability", "Goal Context",
        "Reality scope", "Work Field Pattern", "Family Field Pattern", "Pattern Pollution Candidate",
        "Transfer Candidate", "Self Continuity", "different identities", "different personalities"
    ],
    "attention_transfer_boundary_v1.md": [
        "Attention Transfer", "source", "target", "Field relation", "compatible Condition",
        "Information Value", "Self Capability", "current Reality", "Driving safety", "family relationship",
        "Context Similarity Candidate", "Transfer Candidate", "Validation", "Target Attention Prior Candidate",
        "cannot directly change", "Self Identity", "Decision", "Action"
    ],
    "attention_self_continuity_boundary_v1.md": [
        "Attention Adaptation", "Self Capability Candidate", "Self Review", "Adaptive", "Transient",
        "Identity", "Survival Constitution", "Self Continuity", "context-bound", "not separate selves",
        "cannot modify Identity", "cannot modify Self Model", "Conflict Candidate", "personality"
    ],
    "attention_context_consistency_whitebox_v1.md": [
        "Attention Pattern", "Field Context", "Condition", "Valid Scope", "Pattern Isolation",
        "Transfer Boundary", "Attention Conflict Candidate", "Brain Evaluation", "Context Similarity Candidate",
        "Transfer Candidate", "Target Attention Prior Candidate", "Self Capability Candidate", "Self Review",
        "does not directly control Attention", "overwrites another Field", "modifies Identity", "Personality",
        "Role", "Emotion", "Social", "B Runtime"
    ],
    "attention_context_consistency_go_no_go_v1.md": [
        "Attention Pattern", "Field Context", "Condition", "Valid Scope", "Pattern Isolation",
        "Attention Transfer", "Self Capability", "provenance", "current Reality", "Work", "family",
        "friend", "network", "navigation", "maintenance", "Attention Conflict Candidate", "automatic override",
        "Self Review", "Identity", "Self Continuity", "No Role Runtime", "No Emotion Runtime", "No Social Field",
        "No B Runtime", "no automatic learning", "no automatic personality modification", "No Action", "No Decision",
        "No Runtime", "automatic conflict resolution", "direct cross-context transfer", "WAITING_FOR_USER_TERMINAL_VERIFICATION"
    ],
}

JSON_REQ = {
    "attention_context_binding_contract_v1.json": [
        "Attention Context Binding Contract", "pattern_reference", "field_context", "condition",
        "self_capability", "goal_context", "reality_reference", "valid_scope", "expiry_or_review",
        "pattern_is_context_bound", "cross_context_default_transfer", "direct_attention_control", "identity_mutation"
    ],
    "attention_conflict_candidate_schema_v1.json": [
        "Attention Conflict Candidate Schema", "field_context", "active_patterns", "pattern_scopes",
        "conflict_type", "conflict_reason", "resource_constraint", "unknowns", "provenance",
        "Brain Evaluation", "automatic_resolution", "automatic_override", "decision_authority", "action_authority"
    ],
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
