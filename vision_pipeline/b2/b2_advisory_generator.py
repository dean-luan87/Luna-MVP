"""
B2 Advisory Generator - 建议生成器

职责：
- 将 FutureWorld 转为 Advisory
- 不下指令，只给建议

只允许输出：
- DEESCALATE
- PREWARN
- PREPARE
"""

from typing import Optional, Dict, Any, List
from .b2_types import Advisory
from .b2_future_simulator import FutureWorld


class B2AdvisoryGenerator:
    """
    B2 建议生成器
    
    核心职责：
    - 将未来世界投影结果转为 Advisory
    - 不下指令，只给建议
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化建议生成器
        
        Args:
            config: 配置字典
        """
        self.config = config or {}
    
    def generate_advisory(
        self,
        future_world: FutureWorld,
    ) -> Optional[Advisory]:
        """
        生成建议
        
        Args:
            future_world: 未来世界投影结果
        
        Returns:
            Advisory 或 None（如果不需要建议）
        """
        # 检查是否有潜在冲突
        if future_world.potential_intersections:
            # 有冲突：生成 PREWARN
            earliest_impact = min(
                future_world.potential_intersections,
                key=lambda x: x.get("time_sec", float("inf"))
            )
            
            return Advisory(
                advisory_type="PREWARN",
                priority=0,
                confidence=0.7,
                time_to_impact_sec=earliest_impact.get("time_sec"),
                reason_code="FUTURE_CONFLICT",
                related_corridor_id=None,
                payload={
                    "impact_count": len(future_world.potential_intersections),
                    "earliest_impact_time": earliest_impact.get("time_sec"),
                }
            )
        else:
            # 无冲突：生成 DEESCALATE
            return Advisory(
                advisory_type="DEESCALATE",
                priority=2,
                confidence=0.6,
                time_to_impact_sec=None,
                reason_code="FUTURE_CLEAR",
                related_corridor_id=None,
                payload={
                    "horizon_sec": future_world.horizon_sec,
                }
            )

