# -*- coding: utf-8 -*-
"""ENGAGED 介入强度 v0 单元测试（含 A1 L2 时间窗）"""

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from intervention.engagement_v0 import (
    EngagementV0,
    L2_HOLD_SECONDS,
    PAL_L2_THRESHOLD,
    COMPLEXITY_L2_THRESHOLD,
    VC_L2_THRESHOLD,
)


def _tick(e, rhythm, pal, complexity, vc, control, now=0.0):
    return e.tick(
        now=now,
        rhythm_state=rhythm,
        pal=pal,
        complexity=complexity,
        vc=vc,
        control_mode=control,
    )


def test_non_engaged_returns_l0():
    """非 ENGAGED 时返回 L0"""
    e = EngagementV0()
    out = _tick(e, "IDLE", pal=0.5, complexity=0.8, vc=0.9, control="ASSISTED")
    assert out.level == "L0"
    out = _tick(e, "PREPARE", pal=0.5, complexity=0.8, vc=0.9, control="ASSISTED")
    assert out.level == "L0"


def test_l1_conditions():
    """L1：pal<0.35 且 complexity<0.60（默认）"""
    e = EngagementV0()
    out = _tick(e, "ENGAGED", pal=0.25, complexity=0.50, vc=0.7, control="GUARDED")
    assert out.level == "L1"
    assert out.advice_scale == 0.7
    assert out.pal_lookahead_m == 8.0


def test_l2_single_tick_stays_l1():
    """A1：单 tick 满足 L2 条件仍为 L1（需连续 ≥ L2_HOLD_SECONDS）"""
    e = EngagementV0()
    out = _tick(e, "ENGAGED", pal=0.40, complexity=0.55, vc=0.7, control="GUARDED", now=0.0)
    assert out.level == "L1"


def test_l2_by_pal_after_hold():
    """L2：时间累计 ≥ 3s（每拍 dt=1，需 3 拍累计）后进入 L2"""
    e = EngagementV0()
    _tick(e, "ENGAGED", pal=0.40, complexity=0.55, vc=0.7, control="GUARDED", now=0.0)
    _tick(e, "ENGAGED", pal=0.40, complexity=0.55, vc=0.7, control="GUARDED", now=1.0)
    _tick(e, "ENGAGED", pal=0.40, complexity=0.55, vc=0.7, control="GUARDED", now=2.0)
    out = _tick(e, "ENGAGED", pal=0.40, complexity=0.55, vc=0.7, control="GUARDED", now=3.0)
    assert out.level == "L2"


def test_l2_by_complexity_after_hold():
    """L2：时间累计 ≥ 3s 后进入 L2"""
    e = EngagementV0()
    _tick(e, "ENGAGED", pal=0.25, complexity=0.65, vc=0.7, control="GUARDED", now=0.0)
    _tick(e, "ENGAGED", pal=0.25, complexity=0.65, vc=0.7, control="GUARDED", now=1.0)
    _tick(e, "ENGAGED", pal=0.25, complexity=0.65, vc=0.7, control="GUARDED", now=2.0)
    out = _tick(e, "ENGAGED", pal=0.25, complexity=0.65, vc=0.7, control="GUARDED", now=3.0)
    assert out.level == "L2"


def test_l3_requires_not_guarded():
    """L3：control_mode=GUARDED 时不出现 L3"""
    e = EngagementV0()
    out = _tick(e, "ENGAGED", pal=0.55, complexity=0.80, vc=0.85, control="GUARDED", now=0.0)
    assert out.level != "L3"


def test_l3_when_assisted():
    """L3：pal>=0.50, complexity>=0.75, vc>=0.75, control!=GUARDED（L3 逻辑未改）"""
    e = EngagementV0()
    out = _tick(e, "ENGAGED", pal=0.55, complexity=0.80, vc=0.85, control="ASSISTED", now=0.0)
    assert out.level == "L3"
    assert out.advice_scale == 1.0
    assert out.pal_lookahead_m == 18.0


def test_downgrade_needs_two_ticks():
    """降级需连续 2 个窗口（A1 不改退出）"""
    e = EngagementV0()
    _tick(e, "ENGAGED", pal=0.55, complexity=0.80, vc=0.85, control="ASSISTED", now=0.0)
    assert e._level == "L3"
    out = _tick(e, "ENGAGED", pal=0.25, complexity=0.50, vc=0.7, control="GUARDED", now=1.0)
    assert out.level == "L3"
    out = _tick(e, "ENGAGED", pal=0.25, complexity=0.50, vc=0.7, control="GUARDED", now=2.0)
    assert out.level == "L1"


def test_l2_after_hold_then_stay():
    """A1：时间累计 ≥ 3s 进入 L2 后，同条件保持 L2"""
    e = EngagementV0()
    for t in (0.0, 1.0, 2.0, 3.0):
        _tick(e, "ENGAGED", pal=0.40, complexity=0.55, vc=0.7, control="GUARDED", now=t)
    out = _tick(e, "ENGAGED", pal=0.40, complexity=0.55, vc=0.7, control="GUARDED", now=4.0)
    assert out.level == "L2"
