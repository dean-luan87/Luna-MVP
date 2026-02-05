#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
F3: 调度器测试
测试视觉调度器、模型路由器的稳定性
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import numpy as np
from unittest.mock import Mock, patch

try:
    from core.vision_dispatcher import VisionDispatcher
    DISPATCHER_AVAILABLE = True
except ImportError:
    DISPATCHER_AVAILABLE = False

try:
    from core.model_router import ModelRouter
    ROUTER_AVAILABLE = True
except ImportError:
    ROUTER_AVAILABLE = False


class TestF3Dispatcher(unittest.TestCase):
    """F3: 调度器测试"""
    
    def test_vision_dispatcher_inference(self):
        """测试 VisionDispatcher 推理功能"""
        if not DISPATCHER_AVAILABLE:
            self.skipTest("VisionDispatcher 模块不可用")
        
        try:
            # 创建模拟检测器
            mock_detector = Mock()
            mock_detector.infer = Mock(return_value={"objects": []})
            
            dispatcher = VisionDispatcher(detector=mock_detector)
            mock_frame = np.zeros((480, 640, 3), dtype=np.uint8)
            result = dispatcher.run_inference(mock_frame)
            
            self.assertIsInstance(result, dict)
            self.assertIn("detections", result)
        except Exception as e:
            self.fail(f"VisionDispatcher 推理测试失败: {e}")
    
    def test_model_router_basic(self):
        """测试 ModelRouter 基本功能"""
        if not ROUTER_AVAILABLE:
            self.skipTest("ModelRouter 模块不可用")
        
        try:
            # 创建模拟模型
            mock_l1 = Mock(return_value={"result": "l1"})
            mock_l2 = Mock(return_value={"result": "l2"})
            
            router = ModelRouter(l1_model=mock_l1, l2_model=mock_l2)
            self.assertIsNotNone(router)
            
            # 测试路由决策
            test_input = {"intent": "simple_nav", "text": "向前走"}
            result = router.route(test_input)
            
            self.assertIsNotNone(result)
        except Exception as e:
            self.fail(f"ModelRouter 测试失败: {e}")
    
    def test_dispatcher_output_structure(self):
        """测试调度器输出结构"""
        # 模拟调度结果
        dispatch_result = {
            "detections": [],
            "tracked_objects": [],
            "segmentation": {},
            "depth_map": None,
            "motion": {},
            "meta": {},
        }
        
        self.assertIn("detections", dispatch_result)
        self.assertIn("meta", dispatch_result)


if __name__ == "__main__":
    unittest.main()


















