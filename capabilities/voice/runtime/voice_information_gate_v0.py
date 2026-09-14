# -*- coding: utf-8 -*-
"""
Information Sufficiency / Confirmation Gate v0 (Missing/Ambiguous Reference).

Hard constraints:
- Must NOT fabricate reference bindings.
- Must be conservative: if obvious deictic terms are present and no unique binding facts exist, require confirmation.
- Must NOT use vision summaries or memory to auto-bind references in v0.
"""

from __future__ import annotations

from typing import Any, Optional, Tuple

from capabilities.voice.bridge.bridge_decision import BridgeDecision
from capabilities.voice.schemas.voice_input_event import VoiceInputEvent
from capabilities.voice.runtime.voice_v1_session_state_anchor import VoiceV1SessionStateAnchor


_DEICTIC_TERMS_V0: Tuple[str, ...] = ("这个", "那个", "这里", "那里")


def _contains_deictic_term(text: str) -> bool:
    t = (text or "").strip()
    if not t:
        return False
    return any(term in t for term in _DEICTIC_TERMS_V0)


def _proposal_has_explicit_binding(proposal: Any) -> bool:
    """
    v0: extremely conservative. Only treat as bound if proposal carries an explicit target identifier.
    Most Stage-1 proposals do not; device_action alone is NOT a binding.
    """
    if proposal is None:
        return False
    for attr in ("target_id", "object_id", "place_id", "destination_id", "reference_id"):
        try:
            v = getattr(proposal, attr, None)
        except Exception:
            v = None
        if v is not None and str(v).strip():
            return True
    return False


def evaluate_missing_or_ambiguous_reference_v0(
    *,
    event: VoiceInputEvent,
    session_state_anchor: Optional[VoiceV1SessionStateAnchor],
    bridge_decision: Optional[BridgeDecision],
) -> Tuple[bool, str]:
    """
    Returns (requires_confirmation, reason_code).

    v0 rule:
    - If input contains a deictic term AND we do NOT have explicit binding facts -> requires confirmation.
    - v0 does not attempt to bind from last_user_text/last_system_text or vision summaries.
    """
    text = (event.wake_word_stripped or event.normalized_text or event.effective_raw_text() or "").strip()
    if not _contains_deictic_term(text):
        return False, "ok"

    # v0: session_state_anchor has no binding structure -> treated as insufficient by default.
    _ = session_state_anchor
    if bridge_decision is not None and _proposal_has_explicit_binding(getattr(bridge_decision, "proposal", None)):
        return False, "ok"

    return True, "missing_or_ambiguous_reference"

