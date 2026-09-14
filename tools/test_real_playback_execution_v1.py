#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最小真实执行层（Playback Plane + Audio Worker）V1 验证：

覆盖：
1) 默认关闭（LUNA_ENABLE_REAL_PLAYBACK_EXECUTION_V1=0）：不要求走真实执行层（本脚本验证 plane/worker 独立可用）
2) 开启后：submit(audio_bytes) 能看到 started -> finished（同一 request_id）
3) 强制失败：能看到 playback_failed
4) 强制取消：能看到 playback_cancelled

说明：
- 本测试直接调用 playback_plane_v1，避免依赖 TTS provider 可执行文件。
- 事件落盘使用与主线一致的 JSONL envelope：type=playback_runtime, data.request_id。
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


def _assert(name: str, cond: bool, msg: str = "") -> None:
    if not cond:
        raise AssertionError(f"[{name}] {msg}")


def _append(path: Path, typ: str, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"type": typ, "data": data}, ensure_ascii=False) + "\n")


def _read(path: Path) -> list[dict]:
    if not path.exists():
        return []
    out: list[dict] = []
    for ln in path.read_text(encoding="utf-8").splitlines():
        ln = ln.strip()
        if ln:
            out.append(json.loads(ln))
    return out


def _events(rows: list[dict], rid: str) -> list[str]:
    evs: list[str] = []
    for r in rows:
        if r.get("type") != "playback_runtime":
            continue
        d = r.get("data") if isinstance(r.get("data"), dict) else {}
        if d.get("request_id") != rid:
            continue
        ev = d.get("event")
        if isinstance(ev, str):
            evs.append(ev)
    return evs


def main() -> None:
    trace_path = Path("logs/real_playback_execution_v1_test.jsonl")
    if trace_path.exists():
        trace_path.unlink()

    def emit(typ: str, data: dict) -> None:
        _append(trace_path, typ, data)

    plane = get_playback_plane_v1()

    # 1) normal success: started -> finished
    os.environ.pop("LUNA_AUDIO_WORKER_V1_FORCE_FAIL", None)
    os.environ.pop("LUNA_AUDIO_WORKER_V1_FORCE_CANCEL", None)
    rid1 = f"rid_exec_{int(time.time()*1000)}"
    ok, reason = plane.submit(request_id=rid1, audio_bytes=b"FAKEAUDIO", metadata={"t": "ok"}, emit=emit)
    _assert("enqueue_ok", ok, reason)
    time.sleep(0.05)
    rows1 = _read(trace_path)
    ev1 = _events(rows1, rid1)
    _assert("has_started", "playback_started" in ev1, f"evs={ev1}")
    _assert("has_finished", "playback_finished" in ev1, f"evs={ev1}")

    # 2) force fail
    os.environ["LUNA_AUDIO_WORKER_V1_FORCE_FAIL"] = "1"
    rid2 = f"rid_exec_{int(time.time()*1000)+1}"
    ok2, _ = plane.submit(request_id=rid2, audio_bytes=b"FAKEAUDIO", metadata={"t": "fail"}, emit=emit)
    _assert("enqueue_ok_failcase", ok2)
    time.sleep(0.05)
    rows2 = _read(trace_path)
    ev2 = _events(rows2, rid2)
    _assert("fail_has_started", "playback_started" in ev2, f"evs={ev2}")
    _assert("fail_has_failed", "playback_failed" in ev2, f"evs={ev2}")
    os.environ.pop("LUNA_AUDIO_WORKER_V1_FORCE_FAIL", None)

    # 3) force cancel
    os.environ["LUNA_AUDIO_WORKER_V1_FORCE_CANCEL"] = "1"
    rid3 = f"rid_exec_{int(time.time()*1000)+2}"
    ok3, _ = plane.submit(request_id=rid3, audio_bytes=b"FAKEAUDIO", metadata={"t": "cancel"}, emit=emit)
    _assert("enqueue_ok_cancelcase", ok3)
    time.sleep(0.05)
    rows3 = _read(trace_path)
    ev3 = _events(rows3, rid3)
    _assert("cancel_has_cancelled", "playback_cancelled" in ev3, f"evs={ev3}")
    os.environ.pop("LUNA_AUDIO_WORKER_V1_FORCE_CANCEL", None)

    print("All real playback execution v1 checks passed.")


if __name__ == "__main__":
    main()

