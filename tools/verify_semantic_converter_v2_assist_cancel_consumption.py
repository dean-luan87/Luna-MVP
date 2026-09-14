# -*- coding: utf-8 -*-
"""
Verify control.cancel assisted candidate + consumption (v0 mirror of stop).

Asserts:
- '取消' with semantic enabled: candidate=true AND consumed=true
- semantic disabled: candidate/consumption remain false/no-signal
- dispatch behavior unchanged (dispatch_type + bridge route)
- V1 minimal flow unaffected (run separately)
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
        "assist_cancel": md.get("semantic_v2_assist_v0_cancel"),
        "consumption_cancel": md.get("semantic_v2_assist_consumption_v0_cancel"),
    }


def main() -> None:
    base = _run("取消", enable_semantic=False)
    sem = _run("取消", enable_semantic=True)
    assert base["dispatch"] == sem["dispatch"], f"dispatch_changed base={base['dispatch']} sem={sem['dispatch']}"

    a = sem["assist_cancel"]
    assert isinstance(a, dict), f"assist_cancel_missing:{a!r}"
    assert a.get("assist_candidate") is True, f"assist_candidate_not_true:{a}"
    assert a.get("semantic_intent") == "control.cancel"

    c = sem["consumption_cancel"]
    assert isinstance(c, dict), f"consumption_cancel_missing:{c!r}"
    assert c.get("assist_consumed") is True, f"assist_consumed_not_true:{c}"
    assert c.get("semantic_intent") == "control.cancel"

    # semantic off should show no-signal structures
    a0 = base["assist_cancel"]
    c0 = base["consumption_cancel"]
    assert isinstance(a0, dict) and a0.get("assist_candidate") is False and a0.get("semantic_intent") is None
    assert isinstance(c0, dict) and c0.get("assist_consumed") is False and c0.get("semantic_intent") is None

    print("VERIFY_SEMANTIC_CONVERTER_V2_ASSIST_CANCEL_CONSUMPTION: ALL_OK")
    print(json.dumps({"baseline": base, "with_semantic": sem}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

