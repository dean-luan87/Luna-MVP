#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
充足性判断模块（V1.8 冻结态）

Judge 层只产出"状态 + Code"，不产出"解释"。
所有 reason 只能来自白名单 ReasonCode。
"""

from typing import List, Dict, Any
from dataclasses import dataclass
from enum import Enum


class SufficiencyStatus(Enum):
    """充足性状态"""
    SUFFICIENT = "sufficient"
    INSUFFICIENT = "insufficient"


class ReasonCode(Enum):
    """充足性判断原因代码（白名单）"""
    # 数据量不足
    DATA_COUNT_TOO_LOW = "DATA_COUNT_TOO_LOW"
    # 必需对象缺失
    REQUIRED_OBJECT_NOT_FOUND = "REQUIRED_OBJECT_NOT_FOUND"
    # 置信度过低
    OBJECT_CONFIDENCE_LOW = "OBJECT_CONFIDENCE_LOW"
    # 上下文信息不足
    CONTEXT_INSUFFICIENT = "CONTEXT_INSUFFICIENT"


@dataclass
class JudgeResult:
    """判断结果（冻结态：只包含状态和代码，不包含解释）"""
    status: SufficiencyStatus
    reasons: List[str]  # 只包含 ReasonCode 值（字符串形式）


def check_sufficiency(data: List[Any], min_count: int = 5) -> JudgeResult:
    """
    检查数据充足性
    
    Args:
        data: 待检查的数据列表
        min_count: 最小数据量阈值（可配置）
    
    Returns:
        JudgeResult: 只包含状态和原因代码，不包含解释性文本
    """
    reasons: List[str] = []
    
    # 检查数据量
    if len(data) < min_count:
        reasons.append(ReasonCode.DATA_COUNT_TOO_LOW.value)
    
    # 判断状态
    if reasons:
        status = SufficiencyStatus.INSUFFICIENT
    else:
        status = SufficiencyStatus.SUFFICIENT
    
    return JudgeResult(
        status=status,
        reasons=reasons
    )
