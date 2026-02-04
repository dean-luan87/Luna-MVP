"""
Governance Pipeline (C-4 总协调器)

表达治理管道

职责：
- 协调 C-4.1 ~ C-4.4 所有模块
- 提供统一的治理接口
- 输出治理决策
"""

from typing import Dict, Any
from .expression_gate import ExpressionGate
from .rate_limiter import RateLimiter
from .confirmation_manager import ConfirmationManager
from .escalation_manager import EscalationManager
from ..contracts.navigation_contract import NavigationExpressionContract
from ..calibration.expression_params import ExpressionParams


class GovernancePipeline:
    """
    表达治理管道
    
    职责：
    - 协调所有治理模块
    - 输出治理决策
    - 一期：规则驱动
    - 二期：可接入学习模型
    """
    
    def __init__(
        self,
        gate: ExpressionGate = None,
        limiter: RateLimiter = None,
        confirmer: ConfirmationManager = None,
        escalator: EscalationManager = None
    ):
        """
        初始化治理管道
        
        Args:
            gate: 表达闸门（可选，默认创建）
            limiter: 节流器（可选，默认创建）
            confirmer: 确认管理器（可选，默认创建）
            escalator: 升级管理器（可选，默认创建）
        """
        self.gate = gate or ExpressionGate()
        self.limiter = limiter or RateLimiter()
        self.confirmer = confirmer or ConfirmationManager()
        self.escalator = escalator or EscalationManager()
    
    def process(
        self,
        contract: NavigationExpressionContract,
        params: ExpressionParams,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        处理表达治理
        
        流程：
        1. Gate 检查：是否允许表达
        2. Rate Limiter 检查：是否节流
        3. Confirmation Manager 检查：是否需要确认
        4. Escalation Manager 检查：升级等级
        
        Args:
            contract: 导航合约
            params: 表达参数
            context: 上下文
            
        Returns:
            Dict[str, Any]: 治理决策
                - action: "allow" | "blocked" | "rate_limited"
                - confirm: bool（是否需要确认）
                - level: int（升级等级 1-5）
                - reason: str（原因）
        """
        # 1. Gate 检查
        if not self.gate.allow(contract, params, context):
            return {
                "action": "blocked",
                "reason": "gate_rejected",
                "confirm": False,
                "level": 1
            }
        
        # 2. Rate Limiter 检查
        action_key = contract.action
        urgency = params.urgency_level
        if not self.limiter.allow(action_key, urgency=urgency):
            return {
                "action": "rate_limited",
                "reason": "rate_limit_exceeded",
                "confirm": False,
                "level": 1
            }
        
        # 3. Confirmation Manager 检查
        should_confirm = self.confirmer.should_confirm(contract, context)
        
        # 4. Escalation Manager 检查
        escalation_context = {
            "collision_risk": context.get("collision_risk", False),
            "high_urgency": context.get("high_urgency", False),
            "urgency_level": params.urgency_level
        }
        level = self.escalator.level(escalation_context)
        
        return {
            "action": "allow",
            "confirm": should_confirm,
            "level": level,
            "reason": "approved"
        }
    
    def reset_on_state_change(self, new_state: str):
        """
        状态变化时重置（用于节流器）
        
        Args:
            new_state: 新状态
        """
        self.limiter.reset_on_state_change(new_state)
