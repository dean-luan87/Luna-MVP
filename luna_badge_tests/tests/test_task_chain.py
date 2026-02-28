#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
任务链测试
测试连贯任务链的稳定性（1.3.0 新增）
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from unittest.mock import Mock

try:
    from core.task.task_chain import TaskChain
    TASK_CHAIN_AVAILABLE = True
except ImportError:
    TASK_CHAIN_AVAILABLE = False

try:
    from core.task_chain_manager import TaskChainManager
    TASK_CHAIN_MANAGER_AVAILABLE = True
except ImportError:
    TASK_CHAIN_MANAGER_AVAILABLE = False


class TestTaskChain(unittest.TestCase):
    """任务链测试"""
    
    def test_task_chain_basic(self):
        """测试 TaskChain 基本功能"""
        if not TASK_CHAIN_AVAILABLE:
            self.skipTest("TaskChain 模块不可用")
        
        try:
            chain = TaskChain("test_chain")
            self.assertIsNotNone(chain)
            self.assertEqual(chain.name, "test_chain")
            self.assertEqual(chain.state, "IDLE")
        except Exception as e:
            self.fail(f"TaskChain 初始化失败: {e}")
    
    def test_task_chain_state_transition(self):
        """测试任务链状态转换"""
        if not TASK_CHAIN_AVAILABLE:
            self.skipTest("TaskChain 模块不可用")
        
        try:
            chain = TaskChain("test_chain")
            
            # 测试状态转换
            chain.start()
            self.assertEqual(chain.state, "RUNNING")
            
            chain.pause()
            self.assertEqual(chain.state, "PAUSED")
            
            chain.resume()
            self.assertEqual(chain.state, "RUNNING")
            
            chain.complete()
            self.assertEqual(chain.state, "COMPLETED")
        except Exception as e:
            self.fail(f"TaskChain 状态转换测试失败: {e}")
    
    def test_task_chain_manager_basic(self):
        """测试 TaskChainManager 基本功能"""
        if not TASK_CHAIN_MANAGER_AVAILABLE:
            self.skipTest("TaskChainManager 模块不可用")
        
        try:
            manager = TaskChainManager()
            self.assertIsNotNone(manager)
        except Exception as e:
            self.fail(f"TaskChainManager 初始化失败: {e}")


if __name__ == "__main__":
    unittest.main()







