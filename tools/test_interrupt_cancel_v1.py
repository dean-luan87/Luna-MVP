#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最小 cancel（V1）验证：

1) cancel 默认关闭：调用 cancel 不应产生 playback_cancelled
2) 开启 cancel：started 后 cancel 能产生 playback_cancelled，且不再产生 playback_finished
3) 同一 request_id 可对账（started + cancelled）
4) finished 与 cancelled 不混淆
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
    trace_path = Path("logs/interrupt_cancel_v1_test.jsonl")
    if trace_path.exists():
        trace_path.unlink()

    def emit(typ: str, data: dict) -> None:
        _append(trace_path, typ, data)

    plane = get_playback_plane_v1()

    # 1) cancel disabled
    os.environ.pop("LUNA_ENABLE_INTERRUPT_CANCEL_V1", None)
    os.environ["LUNA_AUDIO_WORKER_V1_SIMULATED_PLAY_MS"] = "80"
    rid0 = f"rid_cancel_{int(time.time()*1000)}"
    ok0, _ = plane.submit(request_id=rid0, audio_bytes=b"FAKEAUDIO", metadata={"t": "0"}, emit=emit)
    _assert("submit_ok0", ok0)
    time.sleep(0.02)
    okc0, reason0 = plane.cancel(request_id=rid0, reason="test_cancel")
    _assert("cancel_disabled_false", okc0 is False and reason0 == "cancel_disabled")
    time.sleep(0.10)
    ev0 = _events(_read(trace_path), rid0)
    _assert("disabled_no_cancelled", "playback_cancelled" not in ev0, f"evs={ev0}")

    # 2) cancel enabled: started then cancelled, no finished
    os.environ["LUNA_ENABLE_INTERRUPT_CANCEL_V1"] = "1"
    rid1 = f"rid_cancel_{int(time.time()*1000)+1}"
    ok1, _ = plane.submit(request_id=rid1, audio_bytes=b"FAKEAUDIO", metadata={"t": "1"}, emit=emit)
    _assert("submit_ok1", ok1)
    time.sleep(0.02)  # allow started to be emitted
    okc1, reason1 = plane.cancel(request_id=rid1, reason="test_cancel_after_started")
    _assert("cancel_ok", okc1, reason1)
    time.sleep(0.12)
    ev1 = _events(_read(trace_path), rid1)
    _assert("has_started", "playback_started" in ev1, f"evs={ev1}")
    _assert("has_cancelled", "playback_cancelled" in ev1, f"evs={ev1}")
    _assert("no_finished_after_cancel", "playback_finished" not in ev1, f"evs={ev1}")

    print("All interrupt/cancel v1 checks passed.")


if __name__ == "__main__":
    main()

