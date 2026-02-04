"""
FSM Policy Models (v1.4.8 StepB-5)

策略建议数据结构
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class FSMSuggestion:
    """
    给 FSM 的策略建议：只建议，不强制
    """
    # PRE_TURN 触发距离建议（米）
    pre_turn_distance_m: Optional[float] = None
    
    # 是否允许 GPS 参与 FSM 相关判断（仅建议）
    allow_gps: Optional[bool] = None
    
    # 是否建议"锁定当前路线阶段"（减少抖动）
    prefer_lock: Optional[bool] = None
    
    # 本轮建议的理由（用于日志/回放）
    reason: str = ""
    
    # 可选：附带证据快照（用于调试，不进入核心决策）
    evidence: Optional[Dict[str, Any]] = None






