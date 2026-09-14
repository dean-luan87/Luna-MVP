"""
测试 TTS Routers 层的 NavigationVoiceRouter

验证按照用户提供的 diff 架构实现的路由器功能
"""

import sys
import os
import time
import pytest

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from task_engine.tts.routers.navigation_voice_router import NavigationVoiceRouter
from task_engine.tts.routers.time_window_gate import TimeWindowGate
from task_engine.tts import tts_manager


def setup_function(_):
    """每个测试前清空状态"""
    tts_manager.clear()


def test_route_turn_with_throttling():
    """测试 route_turn 方法的时间窗口节流"""
    router = NavigationVoiceRouter()
    router.reset()

    # 第一次：通过
    router.route_turn("左转", distance=50)
    queue1 = tts_manager.get_queue()
    assert len(queue1) == 1
    assert "左转" in queue1[0].text

    # 立即第二次：被节流
    tts_manager.clear()
    router.route_turn("右转", distance=30)
    queue2 = tts_manager.get_queue()
    assert len(queue2) == 0

    # 等待超过窗口后：通过
    time.sleep(2.1)
    router.route_turn("直行")
    queue3 = tts_manager.get_queue()
    assert len(queue3) == 1


def test_route_straight_with_throttling():
    """测试 route_straight 方法的时间窗口节流"""
    router = NavigationVoiceRouter()
    router.reset()

    # 第一次：通过
    router.route_straight(distance=100)
    queue1 = tts_manager.get_queue()
    assert len(queue1) == 1

    # 立即第二次：被节流
    tts_manager.clear()
    router.route_straight(distance=50)
    queue2 = tts_manager.get_queue()
    assert len(queue2) == 0

    # 等待超过窗口后：通过
    time.sleep(2.1)
    router.route_straight()
    queue3 = tts_manager.get_queue()
    assert len(queue3) == 1


def test_route_obstacle_warning_with_throttling():
    """测试 route_obstacle_warning 方法的时间窗口节流"""
    router = NavigationVoiceRouter()
    router.reset()

    # 第一次：通过
    router.route_obstacle_warning(direction="前方", distance_m=10)
    queue1 = tts_manager.get_queue()
    assert len(queue1) == 1
    assert "障碍物" in queue1[0].text

    # 立即第二次：被节流
    tts_manager.clear()
    router.route_obstacle_warning(direction="左侧", distance_m=5)
    queue2 = tts_manager.get_queue()
    assert len(queue2) == 0

    # 等待超过窗口后：通过
    time.sleep(0.9)
    router.route_obstacle_warning()
    queue3 = tts_manager.get_queue()
    assert len(queue3) == 1


def test_route_generic_safety():
    """测试 route_generic 方法处理安全类别"""
    router = NavigationVoiceRouter()
    router.reset()

    router.route_generic("SAFETY", "前方有危险")
    queue = tts_manager.get_queue()
    assert len(queue) == 1
    assert queue[0].meta.get("ttscategory") == "safety"


def test_route_generic_navigation():
    """测试 route_generic 方法处理导航类别"""
    router = NavigationVoiceRouter()
    router.reset()

    router.route_generic("NAVIGATION", "前方 50 米左转", direction="左转", distance_m=50)
    queue = tts_manager.get_queue()
    assert len(queue) == 1
    assert queue[0].meta.get("ttscategory") == "navigation"
    assert "左转" in queue[0].text


def test_route_generic_with_throttling():
    """测试 route_generic 方法的时间窗口节流"""
    router = NavigationVoiceRouter()
    router.reset()

    # 第一次：通过
    router.route_generic("NAVIGATION", "前方 50 米左转")
    queue1 = tts_manager.get_queue()
    assert len(queue1) == 1

    # 立即第二次：被节流
    tts_manager.clear()
    router.route_generic("NAVIGATION", "前方 30 米右转")
    queue2 = tts_manager.get_queue()
    assert len(queue2) == 0

    # 等待超过窗口后：通过
    time.sleep(2.1)
    router.route_generic("NAVIGATION", "前方 20 米直行")
    queue3 = tts_manager.get_queue()
    assert len(queue3) == 1


def test_safety_and_navigation_independent():
    """测试安全播报和导航播报的时间窗口相互独立"""
    router = NavigationVoiceRouter()
    router.reset()

    # 安全播报
    router.route_obstacle_warning()
    queue1 = tts_manager.get_queue()
    assert len(queue1) == 1

    # 安全播报被节流
    tts_manager.clear()
    router.route_obstacle_warning()
    queue2 = tts_manager.get_queue()
    assert len(queue2) == 0

    # 导航播报不受影响（独立窗口）
    router.route_turn("左转")
    queue3 = tts_manager.get_queue()
    assert len(queue3) == 1

    # 导航播报被节流
    tts_manager.clear()
    router.route_turn("右转")
    queue4 = tts_manager.get_queue()
    assert len(queue4) == 0


def test_reset_clears_gate():
    """测试 reset 方法清除时间窗口状态"""
    router = NavigationVoiceRouter()
    router.reset()

    # 播报一次
    router.route_turn("左转")
    tts_manager.clear()

    # 立即再次：被节流
    router.route_turn("右转")
    queue1 = tts_manager.get_queue()
    assert len(queue1) == 0

    # 重置后：立即允许
    router.reset()
    router.route_turn("直行")
    queue2 = tts_manager.get_queue()
    assert len(queue2) == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

