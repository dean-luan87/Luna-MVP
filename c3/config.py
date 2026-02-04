# -*- coding: utf-8 -*-
from dataclasses import dataclass


@dataclass
class C3Config:
    enabled: bool = False  # 默认关闭

    # 学习门槛
    min_evidence: int = 5          # 延迟沉淀
    min_confidence: float = 0.6    # 成熟阈值

    # 环境门槛
    max_complexity: float = 0.5
    allowed_safety = ("SAFE",)
    allowed_control = ("ASSISTED", "SHARED")

    # 遗忘/衰减
    pending_ttl_days: float = 7.0
    decay_start_days: float = 14.0
    decay_rate_per_day: float = 0.98

    # 负样本触发
    negative_min_hits: int = 2
    negative_window_sec: int = 60
