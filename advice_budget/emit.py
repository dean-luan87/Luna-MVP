from __future__ import annotations

from typing import List, Optional

from .arbiter import AdviceArbiter
from .types import AdviceCandidate


def choose_advice_to_emit(
    arbiter: AdviceArbiter,
    candidates: List[AdviceCandidate],
) -> Optional[AdviceCandidate]:
    return arbiter.arbitrate(candidates)
