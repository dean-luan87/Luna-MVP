from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Dict, Any


class EnvelopeStatus(str, Enum):
    WITHIN_ENVELOPE = "WITHIN_ENVELOPE"
    SAFE_ENOUGH = "SAFE_ENOUGH"
    ADMISSIBLE = "ADMISSIBLE"
    UNACCEPTABLE = "UNACCEPTABLE"


@dataclass(frozen=True)
class EnvelopeSignal:
    status: EnvelopeStatus
    reasons: List[str]
    confidence: Optional[float]
    timestamp: float


_FORBIDDEN_SYSTEM_KEYS = {"authority", "abilities", "decision", "selected_result", "reason", "user_input", "emotion"}


def assert_envelope_inputs(system_snapshot: Dict[str, Any], risk_projection: Dict[str, Any]) -> None:
    for key in _FORBIDDEN_SYSTEM_KEYS:
        assert key not in system_snapshot, "[ENVELOPE-INV] forbidden system_snapshot key"
    for key in {"decision", "action"}:
        assert key not in risk_projection, "[ENVELOPE-INV] forbidden risk_projection key"


def assert_envelope_output(signal: EnvelopeSignal) -> None:
    forbidden = {"decision", "action", "STOP", "HOLD", "REQUEST_TAKEOVER"}
    assert forbidden.isdisjoint(signal.__dict__.keys()), "[ENVELOPE-INV] forbidden output field"


def evaluate_envelope(system_snapshot: Dict[str, Any], risk_projection: Dict[str, Any]) -> EnvelopeSignal:
    assert_envelope_inputs(system_snapshot, risk_projection)
    timestamp = float(system_snapshot.get("ts", 0.0))
    signal = EnvelopeSignal(
        status=EnvelopeStatus.WITHIN_ENVELOPE,
        reasons=[],
        confidence=1.0,
        timestamp=timestamp,
    )
    assert_envelope_output(signal)
    return signal
