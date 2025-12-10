# brightness_meter.py
import cv2
import numpy as np


class BrightnessMeter:
    """
    从单帧图像提取基础亮度指标：
    - 平均亮度 Y
    - Y 分布（供直方图分析器使用）
    """

    def __init__(self):
        pass

    def compute_luma(self, frame):
        """
        输入：RGB/BGR 帧
        输出：平均亮度值 Y（0~255）
        """
        if frame is None:
            return 0

        # 如果是 BGR 则先转换
        if len(frame.shape) == 3 and frame.shape[2] == 3:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Y = 0.299R + 0.587G + 0.114B
        R = frame[:, :, 0].astype(np.float32)
        G = frame[:, :, 1].astype(np.float32)
        B = frame[:, :, 2].astype(np.float32)
        Y = 0.299 * R + 0.587 * G + 0.114 * B

        mean_luma = float(np.mean(Y))
        return mean_luma














