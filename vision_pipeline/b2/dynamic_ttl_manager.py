"""
Dynamic TTL Manager - B2 v0.2 C阶段：决策节律动态拉长

核心思想：
- 安全直路：B2 → 20s 一次
- 复杂路口：B2 → 3~5s 一次
- 根据"未来不确定性"动态调整 TTL

这不是"学习"，而是"基于预演结果的规则调整"
"""

from typing import Optional
from .future_simulation_result import FutureSimulationResult


class DynamicTTLManager:
    """
    B2 v0.2 C阶段：动态 TTL 管理器
    
    核心职责：
    - 根据未来不确定性计算动态 TTL
    - 安全场景 → 长 TTL（降低频率）
    - 复杂场景 → 短 TTL（提高频率）
    """
    
    def __init__(
        self,
        base_ttl_sec: float = 10.0,
        min_ttl_sec: float = 3.0,
        max_ttl_sec: float = 20.0,
    ):
        """
        初始化动态 TTL 管理器
        
        Args:
            base_ttl_sec: 基础 TTL（秒），默认 10 秒
            min_ttl_sec: 最小 TTL（秒），默认 3 秒（复杂路口）
            max_ttl_sec: 最大 TTL（秒），默认 20 秒（安全直路）
        """
        self.base_ttl_sec = base_ttl_sec
        self.min_ttl_sec = min_ttl_sec
        self.max_ttl_sec = max_ttl_sec
    
    def compute_ttl(
        self,
        sim_result: Optional[FutureSimulationResult],
        has_task_chain: bool = False,
    ) -> float:
        """
        根据预演结果计算动态 TTL
        
        规则（C阶段核心）：
        1. 有碰撞 / 路径重叠 → 短 TTL（3~5s）
        2. 有区域进入 → 中等 TTL（8~10s）
        3. 完全安全 → 长 TTL（15~20s）
        4. 有任务链 → 稍微降低 TTL（更关注）
        
        Args:
            sim_result: 未来预演结果（可选）
            has_task_chain: 是否有任务链
        
        Returns:
            float: 动态 TTL（秒）
        """
        # 如果没有预演结果，使用基础 TTL
        if sim_result is None:
            return self.base_ttl_sec
        
        # 计算"未来不确定性"指标
        uncertainty_score = self._compute_uncertainty_score(sim_result)
        
        # 根据不确定性调整 TTL
        # uncertainty_score: 0.0 (完全安全) → 1.0 (高度不确定)
        # TTL: max_ttl_sec (20s) → min_ttl_sec (3s)
        ttl = self.max_ttl_sec - (uncertainty_score * (self.max_ttl_sec - self.min_ttl_sec))
        
        # 有任务链时，稍微降低 TTL（更关注）
        if has_task_chain:
            ttl *= 0.8
        
        # 限制在范围内
        ttl = max(self.min_ttl_sec, min(self.max_ttl_sec, ttl))
        
        return ttl
    
    def _compute_uncertainty_score(
        self,
        sim_result: FutureSimulationResult,
    ) -> float:
        """
        计算未来不确定性评分（0.0 ~ 1.0）
        
        规则：
        - 有碰撞（特别是近期碰撞）→ 高不确定性
        - 有路径重叠 → 中等不确定性
        - 有区域进入 → 低不确定性
        - 完全安全 → 0.0
        
        Args:
            sim_result: 未来预演结果
        
        Returns:
            float: 不确定性评分（0.0 ~ 1.0）
        """
        score = 0.0
        
        # 1. 碰撞事件（权重最高）
        if sim_result.collisions:
            # 计算最近碰撞时间
            # 兼容 dict 和 CollisionEvent 对象
            collision_times = []
            for c in sim_result.collisions:
                if isinstance(c, dict):
                    collision_times.append(c.get("t_sec", c.get("t", 999.0)))
                else:
                    collision_times.append(getattr(c, "t_sec", 999.0))
            if collision_times:
                min_collision_time = min(collision_times)
                # 越近的碰撞，不确定性越高
                if min_collision_time <= 3.0:
                    score += 0.8  # 3秒内碰撞 → 高不确定性
                elif min_collision_time <= 5.0:
                    score += 0.5  # 5秒内碰撞 → 中等不确定性
                else:
                    score += 0.3  # 5秒后碰撞 → 低不确定性
        
        # 2. 路径重叠（权重中等）
        if sim_result.path_overlap:
            score += 0.4
        
        # 3. 区域进入（权重较低）
        if sim_result.region_enter:
            # 计算最近区域进入时间
            # 兼容 dict 和 RegionEnterEvent 对象
            region_times = []
            for r in sim_result.region_enter:
                if isinstance(r, dict):
                    region_times.append(r.get("t_sec", r.get("t", 999.0)))
                else:
                    region_times.append(getattr(r, "t_sec", 999.0))
            if region_times:
                min_region_time = min(region_times)
                if min_region_time <= 5.0:
                    score += 0.2
                else:
                    score += 0.1
        
        # 限制在 0.0 ~ 1.0
        return min(1.0, score)

