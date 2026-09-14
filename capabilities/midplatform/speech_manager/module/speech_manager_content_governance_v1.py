from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.speech_manager.module.speech_manager_module_types_v1 import (
    not_fact,
)


FORBIDDEN_FACT_PHRASES = (
    "已经确认",
    "一定是",
    "已经到达",
    "已确认",
    "real tts",
)


def build_speech_manager_content_candidate_v1(
    input_candidate: Mapping[str, Any],
) -> Dict[str, Any]:
    original_text = str(input_candidate.get("speech_text") or "").strip()
    normalized_text = " ".join(original_text.split())
    if not normalized_text:
        normalized_text = "请先确认后再继续。"

    fact_risk = any(marker in normalized_text for marker in FORBIDDEN_FACT_PHRASES)
    content_class = "candidate_text" if not fact_risk else "candidate_text_degraded"
    speakable = not fact_risk

    return {
        "schema_version": "speech_manager_content_governance_v1",
        "original_text": original_text,
        "normalized_text": normalized_text,
        "speakable": speakable,
        "content_class": content_class,
        "guard_reason": "degraded_to_candidate_text"
        if fact_risk
        else "candidate_text_allowed",
        "speaker_identity_candidate": input_candidate.get("speaker_identity_candidate"),
        "speaker_identity_auto_confirmed": False,
        "asr_candidate_auto_fact": False,
        "generated_speech_candidate_only": True,
        **not_fact(),
    }
