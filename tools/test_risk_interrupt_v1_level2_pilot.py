#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
risk_interrupt_v1 Level 2 受限试点（V1）验证（不做中断/恢复，仅验证“提交前替换”抢占策略）：

覆盖：
1) 默认关闭 pilot → 不发生 output_decision:preempt 记录
2) pilot 开启但 risk_level=low → 不抢占
3) pilot 开启 + risk_level=high → 对 prompt 输出进行提交前替换，并写入 output_decision 观测
4) 关闭/回退开关后秒退回 Level 1（不再抢占）
"""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from capabilities.voice.runtime.voice_input_session_manager import VoiceInputSessionManager  # noqa: E402
from capabilities.voice.schemas.voice_runtime_context import VoiceRuntimeContext  # noqa: E402


def _assert(name: str, cond: bool, msg: str = "") -> None:
    if not cond:
        raise AssertionError(f"[{name}] {msg}")


def _read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows: list[dict] = []
    for ln in path.read_text(encoding="utf-8").splitlines():
        ln = ln.strip()
        if not ln:
            continue
        rows.append(json.loads(ln))
    return rows


def _has_preempt_decision(rows: list[dict], rid: str) -> bool:
    for r in rows:
        if r.get("type") != "output_decision":
            continue
        d = r.get("data") if isinstance(r.get("data"), dict) else {}
        if d.get("request_id") != rid:
            continue
        if d.get("reason") == "risk_interrupt_v1_level2_pilot_preempt_before_submit":
            return True
    return False


def _dispatch(*, risk_level: str, trace_path: Path) -> dict:
    ctx = VoiceRuntimeContext(
        current_session_id="s_pilot",
        metadata={"risk_summary_v1": {"risk_level": risk_level, "risk_interrupt_preempt": False, "timestamp_ms": 1700006000000}},
    )
    mgr = VoiceInputSessionManager()
    res = mgr.process_final_text_with_dispatch(
        "你好",  # 普通态无唤醒词，预期 rejected_input（prompt）
        now=time.time(),
        is_task_mode=False,
        session_id="s_pilot",
        runtime_context=ctx,
    )
    return res.to_dict()


def main() -> None:
    trace_path = Path("logs/risk_interrupt_level2_pilot_v1_test.jsonl")
    if trace_path.exists():
        trace_path.unlink()

    os.environ["LUNA_REAL_OUTPUT_SUBMIT_V1_TRACE_JSONL"] = str(trace_path)
    os.environ["LUNA_ENABLE_REAL_OUTPUT_SUBMIT_V1"] = "1"
    os.environ["LUNA_REAL_OUTPUT_SUBMIT_V1_EXECUTE_TTS"] = "0"

    # risk enabled, whitebox_only must be 0 to allow pilot
    os.environ["LUNA_ENABLE_RISK_INTERRUPT_V1"] = "1"
    os.environ["LUNA_RISK_INTERRUPT_WHITEBOX_ONLY"] = "0"

    # 1) pilot off
    os.environ["LUNA_ENABLE_RISK_INTERRUPT_V1_LEVEL2_PILOT"] = "0"
    d0 = _dispatch(risk_level="high", trace_path=trace_path)
    rid0 = str(d0.get("request_id") or "")
    rows0 = _read_jsonl(trace_path)
    _assert("pilot_off_no_preempt", not _has_preempt_decision(rows0, rid0))

    # 2) pilot on, low risk
    os.environ["LUNA_ENABLE_RISK_INTERRUPT_V1_LEVEL2_PILOT"] = "1"
    d1 = _dispatch(risk_level="low", trace_path=trace_path)
    rid1 = str(d1.get("request_id") or "")
    rows1 = _read_jsonl(trace_path)
    _assert("low_risk_no_preempt", not _has_preempt_decision(rows1, rid1))

    # 3) pilot on, high risk
    d2 = _dispatch(risk_level="high", trace_path=trace_path)
    rid2 = str(d2.get("request_id") or "")
    rows2 = _read_jsonl(trace_path)
    _assert("high_risk_preempt", _has_preempt_decision(rows2, rid2))

    # 4) rollback pilot off again
    os.environ["LUNA_ENABLE_RISK_INTERRUPT_V1_LEVEL2_PILOT"] = "0"
    d3 = _dispatch(risk_level="critical", trace_path=trace_path)
    rid3 = str(d3.get("request_id") or "")
    rows3 = _read_jsonl(trace_path)
    _assert("rollback_no_preempt", not _has_preempt_decision(rows3, rid3))

    print("All risk_interrupt_v1 level2 pilot checks passed.")


if __name__ == "__main__":
    main()

