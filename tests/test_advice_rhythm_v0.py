# -*- coding: utf-8 -*-
"""E) Advice 内容类型节律 v0 单元测试"""

import time

import pytest

from intervention.advice_rhythm_v0 import (
    ENV_AWARENESS,
    NAVIGATION_HINT,
    SAFETY_REMINDER,
    TASK_STATE,
    AdviceRhythmV0,
    advice_type_gate,
    get_advice_rhythm_v0,
    normalize_advice_type,
    reset_advice_rhythm_state,
)


def test_normalize_advice_type():
    assert normalize_advice_type("TASK_STATE", False) == TASK_STATE
    assert normalize_advice_type("NAVIGATION_HINT", False) == NAVIGATION_HINT
    assert normalize_advice_type("ENV_AWARENESS", False) == ENV_AWARENESS
    assert normalize_advice_type("REMINDER_FREQUENCY", False) == ENV_AWARENESS
    assert normalize_advice_type("unknown", True) == SAFETY_REMINDER
    assert normalize_advice_type(None, False) == TASK_STATE


def test_advice_type_gate_safety_always_allowed():
    allowed, reason = advice_type_gate(SAFETY_REMINDER, {"SAFETY_REMINDER": 100})
    assert allowed is True
    assert reason == "OK"


def test_advice_type_gate_quota():
    # NAVIGATION_HINT quota=2
    assert advice_type_gate(NAVIGATION_HINT, {}) == (True, "OK")
    assert advice_type_gate(NAVIGATION_HINT, {"NAVIGATION_HINT": 1}) == (True, "OK")
    assert advice_type_gate(NAVIGATION_HINT, {"NAVIGATION_HINT": 2}) == (False, "QUOTA_EXCEEDED")
    assert advice_type_gate(NAVIGATION_HINT, {"NAVIGATION_HINT": 3}) == (False, "QUOTA_EXCEEDED")

    # TASK_STATE quota=1
    assert advice_type_gate(TASK_STATE, {}) == (True, "OK")
    assert advice_type_gate(TASK_STATE, {"TASK_STATE": 1}) == (False, "QUOTA_EXCEEDED")


def test_advice_rhythm_v0_sliding_window():
    r = AdviceRhythmV0(window_sec=2.0)
    now = time.time()

    # 播报 2 次 NAVIGATION_HINT
    r.record_spoken(NAVIGATION_HINT, now)
    r.record_spoken(NAVIGATION_HINT, now + 0.5)
    stats = r.window_stats(now + 1)
    assert stats.get(NAVIGATION_HINT, 0) == 2

    # 第三次应被拒绝
    allowed, _, _, trace = r.check(NAVIGATION_HINT, False, now + 1)
    assert allowed is False
    assert trace["reason"] == "QUOTA_EXCEEDED"

    # 滑窗过期后应允许
    stats_after = r.window_stats(now + 5)
    assert stats_after.get(NAVIGATION_HINT, 0) == 0
    allowed2, _, _, _ = r.check(NAVIGATION_HINT, False, now + 5)
    assert allowed2 is True


def test_advice_rhythm_v0_safety_unlimited():
    r = AdviceRhythmV0(window_sec=2.0)
    now = time.time()
    for _ in range(10):
        r.record_spoken(SAFETY_REMINDER, now)
    allowed, _, _, trace = r.check(SAFETY_REMINDER, True, now)
    assert allowed is True
    assert trace["reason"] == "OK"


def test_get_advice_rhythm_v0_singleton():
    reset_advice_rhythm_state()
    a = get_advice_rhythm_v0()
    b = get_advice_rhythm_v0()
    assert a is b
