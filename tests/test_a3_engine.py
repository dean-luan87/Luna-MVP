from a3.engine import A3Engine
from a3.config import A3Config
from a3.types import A3Signals, SafetyLevel, ControlMode


def test_disabled_returns_neutral():
    eng = A3Engine(A3Config(enabled=False))
    mode = eng.tick(A3Signals())
    assert mode.safety_level == SafetyLevel.SAFE
    assert mode.control_mode == ControlMode.ASSISTED


def test_redline_forces_danger_guarded():
    cfg = A3Config(enabled=True)
    eng = A3Engine(cfg)
    s = A3Signals(redline_hit=True)
    mode = eng.tick(s)
    assert mode.safety_level == SafetyLevel.DANGER
    assert mode.control_mode == ControlMode.GUARDED


def test_hold_prevents_fast_downgrade():
    cfg = A3Config(enabled=True)
    cfg.smoothing.alpha = 1.0
    cfg.thresholds.min_mode_hold_ms = 2000
    eng = A3Engine(cfg)

    s1 = A3Signals(redline_hit=True)
    m1 = eng.tick(s1, now_ms=1000)
    assert m1.control_mode == ControlMode.GUARDED

    s2 = A3Signals(risk_density=0.0)
    m2 = eng.tick(s2, now_ms=1500)
    assert m2.control_mode == ControlMode.GUARDED

    m3 = eng.tick(s2, now_ms=4000)
    assert m3.control_mode != ControlMode.GUARDED
