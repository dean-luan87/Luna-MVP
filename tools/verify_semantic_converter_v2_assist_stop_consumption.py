# -*- coding: utf-8 -*-
"""
Verify Semantic V2 assisted consumption v0 for control.stop.

Asserts:
- '停止' with semantic enabled: assist_candidate=true AND assist_consumed=true
- '你是谁' with semantic enabled: no stop consumption
- semantic disabled: consumption false with no semantic signal
- dispatch behavior unchanged (dispatch_type + bridge route)
"""

from __future__ import annotations

import json
import os
from typing import Any, Dict, Tuple

from capabilities.voice.runtime.voice_input_session_manager import VoiceInputSessionManager


def _digest(res) -> Tuple[str, str]:
    dt = str(getattr(res, "dispatch_type", "") or "")
    route = ""
    bd = getattr(res, "bridge_decision", None)
    if bd is not None:
        r = getattr(bd, "route", None)
        route = str(getattr(r, "value", "") or r or "")
    return dt, route


def _run(text: str, *, enable_semantic: bool) -> Dict[str, Any]:
    env = dict(os.environ)
    if enable_semantic:
        env["LUNA_VOICE_ENABLE_SEMANTIC_CONVERTER_V2_STUB"] = "1"
    else:
        env.pop("LUNA_VOICE_ENABLE_SEMANTIC_CONVERTER_V2_STUB", None)

    os.environ.clear()
    os.environ.update(env)

    mgr = VoiceInputSessionManager()
    res = mgr.process_final_text_with_dispatch(
        text,
        now=1.0,
        is_task_mode=True,
        session_id="s",
        source_type="simulated",
    )
    md = dict(getattr(res, "metadata", {}) or {})
    return {
        "text": text,
        "dispatch": _digest(res),
        "shadow": md.get("semantic_v2_shadow"),
        "assist": md.get("semantic_v2_assist_v0"),
        "consumption": md.get("semantic_v2_assist_consumption_v0"),
    }


def main() -> None:
    base_stop = _run("停止", enable_semantic=False)
    sem_stop = _run("停止", enable_semantic=True)
    assert base_stop["dispatch"] == sem_stop["dispatch"], "dispatch_changed_for_stop"

    assert isinstance(sem_stop["assist"], dict), "assist_missing_for_stop"
    assert sem_stop["assist"].get("assist_candidate") is True, f"assist_candidate_not_true:{sem_stop['assist']}"

    cons = sem_stop["consumption"]
    assert isinstance(cons, dict), "consumption_missing_for_stop"
    assert cons.get("assist_consumed") is True, f"assist_consumed_not_true:{cons}"
    assert cons.get("semantic_intent") == "control.stop"

    # '你是谁' should not consume stop
    sem_id = _run("你是谁", enable_semantic=True)
    c2 = sem_id["consumption"]
    if isinstance(c2, dict):
        assert c2.get("semantic_intent") != "control.stop" or c2.get("assist_consumed") is False

    # semantic off should not consume
    c0 = base_stop["consumption"]
    assert isinstance(c0, dict), "consumption_missing_when_semantic_off"
    assert c0.get("assist_consumed") is False
    assert c0.get("semantic_intent") is None

    print("VERIFY_SEMANTIC_CONVERTER_V2_ASSIST_STOP_CONSUMPTION: ALL_OK")
    print(
        json.dumps(
            {
                "stop_baseline": base_stop,
                "stop_with_semantic": sem_stop,
                "identity_with_semantic": sem_id,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()

