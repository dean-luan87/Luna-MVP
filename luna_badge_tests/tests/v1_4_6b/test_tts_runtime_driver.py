"""
测试 TTS Runtime Driver

验证：
1. process_once() 消费队列中的 Utterance
2. _speak_utterance() 被正确调用
3. 字符串自动包装为 Utterance
4. 后台线程 start/stop 控制
"""

import sys
import os
import time
import unittest

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from task_engine.tts import TTSRuntimeDriver, tts_manager, Utterance


def setup_module(module):
    """每个模块开始前清空一下队列，避免其他测试残留"""
    tts_manager.clear()


def test_process_once_consumes_queue():
    """
    process_once 应该消费掉队列中的 Utterance。
    """
    tts_manager.clear()
    driver = TTSRuntimeDriver(manager=tts_manager)

    tts_manager.speak("测试一")
    tts_manager.speak("测试二")

    driver.process_once()

    # 队列应该被消费完
    assert len(tts_manager.get_queue()) == 0


def test_process_once_calls_speak_utterance(monkeypatch):
    """
    验证 _speak_utterance 确实被调用，并按顺序处理。
    """
    tts_manager.clear()
    driver = TTSRuntimeDriver(manager=tts_manager)

    calls = []

    def fake_speak(self, utter):
        calls.append(utter.text)

    monkeypatch.setattr(TTSRuntimeDriver, "_speak_utterance", fake_speak)

    tts_manager.speak("你好")
    tts_manager.speak("世界")

    driver.process_once()

    assert calls == ["你好", "世界"]


def test_process_once_wraps_plain_string(monkeypatch):
    """
    即使队列里不是 Utterance，而是字符串，也能被包装并正确处理。
    """
    tts_manager.clear()
    driver = TTSRuntimeDriver(manager=tts_manager)

    received = []

    def fake_speak(self, utter):
        received.append((type(utter), utter.text))

    monkeypatch.setattr(TTSRuntimeDriver, "_speak_utterance", fake_speak)

    # 模拟旧代码往队列里塞纯字符串
    tts_manager.enqueue("纯文本播报")

    driver.process_once()

    assert len(received) == 1
    cls, text = received[0]
    assert cls is Utterance
    assert text == "纯文本播报"


def test_driver_thread_start_and_stop():
    """
    验证 start/stop 能正常控制后台线程。
    这里只做轻量级的状态检查，不依赖真实 TTS。
    """
    driver = TTSRuntimeDriver(manager=tts_manager, loop_interval=0.05)
    assert driver.is_running is False

    driver.start()
    # 给线程一点时间启动
    time.sleep(0.1)
    assert driver.is_running is True

    driver.stop()
    # stop() 返回后应当已经标记为 not running
    assert driver.is_running is False


def test_driver_processes_queue_in_background(monkeypatch):
    """
    验证后台线程能够持续处理队列中的内容。
    """
    tts_manager.clear()
    driver = TTSRuntimeDriver(manager=tts_manager, loop_interval=0.05)

    calls = []

    def fake_speak(self, utter):
        calls.append(utter.text)

    monkeypatch.setattr(TTSRuntimeDriver, "_speak_utterance", fake_speak)

    driver.start()

    # 添加一些内容到队列
    tts_manager.speak("后台测试一")
    time.sleep(0.1)  # 等待线程处理

    tts_manager.speak("后台测试二")
    time.sleep(0.1)  # 等待线程处理

    driver.stop()

    # 验证内容被处理
    assert len(calls) >= 2
    assert "后台测试一" in calls
    assert "后台测试二" in calls


if __name__ == "__main__":
    unittest.main()












