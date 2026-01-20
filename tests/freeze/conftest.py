import pytest
from luna_badge_v1_2.governance.output_controller.controller import ModelOutputController
from luna_badge_v1_2.governance.risk_center.interfaces.signal import EnvelopeSignal


@pytest.fixture
def base_snapshot():
    return {
        "model_outputs": [
            {
                "model_id": "vision_model_v1",
                "model_version": "v1",
                "confidence": 0.9,
                "meta": {},
                "output": {"intent": "move", "speed": 0.2},
            }
        ],
        "system_snapshot": {
            "ts": 0.0,
            "self": {"position": {"x": 0.0, "y": 0.0}, "velocity": {"x": 0.0, "y": 0.0}, "heading": 0.0},
            "objects": [],
            "restricted_zones": [],
            "perception_state": "READY",
            "calibration_state": "OK",
            "hardware_state": "OK",
            "control_distortion": "FALSE",
            "gate": "PASS",
        },
    }


class _StubRisk:
    def __init__(self, signal):
        self._signal = signal

    def evaluate(self, *_args, **_kwargs):
        return self._signal


@pytest.fixture
def low_risk_controller():
    ctrl = ModelOutputController()
    ctrl._risk = _StubRisk(EnvelopeSignal(False, "NONE", "VISION", "UNKNOWN", None, []))
    return ctrl


@pytest.fixture
def high_risk_controller():
    ctrl = ModelOutputController()
    ctrl._risk = _StubRisk(EnvelopeSignal(True, "HIGH", "VISION", "DYNAMIC", 1.0, []))
    return ctrl


@pytest.fixture
def fixed_time(monkeypatch):
    import time

    monkeypatch.setattr(time, "time", lambda: 1000.0)
    return 1000.0
