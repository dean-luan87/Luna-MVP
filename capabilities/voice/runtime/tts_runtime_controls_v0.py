# -*- coding: utf-8 -*-
"""
Runtime TTS controls (v0).

Goal: allow in-dialogue commands to adjust runtime TTS parameters safely.

Hard boundaries:
- runtime-only (in-memory); does not persist to disk by default
- does not generate speech text
- does not change navigation semantics
"""

from __future__ import annotations

import threading
from typing import Optional


_lock = threading.Lock()
_tts_speed: float = 0.75  # default (requested), global TTS speed tier
_tts_speed_last_source: str = "default"
_tts_speed_last_set_at_s: float = 0.0


def clamp_speed(x: float) -> float:
    v = float(x)
    if v < 0.25:
        return 0.25
    if v > 1.0:
        return 1.0
    # snap to 0.25 step
    step = 0.25
    snapped = round(v / step) * step
    # avoid 0.0 due to rounding
    if snapped < 0.25:
        snapped = 0.25
    if snapped > 1.0:
        snapped = 1.0
    return float(snapped)


def get_qwen_speed() -> float:
    # Back-compat alias. Qwen speed is driven by global TTS speed tier.
    return get_tts_speed()


def set_qwen_speed(x: float) -> float:
    # Back-compat alias. Sets global TTS speed tier.
    return set_tts_speed(x, source="legacy_alias:set_qwen_speed")


def step_qwen_speed(delta_steps: int) -> float:
    # Back-compat alias. Steps global TTS speed tier.
    return step_tts_speed(delta_steps, source="legacy_alias:step_qwen_speed")


def get_tts_speed() -> float:
    with _lock:
        return float(_tts_speed)


def get_tts_speed_control_meta() -> dict:
    """
    Whitebox metadata for speed control.
    Runtime-only; does not persist.
    """
    with _lock:
        return {
            "tts_runtime_speed": float(_tts_speed),
            "speed_control_source": str(_tts_speed_last_source or "unknown"),
            "speed_control_last_set_at_s": float(_tts_speed_last_set_at_s or 0.0),
        }


def set_tts_speed(x: float, *, source: Optional[str] = None) -> float:
    v = clamp_speed(float(x))
    with _lock:
        global _tts_speed
        global _tts_speed_last_source
        global _tts_speed_last_set_at_s
        _tts_speed = v
        _tts_speed_last_source = str(source) if source else "unknown"
        try:
            import time

            _tts_speed_last_set_at_s = float(time.time())
        except Exception:
            _tts_speed_last_set_at_s = 0.0
    return v


def step_tts_speed(delta_steps: int, *, source: Optional[str] = None) -> float:
    with _lock:
        cur = float(_tts_speed)
    return set_tts_speed(cur + (0.25 * int(delta_steps)), source=source)

