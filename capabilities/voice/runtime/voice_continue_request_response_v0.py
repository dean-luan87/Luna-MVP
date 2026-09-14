# -*- coding: utf-8 -*-
"""
Continue Request Response v0 — fixed confirmation template when Information Gate blocks.

Read-only helpers: phrase detection + trigger conditions only.
No resume/repeat execution; no gate logic changes.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from capabilities.voice.schemas.voice_input_event import VoiceInputEvent

if TYPE_CHECKING:
    from capabilities.voice.runtime.voice_final_text_dispatch_result import VoiceFinalTextDispatchResult

# Single fixed template (Topic 04 / Information Gate hit + continue-request phrasing).
CONTINUE_REQUEST_INFO_CONFIRM_TEMPLATE_V0: str = (
    "我现在还不能继续，因为关键信息还不明确。请先告诉我你指的是哪一个对象。"
)

_CONTINUE_REQUEST_PHRASES_V0: tuple[str, ...] = (
    "继续",
    "按我说的做",
    "别停",
)


def text_contains_continue_request_v0(text: str) -> bool:
    """Conservative substring match; does not imply execution permission."""
    t = (text or "").strip()
    if not t:
        return False
    return any(p in t for p in _CONTINUE_REQUEST_PHRASES_V0)


def should_trigger_continue_request_info_confirmation_template_v0(
    res: "VoiceFinalTextDispatchResult",
    *,
    event: VoiceInputEvent,
) -> bool:
    """
    True iff Information Confirmation Gate v0 has blocked submit with requires_confirmation,
    and user text looks like a continue/proceed request (minimal phrase set).
    """
    ig = (res.metadata or {}).get("information_confirmation_gate_v0")
    if not isinstance(ig, dict):
        return False
    if ig.get("gate_passed") is not False:
        return False
    if ig.get("requires_confirmation") is not True:
        return False
    u = (event.wake_word_stripped or event.normalized_text or event.effective_raw_text() or "").strip()
    return text_contains_continue_request_v0(u)
