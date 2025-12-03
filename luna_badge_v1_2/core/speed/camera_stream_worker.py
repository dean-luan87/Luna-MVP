"""
Camera Stream Worker
1.4.1-speed.2: 摄像头独立采集线程
将摄像头捕获从主线程剥离，使帧率不受 YOLO/OCR 或导航逻辑影响
"""
import time
from typing import Optional

import cv2
import numpy as np

from core.speed.worker_base import WorkerBase
from core.speed.vision_buffer import VisionBuffer
from core.health.metrics_collector import MetricsCollector


class CameraStreamWorker(WorkerBase):
    """
    摄像头采集 Worker
    
    功能：
    - 独立线程持续采集摄像头帧
    - 写入 RingBuffer 供其他模块使用
    - 帧率控制（FPS limit）
    - 自动重连机制
    """
    
    def __init__(self, cam_index: int = 0, fps_limit: int = 20):
        """
        初始化摄像头采集 Worker
        
        Args:
            cam_index: 摄像头索引（默认 0）
            fps_limit: 帧率限制（默认 20 FPS）
        """
        super().__init__("CameraStreamWorker")
        self.cam_index = cam_index
        self.fps_limit = fps_limit
        self.buffer = VisionBuffer(size=3)
        self.cap: Optional[cv2.VideoCapture] = None
        self.last_capture_ts = 0.0
        self.frame_count = 0
        self.error_count = 0
        self._camera_initialized = False

    def init_camera(self) -> bool:
        """
        初始化摄像头
        
        Returns:
            True 如果成功，False 否则
        """
        try:
            if self.cap is not None:
                self.cap.release()
            
            self.cap = cv2.VideoCapture(self.cam_index)
            if not self.cap.isOpened():
                self.logger.error(f"Camera {self.cam_index} failed to open")
                self._camera_initialized = False
                return False
            else:
                self.logger.info(f"Camera {self.cam_index} initialized (FPS limit: {self.fps_limit})")
                self._camera_initialized = True
                return True
        except Exception as e:
            self.logger.exception(f"Camera initialization error: {e}")
            self._camera_initialized = False
            return False

    def loop(self) -> None:
        """Worker 主循环"""
        # 如果摄像头未初始化，尝试初始化
        if not self._camera_initialized or self.cap is None:
            if not self.init_camera():
                time.sleep(0.1)  # 等待后重试
                return

        # 帧率控制
        now = time.time()
        frame_interval = 1.0 / self.fps_limit
        if now - self.last_capture_ts < frame_interval:
            time.sleep(0.005)  # 短暂休眠，避免 CPU 占用过高
            return

        # 采集帧
        try:
            with MetricsCollector.timeit("camera_stream.capture"):
                ret, frame = self.cap.read()

            if not ret or frame is None:
                self.logger.warning("Camera returned empty frame")
                self.error_count += 1
                MetricsCollector.incr("camera_stream.errors")
                # 如果连续错误，尝试重新初始化
                if self.error_count > 10:
                    self.logger.warning("Too many errors, reinitializing camera...")
                    self._camera_initialized = False
                    self.error_count = 0
                return

            # 写入缓冲区
            self.buffer.write(frame)
            self.last_capture_ts = now
            self.frame_count += 1
            self.error_count = 0  # 重置错误计数
            MetricsCollector.incr("camera_stream.frames")

        except Exception as e:
            self.logger.exception(f"Camera capture error: {e}")
            self.error_count += 1
            MetricsCollector.incr("camera_stream.errors")
            time.sleep(0.1)  # 错误后短暂休眠

    def stop_worker(self) -> None:
        """停止 Worker 并释放摄像头"""
        super().stop_worker()
        if self.cap is not None:
            try:
                self.cap.release()
                self.logger.info("Camera released")
            except Exception as e:
                self.logger.exception(f"Error releasing camera: {e}")
            finally:
                self.cap = None
                self._camera_initialized = False

    def get_stats(self) -> dict:
        """
        获取统计信息
        
        Returns:
            包含帧数、错误数等统计信息的字典
        """
        return {
            "frame_count": self.frame_count,
            "error_count": self.error_count,
            "buffer_write_count": self.buffer.get_write_count(),
            "has_recent_frame": self.buffer.has_recent_frame(),
            "camera_initialized": self._camera_initialized,
        }

