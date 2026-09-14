from typing import List

from world_knowledge.schema import ObservationSignal


class EvidenceRecorder:
    """
    Record OCR/vision/web signals for later verification and curation.
    """

    def __init__(self):
        self._buf: List[ObservationSignal] = []

    def add(self, signal: ObservationSignal):
        self._buf.append(signal)

    def drain(self) -> List[ObservationSignal]:
        out = self._buf
        self._buf = []
        return out
