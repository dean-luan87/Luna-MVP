# -*- coding: utf-8 -*-
"""
Gate Runtime Profile v0.5（冻结版）

这是 v0.5 的核心，不可省略。
让 Gate 从"规则判断器"升级为"真实调度中枢"。
"""

from dataclasses import dataclass
from typing import Optional, Literal


@dataclass
class GateRuntimeProfile:
    """
    Gate Runtime Profile v0.5
    
    这是 v0.5 的核心，不可省略。
    Gate 不只是"是否允许"，Gate 必须明确告诉 B：
    - 你可以跑多快（tick_interval_ms）
    - 跑多重（compute_level）
    - 跑到什么程度（authority_scope）
    """
    
    # 运行态裁决
    gate_mode: Literal["ACTIVE", "READ_ONLY", "SUSPENDED"]
    
    # 调度裁决核心
    compute_level: Literal["NONE", "LIGHT", "FULL"]
    tick_interval_ms: int
    allow_future_probe: bool = False  # v0.5 固定为 False
    authority_scope: Literal["ADVISORY_ONLY"] = "ADVISORY_ONLY"  # v0.5 固定为 ADVISORY_ONLY
    
    # 阻断原因（仅在 gate_mode != ACTIVE 时非 null）
    blocked_by: Optional[str] = None
    
    # 人类可读解释
    human_reason: str = ""
    
    def to_dict(self) -> dict:
        """转换为字典（用于 trace / JSON）"""
        return {
            "gate_mode": self.gate_mode,
            "runtime_profile": {
                "compute_level": self.compute_level,
                "tick_interval_ms": self.tick_interval_ms,
                "allow_future_probe": self.allow_future_probe,
                "authority_scope": self.authority_scope,
            },
            "blocked_by": self.blocked_by,
            "human_reason": self.human_reason,
        }
    
    def validate(self) -> list[str]:
        """
        验证 profile 的合法性
        
        Returns:
            违规列表（空列表表示合法）
        """
        violations = []
        
        # 验证 compute_level 与 gate_mode 的一致性
        if self.compute_level == "NONE" and self.gate_mode != "SUSPENDED":
            violations.append("compute_level=NONE 必须等价于 gate_mode=SUSPENDED")
        
        # 验证 tick_interval_ms
        if self.tick_interval_ms < 1:
            violations.append("tick_interval_ms 必须 >= 1")
        
        # 验证 allow_future_probe（v0.5 必须为 False）
        if self.allow_future_probe is True:
            violations.append("v0.5 禁止 allow_future_probe=true")
        
        # 验证 authority_scope（v0.5 必须为 ADVISORY_ONLY）
        if self.authority_scope != "ADVISORY_ONLY":
            violations.append("v0.5 禁止 authority_scope != ADVISORY_ONLY")
        
        # 验证 blocked_by（仅在 gate_mode != ACTIVE 时必填）
        if self.gate_mode != "ACTIVE" and self.blocked_by is None:
            violations.append("gate_mode != ACTIVE 时 blocked_by 必填")
        
        return violations
