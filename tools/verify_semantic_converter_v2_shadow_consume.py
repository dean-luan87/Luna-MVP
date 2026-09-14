# -*- coding: utf-8 -*-
"""
Verify SemanticConverterV2 shadow consume wiring.

Goals:
- V2 semantic payload (from ev.metadata["luna_voice_semantic_v2"]) is read by dispatcher
- Shadow summary is attached into dispatch result metadata["semantic_v2_shadow"]
- Dispatch behavior (dispatch_type / bridge route when present) is unchanged vs baseline
"""

from __future__ import annotations

import json
import os
from typing import Any, Dict, Optional, Tuple

from capabilities.voice.runtime.voice_input_session_manager import VoiceInputSessionManager


def _digest(res) -> Tuple[str, str]:
    dt = str(getattr(res, "dispatch_type", "") or "")
    route = ""
    bd = getattr(res, "bridge_decision", None)
    if bd is not None:
        r = getattr(bd, "route", None)
        route = str(getattr(r, "value", "") or r or "")
    return dt, route


def _run_once(text: str, *, enable_semantic: bool) -> Dict[str, Any]:
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
        is_task_mode=True,  # avoid wake-word gating; does not change dispatcher logic
        session_id="s",
        source_type="simulated",
    )
    md = dict(getattr(res, "metadata", {}) or {})
    shadow = md.get("semantic_v2_shadow")
    return {"text": text, "dispatch": _digest(res), "shadow": shadow, "dispatch_type": res.dispatch_type}


def main() -> None:
    tests = ["停止", "你是谁", "今天天气怎么样"]
    out = []
    for t in tests:
        base = _run_once(t, enable_semantic=False)
        with_sem = _run_once(t, enable_semantic=True)
        assert base["dispatch"] == with_sem["dispatch"], f"dispatch_changed text={t!r} base={base['dispatch']} v2={with_sem['dispatch']}"
        shadow = with_sem["shadow"]
        assert isinstance(shadow, dict), f"shadow_missing text={t!r} shadow={shadow!r}"
        for k in ("semantic_intent", "shadow_status", "dispatch_route", "dispatch_kind", "note"):
            assert k in shadow, f"shadow_key_missing text={t!r} missing={k!r}"
        out.append({"baseline": base, "with_semantic": with_sem})

    print("VERIFY_SEMANTIC_CONVERTER_V2_SHADOW_CONSUME: ALL_OK")
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

