from __future__ import annotations

import time
from typing import List, Optional

from .types import AdviceCandidate
from .levels import AdviceLevel
from .frequency_engine import FrequencyEngine


class AdviceArbiter:
    def __init__(self, freq_engine: FrequencyEngine):
        self.freq_engine = freq_engine

    def arbitrate(
        self,
        candidates: List[AdviceCandidate],
        now: Optional[float] = None,
    ) -> Optional[AdviceCandidate]:
        if not candidates:
            return None

        now = now or time.time()

        emergencies = [c for c in candidates if self._is_emergency(c)]
        if emergencies:
            return max(emergencies, key=lambda c: c.priority)

        normals = sorted(
            candidates,
            key=lambda c: (c.priority, self._source_weight(c.source)),
            reverse=True,
        )

        for c in normals:
            if self.freq_engine.can_emit(
                advice_kind=c.kind,
                source=c.source,
                level=AdviceLevel.NORMAL,
                now=now,
            ):
                return c

        return None

    def mark_emitted(self, c: AdviceCandidate, now: Optional[float] = None):
        now = now or time.time()
        level = AdviceLevel.EMERGENCY if self._is_emergency(c) else AdviceLevel.NORMAL
        self.freq_engine.mark_emitted(
            advice_kind=c.kind,
            source=c.source,
            level=level,
            now=now,
        )

    @staticmethod
    def _source_weight(source: str) -> int:
        return {
            "pal": 3,
            "roi": 2,
            "ocr": 1,
        }.get(source, 0)

    @staticmethod
    def _is_emergency(c: AdviceCandidate) -> bool:
        if isinstance(c.level, AdviceLevel):
            return c.level == AdviceLevel.EMERGENCY
        return str(c.level) == AdviceLevel.EMERGENCY.value
