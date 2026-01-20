#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
V1.8.1 快速回滚等价性验证脚本

用途：快速验证 observer_mode=false 时的基本等价性
注意：这是辅助脚本，不能替代完整测试
"""

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def check_observer_mode_defaults():
    """检查 observer_mode 默认值是否正确"""
    print("=" * 70)
    print("TC-06 快速验证: observer_mode 默认值检查")
    print("=" * 70)
    print()
    
    # 检查 Task 数据类
    task_file = "Luna_Badge/core/task_chain_manager.py"
    if os.path.exists(task_file):
        with open(task_file, "r", encoding="utf-8") as f:
            content = f.read()
            
        checks = {
            "observer_mode 默认值 False": "observer_mode: bool = False" in content,
            "创建任务时默认 False": 'observer_mode=False' in content,
            "from_dict 默认 False": 'observer_mode=data.get("observer_mode", False)' in content,
        }
        
        print("📋 Task 数据类检查")
        print("-" * 70)
        all_pass = True
        for check_name, result in checks.items():
            status = "✅" if result else "❌"
            print(f"  {status} {check_name}")
            if not result:
                all_pass = False
        
        if all_pass:
            print()
            print("✅ Task 数据类检查通过")
        else:
            print()
            print("❌ Task 数据类检查未通过")
            return False
    else:
        print(f"❌ 文件不存在: {task_file}")
        return False
    
    return True


def check_logging_isolation():
    """检查日志隔离逻辑"""
    print()
    print("=" * 70)
    print("TC-07 快速验证: 日志隔离检查")
    print("=" * 70)
    print()
    
    log_file = "Luna_Badge/core/log_manager.py"
    if os.path.exists(log_file):
        with open(log_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        checks = {
            "observer_enabled 检查": "if not observer_enabled:" in content,
            "异常处理": "except Exception as e:" in content or "try:" in content,
            "不抛出异常": "不抛出异常" in content or "不影响主流程" in content,
        }
        
        print("📋 日志隔离检查")
        print("-" * 70)
        all_pass = True
        for check_name, result in checks.items():
            status = "✅" if result else "❌"
            print(f"  {status} {check_name}")
            if not result:
                all_pass = False
        
        if all_pass:
            print()
            print("✅ 日志隔离检查通过")
        else:
            print()
            print("❌ 日志隔离检查未通过")
            return False
    else:
        print(f"❌ 文件不存在: {log_file}")
        return False
    
    return True


def main():
    """主函数"""
    print()
    print("=" * 70)
    print("V1.8.1 快速回滚等价性验证")
    print("=" * 70)
    print()
    print("⚠️  注意: 这是代码层面的快速检查，")
    print("   不能替代完整的系统测试。")
    print()
    
    # 执行检查
    result1 = check_observer_mode_defaults()
    result2 = check_logging_isolation()
    
    print()
    print("=" * 70)
    if result1 and result2:
        print("✅ 快速验证通过")
        print()
        print("📝 下一步:")
        print("   1. 执行完整的人工测试（TC-06 / TC-07）")
        print("   2. 验证系统行为与 v1.8 完全一致")
        print("   3. 记录结果到 docs/V1_8_1_TEST_EXECUTION_LOG.md")
    else:
        print("❌ 快速验证未通过")
        print()
        print("📝 建议:")
        print("   1. 修复代码问题")
        print("   2. 重新运行验证")
    print("=" * 70)


if __name__ == "__main__":
    main()


