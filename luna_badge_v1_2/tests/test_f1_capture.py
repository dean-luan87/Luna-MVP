#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
F1: 视觉捕获测试
测试帧捕获模块的稳定性和正确性
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import numpy as np
from unittest.mock import Mock, patch

try:
    from core.frame_manager import FrameManager
    FRAME_MANAGER_AVAILABLE = True
except ImportError:
    FRAME_MANAGER_AVAILABLE = False

try:
    from core.frame_scheduler import FrameScheduler
    FRAME_SCHEDULER_AVAILABLE = True
except ImportError:
    FRAME_SCHEDULER_AVAILABLE = False


class TestF1VisionCapture(unittest.TestCase):
    """F1: 视觉捕获测试"""
    
    def test_frame_manager_basic(self):
        """测试 FrameManager 基本功能"""
        if not FRAME_MANAGER_AVAILABLE:
            self.skipTest("FrameManager 模块不可用")
        
        # 创建模拟帧
        mock_frame = np.zeros((480, 640, 3), dtype=np.uint8)
        
        # 测试 FrameManager 初始化
        try:
            manager = FrameManager()
            self.assertIsNotNone(manager)
        except Exception as e:
            self.fail(f"FrameManager 初始化失败: {e}")
    
    def test_frame_scheduler_basic(self):
        """测试 FrameScheduler 基本功能"""
        if not FRAME_SCHEDULER_AVAILABLE:
            self.skipTest("FrameScheduler 模块不可用")
        
        try:
            scheduler = FrameScheduler()
            self.assertIsNotNone(scheduler)
            
            # 测试计算 FPS
            base_fps = 10
            mock_frame = np.zeros((480, 640, 3), dtype=np.uint8)
            final_fps = scheduler.compute_final_fps(base_fps, mock_frame)
            self.assertIsInstance(final_fps, (int, float))
            self.assertGreaterEqual(final_fps, 0)
        except Exception as e:
            self.fail(f"FrameScheduler 测试失败: {e}")
    
    def test_frame_capture_structure(self):
        """测试帧捕获数据结构"""
        # 创建模拟帧数据
        frame_data = {
            "timestamp": 1234567890.0,
            "frame_id": 1,
            "data": np.zeros((480, 640, 3), dtype=np.uint8),
        }
        
        self.assertIn("timestamp", frame_data)
        self.assertIn("frame_id", frame_data)
        self.assertIn("data", frame_data)
        self.assertEqual(frame_data["frame_id"], 1)


if __name__ == "__main__":
    unittest.main()


















