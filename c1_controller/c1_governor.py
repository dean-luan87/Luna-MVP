"""
C1 抽帧频率控制（Governor）

防止算力爆炸和完全失明。
"""

import time


class C1Governor:
    """
    C1 频率控制器
    
    职责：
    - 限制 fps 在合理范围内
    - 防止算力爆炸（MAX_FPS）
    - 防止完全失明（MIN_FPS）
    """
    
    MIN_FPS = 1
    MAX_FPS = 10
    
    @staticmethod
    def clamp_fps(fps: int) -> int:
        """
        限制 fps 在合理范围内
        
        Args:
            fps: 目标 fps
        
        Returns:
            限制后的 fps（在 [MIN_FPS, MAX_FPS] 范围内，但允许 0 表示暂停）
        """
        # 允许 0（表示暂停）
        if fps == 0:
            return 0
        return max(C1Governor.MIN_FPS, min(C1Governor.MAX_FPS, fps))


class FrameRateGovernor:
    """
    帧率控制器（轻量级）
    
    职责：
    - 根据 target_fps 控制是否允许处理当前帧
    - 不阻塞、不 sleep、不影响主循环
    - 丢帧是"自然行为"
    
    设计原则：
    - 摄像头仍然可以高频采集（避免硬件重连/抖动）
    - Pipeline 只按 target_fps 接收 frame
    - 不改 CameraHandler 的采集能力，只在"是否交付 frame"这一层做节流
    """
    
    def __init__(self):
        self._last_emit_ts = 0.0
    
    def allow(self, target_fps: int) -> bool:
        """
        判断是否允许处理当前帧
        
        Args:
            target_fps: 目标 fps（来自 C1Decision）
        
        Returns:
            如果允许处理当前帧，返回 True；否则返回 False
        """
        if target_fps <= 0:
            return False
        
        now = time.time()
        min_interval = 1.0 / target_fps
        
        if now - self._last_emit_ts >= min_interval:
            self._last_emit_ts = now
            return True
        
        return False
