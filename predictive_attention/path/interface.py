from __future__ import annotations

from typing import Protocol

from predictive_attention.context import PalContext
from predictive_attention.schema import PathStackState


class PathManager(Protocol):
    def update(self, ctx: PalContext) -> PathStackState:
        """Update main/branch path state from motion samples. No side effects."""
