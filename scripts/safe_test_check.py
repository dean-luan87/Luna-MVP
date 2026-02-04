#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
V1.8.1 安全测试检查脚本（不导入系统模块）

用途：通过代码静态分析进行测试，避免导入依赖导致崩溃
"""

import os
import re

def check_tc06():
    """TC-06: 全局回滚测试 - 代码检查"""
    print("=" * 70)
    print("TC-06: 全局回滚测试 - 代码检查")
    print("=" * 70)
    print()
    
    task_file = "Luna_Badge/core/task_chain_manager.py"
    if not os.path.exists(task_file):
        print(f"❌ 文件不存在: {task_file}")
        return False
    
    with open(task_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    checks = {
        "observer_mode 字段定义": r"observer_mode:\s*bool\s*=\s*False",
        "create_task 默认 False": r"observer_mode\s*=\s*False",
        "from_dict 向后兼容": r'observer_mode\s*=\s*data\.get\("observer_mode",\s*False\)',
        "to_dict 包含字段": r'"observer_mode"|\'observer_mode\'',
        "继承逻辑检查": r"if\s+completed_task\.observer_mode:",
        "正确复制状态": r"next_task\.observer_mode\s*=\s*completed_task\.observer_mode",
    }
    
    all_pass = True
    for check_name, pattern in checks.items():
        if re.search(pattern, content):
            print(f"  ✅ {check_name}")
        else:
            print(f"  ❌ {check_name}")
            all_pass = False
    
    print()
    return all_pass


def check_tc07():
    """TC-07: 日志回滚测试 - 代码检查"""
    print("=" * 70)
    print("TC-07: 日志回滚测试 - 代码检查")
    print("=" * 70)
    print()
    
    log_file = "Luna_Badge/core/log_manager.py"
    if not os.path.exists(log_file):
        print(f"❌ 文件不存在: {log_file}")
        return False
    
    with open(log_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 查找 log_observer_mode_event 方法
    method_match = re.search(
        r"def\s+log_observer_mode_event\([^)]*\):",
        content
    )
    
    if not method_match:
        print("  ❌ 未找到 log_observer_mode_event 方法")
        return False
    
    method_start = method_match.start()
    # 查找下一个方法或类定义
    next_method = re.search(
        r"\n\s+def\s+\w+\(|class\s+\w+:",
        content[method_start:]
    )
    
    if next_method:
        method_content = content[method_start:method_start + next_method.start()]
    else:
        method_content = content[method_start:]
    
    checks = {
        "observer_enabled 参数": r"observer_enabled:\s*bool\s*=\s*False",
        "observer_enabled 检查": r"if\s+not\s+observer_enabled:",
        "metadata.active 检查": r'metadata\.get\("active",\s*False\)',
        "异常处理": r"except\s+Exception",
        "不抛出异常": r"不抛出异常|不影响主流程",
        "observer_trigger_reason 字段": r'"observer_trigger_reason"|\'observer_trigger_reason\'',
        "observer_level 字段": r'"observer_level"|\'observer_level\'',
        "observer_user_response 字段": r'"observer_user_response"|\'observer_user_response\'',
    }
    
    all_pass = True
    for check_name, pattern in checks.items():
        if re.search(pattern, method_content):
            print(f"  ✅ {check_name}")
        else:
            print(f"  ❌ {check_name}")
            all_pass = False
    
    print()
    return all_pass


def check_config():
    """配置检查"""
    print("=" * 70)
    print("配置检查")
    print("=" * 70)
    print()
    
    # 检查 config.py
    config_file = "config.py"
    if os.path.exists(config_file):
        with open(config_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        if "OBSERVER_MODE_ENABLED" in content:
            print("  ✅ config.py 包含 OBSERVER_MODE_ENABLED")
            if "os.environ.get('OBSERVER_MODE_ENABLED', 'false')" in content:
                print("  ✅ 支持环境变量覆盖")
        else:
            print("  ❌ config.py 不包含 OBSERVER_MODE_ENABLED")
            return False
    else:
        print(f"  ❌ 文件不存在: {config_file}")
        return False
    
    # 检查 config/system_config.yaml
    yaml_file = "config/system_config.yaml"
    if os.path.exists(yaml_file):
        with open(yaml_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        if "observer_mode_enabled" in content:
            print("  ✅ config/system_config.yaml 包含 observer_mode_enabled")
            if "observer_mode_enabled: false" in content:
                print("  ✅ 默认值为 false")
        else:
            print("  ❌ config/system_config.yaml 不包含 observer_mode_enabled")
            return False
    else:
        print(f"  ❌ 文件不存在: {yaml_file}")
        return False
    
    print()
    return True


def main():
    """主函数"""
    print()
    print("=" * 70)
    print("V1.8.1 安全测试检查（不导入系统模块）")
    print("=" * 70)
    print()
    print("⚠️  注意: 这是代码静态分析，不导入任何系统模块")
    print("   避免导入依赖导致崩溃")
    print()
    
    results = {
        "TC-06": check_tc06(),
        "TC-07": check_tc07(),
        "配置": check_config(),
    }
    
    print("=" * 70)
    print("测试结果总结")
    print("=" * 70)
    print()
    
    all_pass = True
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} {test_name}")
        if not result:
            all_pass = False
    
    print()
    if all_pass:
        print("✅ 所有代码层面检查通过")
        print()
        print("📝 下一步:")
        print("   代码层面验证已完成，可以开始系统测试")
        print("   系统测试需要实际运行系统，请按照测试指南执行")
    else:
        print("❌ 部分检查未通过，请修复后再测试")
    
    print()
    print("=" * 70)


if __name__ == "__main__":
    main()

