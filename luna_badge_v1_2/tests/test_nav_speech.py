from core.logging import get_logger

#!/usr/bin/env python3
log = get_logger("test_nav_speech")
"""
Navigation Speech Manager 测试脚本（F8）

测试导航语音策略与模板模块
"""

import sys
import os
import time
import logging
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)

from capabilities.speech.nav_speech_manager import NavSpeechManager

logger = logging.getLogger(__name__)


def create_test_nav_results():
    """创建测试用的导航决策序列"""
    scenarios = [
        # 连续 FORWARD
        {"decision": "FORWARD", "offset": 0.0, "message": "前方可通行，请直行"},
        {"decision": "FORWARD", "offset": 0.0, "message": "前方可通行，请直行"},
        {"decision": "FORWARD", "offset": 0.0, "message": "前方可通行，请直行"},
        {"decision": "FORWARD", "offset": 0.0, "message": "前方可通行，请直行"},
        
        # 切换到 SLIGHT_RIGHT
        {"decision": "SLIGHT_RIGHT", "offset": 0.8, "message": "右侧稍微更通畅，请向右一点"},
        {"decision": "SLIGHT_RIGHT", "offset": 0.9, "message": "右侧稍微更通畅，请向右一点"},
        {"decision": "SLIGHT_RIGHT", "offset": 0.7, "message": "右侧稍微更通畅，请向右一点"},
        
        # 切换到 HARD_RIGHT
        {"decision": "HARD_RIGHT", "offset": 1.5, "message": "右前方更通畅，请向右移动"},
        {"decision": "HARD_RIGHT", "offset": 1.6, "message": "右前方更通畅，请向右移动"},
        
        # 突然 STOP（普通）
        {"decision": "STOP", "offset": 0.0, "message": "前方无法通行，请原地停下"},
        
        # 再次 STOP（危险）
        {"decision": "STOP", "offset": 0.0, "message": "前方无法通行，请原地停下"},
    ]
    
    return scenarios


def test_nav_speech_cooldown():
    """测试冷却时间机制"""
    log.info("\n" + "=" * 80)
    log.info("🧪 Navigation Speech Manager 测试（冷却时间）")
    log.info("=" * 80")

    try:
        # 创建管理器
        log.info("\n📦 正在初始化 NavSpeechManager...")
        manager = NavSpeechManager()
        log.info("✅ NavSpeechManager 初始化成功")

        # 创建测试序列
        log.info("\n📋 创建测试序列...")
        scenarios = create_test_nav_results()

        log.info("\n🔍 测试冷却时间机制:\n")
        log.info("帧 | 决策         | 是否播报 | 文本")
        log.info("-" * 80")

        for i, nav_result in enumerate(scenarios):
            decision = nav_result["decision"]
            
            # 模拟快速帧（每 0.1 秒一帧）
            if i > 0:
                time.sleep(0.1)

            event = manager.build_from_nav(nav_result, danger=(i >= len(scenarios) - 2))

            if event:
                status = "✅ 是"
                text_short = event["text"][:30] + "..." if len(event["text"]) > 30 else event["text"]
                log.info(f"{i+1:2d} | {decision:12s} | {status:8s} | {text_short}")
            else:
                status = "❌ 否（冷却中）"
                log.info(f"{i+1:2d} | {decision:12s} | {status:8s} | -")

        log.info("\n✅ 冷却时间测试完成")
        log.info("\n💡 观察:")
        log.info("   - FORWARD 连续多帧，应该只播报一次（5秒冷却）")
        log.info("   - SLIGHT_RIGHT 连续多帧，应该只播报一次（3秒冷却）")
        log.info("   - STOP 可以频繁播报（0.5秒冷却）")

        return True

    except Exception as e:
        log.info(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_nav_speech_priority():
    """测试优先级机制"""
    log.info("\n" + "=" * 80)
    log.info("🧪 Navigation Speech Manager 测试（优先级）")
    log.info("=" * 80")

    try:
        manager = NavSpeechManager()

        test_cases = [
            {"decision": "FORWARD", "priority": 0, "style": "calm"},
            {"decision": "SLIGHT_LEFT", "priority": 1, "style": "calm"},
            {"decision": "SLIGHT_RIGHT", "priority": 1, "style": "calm"},
            {"decision": "HARD_LEFT", "priority": 2, "style": "alert"},
            {"decision": "HARD_RIGHT", "priority": 2, "style": "alert"},
            {"decision": "STOP", "priority": 3, "style": "alert"},
        ]

        log.info("\n🔍 测试优先级和风格:\n")
        log.info("决策         | 优先级 | 风格   | 可打断 | 文本")
        log.info("-" * 80")

        for case in test_cases:
            nav_result = {
                "decision": case["decision"],
                "offset": 0.0,
                "message": f"测试消息：{case['decision']}"
            }

            event = manager.build_from_nav(nav_result)

            if event:
                interruptible = "是" if event["interruptible"] else "否"
                text_short = event["text"][:20] + "..." if len(event["text"]) > 20 else event["text"]
                log.info(f"{case['decision']:12s} | {event['priority']:6d} | {event['style']:6s} | {interruptible:6s} | {text_short}")

            # 重置状态以便测试下一个
            manager.reset()

        log.info("\n✅ 优先级测试完成")

        return True

    except Exception as e:
        log.info(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_nav_speech_danger():
    """测试危险场景"""
    log.info("\n" + "=" * 80)
    log.info("🧪 Navigation Speech Manager 测试（危险场景）")
    log.info("=" * 80")

    try:
        manager = NavSpeechManager()

        # 普通 STOP
        nav_result_normal = {
            "decision": "STOP",
            "offset": 0.0,
            "message": "前方无法通行，请原地停下"
        }

        event_normal = manager.build_from_nav(nav_result_normal, danger=False)
        log.info(f"\n📋 普通 STOP:")
        if event_normal:
            log.info(f"   文本: {event_normal['text']}")

        # 等待一下，避免冷却
        time.sleep(0.6)

        # 危险 STOP
        event_danger = manager.build_from_nav(nav_result_normal, danger=True)
        log.info(f"\n📋 危险 STOP:")
        if event_danger:
            log.info(f"   文本: {event_danger['text']}")

        log.info("\n✅ 危险场景测试完成")
        log.info("\n💡 观察:")
        log.info("   - 危险 STOP 应该使用加重提示：" + (event_danger['text'] if event_danger else "")")

        return True

    except Exception as e:
        log.info(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_nav_speech_state_change():
    """测试状态切换感知"""
    log.info("\n" + "=" * 80)
    log.info("🧪 Navigation Speech Manager 测试（状态切换）")
    log.info("=" * 80")

    try:
        manager = NavSpeechManager()

        # 模拟状态切换序列
        transitions = [
            ("FORWARD", 0.0),
            ("FORWARD", 0.0),  # 相同，应该不播报
            ("SLIGHT_RIGHT", 0.8),  # 切换，应该播报
            ("SLIGHT_RIGHT", 0.9),  # 相同，冷却中
            ("HARD_RIGHT", 1.5),  # 切换，应该播报
            ("STOP", 0.0),  # 切换，应该播报
        ]

        log.info("\n🔍 测试状态切换感知:\n")
        log.info("切换 | 新决策      | 上一次决策 | 是否播报")
        log.info("-" * 60")

        for i, (new_decision, offset) in enumerate(transitions):
            last_decision = manager.get_last_decision()

            nav_result = {
                "decision": new_decision,
                "offset": offset,
                "message": f"测试消息：{new_decision}"
            }

            event = manager.build_from_nav(nav_result)

            if event:
                status = "✅ 是"
                decision_str = new_decision
            else:
                status = "❌ 否"
                decision_str = new_decision

            last_str = last_decision if last_decision else "无"
            log.info(f"{i+1:2d}   | {decision_str:12s} | {last_str:10s} | {status}")

            # 模拟时间流逝（避免冷却）
            if i < len(transitions) - 1:
                time.sleep(0.1)

        log.info("\n✅ 状态切换测试完成")
        log.info("\n💡 观察:")
        log.info("   - 相同决策连续时，应该不播报（冷却中）")
        log.info("   - 决策切换时，应该触发播报")

        return True

    except Exception as e:
        log.info(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主函数"""
    log.info("🚀 Navigation Speech Manager 测试开始")
    log.info("=" * 80")

    try:
        # 1. 冷却时间测试
        success1 = test_nav_speech_cooldown()

        if not success1:
            log.info("\n❌ 冷却时间测试失败")
            return 1

        # 2. 优先级测试
        success2 = test_nav_speech_priority()

        if not success2:
            log.info("\n❌ 优先级测试失败")
            return 1

        # 3. 危险场景测试
        success3 = test_nav_speech_danger()

        if not success3:
            log.info("\n❌ 危险场景测试失败")
            return 1

        # 4. 状态切换测试
        success4 = test_nav_speech_state_change()

        if not success4:
            log.info("\n❌ 状态切换测试失败")
            return 1

        log.info(f"\n{'='*80}")
        log.info("🎉 所有测试完成！")
        log.info(f"{'='*80}")
        log.info("\n💡 提示:")
        log.info("   - 修改 core/speech/nav_speech_config.py 可以调整冷却时间和模板")
        log.info("   - 优先级: STOP(3) > HARD_*(2) > SLIGHT_*(1) > FORWARD(0)")
        log.warning("   - 风格: STOP/HARD_* 使用 alert，其他使用 calm")
        log.info("   - 只有 STOP 优先级的事件不可被打断（interruptible=False）")

        return 0

    except KeyboardInterrupt:
        log.info("\n\n👋 用户中断")
        return 0
    except Exception as e:
        log.info(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
























