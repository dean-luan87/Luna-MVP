# -*- coding: utf-8 -*-
"""
v1.8.4: Risk 调试快照（Debug Snapshot）

职责：
- 生成每一帧的 risk 评估快照
- 让工程师一眼看懂：当前帧里 risk 为什么"有 / 没有 / 没说话"

设计原则：
- 不影响功能逻辑
- 不触发任何播报
- 只读快照
- 每一帧可选生成
- 结构化（dict / JSON）
"""

from dataclasses import dataclass, asdict
from typing import List, Optional, Dict, Any, Tuple


@dataclass
class RiskObjectSnapshot:
    """
    单个风险对象的快照
    
    包含该对象在当前帧的完整评估状态
    """
    risk_id: str
    risk_type: str
    dynamic_active: Optional[bool]  # 动态区域是否激活
    hazard_level: float  # 当前 hazard_level（已应用动态修正）
    distance_m: Optional[float]  # 到危险边界的距离
    trend: str  # 边缘趋势（APPROACHING / LEAVING / STABLE）
    risk_level: float  # 当前 RiskLevel
    delta_risk: float  # ΔRisk（当前 RiskLevel - 上次 RiskLevel）
    state: str  # 状态机状态（DORMANT / WARNED / COOLDOWN）
    reason: Optional[str] = None  # 未参与计算的原因（如 "dynamic_inactive"）


@dataclass
class RiskDebugSnapshot:
    """
    Risk 调试快照
    
    包含当前帧所有风险对象的评估状态和最终决策结果
    
    v1.8.5 Phase A 扩展：
    - scene: 场景信息（只读，不参与判断）
    
    v1.8.5 Phase B 扩展：
    - scene_registry: 场景注册表状态（只读，不参与判断）
    """
    ts: float  # 时间戳
    user_xy: Tuple[float, float]  # 用户位置
    objects: List[RiskObjectSnapshot]  # 所有风险对象的快照
    advisory_triggered: bool  # 是否触发了 ADVISORY
    advisory_text: Optional[str] = None  # 如果触发，播报文本是什么
    scene: Optional[Dict[str, Any]] = None  # v1.8.5 Phase A: 场景信息（只读，不参与判断）
    scene_registry: Optional[Dict[str, Any]] = None  # v1.8.5 Phase B: 场景注册表状态（只读，不参与判断）

    def to_dict(self) -> Dict[str, Any]:
        """
        转换为字典（用于 JSON 序列化或日志输出）
        
        Returns:
            Dict[str, Any]: 快照字典
        """
        return asdict(self)

