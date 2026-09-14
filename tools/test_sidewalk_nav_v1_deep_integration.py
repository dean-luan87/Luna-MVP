#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sidewalk_nav_v1：主线深联调（阶段 1 / whitebox-only）验证

覆盖：
1) 默认关闭 → 主链零侵入（metadata 无 sidewalk_nav_v1）
2) 开启 + whitebox-only + context 有环境摘要 → 主线 metadata 出现 sidewalk_nav_v1 白盒
3) 同时存在风险压制（high/critical 或 risk_interrupt_preempt）→ final_spoken_output 为空且 output_suppressed_by_risk=true
4) 输出内容不变（dispatch_type/notes 不应因接入改变）
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
    os.environ["LUNA_ENABLE_SIDEWALK_NAV_V1"] = enable
    os.environ["LUNA_SIDEWALK_NAV_WHITEBOX_ONLY"] = wb_only

    mgr = VoiceInputSessionManager()
    res = mgr.process_final_text_with_dispatch(
        "帮我设一个三分钟的计时器",
        now=time.time(),
        is_task_mode=True,
        session_id="s_sw",
        runtime_context=ctx,
    )
    return res.to_dict()


def main() -> None:
    base_ctx = VoiceRuntimeContext(
        current_session_id="s_sw",
        metadata={
            "sidewalk_env_summary_v1": {
                "scene_candidate": "outdoor_walkway",
                "path_confidence": 0.8,
                "is_outdoor": True,
            }
        },
    )

    # 1) 默认关闭：零侵入
    d0 = _run(enable="0", wb_only="1", ctx=base_ctx)
    _assert("disabled_no_wb", "sidewalk_nav_v1" not in (d0.get("metadata") or {}))
    base_dispatch_type = d0.get("dispatch_type")
    base_notes = d0.get("notes")

    # 2) 开启 + whitebox-only：应挂白盒
    d1 = _run(enable="1", wb_only="1", ctx=base_ctx)
    md1 = d1.get("metadata") or {}
    _assert("enabled_wb_attached", "sidewalk_nav_v1" in md1)
    wb = md1.get("sidewalk_nav_v1") or {}
    _assert("wb_is_dict", isinstance(wb, dict) and bool(wb))
    _assert("wb_final_spoken_empty", wb.get("final_spoken_output") == "")
    _assert("dispatch_type_unchanged", d1.get("dispatch_type") == base_dispatch_type)
    _assert("notes_unchanged", d1.get("notes") == base_notes)

    # 3) 风险压制：high risk
    ctx_risk = VoiceRuntimeContext(
        current_session_id="s_sw",
        metadata={
            **(base_ctx.metadata or {}),
            "risk_summary_v1": {
                "risk_level": "high",
                "risk_type": "vehicle",
                "risk_interrupt_preempt": False,
                "timestamp_ms": 1700004000000,
            },
        },
    )
    d2 = _run(enable="1", wb_only="1", ctx=ctx_risk)
    wb2 = (d2.get("metadata") or {}).get("sidewalk_nav_v1") or {}
    _assert("suppressed_flag", wb2.get("output_suppressed_by_risk") is True)
    _assert("suppressed_spoken_empty", wb2.get("final_spoken_output") == "")

    # 4) 风险压制：risk_interrupt_preempt
    ctx_preempt = VoiceRuntimeContext(
        current_session_id="s_sw",
        metadata={
            **(base_ctx.metadata or {}),
            "risk_summary_v1": {
                "risk_level": "low",
                "risk_type": "test",
                "risk_interrupt_preempt": True,
                "timestamp_ms": 1700004000001,
            },
        },
    )
    d3 = _run(enable="1", wb_only="1", ctx=ctx_preempt)
    wb3 = (d3.get("metadata") or {}).get("sidewalk_nav_v1") or {}
    _assert("preempt_suppressed", wb3.get("output_suppressed_by_risk") is True)
    _assert("preempt_spoken_empty", wb3.get("final_spoken_output") == "")

    print("All sidewalk_nav_v1 deep integration checks passed.")


if __name__ == "__main__":
    main()

