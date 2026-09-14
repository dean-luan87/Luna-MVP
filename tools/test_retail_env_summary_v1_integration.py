#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
retail_env_summary_v1 主线接入验证：稳定化 → runtime_context → retail_find_item_v1 消费。
"""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from capabilities.voice.runtime.voice_final_text_dispatcher import (  # noqa: E402
    _maybe_stabilize_runtime_context_retail_env_v1,
)
from capabilities.voice.runtime.voice_input_session_manager import VoiceInputSessionManager  # noqa: E402
from capabilities.voice.schemas.voice_input_event import VoiceInputEvent  # noqa: E402
from capabilities.voice.schemas.voice_runtime_context import VoiceRuntimeContext  # noqa: E402


def _assert(name: str, cond: bool, msg: str = "") -> None:
    if not cond:
        raise AssertionError(f"[{name}] {msg}")


def main() -> None:
    os.environ["LUNA_ENABLE_RETAIL_ENV_SUMMARY_STABILIZER_V1"] = "1"
    os.environ["LUNA_ENABLE_RETAIL_FIND_ITEM_V1"] = "1"
    os.environ["LUNA_RETAIL_FIND_ITEM_WHITEBOX_ONLY"] = "1"

    now = time.time()
    ev = VoiceInputEvent(
        request_id="r1",
        session_id="s1",
        timestamp=now,
        raw_text="test",
        normalized_text="test",
        is_task_mode=True,
    )

    # 1) 原始字段 → 稳定化写入 metadata（且不影响 intent/risk）
    intent_ref = {"active": True, "query": "牛奶", "ocr_budget_ok": True}
    risk_ref = {"risk_level": "low", "risk_type": "none"}
    raw_ctx = VoiceRuntimeContext(
        current_session_id="s1",
        metadata={
            "retail_env_summary_v1": {
                "scene_type_candidate": "retail_shelf",
                "retail_context_confidence": 0.72,
                "shelf_visible": True,
                "gating_passed": True,
            },
            "find_item_intent_summary_v1": intent_ref,
            "risk_summary_v1": risk_ref,
        },
    )
    st = _maybe_stabilize_runtime_context_retail_env_v1(ev, raw_ctx)
    re = st.metadata.get("retail_env_summary_v1") or {}
    _assert("schema", str(re.get("summary_schema_version") or "").startswith("retail_env_summary_v1/"))
    _assert("freshness_present", re.get("summary_freshness") in ("fresh", "stale", "ambiguous"))
    _assert("intent_unchanged", st.metadata.get("find_item_intent_summary_v1") is intent_ref)
    _assert("risk_unchanged", st.metadata.get("risk_summary_v1") is risk_ref)

    # 2) 已稳定化 dict → 不重复 build
    st2 = _maybe_stabilize_runtime_context_retail_env_v1(ev, st)
    _assert("idempotent", st2.metadata.get("retail_env_summary_v1") is re)

    # 3) stale
    ctx_stale = VoiceRuntimeContext(
        metadata={
            "retail_env_summary_v1": {
                "scene_type": "retail_aisle",
                "retail_context_confidence": 0.9,
                "shelf_visible": True,
                "event_timestamp": now - 60.0,
            }
        },
    )
    rs = _maybe_stabilize_runtime_context_retail_env_v1(ev, ctx_stale).metadata.get("retail_env_summary_v1") or {}
    _assert("stale", rs.get("summary_freshness") == "stale")

    # 4) ambiguous
    ctx_amb = VoiceRuntimeContext(
        metadata={
            "retail_env_summary_v1": {
                "scene_type": "unknown",
                "retail_context_confidence": 0.18,
                "shelf_visible": False,
            }
        },
    )
    ra = _maybe_stabilize_runtime_context_retail_env_v1(ev, ctx_amb).metadata.get("retail_env_summary_v1") or {}
    _assert("ambiguous", ra.get("summary_freshness") == "ambiguous")

    # 5) 端到端：retail_find_item 消费稳定化 summary（仍 whitebox-only）
    mgr = VoiceInputSessionManager()
    res = mgr.process_final_text_with_dispatch(
        "我在找牛奶",
        now=now,
        is_task_mode=True,
        session_id="s_retail",
        runtime_context=VoiceRuntimeContext(
            current_session_id="s_retail",
            metadata={
                "retail_env_summary_v1": {
                    "scene_type_candidate": "retail_shelf",
                    "retail_context_confidence": 0.8,
                    "shelf_visible": True,
                    "gating_passed": True,
                },
                "find_item_intent_summary_v1": {
                    "active": True,
                    "query": "牛奶",
                    "ocr_budget_ok": True,
                    "need_text_to_progress": True,
                },
            },
        ),
    )
    md = res.metadata or {}
    _assert("wb_attached", "retail_find_item_v1" in md)
    wb = md.get("retail_find_item_v1") or {}
    _assert("final_spoken_empty", wb.get("final_spoken_output") == "")

    # 6) 关闭稳定化：原始 dict 无 schema
    os.environ["LUNA_ENABLE_RETAIL_ENV_SUMMARY_STABILIZER_V1"] = "0"
    ctx_raw_only = VoiceRuntimeContext(
        metadata={
            "retail_env_summary_v1": {
                "scene_type_candidate": "retail_shelf",
                "retail_context_confidence": 0.7,
                "shelf_visible": True,
            }
        },
    )
    st_off = _maybe_stabilize_runtime_context_retail_env_v1(ev, ctx_raw_only)
    raw_back = st_off.metadata.get("retail_env_summary_v1") or {}
    _assert("stabilizer_off", "summary_schema_version" not in raw_back)

    os.environ.pop("LUNA_ENABLE_RETAIL_ENV_SUMMARY_STABILIZER_V1", None)

    print("All retail_env_summary_v1 integration checks passed.")


if __name__ == "__main__":
    main()

