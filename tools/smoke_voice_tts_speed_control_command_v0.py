# -*- coding: utf-8 -*-
"""
Smoke: in-dialogue TTS speed control commands (v0).

This tool simulates a voice shortcut command and applies runtime qwen speed controls
in-memory, without touching navigation.
"""

from __future__ import annotations

import argparse
import os
import time
from typing import Any, Dict


REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
import sys

if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)


from capabilities.voice.bridge.voice_input_router import route_voice_text  # type: ignore
from capabilities.voice.runtime.voice_shortcut_registry import VoiceShortcutRegistry  # type: ignore
from capabilities.voice.runtime.tts_runtime_controls_v0 import (  # type: ignore
    get_tts_speed,
    set_tts_speed,
    step_tts_speed,
    get_tts_speed_control_meta,
)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--text", required=True, help="Simulated user command text, e.g. 语速慢一点 / 语速0.75")
    args = ap.parse_args()

    reg = VoiceShortcutRegistry()
    rd = route_voice_text(
        args.text,
        now=time.time(),
        window_active=False,
        is_task_mode=False,
        registry=reg,
    )
    before = get_tts_speed()
    applied: Dict[str, Any] = {"matched": bool(rd.shortcut is not None), "shortcut_id": getattr(rd.shortcut, "shortcut_id", None)}

    if rd.shortcut is not None:
        sid = rd.shortcut.shortcut_id
        if sid == "dev_tts_speed_down":
            after = step_tts_speed(-1, source="smoke:dev_tts_speed_down")
            applied["action"] = "down"
            applied["after"] = after
        elif sid == "dev_tts_speed_up":
            after = step_tts_speed(1, source="smoke:dev_tts_speed_up")
            applied["action"] = "up"
            applied["after"] = after
        elif sid.startswith("dev_tts_speed_set_"):
            v = sid.replace("dev_tts_speed_set_", "").replace("_", ".")
            after = set_tts_speed(float(v), source=f"smoke:{sid}")
            applied["action"] = "set"
            applied["after"] = after
        else:
            applied["action"] = "not_speed_command"

    after = get_tts_speed()
    print(
        {
            "input_text": args.text,
            "tts_speed_before": before,
            "tts_speed_after": after,
            "speed_meta": get_tts_speed_control_meta(),
            "route_decision": rd.decision,
            "reason_code": rd.reason_code,
            "applied": applied,
        }
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

