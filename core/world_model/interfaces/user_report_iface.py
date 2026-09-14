# -*- coding: utf-8 -*-
"""
v1.8.5: User Report Interface（用户报告接口）

职责：
- 定义用户报告事件的数据结构
- 一期接口：不做 NLP 解析，只做结构化输入

设计原则：
- 用户报告不能直接写 Library
- 必须经过 MemoryRegistry / CandidatePool 分流
"""

from dataclasses import dataclass
from typing import List, Optional, Dict, Any


@dataclass
class UserReportEvent:
    """
    用户报告事件（一期接口）
    
    字段说明：
    - user_id: 用户 ID
    - raw_text: 原始文本（一期不做解析，只存储）
    - report_type: 报告类型（DISCOMFORT / PREFERENCE / FACT_CONFIRM / FACT_CONFLICT）
    - tags: 标签列表（从 raw_text 提取，一期简化）
    - claim_type: 事实类声明类型（可选，用于 FACT_CONFIRM / FACT_CONFLICT）
    - claim_payload: 事实类载荷（可选，用于 FACT_CONFIRM / FACT_CONFLICT）
    - intensity: 强度 [0.0 ~ 1.0]（用于 DISCOMFORT / PREFERENCE）
    - ts: 时间戳
    """
    user_id: str
    raw_text: str
    report_type: str  # "DISCOMFORT" | "PREFERENCE" | "FACT_CONFIRM" | "FACT_CONFLICT"
    tags: List[str]
    claim_type: Optional[str] = None  # e.g. "road_blocked", "flooded"
    claim_payload: Optional[Dict[str, Any]] = None
    intensity: Optional[float] = None
    ts: Optional[float] = None

