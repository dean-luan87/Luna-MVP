from typing import Optional

from c.types import CDecision, CResult, CInput

OBSTACLE_STOP_DISTANCE_M = 0.5
HUMAN_STOP_DISTANCE_M = 0.6


def evaluate(c_input: CInput) -> Optional[CResult]:
    if c_input.perception_health == "lost":
        return CResult(
            decision=CDecision.HOLD,
            reason_code="PERCEPTION_LOST",
            layer="L1",
            facts={"perception_health": "lost"},
        )

    d = c_input.obstacle_distance_m
    if d is not None and d < OBSTACLE_STOP_DISTANCE_M:
        return CResult(
            decision=CDecision.STOP,
            reason_code="OBSTACLE_TOO_CLOSE",
            layer="L1",
            facts={"distance_m": d, "threshold_m": OBSTACLE_STOP_DISTANCE_M},
        )

    h = c_input.human_proximity_m
    if h is not None and h < HUMAN_STOP_DISTANCE_M:
        return CResult(
            decision=CDecision.STOP,
            reason_code="HUMAN_TOO_CLOSE",
            layer="L1",
            facts={"distance_m": h, "threshold_m": HUMAN_STOP_DISTANCE_M},
        )

    return None
