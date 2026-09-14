"""
测试 NavigationVoiceRouter 与 Time Window Gate 的集成
"""

import sys
import os
import time
import pytest

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from task_engine.navigation.navigation_voice_router import (
    NavigationVoiceRouter,
    NavigationVoiceRouterConfig,
    NavigationVoiceRouterState,
)
from task_engine.tts.routers.time_window_gate import TimeWindowGate
from task_engine.tts import Utterance, tts_manager


def make_u(text: str, category: str, priority: int = None) -> Utterance:
    """辅助函数：创建测试用的 Utterance"""
    return Utterance(
        text=text,
        level="info",
        channel="tts",
        priority=priority,
        meta={"category": category, "ttscategory": category.lower()},
    )


def test_safety_throttled_by_time_window():
    """测试安全播报被时间窗口节流"""
    gate = TimeWindowGate(safety_window=0.8)
    router = NavigationVoiceRouter(time_window_gate=gate)
    router.reset()
    tts_manager.clear()

    # 第一次安全播报：通过
    u1 = make_u("前方有障碍物", "SAFETY", priority=90)
    routed1 = router.route_batch([u1])
    assert len(routed1) == 1

    # 立即第二次安全播报：被节流
    u2 = make_u("前方有台阶", "SAFETY", priority=90)
    routed2 = router.route_batch([u2])
    assert len(routed2) == 0

    # 等待超过窗口后：通过
    time.sleep(0.9)
    u3 = make_u("前方有障碍物", "SAFETY", priority=90)
    routed3 = router.route_batch([u3])
    assert len(routed3) == 1


def test_navigation_throttled_by_time_window():
    """测试导航播报被时间窗口节流"""
    gate = TimeWindowGate(navigation_window=2.0)
    router = NavigationVoiceRouter(time_window_gate=gate)
    router.reset()
    tts_manager.clear()

    # 第一次导航播报：通过
    u1 = make_u("前方 50 米左转", "NAVIGATION", priority=75)
    routed1 = router.route_batch([u1])
    assert len(routed1) == 1

    # 立即第二次导航播报：被节流
    u2 = make_u("前方 30 米右转", "NAVIGATION", priority=75)
    routed2 = router.route_batch([u2])
    assert len(routed2) == 0

    # 等待超过窗口后：通过
    time.sleep(2.1)
    u3 = make_u("前方 20 米直行", "NAVIGATION", priority=75)
    routed3 = router.route_batch([u3])
    assert len(routed3) == 1


def test_safety_and_navigation_independent():
    """测试安全播报和导航播报的时间窗口相互独立"""
    gate = TimeWindowGate(safety_window=0.8, navigation_window=2.0)
    # 使用较短的安全静默窗口，避免干扰时间窗口测试
    config = NavigationVoiceRouterConfig(safety_silence_window=1.0)
    router = NavigationVoiceRouter(time_window_gate=gate, config=config)
    router.reset()
    tts_manager.clear()

    # 安全播报
    u_safe1 = make_u("前方有障碍物", "SAFETY", priority=90)
    routed1 = router.route_batch([u_safe1])
    assert len(routed1) == 1

    # 安全播报被节流
    u_safe2 = make_u("前方有台阶", "SAFETY", priority=90)
    routed2 = router.route_batch([u_safe2])
    assert len(routed2) == 0

    # 等待安全静默窗口结束后，导航播报可以播报（但会被时间窗口节流）
    time.sleep(1.1)  # 超过安全静默窗口（1.0s）
    u_nav1 = make_u("前方 50 米左转", "NAVIGATION", priority=75)
    routed3 = router.route_batch([u_nav1])
    assert len(routed3) == 1

    # 导航播报被时间窗口节流
    u_nav2 = make_u("前方 30 米右转", "NAVIGATION", priority=75)
    routed4 = router.route_batch([u_nav2])
    assert len(routed4) == 0

    # 等待安全时间窗口后，安全可以再次播报
    time.sleep(0.9)  # 总共等待 2.0s，超过安全时间窗口（0.8s）
    u_safe3 = make_u("前方有障碍物", "SAFETY", priority=90)
    routed5 = router.route_batch([u_safe3])
    assert len(routed5) == 1

    # 导航窗口未到（总共 2.0s，导航窗口是 2.0s），仍然被节流
    u_nav3 = make_u("前方 20 米直行", "NAVIGATION", priority=75)
    routed6 = router.route_batch([u_nav3])
    assert len(routed6) == 0


def test_safety_priority_overrides_time_window():
    """测试安全播报的优先级仍然高于导航播报（即使被节流）"""
    gate = TimeWindowGate(safety_window=0.8, navigation_window=2.0)
    router = NavigationVoiceRouter(time_window_gate=gate)
    router.reset()
    tts_manager.clear()

    # 安全播报
    u_safe = make_u("前方有障碍物", "SAFETY", priority=90)
    u_nav = make_u("前方 50 米左转", "NAVIGATION", priority=75)

    # 同批次：安全优先
    routed = router.route_batch([u_nav, u_safe])
    assert len(routed) == 1
    assert routed[0].text == "前方有障碍物"

    # 立即再次：安全被节流，但导航也被安全静默窗口抑制
    routed2 = router.route_batch([u_nav])
    assert len(routed2) == 0  # 被安全静默窗口抑制


def test_route_and_speak_with_time_window():
    """测试 route_and_speak 与时间窗口的集成"""
    gate = TimeWindowGate(safety_window=0.8, navigation_window=2.0)
    router = NavigationVoiceRouter(time_window_gate=gate)
    router.reset()
    tts_manager.clear()

    # 第一次播报
    u1 = make_u("前方有障碍物", "SAFETY", priority=90)
    router.route_and_speak([u1])
    queue1 = tts_manager.get_queue()
    assert len(queue1) == 1

    # 立即第二次：被节流
    u2 = make_u("前方有台阶", "SAFETY", priority=90)
    router.route_and_speak([u2])
    queue2 = tts_manager.get_queue()
    assert len(queue2) == 1  # 队列长度不变（没有新增）

    # 等待超过窗口后：通过
    time.sleep(0.9)
    u3 = make_u("前方有障碍物", "SAFETY", priority=90)
    router.route_and_speak([u3])
    queue3 = tts_manager.get_queue()
    assert len(queue3) == 2  # 新增一条


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

