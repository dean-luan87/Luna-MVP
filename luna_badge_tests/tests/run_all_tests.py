#!/usr/bin/env python3
"""
运行所有测试的入口脚本
"""
import sys
import unittest
from pathlib import Path

# 添加项目根目录到路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


def discover_and_run_tests():
    """发现并运行所有测试"""
    # 测试目录
    test_dir = Path(__file__).parent
    
    # 使用 unittest 的 TestLoader 发现所有测试
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 发现各个测试目录中的测试
    for test_subdir in ['unit_tests', 'integration_tests', 'vision_tests', 'navigation_tests']:
        subdir = test_dir / test_subdir
        if subdir.exists():
            tests = loader.discover(str(subdir), pattern='test_*.py')
            suite.addTests(tests)
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 返回退出码
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    exit_code = discover_and_run_tests()
    sys.exit(exit_code)





