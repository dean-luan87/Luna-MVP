from luna_badge_v1_2.governance.instinct_controller.c_threshold_registry import (
    THRESHOLD_REGISTRY,
)
from luna_badge_v1_2.governance.instinct_controller.c_threshold_resolver import (
    resolve_c_threshold_profile,
)
from luna_badge_v1_2.governance.instinct_controller.c_controller import CController


def test_threshold_source_switch_does_not_change_failure():
    snap = {
        "perception_state": "FAILED",
        "gate": "PASS",
        "context_mode": "indoor_safe",
    }

    for key, profile in THRESHOLD_REGISTRY.items():
        c = CController(thresholds=profile)
        assert c.decide(snap) == "REQUEST_TAKEOVER"


def test_resolver_prefers_user_override():
    snap = {
        "context_mode": "indoor_safe",
        "user_preference": "user_conservative",
    }
    assert resolve_c_threshold_profile(snap) == "user_conservative"


def test_resolver_falls_back_to_context_then_default():
    snap_context = {"context_mode": "outdoor_open"}
    assert resolve_c_threshold_profile(snap_context) == "outdoor_open"

    snap_default = {"context_mode": "unknown_context"}
    assert resolve_c_threshold_profile(snap_default) == "default"
