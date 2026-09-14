# -*- coding: utf-8 -*-
"""
Luna Voice V2: Semantic Converter (Stage-1).

Hard boundaries:
- Must not fabricate facts (No Fabrication Rule still applies).
- Must not generate system-level time/space anchors; only consume platform-injected anchors.
- Must return JSON-serializable output (dict of primitives/lists/dicts).
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Protocol

from capabilities.voice.runtime.voice_v1_session_state_anchor import VoiceV1SessionStateAnchor
from capabilities.voice.schemas.voice_input_event import VoiceInputEvent
from capabilities.voice.schemas.voice_runtime_context import VoiceRuntimeContext


SemanticV2Payload = Dict[str, Any]


class SemanticConverterV2(Protocol):
    def convert(
        self,
        event: VoiceInputEvent,
        *,
        session_state_anchor: VoiceV1SessionStateAnchor,
        runtime_context: Optional[VoiceRuntimeContext] = None,
    ) -> Optional[SemanticV2Payload]:
        """
        Convert current voice input into a minimal structured semantic payload.

        Requirements:
        - Return a JSON-serializable dict, or None (no-op).
        - Must not mutate event/session_state_anchor/runtime_context.
        - Must not fabricate missing information.
        """

