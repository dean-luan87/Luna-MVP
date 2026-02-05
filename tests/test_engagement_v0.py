# -*- coding: utf-8 -*-
"""ENGAGED 介入强度 v0 单元测试"""

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from intervention.engagement_v0 import EngagementV0


def _tick(e, rhythm, pal, complexity, vc, control):
    return e.tick(
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


def test_l2_by_pal():
    """L2：pal>=0.35"""
    e = EngagementV0()
    out = _tick(e, "ENGAGED", pal=0.40, complexity=0.50, vc=0.7, control="GUARDED")
    assert out.level == "L2"


def test_l2_by_complexity():
    """L2：complexity>=0.60"""
    e = EngagementV0()
    out = _tick(e, "ENGAGED", pal=0.25, complexity=0.65, vc=0.7, control="GUARDED")
    assert out.level == "L2"


def test_l3_requires_not_guarded():
    """L3：control_mode=GUARDED 时不出现 L3"""
    e = EngagementV0()
    out = _tick(e, "ENGAGED", pal=0.55, complexity=0.80, vc=0.85, control="GUARDED")
    assert out.level != "L3"


def test_l3_when_assisted():
    """L3：pal>=0.50, complexity>=0.75, vc>=0.75, control!=GUARDED"""
    e = EngagementV0()
    out = _tick(e, "ENGAGED", pal=0.55, complexity=0.80, vc=0.85, control="ASSISTED")
    assert out.level == "L3"
    assert out.advice_scale == 1.0
    assert out.pal_lookahead_m == 18.0


def test_downgrade_needs_two_ticks():
    """降级需连续 2 个窗口"""
    e = EngagementV0()
    _tick(e, "ENGAGED", pal=0.50, complexity=0.80, vc=0.85, control="ASSISTED")
    assert e._level == "L3"
    # 1 tick 满足 L1，不降级
    out = _tick(e, "ENGAGED", pal=0.25, complexity=0.50, vc=0.7, control="GUARDED")
    assert out.level == "L3"
    # 2 tick 满足 L1，降级
    out = _tick(e, "ENGAGED", pal=0.25, complexity=0.50, vc=0.7, control="GUARDED")
    assert out.level == "L1"


def test_upgrade_immediate():
    """升级立即生效"""
    e = EngagementV0()
    _tick(e, "ENGAGED", pal=0.25, complexity=0.50, vc=0.7, control="GUARDED")
    assert e._level == "L1"
    out = _tick(e, "ENGAGED", pal=0.40, complexity=0.50, vc=0.7, control="GUARDED")
    assert out.level == "L2"
