"""
C1 核心控制器（真正的 C1）

C1 只做一件事：
decision = C1Controller.decide(c1_input)

PipelineController 只依赖这个结果，其余一概不关心。
"""

from c1_controller.c1_state import C1State
from c1_controller.c1_types import C1Input, C1Decision
from c1_controller.c1_safety_guard import C1SafetyGuard
from c1_controller.c1_privacy_guard import C1PrivacyGuard
from c1_controller.c1_policy import C1Policy
from c1_controller.c1_governor import C1Governor


class C1Controller:
    """
    C1 主控制器
    
    职责：
    - 接收 C1Input，输出 C1Decision
    - 协调各个子模块（safety guard, privacy guard, policy, governor）
    - 管理状态转换
    """
    
    def __init__(self):
        self.state = C1State.STABLE
    
    def get_current_state(self) -> C1State:
        """
        获取当前状态（用于日志）
        
        Returns:
            当前 C1 状态
        """
        return self.state
    
    def decide(self, c1_input: C1Input) -> C1Decision:
        """
        C1 核心决策函数（唯一对外接口）
        
        PipelineController 只调用这个方法。
        
        决策流程：
        1. 隐私硬规则（最高优先级）
        2. 安全检查
        3. 策略决策
        4. 频率限制
        
        Args:
            c1_input: C1 输入信号
        
        Returns:
            C1Decision（是否允许抽帧、目标 fps、观察模式、优先级、原因）
        """
        # 1️⃣ 隐私硬规则
        if not C1PrivacyGuard.allow_camera(
            c1_input.privacy_zone,
            c1_input.user_camera_override
        ):
            self.state = C1State.SUSPENDED
            return C1Decision(
                allow_frame=False,
                target_fps=0,
                observation_mode="none",
                priority="none",
                reason="privacy_guard"
            )
        
        # 2️⃣ 安全检查
        safety_state = C1SafetyGuard.evaluate(
            c1_input.motion_score,
            c1_input.frame_diff_score
        )
        if safety_state:
            self.state = safety_state
        else:
            # 3️⃣ 状态转换（如果没有被安全阻断）
            # 优先级：ALERT > TRANSITION > STABLE
            if c1_input.risk_hint:
                self.state = C1State.ALERT
            elif c1_input.next_scene_hint:
                self.state = C1State.TRANSITION
            else:
                self.state = C1State.STABLE
        
        # 4️⃣ 策略决策
        allow, fps, mode, priority = C1Policy.decide(self.state)
        fps = C1Governor.clamp_fps(fps)
        
        return C1Decision(
            allow_frame=allow,
            target_fps=fps,
            observation_mode=mode,
            priority=priority,
            reason=self.state.value
        )
