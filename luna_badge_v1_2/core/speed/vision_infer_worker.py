"""
Vision Inference Worker
1.4.1-speed.3: 独立推理线程
1.4.1-speed.4: 集成 ModelSwitcher
将 YOLO/OCR 推理从主线程剥离，实现非阻塞视觉处理
"""
import time
from typing import Optional, Any

import cv2
import numpy as np

from core.speed.worker_base import WorkerBase
from core.speed.speed_context import SpeedContext
from core.speed.model_switcher import ModelSwitcher
from core.health.metrics_collector import MetricsCollector


class VisionInferWorker(WorkerBase):
    """
    独立推理线程
    
    功能：
    - 不负责摄像头采集
    - 只从 SpeedContext.camera_worker 读取最新帧
    - 执行 YOLO 推理（通过 ModelSwitcher）
    - 推理结果写入 SpeedContext（共享状态）
    - 自动丢弃旧帧，只处理最新帧
    """
    
    def __init__(self, heavy_model: Any, light_model: Optional[Any] = None, infer_interval: float = 0.1):
        """
        初始化推理 Worker
        
        Args:
            heavy_model: 重型模型（高精度）
            light_model: 轻型模型（快速），可选
            infer_interval: 推理间隔（秒），默认 0.1 秒（10 FPS）
        """
        super().__init__("VisionInferWorker")
        self.switcher = ModelSwitcher(heavy_model, light_model)
        self.infer_interval = infer_interval
        self.last_infer_ts = 0.0
        self.infer_count = 0
        self.error_count = 0

    def loop(self) -> None:
        """Worker 主循环"""
        # 获取摄像头最新帧
        camera_worker = SpeedContext.camera_worker
        
        if camera_worker is None:
            time.sleep(0.02)
            return

        # 检查是否有最近的帧
        if not camera_worker.buffer.has_recent_frame(timeout=0.5):
            time.sleep(0.01)
            return

        # 帧率控制
        now = time.time()
        if now - self.last_infer_ts < self.infer_interval:
            time.sleep(0.005)
            return

        # 获取最新帧（带元数据）
        frame, ts, seq = camera_worker.buffer.read_latest_meta()
        if frame is None:
            time.sleep(0.01)
            return

        # YOLO 推理（通过 ModelSwitcher）
        try:
            with MetricsCollector.timeit("vision_infer.yolo"):
                results = self.switcher.infer(frame)

            # 写入 SpeedContext（共享状态）
            SpeedContext.set_yolo_result(results, self.switcher.active_name)

            MetricsCollector.incr("vision_infer.frames")
            self.infer_count += 1
            self.last_infer_ts = SpeedContext.last_yolo_ts
            self.error_count = 0  # 重置错误计数

        except Exception as e:
            self.logger.exception(f"YOLO inference error: {e}")
            self.error_count += 1
            MetricsCollector.incr("vision_infer.errors")
            
            # 如果连续错误过多，短暂休眠
            if self.error_count > 10:
                time.sleep(0.1)

    def get_stats(self) -> dict:
        """
        获取统计信息
        
        Returns:
            包含推理次数、错误数等统计信息的字典
        """
        switcher_stats = self.switcher.get_stats()
        return {
            "infer_count": self.infer_count,
            "error_count": self.error_count,
            "last_infer_ts": self.last_infer_ts,
            "has_recent_result": (
                SpeedContext.last_yolo_ts > 0 and
                (time.time() - SpeedContext.last_yolo_ts) < 1.0
            ),
            **switcher_stats,
        }

