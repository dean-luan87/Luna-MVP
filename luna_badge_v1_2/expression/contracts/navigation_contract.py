"""
Navigation Contract (C-1)

导航合约定义

约束规则（写在类注释中）：
- turn_* 必须有 direction
- distance_m == 0 只允许在 stop / immediate_turn
- offset_m 不能为负
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any, Literal
import time
from .base_contract import BaseExpressionContract

# 导航动作类型
ACTION_GO_STRAIGHT = "go_straight"
ACTION_TURN_LEFT = "turn_left"
ACTION_TURN_RIGHT = "turn_right"
ACTION_STOP = "stop"

# 导航 Contract 字段定义
NAVIGATION_CONTRACT_FIELDS = {
    "action": str,              # go_straight / turn_left / turn_right / stop
    "distance_m": float,        # 距离（米）
    "offset_m": Optional[float],  # 偏移（米，可选）
    "direction": str,            # left / right / front
    "landmark_hint": Optional[str],  # 地标提示（可选）
    "confidence": float         # 置信度 0~1
}


@dataclass
class NavigationExpressionContract(BaseExpressionContract):
    """
    NavigationExpressionContract(BaseExpressionContract)
    
    字段必须包含：
    - action: Literal["go_straight", "turn_left", "turn_right", "stop"]
    - distance_m: float                    # >= 0
    - direction: Optional[Literal["left", "right", "front", "back"]]
    - offset_m: Optional[float]            # lateral offset
    - landmark_hint: Optional[str]
    
    约束规则：
    - turn_* 必须有 direction
    - distance_m == 0 只允许在 stop / immediate_turn
    - offset_m 不能为负
    """
    action: Literal["go_straight", "turn_left", "turn_right", "stop"]
    distance_m: float                    # >= 0
    direction: Optional[Literal["left", "right", "front", "back"]] = None
    offset_m: Optional[float] = None     # lateral offset
    landmark_hint: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """
        转换为字典
        
        Returns:
            Dict[str, Any]: 合约字典
        """
        result = super().to_dict()
        result.update({
            "action": self.action,
            "distance_m": self.distance_m
        })
        
        if self.direction is not None:
            result["direction"] = self.direction
        
        if self.offset_m is not None:
            result["offset_m"] = self.offset_m
        
        if self.landmark_hint is not None:
            result["landmark_hint"] = self.landmark_hint
        
        return result


def create_navigation_contract(
    action: str,
    distance_m: float,
    confidence: float,
    source: str = "fsm",
    direction: Optional[str] = None,
    offset_m: Optional[float] = None,
    landmark_hint: Optional[str] = None
) -> NavigationExpressionContract:
    """
    创建导航合约
    
    Args:
        action: 动作类型
        distance_m: 距离（米）
        confidence: 置信度
        source: 数据源（默认 "fsm"）
        direction: 方向（可选）
        offset_m: 偏移（可选）
        landmark_hint: 地标提示（可选）
        
    Returns:
        NavigationExpressionContract: 导航合约
    """
    return NavigationExpressionContract(
        intent_type="navigation",
        source=source,
        confidence=confidence,
        timestamp=time.time(),
        action=action,
        distance_m=distance_m,
        direction=direction,
        offset_m=offset_m,
        landmark_hint=landmark_hint
    )
