# -*- coding: utf-8 -*-
"""
Luna Voice V2 semantic converter stub.

This module intentionally does NOT connect to any model/provider. It exists to verify:
- call location is correct
- payload structure is stable and carried via VoiceInputEvent.metadata
- mainline behavior is unchanged when converter fails/returns None
"""

from __future__ import annotations

import os
import re
from typing import Any, Dict, Optional, Tuple

from capabilities.voice.interfaces.semantic_converter_v2 import SemanticConverterV2, SemanticV2Payload
from capabilities.voice.runtime.voice_v1_session_state_anchor import VoiceV1SessionStateAnchor
from capabilities.voice.schemas.voice_input_event import VoiceInputEvent
from capabilities.voice.schemas.voice_runtime_context import VoiceRuntimeContext


def semantic_v2_stub_enabled() -> bool:
    return str(os.getenv("LUNA_VOICE_ENABLE_SEMANTIC_CONVERTER_V2_STUB", "0")).strip() == "1"

def _base_payload(raw: str, norm: str, *, version: str) -> Dict[str, Any]:
    # Hard boundaries: keep everything conservative; do not invent entities/references/task type.
    return {
        "version": version,
        "raw_text": raw,
        "normalized_text": norm,
        "intent": "unknown",
        "entities": [],
        "references": [],
        "ambiguities": [],
        "requires_followup": False,
        "candidate_task_type": None,
        "confidence": 0.0,
        "safety_flags": [],
    }


def _normalize_for_rule_match(text: str) -> str:
    t = (text or "").strip().lower()
    # remove whitespace-like chars for short commands
    t = re.sub(r"\s+", "", t)
    return t


def _rule_match_intent(norm_for_match: str) -> Tuple[str, float]:
    """
    Rule-based minimal intent mapping.
    Keep it small, explainable, conservative.
    """
    # 控制类
    if norm_for_match in {"停一下", "停止", "停", "暂停"}:
        return "control.stop", 0.8
    if norm_for_match in {"继续"}:
        return "control.resume", 0.8
    if norm_for_match in {"重复一遍", "再说一遍", "再讲一遍", "重复", "再来一遍"}:
        return "control.repeat", 0.8
    if norm_for_match in {"取消"}:
        return "control.cancel", 0.8
    if norm_for_match in {"结束对话"}:
        return "control.end_conversation", 0.8

    # 确认类（尽量强命中短词）
    if norm_for_match in {"是", "对", "好"}:
        return "confirm.yes", 0.8
    if norm_for_match in {"不是", "不对", "不要"}:
        return "confirm.no", 0.8

    # 基础问询类
    if norm_for_match in {"你是谁"}:
        return "ask.identity", 0.8
    if norm_for_match in {"你现在能做什么", "你能做什么"}:
        return "ask.capability", 0.8
    if norm_for_match in {"你刚刚说了什么", "你刚才说了什么"}:
        return "ask.last_reply", 0.8

    return "unknown", 0.0


class NoOpSemanticConverterV2(SemanticConverterV2):
    """
    Default stub implementation.

    Test modes (dev only):
    - LUNA_VOICE_SEMANTIC_V2_STUB_MODE=return_none -> returns None
    - LUNA_VOICE_SEMANTIC_V2_STUB_MODE=raise -> raises RuntimeError
    """

    def convert(
        self,
        event: VoiceInputEvent,
        *,
        session_state_anchor: VoiceV1SessionStateAnchor,
        runtime_context: Optional[VoiceRuntimeContext] = None,
    ) -> Optional[SemanticV2Payload]:
        mode = str(os.getenv("LUNA_VOICE_SEMANTIC_V2_STUB_MODE", "")).strip().lower()
        if mode == "return_none":
            return None
        if mode == "raise":
            raise RuntimeError("semantic_v2_stub_forced_error")

        raw = (event.effective_raw_text() or "").strip()
        norm = str(event.wake_word_stripped or event.normalized_text or raw).strip()

        return _base_payload(raw, norm, version="v2_stub")


class RuleBasedSemanticConverterV2(SemanticConverterV2):
    """
    Rule-based minimal converter (v0).

    Scope (only):
    - 控制类：stop/resume/repeat/cancel/end_conversation
    - 确认类：yes/no
    - 基础问询：identity/capability/last_reply

    Everything else stays conservative unknown.
    """

    def convert(
        self,
        event: VoiceInputEvent,
        *,
        session_state_anchor: VoiceV1SessionStateAnchor,
        runtime_context: Optional[VoiceRuntimeContext] = None,
    ) -> Optional[SemanticV2Payload]:
        # Keep dev test modes consistent with stub.
        mode = str(os.getenv("LUNA_VOICE_SEMANTIC_V2_STUB_MODE", "")).strip().lower()
        if mode == "return_none":
            return None
        if mode == "raise":
            raise RuntimeError("semantic_v2_rule_based_forced_error")

        raw = (event.effective_raw_text() or "").strip()
        norm = str(event.wake_word_stripped or event.normalized_text or raw).strip()
        payload = _base_payload(raw, norm, version="v2_rule_based_v0")

        # V3 -> V2 shadow read (read-only): see vision semantic input pack but do not interpret it.
        try:
            v3 = (event.metadata or {}).get("luna_voice_vision_semantic_v3_input")
            seen = isinstance(v3, dict)
            sources = []
            if seen:
                ss = v3.get("source_summaries")
                if isinstance(ss, list):
                    sources = [str(x) for x in ss if str(x)]
            payload["vision_shadow"] = {
                "vision_input_seen": bool(seen),
                "vision_sources": sources,
                "vision_shadow_status": "seen_not_interpreted" if seen else "not_seen",
            }
        except Exception:
            payload["vision_shadow"] = {
                "vision_input_seen": False,
                "vision_sources": [],
                "vision_shadow_status": "not_seen",
            }

        intent, conf = _rule_match_intent(_normalize_for_rule_match(norm))
        if intent != "unknown":
            payload["intent"] = intent
            payload["confidence"] = conf
        return payload


_DEFAULT_CONVERTER: SemanticConverterV2 = RuleBasedSemanticConverterV2()


def get_default_semantic_converter_v2() -> SemanticConverterV2:
    return _DEFAULT_CONVERTER

