#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
risk_interrupt_v1 试点回退 telemetry（pilot_state_transition）最小验证：

覆盖：
1) 记录一次 level2b_to_level2a（通过制造 cancel+replace 链不闭合）
2) 记录一次 level2a_to_level1（通过 operator toggle 关闭 level2a）
3) 记录一次 any_to_level0（通过 operator toggle 关闭 risk 或 submit）
4) analyzer 可直接统计出对应计数
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
from tools.analyze_risk_interrupt_v1_pilot import analyze  # noqa: E402


def _assert(name: str, cond: bool, msg: str = "") -> None:
    if not cond:
        raise AssertionError(f"[{name}] {msg}")


def _read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    out: list[dict] = []
    for ln in path.read_text(encoding="utf-8").splitlines():
        ln = ln.strip()
        if ln:
            out.append(json.loads(ln))
    return out


def main() -> None:
    trace_path = Path("logs/risk_interrupt_state_transition_v1_test.jsonl")
    if trace_path.exists():
        trace_path.unlink()

    os.environ["LUNA_REAL_OUTPUT_SUBMIT_V1_TRACE_JSONL"] = str(trace_path)
    os.environ["LUNA_ENABLE_REAL_OUTPUT_SUBMIT_V1"] = "1"
    os.environ["LUNA_REAL_OUTPUT_SUBMIT_V1_EXECUTE_TTS"] = "0"

    os.environ["LUNA_ENABLE_RISK_INTERRUPT_V1"] = "1"
    os.environ["LUNA_RISK_INTERRUPT_WHITEBOX_ONLY"] = "0"

    # enable both pilots
    os.environ["LUNA_ENABLE_RISK_INTERRUPT_V1_LEVEL2_PILOT"] = "1"
    os.environ["LUNA_ENABLE_RISK_INTERRUPT_V1_CANCEL_REPLACE_PILOT"] = "1"

    mgr = VoiceInputSessionManager()

    # 1) force cancel+replace chain broken (no playback_cancelled observed)
    os.environ["LUNA_ENABLE_REAL_PLAYBACK_EXECUTION_V1"] = "1"
    os.environ["LUNA_ENABLE_INTERRUPT_CANCEL_V1"] = "1"
    os.environ["LUNA_RISK_INTERRUPT_CANCEL_REPLACE_WAIT_MS"] = "20"
    # ensure we do NOT produce playback_cancelled automatically
    os.environ.pop("LUNA_AUDIO_WORKER_V1_FORCE_CANCEL", None)

    ctx_hi = VoiceRuntimeContext(current_session_id="s", metadata={"risk_summary_v1": {"risk_level": "high"}})
    _ = mgr.process_final_text_with_dispatch("你好", now=time.time(), is_task_mode=False, session_id="s", runtime_context=ctx_hi)
    time.sleep(0.03)

    rows = _read_jsonl(trace_path)
    trans = [r for r in rows if r.get("type") == "pilot_state_transition"]
    _assert("has_transition_event", len(trans) >= 1, "no pilot_state_transition emitted")
    _assert(
        "has_level2b_to_level2a",
        any((r.get("data") or {}).get("transition") == "level2b_to_level2a" for r in trans),
        "missing level2b_to_level2a",
    )

    # 2) operator toggle: level2a -> level1
    os.environ["LUNA_ENABLE_RISK_INTERRUPT_V1_LEVEL2_PILOT"] = "0"
    _ = mgr.process_final_text_with_dispatch("你好", now=time.time(), is_task_mode=False, session_id="s", runtime_context=ctx_hi)
    time.sleep(0.01)

    # 3) operator toggle: any -> level0 (disable risk)
    os.environ["LUNA_ENABLE_RISK_INTERRUPT_V1"] = "0"
    _ = mgr.process_final_text_with_dispatch("你好", now=time.time(), is_task_mode=False, session_id="s", runtime_context=ctx_hi)
    time.sleep(0.01)

    # 4) analyzer counts
    res = analyze([trace_path])
    m = res.get("metrics_by_request_id") or {}
    _assert("count_level1", int(m.get("fallback_to_level1_count") or 0) >= 1, f"m={m}")
    _assert("count_level0", int(m.get("fallback_to_level0_count") or 0) >= 1, f"m={m}")

    print("All pilot_state_transition v1 checks passed.")


if __name__ == "__main__":
    main()

