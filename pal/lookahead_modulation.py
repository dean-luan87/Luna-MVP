# -*- coding: utf-8 -*-
"""
PAL 前瞻距离只读调制（C）

ENGAGED 的介入强度影响 PAL 的前瞻距离。
不改 PAL v0 内部评分逻辑，非 ENGAGED 行为完全不变。
"""

from __future__ import annotations

from typing import Any, Dict, Optional

PAL_DEFAULT_LOOKAHEAD_M = 6.0


def apply_pal_lookahead(
    pal_base_lookahead_m: float,
    engagement: Optional[Dict[str, Any]],
    control_mode: str,
) -> float:
    """
    非 ENGAGED 或 GUARDED：返回 base，行为不变。
    ENGAGED 且 control_mode != GUARDED：返回 engagement.pal_lookahead_m。
    """
    if control_mode == "GUARDED":
        return pal_base_lookahead_m
    if not engagement or engagement.get("level", "L0") == "L0":
        return pal_base_lookahead_m
    look = engagement.get("pal_lookahead_m")
    if look is not None and look > 0:
        return float(look)
    return pal_base_lookahead_m
