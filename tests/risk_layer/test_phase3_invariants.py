import pytest

from luna_badge_v1_2.governance.risk_center.phase3.invariants import assert_phase3_invariants


def test_phase3_forbidden_reads():
    with pytest.raises(AssertionError):
        assert_phase3_invariants({"decision": "execute"})
    with pytest.raises(AssertionError):
        assert_phase3_invariants({"authority": "A3"})
    with pytest.raises(AssertionError):
        assert_phase3_invariants({"c_decision": "STOP"})
from collections import deque

from luna_badge_v1_2.governance.risk_layer.dynamic.cpa import is_cpa_invalidated
from luna_badge_v1_2.governance.risk_layer.dynamic.trajectory_shape import estimate_curvature
from luna_badge_v1_2.governance.risk_layer.evaluator import apply_risk_decay, smooth_risk_over_window
from luna_badge_v1_2.governance.risk_layer.interfaces import Vec2, RiskSignal, WorldObject, WorldSnapshot
from luna_badge_v1_2.governance.risk_layer.evaluator import RiskEvaluator


def test_cpa_invalidation():
    assert is_cpa_invalidated(1.0, 0.1, 1.0, 2.0) is True
    assert is_cpa_invalidated(1.0, 1.0, 1.0, 0.5) is False


def test_curvature_breaks_vo():
    curv = estimate_curvature(0.0, 2.0, dt=1.0)
    assert curv > 0.7


def test_risk_decay_on_no_evidence():
    prev = RiskSignal(True, "HIGH", "RELATIVE_MOTION", 1.0, None, [])
    curr = RiskSignal(False, "LOW", "UNKNOWN", None, None, [])
    decayed = apply_risk_decay(prev, curr)
    assert decayed.risk_level in {"MEDIUM", "LOW"}


def test_smoothing_uses_worst_level():
    signals = deque(
        [
            RiskSignal(True, "LOW", "UNKNOWN", None, None, []),
            RiskSignal(True, "HIGH", "RELATIVE_MOTION", 1.0, None, []),
            RiskSignal(True, "LOW", "UNKNOWN", None, None, []),
        ],
        maxlen=3,
    )
    worst = smooth_risk_over_window(signals)
    assert worst.risk_level == "HIGH"


def test_curvature_reduces_vo_risk_level():
    evaluator = RiskEvaluator()
    snap1 = WorldSnapshot(
        ts=0.0,
        self_position=Vec2(0.0, 0.0),
        self_velocity=Vec2(1.0, 0.0),
        self_heading=0.0,
        objects=[WorldObject("o1", Vec2(5.0, 0.0), Vec2(-1.0, 0.0), 0.5, "vehicle")],
        restricted_zones=[],
    )
    evaluator.evaluate(snap1, horizon_sec=5.0)
    snap2 = WorldSnapshot(
        ts=1.0,
        self_position=Vec2(1.0, 0.0),
        self_velocity=Vec2(1.0, 0.0),
        self_heading=2.0,
        objects=[WorldObject("o1", Vec2(4.0, 0.0), Vec2(-1.0, 0.0), 0.5, "vehicle")],
        restricted_zones=[],
    )
    signal = evaluator.evaluate(snap2, horizon_sec=5.0)
    assert signal.risk_level in {"MEDIUM", "LOW", "UNKNOWN"}
