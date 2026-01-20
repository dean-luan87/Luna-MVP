"""
Advisory Value System - B2 v0.2 Part 2

Part 2：AdvisoryValueSystem（工程结构，不是算法）

定位（工程口径）：
- 不参与世界理解
- 不做决策
- 不学习
- 只做一件事：把 B2 的"未来事实"转换成「信息价值标签」
"""

from dataclasses import dataclass, field
from typing import Dict, Any, Optional, Literal
from .future_simulation_result import FutureSimulationResult


@dataclass
class Advisory:
    """
    Advisory 数据结构（C 与 B 的唯一接口）
    
    2.2 Advisory 数据结构（C 与 B 的唯一接口）
    """
    type: Literal["PREWARN", "DEESCALATE", "NEUTRAL"]  # 类型
    ttl_sec: float  # 建议有效期
    confidence: float  # 0.0 ~ 1.0
    payload: Dict[str, Any] = field(default_factory=dict)  # 事实描述（非语言）


class AdvisoryValueSystem:
    """
    B2 v0.2 Part 2: Advisory Value System
    
    核心职责：
    - 把 FutureSimulationResult 转换成 Advisory
    - 不做决策，只做价值映射
    """
    
    def __init__(self):
        """初始化 Advisory Value System"""
        pass
    
    def generate_advisory(
        self,
        sim_result: FutureSimulationResult,
        has_task_chain: bool = False,
        c_state: Optional[str] = None,  # 只读，不影响 C
    ) -> Advisory:
        """
        生成 Advisory（输入 → 输出关系）
        
        输入：
        - FutureSimulationResult
        - 当前任务链状态（有 / 无）
        - 当前 C 状态（STABLE / RECOVERING，仅只读）
        
        输出（给 C）：
        Advisory(
            type="PREWARN",
            ttl_sec=5,
            confidence=0.7,
            payload={
                "reason": "path_overlap",
                "t": 3.0,
                "object_id": "bike_12"
            }
        )
        
        Args:
            sim_result: 未来预演结果
            has_task_chain: 是否有任务链
            c_state: C 当前状态（只读）
        
        Returns:
            Advisory: 给 C 的建议
        """
        # 2.4 价值映射规则（v0.2 定死）
        if sim_result.collisions:
            # 找到最早的碰撞
            earliest_collision = min(sim_result.collisions, key=lambda c: c.t_sec)
            
            if earliest_collision.t_sec <= 3.0:
                # collision in <= 3s
                confidence = 0.9
                advisory_type = "PREWARN"
                payload = {
                    "reason": "collision",
                    "t": earliest_collision.t_sec,
                    "object_id": earliest_collision.obj_id,
                    "distance": earliest_collision.distance,
                }
            else:
                # collision in > 3s
                confidence = 0.7
                advisory_type = "PREWARN"
                payload = {
                    "reason": "collision",
                    "t": earliest_collision.t_sec,
                    "object_id": earliest_collision.obj_id,
                }
        elif sim_result.path_overlap:
            # path_overlap in <= 5s
            # 简化：如果有 path_overlap，假设在 5s 内
            confidence = 0.7
            advisory_type = "PREWARN"
            payload = {
                "reason": "path_overlap",
                "t": 5.0,  # 简化
            }
        elif sim_result.region_enter:
            # region_enter
            earliest_region = min(sim_result.region_enter, key=lambda r: r.t_sec)
            confidence = 0.5
            advisory_type = "PREWARN"
            payload = {
                "reason": "region_enter",
                "t": earliest_region.t_sec,
                "region_id": earliest_region.region_id,
                "region_type": earliest_region.region_type,
            }
        else:
            # 无风险
            confidence = 0.3
            advisory_type = "DEESCALATE"
            payload = {
                "reason": "no_risk",
            }
        
        # 计算 TTL（基于 horizon）
        ttl_sec = min(10.0, sim_result.horizon_sec)
        
        return Advisory(
            type=advisory_type,
            ttl_sec=ttl_sec,
            confidence=confidence,
            payload=payload,
        )

