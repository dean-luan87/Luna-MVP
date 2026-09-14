"""
C1 状态触发条件

定义状态转换的触发条件。
"""

from typing import Optional
from .c1_types import C1State, C1Input


class C1Triggers:
    """
    C1 状态触发器
    
    职责：
    - 根据输入信号判断应该转换到哪个状态
    - 定义状态转换的触发条件
    """
    
    def __init__(self):
        self._current_state: Optional[C1State] = None
    
    def evaluate_state(
        self,
        input_signal: C1Input,
        current_state: Optional[C1State] = None
    ) -> C1State:
        """
        评估应该转换到哪个状态
        
        Args:
            input_signal: C1 输入信号
            current_state: 当前状态（如果为 None，则从 STABLE 开始）
        
        Returns:
            新的 C1 状态
        """
        if current_state is None:
            current_state = C1State.STABLE
        
        self._current_state = current_state
        
        # 优先级顺序（从高到低）：
        # 1. SUSPENDED（最高优先级，由 safety/privacy guard 触发）
        # 2. ALERT（风险提示）
        # 3. TRANSITION（场景变化提示）
        # 4. STABLE（默认）
        
        # 检查是否应该 SUSPENDED（由外部 guard 检查，这里只做基础判断）
        # 注意：实际的 SUSPENDED 判断在 C1Controller 中，由 safety/privacy guard 决定
        
        # 检查 ALERT（风险提示）
        if input_signal.risk_hint:
            return C1State.ALERT
        
        # 检查 TRANSITION（场景变化提示）
        if input_signal.next_scene_hint:
            return C1State.TRANSITION
        
        # 默认 STABLE
        return C1State.STABLE
    
    def should_transition(
        self,
        from_state: C1State,
        to_state: C1State
    ) -> bool:
        """
        判断是否应该进行状态转换
        
        Args:
            from_state: 当前状态
            to_state: 目标状态
        
        Returns:
            如果应该转换，返回 True
        """
        # 如果状态相同，不需要转换
        if from_state == to_state:
            return False
        
        # 允许的状态转换（简化版，后续可以扩展）
        allowed_transitions = {
            C1State.STABLE: [C1State.TRANSITION, C1State.ALERT, C1State.SUSPENDED],
            C1State.TRANSITION: [C1State.STABLE, C1State.ALERT, C1State.SUSPENDED],
            C1State.ALERT: [C1State.STABLE, C1State.TRANSITION, C1State.SUSPENDED],
            C1State.SUSPENDED: [C1State.STABLE, C1State.TRANSITION, C1State.ALERT],
        }
        
        return to_state in allowed_transitions.get(from_state, [])


