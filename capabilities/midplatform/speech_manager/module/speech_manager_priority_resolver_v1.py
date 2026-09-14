from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.speech_manager.module.speech_manager_module_types_v1 import (
    SPEECH_PRIORITY_ORDER,
    not_fact,
)


def build_speech_manager_priority_candidate_v1(
    input_candidate: Mapping[str, Any],
) -> Dict[str, Any]:
    priority_label = str(input_candidate.get("priority_level") or "P4")
    numeric = SPEECH_PRIORITY_ORDER.get(priority_label, SPEECH_PRIORITY_ORDER["P4"])
    policy = {
        "P0": "safety_immediate",
        "P1": "navigation_critical",
        "P2": "task_guidance",
        "P3": "ocr_or_static_guidance",
        "P4": "clarification_or_status",
        "P5": "low_priority",
    }.get(priority_label, "clarification_or_status")
    return {
        "schema_version": "speech_manager_priority_candidate_v1",
        "priority_level": priority_label,
        "priority_numeric": numeric,
        "priority_policy": policy,
        "priority_can_interrupt_lower_priority": priority_label in {"P0", "P1"},
        "priority_source": str(
            input_candidate.get("source_module") or "luna.speech_manager"
        ),
        **not_fact(),
    }
