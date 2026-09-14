#!/usr/bin/env python3
"""V2 static verifier for Cognitive Field architecture."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
MD_REQ = {
    "cognitive_field_constitution_v1.md": ["Cognitive Field", "Reality Field", "bounded", "Decision", "Reasoning", "Planning", "Prediction", "Outcome Evaluation", "Action", "not a data cache", "not a Context Window", "not a Decision Engine"],
    "cognitive_reality_field_model_v1.md": ["Reality Field", "space", "Entity", "Event", "Relation", "State", "does not explain meaning", "not a Decision Engine", "Field State Candidate"],
    "cognitive_situated_field_model_v1.md": ["Situated Cognitive Field", "Reality State", "Self State", "Goal Context", "Rule Reference", "Social Context", "Emotion Influence Candidate", "Attention Bias Candidate", "Priority Influence Candidate", "Relationship Weight Candidate", "no Recommendation", "no Decision"],
    "cognitive_field_layer_boundary_v1.md": ["Reality Field", "Self Field", "Goal Field", "Rule Field", "Social Field", "Emotion Field", "Cognitive Field", "A Route", "Brain", "does not modify Reality State"],
    "cognitive_field_lifecycle_model_v1.md": ["Created", "Activated", "Updated", "Suspended", "Resumed", "Merged", "Closed", "independent Goal", "not a Scheduler Runtime"],
    "cognitive_field_multi_instance_placeholder_v1.md": ["Navigation Field", "Companion Field", "Self Maintenance Field", "multiple Cognitive Field", "placeholder", "multi-field Decision coordination", "multi-role weight competition"],
    "cognitive_field_whitebox_v1.md": ["Reality Neural Operating Space", "Situated Cognitive Field", "Field State", "Unknown", "Provenance", "A Route Input Environment", "Situation Understanding", "Emotional Judgment", "Personality Formation"],
    "cognitive_field_go_no_go_v1.md": ["not a Situation Engine", "Attention Bias", "Priority Influence", "Relationship Weight Candidate", "Created", "Activated", "Updated", "Suspended", "Merged", "Closed", "Relevant Reality", "Rule Reference", "Field does not output Decision", "Multi Field is a placeholder", "No Decision", "No Reasoning", "No Planning", "No Prediction", "No Situation Engine Runtime", "No real model", "No OCR", "No SLAM", "WAITING_FOR_USER_TERMINAL_VERIFICATION"],
}
JSON_REQ = {
    "cognitive_field_schema_v1.json": ["cognitive_field", "reality_layer", "self_layer", "goal_layer", "rule_layer", "social_layer", "emotion_layer", "unknowns", "provenance", "forbidden_outputs", "decision", "prediction"],
    "cognitive_field_activation_contract_v1.json": ["Created", "Activated", "Updated", "Suspended", "Resumed", "Merged", "Closed", "create_goal", "make_decision", "execute_action", "merge_is_structural_only"],
    "cognitive_field_a_route_interface_v1.json": ["Cognitive Field Package", "relevant_reality", "self_state", "goal_context", "rule_reference", "unknown", "provenance", "decision", "recommendation", "action"],
    "cognitive_field_brain_interface_v1.json": ["field_state", "a_route_feedback", "resource_constraint", "conflict_candidate", "raw_reality_database", "raw_model_output", "final_judgment", "field_is_read_organized_environment"],
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
