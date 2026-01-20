# vision_pipeline/b2/v03/param_weight_update.py
from __future__ import annotations
from typing import Dict, List


def suggest_weight_adjustment(
    regression_weights: Dict[str, float],
    top_k: int = 5,
) -> List[str]:
    """
    给出"值得关注/调整"的参数建议
    """
    ranked = sorted(
        regression_weights.items(),
        key=lambda x: abs(x[1]),
        reverse=True,
    )
    return [k for k, _ in ranked[:top_k]]

