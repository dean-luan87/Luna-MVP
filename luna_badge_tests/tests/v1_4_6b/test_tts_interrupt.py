"""
测试 TTS 打断语义（Patch-H）

验证：
1. interrupt=True 的 Utterance 会打断其他普通项
2. 多条 interrupt 时选择最高优先级
3. 没有 interrupt 时行为与 Patch-G 一致
"""

import sys
import os
import unittest

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from task_engine.tts import TTSRuntimeDriver, tts_manager


def setup_module(module):
    """避免其他测试残留"""
    tts_manager.clear()


def test_interrupt_utterance_drops_others_in_same_batch(monkeypatch):
    """
    当本轮队列中存在 interrupt=True 的 Utterance 时：
    - 只播报该 interrupt 项；
    - 其他普通项视为被打断且丢弃。
    """
    tts_manager.clear()
    driver = TTSRuntimeDriver(manager=tts_manager)

    calls = []

    def fake_speak(self, utter):
        calls.append((utter.text, utter.priority, utter.interrupt))

    monkeypatch.setattr(TTSRuntimeDriver, "_speak_utterance", fake_speak)

    # 队列：普通 -> interrupt -> 普通
    tts_manager.speak("普通提示1", priority=50, interrupt=False)
    tts_manager.speak("紧急警告", priority=90, interrupt=True)
    tts_manager.speak("普通提示2", priority=50, interrupt=False)

    driver.process_once()

    # 只应播报那条"紧急警告"
    assert len(calls) == 1
    text, pri, intr = calls[0]
    assert text == "紧急警告"
    assert pri == 90
    assert intr is True

    # 队列应为空
    assert len(tts_manager.get_queue()) == 0


def test_multiple_interrupts_pick_highest_priority(monkeypatch):
    """
    若本轮存在多条 interrupt=True 的 Utterance：
    - 应选择"最高优先级 + 最早创建"的那条。
    """
    tts_manager.clear()
    driver = TTSRuntimeDriver(manager=tts_manager)

    calls = []

    def fake_speak(self, utter):
        calls.append((utter.text, utter.priority))

    monkeypatch.setattr(TTSRuntimeDriver, "_speak_utterance", fake_speak)

    # 注意：TtsManager.speak 先入队的 created_at 更早，
    # pop_all() 会按 priority 降序 + created_at 升序 排序。

    # 先来一个优先级 80 的 interrupt
    tts_manager.speak("高优先级但非最高(80)", priority=80, interrupt=True)
    # 再来一个优先级 95 的 interrupt
    tts_manager.speak("最高优先级(95)", priority=95, interrupt=True)
    # 再来一个普通的
    tts_manager.speak("普通提示", priority=50, interrupt=False)

    driver.process_once()

    # 只应播报优先级最高的那条
    assert len(calls) == 1
    text, pri = calls[0]
    assert text == "最高优先级(95)"
    assert pri == 95


def test_no_interrupt_behaves_as_normal(monkeypatch):
    """
    没有 interrupt=True 的情况下，行为应与 Patch-G 一致：
    - 按 priority 降序 + FIFO 顺序依次播报全部 Utterance。
    """
    tts_manager.clear()
    driver = TTSRuntimeDriver(manager=tts_manager)

    calls = []

    def fake_speak(self, utter):
        calls.append(utter.text)

    monkeypatch.setattr(TTSRuntimeDriver, "_speak_utterance", fake_speak)

    tts_manager.speak("A", priority=50)
    tts_manager.speak("B", priority=90)
    tts_manager.speak("C", priority=50)

    driver.process_once()

    # B（优先级 90）先，A/C 同优先级 50，按 FIFO
    assert calls == ["B", "A", "C"]


def test_interrupt_with_same_priority_picks_first(monkeypatch):
    """
    若多条 interrupt 具有相同优先级，应选择最早创建的那条。
    """
    tts_manager.clear()
    driver = TTSRuntimeDriver(manager=tts_manager)

    calls = []

    def fake_speak(self, utter):
        calls.append(utter.text)

    monkeypatch.setattr(TTSRuntimeDriver, "_speak_utterance", fake_speak)

    # 先创建一个 interrupt
    u1 = tts_manager.speak("第一个 interrupt", priority=80, interrupt=True)
    # 再创建一个同优先级的 interrupt
    u2 = tts_manager.speak("第二个 interrupt", priority=80, interrupt=True)
    
    # 确保第一个更早
    u1.created_at = 1.0
    u2.created_at = 2.0

    driver.process_once()

    # 应该选择第一个（created_at 更早）
    assert len(calls) == 1
    assert calls[0] == "第一个 interrupt"


if __name__ == "__main__":
    unittest.main()












