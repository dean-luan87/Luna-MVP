from typing import Any, Dict, Optional

from .c_state import CState
from .c_types import CAction, COutput
from .c_thresholds import CThresholdProfile, DEFAULT_C_THRESHOLD_PROFILE


def _get_distance(perception_summary: Dict[str, Any]) -> Optional[float]:
    if not isinstance(perception_summary, dict):
        return None
    val = perception_summary.get("nearest_obstacle_distance")
    if val is None:
        return None
    try:
        return float(val)
    except (TypeError, ValueError):
        return None


def rule_emergency_stop(
    system_snapshot: Dict[str, Any],
    perception_summary: Dict[str, Any],
    gate_result: str,
    thresholds: CThresholdProfile = DEFAULT_C_THRESHOLD_PROFILE,
) -> Optional[COutput]:
    if str(gate_result).upper() == "BLOCK":
        return COutput(
            action=CAction.STOP,
            confidence=1.0,
            reason="emergency_stop_gate_block",
            c_state=CState.ACTIVE,
        )

    dist = _get_distance(perception_summary)
    dynamic_rush = bool(perception_summary.get("dynamic_target_fast_approach", False))
    approach_speed = perception_summary.get("approach_speed_mps")
    if approach_speed is not None:
        try:
            if float(approach_speed) > thresholds.approach_speed_fast_mps:
                dynamic_rush = True
        except (TypeError, ValueError):
            pass
    if dist is not None and dist < thresholds.obstacle_critical_m:
        return COutput(
            action=CAction.STOP,
            confidence=1.0,
            reason="emergency_stop_distance",
            c_state=CState.ACTIVE,
        )

    if dynamic_rush:
        return COutput(
            action=CAction.STOP,
            confidence=1.0,
            reason="emergency_stop_dynamic",
            c_state=CState.ACTIVE,
        )

    return None


def rule_hard_block(
    system_snapshot: Dict[str, Any],
    perception_summary: Dict[str, Any],
) -> Optional[COutput]:
    perception_state = str(system_snapshot.get("perception_state", "")).upper()
    calibration_state = str(system_snapshot.get("calibration_state", "")).upper()
    sensor_conflict = bool(perception_summary.get("sensor_conflict", False))

    if perception_state in {"FAILED", "NOT_READY"}:
        return COutput(
            action=CAction.HOLD,
            confidence=0.9,
            reason="hard_block_perception",
            c_state=CState.ACTIVE,
        )

    if calibration_state == "FAILED":
        return COutput(
            action=CAction.HOLD,
            confidence=0.9,
            reason="hard_block_calibration",
            c_state=CState.ACTIVE,
        )

    if sensor_conflict:
        return COutput(
            action=CAction.HOLD,
            confidence=0.9,
            reason="hard_block_sensor_conflict",
            c_state=CState.ACTIVE,
        )

    return None


def rule_simple_avoid(perception_summary: Dict[str, Any]) -> Optional[COutput]:
    if not isinstance(perception_summary, dict):
        return None

    left_safer = perception_summary.get("left_safer")
    right_safer = perception_summary.get("right_safer")

    if left_safer is True:
        return COutput(
            action=CAction.AVOID_LEFT,
            confidence=0.6,
            reason="simple_avoid_left",
            c_state=CState.ACTIVE,
        )

    if right_safer is True:
        return COutput(
            action=CAction.AVOID_RIGHT,
            confidence=0.6,
            reason="simple_avoid_right",
            c_state=CState.ACTIVE,
        )

    return None


def rule_hold(
    perception_summary: Dict[str, Any],
    thresholds: CThresholdProfile = DEFAULT_C_THRESHOLD_PROFILE,
) -> Optional[COutput]:
    dist = _get_distance(perception_summary)
    approach_speed = perception_summary.get("approach_speed_mps")
    if dist is not None and dist < thresholds.obstacle_near_m:
        return COutput(
            action=CAction.HOLD,
            confidence=0.7,
            reason="hold_obstacle_near",
            c_state=CState.ACTIVE,
        )
    if approach_speed is not None:
        try:
            if float(approach_speed) > thresholds.approach_speed_fast_mps:
                return COutput(
                    action=CAction.HOLD,
                    confidence=0.7,
                    reason="hold_fast_approach",
                    c_state=CState.ACTIVE,
                )
        except (TypeError, ValueError):
            pass
    return None
