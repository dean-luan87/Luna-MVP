# -*- coding: utf-8 -*-
"""
v1.8.4: 危险对象数据结构定义

职责：
- 定义 RiskObject、RiskGeometry、RiskRuntime 数据结构
- 提供危险对象的完整模型
"""

from dataclasses import dataclass, field
from typing import Literal, Optional, Dict, Any, List, Tuple
import time


@dataclass
class RiskGeometry:
    """
    危险几何信息
    
    - POINT: (x, y) 点
    - LINE: polyline [(x, y), ...] + length_m
    - AREA: polygon [(x, y), ...] + area_m2
    """
    type: Literal["POINT", "LINE", "AREA"]
    points: List[Tuple[float, float]]  # 坐标点列表
    length_m: Optional[float] = None    # LINE 类型使用
    area_m2: Optional[float] = None     # AREA 类型使用


@dataclass
class DynamicProfile:
    """
    动态/潮汐风险配置
    
    说明：
    - ALWAYS: 永远激活（但可以应用 hazard_multiplier）
    - TIME_WINDOW: 按时间窗口激活（例如上下班高峰）
    - CONDITION: 按外部条件激活（预留接口，后续接世界模型）
    
    DynamicProfile 设计约定：
    - dynamic 只决定 RiskObject 是否参与 Risk 计算
    - dynamic 不直接触发警告
    - dynamic 不影响 RiskLevel 的"趋势逻辑"
    - dynamic 的激活/失活不视为 Risk 上升
    """
    mode: Literal["ALWAYS", "TIME_WINDOW", "CONDITION"]
    
    # TIME_WINDOW 模式：活跃时间窗口列表 [(start_hour, end_hour), ...]
    # 例如 [(7, 9), (17, 19)] 表示 7-9 点、17-19 点
    active_windows: Optional[List[Tuple[int, int]]] = None
    
    # hazard 修正倍数（激活时应用）
    hazard_multiplier: float = 1.0
    
    # 非激活时是否完全忽略（不参与 RiskLevel 计算）
    ignore_when_inactive: bool = True


@dataclass
class RiskRuntime:
    """
    危险对象运行时状态
    
    说明：1.8.4 的"时间"只用于 cooldown 与去抖，不参与 RiskLevel
    """
    state: Literal["DORMANT", "WARNED", "COOLDOWN"]
    last_risk_level: float
    last_update_ts: float
    last_warn_ts: Optional[float] = None
    cooldown_until_ts: Optional[float] = None
    edge_distance_m: Optional[float] = None
    edge_trend: Literal["APPROACHING", "LEAVING", "STABLE"] = "STABLE"
    # v1.8.4: 动态区域激活状态（只读，用于调试）
    is_dynamic_active: Optional[bool] = None
    last_dynamic_check_ts: Optional[float] = None


@dataclass
class RiskObject:
    """
    危险对象模型（强制字段）
    
    说明：
    - 1.8.4 的"时间"只用于 cooldown 与去抖，不参与 RiskLevel
    - risk_class 在 1.8.4 先用 STATIC 为主
    """
    risk_id: str
    risk_class: Literal["STATIC", "SEMI_STATIC", "DYNAMIC"]
    risk_type: str  # 见 risk_types.py
    geometry: RiskGeometry
    hazard_level: float  # 0~1（来自 hazard_evaluator）
    confidence: float    # 0~1
    runtime: RiskRuntime
    meta: Dict[str, Any] = field(default_factory=dict)  # 扩展字段（来源、标签、备注）
    dynamic_profile: Optional[DynamicProfile] = None  # v1.8.4: 动态/潮汐风险配置（可选）

    def update_runtime(
        self,
        risk_level: float,
        distance_m: Optional[float],
        trend: Literal["APPROACHING", "LEAVING", "STABLE"],
        now_ts: Optional[float] = None
    ):
        """
        更新运行时状态
        
        Args:
            risk_level: 当前 RiskLevel
            distance_m: 到危险边界的距离
            trend: 边缘趋势
            now_ts: 当前时间戳（如果为 None 则使用 time.time()）
        """
        if now_ts is None:
            now_ts = time.time()
        
        self.runtime.last_risk_level = risk_level
        self.runtime.last_update_ts = now_ts
        self.runtime.edge_distance_m = distance_m
        self.runtime.edge_trend = trend

