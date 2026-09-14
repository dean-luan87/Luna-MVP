#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
真实输出链最小 submit（V1）验证：

1) 默认关闭：旧路径不受影响（仍可分流，且不生成 trace）
2) 开启后：rejected_input 可生成 SpeechRequest 并真实调用 VoiceOutputPlane.submit()
3) request_id 可串起最小 trace 节点（submit_invoked/selection/cutover/playback）
4) 跨域旁路仍只在 metadata/whitebox，不进入 submit（本脚本不启用旁路晋升）
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


def main() -> None:
    trace_path = Path("logs/real_output_submit_v1_test.jsonl")
    if trace_path.exists():
        trace_path.unlink()

    # 1) 默认关闭：走旧路径，不写 trace
    os.environ.pop("LUNA_ENABLE_REAL_OUTPUT_SUBMIT_V1", None)
    os.environ["LUNA_REAL_OUTPUT_SUBMIT_V1_TRACE_JSONL"] = str(trace_path)
    os.environ["LUNA_REAL_OUTPUT_SUBMIT_V1_EXECUTE_TTS"] = "0"

    mgr = VoiceInputSessionManager()
    res0 = mgr.process_final_text_with_dispatch(
        "你好",  # 普通态无唤醒词，预期 reject
        now=time.time(),
        is_task_mode=False,
        session_id="s_submit",
    )
    d0 = res0.to_dict()
    _assert("default_reject", d0.get("dispatch_type") == "rejected_input")
    rows0 = _read_jsonl(trace_path)
    _assert("default_no_trace", len(rows0) == 0, "trace should be empty when submit disabled")

    # 2) 开启 submit：应写入最小闭环 trace
    os.environ["LUNA_ENABLE_REAL_OUTPUT_SUBMIT_V1"] = "1"
    res1 = mgr.process_final_text_with_dispatch(
        "你好",
        now=time.time(),
        is_task_mode=False,
        session_id="s_submit",
    )
    d1 = res1.to_dict()
    rid = str(d1.get("request_id") or "")
    _assert("rid_present", bool(rid))

    rows1 = _read_jsonl(trace_path)
    _assert("trace_written", len(rows1) >= 3, "expected jsonl envelopes written")

    # filter same request_id
    matched = [r for r in rows1 if isinstance(r.get("data"), dict) and r["data"].get("request_id") == rid]
    _assert("trace_has_rid", len(matched) >= 3, "expected records with same request_id")
    types = {r.get("type") for r in matched}
    # dry-run 下不伪造 playback 真状态，因此不要求 playback 事件存在
    for t in ("submit_invoked", "selection", "cutover"):
        _assert("trace_type_" + t, t in types, f"missing type={t}; got {sorted(list(types))}")

    print("All real output submit v1 checks passed.")


if __name__ == "__main__":
    main()

