from luna_badge_v1_2.governance.output_controller.controller import ModelOutputController
from luna_badge_v1_2.governance.risk_center.interfaces.signal import EnvelopeSignal


def _base_snapshot():
    return {
        "ts": 0.0,
        "self": {
            "position": {"x": 0.0, "y": 0.0},
            "velocity": {"x": 0.0, "y": 0.0},
            "heading": 0.0,
        },
        "objects": [],
        "restricted_zones": [],
        "hardware_state": "OK",
        "calibration_state": "READY",
        "control_distortion": "FALSE",
        "system_mode": "RUNTIME",
        "perception_state": "STABLE",
    }


def _valid_output():
    return {
        "model_id": "vision_model_v1",
        "model_version": "v1",
        "result": {"payload": "ok"},
        "confidence": 0.9,
        "meta": {},
    }


def _run_bc(with_risk: bool):
    controller = ModelOutputController()
    controller._c.decide = lambda _: "NONE"
    class _StubRisk:
        def __init__(self, signal):
            self._signal = signal
        def evaluate(self, _snapshot):
            return self._signal

    if with_risk:
        controller._risk = _StubRisk(EnvelopeSignal(True, "HIGH", "VISION", "STATIC_COLLISION", 1.0, []))
    else:
        controller._risk = _StubRisk(EnvelopeSignal(False, "NONE", "VISION", "UNKNOWN", None, []))
    return controller.process(
        task_domain="navigation",
        model_outputs=[_valid_output()],
        system_snapshot=_base_snapshot(),
    )


def test_risk_does_not_affect_decision():
    r1 = _run_bc(with_risk=False)
    r2 = _run_bc(with_risk=True)
    assert r1["decision"] == r2["decision"]


def test_risk_not_in_reason():
    r = _run_bc(with_risk=True)
    assert "risk" not in str(r["reason"]).lower()


def test_bc_snapshot_contains_risk():
    r = _run_bc(with_risk=True)
    risk = r["decision_trace"]["bc_snapshot"]["risk"]
    assert {"present", "level", "type", "time_to_risk"}.issubset(set(risk.keys()))
