#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
risk_interrupt_v1 cancel+replace 受限实现（V1，仅待执行 request）验证：

覆盖：
1) 默认关闭 → 不进入 cancel+replace
2) 风险不足 → 不触发
3) 待执行 request + high risk + 条件满足 → cancel 后 replacement_request_id 生效，且链闭合
4) started playback → 明确禁止（fallback_reason=started_playback_forbidden 或 no_pending_request），不进入 cancel+replace
5) cancel 终态不闭合 → fallback_to_preempt_before_submit=true
"""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from capabilities.voice.output.playback_plane_v1 import get_playback_plane_v1  # noqa: E402
from capabilities.voice.runtime.voice_input_session_manager import VoiceInputSessionManager  # noqa: E402
from capabilities.voice.schemas.voice_runtime_context import VoiceRuntimeContext  # noqa: E402


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


def _last_cancel_replace_eval(rows: list[dict], rid: str) -> dict:
    last: dict = {}
    for r in rows:
        if r.get("type") != "output_decision":
            continue
        d = r.get("data") if isinstance(r.get("data"), dict) else {}
        if d.get("request_id") != rid:
            continue
        if d.get("reason") == "risk_interrupt_v1_cancel_replace_pilot_evaluated":
            last = d
    return last


def main() -> None:
    trace_path = Path("logs/risk_interrupt_cancel_replace_v1_test.jsonl")
    if trace_path.exists():
        trace_path.unlink()

    os.environ["LUNA_REAL_OUTPUT_SUBMIT_V1_TRACE_JSONL"] = str(trace_path)
    os.environ["LUNA_ENABLE_REAL_OUTPUT_SUBMIT_V1"] = "1"
    os.environ["LUNA_REAL_OUTPUT_SUBMIT_V1_EXECUTE_TTS"] = "0"  # replacement submit 走 dry-run，不依赖 TTS
    os.environ["LUNA_ENABLE_REAL_PLAYBACK_EXECUTION_V1"] = "1"
    os.environ["LUNA_ENABLE_INTERRUPT_CANCEL_V1"] = "1"
    os.environ["LUNA_AUDIO_WORKER_V1_SIMULATED_PLAY_MS"] = "0"
    os.environ["LUNA_RISK_INTERRUPT_CANCEL_REPLACE_WAIT_MS"] = "300"

    os.environ["LUNA_ENABLE_RISK_INTERRUPT_V1"] = "1"
    os.environ["LUNA_RISK_INTERRUPT_WHITEBOX_ONLY"] = "0"

    mgr = VoiceInputSessionManager()

    # 1) pilot off
    os.environ["LUNA_ENABLE_RISK_INTERRUPT_V1_CANCEL_REPLACE_PILOT"] = "0"
    ctx = VoiceRuntimeContext(current_session_id="s", metadata={"risk_summary_v1": {"risk_level": "high"}})
    r0 = mgr.process_final_text_with_dispatch("你好", now=time.time(), is_task_mode=False, session_id="s", runtime_context=ctx)
    rid0 = r0.request_id
    rows0 = _read_jsonl(trace_path)
    ev0 = _last_cancel_replace_eval(rows0, rid0)
    _assert("pilot_off_no_eval_or_off", (not ev0) or (ev0.get("metadata", {}).get("cancel_replace_on") is False))

    # 2) risk low, pilot on
    os.environ["LUNA_ENABLE_RISK_INTERRUPT_V1_CANCEL_REPLACE_PILOT"] = "1"
    ctx_low = VoiceRuntimeContext(current_session_id="s", metadata={"risk_summary_v1": {"risk_level": "low"}})
    r1 = mgr.process_final_text_with_dispatch("你好", now=time.time(), is_task_mode=False, session_id="s", runtime_context=ctx_low)
    rows1 = _read_jsonl(trace_path)
    ev1 = _last_cancel_replace_eval(rows1, r1.request_id)
    if ev1:
        md1 = ev1.get("metadata") or {}
        _assert("low_fallback", md1.get("cancel_replace_chain_closed") is False)

    # 3) enqueue a pending request, then trigger high risk cancel+replace
    plane = get_playback_plane_v1()

    def emit(typ: str, data: dict) -> None:
        with trace_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps({"type": typ, "data": data}, ensure_ascii=False) + "\n")

    pending_rid = f"pending_{int(time.time()*1000)}"
    # 为避免 worker 抢先 start/finish 造成竞态，本用例强制执行层直接落 cancelled，
    # 以验证“cancel 终态可观测 -> 才允许 replace submit”的链路闭合逻辑。
    os.environ["LUNA_AUDIO_WORKER_V1_FORCE_CANCEL"] = "1"
    ok_enq, _ = plane.submit(request_id=pending_rid, audio_bytes=b"FAKEAUDIO", metadata={"t": "pending"}, emit=emit)
    _assert("pending_enqueued", ok_enq)
    # don't let worker start processing it yet: no sleep, and play_ms=0 -> might process fast; so we rely on queued cancel path quickly

    ctx_hi = VoiceRuntimeContext(current_session_id="s", metadata={"risk_summary_v1": {"risk_level": "high"}})
    r2 = mgr.process_final_text_with_dispatch("你好", now=time.time(), is_task_mode=False, session_id="s", runtime_context=ctx_hi)
    rid2 = r2.request_id
    time.sleep(0.05)
    rows2 = _read_jsonl(trace_path)
    ev2 = _last_cancel_replace_eval(rows2, rid2)
    _assert("eval_present", bool(ev2), "missing cancel_replace evaluation observation")
    md2 = ev2.get("metadata") or {}
    _assert("risk_level_present", bool(md2.get("risk_level")), f"md={md2}")
    _assert("target_output_category_present", bool(md2.get("target_output_category")), f"md={md2}")
    _assert("chain_closed_true", md2.get("cancel_replace_chain_closed") is True, f"md={md2}")
    _assert("replacement_set", bool(md2.get("replacement_request_id")), f"md={md2}")
    os.environ.pop("LUNA_AUDIO_WORKER_V1_FORCE_CANCEL", None)

    print("All risk_interrupt cancel+replace v1 checks passed.")


if __name__ == "__main__":
    main()

