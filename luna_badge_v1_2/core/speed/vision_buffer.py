"""
Vision RingBuffer
1.4.1-speed.2: 摄像头采集线程的环形缓冲区
1.4.1-speed.4: 升级支持帧序号和新鲜度
用于 CameraStreamWorker -> VisionInferWorker 的帧传递
"""
import threading
import time
from typing import Optional, Tuple
import numpy as np


class VisionBuffer:
    """
    固定容量的环形缓冲区，用于 CameraStreamWorker -> VisionInferWorker
    
    特性：
    - 线程安全
    - 固定容量（避免内存无限增长）
    - 始终保留最新帧
    - 支持超时检测
    - 1.4.1-speed.4: 支持帧序号和元数据
    """
    
    def __init__(self, size: int = 3):
        """
        初始化环形缓冲区
        
        Args:
            size: 缓冲区大小（建议 3，保留最近 3 帧）
        """
        self.size = size
        self.buffer: list[Optional[dict]] = [None] * size
        self.index = 0
        self.lock = threading.Lock()
        self.last_write_ts = 0.0
        self.last_seq = 0
        self.write_count = 0

    def write(self, frame: np.ndarray) -> None:
        """
        写入新帧（覆盖最旧的帧）
        
        Args:
            frame: 图像帧（numpy array）
        """
        with self.lock:
            self.last_seq += 1
            self.buffer[self.index] = {
                "frame": frame.copy() if frame is not None else None,
                "ts": time.time(),
                "seq": self.last_seq,
            }
            self.index = (self.index + 1) % self.size
            self.last_write_ts = self.buffer[(self.index - 1) % self.size]["ts"]
            self.write_count += 1

    def read_latest(self) -> Optional[np.ndarray]:
        """
        读取最新帧
        
        Returns:
            最新的图像帧，如果没有帧则返回 None
        """
        with self.lock:
            latest_index = (self.index - 1) % self.size
            slot = self.buffer[latest_index]
            if slot is None:
                return None
            frame = slot["frame"]
            if frame is not None:
                return frame.copy()
            return None

    def read_latest_meta(self) -> Tuple[Optional[np.ndarray], float, int]:
        """
        返回 (frame, ts, seq)，供高级逻辑使用
        
        Returns:
            (frame, timestamp, sequence_number)
        """
        with self.lock:
            latest_index = (self.index - 1) % self.size
            slot = self.buffer[latest_index]
            if slot is None:
                return None, 0.0, 0
            frame = slot["frame"]
            if frame is not None:
                return frame.copy(), slot["ts"], slot["seq"]
            return None, slot["ts"], slot["seq"]

    def has_recent_frame(self, timeout: float = 0.5) -> bool:
        """
        检查是否有最近的帧（在超时时间内）
        
        Args:
            timeout: 超时时间（秒），默认 0.5 秒
        
        Returns:
            True 如果有最近的帧，False 否则
        """
        with self.lock:
            if self.last_write_ts == 0:
                return False
            return (time.time() - self.last_write_ts) < timeout

    def get_write_count(self) -> int:
        """获取写入帧的总数"""
        with self.lock:
            return self.write_count

    def get_latest_seq(self) -> int:
        """获取最新帧的序号"""
        with self.lock:
            return self.last_seq

    def clear(self) -> None:
        """清空缓冲区"""
        with self.lock:
            self.buffer = [None] * self.size
            self.index = 0
            self.last_write_ts = 0.0
            self.last_seq = 0
            self.write_count = 0

