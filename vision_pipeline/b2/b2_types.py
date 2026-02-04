"""
B2 Types - 标准数据结构

这是整个 B2 的"语言体系"，不统一这个，后面一定会乱。

关键点：
- B2 只输出 Advisory，不输出指令
- C 可以只看 advisory_type + priority + confidence
- FutureBuffer 是"未来剧本缓存"，不是实时决策
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
import time


# =========================
# 基础结构
# =========================

@dataclass
class ImpactEvent:
    """影响事件（可能与任务走廊相交）"""
    event_id: str
    event_type: str  # e.g. "dynamic_object", "static_block", "crowd", "low_visibility"
    position: Any  # world or image coord (opaque to B2)
    velocity: Optional[Any] = None  # may be None
    extent: Optional[Any] = None  # bounding / region
    risk_level: float = 0.0  # 0~1 (来自规则或上游模块)
    affects_corridor: bool = False  # 是否与任务走廊有几何关系
    time_to_impact_sec: Optional[float] = None


@dataclass
class TaskCorridor:
    """任务走廊"""
    corridor_id: str
    source: str  # "route", "heading_guess"
    geometry: Any  # polyline / polygon / cone
    width_m: Optional[float] = None
    confidence: float = 0.0  # 0~1
    horizon_sec: float = 5.0  # 预演时间窗口


# =========================
# B2 核心输出
# =========================

@dataclass
class FutureSegmentBuffer:
    """未来片段缓存（未来剧本缓存，不是实时决策）"""
    horizon_sec: float
    corridor_id: str
    predicted_conflicts: List[ImpactEvent] = field(default_factory=list)
    safe_window_sec: Optional[float] = None
    risk_window_sec: Optional[float] = None
    invalidation_keys: List[str] = field(default_factory=list)
    created_ts: float = field(default_factory=time.time)
    ttl_sec: float = 6.0  # 默认 5~10 秒内


@dataclass
class Advisory:
    """建议信号（不是指令）"""
    advisory_type: str  # PREWARN / DEESCALATE / REROUTE_SUGGEST / LOW_VISIBILITY
    priority: int  # 0 = highest
    time_to_impact_sec: Optional[float] = None
    impact_range_m: Optional[float] = None
    confidence: float = 0.0  # 0~1
    reason_code: str = ""  # ENUM string
    related_corridor_id: Optional[str] = None
    payload: Dict[str, Any] = field(default_factory=dict)  # 额外信息


@dataclass
class ConfidenceReport:
    """置信结构"""
    world_observability: float  # 遮挡/抖动后的可信度
    model_dependency: float  # 依赖历史模型的比例
    corridor_certainty: float
    overall: float


@dataclass
class WorldModelPatch:
    """世界模型增量（默认不下发给 C）"""
    patch_type: str  # "new_region", "updated_obstacle", "crowd_hotspot"
    payload: Dict[str, Any] = field(default_factory=dict)
    confidence: float = 0.0


@dataclass
class B2Output:
    """B2 输出（必须固定结构，便于 C 接入/后端存档）"""
    ts: float
    b2_run_id: str
    trigger_reason: str  # WORLD_CHANGE / EVENT_CHANGE / TTL_EXPIRE / FORCE_FALLBACK

    future_buffer: Optional[FutureSegmentBuffer] = None
    advisories: List[Advisory] = field(default_factory=list)
    confidence: ConfidenceReport = field(default_factory=lambda: ConfidenceReport(
        world_observability=0.0,
        model_dependency=0.0,
        corridor_certainty=0.0,
        overall=0.0,
    ))

    world_model_patch: Optional[WorldModelPatch] = None
    metrics: Dict[str, Any] = field(default_factory=dict)
