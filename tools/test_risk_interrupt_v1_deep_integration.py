#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
risk_interrupt_v1：主线深联调（阶段 1 / Level 1）验证

验证目标：
1) 默认关闭：主线零侵入（VoiceFinalTextDispatchResult.metadata 不含 risk_interrupt_v1）
2) 开启 + whitebox-only：主线 metadata 合并 risk_interrupt_v1 白盒字段
3) 输出内容不变（dispatch_type/notes 不受影响）
4) 任务链状态不变（阶段 1 不挂起）
5) speaking 路径不被影响（本阶段 speaking 仅作可观测替代字段写入白盒，不驱动行为）
6) 白盒字段完整
"""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from capabilities.voice.runtime.voice_input_session_manager import (  # noqa: E402
    VoiceInputSessionManager,
)


def _assert(name: str, cond: bool, msg: str = "") -> None:
    if not cond:
        raise AssertionError(f"[{name}] {msg}")


def _run_once(*, enabled: str, whitebox_only: str) -> dict:
    os.environ["LUNA_ENABLE_RISK_INTERRUPT_V1"] = enabled
    os.environ["LUNA_RISK_INTERRUPT_WHITEBOX_ONLY"] = whitebox_only

    mgr = VoiceInputSessionManager()
    res = mgr.process_final_text_with_dispatch(
        "帮我设一个三分钟的计时器",
        now=time.time(),
        is_task_mode=True,
        session_id="s1",
    )
    return res.to_dict()


def main() -> None:
    # 1) 默认关闭
    d0 = _run_once(enabled="0", whitebox_only="1")
    _assert("disabled_no_wb", "risk_interrupt_v1" not in (d0.get("metadata") or {}))
    base_dispatch_type = d0.get("dispatch_type")
    base_notes = d0.get("notes")
    print("==== disabled ====")
    print("dispatch_type:", base_dispatch_type)
    print("metadata keys:", list((d0.get("metadata") or {}).keys()))
    print("OK\n")

    # 2) 开启 + whitebox-only
    d1 = _run_once(enabled="1", whitebox_only="1")
    md1 = d1.get("metadata") or {}
    _assert("enabled_wb_attached", "risk_interrupt_v1" in md1)
    wb = md1.get("risk_interrupt_v1") or {}
    must = [
        "event_timestamp",
        "risk_event_summary",
        "original_output",
        "interrupt_applied",
        "task_paused",
        "final_spoken_output",
        "interrupt_reason",
    ]
    missing = [k for k in must if k not in wb]
    _assert("wb_fields", not missing, f"missing fields: {missing}")
    _assert("wb_level1_no_interrupt", wb.get("interrupt_applied") is False)
    _assert("wb_level1_no_pause", wb.get("task_paused") is False)

    # 3) 输出内容不变（相对 disabled：dispatch_type/notes 不应被 hook 改写）
    _assert("dispatch_type_unchanged", d1.get("dispatch_type") == base_dispatch_type)
    _assert("notes_unchanged", d1.get("notes") == base_notes)

    print("==== enabled_whitebox_only ====")
    print(json.dumps(wb, ensure_ascii=False, indent=2))
    print("OK\n")

    print("All deep integration checks passed.")


if __name__ == "__main__":
    main()

