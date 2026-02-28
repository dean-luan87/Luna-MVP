"""
测试 NavigationVoiceRouter: 导航语音路由器
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
from task_engine.tts import Utterance


def make_u(text: str, category: str, priority: int = None) -> Utterance:
    """辅助函数：创建测试用的 Utterance"""
    return Utterance(
        text=text,
        level="info",
        channel="tts",
        priority=priority,
        meta={"category": category, "ttscategory": category.lower()},
    )


def test_safety_drops_navigation_in_same_batch():
    """测试安全播报在同批次中优先于导航播报"""
    router = NavigationVoiceRouter()
    router.reset()

    u_nav = make_u("前方 50 米左转", "NAVIGATION", priority=75)
    u_safe = make_u("前方有障碍物！", "SAFETY", priority=80)

    out = router.route_batch([u_nav, u_safe])

    assert len(out) == 1
    assert out[0].text == "前方有障碍物！"
    assert out[0].interrupt is True
    assert out[0].priority >= 80


def test_navigation_suppressed_shortly_after_safety():
    """测试安全播报后短时间内抑制导航播报"""
    state = NavigationVoiceRouterState()
    router = NavigationVoiceRouter(
        config=NavigationVoiceRouterConfig(safety_silence_window=2.0),
        state=state,
    )

    # 第一次：安全播报
    out1 = router.route_batch([make_u("危险！", "SAFETY")])
    assert len(out1) == 1
    assert router.state.last_safety_ts > 0

    # 立即跟一个导航播报，应被抑制
    out2 = router.route_batch([make_u("前方 50 米左转", "NAVIGATION")])
    assert len(out2) == 0

    # 等待超过 silence_window 后，导航播报恢复
    time.sleep(2.1)
    out3 = router.route_batch([make_u("前方 30 米右转", "NAVIGATION")])
    assert len(out3) == 1
    assert out3[0].text == "前方 30 米右转"


def test_chat_can_pass_during_safety_window():
    """测试安全窗口内 CHAT 可以穿透（如果配置允许）"""
    state = NavigationVoiceRouterState()
    router = NavigationVoiceRouter(
        config=NavigationVoiceRouterConfig(
            safety_silence_window=2.0,
            enable_chat_during_safety_window=True,
        ),
        state=state,
    )

    # 安全播报
    router.route_batch([make_u("危险！", "SAFETY")])

    # 安全窗口内，NAVIGATION 被抑制，CHAT 通过
    nav = make_u("前方 50 米左转", "NAVIGATION")
    chat = make_u("我们继续加油", "CHAT")

    out = router.route_batch([nav, chat])
    assert len(out) == 1
    assert out[0].text == "我们继续加油"


def test_chat_blocked_if_config_disabled():
    """测试配置禁止时，安全窗口内 CHAT 也被阻止"""
    state = NavigationVoiceRouterState()
    router = NavigationVoiceRouter(
        config=NavigationVoiceRouterConfig(
            safety_silence_window=2.0,
            enable_chat_during_safety_window=False,
        ),
        state=state,
    )

    # 安全播报
    router.route_batch([make_u("危险！", "SAFETY")])

    nav = make_u("前方 50 米左转", "NAVIGATION")
    chat = make_u("今天天气不错", "CHAT")

    out = router.route_batch([nav, chat])
    # NAVIGATION 被抑制，CHAT 也被配置禁止 -> 全部丢弃
    assert len(out) == 0


def test_multiple_safety_selects_highest_priority():
    """测试多个安全播报时选择优先级最高的"""
    router = NavigationVoiceRouter()
    router.reset()

    u1 = make_u("前方有障碍物", "SAFETY", priority=85)
    u2 = make_u("前方有台阶", "SAFETY", priority=90)
    u3 = make_u("前方人多", "SAFETY", priority=80)

    out = router.route_batch([u1, u2, u3])
    assert len(out) == 1
    assert out[0].text == "前方有台阶"
    assert out[0].priority == 90


def test_safety_priority_tie_selects_earliest():
    """测试优先级相同时选择最早创建的"""
    router = NavigationVoiceRouter()
    router.reset()

    import time
    t1 = time.time()
    u1 = Utterance(
        text="障碍物1",
        priority=90,
        created_at=t1,
        meta={"category": "SAFETY", "ttscategory": "safety"},
    )
    time.sleep(0.01)
    u2 = Utterance(
        text="障碍物2",
        priority=90,
        created_at=time.time(),
        meta={"category": "SAFETY", "ttscategory": "safety"},
    )

    out = router.route_batch([u2, u1])  # u2 在后面但时间更晚
    assert len(out) == 1
    assert out[0].text == "障碍物1"  # 应该选择更早的 u1


def test_normal_flow_all_pass():
    """测试正常流程：没有安全播报时，所有类别都通过"""
    router = NavigationVoiceRouter()
    router.reset()

    nav = make_u("前方 50 米左转", "NAVIGATION")
    task = make_u("导航已开始", "TASK")
    chat = make_u("今天天气不错", "CHAT")

    out = router.route_batch([nav, task, chat])
    assert len(out) == 3


def test_route_and_speak_integrates_with_tts_manager():
    """测试 route_and_speak 与 tts_manager 集成"""
    from task_engine.tts import tts_manager
    router = NavigationVoiceRouter()
    router.reset()
    tts_manager.clear()

    u1 = make_u("前方有障碍物", "SAFETY")
    u2 = make_u("前方 50 米左转", "NAVIGATION")

    router.route_and_speak([u1, u2])

    # 应该只有安全播报进入队列
    queue = tts_manager.get_queue()
    assert len(queue) == 1
    assert queue[0].text == "前方有障碍物"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])












