from typing import Optional

from c.types import CDecision, CResult, CInput


def evaluate(c_input: CInput) -> Optional[CResult]:
    if c_input.traffic_light == "red":
        return CResult(
            decision=CDecision.HOLD,
            reason_code="RED_LIGHT",
            layer="L2",
            facts={"traffic_light": "red"},
        )

    if c_input.crosswalk_signal == "stop":
        return CResult(
            decision=CDecision.HOLD,
            reason_code="CROSSWALK_STOP",
            layer="L2",
            facts={"crosswalk_signal": "stop"},
        )

    if c_input.passage_state == "blocked":
        return CResult(
            decision=CDecision.HOLD,
            reason_code="PASSAGE_BLOCKED",
            layer="L2",
            facts={"passage_state": "blocked"},
        )

    if c_input.floor_state == "moving":
        return CResult(
            decision=CDecision.HOLD,
            reason_code="FLOOR_NOT_ARRIVED",
            layer="L2",
            facts={"floor_state": "moving"},
        )

    if c_input.facility_state == "unavailable":
        return CResult(
            decision=CDecision.HOLD,
            reason_code="FACILITY_UNAVAILABLE",
            layer="L2",
            facts={"facility_state": "unavailable"},
        )

    return None
