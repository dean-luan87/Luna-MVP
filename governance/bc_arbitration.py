from c.types import CDecision


def arbitrate(c_result, b_result):
    if c_result.decision == CDecision.STOP:
        return {"final": "STOP", "source": "C"}
    if c_result.decision == CDecision.HOLD:
        return {"final": "HOLD", "source": "C"}
    return {"final": b_result, "source": "B"}
