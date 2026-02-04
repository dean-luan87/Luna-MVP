#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视频帧提取器
从视频中提取帧用于测试
"""

import cv2
import io
import os
import tempfile
import logging

logger = logging.getLogger(__name__)


class VideoFrameExtractor:
    """视频帧提取器"""
    
    @staticmethod
    def iter_frames_from_bytes(video_bytes, step=15, max_frames=50):
        """
        从视频 bytes 中每隔 step 帧取一帧，最多 max_frames 张。
        
        Args:
            video_bytes: 视频文件的字节数据
            step: 每隔多少帧取一帧
            max_frames: 最多提取多少帧
        
        Returns:
            list[np.ndarray]: 提取的帧列表
        """
        # 创建临时文件
        tmp_path = None
        try:
            with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp:
                tmp.write(video_bytes)
                tmp_path = tmp.name
            
            cap = cv2.VideoCapture(tmp_path)
            frames = []
            idx = 0
            ok, frame = cap.read()
            
            while ok and len(frames) < max_frames:
                if idx % step == 0:
                    frames.append(frame.copy())
                idx += 1
                ok, frame = cap.read()
            
            cap.release()
            
            logger.info(f"从视频中提取了 {len(frames)} 帧（step={step}, max_frames={max_frames}）")
            return frames
        except Exception as e:
            logger.error(f"视频帧提取失败: {e}")
            return []
        finally:
            # 清理临时文件
            if tmp_path and os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except Exception as e:
                    logger.warning(f"删除临时文件失败: {e}")


