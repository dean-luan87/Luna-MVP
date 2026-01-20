# vision_pipeline/b2/v03/debug_snapshot.py
# B2 v0.3 调试截图工具：变化前/后画面保存

import cv2
import os
from typing import Optional


class B2Snapshotter:
    """
    B2 v0.3 调试截图器
    - 在关键变化时保存变化前/后的画面
    - 用于人工审计和验证
    """
    
    def __init__(self, out_dir: str = "b2_snapshots"):
        """
        :param out_dir: 截图保存目录
        """
        self.out_dir = out_dir
        os.makedirs(out_dir, exist_ok=True)
    
    def _fmt_time(self, ts: float) -> str:
        """
        格式化时间戳为文件名友好的格式
        :param ts: 时间戳（秒）
        :return: 格式化的时间字符串，如 "03m15s"
        """
        mm = int(ts // 60)
        ss = int(ts % 60)
        return f"{mm:02d}m{ss:02d}s"
    
    def save(self, frame, ts: float, tag: str) -> str:
        """
        保存截图
        :param frame: OpenCV 图像（numpy array）
        :param ts: 时间戳（秒）
        :param tag: 标签（如 "BEFORE_DECISION"）
        :return: 保存的文件路径
        """
        name = f"{self._fmt_time(ts)}_{tag}.jpg"
        path = os.path.join(self.out_dir, name)
        cv2.imwrite(path, frame)
        return path

