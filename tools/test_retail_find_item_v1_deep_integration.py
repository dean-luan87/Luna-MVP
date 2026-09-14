#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
retail_find_item_v1：主线深联调（阶段 1 / whitebox-only）验证

覆盖：
1) 默认关闭 → 主链零侵入（metadata 无 retail_find_item_v1）
2) 开启 + whitebox-only + context 有零售环境摘要与找货意图摘要 → 白盒正常生成并挂载
3) 风险压制（high/critical 或 risk_interrupt_preempt）→ final_spoken_output 为空且 output_suppressed_by_risk=true
4) 输出内容不变（dispatch_type/notes 不应因接入改变）
5) 非零售环境或无意图：不误触发外显（深接入阶段本就不外显；但应保持 gating/ocr_trigger_reason 合理）
"""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from capabilities.voice.runtime.voice_input_session_manager import (  # noqa: E402
    VoiceInputSessionManager,
)
from capabilities.voice.schemas.voice_runtime_context import VoiceRuntimeContext  # noqa: E402


def _assert(name: str, cond: bool, msg: str = "") -> None:
    if not cond:
        raise AssertionError(f"[{name}] {msg}")


def _run(*, enable: str, wb_only: str, ctx: VoiceRuntimeContext) -> dict:
    os.environ["LUNA_ENABLE_RETAIL_FIND_ITEM_V1"] = enable
    os.environ["LUNA_RETAIL_FIND_ITEM_WHITEBOX_ONLY"] = wb_only

    mgr = VoiceInputSessionManager()
    res = mgr.process_final_text_with_dispatch(
        "帮我设一个三分钟的计时器",
        now=time.time(),
        is_task_mode=True,
        session_id="s_retail",
        runtime_context=ctx,
    )
    return res.to_dict()


def main() -> None:
    ctx_ok = VoiceRuntimeContext(
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
                "query": "矿泉水",
                "user_requested_reading": True,
                "need_text_to_progress": False,
                "ocr_budget_ok": True,
            },
            "risk_summary_v1": {
                "risk_level": "low",
                "risk_interrupt_preempt": False,
                "timestamp_ms": 1700005000000,
            },
        },
    )

    # 1) 默认关闭：零侵入
    d0 = _run(enable="0", wb_only="1", ctx=ctx_ok)
    _assert("disabled_no_wb", "retail_find_item_v1" not in (d0.get("metadata") or {}))
    base_dispatch_type = d0.get("dispatch_type")
    base_notes = d0.get("notes")

    # 2) 开启 + whitebox-only：应挂白盒
    d1 = _run(enable="1", wb_only="1", ctx=ctx_ok)
    md1 = d1.get("metadata") or {}
    _assert("enabled_wb_attached", "retail_find_item_v1" in md1)
    wb = md1.get("retail_find_item_v1") or {}
    _assert("wb_dict", isinstance(wb, dict) and bool(wb))
    _assert("wb_final_spoken_empty", wb.get("final_spoken_output") == "")
    _assert("dispatch_type_unchanged", d1.get("dispatch_type") == base_dispatch_type)
    _assert("notes_unchanged", d1.get("notes") == base_notes)

    # 3) 风险压制：high
    ctx_high = VoiceRuntimeContext(
        current_session_id="s_retail",
        metadata={
            **(ctx_ok.metadata or {}),
            "risk_summary_v1": {
                "risk_level": "high",
                "risk_type": "vehicle",
                "risk_interrupt_preempt": False,
                "timestamp_ms": 1700005000001,
            },
        },
    )
    d2 = _run(enable="1", wb_only="1", ctx=ctx_high)
    wb2 = (d2.get("metadata") or {}).get("retail_find_item_v1") or {}
    _assert("suppressed_flag", wb2.get("output_suppressed_by_risk") is True)
    _assert("suppressed_spoken_empty", wb2.get("final_spoken_output") == "")

    # 4) 风险压制：risk_interrupt_preempt
    ctx_preempt = VoiceRuntimeContext(
        current_session_id="s_retail",
        metadata={
            **(ctx_ok.metadata or {}),
            "risk_summary_v1": {
                "risk_level": "low",
                "risk_type": "test",
                "risk_interrupt_preempt": True,
                "timestamp_ms": 1700005000002,
            },
        },
    )
    d3 = _run(enable="1", wb_only="1", ctx=ctx_preempt)
    wb3 = (d3.get("metadata") or {}).get("retail_find_item_v1") or {}
    _assert("preempt_suppressed", wb3.get("output_suppressed_by_risk") is True)
    _assert("preempt_spoken_empty", wb3.get("final_spoken_output") == "")

    # 5) 非零售环境：gating 不通过
    ctx_non = VoiceRuntimeContext(
        current_session_id="s_retail",
        metadata={
            "retail_env_summary_v1": {
                "scene_type_candidate": "unknown",
                "retail_context_confidence": 0.2,
                "shelf_visible": False,
                "gating_passed": False,
            },
            "find_item_intent_summary_v1": {
                "active": True,
                "query": "矿泉水",
                "user_requested_reading": True,
                "ocr_budget_ok": True,
            },
        },
    )
    d4 = _run(enable="1", wb_only="1", ctx=ctx_non)
    wb4 = (d4.get("metadata") or {}).get("retail_find_item_v1") or {}
    _assert("non_retail_wb_present", isinstance(wb4, dict) and bool(wb4))
    _assert("non_retail_gating_false", (wb4.get("gating_result") or {}).get("passed") is False)
    _assert("non_retail_spoken_empty", wb4.get("final_spoken_output") == "")

    # 6) 零售环境但无意图：不触发 OCR
    ctx_no_intent = VoiceRuntimeContext(
        current_session_id="s_retail",
        metadata={
            "retail_env_summary_v1": {
                "scene_type_candidate": "retail_shelf",
                "retail_context_confidence": 0.8,
                "shelf_visible": True,
                "gating_passed": True,
            },
            "find_item_intent_summary_v1": {
                "active": False,
            },
        },
    )
    d5 = _run(enable="1", wb_only="1", ctx=ctx_no_intent)
    wb5 = (d5.get("metadata") or {}).get("retail_find_item_v1") or {}
    _assert("no_intent_wb_present", isinstance(wb5, dict) and bool(wb5))
    _assert("no_intent_ocr_reason", wb5.get("ocr_trigger_reason") == "no_active_intent")
    _assert("no_intent_spoken_empty", wb5.get("final_spoken_output") == "")

    print("All retail_find_item_v1 deep integration checks passed.")


if __name__ == "__main__":
    main()

