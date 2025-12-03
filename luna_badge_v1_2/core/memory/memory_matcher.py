from core.logging import get_logger

log = get_logger("memory_matcher")
"""
MemoryMatcher（静态环境匹配器，1.3.0 MVP）

功能：
- 记录一个"记忆场景"的特征（Scene Signature）
- 与当前帧匹配，输出匹配度（0~1）

技术实现：
- ORB 提取关键点与描述子
- BFMatcher 匹配描述子
- 匹配数量归一化为匹配度

说明：
- 记忆场景可由上层主动设置，如 memory_matcher.set_memory(frame)
"""

import cv2
import numpy as np
from typing import Optional, Dict, Any


class MemoryMatcher:
    def __init__(self):
        # ORB: 轻量，高速，适合移动端
        self.orb = cv2.ORB_create(
            nfeatures=500,
            scaleFactor=1.2,
            nlevels=8
        )

        # 存储记忆场景签名
        self.memory_signature: Optional[Dict[str, Any]] = None

        # BFMatcher，使用 Hamming 距离（ORB 描述子用 Hamming）
        self.matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    # ----------------------------------------------------------- #
    # 记忆场景设置
    # ----------------------------------------------------------- #

    def set_memory(self, frame):
        """
        设置记忆场景：
        - 提取 ORB 关键点 & 描述子
        - 保存用于后续匹配
        """

        kp, des = self.orb.detectAndCompute(frame, None)

        if des is None:
            log.warning("[MemoryMatcher] Warning: memory frame has no descriptors.")
            return

        self.memory_signature = {
            "kp": kp,
            "des": des
        }

        log.info(f"[MemoryMatcher] Memory scene saved with {len(kp)} keypoints.")

    # ----------------------------------------------------------- #
    # 匹配当前帧与记忆场景
    # ----------------------------------------------------------- #

    def match(self, frame) -> float:
        """
        输入当前帧，返回与记忆场景的匹配度 0~1
        """
        if self.memory_signature is None:
            return 0.0

        memory_des = self.memory_signature["des"]

        # 提取当前帧的 ORB 描述子
        kp2, des2 = self.orb.detectAndCompute(frame, None)
        if des2 is None:
            return 0.0

        # 匹配
        matches = self.matcher.match(memory_des, des2)

        if len(matches) == 0:
            return 0.0

        # 简单评分：匹配数量归一化
        # 最大500，为 nfeatures 参数
        match_score = min(len(matches) / 500.0, 1.0)

        return float(match_score)










