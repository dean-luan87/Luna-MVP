"""
C1 观察策略（轻 / 重 / 优先级）

根据状态决定抽帧策略。
"""

from c1_controller.c1_state import C1State


class C1Policy:
    """
    C1 策略引擎
    
    职责：
    - 根据状态决定是否抽帧、fps、观察模式、优先级
    """
    
    @staticmethod
    def decide(state: C1State):
        """
        根据状态决定抽帧策略
        
        Args:
            state: 当前 C1 状态
        
        Returns:
            (allow_frame, target_fps, observation_mode, priority)
        """
        if state == C1State.SUSPENDED:
            return False, 0, "none", "none"
        
        if state == C1State.ALERT:
            return True, 8, "local", "safety"
        
        if state == C1State.TRANSITION:
            return True, 4, "surround", "navigation"
        
        # STABLE（默认）
        return True, 2, "forward", "environment"
