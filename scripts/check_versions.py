#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
版本检查脚本
检查所有模块的版本信息
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple

def find_version_in_file(file_path: Path) -> Tuple[str, bool]:
    """从文件中提取版本信息"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 查找 __version__ = "x.x.x"
        version_match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
        if version_match:
            return version_match.group(1), True
        
        return "未找到", False
    except Exception as e:
        return f"错误: {e}", False

def check_versions():
    """检查所有模块版本"""
    project_root = Path(__file__).parent.parent
    
    # 检查主版本文件
    version_file = project_root / "VERSION"
    if version_file.exists():
        with open(version_file, 'r') as f:
            main_version = f.read().strip()
        print(f"📦 主版本号: {main_version}")
    else:
        print("⚠️ 未找到VERSION文件")
        main_version = None
    
    print("\n" + "="*60)
    print("模块版本检查")
    print("="*60)
    
    # 检查Luna_Badge核心模块
    print("\n🔷 Luna_Badge 核心模块:")
    badge_core = project_root / "Luna_Badge" / "core"
    badge_modules = [
        "system_orchestrator_enhanced.py",
        "whisper_recognizer.py",
        "tts_manager.py",
        "vision_ocr_engine.py",
        "step_detector.py",
        "navigation_manager.py",
        "task_engine.py",
        "memory_store.py",
        "log_manager.py",
    ]
    
    for module in badge_modules:
        file_path = badge_core / module
        if file_path.exists():
            version, found = find_version_in_file(file_path)
            status = "✅" if found and version != "未找到" else "❌"
            print(f"  {status} {module:40} {version}")
        else:
            print(f"  ⚠️  {module:40} 文件不存在")
    
    # 检查Luna-mid学习模块
    print("\n🔷 Luna-mid 学习模块:")
    mid_core = project_root / "Luna-mid" / "core"
    mid_modules = [
        "__init__.py",
        "error_learning.py",
        "task_optimizer.py",
        "user_habit_analyzer.py",
        "visual_learning.py",
        "learning_manager.py",
    ]
    
    for module in mid_modules:
        file_path = mid_core / module
        if file_path.exists():
            version, found = find_version_in_file(file_path)
            status = "✅" if found and version != "未找到" else "❌"
            print(f"  {status} {module:40} {version}")
        else:
            print(f"  ⚠️  {module:40} 文件不存在")
    
    # 统计
    print("\n" + "="*60)
    print("版本统计")
    print("="*60)
    
    all_versions = {}
    for module in badge_modules + mid_modules:
        if module == "__init__.py":
            file_path = mid_core / module
        elif module.startswith("system") or module.startswith("whisper") or module.startswith("tts") or module.startswith("vision") or module.startswith("step") or module.startswith("navigation") or module.startswith("task") or module.startswith("memory") or module.startswith("log"):
            file_path = badge_core / module
        else:
            file_path = mid_core / module
            
        if file_path.exists():
            version, found = find_version_in_file(file_path)
            if found and version != "未找到":
                all_versions[version] = all_versions.get(version, 0) + 1
    
    for version, count in sorted(all_versions.items()):
        print(f"  {version}: {count} 个模块")
    
    if main_version and main_version in all_versions:
        print(f"\n✅ 主版本 {main_version} 与模块版本一致")
    elif main_version:
        print(f"\n⚠️ 主版本 {main_version} 与模块版本不一致")

if __name__ == "__main__":
    check_versions()

