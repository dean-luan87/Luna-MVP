from typing import Optional

from c.types import CDecision, CResult, CInput

CONFIDENCE_THRESHOLD = 0.7


def evaluate(c_input: CInput) -> Optional[CResult]:
    for key, value in c_input.confidence.items():
        if value < CONFIDENCE_THRESHOLD:
            return CResult(
                decision=CDecision.HOLD,
                reason_code=f"{key.upper()}_UNCERTAIN",
                layer="L3",
                facts={"confidence": value, "threshold": CONFIDENCE_THRESHOLD},
            )
    return None
