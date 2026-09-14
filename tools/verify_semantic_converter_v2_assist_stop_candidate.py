# -*- coding: utf-8 -*-
"""
Verify Semantic V2 Assisted Routing v0 (control.stop only) metadata output.

This script asserts:
- with semantic enabled, '停止' yields assist_candidate=true
- '你是谁' does not produce stop candidate
- with semantic disabled, stop candidate is not produced
- dispatch behavior remains unchanged (dispatch_type + bridge route)
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
        is_task_mode=True,  # keep router open without wake word
        session_id="s",
        source_type="simulated",
    )
    md = dict(getattr(res, "metadata", {}) or {})
    return {
        "text": text,
        "dispatch": _digest(res),
        "shadow": md.get("semantic_v2_shadow"),
        "assist": md.get("semantic_v2_assist_v0"),
    }


def main() -> None:
    # A: stop
    base_stop = _run("停止", enable_semantic=False)
    sem_stop = _run("停止", enable_semantic=True)
    assert base_stop["dispatch"] == sem_stop["dispatch"], "dispatch_changed_for_stop"
    assert isinstance(sem_stop["assist"], dict), "assist_missing_for_stop"
    assert sem_stop["assist"].get("assist_candidate") is True, f"stop_candidate_not_true:{sem_stop['assist']}"
    assert sem_stop["assist"].get("semantic_intent") == "control.stop"

    # B: identity question must not create stop candidate
    sem_id = _run("你是谁", enable_semantic=True)
    assist_id = sem_id["assist"]
    if isinstance(assist_id, dict):
        assert assist_id.get("semantic_intent") != "control.stop" or assist_id.get("assist_candidate") is False

    # C: semantic off should not create stop candidate
    assist_off = base_stop["assist"]
    if isinstance(assist_off, dict):
        assert assist_off.get("assist_candidate") is False

    print("VERIFY_SEMANTIC_CONVERTER_V2_ASSIST_STOP_CANDIDATE: ALL_OK")
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

