#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
risk_interrupt_v1：真实风险摘要来源（context 优先）接入验证（Level 1 / whitebox-only）

覆盖：
1) 默认关闭 → 零侵入（metadata 无 risk_interrupt_v1）
2) 开启 + context 含 risk_summary_v1 → 成功写入白盒，且白盒 risk_level 来自 context
3) 开启 + context 无值但 event.metadata 有值 → 回退兼容成立
4) 开启 + context 与 event.metadata 同时存在 → context 优先
5) 输出内容不变（dispatch_type/notes 不应因接入改变）
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


def _dispatch(*, runtime_context: VoiceRuntimeContext | None, inject_event_meta: dict | None) -> dict:
    mgr = VoiceInputSessionManager()
    now = time.time()

    # 通过先构造 event，再调用 dispatcher，来测试 event.metadata 回退与优先级。
    ev = mgr.process_final_text(
        "帮我设一个三分钟的计时器",
        now=now,
        is_task_mode=True,
        session_id="s_ctx",
    )
    if inject_event_meta:
        # 仅用于测试回退口径；不代表推荐把风险塞进 VoiceInputEvent。
        ev.metadata = {**(ev.metadata or {}), **inject_event_meta}  # type: ignore[attr-defined]

    from capabilities.voice.runtime.voice_final_text_dispatcher import dispatch_voice_final_text  # noqa: E402

    res = dispatch_voice_final_text(
        ev,
        pending_confirmation_context=False,
        registry=mgr.registry,
        runtime_context=runtime_context,
    )
    return res.to_dict()


def main() -> None:
    # 1) 默认关闭
    os.environ["LUNA_ENABLE_RISK_INTERRUPT_V1"] = "0"
    os.environ["LUNA_RISK_INTERRUPT_WHITEBOX_ONLY"] = "1"
    d0 = _dispatch(runtime_context=None, inject_event_meta=None)
    _assert("disabled_no_wb", "risk_interrupt_v1" not in (d0.get("metadata") or {}))
    base_dispatch_type = d0.get("dispatch_type")
    base_notes = d0.get("notes")

    # 2) 开启 + context 有值
    os.environ["LUNA_ENABLE_RISK_INTERRUPT_V1"] = "1"
    os.environ["LUNA_RISK_INTERRUPT_WHITEBOX_ONLY"] = "1"
    ctx = VoiceRuntimeContext(
        current_session_id="s_ctx",
        metadata={
            "risk_summary_v1": {
                "risk_level": "medium",
                "risk_type": "crowd_close",
                "direction_hint": "front",
                "distance_band": "near",
                "confidence": 0.6,
                "timestamp_ms": 1700003000000,
                "source": "runtime_rule",
            }
        },
    )
    d1 = _dispatch(runtime_context=ctx, inject_event_meta=None)
    wb1 = (d1.get("metadata") or {}).get("risk_interrupt_v1") or {}
    _assert("ctx_wb_attached", isinstance(wb1, dict) and bool(wb1))
    _assert("ctx_level", (wb1.get("risk_event_summary") or {}).get("risk_level") == "medium")
    _assert("ctx_no_change_dispatch_type", d1.get("dispatch_type") == base_dispatch_type)
    _assert("ctx_no_change_notes", d1.get("notes") == base_notes)

    # 3) 开启 + context 无值但 event.metadata 有值 → 回退
    ctx_empty = VoiceRuntimeContext(current_session_id="s_ctx", metadata={})
    d2 = _dispatch(
        runtime_context=ctx_empty,
        inject_event_meta={
            "risk_level": "low",
            "risk_type": "test_fallback",
            "direction_hint": "unknown",
            "distance_band": "far",
            "risk_confidence": 0.2,
        },
    )
    wb2 = (d2.get("metadata") or {}).get("risk_interrupt_v1") or {}
    _assert("fallback_wb_attached", isinstance(wb2, dict) and bool(wb2))
    _assert("fallback_level", (wb2.get("risk_event_summary") or {}).get("risk_level") == "low")

    # 4) 开启 + 同时存在 → context 优先
    d3 = _dispatch(
        runtime_context=ctx,
        inject_event_meta={
            "risk_level": "critical",
            "risk_type": "should_not_win",
        },
    )
    wb3 = (d3.get("metadata") or {}).get("risk_interrupt_v1") or {}
    _assert("ctx_priority", (wb3.get("risk_event_summary") or {}).get("risk_level") == "medium", "context should win over event.metadata")

    print("All context-source integration checks passed.")


if __name__ == "__main__":
    main()

