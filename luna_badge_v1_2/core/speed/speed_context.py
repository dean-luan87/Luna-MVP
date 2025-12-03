"""
Speed Engine 共享上下文
1.4.1-speed.1: 线程基础框架
1.4.1-speed.2: 添加 CameraStreamWorker 支持
"""
from typing import Literal, Optional

SpeedMode = Literal["normal", "fast", "safe"]


class SpeedContext:
    """
    SpeedEngine 的共享上下文，包括线程运行状态、模式等。
    1.4.1-speed.1 仅作为占位，将在 speed.4 扩展。
    1.4.1-speed.2 添加 CameraStreamWorker 支持。
    """
    
    speed_mode: SpeedMode = "normal"  # normal, fast, safe
    camera_worker: Optional[object] = None  # CameraStreamWorker 实例
    
    # 1.4.1-speed.3: 推理结果共享状态
    current_yolo_result: Optional[Any] = None  # 当前 YOLO 推理结果
    last_yolo_ts: float = 0.0  # 最后一次推理时间戳

    @staticmethod
    def set_mode(mode: SpeedMode):
        """
        设置速度模式
        
        Args:
            mode: 速度模式（normal, fast, safe）
        """
        SpeedContext.speed_mode = mode

    @staticmethod
    def get_mode() -> SpeedMode:
        """
        获取当前速度模式
        
        Returns:
            当前速度模式
        """
        return SpeedContext.speed_mode

    @staticmethod
    def set_camera_worker(worker):
        """
        设置 CameraStreamWorker 实例
        
        Args:
            worker: CameraStreamWorker 实例
        """
        SpeedContext.camera_worker = worker

    @staticmethod
    def get_latest_frame():
        """
        获取最新帧（从 CameraStreamWorker 的 buffer）
        
        Returns:
            最新的图像帧，如果没有则返回 None
        """
        if SpeedContext.camera_worker is None:
            return None
        return SpeedContext.camera_worker.buffer.read_latest()

