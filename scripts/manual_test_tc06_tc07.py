#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
V1.8.1 人工测试辅助脚本 - TC-06 / TC-07

用途：辅助执行回滚等价性测试（TC-06 / TC-07）
注意：这是辅助脚本，需要人工验证和记录
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

def check_config_file():
    """检查配置文件"""
    print("=" * 70)
    print("步骤 1: 检查配置文件")
    print("=" * 70)
    print()
    
    config_files = [
        "config/system_config.yaml",
        "config.py",
    ]
    
    found = False
    for config_file in config_files:
        if os.path.exists(config_file):
            print(f"✅ 找到配置文件: {config_file}")
            found = True
            
            # 检查是否包含 OBSERVER_MODE_ENABLED
            with open(config_file, "r", encoding="utf-8") as f:
                content = f.read()
                if "OBSERVER_MODE_ENABLED" in content or "observer_mode" in content.lower():
                    print(f"   包含 observer_mode 相关配置")
                else:
                    print(f"   ⚠️  未找到 observer_mode 相关配置")
    
    if not found:
        print("⚠️  未找到配置文件")
        print("   建议手动设置环境变量或配置文件")
    
    print()
    return found


def check_v18_baseline():
    """检查 v1.8 基线版本"""
    print("=" * 70)
    print("步骤 2: 检查 v1.8 基线版本")
    print("=" * 70)
    print()
    
    # 检查版本文件
    version_file = "VERSION"
    if os.path.exists(version_file):
        with open(version_file, "r", encoding="utf-8") as f:
            version = f.read().strip()
        print(f"✅ 当前版本: {version}")
    else:
        print("⚠️  未找到 VERSION 文件")
    
    # 检查是否有 v1.8 相关文档
    v18_docs = [
        "docs/V1_8_FREEZE_DECLARATION.md",
        "docs/V1_8_FREEZE_CONFIRMATION.md",
    ]
    
    print()
    print("📄 v1.8 相关文档:")
    for doc in v18_docs:
        if os.path.exists(doc):
            print(f"  ✅ {doc}")
        else:
            print(f"  ⬜ {doc}")
    
    print()
    print("⚠️  请确认:")
    print("  1. v1.8 基线版本是否可用？")
    print("  2. v1.8.1 版本是否已部署？")
    print()


def generate_test_checklist():
    """生成测试检查清单"""
    print("=" * 70)
    print("TC-06: 全局回滚测试 - 检查清单")
    print("=" * 70)
    print()
    
    checklist = [
        "设置 OBSERVER_MODE_ENABLED=false",
        "运行完整导航流程",
        "运行医院挂号流程",
        "对比 v1.8 基线版本的行为",
        "检查播报内容是否一致",
        "检查任务流是否一致",
        "检查交互流程是否一致",
    ]
    
    for i, item in enumerate(checklist, 1):
        print(f"  [ ] {i}. {item}")
    
    print()
    print("判定标准:")
    print("  ✅ 所有行为与 v1.8 完全一致 → PASS")
    print("  ❌ 任何差异 → FAIL（阻断版本）")
    print()
    
    print("=" * 70)
    print("TC-07: 日志回滚测试 - 检查清单")
    print("=" * 70)
    print()
    
    checklist = [
        "设置 OBSERVER_MODE_ENABLED=false",
        "运行系统，触发所有场景",
        "检查日志文件（logs/ 目录）",
        "检查控制台输出",
        "搜索 observer_* 字段",
        "确认不存在 observer_* 字段",
    ]
    
    for i, item in enumerate(checklist, 1):
        print(f"  [ ] {i}. {item}")
    
    print()
    print("判定标准:")
    print("  ✅ 日志中无 observer_* 字段 → PASS")
    print("  ❌ 存在 observer_* 字段 → FAIL（阻断版本）")
    print()


def check_log_files():
    """检查日志文件"""
    print("=" * 70)
    print("步骤 3: 检查日志文件")
    print("=" * 70)
    print()
    
    log_dirs = [
        "logs",
        "Luna_Badge/logs",
        "luna_backend/logs",
    ]
    
    found_logs = False
    for log_dir in log_dirs:
        if os.path.exists(log_dir):
            print(f"✅ 找到日志目录: {log_dir}")
            found_logs = True
            
            # 列出最近的日志文件
            log_files = []
            for root, dirs, files in os.walk(log_dir):
                for file in files:
                    if file.endswith(('.log', '.json')):
                        log_files.append(os.path.join(root, file))
            
            if log_files:
                print(f"   找到 {len(log_files)} 个日志文件")
                print("   最近的日志文件:")
                for log_file in sorted(log_files, key=os.path.getmtime, reverse=True)[:5]:
                    print(f"     - {log_file}")
            else:
                print("   ⚠️  未找到日志文件")
    
    if not found_logs:
        print("⚠️  未找到日志目录")
        print("   日志可能在其他位置，请手动检查")
    
    print()


def search_observer_fields_in_logs():
    """在日志中搜索 observer_* 字段"""
    print("=" * 70)
    print("步骤 4: 搜索日志中的 observer_* 字段")
    print("=" * 70)
    print()
    
    log_dirs = [
        "logs",
        "Luna_Badge/logs",
        "luna_backend/logs",
    ]
    
    observer_keywords = [
        "observer_trigger_reason",
        "observer_level",
        "observer_user_response",
        "observer_enabled",
        "observer_bypass_reason",
        "observer_mode",
    ]
    
    found_observer = False
    for log_dir in log_dirs:
        if os.path.exists(log_dir):
            for root, dirs, files in os.walk(log_dir):
                for file in files:
                    if file.endswith(('.log', '.json')):
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                                content = f.read()
                                for keyword in observer_keywords:
                                    if keyword in content:
                                        print(f"⚠️  在 {file_path} 中找到: {keyword}")
                                        found_observer = True
                        except Exception as e:
                            pass  # 忽略无法读取的文件
    
    if not found_observer:
        print("✅ 未在日志中找到 observer_* 字段")
    else:
        print()
        print("❌ 发现 observer_* 字段，TC-07 可能失败")
    
    print()


def generate_test_record_template():
    """生成测试记录模板"""
    print("=" * 70)
    print("测试记录模板")
    print("=" * 70)
    print()
    
    template = {
        "TC-06": {
            "执行人": "",
            "日期": datetime.now().strftime("%Y-%m-%d"),
            "版本": "",
            "OBSERVER_MODE_ENABLED": False,
            "结果": "PASS / FAIL",
            "与 v1.8 是否完全一致": "是 / 否",
            "证据": "",
            "结论": "允许继续 / 阻断版本",
        },
        "TC-07": {
            "执行人": "",
            "日期": datetime.now().strftime("%Y-%m-%d"),
            "版本": "",
            "OBSERVER_MODE_ENABLED": False,
            "结果": "PASS / FAIL",
            "与 v1.8 是否完全一致": "是 / 否",
            "证据": "",
            "结论": "允许继续 / 阻断版本",
        },
    }
    
    print("请将以下信息记录到 docs/V1_8_1_TEST_EXECUTION_LOG.md:")
    print()
    print(json.dumps(template, indent=2, ensure_ascii=False))
    print()


def main():
    """主函数"""
    print()
    print("=" * 70)
    print("V1.8.1 人工测试辅助脚本 - TC-06 / TC-07")
    print("=" * 70)
    print()
    print("⚠️  注意: 这是辅助脚本，需要人工验证和记录")
    print()
    
    # 执行检查
    check_config_file()
    check_v18_baseline()
    check_log_files()
    search_observer_fields_in_logs()
    
    # 生成检查清单
    generate_test_checklist()
    
    # 生成记录模板
    generate_test_record_template()
    
    print("=" * 70)
    print("✅ 辅助检查完成")
    print("=" * 70)
    print()
    print("📝 下一步:")
    print("   1. 按照检查清单执行测试")
    print("   2. 记录结果到 docs/V1_8_1_TEST_EXECUTION_LOG.md")
    print("   3. 如果 TC-06 / TC-07 任一失败，立即终止测试")
    print()


if __name__ == "__main__":
    main()


