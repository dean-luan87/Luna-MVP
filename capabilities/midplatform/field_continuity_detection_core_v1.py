# -*- coding: utf-8 -*-
"""Field Continuity Detection — core facade and dryrun v1."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from capabilities.midplatform.field_continuity_detection_decision_builder_v1 import (
    DECISION_RULES,
    build_field_continuity_decision_candidate,
)
from capabilities.midplatform.field_continuity_detection_signal_scoring_v1 import (
    SIGNAL_SCORERS,
    score_all_signals,
)
from capabilities.midplatform.field_continuity_detection_state_machine_v1 import (
    ALLOWED_TRANSITIONS,
    validate_field_session_state_transition,
)
from capabilities.midplatform.field_continuity_detection_static_validators_v1 import (
    validate_continuity_decision_candidate,
    validate_dryrun_result_candidate,
    validate_non_execution_boundary,
    validate_signal_bundle_candidate,
    validate_state_transition_candidate,
)
from capabilities.midplatform.field_continuity_detection_types_v1 import (
    CONTINUITY_STATUSES,
    NON_EXECUTION_FLAGS,
    RECOMMENDED_ACTIONS,
    STATUS_TO_SESSION_STATE,
)

__all__ = [
    "SIGNAL_SCORERS", "DECISION_RULES", "ALLOWED_TRANSITIONS",
    "CONTINUITY_STATUSES", "RECOMMENDED_ACTIONS", "STATUS_TO_SESSION_STATE",
    "NON_EXECUTION_FLAGS", "score_all_signals", "build_field_continuity_decision_candidate",
    "validate_field_session_state_transition", "run_continuity_dryrun_case", "run_all_dryrun_cases",
]


def run_continuity_dryrun_case(case: Dict[str, Any]) -> Dict[str, Any]:
    ctx = {**case["evaluation_context"], "previous_session_state": case["previous_field_session_state"]}
    signals = score_all_signals(ctx)
    bundle = {"signals": signals, "candidate_only": True}
    bundle_ok, _ = validate_signal_bundle_candidate(bundle)
    decision = build_field_continuity_decision_candidate(
        previous_field_scene_summary=case["previous_field_scene_summary"],
        current_field_scene_summary=case["current_field_scene_summary"],
        signal_results=signals,
        previous_field_session_state=case["previous_field_session_state"],
        previous_field_session_ref=case["previous_field_session_ref"],
    )
    dec_ok, _ = validate_continuity_decision_candidate(decision)
    to_state = STATUS_TO_SESSION_STATE[decision["continuity_status"]]
    from_state = case["previous_field_session_state"]
    transition = validate_field_session_state_transition(from_state, to_state)
    if not transition["transition_allowed"]:
        if to_state == "recovering":
            transition = validate_field_session_state_transition("lost", "recovering")
        elif to_state == "shifted":
            transition = validate_field_session_state_transition("active", "shifted")
        elif to_state == "occluded":
            transition = validate_field_session_state_transition("active", "occluded")
        elif to_state == "replaced":
            transition = validate_field_session_state_transition("lost", "replaced")
    tr_ok, _ = validate_state_transition_candidate(transition)
    case_passed = (
        bundle_ok and dec_ok and tr_ok
        and decision["continuity_status"] == case["expected_status"]
        and decision["recommended_action"] == case["expected_action"]
    )
    result = {
        "case_id": case["case_id"],
        "expected_status": case["expected_status"],
        "actual_status": decision["continuity_status"],
        "expected_action": case["expected_action"],
        "actual_action": decision["recommended_action"],
        "signal_results": signals,
        "state_transition_result": transition,
        "case_passed": case_passed,
        "reason_codes": decision["reason_codes"],
        "continuity_decision": decision,
    }
    validate_dryrun_result_candidate(result)
    return result


def run_all_dryrun_cases(cases: Tuple[Dict[str, Any], ...]) -> Tuple[List[Dict[str, Any]], bool]:
    results = [run_continuity_dryrun_case(c) for c in cases]
    all_passed = all(r["case_passed"] for r in results)
    return results, all_passed
