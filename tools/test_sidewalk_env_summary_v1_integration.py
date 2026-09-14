#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sidewalk_env_summary_v1 主线接入验证：稳定化 → runtime_context → sidewalk_nav_v1 消费。
"""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from capabilities.voice.runtime.voice_final_text_dispatcher import (  # noqa: E402
    _maybe_stabilize_runtime_context_sidewalk_env_v1,
)
from capabilities.voice.runtime.voice_input_session_manager import VoiceInputSessionManager  # noqa: E402
from capabilities.voice.schemas.voice_input_event import VoiceInputEvent  # noqa: E402
from capabilities.voice.schemas.voice_runtime_context import VoiceRuntimeContext  # noqa: E402


def _assert(name: str, cond: bool, msg: str = "") -> None:
    if not cond:
        raise AssertionError(f"[{name}] {msg}")


def main() -> None:
    os.environ["LUNA_ENABLE_SIDEWALK_ENV_SUMMARY_STABILIZER_V1"] = "1"
    os.environ["LUNA_ENABLE_SIDEWALK_NAV_V1"] = "1"
    os.environ["LUNA_SIDEWALK_NAV_WHITEBOX_ONLY"] = "1"

    now = time.time()
    ev = VoiceInputEvent(
        request_id="r1",
        session_id="s1",
        timestamp=now,
        raw_text="test",
        normalized_text="test",
        is_task_mode=True,
    )

    # 1) 原始字段 → 稳定化写入 metadata
    raw_ctx = VoiceRuntimeContext(
        current_session_id="s1",
        metadata={
            "sidewalk_env_summary_v1": {
                "scene_candidate": "outdoor_walkway",
                "path_confidence": 0.82,
                "is_outdoor": True,
            },
            "risk_summary_v1": {"risk_level": "low", "risk_type": "none"},
        },
    )
    risk_ref = raw_ctx.metadata["risk_summary_v1"]
    st = _maybe_stabilize_runtime_context_sidewalk_env_v1(ev, raw_ctx)
    sw = st.metadata.get("sidewalk_env_summary_v1") or {}
    _assert("schema", str(sw.get("summary_schema_version") or "").startswith("sidewalk_env_summary_v1/"))
    _assert("fresh", sw.get("summary_freshness") == "fresh")
    _assert("risk_unchanged", st.metadata.get("risk_summary_v1") is risk_ref)

    # 2) 已稳定化 dict → 不重复 build
    st2 = _maybe_stabilize_runtime_context_sidewalk_env_v1(ev, st)
    _assert("idempotent", st2.metadata.get("sidewalk_env_summary_v1") is sw)

    # 3) stale
    ev_old = VoiceInputEvent(
        request_id="r2",
        session_id="s1",
        timestamp=now,
        raw_text="t",
        normalized_text="t",
        is_task_mode=True,
    )
    ctx_stale = VoiceRuntimeContext(
        metadata={
            "sidewalk_env_summary_v1": {
                "scene_candidate": "outdoor_walkway",
                "path_confidence": 0.9,
                "is_outdoor": True,
                "event_timestamp": now - 30.0,
            }
        },
    )
    sws = _maybe_stabilize_runtime_context_sidewalk_env_v1(ev_old, ctx_stale).metadata.get("sidewalk_env_summary_v1") or {}
    _assert("stale", sws.get("summary_freshness") == "stale")

    # 4) ambiguous
    ctx_amb = VoiceRuntimeContext(
        metadata={
            "sidewalk_env_summary_v1": {
                "scene_candidate": "unknown",
                "path_confidence": 0.15,
                "is_outdoor": False,
            }
        },
    )
    swa = _maybe_stabilize_runtime_context_sidewalk_env_v1(ev, ctx_amb).metadata.get("sidewalk_env_summary_v1") or {}
    _assert("ambiguous", swa.get("summary_freshness") == "ambiguous")

    # 5) 端到端：sidewalk_nav 消费稳定化 summary
    mgr = VoiceInputSessionManager()
    res = mgr.process_final_text_with_dispatch(
        "帮我设一个三分钟的计时器",
        now=now,
        is_task_mode=True,
        session_id="s_sw",
        runtime_context=VoiceRuntimeContext(
            current_session_id="s_sw",
            metadata={
                "sidewalk_env_summary_v1": {
                    "scene_candidate": "outdoor_walkway",
                    "path_confidence": 0.8,
                    "is_outdoor": True,
                }
            },
        ),
    )
    md = res.metadata or {}
    _assert("wb_attached", "sidewalk_nav_v1" in md)
    wb = md.get("sidewalk_nav_v1") or {}
    _assert("nav_hint", isinstance(wb.get("navigation_hint"), str))

    # 6) 关闭稳定化：原始 dict 无 schema
    os.environ["LUNA_ENABLE_SIDEWALK_ENV_SUMMARY_STABILIZER_V1"] = "0"
    ctx_raw_only = VoiceRuntimeContext(
        metadata={
            "sidewalk_env_summary_v1": {
                "scene_candidate": "outdoor_walkway",
                "path_confidence": 0.7,
                "is_outdoor": True,
            }
        },
    )
    st_off = _maybe_stabilize_runtime_context_sidewalk_env_v1(ev, ctx_raw_only)
    raw_back = st_off.metadata.get("sidewalk_env_summary_v1") or {}
    _assert("stabilizer_off", "summary_schema_version" not in raw_back)

    os.environ.pop("LUNA_ENABLE_SIDEWALK_ENV_SUMMARY_STABILIZER_V1", None)

    print("All sidewalk_env_summary_v1 integration checks passed.")


if __name__ == "__main__":
    main()
