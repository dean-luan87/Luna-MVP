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
    """摄像头处理器"""
    
    def __init__(self, camera_index: int = None, width: int = None, height: int = None):
        self.camera_index = camera_index or CAMERA_CONFIG['camera_index']
        self.width = width or CAMERA_CONFIG['width']
        self.height = height or CAMERA_CONFIG['height']
        self.cap = None
        self._initialize_camera()
    
    def _initialize_camera(self):
        """初始化摄像头"""
        import platform
        
        # 检查摄像头可用性
        self._check_camera_availability()
        
        # 尝试不同的摄像头初始化方式
        camera_initialized = False
        
        # 方法1: 尝试使用AVFoundation后端（Mac推荐）
        if platform.system() == 'Darwin':  # macOS
            try:
                logger.info("尝试使用AVFoundation后端初始化摄像头...")
                self.cap = cv2.VideoCapture(self.camera_index, cv2.CAP_AVFOUNDATION)
                if self.cap.isOpened():
                    camera_initialized = True
                    logger.info(f"AVFoundation后端摄像头初始化成功: {self.camera_index}")
                else:
                    self.cap.release()
                    self.cap = None
            except Exception as e:
                logger.warning(f"AVFoundation后端初始化失败: {e}")
                self.cap = None
        
        # 方法2: 尝试默认后端
        if not camera_initialized:
            try:
                logger.info("尝试使用默认后端初始化摄像头...")
                self.cap = cv2.VideoCapture(self.camera_index)
                if self.cap.isOpened():
                    camera_initialized = True
                    logger.info(f"默认后端摄像头初始化成功: {self.camera_index}")
                else:
                    self.cap.release()
                    self.cap = None
            except Exception as e:
                logger.warning(f"默认后端初始化失败: {e}")
                self.cap = None
        
        # 方法3: 尝试备用摄像头索引
        if not camera_initialized and self.camera_index == 0:
            try:
                logger.info("尝试使用备用摄像头索引...")
                self.cap = cv2.VideoCapture(1)
                if self.cap.isOpened():
                    camera_initialized = True
                    self.camera_index = 1
                    logger.info(f"备用摄像头初始化成功: {self.camera_index}")
                else:
                    self.cap.release()
                    self.cap = None
            except Exception as e:
                logger.warning(f"备用摄像头初始化失败: {e}")
                self.cap = None
        
        if not camera_initialized:
            logger.error("所有摄像头初始化方法都失败了")
            self.cap = None
            return
        
        # 设置摄像头参数
        try:
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
            self.cap.set(cv2.CAP_PROP_FPS, CAMERA_CONFIG['fps'])
            
            # 验证设置是否生效
            actual_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            actual_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            actual_fps = self.cap.get(cv2.CAP_PROP_FPS)
            
            logger.info(f"摄像头参数设置完成:")
            logger.info(f"  - 索引: {self.camera_index}")
            logger.info(f"  - 分辨率: {actual_width}x{actual_height}")
            logger.info(f"  - 帧率: {actual_fps:.1f} FPS")
            
        except Exception as e:
            logger.warning(f"摄像头参数设置失败: {e}")
    
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
        
        # 尝试检测可用的摄像头
        available_cameras = []
        for i in range(3):  # 检查前3个摄像头索引
            try:
                cap = cv2.VideoCapture(i)
                if cap.isOpened():
                    available_cameras.append(i)
                    cap.release()
            except:
                pass
        
        if available_cameras:
            logger.info(f"检测到可用摄像头: {available_cameras}")
        else:
            logger.warning("未检测到可用摄像头")
    
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
                logger.warning("无法读取摄像头帧")
                return None
            
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
