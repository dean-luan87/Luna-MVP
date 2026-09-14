#!/usr/bin/env python3
"""V2 final verifier for Self Capability Profile architecture contracts."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent

MD_REQ = {
    "self_capability_profile_model_v1.md": [
        "Self Capability Profile", "long-term", "context-bound", "Capability State", "Hardware Capability", "Memory",
        "Performance Evidence", "not a score", "not a personality", "not a Goal", "not a Decision", "not a Model self-evaluation",
        "Experience", "Memory", "Capability Assessment", "Future Attention / Decision Support", "Current Reality",
        "Identity remains continuous", "multi-dimensional capability space", "Perception", "Field Understanding", "Task Execution",
        "Adaptation", "Information Seeking", "Reliability", "Capability × Field × Condition", "Indoor", "Outdoor", "Low Light",
        "Dynamic Crowd", "Outcome Evidence", "Experience Pattern", "Failure Attribution", "Confidence Calibration",
        "Model self-report", "Known Strength", "Known Limitation", "Unknown", "Capability Confidence Increase Candidate",
        "Capability Growth Candidate", "Human Calibration Interface", "Attention Adjustment Candidate", "Model Selection Candidate",
        "Model Manager supplies implementation options", "does not define Luna's Capability Profile", "No automatic learning",
        "automatic capability upgrade", "Model Training", "model parameter modification", "Emotion Runtime", "Role System",
        "Social Runtime", "B Route", "Action Runtime"
    ],
    "capability_confidence_model_v1.md": [
        "Capability confidence is contextual", "not a single score", "Performance Evidence", "Outcome Evidence", "Experience Pattern",
        "Failure Attribution", "Confidence Calibration", "Confidence Candidate", "Capability", "Field", "Condition", "time",
        "source", "provenance", "Unknown", "Knowing that I do not know", "Human Review", "candidate", "Reality", "Goal",
        "Decision", "Identity", "Model parameters", "Action", "Model self-confidence"
    ],
    "capability_growth_model_v1.md": [
        "Growth is a validated historical pattern", "not automatic upgrade", "Performance Evidence", "Capability Growth Candidate",
        "OCR Capability Confidence Increase Candidate", "Context", "Failure Attribution", "Confidence Calibration", "provenance",
        "human calibration availability", "Performance Pattern", "Growth Candidate", "Assessment Review", "Capability Adjustment Candidate",
        "single success", "Provider/model replacement", "Hardware State", "Resource State", "Field Condition",
        "No automatic capability upgrade", "Model Training", "model parameter modification", "automatic learning"
    ],
    "capability_limitation_model_v1.md": [
        "Capability Limitation", "Known Strength", "Known Limitation", "Unknown", "Capability × Field × Condition", "Indoor Navigation",
        "Night Vision", "Crowded Outdoor", "Performance Evidence", "Outcome Evidence", "Failure Attribution", "Hardware/Resource evidence",
        "temporary State degradation", "Model availability", "network failure", "goal mismatch", "Attention Adjustment Candidate",
        "alternative Capability Candidate", "Model Selection Candidate", "does not create a Goal", "make a Decision", "modify Identity",
        "directly control Action", "permanently define a Luna"
    ],
    "capability_whitebox_v1.md": [
        "Experience", "Memory", "Performance Evidence", "Capability Assessment", "Self Capability Profile",
        "Future Attention / Decision Support", "Outcome Evidence", "Experience Pattern", "Failure Attribution", "Confidence Calibration",
        "Model self-evaluation", "Capability × Field × Condition", "Unknown", "Human Calibration Interface", "Goal and final Decision",
        "Model Manager", "Hardware Capability", "Attention Adjustment Candidate", "Model Selection Candidate", "Self Capability Profile → Attention Adjustment Candidate",
        "Self Capability Profile → Model Selection Candidate", "Profile → Reality", "Profile → Goal", "Profile → Decision", "Profile → Identity Mutation",
        "Profile → Model Parameter Mutation", "Profile → Action", "No automatic learning", "automatic capability upgrade", "Model Training",
        "Emotion Runtime", "Role System", "Social Runtime", "B Route", "Action Runtime"
    ],
    "capability_go_no_go_v1.md": [
        "Self Capability Awareness layer", "not a score system", "Experience", "Memory", "Performance Evidence", "Capability Assessment",
        "Self Capability Profile", "Future Attention / Decision Support", "Perception", "Field Understanding", "Task Execution", "Adaptation",
        "Information Seeking", "Reliability", "Capability × Field × Condition", "Outcome Evidence", "Experience Pattern", "Failure Attribution",
        "Confidence Calibration", "Model self-evaluation", "Known Strength", "Known Limitation", "Unknown", "Human Calibration",
        "Attention", "Model Manager", "Identity", "Goal", "Decision", "Reality", "Action", "No automatic learning",
        "No automatic capability upgrade", "No Model Training", "No model parameter modification", "No Emotion Runtime", "No Role System",
        "No Social Runtime", "No B Route", "No Action Runtime", "directly modify Reality", "directly modify Goal", "directly modify Decision",
        "directly modify Identity", "WAITING_FOR_USER_TERMINAL_VERIFICATION"
    ]
}

JSON_REQ = {
    "capability_dimension_schema_v1.json": [
        "Capability Dimension Schema v1", "capability_id", "dimension", "Perception", "Field Understanding", "Task Execution",
        "Adaptation", "Information Seeking", "Reliability", "field_reference", "condition", "known_strength", "known_limitation",
        "unknown", "current_state_reference", "hardware_reference", "memory_reference", "confidence_candidate", "provenance",
        "assessment_candidate", "identity_is_unchanged", "unknowns_are_preserved"
    ],
    "capability_assessment_contract_v1.json": [
        "Capability Assessment Contract v1", "capability_reference", "field_reference", "condition", "outcome_evidence",
        "experience_pattern", "failure_attribution", "confidence_calibration", "performance_window", "assessment_candidate",
        "model_self_evaluation_accepted", "current_reality_precedence", "human_calibration_interface", "assessment_does_not_modify_identity",
        "assessment_does_not_modify_goal", "assessment_does_not_modify_decision", "unknowns_are_preserved"
    ],
    "capability_performance_evidence_schema_v1.json": [
        "Capability Performance Evidence Schema v1", "evidence_id", "capability_reference", "field_reference", "condition",
        "task_reference", "outcome_reference", "success_signal", "failure_signal", "failure_attribution", "confidence", "uncertainty",
        "timestamp", "provenance", "unknowns", "is_model_self_report", "evidence_is_not_capability", "evidence_requires_assessment",
        "unknowns_are_preserved"
    ],
    "capability_confidence_model_v1.json": [
        "Capability Confidence Model v1", "capability_reference", "field_reference", "condition", "performance_evidence",
        "outcome_evidence", "experience_pattern", "failure_attribution", "confidence_calibration", "recency", "uncertainty",
        "confidence_candidate", "unknown", "model_self_confidence_not_accepted", "human_calibration_interface",
        "confidence_does_not_modify_goal", "confidence_does_not_modify_decision", "unknowns_are_preserved"
    ],
    "luna_skill_profile_schema_v1.json": [
        "Luna Skill Profile Schema v1", "profile_id", "specialization", "strong_fields", "weak_fields", "unknown_fields",
        "experience_count", "confidence_summary", "Perception", "Field Understanding", "Task Execution", "Adaptation",
        "Information Seeking", "Reliability", "context_binding_required", "identity_reference", "profile_is_not_personality",
        "profile_is_not_goal", "profile_is_not_decision", "human_calibration_interface", "unknowns_are_preserved"
    ],
    "capability_memory_interface_v1.json": [
        "Capability Memory Interface v1", "memory_reference", "experience_reference", "performance_evidence_reference",
        "capability_assessment_candidate", "field_reference", "condition", "memory_is_supporting_evidence",
        "experience_is_not_capability_automatically", "assessment_required", "current_reality_precedence", "unknowns_are_preserved"
    ],
    "capability_attention_interface_v1.json": [
        "Capability Attention Interface v1", "capability_profile_reference", "field_reference", "condition",
        "attention_adjustment_candidate", "observation_adjustment_candidate", "review_or_recheck_candidate", "known_limitation", "unknown",
        "attention_adjustment_is_candidate_only", "profile_does_not_directly_allocate_attention", "profile_does_not_modify_goal",
        "profile_does_not_modify_decision", "unknowns_are_preserved"
    ],
    "capability_model_manager_interface_v1.json": [
        "Capability Model Manager Interface v1", "capability_need", "self_capability_state", "hardware_state", "model_selection_candidate",
        "implementation_options", "resource_constraints", "context", "model_manager_provides_options", "model_manager_does_not_define_capability",
        "model_manager_does_not_modify_identity", "model_manager_does_not_modify_goal", "model_manager_does_not_modify_decision",
        "automatic_model_switching", "unknowns_are_preserved"
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
