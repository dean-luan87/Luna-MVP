"""
MovementEstimator（用户移动速度估计，1.3.0 MVP）

实现方式：
- 使用光流法（Farneback）计算连续两帧之间的流动强度
- 将平均光流向量长度映射为速度等级

输出：
- "fast"
- "normal"
- "slow"
- "still"
"""

import cv2
import numpy as np


class MovementEstimator:
    def __init__(self, resize_w=160, resize_h=120):
        self.prev_gray = None
        self.resize_w = resize_w
        self.resize_h = resize_h

    # --------------------------------------------------------- #
    # 主入口
    # --------------------------------------------------------- #

    def get_speed(self, frame) -> str:
        """
        输入：BGR frame
        输出：速度等级字符串
        """

        # 1. 转灰度 & 降分辨率
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_small = cv2.resize(gray, (self.resize_w, self.resize_h))

        # 2. 若没有上一帧，则保存并返回 still
        if self.prev_gray is None:
            self.prev_gray = gray_small
            return "still"

        # 3. 计算光流
        flow = cv2.calcOpticalFlowFarneback(
            self.prev_gray, gray_small,
            None,
            0.5, 3, 15, 3, 5, 1.2, 0
        )

        self.prev_gray = gray_small

        # flow 是 (h, w, 2) → 每个像素一个光流向量 (vx, vy)
        mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])

        # 4. 计算平均光流模长
        mean_mag = float(np.mean(mag))

        # 5. 光流大小 → 速度等级映射
        if mean_mag < 0.3:
            return "still"
        elif mean_mag < 1.0:
            return "slow"
        elif mean_mag < 3.0:
            return "normal"
        else:
            return "fast"

























