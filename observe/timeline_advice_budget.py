from __future__ import annotations

from typing import Dict, Any, List

from advice_budget.schema import AdviceDecision, AdviceCandidate


def snapshot_advice_budget_debug(
    decisions: List[AdviceDecision],
    candidates: List[AdviceCandidate],
) -> Dict[str, Any]:
    return {
        "count": len(decisions),
        "items": [
            {
                "kind": c.kind,
                "is_safety": c.is_safety,
                "value": c.value,
                "source": c.source,
                "allow": d.allow,
                "urgency": d.urgency,
                "cooldown_s": d.cooldown_s,
                "reason": d.reason,
            }
            for c, d in zip(candidates, decisions)
        ],
    }
