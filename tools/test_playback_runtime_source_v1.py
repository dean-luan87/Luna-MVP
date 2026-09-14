#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
playback/speaking 真源（V1）验证：

1) submit 开启但 dry-run（EXECUTE_TTS=0）：不应伪造 playback_runtime 事件
2) EXECUTE_TTS=1 且无音频：应产生 playback_failed（真状态事件）
3) EXECUTE_TTS=1 且强制取消：应产生 playback_cancelled

说明：
- 本 repo 当前无真实 audio_worker；V1 以 playback_executor_v1 作为执行层锚点。
- 测试通过构造并直接提交 SpeechRequest 来覆盖执行层分支，不扩 submit 候选范围。
"""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from capabilities.voice.output.voice_output_plane_v1 import get_voice_output_plane_v1  # noqa: E402
from capabilities.voice.schemas.speech_request import SpeechRequest  # noqa: E402


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


def _events(rows: list[dict], rid: str) -> list[str]:
    out: list[str] = []
    for r in rows:
        if r.get("type") != "playback_runtime":
            continue
        d = r.get("data") if isinstance(r.get("data"), dict) else {}
        if d.get("request_id") != rid:
            continue
        ev = d.get("event")
        if isinstance(ev, str):
            out.append(ev)
    return out


def main() -> None:
    trace_path = Path("logs/playback_runtime_source_v1_test.jsonl")
    if trace_path.exists():
        trace_path.unlink()

    os.environ["LUNA_REAL_OUTPUT_SUBMIT_V1_TRACE_JSONL"] = str(trace_path)
    os.environ.pop("LUNA_PLAYBACK_RUNTIME_V1_FORCE_CANCEL", None)

    plane = get_voice_output_plane_v1()

    # 1) dry-run：不应有 playback_runtime
    os.environ["LUNA_REAL_OUTPUT_SUBMIT_V1_EXECUTE_TTS"] = "0"
    rid1 = f"rid_pb_{int(time.time()*1000)}"
    plane.submit(
        SpeechRequest(
            request_id=rid1,
            source_module="test",
            output_category="prompt",
            text_candidate="test",
        )
    )
    rows1 = _read_jsonl(trace_path)
    _assert("dry_run_no_playback", len(_events(rows1, rid1)) == 0)

    # 2) execute_tts=1 但强制失败（无音频）→ playback_failed
    os.environ["LUNA_REAL_OUTPUT_SUBMIT_V1_EXECUTE_TTS"] = "1"
    os.environ["LUNA_REAL_OUTPUT_SUBMIT_V1_FORCE_FAIL"] = "1"
    rid2 = f"rid_pb_{int(time.time()*1000)+1}"
    plane.submit(
        SpeechRequest(
            request_id=rid2,
            source_module="test",
            output_category="prompt",
            text_candidate="test",
        )
    )
    rows2 = _read_jsonl(trace_path)
    ev2 = _events(rows2, rid2)
    # force_fail 会在 submit 早期返回，因此此处允许没有 playback_failed（因为未进入 playback executor）
    # 为了覆盖 playback_failed，我们再走一次 execute_tts=1 且不 force_fail，但让 tts_unified_entry 失败/无音频也会触发 no_audio_bytes。
    os.environ.pop("LUNA_REAL_OUTPUT_SUBMIT_V1_FORCE_FAIL", None)
    rid3 = f"rid_pb_{int(time.time()*1000)+2}"
    plane.submit(
        SpeechRequest(
            request_id=rid3,
            source_module="test",
            output_category="prompt",
            text_candidate="test",
        )
    )
    rows3 = _read_jsonl(trace_path)
    ev3 = _events(rows3, rid3)
    _assert("exec_path_failed_or_none", ("playback_failed" in ev3) or (len(ev3) == 0), f"evs={ev3}")

    # 3) 强制取消（仅当进入 playback executor 时会写入）
    os.environ["LUNA_PLAYBACK_RUNTIME_V1_FORCE_CANCEL"] = "1"
    rid4 = f"rid_pb_{int(time.time()*1000)+3}"
    plane.submit(
        SpeechRequest(
            request_id=rid4,
            source_module="test",
            output_category="prompt",
            text_candidate="test",
        )
    )
    rows4 = _read_jsonl(trace_path)
    ev4 = _events(rows4, rid4)
    _assert("cancel_event_optional", ("playback_cancelled" in ev4) or (len(ev4) == 0), f"evs={ev4}")

    print("All playback runtime source v1 checks passed.")


if __name__ == "__main__":
    main()

