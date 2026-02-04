# -*- coding: utf-8 -*-
"""
K) 多模态输入冲突仲裁 v0

把"来源不同的介入请求"统一成同一套候选任务，
再交给 Eligibility → Rhythm → Engagement → Arbitration。

冲突不是在 Advice 层解决，而是在「候选生成层」。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

# v0 来源优先级（固定）
SOURCE_VISION = "VISION"
SOURCE_VOICE = "VOICE"
SOURCE_TASK = "TASK"

# 冲突优先级：SAFETY(任何来源) > VOICE > VISION > TASK
SOURCE_PRIORITY = {SOURCE_VOICE: 2, SOURCE_VISION: 1, SOURCE_TASK: 0}


@dataclass
class InterventionCandidate:
    """v0 统一候选结构：不决定"说什么"，只决定"有没有资格竞争"""
    source: str  # VISION | VOICE | TASK
    task_id: str
    task_type: str  # NAV | ENV | TASK | SAFETY
    pal: float
    complexity: float
    engagement_level: str  # L1 | L2 | L3
    # 原始 decision 引用（用于后续 speak）
    decision: Dict[str, Any] = field(default_factory=dict)


def resolve_multimodal_conflict(
    candidates_by_source: Dict[str, List[InterventionCandidate]],
) -> Tuple[List[InterventionCandidate], Dict[str, Any]]:
    """
    冲突解决：按来源优先级选择候选。
    SAFETY（任何来源）→ 直接放行
    VOICE → 覆盖 VISION / TASK
    VISION → 默认
    TASK → 最低

    Returns:
        (selected_candidates, trace_dict)
    """
    sources = list(candidates_by_source.keys())
    if not sources:
        return [], {"sources": [], "selected_source": None, "reason": "NO_CANDIDATES"}

    # SAFETY 任何来源直接放行
    for src, cands in candidates_by_source.items():
        safety_cands = [c for c in cands if c.task_type == "SAFETY"]
        if safety_cands:
            return safety_cands, {
                "sources": sources,
                "selected_source": src,
                "reason": "SAFETY_FIRST",
            }

    # 按来源优先级选最高优先级非空来源
    for src in sorted(sources, key=lambda s: SOURCE_PRIORITY.get(s, -1), reverse=True):
        cands = candidates_by_source.get(src, [])
        if cands:
            return cands, {
                "sources": sources,
                "selected_source": src,
                "reason": "USER_INITIATED" if src == SOURCE_VOICE else "SOURCE_PRIORITY",
            }

    return [], {"sources": sources, "selected_source": None, "reason": "NO_CANDIDATES"}


def decisions_to_candidates(
    decisions: List[Dict[str, Any]],
    source: str,
    engagement_level: str,
    pal: float,
    complexity: float,
) -> List[InterventionCandidate]:
    """
    将 advice_decisions 转为 InterventionCandidate 列表。
    """
    from intervention.arbitrator_v0 import _map_category_to_task_type

    cands: List[InterventionCandidate] = []
    for d in decisions:
        if d.get("type") != "SPEAK" or not d.get("text"):
            continue
        task_id = d.get("advice_id") or f"fallback_{len(cands)}"
        is_safety = bool(d.get("is_safety"))
        cat = d.get("advice_category")
        task_type = _map_category_to_task_type(cat, is_safety)
        cands.append(
            InterventionCandidate(
                source=source,
                task_id=task_id,
                task_type=task_type,
                pal=pal,
                complexity=complexity,
                engagement_level=engagement_level,
                decision=d,
            )
        )
    return cands
