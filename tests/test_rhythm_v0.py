# -*- coding: utf-8 -*-
"""ACTIVE × PAL 节律 v0 单元测试"""

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from intervention.rhythm_v0 import ActivePalRhythmV0, reset_rhythm_state


def test_idle_to_prepare():
    """IDLE → PREPARE：eligible + pal>=0.15 + vc>=0.6"""
    r = ActivePalRhythmV0()
    s = r.tick(now=100.0, pal=0.20, eligible=True, vc=0.7, task_state="ACTIVE")
    assert s == "PREPARE"


def test_idle_stays_idle_when_not_eligible():
    """IDLE 保持：eligible=False"""
    r = ActivePalRhythmV0()
    s = r.tick(now=100.0, pal=0.20, eligible=False, vc=0.7, task_state="ACTIVE")
    assert s == "IDLE"


def test_idle_stays_idle_when_pal_low():
    """IDLE 保持：pal < 0.15"""
    r = ActivePalRhythmV0()
    s = r.tick(now=100.0, pal=0.10, eligible=True, vc=0.7, task_state="ACTIVE")
    assert s == "IDLE"


def test_prepare_to_engaged():
    """PREPARE → ENGAGED：pal>=0.20 持续 2 秒"""
    r = ActivePalRhythmV0()
    r.tick(now=100.0, pal=0.20, eligible=True, vc=0.7, task_state="ACTIVE")
    assert r.state == "PREPARE"
    # 1 秒后仍 PREPARE
    s = r.tick(now=101.0, pal=0.25, eligible=True, vc=0.7, task_state="ACTIVE")
    assert s == "PREPARE"
    # 2 秒后进入 ENGAGED
    s = r.tick(now=102.0, pal=0.25, eligible=True, vc=0.7, task_state="ACTIVE")
    assert s == "ENGAGED"


def test_prepare_to_idle_when_pal_drops():
    """PREPARE → IDLE：pal < 0.10"""
    r = ActivePalRhythmV0()
    r.tick(now=100.0, pal=0.20, eligible=True, vc=0.7, task_state="ACTIVE")
    s = r.tick(now=101.0, pal=0.05, eligible=True, vc=0.7, task_state="ACTIVE")
    assert s == "IDLE"


def test_engaged_to_idle_min_duration():
    """ENGAGED → IDLE：需满 5 秒"""
    r = ActivePalRhythmV0()
    r.tick(now=100.0, pal=0.20, eligible=True, vc=0.7, task_state="ACTIVE")
    r.tick(now=102.0, pal=0.25, eligible=True, vc=0.7, task_state="ACTIVE")
    assert r.state == "ENGAGED"
    # 3 秒后 pal 降，但未满 5 秒，仍 ENGAGED
    s = r.tick(now=105.0, pal=0.05, eligible=True, vc=0.7, task_state="ACTIVE")
    assert s == "ENGAGED"
    # 6 秒后（从 102 进入 ENGAGED 算起）可退出
    s = r.tick(now=108.0, pal=0.05, eligible=True, vc=0.7, task_state="ACTIVE")
    assert s == "IDLE"


def test_cooldown():
    """ENGAGED→IDLE 后冷却 5 秒"""
    r = ActivePalRhythmV0()
    r.tick(now=100.0, pal=0.20, eligible=True, vc=0.7, task_state="ACTIVE")
    r.tick(now=102.0, pal=0.25, eligible=True, vc=0.7, task_state="ACTIVE")
    r.tick(now=108.0, pal=0.05, eligible=True, vc=0.7, task_state="ACTIVE")
    assert r.state == "IDLE"
    # 2 秒后仍冷却，不能进 PREPARE
    s = r.tick(now=110.0, pal=0.25, eligible=True, vc=0.7, task_state="ACTIVE")
    assert s == "IDLE"
    # 6 秒后（从 108 退出算起）可进 PREPARE
    s = r.tick(now=114.0, pal=0.25, eligible=True, vc=0.7, task_state="ACTIVE")
    assert s == "PREPARE"
