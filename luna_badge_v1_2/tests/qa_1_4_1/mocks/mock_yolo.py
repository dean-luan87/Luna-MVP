"""
YOLO 模型模拟模块
用于测试中模拟 YOLO 推理行为
"""
import time
from typing import Any, Optional


class MockYOLODetector:
    """模拟 YOLO 检测器，用于测试"""
    
    def __init__(self, latency_ms: float = 50.0, enabled: bool = True):
        """
        初始化模拟 YOLO 检测器
        
        Args:
            latency_ms: 模拟推理延迟（毫秒）
            enabled: 是否启用
        """
        self.latency_ms = latency_ms
        self.enabled = enabled
        self.infer_count = 0
        self.last_infer_time = 0.0
    
    def detect(self, image: Any) -> Any:
        """
        执行检测（模拟）
        
        Args:
            image: 输入图像
        
        Returns:
            检测结果
        """
        if not self.enabled:
            return None
        
        # 模拟推理延迟
        time.sleep(self.latency_ms / 1000.0)
        
        self.infer_count += 1
        self.last_infer_time = time.time()
        
        # 返回模拟结果
        from core.yolo_detector import DetectionResult
        return DetectionResult(boxes=[])
    
    def pause(self) -> None:
        """暂停推理（模拟超时）"""
        self.enabled = False
    
    def resume(self) -> None:
        """恢复推理"""
        self.enabled = True





