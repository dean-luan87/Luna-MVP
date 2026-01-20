#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
v1.4.3 测试执行脚本
运行所有 v1.4.3 相关测试
"""

import sys
import os
import subprocess

# 添加项目路径
_script_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.normpath(os.path.join(_script_dir, '..'))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)


def run_tests():
    """运行所有 v1.4.3 测试"""
    test_files = [
        "test_inquiry_parser.py",
        "test_taskchain.py",
        "test_decision_core.py",
        "test_integration_flow.py",
        "test_scenarios.py",
    ]
    
    print("=" * 60)
    print("Luna Badge v1.4.3 测试套件")
    print("=" * 60)
    print()
    
    results = []
    for test_file in test_files:
        test_path = os.path.join(_script_dir, test_file)
        if not os.path.exists(test_path):
            print(f"⚠️  测试文件不存在: {test_file}")
            results.append((test_file, False))
            continue
        
        print(f"运行测试: {test_file}")
        print("-" * 60)
        
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pytest", test_path, "-v"],
                cwd=_project_root,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print(f"✅ {test_file} 通过")
                results.append((test_file, True))
            else:
                print(f"❌ {test_file} 失败")
                print(result.stdout)
                print(result.stderr)
                results.append((test_file, False))
        except Exception as e:
            print(f"❌ {test_file} 执行异常: {e}")
            results.append((test_file, False))
        
        print()
    
    # 总结
    print("=" * 60)
    print("测试总结")
    print("=" * 60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_file, success in results:
        status = "✅ 通过" if success else "❌ 失败"
        print(f"{test_file}: {status}")
    
    print()
    print(f"总计: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！")
        return 0
    else:
        print("⚠️  部分测试失败，请检查")
        return 1


if __name__ == "__main__":
    sys.exit(run_tests())













