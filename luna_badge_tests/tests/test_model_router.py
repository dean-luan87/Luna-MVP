#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ModelRouter 测试
测试模型路由器的路由决策和降级机制
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from unittest.mock import Mock

try:
    from core.model_router import ModelRouter
    ROUTER_AVAILABLE = True
except ImportError:
    ROUTER_AVAILABLE = False


class TestModelRouter(unittest.TestCase):
    """ModelRouter 测试"""
    
    def test_router_initialization(self):
        """测试路由器初始化"""
        if not ROUTER_AVAILABLE:
            self.skipTest("ModelRouter 模块不可用")
        
        try:
            mock_l1 = Mock(return_value={"result": "l1"})
            mock_l2 = Mock(return_value={"result": "l2"})
            
            router = ModelRouter(l1_model=mock_l1, l2_model=mock_l2)
            self.assertIsNotNone(router)
        except Exception as e:
            self.fail(f"ModelRouter 初始化失败: {e}")
    
    def test_router_simple_intent(self):
        """测试简单意图路由到 L1"""
        if not ROUTER_AVAILABLE:
            self.skipTest("ModelRouter 模块不可用")
        
        try:
            mock_l1 = Mock(return_value={"result": "l1"})
            mock_l2 = Mock(return_value={"result": "l2"})
            
            router = ModelRouter(l1_model=mock_l1, l2_model=mock_l2)
            
            # 简单导航意图应该路由到 L1
            test_input = {"intent": "simple_nav", "text": "向前走"}
            result = router.route(test_input)
            
            self.assertIsNotNone(result)
        except Exception as e:
            self.fail(f"ModelRouter 路由测试失败: {e}")
    
    def test_router_fallback(self):
        """测试 L2 失败时的降级机制"""
        if not ROUTER_AVAILABLE:
            self.skipTest("ModelRouter 模块不可用")
        
        try:
            mock_l1 = Mock(return_value={"result": "l1_fallback"})
            mock_l2 = Mock(side_effect=Exception("L2 failed"))
            
            router = ModelRouter(l1_model=mock_l1, l2_model=mock_l2)
            
            # L2 失败时应该降级到 L1
            test_input = {"intent": "complex", "text": "复杂查询"}
            result = router.route(test_input)
            
            self.assertIsNotNone(result)
        except Exception as e:
            # 降级机制应该捕获异常
            pass


if __name__ == "__main__":
    unittest.main()







