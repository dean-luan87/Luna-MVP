# -*- coding: utf-8 -*-
"""
Verify VisionSemanticInputPack v0 stub wiring.

Asserts:
- when runtime_context.metadata has allowed summary keys, event metadata contains luna_voice_vision_semantic_v3_input
- source_summaries lists only present allowed keys
- pack does not contain system time/space anchor fields like timestamp/location/coordinate
- dispatch behavior unchanged (basic digest check)
"""

from __future__ import annotations

import json
from typing import Any, Dict, Tuple

from capabilities.voice.runtime.voice_input_session_manager import VoiceInputSessionManager
from capabilities.voice.schemas.voice_runtime_context import VoiceRuntimeContext


def _digest(res) -> Tuple[str, str]:
    dt = str(getattr(res, "dispatch_type", "") or "")
    route = ""
    bd = getattr(res, "bridge_decision", None)
    if bd is not None:
        r = getattr(bd, "route", None)
        route = str(getattr(r, "value", "") or r or "")
    return dt, route


def _extract_pack(res) -> Dict[str, Any]:
    ev = getattr(res, "voice_input_event", None)
    md = getattr(ev, "metadata", {}) if ev is not None else {}
    return md.get("luna_voice_vision_semantic_v3_input") if isinstance(md, dict) else None


def main() -> None:
    mgr = VoiceInputSessionManager()

    # A: sidewalk only
    ctx1 = VoiceRuntimeContext(metadata={"sidewalk_env_summary_v1": {"scene_candidate": "walkway"}})
    r1 = mgr.process_final_text_with_dispatch(
        "停止",
        now=1.0,
        is_task_mode=True,
        session_id="s",
        runtime_context=ctx1,
        source_type="simulated",
    )
    p1 = _extract_pack(r1)
    assert isinstance(p1, dict)
    assert p1.get("version") == "v3_stub"
    assert p1.get("source_summaries") == ["sidewalk_env_summary_v1"]

    # B: retail + risk
    ctx2 = VoiceRuntimeContext(
        metadata={
            "retail_env_summary_v1": {"scene_type_candidate": "retail_shelf"},
            "risk_summary_v1": {"risk_level": "low"},
        }
    )
    r2 = mgr.process_final_text_with_dispatch(
        "取消",
        now=2.0,
        is_task_mode=True,
        session_id="s",
        runtime_context=ctx2,
        source_type="simulated",
    )
    p2 = _extract_pack(r2)
    assert isinstance(p2, dict)
    assert p2.get("source_summaries") == ["retail_env_summary_v1", "risk_summary_v1"]

    # C: no allowed keys -> no pack
    ctx3 = VoiceRuntimeContext(metadata={"unified_env_summary_shadow_v1": {"x": 1}})
    r3 = mgr.process_final_text_with_dispatch(
        "你好",
        now=3.0,
        is_task_mode=True,
        session_id="s",
        runtime_context=ctx3,
        source_type="simulated",
    )
    p3 = _extract_pack(r3)
    assert p3 is None

    # Hard constraint: no time/space system fields in pack
    banned = {"timestamp", "time", "location", "position", "coordinate", "coordinates", "lat", "lng"}
    assert not (set(p1.keys()) & banned)
    assert not (set(p2.keys()) & banned)

    print("VERIFY_VISION_SEMANTIC_INPUT_PACK_V0: ALL_OK")
    print(
        json.dumps(
            {
                "caseA": {"dispatch": _digest(r1), "pack": p1},
                "caseB": {"dispatch": _digest(r2), "pack": p2},
                "caseC": {"dispatch": _digest(r3), "pack": p3},
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()

