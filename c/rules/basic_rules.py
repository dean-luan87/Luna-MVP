from c.types import CDecision, CResult, CInput


def evaluate_basic_rules(c_input: CInput) -> CResult:
    if c_input.perception_health == "lost":
        return CResult(
            decision=CDecision.HOLD,
            reason_code="PERCEPTION_LOST",
            layer="L1",
            facts={"perception_health": "lost"},
        )

    if c_input.obstacle_distance_m is not None and c_input.obstacle_distance_m < 0.5:
        return CResult(
            decision=CDecision.STOP,
            reason_code="OBSTACLE_TOO_CLOSE",
            layer="L1",
            facts={"distance_m": c_input.obstacle_distance_m},
        )

    return CResult(
        decision=CDecision.PASS,
        reason_code="NO_IMMEDIATE_RISK",
        layer="NONE",
        facts={},
    )
