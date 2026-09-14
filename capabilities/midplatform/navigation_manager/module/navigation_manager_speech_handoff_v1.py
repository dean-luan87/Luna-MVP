from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.navigation_manager.module.navigation_manager_module_types_v1 import (
    not_fact,
)


def build_navigation_speech_handoff_candidate_v1(
    input_candidate: Mapping[str, Any], guidance_candidate: Mapping[str, Any]
) -> Dict[str, Any]:
    guidance = guidance_candidate.get("guidance_candidate") or {}
    guidance_text = str(guidance.get("guidance_text_candidate") or "")
    return {
        "schema_version": "navigation_manager_speech_handoff_v1",
        "speech_handoff_candidate": {
            "candidate_id": f"speech_handoff_{input_candidate.get('navigation_request_id')}",
            "request_id": f"speech_req_{input_candidate.get('navigation_request_id')}",
            "source_module": "luna.navigation_manager",
            "priority_level": "P1_navigation_critical",
            "speech_text": guidance_text,
            "candidate_only": True,
            **not_fact(),
        },
        **not_fact(),
    }
