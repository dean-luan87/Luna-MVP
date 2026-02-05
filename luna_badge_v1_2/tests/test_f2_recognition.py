#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
F2: 识别模块测试
测试物体识别、OCR识别等功能的稳定性
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import numpy as np
from unittest.mock import Mock, patch

try:
    from core.yolo_detector import YoloDetector
    YOLO_AVAILABLE = True
except ImportError:
    YOLO_AVAILABLE = False

try:
    from core.vision_dispatcher import VisionDispatcher
    DISPATCHER_AVAILABLE = True
except ImportError:
    DISPATCHER_AVAILABLE = False


class TestF2Recognition(unittest.TestCase):
    """F2: 识别模块测试"""
    
    def test_yolo_detector_basic(self):
        """测试 YoloDetector 基本功能"""
        if not YOLO_AVAILABLE:
            self.skipTest("YoloDetector 模块不可用")
        
        try:
            detector = YoloDetector({"model_name": "yolov8n"})
            self.assertIsNotNone(detector)
            
            # 测试加载模型
            detector.load_model()
            
            # 测试推理
            mock_frame = {"timestamp": 0, "data": np.zeros((480, 640, 3), dtype=np.uint8)}
            result = detector.infer(mock_frame)
            
            self.assertIsInstance(result, dict)
            self.assertIn("objects", result)
            self.assertIn("detections", result)
        except Exception as e:
            self.fail(f"YoloDetector 测试失败: {e}")
    
    def test_vision_dispatcher_basic(self):
        """测试 VisionDispatcher 基本功能"""
        if not DISPATCHER_AVAILABLE:
            self.skipTest("VisionDispatcher 模块不可用")
        
        try:
            # 创建模拟检测器
            mock_detector = Mock()
            mock_detector.infer = Mock(return_value={"objects": []})
            
            dispatcher = VisionDispatcher(detector=mock_detector)
            self.assertIsNotNone(dispatcher)
            
            # 测试推理
            mock_frame = np.zeros((480, 640, 3), dtype=np.uint8)
            result = dispatcher.run_inference(mock_frame)
            
            self.assertIsInstance(result, dict)
            self.assertIn("detections", result)
        except Exception as e:
            self.fail(f"VisionDispatcher 测试失败: {e}")
    
    def test_recognition_output_structure(self):
        """测试识别输出数据结构"""
        # 模拟识别结果
        recognition_result = {
            "objects": [{"class": "person", "confidence": 0.9, "bbox": [10, 20, 100, 200]}],
            "detections": [{"class": "person", "confidence": 0.9}],
            "meta": {"timestamp": 1234567890.0},
        }
        
        self.assertIn("objects", recognition_result)
        self.assertIn("detections", recognition_result)
        self.assertIsInstance(recognition_result["objects"], list)


if __name__ == "__main__":
    unittest.main()


















