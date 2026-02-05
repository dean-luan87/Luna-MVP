"""
测试 NavigationEventPostProcessor: 事件后处理（合并/抑制/去噪）
"""

import sys
import os
import time
import pytest

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from task_engine.navigation.nav_event_post_processor import NavigationEventPostProcessor


def test_cooldown():
    """测试冷却时间：短时间内重复事件被抑制"""
    p = NavigationEventPostProcessor()
    p.reset()

    ev = {"code": "obstacle_front", "distance": 1.0, "type": "danger"}

    # 第一次通过
    out1 = p.process([ev])
    assert len(out1) == 1

    # 立即触发第二次 → 会被冷却阻止
    out2 = p.process([ev])
    assert len(out2) == 0

    # 等待冷却时间后，应该可以通过（但需要改变距离以避免抖动过滤）
    time.sleep(4.1)
    ev3 = {"code": "obstacle_front", "distance": 1.5, "type": "danger"}  # 改变距离
    out3 = p.process([ev3])
    assert len(out3) == 1


def test_jitter_filter():
    """测试抖动过滤：距离变化小于阈值时被抑制"""
    p = NavigationEventPostProcessor()
    p.reset()

    ev1 = {"code": "obstacle_front", "distance": 1.0, "type": "danger"}
    ev2 = {"code": "obstacle_front", "distance": 1.1, "type": "danger"}  # 抖动差 0.1，小于 0.3 阈值

    out1 = p.process([ev1])
    assert len(out1) == 1

    # 立即触发第二次，距离变化太小 → 抖动滤掉
    out2 = p.process([ev2])
    assert len(out2) == 0

    # 等待冷却时间后，距离变化足够大时，应该通过
    time.sleep(4.1)
    ev3 = {"code": "obstacle_front", "distance": 1.5, "type": "danger"}  # 变化 0.5 > 0.3
    out3 = p.process([ev3])
    assert len(out3) == 1


def test_critical_event_override():
    """测试严重事件优先级：严重事件发生时忽略其他事件"""
    p = NavigationEventPostProcessor()
    p.reset()

    evs = [
        {"code": "obstacle_front", "distance": 0.7, "type": "danger"},
        {"code": "stairs_up", "distance": 1.0, "type": "danger"},
    ]

    out = p.process(evs)
    assert len(out) == 1
    assert out[0]["code"] == "obstacle_front"  # 最危险的事件优先


def test_critical_event_selects_closest():
    """测试严重事件选择：多个严重事件时选择距离最近的"""
    p = NavigationEventPostProcessor()
    p.reset()

    evs = [
        {"code": "stairs_down", "distance": 1.5, "type": "danger"},
        {"code": "obstacle_front", "distance": 0.5, "type": "danger"},  # 更近
    ]

    out = p.process(evs)
    assert len(out) == 1
    assert out[0]["code"] == "obstacle_front"
    assert out[0]["distance"] == 0.5


def test_multiple_normal_events_all_pass():
    """测试多个一般事件：都通过冷却和抖动时全部输出"""
    p = NavigationEventPostProcessor()
    p.reset()

    evs = [
        {"code": "road_narrow", "type": "navigation"},
        {"code": "water_puddle", "type": "danger"},
    ]

    out = p.process(evs)
    assert len(out) == 2


def test_critical_blocks_normal():
    """测试严重事件阻塞一般事件"""
    p = NavigationEventPostProcessor()
    p.reset()

    evs = [
        {"code": "road_narrow", "type": "navigation"},
        {"code": "obstacle_front", "distance": 0.8, "type": "danger"},  # 严重事件
    ]

    out = p.process(evs)
    assert len(out) == 1
    assert out[0]["code"] == "obstacle_front"


def test_empty_events():
    """测试空事件列表"""
    p = NavigationEventPostProcessor()
    out = p.process([])
    assert len(out) == 0


def test_event_without_code_skipped():
    """测试缺少 code 的事件被跳过"""
    p = NavigationEventPostProcessor()
    p.reset()

    evs = [
        {"distance": 1.0, "type": "danger"},  # 缺少 code
    ]

    out = p.process(evs)
    assert len(out) == 0


def test_jitter_without_distance():
    """测试没有距离信息的事件不进行抖动过滤"""
    p = NavigationEventPostProcessor()
    p.reset()

    ev1 = {"code": "road_narrow", "type": "navigation"}
    ev2 = {"code": "road_narrow", "type": "navigation"}

    out1 = p.process([ev1])
    assert len(out1) == 1

    # road_narrow 没有抖动阈值，但会被冷却阻止
    out2 = p.process([ev2])
    assert len(out2) == 0


def test_reset_clears_state():
    """测试 reset() 清除所有状态"""
    p = NavigationEventPostProcessor()
    p.reset()

    ev = {"code": "obstacle_front", "distance": 1.0, "type": "danger"}

    # 第一次通过
    out1 = p.process([ev])
    assert len(out1) == 1

    # 立即触发第二次 → 被冷却阻止
    out2 = p.process([ev])
    assert len(out2) == 0

    # reset 后应该可以通过
    p.reset()
    out3 = p.process([ev])
    assert len(out3) == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

