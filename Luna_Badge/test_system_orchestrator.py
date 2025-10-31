#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
系统控制中枢测试脚本
验证语音、视觉、导航、记忆等模块的联动
"""

import sys
import logging
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def test_orchestrator_basic():
    """测试控制中枢基础功能"""
    print("=" * 70)
    print("🧠 测试1: 控制中枢基础功能")
    print("=" * 70)
    
    from core.system_orchestrator import SystemOrchestrator, SystemState, UserIntent
    
    # 创建控制中枢（不加载实际模块）
    orchestrator = SystemOrchestrator()
    
    # 测试状态管理
    print("\n📊 测试状态管理:")
    orchestrator.set_state(SystemState.IDLE)
    print(f"  当前状态: {orchestrator.state}")
    
    # 测试启动/停止
    print("\n🔄 测试启动/停止:")
    orchestrator.start()
    print("  ✅ 控制中枢已启动")
    
    orchestrator.stop()
    print("  ✅ 控制中枢已停止")
    
    print("\n✅ 测试1完成\n")


def test_intent_parsing():
    """测试意图解析"""
    print("=" * 70)
    print("🎯 测试2: 意图解析")
    print("=" * 70)
    
    from core.system_orchestrator import SystemOrchestrator, UserIntent
    
    orchestrator = SystemOrchestrator()
    
    # 测试用例
    test_cases = [
        ("我要去厕所", UserIntent.FIND_TOILET),
        ("哪里有电梯", UserIntent.FIND_ELEVATOR),
        ("去305号诊室", UserIntent.FIND_DESTINATION),
        ("这条路记住", UserIntent.REMEMBER_PATH),
        ("开始导航", UserIntent.START_NAVIGATION),
        ("取消", UserIntent.CANCEL),
    ]
    
    print("\n📝 测试意图解析:")
    for text, expected_intent in test_cases:
        result = orchestrator._parse_intent(text)
        status = "✅" if result.intent == expected_intent else "❌"
        print(f"  {status} 文本: '{text}' -> 意图: {result.intent.value} (置信度: {result.confidence:.2f})")
    
    print("\n✅ 测试2完成\n")


def test_visual_event_parsing():
    """测试视觉事件解析"""
    print("=" * 70)
    print("👁️ 测试3: 视觉事件解析")
    print("=" * 70)
    
    from core.system_orchestrator import SystemOrchestrator, VisualEvent
    
    orchestrator = SystemOrchestrator()
    
    # 重新导入以避免循环引用
    
    # 测试用例
    test_cases = [
        ({"classes": ["stairs", "person"]}, VisualEvent.STAIRS_DETECTED),
        ({"classes": ["elevator"]}, VisualEvent.ELEVATOR_DETECTED),
        ({"classes": ["toilet", "sign"]}, VisualEvent.TOILET_SIGN_DETECTED),
        ({"classes": ["exit", "door"]}, VisualEvent.EXIT_SIGN_DETECTED),
        ({"classes": ["obstacle"]}, VisualEvent.OBSTACLE_DETECTED),
        ({"classes": ["person"]}, VisualEvent.SAFE),
        ({}, VisualEvent.SAFE),
    ]
    
    print("\n📝 测试视觉事件解析:")
    for detection, expected_event in test_cases:
        result = orchestrator._parse_visual_event(detection)
        status = "✅" if result == expected_event else "❌"
        print(f"  {status} 检测: {detection} -> 事件: {result.value if result else 'None'}")
    
    print("\n✅ 测试3完成\n")


def test_with_mock_modules():
    """使用模拟模块测试完整流程"""
    print("=" * 70)
    print("🔄 测试4: 模拟模块集成")
    print("=" * 70)
    
    from core.system_orchestrator import SystemOrchestrator
    
    # 创建模拟模块
    class MockWhisper:
        def recognize_audio_file(self):
            return "我要去厕所"
    
    class MockTTS:
        def speak(self, text):
            print(f"  🔊 TTS播报: {text}")
    
    class MockNavigator:
        def plan_path_to_facility(self, facility):
            return {
                "distance": 15,
                "direction": "前方",
                "path": ["直行10米", "左转", "直行5米"]
            }
        
        def plan_path(self, destination):
            return {
                "distance": 30,
                "path": ["直行20米", "上电梯到3楼", "直行10米"]
            }
    
    class MockMemory:
        def save_path_memory(self, scenes):
            print(f"  💾 保存路径记忆: {len(scenes) if scenes else 0}个场景")
        
        def save_navigation_memory(self, path, destination):
            print(f"  💾 保存导航记忆: 目的地={destination}")
    
    class MockCamera:
        def record_scenes_for_memory(self):
            return [
                {"image": "path/to/scene1.jpg", "description": "入口"},
                {"image": "path/to/scene2.jpg", "description": "走廊"}
            ]
    
    # 创建控制中枢并注入模拟模块
    orchestrator = SystemOrchestrator(
        whisper_recognizer=MockWhisper(),
        tts_manager=MockTTS(),
        navigator=MockNavigator(),
        memory_manager=MockMemory(),
        camera_manager=MockCamera()
    )
    
    # 启动控制中枢
    orchestrator.start()
    
    # 测试语音输入处理
    print("\n🎤 测试语音输入处理:")
    try:
        orchestrator.handle_voice_input()
    except Exception as e:
        logger.error(f"语音处理失败: {e}")
    
    # 等待事件处理
    import time
    time.sleep(1)
    
    # 测试视觉事件处理
    print("\n👁️ 测试视觉事件处理:")
    detection = {
        "classes": ["stairs"],
        "confidence": 0.95,
        "bbox": [100, 100, 200, 300]
    }
    orchestrator.handle_visual_event(detection)
    
    # 等待事件处理
    time.sleep(1)
    
    # 停止控制中枢
    orchestrator.stop()
    
    # 显示日志
    print("\n📋 动作日志:")
    logs = orchestrator.get_logs(limit=10)
    for log in logs:
        print(f"  {log['action_type']}: {log['data']}")
    
    print("\n✅ 测试4完成\n")


def test_demo_scenarios():
    """测试Demo场景"""
    print("=" * 70)
    print("🎬 测试5: Demo场景验证")
    print("=" * 70)
    
    from core.system_orchestrator import SystemOrchestrator, UserIntent, VisualEvent
    
    orchestrator = SystemOrchestrator()
    
    print("\n📝 场景1: 语音流程")
    print("-" * 70)
    
    # 模拟语音输入
    test_commands = [
        "我要去厕所",
        "哪里有电梯",
        "去305号诊室",
        "这条路记住",
        "开始导航",
        "取消"
    ]
    
    for cmd in test_commands:
        print(f"\n用户说: '{cmd}'")
        result = orchestrator._parse_intent(cmd)
        print(f"  -> 意图: {result.intent.value} (置信度: {result.confidence:.2f})")
        print(f"  -> 提取数据: {result.extracted_data}")
    
    print("\n📝 场景2: 视觉流程")
    print("-" * 70)
    
    # 模拟视觉检测
    visual_detections = [
        {"classes": ["stairs"]},
        {"classes": ["elevator"]},
        {"classes": ["toilet", "sign"]},
        {"classes": ["exit"]},
        {"classes": ["obstacle"]},
    ]
    
    for detection in visual_detections:
        print(f"\n检测到: {detection}")
        event = orchestrator._parse_visual_event(detection)
        print(f"  -> 事件: {event.value if event else 'None'}")
        
        # 模拟反馈
        feedback_map = {
            VisualEvent.STAIRS_DETECTED: "前方有台阶，请小心",
            VisualEvent.ELEVATOR_DETECTED: "已到达电梯，请注意看标识",
            VisualEvent.TOILET_SIGN_DETECTED: "左侧有卫生间标识",
            VisualEvent.EXIT_SIGN_DETECTED: "前方有出口标识",
            VisualEvent.OBSTACLE_DETECTED: "前方有障碍物，请绕行"
        }
        feedback = feedback_map.get(event)
        if feedback:
            print(f"  -> 🔊 播报: {feedback}")
    
    print("\n📝 场景3: 联合流程")
    print("-" * 70)
    
    print("\n1. 用户说: '带我去305号诊室'")
    intent = orchestrator._parse_intent("带我去305号诊室")
    print(f"   -> 意图: {intent.intent.value}")
    print(f"   -> 🔍 提取目的地: {orchestrator._extract_destination('带我去305号诊室')}")
    print("   -> 生成路径并播报")
    
    print("\n2. 途中检测到电梯")
    event = orchestrator._parse_visual_event({"classes": ["elevator"]})
    print(f"   -> 事件: {event.value}")
    print("   -> 🔊 播报: '已到达电梯，请按三楼'")
    
    print("\n3. 保存导航记忆")
    print("   -> 💾 记录路径和目的地")
    
    print("\n✅ 测试5完成\n")


def main():
    """主测试函数"""
    print("\n" + "=" * 70)
    print("🧠 Luna Badge 系统控制中枢完整测试")
    print("=" * 70)
    
    try:
        # 基础功能测试
        test_orchestrator_basic()
        
        # 意图解析测试
        test_intent_parsing()
        
        # 视觉事件测试
        test_visual_event_parsing()
        
        # 模拟模块集成测试
        test_with_mock_modules()
        
        # Demo场景测试
        test_demo_scenarios()
        
        print("=" * 70)
        print("✅ 所有测试完成")
        print("=" * 70)
        
    except Exception as e:
        logger.error(f"测试失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

