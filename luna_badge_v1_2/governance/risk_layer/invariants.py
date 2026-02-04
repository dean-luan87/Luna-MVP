from .interfaces import RiskSignal


FORBIDDEN_KEYS = {
    "action",
    "decision",
    "command",
    "recommendation",
    "STOP",
    "HOLD",
    "REQUEST_TAKEOVER",
}


def assert_risk_invariants(signal: RiskSignal) -> None:
    for key in FORBIDDEN_KEYS:
        assert key not in signal.__dict__, "[RISK-INV] forbidden field present"
