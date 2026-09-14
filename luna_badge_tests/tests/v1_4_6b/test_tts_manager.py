"""
测试 TtsManager 和 Utterance

验证：
1. TtsManager.speak() 正确添加 Utterance 到队列
2. TtsManager.enqueue() 和 pop_all() 正常工作
3. 模块级单例 tts_manager 可用
"""

import sys
import os
import unittest

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from task_engine.tts import TtsManager, tts_manager, Utterance


def test_tts_manager_speak_adds_utterance_to_queue():
    """测试：TtsManager.speak() 正确添加 Utterance 到队列"""
    mgr = TtsManager()
    assert mgr.get_queue() == []

    u = mgr.speak("hello world", level="info")
    q = mgr.get_queue()

    assert len(q) == 1
    assert isinstance(q[0], Utterance)
    assert q[0].text == "hello world"
    assert q[0].level == "info"
    assert q[0].channel == "tts"
    assert isinstance(q[0].created_at, float)


def test_tts_manager_enqueue_and_pop_all():
    """测试：TtsManager.enqueue() 和 pop_all() 正常工作"""
    mgr = TtsManager()
    u1 = Utterance(text="a")
    u2 = Utterance(text="b", level="warning")

    mgr.enqueue(u1)
    mgr.enqueue(u2)

    queue_before = mgr.get_queue()
    assert len(queue_before) == 2

    popped = mgr.pop_all()
    assert len(popped) == 2
    assert mgr.get_queue() == []


def test_module_level_tts_manager_is_usable():
    """测试：模块级单例 tts_manager 可用"""
    # 验证全局单例可用，避免初始化问题
    tts_manager.pop_all()
    tts_manager.speak("test one")
    tts_manager.speak("test two")

    queue = tts_manager.pop_all()
    texts = [u.text for u in queue]
    assert texts == ["test one", "test two"]


def test_utterance_to_dict():
    """测试：Utterance.to_dict() 序列化"""
    u = Utterance(
        text="hello",
        level="warning",
        channel="tts",
        meta={"emotion": "happy"},
    )
    d = u.to_dict()

    assert d["text"] == "hello"
    assert d["level"] == "warning"
    assert d["channel"] == "tts"
    assert d["meta"]["emotion"] == "happy"
    assert "created_at" in d


def test_tts_manager_speak_with_meta():
    """测试：TtsManager.speak() 支持元数据"""
    mgr = TtsManager()
    u = mgr.speak("hello", level="info", emotion="happy", priority=80)

    assert u.meta.get("emotion") == "happy"
    # priority 现在是 Utterance 的直接字段，不在 meta 中
    assert u.priority == 80


def test_tts_manager_clear():
    """测试：TtsManager.clear() 清空队列"""
    mgr = TtsManager()
    mgr.speak("a")
    mgr.speak("b")

    assert len(mgr.get_queue()) == 2

    mgr.clear()
    assert len(mgr.get_queue()) == 0


if __name__ == "__main__":
    unittest.main()

