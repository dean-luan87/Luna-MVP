"""
World Signature - B2 v0.2 缓存逻辑：第一层

世界指纹（WorldSignature）

核心思想：
- 粗粒度、抗抖动、抗噪声的世界状态摘要
- 用来回答："我现在还在同一个世界里吗？"
- 宁愿误判"世界变了"，也不要误判"世界没变"
"""

from dataclasses import dataclass
from typing import Optional, List, Set, Tuple, Any


@dataclass(frozen=True)
class WorldSignature:
    """
    B2 v0.2 缓存逻辑：第一层 - 世界指纹
    
    Task 1.1: WorldSignature 数据结构（frozen dataclass）
    
    核心职责：
    - 生成粗粒度、抗抖动的世界状态摘要
    - 判断"我现在还在同一个世界里吗？"
    
    设计原则：
    - 宁愿误判"世界变了"（多算一次）
    - 也不要误判"世界没变"（错过风险）
    """
    heading_bucket: int  # 朝向分桶（例如每 30° 一档）
    speed_bucket: int  # 速度分桶（0=静止, 1=慢, 2=中, 3=快）
    density_bucket: int  # 动态目标密度（0=低, 1=中, 2=高）
    has_path: bool  # 是否存在任务链路径
    region_ids: Tuple[str, ...]  # 可见大区域 ID（排序后的元组）
    
    def digest(self) -> str:
        """
        Task 1.1: digest() 方法
        
        计算世界指纹 hash（用于日志和比较）
        
        Returns:
            str: 世界指纹 hash（短格式，用于日志）
        """
        hash_value = hash((
            self.heading_bucket,
            self.speed_bucket,
            self.density_bucket,
            self.has_path,
            self.region_ids
        ))
        # 转换为正数并取前 8 位（用于日志）
        return f"{abs(hash_value) % (10**8):08d}"
    
    def __str__(self) -> str:
        """字符串表示（用于日志）"""
        return f"WorldSignature(digest={self.digest()})"



