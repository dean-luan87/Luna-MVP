# -*- coding: utf-8 -*-
"""
v1.8.4: 风险引擎（RiskLevel 计算 + ΔRisk 趋势 + 状态机）

职责：
- 计算 RiskLevel（HazardLevel × ProximityFactor × TrendFactor）
- 检测态势上升（ΔRisk）
- 管理状态机（DORMANT → WARNED → COOLDOWN）
"""

import time
import logging
from typing import Optional, Literal
from core.risk.risk_object import RiskObject
from core.risk.risk_types import get_risk_config
from core.risk.geometry_utils import distance_to_geometry

logger = logging.getLogger(__name__)


class RiskEngine:
    """
    风险引擎
    
    核心原则：
    - RiskLevel 不含时间累积项
    - 只判断态势上升，不判断"已安全"
    - 时间只用于 cooldown 与去抖
    """
    
    def __init__(self, trend_eps: float = 0.25):
        """
        初始化风险引擎
        
        Args:
            trend_eps: 趋势判断阈值（米），距离变化小于此值视为稳定
        """
        self.trend_eps = trend_eps
    
    def proximity_factor(self, distance_m: float, d0: float) -> float:
        """
        计算接近因子（ProximityFactor）
        
        仅基于"到危险边界的距离"，不做行为推断。
        
        Args:
            distance_m: 到危险边界的距离（米）
            d0: 距离归一化基准（米）
        
        Returns:
            float: ProximityFactor (0~1)，越近越大
        """
        if distance_m >= d0:
            return 0.0
        
        # 线性插值：距离越近，因子越大
        x = max(0.0, min(1.0, (d0 - distance_m) / d0))
        return x
    
    def trend_factor(self, trend: Literal["APPROACHING", "LEAVING", "STABLE"]) -> float:
        """
        计算趋势因子（TrendFactor）
        
        只关心距离变化趋势（近/远/稳定），不关心姿态。
        
        Args:
            trend: 边缘趋势
        
        Returns:
            float: TrendFactor
        """
        if trend == "APPROACHING":
            return 1.15
        elif trend == "LEAVING":
            return 0.95
        else:
            return 1.0
    
    def calculate_risk_level(
        self,
        risk_object: RiskObject,
        user_xy: tuple[float, float]
    ) -> tuple[float, float]:
        """
        计算态势风险等级（RiskLevel）
        
        RiskLevel = HazardLevel × Confidence × ProximityFactor × TrendFactor
        
        Args:
            risk_object: 危险对象
            user_xy: 用户位置 (x, y)
        
        Returns:
            tuple[float, float]: (risk_level, distance_m)
                - risk_level: RiskLevel (0.0 ~ 理论上限)
                - distance_m: 到危险边界的距离（米）
        """
        # 计算距离
        distance_m = distance_to_geometry(user_xy, risk_object.geometry)
        
        # 获取配置
        config = get_risk_config(risk_object.risk_type)
        d0 = config.get("d0", 10.0)
        
        # 计算 ProximityFactor
        prox = self.proximity_factor(distance_m, d0)
        
        # 计算 TrendFactor
        trend = risk_object.runtime.edge_trend
        trendf = self.trend_factor(trend)
        
        # 计算 RiskLevel
        # confidence 参与计算，能抑制不确定误报
        risk_level = risk_object.hazard_level * risk_object.confidence * prox * trendf
        
        # 限制在合理范围
        risk_level = max(0.0, min(2.0, risk_level))  # 理论上限为 2.0（hazard=1.0, conf=1.0, prox=1.0, trend=2.0）
        
        return risk_level, distance_m
    
    def calc_trend(
        self,
        prev_dist: Optional[float],
        curr_dist: float
    ) -> Literal["APPROACHING", "LEAVING", "STABLE"]:
        """
        计算边缘趋势
        
        Args:
            prev_dist: 上一次距离（米）
            curr_dist: 当前距离（米）
        
        Returns:
            str: 趋势（"APPROACHING" | "LEAVING" | "STABLE"）
        """
        if prev_dist is None:
            return "STABLE"
        
        if curr_dist < prev_dist - self.trend_eps:
            return "APPROACHING"
        elif curr_dist > prev_dist + self.trend_eps:
            return "LEAVING"
        else:
            return "STABLE"
    
    def should_warn(
        self,
        risk_object: RiskObject,
        current_risk_level: float,
        now_ts: Optional[float] = None
    ) -> bool:
        """
        判断是否应该触发警告
        
        唯一合法触发：ΔRisk > delta_warn 且不在 cooldown
        
        Args:
            risk_object: 危险对象
            current_risk_level: 当前 RiskLevel
            now_ts: 当前时间戳（如果为 None 则使用 time.time()）
        
        Returns:
            bool: 是否应该触发警告
        """
        if now_ts is None:
            now_ts = time.time()
        
        # 检查 cooldown
        if risk_object.runtime.cooldown_until_ts and now_ts < risk_object.runtime.cooldown_until_ts:
            return False
        
        # 获取配置
        config = get_risk_config(risk_object.risk_type)
        delta_warn = config.get("delta_warn", 0.15)
        
        # 计算 ΔRisk
        last_risk = risk_object.runtime.last_risk_level
        delta = current_risk_level - last_risk
        
        # 判断是否超过阈值
        if delta >= delta_warn:
            logger.debug(
                f"[RiskEngine] 检测到态势上升: risk_id={risk_object.risk_id}, "
                f"delta={delta:.3f} >= {delta_warn:.3f}, "
                f"current={current_risk_level:.3f}, last={last_risk:.3f}"
            )
            return True
        
        # 可选：SafetyBoundary 越界事件（接口桩）
        # if safety_boundary_iface.is_breached(...): return True
        
        return False
    
    def update_state(
        self,
        risk_object: RiskObject,
        warned: bool,
        now_ts: Optional[float] = None
    ) -> RiskObject:
        """
        更新状态机
        
        Args:
            risk_object: 危险对象
            warned: 是否触发了警告
            now_ts: 当前时间戳（如果为 None 则使用 time.time()）
        
        Returns:
            RiskObject: 更新后的危险对象
        """
        if now_ts is None:
            now_ts = time.time()
        
        config = get_risk_config(risk_object.risk_type)
        cooldown_s = config.get("cooldown_s", 12.0)
        
        if warned:
            # 触发警告 → 进入 COOLDOWN 状态
            risk_object.runtime.state = "COOLDOWN"
            risk_object.runtime.last_warn_ts = now_ts
            risk_object.runtime.cooldown_until_ts = now_ts + cooldown_s
            
            logger.info(
                f"[RiskEngine] 触发警告: risk_id={risk_object.risk_id}, "
                f"cooldown_until={risk_object.runtime.cooldown_until_ts:.1f}"
            )
        else:
            # 检查 cooldown 是否结束
            if risk_object.runtime.cooldown_until_ts and now_ts >= risk_object.runtime.cooldown_until_ts:
                risk_object.runtime.state = "DORMANT"
                risk_object.runtime.cooldown_until_ts = None
        
        return risk_object


