"""
Confirmation Manager (C-4.3)

确认机制

职责：
"这句话是不是有歧义，需要确认用户是否理解？"

这是避免误导视障用户的关键。

一期确认触发条件：
- confidence ∈ [0.6, 0.75]
- 或 场景切换（室内 → 室外）
- 或 用户连续犹豫（来自 FSM）

二期可以接入：
- 用户历史理解度
- 是否经常回答"是/不是"
"""

from typing import Dict, Any
from ..contracts.navigation_contract import NavigationExpressionContract


class ConfirmationManager:
    """
    确认管理器
    
    职责：
    - 判断是否需要确认
    - 避免误导用户
    - 一期：规则驱动
    - 二期：可接入用户理解度模型
    """
    
    def __init__(
        self,
        low_confidence_threshold: float = 0.6,
        high_confidence_threshold: float = 0.75
    ):
        """
        初始化确认管理器
        
        Args:
            low_confidence_threshold: 低置信度阈值（默认 0.6）
            high_confidence_threshold: 高置信度阈值（默认 0.75）
        """
        self.low_confidence_threshold = low_confidence_threshold
        self.high_confidence_threshold = high_confidence_threshold
    
    def should_confirm(
        self,
        contract: NavigationExpressionContract,
        context: Dict[str, Any]
    ) -> bool:
        """
        判断是否需要确认
        
        一期确认触发条件：
        1. confidence ∈ [low_threshold, high_threshold]
        2. 场景切换（室内 → 室外）
        3. 用户连续犹豫（来自 FSM）
        
        Args:
            contract: 导航合约
            context: 上下文（包含 scene_changed, user_hesitation 等）
            
        Returns:
            bool: True 表示需要确认
        """
        # 1. 置信度区间检查
        confidence = contract.confidence
        if (self.low_confidence_threshold <= confidence <= self.high_confidence_threshold):
            return True
        
        # 2. 场景切换检查
        if context.get("scene_changed", False):
            return True
        
        # 3. 用户连续犹豫检查
        if context.get("user_hesitation", False):
            return True
        
        # 4. 关键动作（如转弯）在低置信度时也需要确认
        if contract.action in {"turn_left", "turn_right"} and confidence < 0.8:
            return True
        
        return False
