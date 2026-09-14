from __future__ import annotations

from abc import ABC, abstractmethod

from .types import A3Signals


class A3SignalProvider(ABC):
    @abstractmethod
    def collect(self) -> A3Signals:
        """Collect snapshot signals from the running system (read-only)."""
        raise NotImplementedError
