from typing import Optional

from ..interfaces.signal import EnvelopeSignal


_ORDER = ["NONE", "LOW", "MEDIUM", "HIGH"]


def _rank(level: str) -> int:
    return _ORDER.index(level)


def apply_decay(previous: Optional[EnvelopeSignal], current: EnvelopeSignal) -> EnvelopeSignal:
    if previous is None:
        return current
    if current.present:
        return current
    # already decayed evidence (e.g., from risk_layer)
    if current.level != "NONE":
        return current
    prev_rank = _rank(previous.level)
    new_rank = max(prev_rank - 1, 0)
    return EnvelopeSignal(
        present=new_rank > 0,
        level=_ORDER[new_rank],
        domain=previous.domain,
        type=previous.type,
        time_to_event=None,
        reason_codes=previous.reason_codes + ["DECAY_NO_EVIDENCE"],
    )
