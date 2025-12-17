"""
Expression Gate (C-4.1)

表达闸门

职责：
回答一句话："这句话，现在有没有资格被说出来？"

⚠️ 注意
Gate 只返回 True / False
不输出、不日志、不提示用户
"""

from typing import Dict, Any
from ..contracts.navigation_contract import NavigationExpressionContract
from ..calibration.expression_params import ExpressionParams


class ExpressionGate:
    """
    表达闸门
    
    职责：
    - 判断是否允许表达
    - 一期：规则驱动
    - 二期：可接入模型
    """
    
    def __init__(self, min_confidence: float = 0.6):
        """
        初始化表达闸门
        
        Args:
            min_confidence: 最小置信度阈值（默认 0.6）
        """
        self.min_confidence = min_confidence
    
    def allow(
        self,
        contract: NavigationExpressionContract,
        params: ExpressionParams,
        context: Dict[str, Any]
    ) -> bool:
        """
        判断是否允许表达
        
        判断依据（一期规则）：
        1. 置信度：confidence < min_confidence → 不允许
        2. 状态：FSM 非关键状态 → 降级（可选）
        3. 场景：SAFE_MODE → 强制允许
        4. 重复：与上一条语义相同 → 阻断
        
        Args:
            contract: 导航合约
            params: 表达参数
            context: 上下文（包含 duplicate, scene, fsm_state 等）
            
        Returns:
            bool: True 才允许继续输出
        """
        # 1. 置信度检查
        if contract.confidence < self.min_confidence:
            return False
        
        # 2. 重复检查
        if context.get("duplicate", False):
            return False
        
        # 3. 安全模式强制允许
        if context.get("scene") == "safe_mode":
            return True
        
        # 4. FSM 状态检查（可选）
        fsm_state = context.get("fsm_state")
        if fsm_state:
            # 非关键状态可以降级，但不完全阻断
            if fsm_state in {"IDLE", "PAUSE"}:
                # 可以允许，但优先级降低（由上层处理）
                pass
        
        return True
