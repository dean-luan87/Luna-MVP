# -*- coding: utf-8 -*-
"""
Verify V3 -> V2 vision shadow read (SemanticConverterV2).

Asserts:
- when V3 pack exists in event.metadata, V2 payload includes vision_shadow with seen_not_interpreted and correct sources
- when V3 pack absent, vision_input_seen=false (or status not_seen)
- intent is unchanged by vision shadow (still driven only by rule text)
"""

from __future__ import annotations

import json

from capabilities.voice.runtime.semantic_converter_v2 import RuleBasedSemanticConverterV2
from capabilities.voice.runtime.voice_v1_session_state_anchor import VoiceV1SessionStateAnchor
from capabilities.voice.schemas.voice_input_event import VoiceInputEvent


def main() -> None:
    conv = RuleBasedSemanticConverterV2()

    # A: with V3 pack
    ev1 = VoiceInputEvent(raw_text="停止", text="停止", normalized_text="停止", metadata={})
    ev1.metadata["luna_voice_vision_semantic_v3_input"] = {
        "version": "v3_stub",
        "source_summaries": ["sidewalk_env_summary_v1", "risk_summary_v1"],
        "scene_type": None,
        "task_relevant_facts": [],
        "risk_facts": [],
        "environment_facts": [],
        "uncertainties": [],
        "confidence": 0.0,
        "anchor_ref": None,
    }
    anchor = VoiceV1SessionStateAnchor()
    anchor.begin_from_event(ev1)
    out1 = conv.convert(ev1, session_state_anchor=anchor, runtime_context=None)
    assert out1 is not None
    vs1 = out1.get("vision_shadow")
    assert isinstance(vs1, dict)
    assert vs1.get("vision_input_seen") is True
    assert vs1.get("vision_shadow_status") == "seen_not_interpreted"
    assert vs1.get("vision_sources") == ["sidewalk_env_summary_v1", "risk_summary_v1"]
    # intent should remain rule-driven by text, not by vision
    assert out1.get("intent") == "control.stop"

    # B: without V3 pack
    ev2 = VoiceInputEvent(raw_text="停止", text="停止", normalized_text="停止", metadata={})
    anchor2 = VoiceV1SessionStateAnchor()
    anchor2.begin_from_event(ev2)
    out2 = conv.convert(ev2, session_state_anchor=anchor2, runtime_context=None)
    assert out2 is not None
    vs2 = out2.get("vision_shadow")
    assert isinstance(vs2, dict)
    assert vs2.get("vision_input_seen") is False
    assert vs2.get("vision_shadow_status") == "not_seen"
    assert vs2.get("vision_sources") == []
    assert out2.get("intent") == "control.stop"

    print("VERIFY_SEMANTIC_CONVERTER_V2_VISION_SHADOW_READ: ALL_OK")
    print(
        json.dumps(
            {"with_pack": out1.get("vision_shadow"), "without_pack": out2.get("vision_shadow")},
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()

