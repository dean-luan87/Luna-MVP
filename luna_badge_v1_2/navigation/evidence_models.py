"""
Evidence Models (v1.4.8 Step 5)

统一证据数据结构定义
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class EvidenceSource(Enum):
    """证据来源"""
    VISUAL = "VISUAL"
    MAP = "MAP"
    GPS = "GPS"
    SYSTEM = "SYSTEM"


class EvidenceKind(Enum):
    """证据类型"""
    # 场景相关
    SCENE_INDOOR = "SCENE_INDOOR"
    SCENE_OUTDOOR = "SCENE_OUTDOOR"
    SCENE_TRANSITION = "SCENE_TRANSITION"
    
    # 定位相关
    LANDMARK_MATCH = "LANDMARK_MATCH"
    VISUAL_STABILITY = "VISUAL_STABILITY"
    GPS_STABILITY = "GPS_STABILITY"
    PATH_CONSISTENCY = "PATH_CONSISTENCY"
    
    # 冲突相关
    CONFLICT = "CONFLICT"


@dataclass
class Evidence:
    """证据数据类（必须包含 TTL 与 meta）"""
    source: EvidenceSource
    kind: EvidenceKind
    value: float          # 0..1
    ts: float
    ttl_s: float         # Time To Live (秒)
    meta: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AuthorityConfidenceSnapshot:
    """
    AuthorityConfidenceSnapshot（Step5 核心产物）
    
    注意：dominant_candidate 只是"候选态势"，不是裁决结果
    """
    visual_score: float
    map_vision_score: float
    gps_score: float
    
    dominant_candidate: Optional[str]  # "VISUAL" / "MAP_VISION" / "GPS"（先用 str，避免和 Step3 enum耦合）
    confidence_gap: float              # top1 - top2
    
    stability: float                   # 稳定性分数
    decay_state: Dict[str, float]      # 衰减状态（各证据的当前值）
    reason_trace: List[str]            # 原因追踪
    
    ts: float
    window_s: float                    # 时间窗口大小（秒）






