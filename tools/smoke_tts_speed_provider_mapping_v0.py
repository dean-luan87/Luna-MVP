#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Smoke (dry-run): Runtime TTS speed tier -> provider-specific mapping evidence (v0).

No network calls. Does not synthesize real audio.
Outputs mapping values for:
- qwen.speed
- piper.length_scale
- macOS say rate
"""

from __future__ import annotations

import argparse
import os
import sys


REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)


from capabilities.voice.runtime.tts_runtime_controls_v0 import (  # type: ignore
    get_tts_speed,
    get_tts_speed_control_meta,
    set_tts_speed,
)
from capabilities.voice.runtime.tts_unified_entry import (  # type: ignore
    _speed_to_macos_say_rate,
    _speed_to_piper_length_scale,
)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--speed", type=float, default=None, help="Optional: set runtime speed tier first (0.25~1.0 step 0.25)")
    args = ap.parse_args()

    if args.speed is not None:
        set_tts_speed(float(args.speed), source="smoke:manual_speed")

    speed = float(get_tts_speed())
    meta = get_tts_speed_control_meta()
    out = {
        **meta,
        "provider_mapping": {
            "qwen.speed": speed,
            "piper.length_scale": _speed_to_piper_length_scale(speed),
            "macos_say.rate": _speed_to_macos_say_rate(speed),
        },
        "inheritance_expectation": {
            "fallback_to_piper_should_inherit_speed": True,
            "fallback_to_macos_say_should_inherit_speed": True,
        },
    }
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

