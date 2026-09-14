#!/usr/bin/env python3
"""V2 static verifier for Cognitive Decision Integration architecture."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent

MD_REQ = {
    "cognitive_decision_integration_model_v1.md": [
        "Decision Integration", "Situation Candidate", "Option Candidate Space", "Option Evaluation Candidates",
        "Decision Context Package", "Decision Candidate", "Brain Review", "Accepted", "Modified", "Rejected",
        "More Information", "Situation", "Options", "Constraints", "Risk", "Unknown", "Capability", "Self State",
        "Confidence", "Evidence Support", "Experience Reference", "not an Action Command", "does not imply execution",
        "Brain retains final judgment authority", "does not change Goal", "does not execute Action", "select a Provider",
        "Reducer remains the sole State mutation authority"
    ],
    "decision_trace_integration_v1.md": [
        "Integrated trace", "Situation Candidate", "Option Candidate Space", "Option Evaluation Candidates",
        "Decision Context Package", "Decision Candidate", "Brain Review Candidate", "Revision", "Acceptance",
        "Rejection", "situation reference", "option list", "constraints", "risk", "unknown", "capability",
        "Self State", "confidence", "Evidence Support", "Experience Reference", "rejected options",
        "private chain-of-thought", "Action plan", "Action Command", "Runtime record", "Outcome claim",
        "Goal mutation", "final cognitive judgment boundary"
    ],
    "decision_unknown_boundary_v1.md": [
        "Unknown", "Decision Context Package", "Brain Review", "lower confidence candidate", "request for more information",
        "safer alternative candidate", "deferred review candidate", "request more information", "accept a candidate",
        "modify candidate", "reject candidate", "Unknown into Fact", "silently remove", "Revision Candidate",
        "execute Action", "modify Goal"
    ],
    "decision_integration_whitebox_v1.md": [
        "Situation", "Options", "Constraints", "Risk", "Unknown", "Capability", "Self State", "Confidence",
        "Decision Context Package", "Decision Candidate", "Brain Review Interface", "Accept", "Modify", "Reject",
        "More Information", "Decision Revision Candidate", "final value judgment", "modify Goal", "modify Reality",
        "execute Action", "Action Command", "Provider", "bypass Brain", "new trace reference", "Reducer remains the sole State mutation authority",
        "No Action Runtime", "No automatic execution", "No Provider Decision", "No Emotion Runtime", "No Role Runtime",
        "No Social Runtime", "No B Runtime", "No Prediction"
    ],
    "decision_integration_go_no_go_v1.md": [
        "Situation", "Options", "Constraints", "Risk", "Unknown", "Capability", "Self State", "Confidence",
        "Decision Context Package", "Action Command", "Execution", "Outcome", "final value approval", "Brain Review Interface",
        "Accept", "Modify", "Reject", "Request More Information", "Goal", "Value", "final Decision authority",
        "Decision Trace", "rejected options", "provenance", "revision references", "Decision Revision Candidate",
        "Unknown cannot be hidden", "convert into Fact", "does not modify Goal", "Reality", "Self Identity", "State",
        "does not execute Action", "Reducer remains the sole State mutation authority", "No Action", "No Action Runtime",
        "No automatic execution", "No Action Command", "No Provider Decision", "No Emotion", "No Role", "No Social Runtime",
        "No B", "No Prediction", "No automatic learning", "No online learning", "No real model", "No OCR", "No SLAM",
        "No Camera", "No Hardware Runtime", "No direct Goal mutation", "No direct Reality mutation", "No direct Decision execution",
        "WAITING_FOR_USER_TERMINAL_VERIFICATION"
    ]
}

JSON_REQ = {
    "decision_context_package_schema_v1.json": [
        "Decision Context Package Schema", "package_id", "situation", "options", "constraints", "risk", "unknown",
        "capability", "self_state", "confidence", "evidence_support", "experience_reference", "provenance",
        "decision_candidate", "review_status", "revision_reference", "package_is_not_action_command",
        "package_is_not_execution", "package_is_not_outcome", "package_does_not_modify_goal",
        "package_does_not_modify_reality", "package_does_not_execute_action", "brain_retains_final_judgment",
        "reducer_is_sole_state_mutation_authority"
    ],
    "decision_brain_interface_v1.json": [
        "Decision Brain Interface", "Brain Review Interface", "decision_context_package", "situation", "options",
        "constraints", "risk", "unknown", "capability", "self_state", "confidence", "provenance", "accept",
        "modify", "reject", "request_more_information", "goal_alignment_review", "value_review", "decision_authority",
        "integration_does_not_command_brain", "integration_does_not_modify_goal", "integration_does_not_modify_value",
        "integration_does_not_create_action", "integration_does_not_execute", "brain_retains_decision_authority",
        "brain_can_request_reobservation"
    ],
    "decision_revision_contract_v1.json": [
        "Decision Revision Contract", "material_new_evidence", "situation_reassessment", "option_constraint_change",
        "capability_state_change", "self_state_change", "brain_review_feedback", "unknown_resolution",
        "unknown_increase", "New Evidence or Brain Feedback", "Situation Reassessment Candidate",
        "Option Regeneration Candidate", "Decision Context Package Revision", "Brain Review", "revision_id",
        "previous_package_reference", "change_reason", "changed_evidence", "changed_options", "changed_constraints",
        "confidence_change", "revision_is_candidate_only", "does_not_execute_action", "does_not_modify_goal",
        "does_not_modify_reality", "does_not_hide_previous_trace", "brain_review_required", "reducer_is_sole_state_mutation_authority"
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
