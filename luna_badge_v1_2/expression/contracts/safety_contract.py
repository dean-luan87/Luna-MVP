"""
Safety Contract (C-1)

安全相关合约字段
"""

from typing import Optional, Dict, Any

# 安全类型
SAFETY_TYPE_BLOCKED = "blocked"
SAFETY_TYPE_HAZARD = "hazard"
SAFETY_TYPE_WARNING = "warning"

# Safety Contract 字段定义
SAFETY_CONTRACT_FIELDS = {
    "safety_type": str,          # blocked / hazard / warning
    "direction": str,            # left / right / front / back
    "distance_m": float,        # 距离（米）
    "severity": int,             # 严重程度 0-3
    "confidence": float,         # 置信度 0~1
    "description": Optional[str]  # 描述（可选）
}

def create_safety_contract(
    safety_type: str,
    direction: str,
    distance_m: float,
    severity: int,
    confidence: float,
    description: Optional[str] = None
) -> Dict[str, Any]:
    """
    创建安全合约
    
    Args:
        safety_type: 安全类型
        direction: 方向
        distance_m: 距离（米）
        severity: 严重程度
        confidence: 置信度
        description: 描述（可选）
        
    Returns:
        Dict[str, Any]: 安全合约
    """
    contract = {
        "safety_type": safety_type,
        "direction": direction,
        "distance_m": distance_m,
        "severity": severity,
        "confidence": confidence
    }
    
    if description is not None:
        contract["description"] = description
    
    return contract
