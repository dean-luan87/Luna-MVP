# -*- coding: utf-8 -*-
"""
摄像头处理模块
"""

import cv2
import numpy as np
import logging
from typing import Optional, Tuple

# 配置导入
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import CAMERA_CONFIG

logger = logging.getLogger(__name__)


class CameraHandler:
    """摄像头处理器（支持摄像头索引或视频文件路径）"""

    def __init__(
        self,
        camera_index: int = None,
        video_path: Optional[str] = None,
        width: int = None,
        height: int = None,
    ):
        self.video_path = video_path
        self.camera_index = camera_index if camera_index is not None else CAMERA_CONFIG["camera_index"]
        self.width = width or CAMERA_CONFIG['width']
        self.height = height or CAMERA_CONFIG['height']
        self.cap = None
        self.backend_name = CAMERA_CONFIG.get("camera_backend", "default")
        self._video_ended = False  # 视频文件读完后为 True
        self._video_frame_count = 0  # 已从视频读取的帧数（用于确认日志节流）
        self._initialize_camera()

    def _initialize_camera(self):
        """初始化摄像头或打开视频文件"""
        if self.video_path:
            self._open_video()
        else:
            self._open_camera()

    def _open_video(self):
        """从视频文件打开"""
        logger.info("从视频文件打开: %s", self.video_path)
        self.cap = cv2.VideoCapture(self.video_path)
        if not self.cap or not self.cap.isOpened():
            if self.cap:
                self.cap.release()
            self.cap = None
            logger.error("视频文件打开失败: %s", self.video_path)
            return
        w = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        logger.info("视频打开成功: %s, %dx%d, %.1f FPS", self.video_path, w, h, fps)

    def _open_camera(self):
        """初始化物理摄像头"""
        import platform

        self._check_camera_availability()

        if platform.system() == "Darwin" and self.backend_name == "avfoundation":
            logger.info("使用AVFoundation后端初始化摄像头...")
            self.cap = cv2.VideoCapture(self.camera_index, cv2.CAP_AVFOUNDATION)
        else:
            logger.info("使用默认后端初始化摄像头...")
            self.cap = cv2.VideoCapture(self.camera_index)

        if not self.cap or not self.cap.isOpened():
            if self.cap:
                self.cap.release()
            self.cap = None
            logger.error(f"摄像头初始化失败: index={self.camera_index}, backend={self.backend_name}")
            return
        logger.info(f"摄像头初始化成功: index={self.camera_index}, backend={self.backend_name}")

        try:
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
            self.cap.set(cv2.CAP_PROP_FPS, CAMERA_CONFIG['fps'])

            actual_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            actual_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            actual_fps = self.cap.get(cv2.CAP_PROP_FPS)

            logger.info("摄像头参数设置完成:")
            logger.info("  - 索引: %s", self.camera_index)
            logger.info("  - 分辨率: %dx%d", actual_width, actual_height)
            logger.info("  - 帧率: %.1f FPS", actual_fps)

        except Exception as e:
            logger.warning("摄像头参数设置失败: %s", e)
    
    def _check_camera_availability(self):
        """检查摄像头可用性"""
        import platform
        
        logger.info("检查摄像头可用性...")
        
        # 检查系统平台
        system = platform.system()
        logger.info(f"操作系统: {system}")
        
        # 检查OpenCV版本
        logger.info(f"OpenCV版本: {cv2.__version__}")
        
        # 检查可用的摄像头后端
        backends = []
        if hasattr(cv2, 'CAP_AVFOUNDATION'):
            backends.append("AVFoundation")
        if hasattr(cv2, 'CAP_V4L2'):
            backends.append("V4L2")
        if hasattr(cv2, 'CAP_DSHOW'):
            backends.append("DirectShow")
        
        logger.info(f"可用的摄像头后端: {', '.join(backends) if backends else '无'}")
        
        # 不自动探测摄像头索引，避免隐式 fallback
        logger.info(f"使用摄像头索引: {self.camera_index}")
    
    def read_frame(self) -> Optional[np.ndarray]:
        """
        读取一帧图像
        
        Returns:
            图像数据，如果失败返回None
        """
        if self.cap is None:
            logger.warning("摄像头未初始化")
            return None
        
        try:
            ret, frame = self.cap.read()
            if not ret:
                if self.video_path:
                    self._video_ended = True
                    logger.info("视频已播放完毕")
                else:
                    logger.warning("无法读取摄像头帧")
                return None

            # 确认使用视频帧：每 30 帧打一次 INFO，便于确认输入源是视频而非摄像头
            if self.video_path:
                self._video_frame_count += 1
                pos = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
                if self._video_frame_count == 1:
                    msg = "输入源=视频文件，正在使用视频帧 | 首帧 shape=%s 路径=%s" % (frame.shape, self.video_path)
                    logger.info(msg)
                    print("[视频确认] " + msg)  # 无条件打印，确保终端可见
                elif self._video_frame_count % 30 == 0:
                    logger.info("从视频读帧 #%d (pos=%d) shape=%s", self._video_frame_count, pos, frame.shape)

            return frame
        except Exception as e:
            logger.error(f"读取摄像头帧失败: {e}")
            return None
    
    def get_frame_size(self) -> Tuple[int, int]:
        """
        获取帧尺寸
        
        Returns:
            (宽度, 高度)
        """
        if self.cap is None:
            return (0, 0)
        
        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        return (width, height)
    
    def get_fps(self) -> float:
        """
        获取输入源帧率（视频文件返回视频 FPS，摄像头返回配置/实际 FPS）。

        Returns:
            帧率，无法获取时返回 0
        """
        if self.cap is None or not self.cap.isOpened():
            return 0.0
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        return float(fps) if fps and fps > 0 else (float(CAMERA_CONFIG.get("fps", 30)) if not self.video_path else 0.0)

    def is_opened(self) -> bool:
        """
        检查摄像头是否打开

        Returns:
            是否打开
        """
        return self.cap is not None and self.cap.isOpened()
    
    def release(self):
        """释放摄像头资源"""
        if self.cap is not None:
            self.cap.release()
            logger.info("摄像头资源已释放")
    
    def __del__(self):
        """析构函数"""
        self.release()
