#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
request 真源（V1）验证：

1) submit 关闭时：无 request_runtime 事件落盘
2) submit 开启且成功时：至少能看到 request_created/request_submitted/request_terminal_observed（同一 request_id）
3) submit 开启但 force_reject/force_fail 时：能看到对应终态事件
4) 同一 request_id 可串起整条 request 层轨迹（最小要求：created + submitted + terminal）
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


def _run_once(mgr: VoiceInputSessionManager) -> dict:
    res = mgr.process_final_text_with_dispatch(
        "你好",  # 普通态无唤醒词，预期 reject -> prompt -> submit 候选
        now=time.time(),
        is_task_mode=False,
        session_id="s_req_rt",
    )
    return res.to_dict()


def _events_for_request(rows: list[dict], rid: str) -> list[str]:
    evs: list[str] = []
    for r in rows:
        if r.get("type") != "request_runtime":
            continue
        d = r.get("data") if isinstance(r.get("data"), dict) else {}
        if d.get("request_id") != rid:
            continue
        ev = d.get("event")
        if isinstance(ev, str):
            evs.append(ev)
    return evs


def main() -> None:
    trace_path = Path("logs/request_runtime_source_v1_test.jsonl")
    if trace_path.exists():
        trace_path.unlink()

    mgr = VoiceInputSessionManager()

    # 1) submit 关闭：无 request_runtime
    os.environ.pop("LUNA_ENABLE_REAL_OUTPUT_SUBMIT_V1", None)
    os.environ["LUNA_REAL_OUTPUT_SUBMIT_V1_TRACE_JSONL"] = str(trace_path)
    os.environ["LUNA_REAL_OUTPUT_SUBMIT_V1_EXECUTE_TTS"] = "0"
    os.environ.pop("LUNA_REAL_OUTPUT_SUBMIT_V1_FORCE_REJECT", None)
    os.environ.pop("LUNA_REAL_OUTPUT_SUBMIT_V1_FORCE_FAIL", None)

    d0 = _run_once(mgr)
    rid0 = str(d0.get("request_id") or "")
    rows0 = _read_jsonl(trace_path)
    _assert("disabled_no_request_runtime", len(_events_for_request(rows0, rid0)) == 0)

    # 2) submit 开启：成功（dry-run）
    os.environ["LUNA_ENABLE_REAL_OUTPUT_SUBMIT_V1"] = "1"
    d1 = _run_once(mgr)
    rid1 = str(d1.get("request_id") or "")
    rows1 = _read_jsonl(trace_path)
    evs1 = _events_for_request(rows1, rid1)
    _assert("enabled_has_created", "request_created" in evs1, f"evs={evs1}")
    _assert("enabled_has_submitted", "request_submitted" in evs1, f"evs={evs1}")
    _assert("enabled_has_terminal", "request_terminal_observed" in evs1, f"evs={evs1}")

    # 3) force_reject
    os.environ["LUNA_REAL_OUTPUT_SUBMIT_V1_FORCE_REJECT"] = "1"
    os.environ.pop("LUNA_REAL_OUTPUT_SUBMIT_V1_FORCE_FAIL", None)
    d2 = _run_once(mgr)
    rid2 = str(d2.get("request_id") or "")
    rows2 = _read_jsonl(trace_path)
    evs2 = _events_for_request(rows2, rid2)
    _assert("reject_has_submitted", "request_submitted" in evs2, f"evs={evs2}")
    _assert("reject_has_rejected", "request_submit_rejected" in evs2, f"evs={evs2}")

    # 4) force_fail
    os.environ.pop("LUNA_REAL_OUTPUT_SUBMIT_V1_FORCE_REJECT", None)
    os.environ["LUNA_REAL_OUTPUT_SUBMIT_V1_FORCE_FAIL"] = "1"
    d3 = _run_once(mgr)
    rid3 = str(d3.get("request_id") or "")
    rows3 = _read_jsonl(trace_path)
    evs3 = _events_for_request(rows3, rid3)
    _assert("fail_has_submitted", "request_submitted" in evs3, f"evs={evs3}")
    _assert("fail_has_failed", "request_submit_failed" in evs3, f"evs={evs3}")

    print("All request runtime source v1 checks passed.")


if __name__ == "__main__":
    main()

