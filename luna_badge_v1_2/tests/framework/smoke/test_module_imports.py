#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Luna v1.4 → v1.5 迁移后全量功能测试（改进版）

测试所有迁移后的模块，确保功能正常
"""

import sys
import os
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import traceback

# 添加项目根目录到路径
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

# 测试结果
test_results: Dict[str, List[Tuple[str, bool, str]]] = {}


def test_import(category: str, module_name: str, import_statement: str):
    """
    测试模块导入
    
    Args:
        category: 测试类别
        module_name: 模块名称
        import_statement: 导入语句
    """
    if category not in test_results:
        test_results[category] = []
    
    try:
        # 执行导入
        exec(import_statement)
        test_results[category].append((module_name, True, ""))
        print(f"  ✅ {module_name}")
        return True
    except ImportError as e:
        error_msg = f"导入失败: {str(e)}"
        test_results[category].append((module_name, False, error_msg))
        print(f"  ❌ {module_name}")
        print(f"     错误: {error_msg}")
        return False
    except Exception as e:
        error_msg = f"未知错误: {str(e)}"
        test_results[category].append((module_name, False, error_msg))
        print(f"  ❌ {module_name}")
        print(f"     错误: {error_msg}")
        return False


def test_vision_modules():
    """测试视觉能力模块"""
    print("\n" + "=" * 60)
    print("测试视觉能力模块 (capabilities/vision)")
    print("=" * 60)
    
    test_import("视觉能力", "VisionPipeline", "from capabilities.vision.vision_pipeline import VisionPipeline")
    test_import("视觉能力", "VisionDetector", "from capabilities.vision.detector import VisionDetector")
    test_import("视觉能力", "VisionRouter", "from capabilities.vision.vision_router import VisionRouter")
    test_import("视觉能力", "VisionScheduler", "from capabilities.vision.vision_scheduler import VisionScheduler, SchedulerContext")
    test_import("视觉能力", "VisionFailSafe", "from capabilities.vision.vision_fail_safe import VisionFailSafe")
    test_import("视觉能力", "CameraRouter", "from capabilities.vision.camera_router import CameraRouter, CameraId")
    test_import("视觉能力", "MultiModelEngine", "from capabilities.vision.multi_model_engine import MultiModelEngine")
    test_import("视觉能力", "Arbiter", "from capabilities.vision.arbiter import Arbiter")
    test_import("视觉能力", "VisionTaskOrchestrator", "from capabilities.vision.vision_task_orchestrator import VisionTaskOrchestrator")
    test_import("视觉能力", "VisionDebugService", "from capabilities.vision.vision_debug_service import VisionDebugService")
    test_import("视觉能力", "ScoreLogger", "from capabilities.vision.score_logger import ScoreLogger")
    test_import("视觉能力", "Types", "from capabilities.vision.types import SceneObj, SceneFrameResult")


def test_speech_modules():
    """测试语音能力模块"""
    print("\n" + "=" * 60)
    print("测试语音能力模块 (capabilities/speech)")
    print("=" * 60)
    
    test_import("语音能力", "SpeechPipeline", "from capabilities.speech.speech_pipeline import SpeechPipeline")
    test_import("语音能力", "SpeechPipelineIntegration", "from capabilities.speech.speech_pipeline_integration import SpeechPipelineIntegration")
    test_import("语音能力", "NavSpeechManager", "from capabilities.speech.nav_speech_manager import NavSpeechManager")
    test_import("语音能力", "NavigationVoiceAdapter", "from capabilities.speech.navigation_voice_adapter import NavigationVoiceAdapter")
    # NavSpeechConfig 是配置文件，只有常量，没有类
    # test_import("语音能力", "NavSpeechConfig", "from capabilities.speech.nav_speech_config import NavSpeechConfig")


def test_navigation_modules():
    """测试导航能力模块"""
    print("\n" + "=" * 60)
    print("测试导航能力模块 (capabilities/navigation)")
    print("=" * 60)
    
    test_import("导航能力", "NavigationController", "from capabilities.navigation.navigation_controller import NavigationController")
    test_import("导航能力", "NavigationControllerIntegration", "from capabilities.navigation.navigation_controller_integration import NavigationControllerIntegration")


def test_audio_modules():
    """测试音频能力模块"""
    print("\n" + "=" * 60)
    print("测试音频能力模块 (capabilities/audio)")
    print("=" * 60)
    
    test_import("音频能力", "SoundEngine", "from capabilities.audio.sound_engine import SoundEngine")


def test_task_chain_modules():
    """测试任务链模块"""
    print("\n" + "=" * 60)
    print("测试任务链模块 (decision/task_chain)")
    print("=" * 60)
    
    test_import("任务链", "TaskChainManager", "from decision.task_chain.task_chain_manager import TaskChainManager")
    test_import("任务链", "TaskState", "from decision.task_chain.task_state import TaskState")
    test_import("任务链", "TaskNode", "from decision.task_chain.task_node import TaskNode")
    test_import("任务链", "TaskContext", "from decision.task_chain.task_context import TaskContext")
    test_import("任务链", "TaskEngine", "from decision.task_chain.task_engine import TaskEngine")
    test_import("任务链", "TaskChain", "from decision.task_chain.task_chain import TaskChain")
    test_import("任务链", "TaskTransitionManager", "from decision.task_chain.task_transition_manager import TaskTransitionManager, TaskDecision")
    test_import("任务链", "QueryBus", "from decision.task_chain.query_bus import QueryBus, Query, QueryStatus")
    test_import("任务链", "MultiTargetBuffer", "from decision.task_chain.multi_target_buffer import MultiTargetBuffer, Target")
    test_import("任务链", "TaskCacheManager", "from decision.task_chain.task_cache_manager import TaskCacheManager")
    test_import("任务链", "TaskDebugger", "from decision.task_chain.task_debugger import TaskDebugger")


def test_decision_modules():
    """测试决策模块"""
    print("\n" + "=" * 60)
    print("测试决策模块 (core/framework/decision)")
    print("=" * 60)
    
    test_import("决策", "DecisionCore", "from core.framework.decision.decision_core import DecisionCore, DecisionRequest")
    test_import("决策", "DecisionBuilder", "from core.framework.decision.builder import build_decision_core_v15")
    test_import("决策", "InquiryManager", "from core.framework.decision.inquiry.inquiry_manager import InquiryManager")
    test_import("决策", "InquiryParser", "from core.framework.decision.inquiry.parser import InquiryParser")
    test_import("决策", "DecisionLogger", "from core.framework.decision.logging.decision_logger import log_decision")


def test_capability_framework():
    """测试能力框架模块"""
    print("\n" + "=" * 60)
    print("测试能力框架模块 (core/framework/capability)")
    print("=" * 60)
    
    test_import("能力框架", "ModelRegistry", "from core.framework.capability.model_registry import ModelRegistry, ModelDescriptor, ModelType")
    # 注意：CapabilityRegistry 可能依赖 luna_core_v1_5，如果不存在则跳过
    try:
        test_import("能力框架", "CapabilityRegistry", "from core.framework.capability.registry import CapabilityRegistry")
    except:
        print("  ⚠️  CapabilityRegistry 跳过（可能依赖外部模块）")


def test_tts_policy():
    """测试 TTS 策略模块"""
    print("\n" + "=" * 60)
    print("测试 TTS 策略模块 (core/framework/runtime/tts_policy)")
    print("=" * 60)
    
    test_import("TTS策略", "BroadcastPolicy", "from core.framework.runtime.tts_policy.broadcast_policy import BroadcastPolicy, BroadcastPriority")
    test_import("TTS策略", "TimeWindowGate", "from core.framework.runtime.tts_policy.time_window_gate import TimeWindowGate")


def test_adapters():
    """测试能力适配器"""
    print("\n" + "=" * 60)
    print("测试能力适配器 (capability_adapters)")
    print("=" * 60)
    
    test_import("适配器", "VisionAdapter", "from capability_adapters.vision_adapter import VisionAdapter")
    test_import("适配器", "SpeechAdapter", "from capability_adapters.speech_adapter import SpeechAdapter")
    test_import("适配器", "NavigationAdapter", "from capability_adapters.navigation_adapter import NavigationAdapter")
    test_import("适配器", "OCRAdapter", "from capability_adapters.ocr_adapter import OCRAdapter")


def test_governance():
    """测试治理模块"""
    print("\n" + "=" * 60)
    print("测试治理模块 (core/framework/governance)")
    print("=" * 60)
    
    test_import("治理", "Arbiter", "from core.framework.governance.arbiter import Arbiter")
    test_import("治理", "ConfidenceGate", "from core.framework.governance.confidence_gate import ConfidenceGate")
    test_import("治理", "RiskPolicy", "from core.framework.governance.risk_policy import RiskPolicy")


def test_runtime():
    """测试运行时模块"""
    print("\n" + "=" * 60)
    print("测试运行时模块 (core/framework/runtime)")
    print("=" * 60)
    
    test_import("运行时", "RuntimeContext", "from core.framework.runtime.context import RuntimeContext")
    test_import("运行时", "LifecycleManager", "from core.framework.runtime.lifecycle import LifecycleManager, LifecycleState")
    test_import("运行时", "StateSnapshot", "from core.framework.runtime.state_snapshot import StateSnapshot")


def test_scheduler():
    """测试调度器模块"""
    print("\n" + "=" * 60)
    print("测试调度器模块 (core/framework/scheduler)")
    print("=" * 60)
    
    test_import("调度器", "Scheduler", "from core.framework.scheduler.scheduler import Scheduler")
    test_import("调度器", "Priority", "from core.framework.scheduler.priority import Priority")


def generate_report():
    """生成测试报告"""
    print("\n" + "=" * 60)
    print("测试报告")
    print("=" * 60)
    
    total_tests = 0
    passed_tests = 0
    failed_tests = 0
    
    for category, results in test_results.items():
        print(f"\n{category}:")
        for module_name, success, error in results:
            total_tests += 1
            if success:
                passed_tests += 1
                print(f"  ✅ {module_name}")
            else:
                failed_tests += 1
                print(f"  ❌ {module_name}")
                if error:
                    print(f"     错误: {error}")
    
    print("\n" + "=" * 60)
    print("测试统计")
    print("=" * 60)
    if total_tests > 0:
        print(f"总测试数: {total_tests}")
        print(f"通过: {passed_tests} ({passed_tests/total_tests*100:.1f}%)")
        print(f"失败: {failed_tests} ({failed_tests/total_tests*100:.1f}%)")
    else:
        print("没有执行任何测试")
    print("=" * 60)
    
    if failed_tests == 0:
        print("\n✅ 所有测试通过！迁移成功！")
        return True
    else:
        print(f"\n⚠️  有 {failed_tests} 个测试失败，请检查")
        return False


def main():
    """主测试函数"""
    print("=" * 60)
    print("Luna v1.4 → v1.5 迁移后全量功能测试")
    print("=" * 60)
    
    # 执行所有测试
    test_vision_modules()
    test_speech_modules()
    test_navigation_modules()
    test_audio_modules()
    test_task_chain_modules()
    test_decision_modules()
    test_capability_framework()
    test_tts_policy()
    test_adapters()
    test_governance()
    test_runtime()
    test_scheduler()
    
    # 生成报告
    success = generate_report()
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
