# vision_pipeline/b2/v03/param_diff.py
from __future__ import annotations
from typing import Dict, Optional


def diff_param_vector(
    prev: Optional[Dict[str, float]],
    cur: Dict[str, float],
    eps: float = 1e-6,
) -> Dict[str, float]:
    """
    计算参数变化量（cur - prev）
    prev 可为 None（表示首个事件）
    """
    if not prev:
        return cur.copy()

    diff: Dict[str, float] = {}
    keys = set(prev.keys()) | set(cur.keys())

    for k in keys:
        v0 = prev.get(k, 0.0)
        v1 = cur.get(k, 0.0)
        d = v1 - v0
        if abs(d) > eps:
            diff[k] = round(d, 4)

    return diff

