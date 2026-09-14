from core.logging import get_logger

#!/usr/bin/env python3
log = get_logger("test_navigation_pipeline")
"""
Navigation Pipeline 测试脚本（F10）

测试完整的导航流水线（F1-F10 整合）
"""

import sys
import os
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
    import cv2
    import numpy as np
except ImportError:
    log.info("❌ OpenCV 或 NumPy 未安装")
    sys.exit(1)

from core.runtime.app_controller import AppController
from core.runtime.navigation_engine import NavigationEngine
from tasks.navigation_context import NavigationContext
from tasks.navigation_task import NavigationTask

logger = logging.getLogger(__name__)


def create_test_frame():
    """创建测试图像帧"""
    # 创建一个简单的测试图像
    frame = np.ones((1080, 1920, 3), dtype=np.uint8) * 128
    
    # 添加一些内容（模拟实际场景）
    # 底部：地面
    frame[800:, :] = [140, 140, 140]
    
    # 中间：可走路径
    cv2.rectangle(frame, (640, 200), (1280, 800), [160, 160, 160], -1)
    
    # 左侧：障碍
    cv2.rectangle(frame, (0, 300), (400, 700), [50, 50, 50], -1)
    
    return frame


def test_navigation_engine():
    """测试导航引擎"""
    log.info("\n" + "=" * 80)
    log.info("🧪 Navigation Engine 测试")
    log.info("=" * 80")

    try:
        # 创建导航引擎
        log.info("\n📦 正在初始化 NavigationEngine...")
        engine = NavigationEngine()
        log.info("✅ NavigationEngine 初始化成功")

        # 创建测试图像
        log.info("\n🖼️ 创建测试图像...")
        test_frame = create_test_frame()
        log.info(f"✅ 测试图像创建成功: {test_frame.shape}")

        # 处理图像
        log.info("\n🔧 正在处理图像...")
        result = engine.process_frame(test_frame)

        if result:
            log.info("✅ 导航引擎处理成功")

            nav_result = result.get("nav_result")
            speech_event = result.get("speech_event")

            if nav_result:
                log.info(f"\n📊 导航决策:")
                log.info(f"   决策: {nav_result.get('decision')}")
                log.info(f"   偏移: {nav_result.get('offset')}")
                log.info(f"   消息: {nav_result.get('message')}")

            if speech_event:
                log.info(f"\n🗣️ 语音事件:")
                log.info(f"   文本: {speech_event.get('text')}")
                log.info(f"   风格: {speech_event.get('style')}")
                log.info(f"   优先级: {speech_event.get('priority')}")

            log.info(f"\n📈 中间数据:")
            log.info(f"   walkable_grid: {result.get('walkable_grid') is not None}")
            log.info(f"   risk_map: {result.get('risk_map') is not None}")

            return True
        else:
            log.info("❌ 导航引擎处理失败")
            return False

    except Exception as e:
        log.info(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_navigation_task_with_engine():
    """测试导航任务（使用 NavigationEngine）"""
    log.info("\n" + "=" * 80)
    log.info("🧪 Navigation Task + Engine 测试")
    log.info("=" * 80")

    try:
        # 创建导航引擎
        log.info("\n📦 正在初始化 NavigationEngine...")
        engine = NavigationEngine()
        log.info("✅ NavigationEngine 初始化成功")

        # 创建上下文
        log.info("\n📦 创建导航上下文...")
        context = NavigationContext(
            target="测试目标",
            target_location=[39.9, 116.4],
        )
        log.info("✅ 导航上下文创建成功")

        # 创建 TTS 管理器（虚拟）
        from core.runtime.app_controller import DummyTTS
        tts = DummyTTS()

        # 创建导航任务
        log.info("\n📦 创建导航任务（使用 NavigationEngine）...")
        nav_task = NavigationTask(
            context=context,
            navigation_engine=engine,
            tts_manager=tts,
        )
        log.info("✅ 导航任务创建成功")

        # 启动任务
        log.info("\n🚀 启动导航任务...")
        assert nav_task.start(), "启动失败"
        log.info("✅ 导航任务已启动")

        # 处理几帧
        log.info("\n🔧 处理测试帧...")
        for i in range(3):
            frame = create_test_frame()
            speech_event = nav_task.update(frame)
            
            if speech_event:
                log.info(f"   帧 {i+1}: 语音={speech_event.get('text', '')[:30]}...")
            else:
                log.info(f"   帧 {i+1}: 无语音事件（可能冷却中）")

        # 暂停
        log.info("\n⏸️ 暂停导航任务...")
        nav_task.pause()
        log.info("✅ 导航任务已暂停")

        # 恢复
        log.info("\n▶️ 恢复导航任务...")
        nav_task.resume()
        log.info("✅ 导航任务已恢复")

        # 停止
        log.info("\n🛑 停止导航任务...")
        nav_task.stop()
        log.info("✅ 导航任务已停止")

        # 检查日志
        event_log = nav_task.get_event_log()
        log.info(f"\n📋 事件日志 ({len(event_log)} 条)")
        for i, event in enumerate(event_log[:5]):  # 只显示前 5 条
            event_type = event.get("event_type", "unknown")
            state = event.get("state", "unknown")
            log.info(f"   {i+1}. {event_type} (状态: {state})")

        return True

    except Exception as e:
        log.info(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_app_controller_demo():
    """测试应用控制器（demo）"""
    log.info("\n" + "=" * 80)
    log.info("🧪 App Controller Demo 测试")
    log.info("=" * 80")

    try:
        # 创建应用控制器
        log.info("\n📦 正在初始化 AppController...")
        controller = AppController(target="测试目的地")
        log.info("✅ AppController 初始化成功")

        log.info("\n💡 注意:")
        log.info("   - 这个测试需要摄像头")
        log.info("   - 如果摄像头不可用，测试将跳过")
        log.info("   - 实际运行时，可以调用 controller.run_navigation_demo()")

        # 检查是否可以打开摄像头
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            log.info("\n⚠️ 摄像头不可用，跳过实际运行测试")
            cap.release()
            return True

        cap.release()

        log.info("\n✅ 摄像头可用，可以运行 demo")
        log.info("   💡 提示: 可以调用 controller.run_navigation_demo() 运行完整 demo")

        return True

    except Exception as e:
        log.info(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_full_pipeline():
    """测试完整流水线（不使用摄像头）"""
    log.info("\n" + "=" * 80)
    log.info("🧪 完整流水线测试（模拟）")
    log.info("=" * 80")

    try:
        # 创建导航引擎
        engine = NavigationEngine()

        # 创建上下文和任务
        context = NavigationContext(target="测试目标")
        from core.runtime.app_controller import DummyTTS
        tts = DummyTTS()

        nav_task = NavigationTask(
            context=context,
            navigation_engine=engine,
            tts_manager=tts,
        )

        # 启动任务
        nav_task.start()

        log.info("\n🔧 模拟处理 10 帧...")

        for i in range(10):
            frame = create_test_frame()
            speech_event = nav_task.update(frame)

            # 模拟时间流逝（避免冷却）
            import time
            time.sleep(0.1)

        # 获取统计信息
        context = nav_task.get_context()
        log.info(f"\n📊 统计信息:")
        log.info(f"   处理帧数: {context.frame_count}")
        log.info(f"   决策统计: {context.decision_count}")
        log.info(f"   事件日志数: {len(nav_task.get_event_log())}")

        # 停止任务
        nav_task.stop()

        log.info("\n✅ 完整流水线测试通过")

        return True

    except Exception as e:
        log.info(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主函数"""
    log.info("🚀 Navigation Pipeline 测试开始")
    log.info("=" * 80")

    import argparse
    parser = argparse.ArgumentParser(description="Navigation Pipeline 测试")
    parser.add_argument(
        "--camera",
        action="store_true",
        help="使用摄像头进行完整 demo 测试",
    )
    args = parser.parse_args()

    try:
        # 1. 导航引擎测试
        success1 = test_navigation_engine()

        if not success1:
            log.info("\n❌ 导航引擎测试失败")
            return 1

        # 2. 导航任务 + 引擎测试
        success2 = test_navigation_task_with_engine()

        if not success2:
            log.info("\n❌ 导航任务 + 引擎测试失败")
            return 1

        # 3. 应用控制器测试
        success3 = test_app_controller_demo()

        if not success3:
            log.info("\n❌ 应用控制器测试失败")
            return 1

        # 4. 完整流水线测试
        success4 = test_full_pipeline()

        if not success4:
            log.info("\n❌ 完整流水线测试失败")
            return 1

        log.info(f"\n{'='*80}")
        log.info("🎉 所有测试完成！")
        log.info(f"{'='*80}")
        log.info("\n💡 提示:")
        log.info("   - NavigationEngine 封装了完整的视觉导航流水线")
        log.info("   - NavigationTask 使用 NavigationEngine 处理每帧")
        log.info("   - AppController 提供了完整 demo 接口")
        log.info("   - 使用 --camera 参数可以运行完整的摄像头 demo")
        log.info("\n📝 运行完整 demo:")
        log.info("   python tests/test_navigation_pipeline.py --camera")

        if args.camera:
            log.info("\n" + "=" * 80)
            log.info("🎬 启动完整摄像头 Demo...")
            log.info("=" * 80")
            controller = AppController(target="测试目的地")
            controller.run_navigation_demo()

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













