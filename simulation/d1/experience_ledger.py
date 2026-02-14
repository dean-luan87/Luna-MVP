# -*- coding: utf-8 -*-
"""
D1 Experience Ledger：占位。
后续写入 C 的发布反馈/回滚反馈，供 Candidate Generator 做“历史避坑”（降低回滚邻域采样概率）。
"""
from typing import Any, Dict, List, Optional

# 占位：当前不落盘，接口预留
def record_feedback(
    candidate_id: str,
    patch_path: str,
    outcome: str,  # "released" | "rolled_back"
    reason: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> None:
    """记录一次发布/回滚反馈。当前 no-op。"""
    pass


def get_rollback_neighborhood(patch_params: Dict[str, float], radius: float = 0.2) -> List[Dict[str, float]]:
    """占位：返回应避免采样的邻域。当前返回空。"""
    return []
