from .interfaces.signal import EnvelopeSignal


FORBIDDEN_KEYS = {"decision", "action", "STOP", "HOLD", "REQUEST_TAKEOVER"}


def assert_envelope_invariants(signal: EnvelopeSignal) -> None:
    for key in FORBIDDEN_KEYS:
        assert key not in signal.__dict__, "[RISK-CENTER-INV] forbidden field present"


def assert_reason_codes_append_only(previous: EnvelopeSignal, current: EnvelopeSignal) -> None:
    prev = previous.reason_codes or []
    curr = current.reason_codes or []
    assert curr[: len(prev)] == prev, "[RISK-CENTER-INV] reason_codes must be append-only"
