"""
Step 12: PriorityScheduler 单元测试

验证优先级调度器的调度规则。
"""

import sys
import os

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from collections import deque
import pytest

from task_engine.tts.utterance import Utterance
from task_engine.tts.priority_scheduler import PriorityScheduler
from task_engine.tts.priority_bands import PriorityBand


def test_safety_queue_always_first():
    """测试安全队列永远优先于主队列"""
    scheduler = PriorityScheduler()
    safety = deque([
        Utterance(text="安全1", priority=100, level="warning"),
    ])
    main = deque([
        Utterance(text="导航1", priority=75, level="info"),
    ])

    u = scheduler.select_next(safety, main)
    assert u.text == "安全1"
    assert len(safety) == 0
    assert len(main) == 1


def test_main_queue_band_and_priority_order():
    """测试主队列内按 band 和 priority 排序"""
    scheduler = PriorityScheduler()
    safety = deque()
    main = deque([
        Utterance(text="chat", priority=10, level="info"),   # P3
        Utterance(text="task", priority=50, level="info"),   # P2
        Utterance(text="nav", priority=75, level="info"),    # P1
    ])

    # 应该先选 P1 (nav)
    u = scheduler.select_next(safety, main)
    assert u.text == "nav"
    assert len(main) == 2

    # 然后选 P2 (task)
    u2 = scheduler.select_next(safety, main)
    assert u2.text == "task"
    assert len(main) == 1

    # 最后选 P3 (chat)
    u3 = scheduler.select_next(safety, main)
    assert u3.text == "chat"
    assert len(main) == 0


def test_same_band_priority_order():
    """测试同 band 内按 priority 排序"""
    scheduler = PriorityScheduler()
    safety = deque()
    main = deque([
        Utterance(text="nav_low", priority=70, level="info"),   # P1, priority=70
        Utterance(text="nav_high", priority=85, level="info"), # P1, priority=85
    ])

    # 应该先选 priority 更高的
    u = scheduler.select_next(safety, main)
    assert u.text == "nav_high"
    assert len(main) == 1

    u2 = scheduler.select_next(safety, main)
    assert u2.text == "nav_low"
    assert len(main) == 0


def test_same_band_same_priority_fifo():
    """测试同 band 同 priority 时按 FIFO 顺序"""
    scheduler = PriorityScheduler()
    safety = deque()
    main = deque([
        Utterance(text="first", priority=75, level="info"),   # P1, priority=75
        Utterance(text="second", priority=75, level="info"),  # P1, priority=75
    ])

    # 应该先选先入队的
    u = scheduler.select_next(safety, main)
    assert u.text == "first"
    assert len(main) == 1

    u2 = scheduler.select_next(safety, main)
    assert u2.text == "second"
    assert len(main) == 0


def test_empty_queues():
    """测试空队列"""
    scheduler = PriorityScheduler()
    safety = deque()
    main = deque()

    u = scheduler.select_next(safety, main)
    assert u is None


def test_priority_band_from_priority():
    """测试 PriorityBand.from_priority 映射"""
    assert PriorityBand.from_priority(100) == PriorityBand.P0_SAFETY
    assert PriorityBand.from_priority(90) == PriorityBand.P0_SAFETY
    assert PriorityBand.from_priority(85) == PriorityBand.P1_NAV
    assert PriorityBand.from_priority(70) == PriorityBand.P1_NAV
    assert PriorityBand.from_priority(50) == PriorityBand.P2_TASK
    assert PriorityBand.from_priority(40) == PriorityBand.P2_TASK
    assert PriorityBand.from_priority(10) == PriorityBand.P3_CHAT
    assert PriorityBand.from_priority(0) == PriorityBand.P3_CHAT


def test_priority_band_comparison():
    """测试 PriorityBand 比较"""
    assert PriorityBand.P0_SAFETY.is_higher_than(PriorityBand.P1_NAV)
    assert PriorityBand.P1_NAV.is_higher_than(PriorityBand.P2_TASK)
    assert PriorityBand.P2_TASK.is_higher_than(PriorityBand.P3_CHAT)
    assert not PriorityBand.P1_NAV.is_higher_than(PriorityBand.P0_SAFETY)


def test_tts_policy_band():
    """测试 TTSPolicy.band() 方法"""
    from task_engine.tts.tts_policy import TTSPolicy
    
    policy_safety = TTSPolicy(
        priority=100,
        interrupt=True
    )
    assert policy_safety.band() == PriorityBand.P0_SAFETY
    
    policy_nav = TTSPolicy(
        priority=75,
        interrupt=False
    )
    assert policy_nav.band() == PriorityBand.P1_NAV
    
    policy_task = TTSPolicy(
        priority=50,
        interrupt=False
    )
    assert policy_task.band() == PriorityBand.P2_TASK


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

