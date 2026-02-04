from typing import Any, Dict

from .c_state import CState, CStateContext
from .c_types import CAction, COutput
from .c_rules import (
    rule_emergency_stop,
    rule_hard_block,
    rule_simple_avoid,
    rule_hold,
)
from .c_thresholds import CThresholdProfile, DEFAULT_C_THRESHOLD_PROFILE
from ..invariants import assert_c_invariants, assert_c_input_invariants


MAX_FAIL_COUNT = 3


class CController:
    def __init__(
        self,
        thresholds: CThresholdProfile = DEFAULT_C_THRESHOLD_PROFILE,
        threshold_version_id: str = "default",
    ):
        self._thresholds = thresholds
        self._threshold_version_id = threshold_version_id

    def handle(
        self,
        system_snapshot: Dict[str, Any],
        perception_summary: Dict[str, Any],
        gate_result: str,
        last_state: CStateContext,
    ) -> COutput:
        assert "authority" not in system_snapshot
        assert "abilities" not in system_snapshot

        if last_state.state == CState.FAILED:
            return COutput(
                action=CAction.REQUEST_TAKEOVER,
                confidence=1.0,
                reason="c_failed_state",
                c_state=CState.FAILED,
                threshold_version_id=self._threshold_version_id,
            )

        if last_state.fail_count >= MAX_FAIL_COUNT:
            return COutput(
                action=CAction.REQUEST_TAKEOVER,
                confidence=1.0,
                reason="c_failed_state",
                c_state=CState.FAILED,
                threshold_version_id=self._threshold_version_id,
            )

        rules = [
            lambda: rule_emergency_stop(system_snapshot, perception_summary, gate_result, self._thresholds),
            lambda: rule_hard_block(system_snapshot, perception_summary),
            lambda: rule_simple_avoid(perception_summary),
            lambda: rule_hold(perception_summary, self._thresholds),
        ]

        for rule in rules:
            output = rule()
            if output is not None:
                output.threshold_version_id = self._threshold_version_id
                return output

        return COutput(
            action=CAction.REQUEST_TAKEOVER,
            confidence=1.0,
            reason="fail_safe",
            c_state=CState.ACTIVE,
            threshold_version_id=self._threshold_version_id,
        )

    def decide(self, system_snapshot: Dict[str, Any]) -> str:
        assert_c_input_invariants(system_snapshot)
        if "authority" in system_snapshot or "abilities" in system_snapshot:
            raise RuntimeError("CController received polluted system_snapshot")

        gate_result = system_snapshot.get("gate", "PASS")
        perception_state = str(system_snapshot.get("perception_state", "")).upper()
        if perception_state == "FAILED":
            decision = CAction.REQUEST_TAKEOVER.value
            assert_c_invariants(decision)
            return decision

        if str(gate_result).upper() == "BLOCK":
            decision = CAction.STOP.value
            assert_c_invariants(decision)
            return decision

        obstacle_dist = system_snapshot.get("nearest_obstacle_distance_m")
        approach_speed = system_snapshot.get("approach_speed_mps")

        if obstacle_dist is not None:
            try:
                dist_val = float(obstacle_dist)
            except (TypeError, ValueError):
                dist_val = None
            if dist_val is not None:
                if dist_val < self._thresholds.obstacle_critical_m:
                    decision = CAction.STOP.value
                    assert_c_invariants(decision)
                    return decision
                if dist_val < self._thresholds.obstacle_near_m:
                    decision = CAction.HOLD.value
                    assert_c_invariants(decision)
                    return decision

        if approach_speed is not None:
            try:
                speed_val = float(approach_speed)
            except (TypeError, ValueError):
                speed_val = None
            if speed_val is not None and speed_val > self._thresholds.approach_speed_fast_mps:
                decision = CAction.HOLD.value
                assert_c_invariants(decision)
                return decision

        decision = CAction.REQUEST_TAKEOVER.value
        assert_c_invariants(decision)
        return decision
