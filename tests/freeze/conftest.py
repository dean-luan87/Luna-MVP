import json
import pathlib
import pytest
from luna_badge_v1_2.governance.output_controller.controller import ModelOutputController
from luna_badge_v1_2.governance.risk_center.interfaces.signal import EnvelopeSignal


FIXTURE_DIR = pathlib.Path(__file__).parent / "fixtures"
FIXTURE_FILES = [
    "F-01_clear_safe_world.json",
    "F-02_static_obstacle_approaching.json",
    "F-03_dynamic_crossing.json",
    "F-04_perception_unstable.json",
    "F-05_hardware_failure.json",
]


@pytest.fixture(params=FIXTURE_FILES, ids=lambda x: x.replace(".json", ""))
def freeze_snapshot(request):
    path = FIXTURE_DIR / request.param
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def base_snapshot():
    path = FIXTURE_DIR / "F-01_clear_safe_world.json"
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _unwrap_fixture(fixture: dict) -> dict:
    snapshot = fixture["system_snapshot"]
    return {
        "ts": snapshot.get("ts", 0.0),
        "frame_id": snapshot.get("frame_id"),
        "context_mode": snapshot.get("context_mode"),
        "self": snapshot.get("self_state", {}),
        "objects": snapshot.get("perceived_objects", []),
        "restricted_zones": snapshot.get("environment", {}).get("restricted_zones", []),
        "perception_state": snapshot.get("system_facts", {}).get("perception_state"),
        "calibration_state": snapshot.get("system_facts", {}).get("calibration_state"),
        "hardware_state": snapshot.get("system_facts", {}).get("hardware_state"),
        "gate": snapshot.get("system_facts", {}).get("gate"),
        "control_distortion": snapshot.get("system_facts", {}).get("control_distortion", "FALSE"),
    }


@pytest.fixture
def freeze_inputs(freeze_snapshot):
    return {
        "system_snapshot": _unwrap_fixture(freeze_snapshot),
        "model_outputs": freeze_snapshot["model_outputs"]["candidate_actions"],
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


@pytest.fixture
def controller():
    return ModelOutputController()
