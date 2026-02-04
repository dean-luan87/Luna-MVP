import pytest

from luna_badge_v1_2.governance.output_controller.controller import ModelOutputController


@pytest.fixture()
def base_snapshot():
    return {
        "hardware_state": "OK",
        "calibration_state": "READY",
        "control_distortion": "FALSE",
        "system_mode": "RUNTIME",
        "perception_state": "STABLE",
        "risk_level": "LOW",
        "context_mode": "NORMAL",
    }


@pytest.fixture()
def mock_valid_output():
    def _factory():
        return {
            "model_id": "vision_model_v1",
            "model_version": "v1",
            "result": {"payload": "ok"},
            "confidence": 0.9,
            "meta": {},
        }

    return _factory


@pytest.fixture()
def mock_controller():
    return ModelOutputController()
