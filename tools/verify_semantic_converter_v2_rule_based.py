# -*- coding: utf-8 -*-
"""
Minimal verification for SemanticConverterV2 rule-based v0.

This does NOT test mainline dispatch behavior; it verifies:
- stable payload shape
- limited intents for a small set of high-frequency inputs
- unknown for non-covered inputs
"""

from __future__ import annotations

import json

from capabilities.voice.runtime.semantic_converter_v2 import RuleBasedSemanticConverterV2
from capabilities.voice.runtime.voice_v1_session_state_anchor import VoiceV1SessionStateAnchor
from capabilities.voice.schemas.voice_input_event import VoiceInputEvent


EXPECTED_KEYS = {
    "version",
    "raw_text",
    "normalized_text",
    "intent",
    "entities",
    "references",
    "ambiguities",
    "requires_followup",
    "candidate_task_type",
    "confidence",
    "safety_flags",
}


def run_case(text: str) -> dict:
    ev = VoiceInputEvent(raw_text=text, text=text, normalized_text=text.strip(), wake_word_stripped="")
    anchor = VoiceV1SessionStateAnchor()
    anchor.begin_from_event(ev)
    conv = RuleBasedSemanticConverterV2()
    out = conv.convert(ev, session_state_anchor=anchor, runtime_context=None)
    assert out is not None
    missing = EXPECTED_KEYS - set(out.keys())
    assert not missing, f"missing_keys={sorted(missing)}"
    extra = set(out.keys()) - EXPECTED_KEYS
    assert not extra, f"extra_keys={sorted(extra)}"
    # hard constraint: must not include time/space system facts
    banned = {"timestamp", "time", "location", "position", "coordinate", "coordinates", "lat", "lng"}
    assert not (set(out.keys()) & banned), f"banned_fields_present={sorted(set(out.keys()) & banned)}"
    return out


def main() -> None:
    tests = [
        ("停止", "control.stop"),
        ("继续", "control.resume"),
        ("重复一遍", "control.repeat"),
        ("取消", "control.cancel"),
        ("是", "confirm.yes"),
        ("不是", "confirm.no"),
        ("你是谁", "ask.identity"),
        ("你现在能做什么", "ask.capability"),
        ("你刚刚说了什么", "ask.last_reply"),
        ("今天天气怎么样", "unknown"),
        ("带我去医院", "unknown"),
    ]

    results = []
    for text, expected_intent in tests:
        out = run_case(text)
        got = out.get("intent")
        assert got == expected_intent, f"text={text!r} expected={expected_intent!r} got={got!r}"
        results.append({"in": text, "intent": got, "confidence": out.get("confidence"), "version": out.get("version")})

    print("VERIFY_SEMANTIC_CONVERTER_V2_RULE_BASED: ALL_OK")
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

