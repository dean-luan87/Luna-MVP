from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Dict, Tuple

from advice_budget.feedback import AdviceFeedback


@dataclass
class AdviceBudgetState:
    last_spoken_ts: Optional[float]
    accept_rate: float
    suppression_score: float
    stats: Dict[Tuple[str, str], dict] = field(default_factory=dict)

    def update_feedback(self, fb: AdviceFeedback):
        key = (fb.kind, fb.source)
        stats = self.stats.setdefault(
            key,
            {
                "shown": 0,
                "accepted": 0,
                "rejected": 0,
                "ema_accept": 0.5,
            },
        )

        stats["shown"] += 1
        if fb.accepted:
            stats["accepted"] += 1
        else:
            stats["rejected"] += 1

        alpha = 0.1
        target = 1.0 if fb.accepted else 0.0
        stats["ema_accept"] = (1 - alpha) * stats["ema_accept"] + alpha * target
