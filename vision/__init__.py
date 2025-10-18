#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Luna Vision 模块
计算机视觉功能集合
"""

__version__ = "1.0.0"
__author__ = "Luna Team"

# 延迟导入，避免依赖问题
def get_object_detector():
    """获取物体检测器"""
    from .object_detection import ObjectDetector
    return ObjectDetector

def get_camera_initializer():
    """获取摄像头初始化器"""
    from .init_camera import CameraInitializer
    return CameraInitializer

def get_ocr_reader():
    """获取OCR阅读器"""
    from .ocr_readout import OCRReader
    return OCRReader

def get_dynamic_tracker():
    """获取动态追踪器"""
    from .dynamic_tracking import DynamicTracker
    return DynamicTracker

def get_night_mode():
    """获取夜间模式"""
    from .night_mode import NightMode
    return NightMode

def get_video_stabilizer():
    """获取视频稳定器"""
    from .video_stabilization import VideoStabilizer
    return VideoStabilizer

def get_face_recognizer():
    """获取人脸识别器"""
    from .face_recognition import FaceRecognizer
    return FaceRecognizer

def get_risk_alert():
    """获取风险警报器"""
    from .risk_alert import RiskAlert
    return RiskAlert

def get_debug_overlay():
    """获取调试覆盖层"""
    from .debug_overlay import DebugOverlay
    return DebugOverlay

# 直接导入基础模块（无额外依赖）
try:
    from .object_detection import ObjectDetector
except ImportError:
    ObjectDetector = None

try:
    from .init_camera import CameraInitializer
except ImportError:
    CameraInitializer = None

__all__ = [
    'ObjectDetector',
    'CameraInitializer',
    'get_object_detector',
    'get_camera_initializer',
    'get_ocr_reader',
    'get_dynamic_tracker',
    'get_night_mode',
    'get_video_stabilizer',
    'get_face_recognizer',
    'get_risk_alert',
    'get_debug_overlay'
]
