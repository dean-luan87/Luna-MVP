"""
Advisory Value Scorer - B2 v0.2 Part 2

信息价值分级（Advisory Value System）

问题：
不是所有"未来信息"都值得告诉 C。
否则：
- C 会被噪声淹没
- 或过度谨慎

评分维度（只 3 个）：
1. 时间距离：越近越重要
2. 空间确定性：overlap > region
3. 连续性：是否连续多次出现

分级结果：
- LOW: 不给 C，只用于建模
- MEDIUM: 给 C，但低权重
- HIGH: 给 C，明确预警

规则（定死）：
- LOW → B2 自己消化
- MEDIUM / HIGH → 才进 AdvisoryQueue
- 同一类型 10 秒内最多 1 条
"""

from dataclasses import dataclass
from typing import Literal, Optional
from .future_simulation_result import FutureSimulationResult
from .b2_types_v02 import B2Advisory


@dataclass
class AdvisoryValueScore:
    """Advisory 价值评分"""
    value: float  # 0~1
    level: Literal["LOW", "MEDIUM", "HIGH"]
    reasons: list  # 评分原因


class AdvisoryValueScorer:
    """
    B2 v0.2 Part 2: Advisory 价值评分器
    
    核心职责：
    - 评估 Advisory 的价值
    - 决定是否给 C
    - 决定权重
    """
    
    def __init__(
        self,
        low_threshold: float = 0.3,
        medium_threshold: float = 0.6,
    ):
        """
        初始化价值评分器
        
        Args:
            low_threshold: LOW 阈值
            medium_threshold: MEDIUM 阈值
        """
        self.low_threshold = low_threshold
        self.medium_threshold = medium_threshold
        self._last_advisory_type: Optional[str] = None
        self._last_advisory_ts: float = 0.0
    
    def score(
        self,
        sim_result: FutureSimulationResult,
        advisory_type: str,
        current_ts: float,
    ) -> AdvisoryValueScore:
        """
        评分 Advisory 价值
        
        Args:
            sim_result: 未来预演结果
            advisory_type: Advisory 类型（PREWARN / DEESCALATE）
            current_ts: 当前时间戳
        
        Returns:
            AdvisoryValueScore: 价值评分
        """
        reasons = []
        value = 0.0
        
        # 维度 1: 时间距离（越近越重要）
        time_weight = self._time_weight(sim_result, reasons)
        
        # 维度 2: 空间确定性（overlap > region）
        spatial_weight = self._spatial_weight(sim_result, reasons)
        
        # 维度 3: 连续性（是否连续多次出现）
        continuity_bonus = self._continuity_bonus(advisory_type, current_ts, reasons)
        
        # 简化评分公式
        value = time_weight * spatial_weight * (1.0 + continuity_bonus)
        value = min(1.0, value)  # 限制在 0~1
        
        # 分级
        if value < self.low_threshold:
            level = "LOW"
        elif value < self.medium_threshold:
            level = "MEDIUM"
        else:
            level = "HIGH"
        
        return AdvisoryValueScore(
            value=value,
            level=level,
            reasons=reasons,
        )
    
    def _time_weight(self, sim_result: FutureSimulationResult, reasons: list) -> float:
        """
        维度 1: 时间距离（越近越重要）
        
        Args:
            sim_result: 未来预演结果
            reasons: 原因列表（用于记录）
        
        Returns:
            float: 时间权重（0~1）
        """
        # 找到最早的事件时间
        min_t = self.horizon_sec
        if sim_result.collisions:
            min_t = min(min_t, min(c.t_sec for c in sim_result.collisions))
        if sim_result.region_enter:
            min_t = min(min_t, min(r.t_sec for r in sim_result.region_enter))
        
        if min_t >= self.horizon_sec:
            reasons.append("no_near_event")
            return 0.1
        
        # 越近越重要：1.0 / (1.0 + t_sec)
        weight = 1.0 / (1.0 + min_t)
        reasons.append(f"time_weight={weight:.2f} (min_t={min_t:.1f}s)")
        return weight
    
    def _spatial_weight(self, sim_result: FutureSimulationResult, reasons: list) -> float:
        """
        维度 2: 空间确定性（overlap > region）
        
        Args:
            sim_result: 未来预演结果
            reasons: 原因列表（用于记录）
        
        Returns:
            float: 空间权重（0~1）
        """
        # overlap（碰撞）比 region（区域）更确定
        if sim_result.collisions:
            # 使用最大 overlap_ratio
            max_overlap = max(c.overlap_ratio for c in sim_result.collisions)
            weight = max_overlap
            reasons.append(f"spatial_weight={weight:.2f} (collision, max_overlap={max_overlap:.2f})")
            return weight
        
        if sim_result.path_overlap:
            weight = 0.7
            reasons.append(f"spatial_weight={weight:.2f} (path_overlap)")
            return weight
        
        if sim_result.region_enter:
            weight = 0.5
            reasons.append(f"spatial_weight={weight:.2f} (region_enter)")
            return weight
        
        reasons.append("spatial_weight=0.0 (no_spatial_event)")
        return 0.0
    
    def _continuity_bonus(self, advisory_type: str, current_ts: float, reasons: list) -> float:
        """
        维度 3: 连续性（是否连续多次出现）
        
        规则：同一类型 10 秒内最多 1 条
        
        Args:
            advisory_type: Advisory 类型
            current_ts: 当前时间戳
            reasons: 原因列表（用于记录）
        
        Returns:
            float: 连续性奖励（0~0.3）
        """
        # 检查是否连续
        if self._last_advisory_type == advisory_type:
            elapsed = current_ts - self._last_advisory_ts
            if elapsed < 10.0:
                # 连续出现，但时间太近，降低价值（避免重复）
                reasons.append(f"continuity_penalty (same_type_in_{elapsed:.1f}s)")
                return -0.2  # 惩罚
        
        # 更新记录
        self._last_advisory_type = advisory_type
        self._last_advisory_ts = current_ts
        
        return 0.0
    
    @property
    def horizon_sec(self) -> float:
        """预演时间窗口（用于时间权重计算）"""
        return 8.0  # 默认 8 秒

