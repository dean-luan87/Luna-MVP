from collections import deque
from typing import Deque, Iterable, List

from ..interfaces.signal import EnvelopeSignal


class HistoryBuffer:
    def __init__(self, maxlen: int = 3) -> None:
        self._buffer: Deque[EnvelopeSignal] = deque(maxlen=maxlen)

    def add(self, signal: EnvelopeSignal) -> None:
        self._buffer.append(signal)

    def list(self) -> List[EnvelopeSignal]:
        return list(self._buffer)
