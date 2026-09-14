#!/usr/bin/env python3
"""V2 static verifier for A Route life-system integration validation.

The User Terminal owns execution of this final phase verifier. The Agent only
performs equivalent V0 parsing and compilation checks.
"""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent

MD_REQ = {
    "cognitive_a_route_life_system_integration_model_v1.md": [
        "External Change", "Reality Update", "Field Adjustment", "Attention Reallocation",
        "Situation Formation", "Goal Alignment", "Task Update", "Option Generation",
        "Decision Integration", "Brain Review", "Action Request Boundary", "Outcome Evidence",
        "Cause Attribution", "Experience Candidate", "Future Attention", "Reality Workspace",
        "Model", "Capability", "Field", "Task", "Action", "Reducer", "Attention is a global",
        "cannot modify Goal", "cannot modify Decision", "Field-bound Cognitive Process",
        "Self Identity remains continuous", "Brain owns Goal", "authorization", "Action Boundary",
        "Experience is a candidate", "24-hour", "7-day", "30-day", "wrong Evidence",
        "Capability degradation", "Task interruption", "Goal conflict", "incorrect Experience",
        "No real Runtime", "No Scheduler implementation", "No Model call", "No OCR", "No SLAM",
        "No Hardware", "No Action execution", "No Emotion", "No Role", "No Social Runtime", "No B Route"
    ],
    "a_route_attention_integration_validation_v1.md": [
        "global cognitive resource scheduling layer", "Reality acquisition", "Capability requests",
        "Task resource allocation", "Brain awareness", "Information Value", "Uncertainty", "Risk",
        "Goal relevance", "Field relevance", "Resource Cost", "survival", "Attention Interrupt",
        "Navigation", "Conversation", "conflict candidate", "Capability degradation", "alternative observation",
        "release", "recovery", "does not modify Goal", "does not modify Decision", "does not execute Action",
        "Brain retains final judgment"
    ],
    "a_route_field_task_integration_validation_v1.md": [
        "Field-bound Cognitive Process", "global task list", "simple queue", "task_id",
        "Goal reference", "constraints", "pending information", "unknowns", "Background", "Suspended",
        "Office Field", "Work Task", "Home Field", "high-risk event", "resume conditions",
        "current Reality", "Field", "Self State", "Attention allocation", "completion evidence",
        "Field does not modify Goal", "Task does not modify Reality", "Reducer", "24-hour", "7-day", "30-day",
        "No automatic planning", "No execution"
    ],
    "a_route_self_continuity_validation_v1.md": [
        "Self", "Identity", "Capability", "State", "Identity Drift", "Office", "Home", "Transit",
        "Capability degradation", "Low battery", "Provider replacement", "Evidence Quality Candidate",
        "Cause Attribution", "Adaptation candidates", "automatic Self rewrite", "Attention", "Situation",
        "Option", "sole State mutation authority"
    ],
    "a_route_brain_authority_validation_v1.md": [
        "Authority matrix", "Reality", "Facts", "Evidence", "Field", "context", "Attention",
        "resource", "Situation", "Task", "A Route / Option", "Brain", "Intent", "Goal", "Value",
        "final Decision", "authorization", "Action Boundary", "Experience", "Brain Review",
        "Goal Conflict", "high-risk Action", "unresolved Unknown", "Capability limits", "Capability → Decision",
        "Model → Goal", "Task → Action", "Experience → Reality", "final Goal", "final Value"
    ],
    "a_route_long_term_stability_validation_v1.md": [
        "24-hour", "7-day", "30-day", "Home", "Transit", "Office", "Field transitions", "Task interruption",
        "Experience candidates", "Identity remains stable", "Attention does not drift", "Reality remains Evidence-first",
        "Unknown remains explicit", "Experience does not replace", "Decision", "Action boundaries",
        "Capability changes", "state pollution", "permission drift", "Task leakage", "Goal drift",
        "resource exhaustion", "fixture-based architecture review", "not a 24-hour Runtime", "not a Scheduler",
        "not a Model call", "not a Hardware test", "online learning"
    ],
    "a_route_life_system_whitebox_v1.md": [
        "Reality / Evidence", "Reality Workspace / Reducer", "Field + Self", "Attention Allocation",
        "Situation Understanding", "Goal Alignment", "Field-bound Task Process", "Option Space",
        "Decision Integration", "Brain Review", "Authorization", "Action Request Boundary", "Outcome Evidence",
        "Cause Attribution", "Experience Candidate", "evidence provenance", "Self Identity/Capability/State",
        "Task lifecycle", "Option tradeoffs", "Decision reference", "Action permission", "Unknowns",
        "Reality → Field → Self → Attention → Situation → Goal → Task → Decision → Action → Outcome → Experience",
        "No real Runtime", "No Scheduler implementation", "No Model call", "No OCR", "No SLAM", "No Hardware",
        "No Action execution", "No Emotion", "No Role", "No Social", "No B", "No Simulation",
        "sole State mutation authority", "No direct Reality mutation", "No direct Goal mutation", "No direct Decision mutation"
    ],
    "a_route_life_system_go_no_go_v1.md": [
        "Complete lifecycle trace", "Reality", "Field", "Self", "Attention", "Situation", "Goal", "Task",
        "Option", "Decision", "Action Boundary", "Outcome", "Experience", "Reality Update", "Field Adjustment",
        "Situation Formation", "Capability requests", "Task priority", "Brain input", "Field-bound Process",
        "Task identity", "context", "Self Identity", "Capability", "State", "Brain retains Goal", "Value",
        "final Decision", "authorization", "Action remains a request boundary", "current Reality",
        "24-hour", "7-day", "30-day", "wrong Evidence", "Capability degradation", "Task interruption",
        "Goal conflict", "incorrect Experience", "Model → Goal", "Capability → Decision", "Action → direct Reality",
        "No real Runtime", "No Scheduler implementation", "No Model call", "No OCR", "No SLAM", "No Hardware",
        "No Action execution", "No Emotion", "No Role", "No Social", "No B", "No Simulation",
        "No online learning", "No automatic planning", "No automatic execution", "No direct Reality mutation",
        "No direct Goal mutation", "No direct Decision mutation", "WAITING_FOR_USER_TERMINAL_VERIFICATION"
    ]
}

JSON_REQ = {
    "a_route_full_lifecycle_trace_schema_v1.json": [
        "A Route Full Lifecycle Trace Schema v1", "trace_id", "external_change", "reality_update",
        "field_adjustment", "self_state", "attention_reallocation", "situation_candidate", "goal_alignment_candidate",
        "task_update_candidate", "option_candidates", "decision_integration_candidate", "brain_review_required",
        "action_request_candidate", "authorization_required", "outcome_evidence", "cause_attribution_candidate",
        "experience_candidate", "future_attention_candidate", "future_capability_adaptation_candidate",
        "reality_over_experience", "identity_continuity", "attention_does_not_modify_goal",
        "attention_does_not_modify_decision", "brain_retains_goal_and_decision_authority", "action_does_not_execute",
        "reducer_is_sole_state_mutation_authority", "no_runtime_execution", "unknowns_are_preserved"
    ],
    "a_route_module_interaction_contract_v1.json": [
        "A Route Module Interaction Contract v1", "Reality", "Field", "Self", "Attention", "Situation",
        "Goal", "Task", "Option", "Decision", "Action", "Outcome", "Experience", "ordered_flow",
        "fact representation", "context organization", "Identity continuity", "resource allocation candidate",
        "situated interpretation candidate", "Brain", "final Decision", "authorization", "request boundary only",
        "validated reference candidate", "Capability to Decision", "Model to Goal", "Experience to Reality",
        "Field to Goal mutation", "Attention to Decision mutation", "Action to direct Reality mutation",
        "Task to automatic execution", "reality_update_requires_evidence_gateway", "reducer_is_sole_state_mutation_authority",
        "brain_is_final_goal_and_decision_authority", "provider_is_not_decision_authority", "runtime_execution_is_out_of_scope",
        "multi_a_is_out_of_scope", "unknowns_are_preserved"
    ],
    "a_route_failure_injection_scenario_v1.json": [
        "A Route Failure Injection Scenario Registry v1", "wrong_evidence", "capability_degradation",
        "task_interruption", "goal_conflict", "incorrect_experience", "fixture_id", "injected_condition",
        "expected_boundary", "candidate_response", "reality_must_not_be_directly_mutated", "goal_must_not_be_directly_mutated",
        "decision_must_not_be_directly_mutated", "self_identity_must_not_be_directly_mutated", "diagnostic_candidate",
        "evidence_gateway", "reducer", "unknowns_preserved", "no_runtime_execution", "no_action_execution"
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
