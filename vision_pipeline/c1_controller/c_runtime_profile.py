"""
C RuntimeProfile v0.5 (Frozen)

与 B 的 GateRuntimeProfile 同构，用于 C 的运行态可观测能力。
这是"驾驶员状态监控"，不是"驾驶行为"。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Optional


class ControlMode(str, Enum):
    """C 运行态裁决"""
    ACTIVE = "ACTIVE"
    DEGRADED = "DEGRADED"
    SUSPENDED = "SUSPENDED"


class ControlLevel(str, Enum):
    """C 控制级别"""
    NONE = "NONE"
    ASSIST = "ASSIST"
    FULL = "FULL"


@dataclass(frozen=True)
class CRuntimeProfile:
    """
    v0.5 frozen runtime control object for C.
    This is the single source of truth for whether/how C executes at runtime.
    
    与 B 的 GateRuntimeProfile 同构，但语义不同：
    - B: 能不能算
    - C: 能不能控
    """
    version: str
    mode: ControlMode
    control_level: ControlLevel
    update_interval_ms: int
    blocked_by: Optional[str] = None
    human_reason: str = ""
    
    # v0.5 扩展字段（与用户需求文档对齐）
    range_m: Optional[float] = None
    confidence_level: Optional[float] = None
    compute_level: Optional[str] = None  # "FULL | PARTIAL | NONE"
    latency_ms: Optional[int] = None
    handoff: Dict[str, Any] = field(default_factory=lambda: {
        "from_b": False,
        "accepted": False,
        "reason": None
    })
    meta: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式（用于 trace）"""
        result = {
            "version": self.version,
            "mode": self.mode.value,
            "control_level": self.control_level.value,
            "update_interval_ms": int(self.update_interval_ms),
            "blocked_by": self.blocked_by,
            "human_reason": self.human_reason,
        }
        
        # 可选字段
        if self.range_m is not None:
            result["range_m"] = float(self.range_m)
        if self.confidence_level is not None:
            result["confidence_level"] = float(self.confidence_level)
        if self.compute_level is not None:
            result["compute_level"] = self.compute_level
        if self.latency_ms is not None:
            result["latency_ms"] = int(self.latency_ms)
        if self.handoff:
            result["handoff"] = self.handoff
        if self.meta:
            result["meta"] = self.meta
        
        return result
