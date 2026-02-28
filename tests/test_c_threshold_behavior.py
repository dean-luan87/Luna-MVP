import pytest

from luna_badge_v1_2.governance.instinct_controller.c_controller import CController
from luna_badge_v1_2.governance.instinct_controller.c_thresholds import CThresholdProfile


def base_snapshot(**kwargs):
    snap = {
        "perception_state": "OK",
        "gate": "PASS",
    }
    snap.update(kwargs)
    return snap


def test_threshold_only_affects_trigger_not_failure():
    """
    阈值变化只能影响是否命中规则
    不能改变失败语义
    """
    low_thresholds = CThresholdProfile(
        obstacle_near_m=5.0,
        obstacle_critical_m=2.0,
        approach_speed_fast_mps=0.5,
    )

    high_thresholds = CThresholdProfile(
        obstacle_near_m=1.0,
        obstacle_critical_m=0.3,
        approach_speed_fast_mps=3.0,
    )

    c_low = CController(thresholds=low_thresholds)
    c_high = CController(thresholds=high_thresholds)

    snapshot = base_snapshot(
        nearest_obstacle_distance_m=2.5,
        approach_speed_mps=1.0,
    )

    out_low = c_low.decide(snapshot)
    out_high = c_high.decide(snapshot)

    assert out_low != out_high
    assert out_low in {"HOLD", "REQUEST_TAKEOVER"}
    assert out_high in {"HOLD", "REQUEST_TAKEOVER"}


def test_failed_state_is_invariant():
    """
    FAILED 状态不受阈值影响
    """
    thresholds = CThresholdProfile(
        obstacle_near_m=100.0,
        obstacle_critical_m=50.0,
        approach_speed_fast_mps=0.1,
    )

    c = CController(thresholds=thresholds)

    snapshot = {
        "perception_state": "FAILED",
        "gate": "PASS",
        "nearest_obstacle_distance_m": 0.1,
    }

    assert c.decide(snapshot) == "REQUEST_TAKEOVER"


def test_gate_block_is_invariant():
    """
    Gate=BLOCK 始终优先
    """
    thresholds = CThresholdProfile(
        obstacle_near_m=0.1,
        obstacle_critical_m=0.05,
        approach_speed_fast_mps=0.1,
    )

    c = CController(thresholds=thresholds)

    snapshot = {
        "perception_state": "OK",
        "gate": "BLOCK",
        "nearest_obstacle_distance_m": 100.0,
    }

    assert c.decide(snapshot) == "STOP"
