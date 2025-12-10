#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一键运行所有测试脚本
"""

import sys
import os
import subprocess
import time

# 添加项目路径
_script_dir = os.path.dirname(os.path.abspath(__file__))
if _script_dir not in sys.path:
    sys.path.insert(0, _script_dir)


def run_test(script_name, description):
    """运行单个测试脚本"""
    print("\n" + "=" * 60)
    print(f"===== {description} =====")
    print("=" * 60)
    print(f"执行脚本: {script_name}")
    print("-" * 60)
    
    script_path = os.path.join(_script_dir, script_name)
    if not os.path.exists(script_path):
        print(f"❌ 脚本不存在: {script_path}")
        return False
    
    try:
        result = subprocess.run(
            [sys.executable, script_path],
            cwd=_script_dir,
            capture_output=False,
            text=True
        )
        if result.returncode == 0:
            print(f"✅ {description} 完成")
            return True
        else:
            print(f"❌ {description} 失败 (退出码: {result.returncode})")
            return False
    except Exception as e:
        print(f"❌ 执行失败: {e}")
        return False


def main():
    print("\n" + "=" * 60)
    print("===== 自动开始执行 1.4.2a 语音系统测试 =====")
    print("=" * 60)
    
    tests = [
        ("modules/test_voice_av.py", "1. 语音底层测试"),
        ("modules/test_main_events.py", "2. 主程序播报链模拟"),
        ("modules/test_guard_chain.py", "3. TTSGuard × 播报链联测"),
    ]
    
    results = []
    for script, desc in tests:
        success = run_test(script, desc)
        results.append((desc, success))
        time.sleep(2)  # 测试间隔
    
    print("\n" + "=" * 60)
    print("===== 测试总结 =====")
    print("=" * 60)
    for desc, success in results:
        status = "✅ 通过" if success else "❌ 失败"
        print(f"{desc}: {status}")
    
    all_passed = all(success for _, success in results)
    if all_passed:
        print("\n🎉 所有测试执行结束，请检查实际语音播放与日志输出结果。")
    else:
        print("\n⚠️  部分测试失败，请检查日志。")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())


