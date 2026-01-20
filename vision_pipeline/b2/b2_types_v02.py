"""
B2 Types v0.2 - 标准数据结构（必须）

这是整个 B2 v0.2 的"语言体系"，不统一这个，后面一定会乱。

A5.1: B2 → C 的唯一接口：B2Advisory

设计原则：
- B2 不下指令
- B2 不改 C 的状态机
- B2 不触发执行
- B2 只提供结构化情报
- C 决定用不用、怎么用
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Literal


@dataclass
class ImpactEvent:
    """
    影响事件（可能与任务走廊相交）
    
    B2 v0.2: 给 B2 的中间产物
    """
    obj_id: str
    t_sec: float  # time to conflict (TTC)
    score: float
    ttc: float  # time to conflict（明确字段）
    overlap_ratio: float  # 重叠比例
    obj_confidence: float  # 对象置信度
    meta: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FutureWorld:
    """未来世界投影结果"""
    horizon_sec: float
    impacts: List[ImpactEvent] = field(default_factory=list)


@dataclass
class B2Advisory:
    """
    B2 建议（不是指令）
    
    A5.1: B2 → C 的唯一接口
    
    B2 → C 对接方案：标准接口结构
    
    ⚠️ 注意：
    - 没有"action"字段
    - 没有"should_do"
    - 只有 information + suggestion
    """
    advisory_type: Literal["PREWARN", "DEESCALATE", "WORLD_NOTE"]  # 未来可能有风险 / 明显安全 / 世界变化
    horizon_sec: float  # 预见的未来时间窗口（5~10s）
    confidence: float  # 0~1，B2 自信度
    impacts: List[ImpactEvent] = field(default_factory=list)  # 可能影响任务链的事件（可为空）
    suggestion: Dict[str, Any] = field(default_factory=dict)  # 给 C 的"建议参数"，不是动作
    trigger_reason: str = "TTL_EXPIRE"  # INIT / WORLD_CHANGE / TTL_EXPIRE / MANUAL / FUTURE_SIM
    meta: Dict[str, Any] = field(default_factory=dict)  # 额外信息（包含 ttl_sec 和 timestamp）
    
    @property
    def ttl_sec(self) -> float:
        """建议有效期（秒）"""
        return self.meta.get("ttl_sec", 10.0)
    
    @property
    def timestamp(self) -> float:
        """Advisory 产生时间戳"""
        return self.meta.get("timestamp", 0.0)
