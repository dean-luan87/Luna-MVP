"""
World Fact Emitter (v1.4.8 Step 12)

将导航内部状态 / 事件，转为 WorldFact
"""

import time
from typing import Dict, Any
from expression.world_fact import WorldFact


class WorldFactEmitter:
    """
    将导航内部状态 / 事件，转为 WorldFact
    """
    
    @staticmethod
    def emit(
        fact_type: str,
        scene: str,
        spatial_ref: Dict[str, Any],
        confidence: float,
        source: str,
        raw_ref_id: str
    ) -> WorldFact:
        """
        发射 WorldFact
        
        Args:
            fact_type: 事实类型（如 "PATH_BLOCKED", "LANDMARK_DETECTED"）
            scene: 场景（"indoor" / "outdoor" / "mixed"）
            spatial_ref: 空间参考（距离、方向、相对位置等）
            confidence: 置信度 0~1
            source: 数据源（"LOCAL_MAP" / "GPS" / "VISION" / "FUSION"）
            raw_ref_id: 回溯到原始系统的ID
            
        Returns:
            WorldFact: 世界事实
        """
        return WorldFact(
            fact_type=fact_type,
            ts=time.time(),
            scene=scene,
            spatial_ref=spatial_ref,
            confidence=confidence,
            source=source,
            raw_ref_id=raw_ref_id
        )






