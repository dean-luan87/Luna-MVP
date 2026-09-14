from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.speech_manager.module.speech_manager_module_types_v1 import (
    INTERRUPTION_INTENT_TYPES,
    not_fact,
)


def build_speech_manager_interruption_plan_v1(
    input_candidate: Mapping[str, Any],
    priority_candidate: Mapping[str, Any],
) -> Dict[str, Any]:
    intent = str(
        input_candidate.get("interruption_intent_type") or "UNKNOWN_OR_AMBIGUOUS"
    )
    if intent not in INTERRUPTION_INTENT_TYPES:
        intent = "UNKNOWN_OR_AMBIGUOUS"

    action = {
        "STOP": "STOP_SPEECH_CANDIDATE",
        "PAUSE": "PAUSE_SPEECH_CANDIDATE",
        "REPEAT": "REPEAT_LAST_SPEECH_CANDIDATE",
        "RESUME": "RESUME_SPEECH_CANDIDATE",
        "CLARIFY": "CLARIFY_PREVIOUS_OUTPUT_CANDIDATE",
        "CORRECT": "CREATE_CORRECTION_EVENT_CANDIDATE",
        "EMERGENCY": "CREATE_SAFETY_OBSERVATION_CANDIDATE",
        "NEW_TASK": "CREATE_NEW_TASK_CANDIDATE",
        "CANCEL_TASK": "CREATE_CANCEL_TASK_CANDIDATE",
        "UNKNOWN_OR_AMBIGUOUS": "SUPPRESS_INTERRUPTION_CANDIDATE",
    }[intent]

    if intent == "RESUME":
        resume_condition = "route_or_context_freshness_recheck_required"
    elif intent == "REPEAT":
        resume_condition = "historical_only_rewrite_required"
    elif intent == "PAUSE":
        resume_condition = "paused_candidate_requires_resume_followup"
    else:
        resume_condition = None

    return {
        "schema_version": "speech_manager_interruption_plan_v1",
        "interruption_intent_type": intent,
        "selected_action_candidate": action,
        "resume_condition": resume_condition,
        "resume_allowed": intent == "RESUME",
        "freshness_check_required": intent in {"REPEAT", "RESUME", "CLARIFY"},
        "speech_gate_required": True,
        "priority_level": priority_candidate.get("priority_level"),
        "priority_numeric": priority_candidate.get("priority_numeric"),
        "source_chain": "speech_manager_interruption_controller_v1",
        **not_fact(),
    }
