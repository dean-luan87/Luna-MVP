# -*- coding: utf-8 -*-
"""
View State Builder（视角状态构造器）

v0.4.3: 将 view_state 正式纳入 perception 构造
目标：只补"资格证明"，不补"能力"
"""

from typing import Dict, Any, Optional


def build_view_state(
    *,
    stability_score: float,
    range_m: float,
    visibility_score: float = 0.75,
    source: str = "vision",
    confidence: float = 0.8,
) -> Dict[str, Any]:
    """
    构造 view_state 字典（工具级，无判断逻辑）
    
    Args:
        stability_score: 稳定性分数 (0.0-1.0)
        range_m: 估计距离（米）
        visibility_score: 可见度分数 (0.0-1.0)，默认 0.75
        source: 数据来源，默认 "vision"
        confidence: 置信度 (0.0-1.0)，默认 0.8
    
    Returns:
        view_state 字典
    
    Note:
        - 没有任何"判断"逻辑
        - 只是封装事实状态
        - 用于 Gate 评估的前提条件
    """
    return {
        "stability_score": round(stability_score, 2),
        "range_m": round(range_m, 2),
        "visibility_score": round(visibility_score, 2),
        "source": source,
        "confidence": round(confidence, 2),
    }


def build_view_state_fallback() -> Dict[str, Any]:
    """
    构造 fallback view_state（当无法获取真实数据时）
    
    返回一个"明确缺失"的 view_state，这会：
    - 自动触发 Gate → READ_ONLY / SUSPENDED
    - 同时 DCS 会标记历史代码为 RED
    
    Returns:
        view_state 字典（标记为 missing）
    """
    return {
        "stability_score": 0.0,
        "range_m": 0.0,
        "visibility_score": 0.0,
        "source": "missing",
        "confidence": 0.0,
    }


def ensure_view_state_in_perception(perception: Dict[str, Any]) -> Dict[str, Any]:
    """
    确保 perception 中包含 view_state（兜底策略）
    
    如果 perception 中没有 view_state，添加 fallback view_state。
    这会自动触发 Gate → READ_ONLY / SUSPENDED，同时 DCS 会标记为 RED。
    
    Args:
        perception: perception 字典
    
    Returns:
        确保包含 view_state 的 perception 字典
    """
    if "view_state" not in perception:
        perception["view_state"] = build_view_state_fallback()
    return perception
