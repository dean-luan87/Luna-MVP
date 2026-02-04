from c.types import CDecision, CResult


def apply_c_veto(c_result: CResult) -> dict:
    if c_result.decision == CDecision.STOP:
        return {"action": "STOP", "reason": c_result.reason_code}
    if c_result.decision == CDecision.HOLD:
        return {"action": "HOLD", "reason": c_result.reason_code}
    return {"action": "PASS", "reason": c_result.reason_code}
