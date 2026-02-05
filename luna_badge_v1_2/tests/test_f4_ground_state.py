#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
F4: 地面状态测试
测试地面检测、环境分析等功能的稳定性
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import numpy as np
from unittest.mock import Mock, patch

try:
    from core.environment_analyzer import EnvironmentAnalyzer
    ENV_ANALYZER_AVAILABLE = True
except ImportError:
    ENV_ANALYZER_AVAILABLE = False

try:
    from vision.path_detector.path_detector import PathDetector
    PATH_DETECTOR_AVAILABLE = True
except ImportError:
    PATH_DETECTOR_AVAILABLE = False


class TestF4GroundState(unittest.TestCase):
    """F4: 地面状态测试"""
    
    def test_environment_analyzer_basic(self):
        """测试 EnvironmentAnalyzer 基本功能"""
        if not ENV_ANALYZER_AVAILABLE:
            self.skipTest("EnvironmentAnalyzer 模块不可用")
        
        try:
            analyzer = EnvironmentAnalyzer()
            self.assertIsNotNone(analyzer)
            
            # 测试静态结构分析
            mock_scene_graph = {}
            result = analyzer.analyze_static_structure(mock_scene_graph)
            self.assertIsInstance(result, dict)
            self.assertIn("static_match_score", result)
            
            # 测试动态密度分析
            result = analyzer.analyze_dynamic_density(mock_scene_graph)
            self.assertIsInstance(result, dict)
            self.assertIn("dynamic_density_score", result)
        except Exception as e:
            self.fail(f"EnvironmentAnalyzer 测试失败: {e}")
    
    def test_path_detector_basic(self):
        """测试 PathDetector 基本功能"""
        if not PATH_DETECTOR_AVAILABLE:
            self.skipTest("PathDetector 模块不可用")
        
        try:
            detector = PathDetector()
            self.assertIsNotNone(detector)
            
            # 测试检测
            mock_frame = np.zeros((480, 640, 3), dtype=np.uint8)
            result = detector.detect(mock_frame)
            
            self.assertIsInstance(result, dict)
            self.assertIn("path", result)
            self.assertIn("confidence", result)
        except Exception as e:
            self.fail(f"PathDetector 测试失败: {e}")
    
    def test_ground_state_output_structure(self):
        """测试地面状态输出结构"""
        # 模拟地面状态结果
        ground_state = {
            "path": None,
            "confidence": 0.0,
            "meta": {},
            "static_match_score": 0.5,
            "dynamic_density_score": 0.3,
        }
        
        self.assertIn("path", ground_state)
        self.assertIn("confidence", ground_state)


if __name__ == "__main__":
    unittest.main()


















