"""
C1 安全兜底机制

⚠️ 注意：
SafetyGuard 只"建议状态"，不做最终决定。
"""

from c1_controller.c1_state import C1State


# 阈值定义
HARD_SHAKE_THRESHOLD = 0.85      # 严重晃动阈值
STATIC_FRAME_THRESHOLD = 0.02   # 可疑静态遮挡阈值


class C1SafetyGuard:
    """
    C1 安全守卫
    
    职责：
    - 检测严重晃动
    - 检测可疑静态遮挡
    - 返回状态建议（不做最终决定）
    """
    
    @staticmethod
    def evaluate(motion_score: float, frame_diff_score: float) -> C1State:
        """
        评估安全状态
        
        Args:
            motion_score: 镜头晃动强度（0~1）
            frame_diff_score: 帧变化幅度（0~1）
        
        Returns:
            如果检测到安全问题，返回建议的状态；否则返回 None
        """
        # 严重晃动：直接暂停视觉
        if motion_score >= HARD_SHAKE_THRESHOLD:
            return C1State.SUSPENDED
        
        # 可疑静态遮挡（长时间 frame diff 极低）
        if frame_diff_score <= STATIC_FRAME_THRESHOLD:
            return C1State.TRANSITION
        
        return None
