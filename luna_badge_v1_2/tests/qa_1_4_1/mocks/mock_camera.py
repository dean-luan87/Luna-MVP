"""
摄像头模拟模块
用于测试中模拟摄像头行为
"""
import numpy as np
import time
from typing import Optional


class MockCamera:
    """模拟摄像头，用于测试"""
    
    def __init__(self, fps: float = 20.0, enabled: bool = True):
        """
        初始化模拟摄像头
        
        Args:
            fps: 帧率
            enabled: 是否启用
        """
        self.fps = fps
        self.enabled = enabled
        self.frame_count = 0
        self.last_frame_time = 0.0
        self.frame_interval = 1.0 / fps if fps > 0 else 0.0
    
    def read(self) -> tuple[bool, Optional[np.ndarray]]:
        """
        读取一帧（模拟）
        
        Returns:
            (success, frame)
        """
        if not self.enabled:
            return False, None
        
        now = time.time()
        if now - self.last_frame_time < self.frame_interval:
            return False, None
        
        # 生成模拟帧
        frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        self.frame_count += 1
        self.last_frame_time = now
        
        return True, frame
    
    def isOpened(self) -> bool:
        """检查摄像头是否打开"""
        return self.enabled
    
    def release(self) -> None:
        """释放摄像头"""
        self.enabled = False
    
    def pause(self) -> None:
        """暂停摄像头（模拟断流）"""
        self.enabled = False
    
    def resume(self) -> None:
        """恢复摄像头"""
        self.enabled = True

