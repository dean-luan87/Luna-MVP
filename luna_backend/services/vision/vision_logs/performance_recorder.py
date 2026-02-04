"""
记录每帧视觉耗时、FPS、YOLO推理耗时等 (v1.2.0)
"""

import time
from typing import Dict, Any, List, Optional
from collections import deque
from utils.logger import vision_log


class PerformanceRecorder:
    """性能记录器"""
    
    def __init__(self, window_size: int = 30):
        """
        初始化性能记录器
        
        Args:
            window_size: 滑动窗口大小（用于计算平均FPS）
        """
        self.window_size = window_size
        self.last_time = time.time()
        self.fps = 0.0
        self.frame_times = deque(maxlen=window_size)
        self.inference_times = deque(maxlen=window_size)
        self.total_frames = 0
    
    def tick(self) -> float:
        """
        记录一帧的时间戳，返回当前FPS
        
        Returns:
            当前FPS
        """
        current = time.time()
        diff = current - self.last_time
        self.last_time = current
        
        if diff > 0:
            frame_fps = 1.0 / diff
            self.frame_times.append(diff)
            self.fps = sum(self.frame_times) / len(self.frame_times) if self.frame_times else 0.0
        else:
            self.fps = 0.0
        
        self.total_frames += 1
        
        return self.fps
    
    def record_inference(self, inference_time: float):
        """
        记录推理耗时
        
        Args:
            inference_time: 推理耗时（秒）
        """
        self.inference_times.append(inference_time)
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        获取性能指标
        
        Returns:
            性能指标字典
        """
        avg_inference = sum(self.inference_times) / len(self.inference_times) if self.inference_times else 0.0
        max_inference = max(self.inference_times) if self.inference_times else 0.0
        min_inference = min(self.inference_times) if self.inference_times else 0.0
        
        return {
            "fps": round(self.fps, 2),
            "total_frames": self.total_frames,
            "avg_frame_time_ms": round(sum(self.frame_times) / len(self.frame_times) * 1000, 2) if self.frame_times else 0.0,
            "avg_inference_time_ms": round(avg_inference * 1000, 2),
            "max_inference_time_ms": round(max_inference * 1000, 2),
            "min_inference_time_ms": round(min_inference * 1000, 2),
            "window_size": self.window_size
        }
    
    def reset(self):
        """重置性能记录器"""
        self.frame_times.clear()
        self.inference_times.clear()
        self.total_frames = 0
        self.fps = 0.0
        self.last_time = time.time()
        vision_log("PERF_RESET", {})



