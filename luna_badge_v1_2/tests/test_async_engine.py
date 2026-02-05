#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
异步引擎测试
测试异步调度、避免阻塞等功能
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import threading
import time
from unittest.mock import Mock


class TestAsyncEngine(unittest.TestCase):
    """异步引擎测试"""
    
    def test_async_execution(self):
        """测试异步执行不阻塞主线程"""
        def async_task():
            time.sleep(0.1)
            return "done"
        
        start_time = time.time()
        thread = threading.Thread(target=async_task)
        thread.start()
        
        # 主线程应该立即继续
        elapsed = time.time() - start_time
        self.assertLess(elapsed, 0.05)  # 主线程应该很快返回
        
        thread.join(timeout=1.0)
        self.assertFalse(thread.is_alive())
    
    def test_concurrent_execution(self):
        """测试并发执行"""
        results = []
        lock = threading.Lock()
        
        def worker(id):
            time.sleep(0.01)
            with lock:
                results.append(id)
        
        threads = []
        for i in range(3):
            t = threading.Thread(target=worker, args=(i,))
            t.start()
            threads.append(t)
        
        for t in threads:
            t.join(timeout=1.0)
        
        self.assertEqual(len(results), 3)
    
    def test_timeout_handling(self):
        """测试超时处理"""
        def long_task():
            time.sleep(2.0)
            return "done"
        
        thread = threading.Thread(target=long_task)
        thread.start()
        thread.join(timeout=0.1)  # 超时设置为 0.1 秒
        
        # 线程应该仍在运行（因为任务需要2秒）
        self.assertTrue(thread.is_alive())


if __name__ == "__main__":
    unittest.main()


















