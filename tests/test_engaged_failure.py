# -*- coding: utf-8 -*-
"""J) ENGAGED 事实信号 v0（signal-only）单元测试"""

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from intervention.engaged_failure import compute_engaged_signal, EngagedSignal


def test_not_engaged_returns_none():
    """未 ENGAGED → 不参与 N 层，返回 None"""
    assert compute_engaged_signal(
        engaged=False,
        action_decided=True,
        action_executed=False,
        rhythm_state="IDLE",
        arbitration_winner=None,
        cooldown_active=False,
    ) is None


def test_engaged_executed_signal():
    """ENGAGED 且已执行 → signal：executed=True, blocked=False, block_stage=None"""
    sig = compute_engaged_signal(
        engaged=True,
        action_decided=True,
        action_executed=True,
        rhythm_state="ENGAGED",
        arbitration_winner="WON",
        cooldown_active=False,
    )
    assert sig is not None
    assert sig.attempted is True
    assert sig.executed is True
    assert sig.blocked is False
    assert sig.block_stage is None


def test_engaged_blocked_cooldown():
    """ENGAGED 未执行且 cooldown_active → block_stage=COOLDOWN"""
    sig = compute_engaged_signal(
        engaged=True,
        action_decided=True,
        action_executed=False,
        rhythm_state="ENGAGED",
        arbitration_winner="WON",
        cooldown_active=True,
    )
    assert sig is not None
    assert sig.blocked is True
    assert sig.block_stage == "COOLDOWN"


def test_engaged_blocked_rhythm():
    """ENGAGED 未执行且 rhythm 非 ENGAGED → block_stage=RHYTHM"""
    sig = compute_engaged_signal(
        engaged=True,
        action_decided=True,
        action_executed=False,
        rhythm_state="IDLE",
        arbitration_winner="WON",
        cooldown_active=False,
    )
    assert sig is not None
    assert sig.blocked is True
    assert sig.block_stage == "RHYTHM"


def test_engaged_blocked_arbitration():
    """ENGAGED 未执行且 arbitration_winner=None → block_stage=ARBITRATION"""
    sig = compute_engaged_signal(
        engaged=True,
        action_decided=False,
        action_executed=False,
        rhythm_state="ENGAGED",
        arbitration_winner=None,
        cooldown_active=False,
    )
    assert sig is not None
    assert sig.blocked is True
    assert sig.block_stage == "ARBITRATION"


def test_engaged_blocked_unknown():
    """ENGAGED 未执行、无 COOLDOWN/RHYTHM/ARBITRATION 归因 → block_stage=UNKNOWN"""
    sig = compute_engaged_signal(
        engaged=True,
        action_decided=True,
        action_executed=False,
        rhythm_state="ENGAGED",
        arbitration_winner="WON",
        cooldown_active=False,
    )
    assert sig is not None
    assert sig.blocked is True
    assert sig.block_stage == "UNKNOWN"


def test_to_trace_dict():
    """to_trace_dict 含 attempted/executed/blocked/block_stage 与 raw_context"""
    sig = compute_engaged_signal(
        engaged=True,
        action_decided=True,
        action_executed=False,
        rhythm_state="ENGAGED",
        arbitration_winner=None,
        cooldown_active=False,
        extra_context={"view_confidence": 0.8},
    )
    d = sig.to_trace_dict()
    assert d["attempted"] is True
    assert d["executed"] is False
    assert d["blocked"] is True
    assert d["block_stage"] == "ARBITRATION"
    assert "raw_context" in d
    assert d["raw_context"].get("arbitration_winner") is None
    assert d["raw_context"].get("view_confidence") == 0.8
