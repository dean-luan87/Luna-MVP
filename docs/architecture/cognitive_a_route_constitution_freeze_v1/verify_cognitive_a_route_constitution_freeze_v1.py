#!/usr/bin/env python3
"""V2 static verifier for A Route Cognitive Constitution freeze."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent

MD_REQ = {
    "a_route_cognitive_constitution_v1.md": [
        "highest architectural constraint", "Reality", "Field", "Attention", "Self", "Situation",
        "Option", "Decision", "Action Boundary", "Outcome", "Experience", "Goal", "Task",
        "Brain owns Intent", "Value", "final Decision", "authorization judgment", "A Route owns",
        "Neural", "second cognitive subject", "Evidence Gateway", "Reducer", "sole State mutation authority",
        "Evidence is not Fact", "Fact is not Situation", "Situation is not Decision", "Unknowns must be preserved",
        "Model → Brain", "Provider → Decision", "Capability → Goal", "Experience → Reality",
        "Field → Goal mutation", "Attention → Decision mutation", "Action → direct Reality mutation",
        "global finite-resource", "Information Value", "Resource Cost", "cannot change Goal",
        "cannot change", "Self = Identity + Capability + State", "Identity is stable", "Identity Drift",
        "Brain-owned Goal", "Field-bound Cognitive Process", "not a global Todo List", "Decision is not Action",
        "Action Intent", "Action Request", "No Action executes", "Outcome Evidence", "Cause Attribution Candidate",
        "Capability is an instrument", "OCR", "Text Evidence", "VLM", "SLAM", "ASR", "Camera", "Hardware",
        "Observation Requirement", "Capability Admission", "Capability Selection", "Provider Execution Boundary",
        "Model Manager", "Provider Replacement", "Evidence Quality Candidate", "Failure", "Unknown is a valid state",
        "Evidence Failure", "Capability Gap", "Execution Gap", "Environment Change", "Random Event",
        "Regression baseline", "No B Route", "No Emotion", "No Role", "No Social Runtime", "No automatic planning",
        "No automatic execution", "real capability runtime"
    ],
    "a_route_constitution_external_capability_boundary_v1.md": [
        "Capability is not Understanding", "Situation", "Decision", "Goal", "Reality", "Brain", "Action",
        "Evidence Gateway", "OCR", "Text Evidence", "VLM", "Scene Evidence Candidate", "SLAM", "Spatial Evidence Candidate",
        "ASR", "Audio/Text Evidence", "Camera", "Hardware", "Provider", "create a Field", "modify Reality",
        "create a Goal", "change Value", "reach Brain directly", "execute Action", "Provider Replacement",
        "Observation Requirement", "Capability Admission", "Capability Selection", "Provider Execution Boundary",
        "Model Manager", "Model Registry", "resource profile", "health state", "Failure contract",
        "Capability State", "Capability Confidence", "No real model calls", "No OCR Runtime", "No VLM Runtime",
        "No SLAM Runtime", "No ASR Runtime", "No Camera", "No Hardware Runtime"
    ],
    "a_route_constitution_failure_unknown_self_continuity_v1.md": [
        "Failure is feedback, not blame", "Prediction/reality difference", "Cause Attribution Candidate",
        "Evidence Failure", "Reality Understanding Failure", "Capability Gap", "Provider Failure", "Execution Gap",
        "Environment Change", "Information Gap", "Understanding Gap", "Random Event", "Decision Factor", "Unknown",
        "Multiple factors may coexist", "One failed Outcome", "Decision Failure", "One successful Outcome",
        "Adaptation Candidate", "Unknown is a first-class state", "Unknown must be preserved", "Identity = stable subject continuity",
        "Capability = what Luna can provide", "State = what Luna is currently like", "Capability degradation",
        "Provider replacement", "Identity Drift", "Reducer remains the sole State mutation authority", "second Brain"
    ],
    "a_route_constitution_regression_baseline_v1.md": [
        "regression baseline", "Level 1", "Level 2", "Level 3", "Level 4", "Level 5", "End-to-End Life Loop",
        "Brain / A Route interaction", "Reality Workspace", "Neural Operating Space", "Context Projection",
        "Cognitive Field", "Continuous Field Flow", "Attention", "Runtime orchestration", "State Machine",
        "Self Capability", "Self State", "Situation", "Option", "Decision Integration", "Action Boundary",
        "Goal / Task / Temporal Continuity", "A Route Life System Integration", "Reality > Experience",
        "Brain final authority", "Reducer sole State mutation authority", "Unknown Preservation",
        "Self Identity Continuity", "Provider Isolation", "Evidence Gateway", "not a Runtime input",
        "new governed phase", "user-terminal verification"
    ],
    "a_route_constitution_whitebox_v1.md": [
        "Reality / Evidence", "Field / Attention / Self", "Situation / Goal / Task", "Option / Decision Candidate",
        "Brain Review / Authorization", "Action Boundary", "External Change", "Outcome", "Cause Attribution",
        "Experience Candidate", "Brain owns Goal", "Reducer is the sole State mutation authority",
        "Capability provides Evidence", "Model Manager governs assets", "Attention allocates finite resources",
        "cannot modify Goal", "cannot modify Decision", "Field and Task provide context", "does not replace Reality",
        "Unknown is preserved", "Self Identity remains continuous", "Action Boundary requests but does not execute",
        "No Runtime", "No Scheduler", "No Model call", "No OCR", "No VLM", "No SLAM", "No ASR", "No Camera",
        "No Hardware", "No Action", "No Emotion", "No Role", "No Social", "No B", "external operation"
    ],
    "a_route_constitution_go_no_go_v1.md": [
        "Brain final authority", "Intent", "Goal", "Value", "Decision", "authorization", "A Route", "Reality",
        "Field", "Attention", "Task", "Action", "Experience", "Capability", "Provider", "Model Manager",
        "Evidence → Reality → Field → Attention → Situation → Option", "Decision → Brain → Action Boundary",
        "Outcome → Experience", "Reducer remains the sole State mutation authority", "Unknown Preservation",
        "Reality > Experience", "Self Identity Continuity", "Provider", "Model", "OCR", "VLM", "SLAM", "ASR",
        "Camera", "Hardware", "Failure", "multi-cause", "Regression baseline", "No Capability Runtime",
        "No Model Manager Runtime", "No real model call", "No Provider execution", "No Action execution",
        "No automatic planning", "No automatic learning", "No Emotion", "No Role", "No Social Runtime", "No B Route",
        "No Simulation", "No direct Reality mutation", "No direct Goal mutation", "No direct Decision mutation",
        "WAITING_FOR_USER_TERMINAL_VERIFICATION"
    ]
}

JSON_REQ = {
    "a_route_constitution_authority_matrix_v1.json": [
        "A Route Constitution Authority Matrix v1", "Brain", "Intent", "Goal", "Value", "final Decision",
        "authorization judgment", "A Route", "Reality interpretation", "Situation", "Option", "Decision Candidate",
        "Outcome interpretation", "Experience Candidate", "Reality Workspace", "Evidence validation", "Reducer",
        "sole State mutation authority", "Cognitive Field", "Attention", "Neural", "Task", "Capability", "Provider",
        "Model Manager", "Action Boundary", "Experience", "forbidden_authority", "Capability to Decision",
        "Model to Goal", "Provider to Brain", "Experience to Reality", "identity_continuity",
        "brain_is_final_cognitive_authority", "no_second_cognitive_subject"
    ],
    "a_route_constitution_information_flow_v1.json": [
        "A Route Constitution Information Flow v1", "External World", "Evidence Gateway", "Reality Workspace",
        "Reality Field", "Cognitive Field", "Attention", "Situation", "Option", "Decision Candidate",
        "Brain Review", "Action Boundary", "External Change", "Outcome Evidence", "Experience Candidate",
        "evidence_is_not_fact", "fact_is_not_situation", "situation_is_not_decision", "experience_does_not_replace_reality",
        "unknowns_are_preserved", "reality_update_requires_evidence_gateway", "reducer_is_sole_state_mutation_authority",
        "Model → Brain", "Provider → Decision", "Capability → Goal", "no_direct_reality_mutation",
        "no_direct_goal_mutation", "no_direct_decision_mutation"
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
