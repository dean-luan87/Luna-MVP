#!/usr/bin/env python3
"""
v1.4.2 完整交付验证脚本
验证所有模块可以正常导入和实例化
"""
import sys
import os
from pathlib import Path

# 添加项目根目录到路径
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

def verify_imports():
    """验证所有模块可以正常导入"""
    print("=" * 60)
    print("验证 v1.4.2 模块导入...")
    print("=" * 60)
    
    errors = []
    
    # 基础设施
    try:
        from infra.logging_manager import get_logger
        print("✅ infra.logging_manager")
    except Exception as e:
        errors.append(f"infra.logging_manager: {e}")
        print(f"❌ infra.logging_manager: {e}")
    
    # 系统模块
    try:
        from core.system.system_monitor import SystemMonitor
        print("✅ core.system.system_monitor")
    except Exception as e:
        errors.append(f"core.system.system_monitor: {e}")
        print(f"❌ core.system.system_monitor: {e}")
    
    try:
        from core.system.safe_mode import SafeModeManager, SafeModeContext
        print("✅ core.system.safe_mode")
    except Exception as e:
        errors.append(f"core.system.safe_mode: {e}")
        print(f"❌ core.system.safe_mode: {e}")
    
    try:
        from core.system.system_recovery_center import RecoveryCenter
        print("✅ core.system.system_recovery_center")
    except Exception as e:
        errors.append(f"core.system.system_recovery_center: {e}")
        print(f"❌ core.system.system_recovery_center: {e}")
    
    # 视觉模块
    try:
        from core.vision.camera_router import CameraRouter, DummyCameraManager
        print("✅ core.vision.camera_router")
    except Exception as e:
        errors.append(f"core.vision.camera_router: {e}")
        print(f"❌ core.vision.camera_router: {e}")
    
    try:
        from core.vision.vision_scheduler import VisionScheduler, SchedulerContext
        print("✅ core.vision.vision_scheduler")
    except Exception as e:
        errors.append(f"core.vision.vision_scheduler: {e}")
        print(f"❌ core.vision.vision_scheduler: {e}")
    
    try:
        from core.vision.vision_fail_safe import VisionFailSafe, FailSafeConfig
        print("✅ core.vision.vision_fail_safe")
    except Exception as e:
        errors.append(f"core.vision.vision_fail_safe: {e}")
        print(f"❌ core.vision.vision_fail_safe: {e}")
    
    # 任务模块
    try:
        from core.task.task_transition_manager import TaskTransitionManager, TaskDecision
        print("✅ core.task.task_transition_manager")
    except Exception as e:
        errors.append(f"core.task.task_transition_manager: {e}")
        print(f"❌ core.task.task_transition_manager: {e}")
    
    try:
        from core.task.multi_target_buffer import MultiTargetBuffer, Target
        print("✅ core.task.multi_target_buffer")
    except Exception as e:
        errors.append(f"core.task.multi_target_buffer: {e}")
        print(f"❌ core.task.multi_target_buffer: {e}")
    
    try:
        from core.task.query_bus import QueryBus, Query
        print("✅ core.task.query_bus")
    except Exception as e:
        errors.append(f"core.task.query_bus: {e}")
        print(f"❌ core.task.query_bus: {e}")
    
    # 导航模块
    try:
        from navigation.navigation_controller import NavigationController, NavState
        print("✅ navigation.navigation_controller")
    except Exception as e:
        errors.append(f"navigation.navigation_controller: {e}")
        print(f"❌ navigation.navigation_controller: {e}")
    
    # 语音模块
    try:
        from speech.intent_parser import IntentParser
        print("✅ speech.intent_parser")
    except Exception as e:
        errors.append(f"speech.intent_parser: {e}")
        print(f"❌ speech.intent_parser: {e}")
    
    try:
        from speech.speech_pipeline import SpeechPipeline, DummyASR, DummyTTS
        print("✅ speech.speech_pipeline")
    except Exception as e:
        errors.append(f"speech.speech_pipeline: {e}")
        print(f"❌ speech.speech_pipeline: {e}")
    
    # 主程序（检查文件是否存在）
    main_file = PROJECT_ROOT / "main.py"
    if main_file.exists():
        print("✅ main.py 文件存在")
    else:
        errors.append("main.py 文件不存在")
        print("❌ main.py 文件不存在")
    
    print("\n" + "=" * 60)
    if errors:
        print(f"❌ 发现 {len(errors)} 个错误:")
        for error in errors:
            print(f"  - {error}")
        return False
    else:
        print("✅ 所有模块导入成功！")
        return True

def verify_instantiation():
    """验证所有模块可以正常实例化"""
    print("\n" + "=" * 60)
    print("验证模块实例化...")
    print("=" * 60)
    
    errors = []
    
    try:
        from infra.logging_manager import get_logger
        logger = get_logger("test")
        print("✅ logging_manager 实例化")
    except Exception as e:
        errors.append(f"logging_manager: {e}")
        print(f"❌ logging_manager: {e}")
    
    try:
        from core.system.system_monitor import SystemMonitor
        monitor = SystemMonitor()
        cpu = monitor.cpu_usage()
        print(f"✅ SystemMonitor 实例化 (CPU: {cpu:.2f})")
    except Exception as e:
        errors.append(f"SystemMonitor: {e}")
        print(f"❌ SystemMonitor: {e}")
    
    try:
        from core.system.safe_mode import SafeModeManager
        from speech.speech_pipeline import DummyTTS
        tts = DummyTTS()
        safe_mode = SafeModeManager(tts.speak)
        print("✅ SafeModeManager 实例化")
    except Exception as e:
        errors.append(f"SafeModeManager: {e}")
        print(f"❌ SafeModeManager: {e}")
    
    try:
        from core.vision.vision_scheduler import VisionScheduler
        scheduler = VisionScheduler()
        print("✅ VisionScheduler 实例化")
    except Exception as e:
        errors.append(f"VisionScheduler: {e}")
        print(f"❌ VisionScheduler: {e}")
    
    try:
        from core.vision.vision_fail_safe import VisionFailSafe, FailSafeConfig
        failsafe = VisionFailSafe(FailSafeConfig())
        print("✅ VisionFailSafe 实例化")
    except Exception as e:
        errors.append(f"VisionFailSafe: {e}")
        print(f"❌ VisionFailSafe: {e}")
    
    try:
        from core.task.query_bus import QueryBus
        from speech.speech_pipeline import DummyTTS
        tts = DummyTTS()
        query_bus = QueryBus(tts.speak)
        print("✅ QueryBus 实例化")
    except Exception as e:
        errors.append(f"QueryBus: {e}")
        print(f"❌ QueryBus: {e}")
    
    print("\n" + "=" * 60)
    if errors:
        print(f"❌ 发现 {len(errors)} 个错误:")
        for error in errors:
            print(f"  - {error}")
        return False
    else:
        print("✅ 所有模块实例化成功！")
        return True

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("Luna Badge v1.4.2 完整交付验证")
    print("=" * 60 + "\n")
    
    import_ok = verify_imports()
    instantiate_ok = verify_instantiation()
    
    print("\n" + "=" * 60)
    if import_ok and instantiate_ok:
        print("🎉 验证通过！所有模块正常！")
        sys.exit(0)
    else:
        print("❌ 验证失败！请检查错误信息。")
        sys.exit(1)

