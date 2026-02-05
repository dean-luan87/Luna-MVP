# -*- coding: utf-8 -*-
"""PAL 前瞻只读调制（C）单元测试"""

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from pal.lookahead_modulation import apply_pal_lookahead


def test_non_engaged_returns_base():
    """非 ENGAGED：返回 base"""
    out = apply_pal_lookahead(6.0, None, "ASSISTED")
    assert out == 6.0
    out = apply_pal_lookahead(6.0, {"level": "L0", "pal_lookahead_m": 8.0}, "ASSISTED")
    assert out == 6.0


def test_guarded_returns_base():
    """GUARDED：即使 ENGAGED 也返回 base"""
    out = apply_pal_lookahead(6.0, {"level": "L2", "pal_lookahead_m": 12.0}, "GUARDED")
    assert out == 6.0


def test_engaged_uses_engagement_lookahead():
    """ENGAGED 且非 GUARDED：使用 engagement.pal_lookahead_m"""
    out = apply_pal_lookahead(6.0, {"level": "L1", "pal_lookahead_m": 8.0}, "ASSISTED")
    assert out == 8.0
    out = apply_pal_lookahead(6.0, {"level": "L2", "pal_lookahead_m": 12.0}, "ASSISTED")
    assert out == 12.0
    out = apply_pal_lookahead(6.0, {"level": "L3", "pal_lookahead_m": 18.0}, "ASSISTED")
    assert out == 18.0
