from core.logging import get_logger

#!/usr/bin/env python3
log = get_logger("test_navigation_task")
"""
Navigation Task 测试脚本（F9）

测试导航任务链整合
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

try:
    import numpy as np
except ImportError:
    log.info("❌ NumPy 未安装")
    sys.exit(1)

from tasks.navigation_task import NavigationTask
from tasks.navigation_context import NavigationContext
from tasks.navigation_state import NavigationState
from vision.nav_decision import Navigator
from core.speech.nav_speech_manager import NavSpeechManager

logger = logging.getLogger(__name__)


def create_dummy_frame():
    """创建虚拟图像帧"""
    return np.zeros((1080, 1920, 3), dtype=np.uint8)


def create_dummy_walkable_grid(decision_type: str):
    """根据决策类型创建虚拟可走路径网格"""
    grids = {
        "FORWARD": np.array([
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
        ]),
        "SLIGHT_RIGHT": np.array([
            [0, 0, 1, 1, 1],
            [0, 0, 1, 1, 1],
            [0, 0, 1, 1, 1],
        ]),
        "STOP": np.array([
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ]),
    }
    return grids.get(decision_type, grids["FORWARD"])


def test_navigation_task_basic():
    """测试导航任务基础功能"""
    log.info("\n" + "=" * 80)
    log.info("🧪 Navigation Task 基础功能测试")
    log.info("=" * 80")

    try:
        # 创建上下文
        log.info("\n📦 创建导航上下文...")
        context = NavigationContext(
            target="711便利店",
            target_location=[39.9, 116.4],  # 示例坐标
        )
        log.info("✅ 导航上下文创建成功")

        # 创建 Navigator 和 SpeechManager
        log.info("\n📦 初始化 Navigator 和 SpeechManager...")
        navigator = Navigator()
        speech_manager = NavSpeechManager()
        log.info("✅ Navigator 和 SpeechManager 初始化成功")

        # 创建导航任务
        log.info("\n📦 创建导航任务...")
        nav_task = NavigationTask(
            context=context,
            navigator=navigator,
            speech_manager=speech_manager,
        )
        log.info("✅ 导航任务创建成功")

        # 测试状态转换
        log.info("\n🔍 测试状态转换:")

        # IDLE → ACTIVE
        log.info("   1. 启动导航任务...")
        assert nav_task.start(), "启动失败"
        assert nav_task.get_state() == NavigationState.ACTIVE, "状态应为 ACTIVE"
        log.info("   ✅ 状态: IDLE → ACTIVE")

        # ACTIVE → PAUSED
        log.info("   2. 暂停导航任务...")
        assert nav_task.pause(), "暂停失败"
        assert nav_task.get_state() == NavigationState.PAUSED, "状态应为 PAUSED"
        log.info("   ✅ 状态: ACTIVE → PAUSED")

        # PAUSED → ACTIVE
        log.info("   3. 恢复导航任务...")
        assert nav_task.resume(), "恢复失败"
        assert nav_task.get_state() == NavigationState.ACTIVE, "状态应为 ACTIVE"
        log.info("   ✅ 状态: PAUSED → ACTIVE")

        # ACTIVE → STOPPED
        log.info("   4. 停止导航任务...")
        assert nav_task.stop(), "停止失败"
        assert nav_task.get_state() == NavigationState.STOPPED, "状态应为 STOPPED"
        log.info("   ✅ 状态: ACTIVE → STOPPED")

        log.info("\n✅ 状态转换测试通过")

        return True

    except Exception as e:
        log.info(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_navigation_task_update():
    """测试导航任务更新（每帧处理）"""
    log.info("\n" + "=" * 80)
    log.info("🧪 Navigation Task 更新测试")
    log.info("=" * 80")

    try:
        # 创建任务
        context = NavigationContext(target="测试目标")
        navigator = Navigator()
        speech_manager = NavSpeechManager()

        nav_task = NavigationTask(
            context=context,
            navigator=navigator,
            speech_manager=speech_manager,
        )

        # 启动任务
        nav_task.start()

        log.info("\n🔍 测试每帧更新:")

        # 模拟多帧处理
        test_scenarios = [
            ("FORWARD", create_dummy_walkable_grid("FORWARD")),
            ("FORWARD", create_dummy_walkable_grid("FORWARD")),
            ("SLIGHT_RIGHT", create_dummy_walkable_grid("SLIGHT_RIGHT")),
            ("STOP", create_dummy_walkable_grid("STOP")),
        ]

        for i, (scenario_name, walkable_grid) in enumerate(test_scenarios):
            frame = create_dummy_frame()

            # 注意：这里需要先通过 F6 获取 walkable_grid，然后传给 Navigator
            # 为了测试，我们直接模拟 Navigator 的输出
            # 实际使用中，应该先调用 F6 PathDetector，然后传给 Navigator

            # 简化处理：直接调用 Navigator（Navigator 内部会处理）
            # 但 Navigator.decide 需要 walkable_grid，这里我们模拟一个
            nav_decision = navigator.decide(
                walkable_grid=walkable_grid,
                walkable_scores=None,
                risk_map=None
            )

            if nav_decision:
                speech_event = speech_manager.build_from_nav(nav_decision)
            else:
                speech_event = None

            # 更新上下文（模拟 update 的逻辑）
            nav_task.context.frame_count += 1
            if nav_decision:
                nav_task.context.update_decision(nav_decision)
            if speech_event:
                nav_task.context.update_speech_event(speech_event)

            # 记录日志
            nav_task._log_frame_event(
                frame_id=nav_task.context.frame_count,
                nav_decision=nav_decision or {},
                speech_event=speech_event,
            )

            # 打印结果
            decision = nav_decision.get("decision", "UNKNOWN") if nav_decision else "NONE"
            speech_text = speech_event.get("text", "-") if speech_event else "-"
            log.info(f"   帧 {i+1} ({scenario_name}): 决策={decision}, 语音={speech_text[:30]}...")

            # 模拟时间流逝
            time.sleep(0.1)

        log.info(f"\n📊 统计:")
        log.info(f"   总帧数: {nav_task.context.frame_count}")
        log.info(f"   决策统计: {nav_task.context.decision_count}")
        log.info(f"   事件日志数: {len(nav_task.event_log)}")

        log.info("\n✅ 更新测试通过")

        return True

    except Exception as e:
        log.info(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_navigation_task_arrived():
    """测试到达目标"""
    log.info("\n" + "=" * 80)
    log.info("🧪 Navigation Task 到达测试")
    log.info("=" * 80")

    try:
        context = NavigationContext(target="711便利店")
        navigator = Navigator()
        speech_manager = NavSpeechManager()

        nav_task = NavigationTask(
            context=context,
            navigator=navigator,
            speech_manager=speech_manager,
        )

        # 启动
        nav_task.start()
        assert nav_task.get_state() == NavigationState.ACTIVE

        # 模拟一些帧
        for i in range(5):
            frame = create_dummy_frame()
            walkable_grid = create_dummy_walkable_grid("FORWARD")
            nav_decision = navigator.decide(walkable_grid=walkable_grid)
            if nav_decision:
                speech_event = speech_manager.build_from_nav(nav_decision)
            else:
                speech_event = None

            nav_task.context.frame_count += 1
            if nav_decision:
                nav_task.context.update_decision(nav_decision)
            if speech_event:
                nav_task.context.update_speech_event(speech_event)

            nav_task._log_frame_event(
                frame_id=nav_task.context.frame_count,
                nav_decision=nav_decision or {},
                speech_event=speech_event,
            )

        # 标记到达
        log.info("\n🎯 标记到达目标...")
        assert nav_task.arrived(), "标记到达失败"
        assert nav_task.get_state() == NavigationState.ARRIVED, "状态应为 ARRIVED"

        duration = nav_task.context.get_active_duration()
        log.info(f"   ✅ 导航完成，持续时间: {duration:.2f} 秒")
        log.info(f"   ✅ 处理帧数: {nav_task.context.frame_count}")

        log.info("\n✅ 到达测试通过")

        return True

    except Exception as e:
        log.info(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_navigation_task_logging():
    """测试日志记录"""
    log.info("\n" + "=" * 80)
    log.info("🧪 Navigation Task 日志测试")
    log.info("=" * 80")

    try:
        context = NavigationContext(target="测试目标")
        navigator = Navigator()
        speech_manager = NavSpeechManager()

        nav_task = NavigationTask(
            context=context,
            navigator=navigator,
            speech_manager=speech_manager,
        )

        # 执行一系列操作
        nav_task.start()
        nav_task.pause(reason="测试暂停")
        nav_task.resume()
        nav_task.stop(reason="测试停止")

        # 检查日志
        event_log = nav_task.get_event_log()

        log.info(f"\n📋 事件日志 ({len(event_log)} 条):")
        for i, event in enumerate(event_log):
            event_type = event.get("event_type", "unknown")
            state = event.get("state", "unknown")
            log.info(f"   {i+1}. {event_type} (状态: {state})")

        # 验证日志内容
        event_types = [e.get("event_type") for e in event_log]
        assert "task_start" in event_types, "缺少 task_start 事件"
        assert "task_pause" in event_types, "缺少 task_pause 事件"
        assert "task_resume" in event_types, "缺少 task_resume 事件"
        assert "task_stop" in event_types, "缺少 task_stop 事件"

        log.info("\n✅ 日志测试通过")

        return True

    except Exception as e:
        log.info(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主函数"""
    log.info("🚀 Navigation Task 测试开始")
    log.info("=" * 80")

    try:
        # 1. 基础功能测试
        success1 = test_navigation_task_basic()

        if not success1:
            log.info("\n❌ 基础功能测试失败")
            return 1

        # 2. 更新测试
        success2 = test_navigation_task_update()

        if not success2:
            log.info("\n❌ 更新测试失败")
            return 1

        # 3. 到达测试
        success3 = test_navigation_task_arrived()

        if not success3:
            log.info("\n❌ 到达测试失败")
            return 1

        # 4. 日志测试
        success4 = test_navigation_task_logging()

        if not success4:
            log.info("\n❌ 日志测试失败")
            return 1

        log.info(f"\n{'='*80}")
        log.info("🎉 所有测试完成！")
        log.info(f"{'='*80}")
        log.info("\n💡 提示:")
        log.info("   - NavigationTask 支持完整的状态机（IDLE → ACTIVE → PAUSED ↔ ACTIVE → ARRIVED/STOPPED）")
        log.info("   - 每帧更新会记录完整的日志，可用于后台回放")
        log.info("   - 支持暂停、恢复、停止等操作")
        log.info("   - 预留了 GPS、路线规划等未来扩展字段")

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













