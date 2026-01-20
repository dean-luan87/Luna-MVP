from typing import Optional

from ..interfaces.signal import EnvelopeSignal
from ..interfaces.snapshot import build_world_snapshot
from ..history.buffer import HistoryBuffer
from .decay import apply_decay
from .smoothing import smooth_over_window
from ...risk_layer.evaluator import RiskEvaluator


class RiskCenter:
    def __init__(self) -> None:
        self._risk = RiskEvaluator()
        self._history = HistoryBuffer(maxlen=3)

    def evaluate(self, snapshot: dict) -> EnvelopeSignal:
        world_snapshot = build_world_snapshot(snapshot)
        risk_signal = self._risk.evaluate(world_snapshot)

        present = bool(risk_signal.risk_present)
        level = risk_signal.risk_level if present else "NONE"
        if level not in {"LOW", "MEDIUM", "HIGH", "NONE"}:
            level = "LOW" if present else "NONE"

        envelope = EnvelopeSignal(
            present=present,
            level=level,
            domain="VISION",
            type=risk_signal.risk_type,
            time_to_event=risk_signal.time_to_risk,
            reason_codes=list(risk_signal.reason_codes),
        )

        previous = self._history.list()[-1] if self._history.list() else None
        envelope = apply_decay(previous, envelope)
        self._history.add(envelope)
        return smooth_over_window(self._history.list(), window=1)
