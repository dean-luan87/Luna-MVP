#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的视频抽帧工具
"""

import cv2
import os
import logging

logger = logging.getLogger(__name__)


class VideoFrameExtractor:
    """
    简单的视频抽帧工具：
    - step: 每隔多少帧抽一帧
    - max_frames: 最多抽多少帧
    """

    def __init__(self, step=10, max_frames=30):
        self.step = step
        self.max_frames = max_frames

    def extract_frames(self, video_path):
        """
        从视频文件中提取帧
        
        Args:
            video_path: 视频文件路径
            
        Returns:
            list: 帧的字节列表（JPEG 格式）
        """
        if not os.path.exists(video_path):
            logger.warning(f"视频文件不存在: {video_path}")
            return []

        cap = cv2.VideoCapture(video_path)
        frames = []
        frame_idx = 0
        saved = 0

        if not cap.isOpened():
            logger.error(f"无法打开视频文件: {video_path}")
            return []

        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                if frame_idx % self.step == 0:
                    # 转成 JPEG bytes
                    ok, buf = cv2.imencode(".jpg", frame)
                    if ok:
                        frames.append(buf.tobytes())
                        saved += 1
                        if saved >= self.max_frames:
                            break

                frame_idx += 1
        finally:
            cap.release()

        logger.info(f"从视频 {video_path} 提取了 {len(frames)} 帧")
        return frames


