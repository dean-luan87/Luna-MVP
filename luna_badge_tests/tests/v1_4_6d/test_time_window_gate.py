"""
测试 Time Window Gate: 播报节流控制器
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


def test_safety_window_throttling():
    """测试安全播报的时间窗口节流"""
    gate = TimeWindowGate(safety_window=0.8)
    gate.reset()

    # 第一次：允许
    assert gate.allow("SAFETY") is True

    # 立即再次：被节流
    assert gate.allow("SAFETY") is False

    # 等待超过窗口后：允许
    time.sleep(0.9)
    assert gate.allow("SAFETY") is True


def test_navigation_window_throttling():
    """测试导航播报的时间窗口节流"""
    gate = TimeWindowGate(navigation_window=2.0)
    gate.reset()

    # 第一次：允许
    assert gate.allow("NAVIGATION") is True

    # 立即再次：被节流
    assert gate.allow("NAVIGATION") is False

    # 等待超过窗口后：允许
    time.sleep(2.1)
    assert gate.allow("NAVIGATION") is True


def test_different_categories_independent():
    """测试不同类别的时间窗口相互独立"""
    gate = TimeWindowGate(safety_window=0.8, navigation_window=2.0)
    gate.reset()

    # 安全播报
    assert gate.allow("SAFETY") is True
    assert gate.allow("SAFETY") is False  # 被节流

    # 导航播报不受影响（独立窗口）
    assert gate.allow("NAVIGATION") is True
    assert gate.allow("NAVIGATION") is False  # 被节流

    # 等待安全窗口后，安全可以再次播报
    time.sleep(0.9)
    assert gate.allow("SAFETY") is True
    assert gate.allow("NAVIGATION") is False  # 导航窗口未到


def test_other_categories_always_allowed():
    """测试其他类别（TASK / CHAT / SYSTEM）不受限制"""
    gate = TimeWindowGate()
    gate.reset()

    # 其他类别始终允许
    assert gate.allow("TASK") is True
    assert gate.allow("TASK") is True
    assert gate.allow("CHAT") is True
    assert gate.allow("SYSTEM") is True
    assert gate.allow("UNKNOWN") is True


def test_reset_clears_timestamps():
    """测试 reset 清除时间戳"""
    gate = TimeWindowGate()
    gate.reset()

    # 播报一次
    gate.allow("SAFETY")
    gate.allow("NAVIGATION")

    # 重置
    gate.reset()

    # 重置后应该立即允许
    assert gate.allow("SAFETY") is True
    assert gate.allow("NAVIGATION") is True


def test_get_last_time():
    """测试获取最后播报时间（通过直接访问内部状态）"""
    gate = TimeWindowGate()
    gate.reset()

    # 初始状态
    assert gate.last_safety_time == 0.0
    assert gate.last_navigation_time == 0.0

    # 播报后
    gate.allow("SAFETY")
    gate.allow("NAVIGATION")

    # 应该有时间戳
    assert gate.last_safety_time > 0
    assert gate.last_navigation_time > 0


def test_custom_window_sizes():
    """测试自定义窗口大小"""
    gate = TimeWindowGate(safety_window=1.5, navigation_window=3.0)
    gate.reset()

    # 安全播报
    assert gate.allow("SAFETY") is True
    assert gate.allow("SAFETY") is False

    # 等待 1.5 秒后允许
    time.sleep(1.6)
    assert gate.allow("SAFETY") is True

    # 导航播报
    assert gate.allow("NAVIGATION") is True
    assert gate.allow("NAVIGATION") is False

    # 等待 3.0 秒后允许
    time.sleep(3.1)
    assert gate.allow("NAVIGATION") is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

