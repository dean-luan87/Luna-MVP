"""
测试 TTS 优先级队列系统

验证：
1. 默认优先级为 50
2. pop_all() 按优先级降序 + created_at 升序排序
3. 同优先级保持 FIFO
4. RuntimeDriver 按优先级顺序消费
"""

import sys
import os
import unittest

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from task_engine.tts import TtsManager, Utterance, tts_manager, TTSRuntimeDriver


def setup_module(module):
    """避免其他测试残留"""
    tts_manager.clear()


def test_default_priority_is_50():
    """测试：默认优先级为 50"""
    mgr = TtsManager()
    mgr.clear()

    u = mgr.speak("默认优先级测试")

    assert isinstance(u, Utterance)
    assert u.priority == 50


def test_pop_all_sorts_by_priority_then_created_at(monkeypatch):
    """测试：pop_all() 按优先级降序 + created_at 升序排序"""
    mgr = TtsManager()
    mgr.clear()

    # 为了可控 created_at，手动构造 Utterance
    base = Utterance(text="A", priority=50)
    b = Utterance(text="B", priority=90)
    c = Utterance(text="C", priority=50)

    # 调整 created_at 顺序：A 最早, C 最晚
    base.created_at = 1.0
    b.created_at = 2.0
    c.created_at = 3.0

    mgr.enqueue(base)
    mgr.enqueue(b)
    mgr.enqueue(c)

    items = mgr.pop_all()
    texts = [u.text for u in items]

    # 期望：
    # - B 优先级最高（90），先播
    # - A 和 C 同为 50，按 created_at 先 A 后 C
    assert texts == ["B", "A", "C"]


def test_same_priority_keeps_fifo():
    """测试：同优先级保持 FIFO"""
    mgr = TtsManager()
    mgr.clear()

    a = mgr.speak("A", priority=50)
    b = mgr.speak("B", priority=50)
    c = mgr.speak("C", priority=50)

    # 模拟创建时间逐步增加
    a.created_at = 1.0
    b.created_at = 2.0
    c.created_at = 3.0

    items = mgr.pop_all()
    texts = [u.text for u in items]

    # 同优先级应该维持 FIFO
    assert texts == ["A", "B", "C"]


def test_runtime_driver_respects_priority(monkeypatch):
    """
    验证 RuntimeDriver.process_once 会按照优先级顺序消费，
    而不是简单 FIFO。
    """
    tts_manager.clear()
    driver = TTSRuntimeDriver(manager=tts_manager)

    calls = []

    def fake_speak(self, utter):
        calls.append(utter.text)

    monkeypatch.setattr(TTSRuntimeDriver, "_speak_utterance", fake_speak)

    # 先追加一个普通优先级
    tts_manager.speak("普通提示1", priority=50)
    # 再追加一个高优先级
    tts_manager.speak("紧急警告", priority=90)
    # 再追加一个普通
    tts_manager.speak("普通提示2", priority=50)

    driver.process_once()

    # 高优先级"紧急警告"应该排在第一
    assert calls[0] == "紧急警告"
    # 其余按 FIFO
    assert calls == ["紧急警告", "普通提示1", "普通提示2"]


def test_priority_range():
    """测试：不同优先级范围的排序"""
    mgr = TtsManager()
    mgr.clear()

    # 创建不同优先级的 Utterance
    low = Utterance(text="低优先级", priority=10)
    medium = Utterance(text="中优先级", priority=50)
    high = Utterance(text="高优先级", priority=90)
    urgent = Utterance(text="紧急", priority=100)

    mgr.enqueue(medium)
    mgr.enqueue(low)
    mgr.enqueue(urgent)
    mgr.enqueue(high)

    items = mgr.pop_all()
    texts = [u.text for u in items]

    # 应该按优先级降序：urgent > high > medium > low
    assert texts == ["紧急", "高优先级", "中优先级", "低优先级"]


if __name__ == "__main__":
    unittest.main()












