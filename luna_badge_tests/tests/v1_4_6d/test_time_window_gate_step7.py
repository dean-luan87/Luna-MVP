"""
Step 7: TimeWindowGate + NavigationVoiceRouter 完整测试套件

测试覆盖：
1. TimeWindowGate 单元测试
   - 基本节流行为
   - 时间窗口后恢复
   - safety 与 navigation 独立节流
   - 默认分类允许

2. NavigationVoiceRouter 集成测试（Mock TTS）
   - 转弯提示被节流
   - 安全提示被节流
   - 两类互不影响
   - 时间窗口后恢复播报
   - 不破坏 existing behavior（不影响 adapter 的逻辑）
"""

import sys
import os
import time
import pytest

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from task_engine.tts.routers.time_window_gate import TimeWindowGate
from task_engine.tts.routers.navigation_voice_router import NavigationVoiceRouter


# -----------------------------
# Mock TTS Manager
# -----------------------------
class MockTTS:
    """模拟 TTS Manager，用于测试"""

    def __init__(self):
        self.history = []
        self.queue = []

    def enqueue(self, utterance):
        """模拟 enqueue 行为"""
        self.history.append(utterance.text if hasattr(utterance, 'text') else str(utterance))
        self.queue.append(utterance)

    def speak(self, text=None, **kwargs):
        """模拟 speak 行为（向后兼容）"""
        self.history.append(text)

    def get_queue(self):
        """获取队列"""
        return self.queue

    def clear(self):
        """清空历史"""
        self.history = []
        self.queue = []


# -----------------------------
# Test: TimeWindowGate 基础行为
# -----------------------------
def test_safety_rate_limit_basic():
    """测试安全播报的基本节流行为"""
    gate = TimeWindowGate(safety_window=0.3)

    # 第一次允许
    assert gate.allow("SAFETY") is True

    # 窗口内不允许
    assert gate.allow("SAFETY") is False

    time.sleep(0.31)
    assert gate.allow("SAFETY") is True


def test_navigation_rate_limit_basic():
    """测试导航播报的基本节流行为"""
    gate = TimeWindowGate(navigation_window=0.4)

    assert gate.allow("NAVIGATION") is True

    # 窗口内拒绝
    assert gate.allow("NAVIGATION") is False

    time.sleep(0.41)
    assert gate.allow("NAVIGATION") is True


def test_independent_windows():
    """测试 safety 与 navigation 独立节流"""
    gate = TimeWindowGate(safety_window=0.2, navigation_window=0.5)

    # SAFETY 首次执行
    assert gate.allow("SAFETY") is True
    # NAVIGATION 不受 SAFETY 影响
    assert gate.allow("NAVIGATION") is True

    # SAFETY 会被拒绝
    assert gate.allow("SAFETY") is False
    # NAVIGATION 会被拒绝
    assert gate.allow("NAVIGATION") is False

    time.sleep(0.25)
    # SAFETY 恢复
    assert gate.allow("SAFETY") is True
    # NAVIGATION 仍不行
    assert gate.allow("NAVIGATION") is False

    time.sleep(0.30)
    assert gate.allow("NAVIGATION") is True


def test_default_allow_other_category():
    """测试默认分类允许（不受节流限制）"""
    gate = TimeWindowGate()

    assert gate.allow("OTHER") is True
    assert gate.allow("RANDOM_TYPE") is True
    assert gate.allow("TASK") is True
    assert gate.allow("CHAT") is True
    assert gate.allow("SYSTEM") is True


# -----------------------------
# Integration Test: NavigationVoiceRouter
# -----------------------------
def test_navigation_voice_router_throttle_turn():
    """测试 NavigationVoiceRouter 的转弯提示被节流"""
    mock = MockTTS()
    router = NavigationVoiceRouter(tts_manager_instance=mock)
    router.reset()

    # 第一次 turn 应被执行
    router.route_turn(direction="左转", distance=5)
    assert len(mock.history) == 1

    # 第二次立即执行应被节流
    router.route_turn(direction="左转", distance=5)
    assert len(mock.history) == 1


def test_navigation_voice_router_turn_recover():
    """测试 NavigationVoiceRouter 的转弯提示在时间窗口后恢复"""
    mock = MockTTS()
    router = NavigationVoiceRouter(tts_manager_instance=mock)
    router.reset()

    router.route_turn("左转", distance=5)
    assert len(mock.history) == 1

    time.sleep(router.gate.navigation_window + 0.05)
    router.route_turn("左转", distance=5)

    assert len(mock.history) == 2


def test_navigation_voice_router_safety_throttling():
    """测试 NavigationVoiceRouter 的安全提示被节流"""
    mock = MockTTS()
    router = NavigationVoiceRouter(tts_manager_instance=mock)
    router.reset()

    router.route_obstacle_warning(direction="前方", distance_m=10)
    assert len(mock.history) == 1

    # 窗口内，忽略
    router.route_obstacle_warning(direction="前方", distance_m=10)
    assert len(mock.history) == 1


def test_safety_and_navigation_independent():
    """测试安全播报和导航播报的时间窗口相互独立"""
    mock = MockTTS()
    router = NavigationVoiceRouter(tts_manager_instance=mock)
    router.reset()

    # SAFETY
    router.route_obstacle_warning(direction="前方")
    assert len(mock.history) == 1

    # NAVIGATION 不受影响
    router.route_turn("右转", distance=3)
    assert len(mock.history) == 2

    # SAFETY 被节流
    router.route_obstacle_warning(direction="左侧")
    assert len(mock.history) == 2

    # NAVIGATION 被节流
    router.route_turn("左转", distance=5)
    assert len(mock.history) == 2


def test_generic_route_throttle():
    """测试通用路由方法的时间窗口节流"""
    mock = MockTTS()
    router = NavigationVoiceRouter(tts_manager_instance=mock)
    router.reset()

    router.route_generic("NAVIGATION", "直行30米")
    assert len(mock.history) == 1

    router.route_generic("NAVIGATION", "直行30米")
    assert len(mock.history) == 1

    time.sleep(router.gate.navigation_window + 0.05)
    router.route_generic("NAVIGATION", "直行30米")
    assert len(mock.history) == 2


def test_generic_route_safety_throttle():
    """测试通用路由方法的安全类别节流"""
    mock = MockTTS()
    router = NavigationVoiceRouter(tts_manager_instance=mock)
    router.reset()

    router.route_generic("SAFETY", "前方有危险")
    assert len(mock.history) == 1

    router.route_generic("SAFETY", "前方有障碍物")
    assert len(mock.history) == 1

    time.sleep(router.gate.safety_window + 0.05)
    router.route_generic("SAFETY", "前方有台阶")
    assert len(mock.history) == 2


def test_route_straight_throttle():
    """测试直行提示的时间窗口节流"""
    mock = MockTTS()
    router = NavigationVoiceRouter(tts_manager_instance=mock)
    router.reset()

    router.route_straight(distance=100)
    assert len(mock.history) == 1

    router.route_straight(distance=50)
    assert len(mock.history) == 1

    time.sleep(router.gate.navigation_window + 0.05)
    router.route_straight()
    assert len(mock.history) == 2


def test_does_not_break_adapter_logic():
    """测试节流系统不影响 adapter 的逻辑"""
    mock = MockTTS()
    router = NavigationVoiceRouter(tts_manager_instance=mock)
    router.reset()

    # 第一次播报：通过
    router.route_turn("左转", distance=50)
    assert len(mock.history) == 1
    assert "左转" in mock.history[0]

    # 被节流：不播报
    router.route_turn("右转", distance=30)
    assert len(mock.history) == 1  # 没有新增

    # 等待窗口后：播报
    time.sleep(router.gate.navigation_window + 0.05)
    router.route_turn("直行")
    assert len(mock.history) == 2
    assert "直行" in mock.history[1]

    # 验证 adapter 的逻辑没有被破坏（文本内容正确）
    assert "左转" in mock.history[0]
    assert "直行" in mock.history[1]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])












