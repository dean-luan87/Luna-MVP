from dataclasses import dataclass
from typing import List, Any

# === Alignment Note ===
# This file implements EnvelopeBus.
# Original issue proposal used risk_center/interfaces/envelope_bus.py.

from .signal import EnvelopeSignal


@dataclass(frozen=True)
class EnvelopeBus:
    signals: List[Any]
