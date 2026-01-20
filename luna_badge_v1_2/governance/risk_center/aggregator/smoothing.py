from typing import List

from ..interfaces.signal import EnvelopeSignal


_ORDER = ["NONE", "LOW", "MEDIUM", "HIGH"]


def smooth_over_window(signals: List[EnvelopeSignal], window: int = 1) -> EnvelopeSignal:
    if not signals:
        return EnvelopeSignal(False, "NONE", "VISION", "UNKNOWN", None, [])
    recent = signals[-window:]
    worst = max(recent, key=lambda s: _ORDER.index(s.level))
    return worst
