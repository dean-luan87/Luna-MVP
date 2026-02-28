"""
测试 TaskExecutionResult × TTS 融合层

验证：
1. TaskExecutionResult.add_utterance() 正确添加单条 TTS 文本
2. TaskExecutionResult.extend_utterances() 正确添加多个 Utterance
3. TaskExecutionResult.pop_utterances_from_tts_manager() 从全局 tts_manager 拉取队列
4. TaskExecutionResult.to_dict() 包含 utterances 序列化
"""

import sys
import os
import unittest

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from task_engine.task_execution_result import TaskExecutionResult
from task_engine.tts import tts_manager, Utterance


def test_add_single_utterance():
    """测试：TaskExecutionResult.add_utterance() 正确添加单条 TTS 文本"""
    r = TaskExecutionResult(
        ask_active=False,
        task_active=False,
    )
    r.add_utterance("hello", level="info")
    
    assert len(r.utterances) == 1
    assert r.utterances[0].text == "hello"
    assert r.utterances[0].level == "info"


def test_extend_utterances():
    """测试：TaskExecutionResult.extend_utterances() 正确添加多个 Utterance"""
    r = TaskExecutionResult(
        ask_active=False,
        task_active=False,
    )
    uts = [Utterance("a"), Utterance("b")]
    r.extend_utterances(uts)
    
    assert len(r.utterances) == 2
    assert r.utterances[1].text == "b"


def test_pop_utterances_from_tts_manager():
    """测试：TaskExecutionResult.pop_utterances_from_tts_manager() 从全局 tts_manager 拉取队列"""
    tts_manager.clear()
    tts_manager.speak("msg1", level="warning")
    tts_manager.speak("msg2", level="info")
    
    r = TaskExecutionResult(
        ask_active=False,
        task_active=False,
    )
    pulled = r.pop_utterances_from_tts_manager()
    
    assert len(pulled) == 2
    assert len(r.utterances) == 2
    assert pulled[0].text == "msg1"
    assert tts_manager.get_queue() == []


def test_to_dict_includes_utterances():
    """测试：TaskExecutionResult.to_dict() 包含 utterances 序列化"""
    r = TaskExecutionResult(
        ask_active=False,
        task_active=False,
    )
    r.add_utterance("hello", level="info")
    
    d = r.to_dict()
    assert "utterances" in d
    assert d["utterances"][0]["text"] == "hello"
    assert d["utterances"][0]["level"] == "info"


def test_add_utterance_with_meta():
    """测试：TaskExecutionResult.add_utterance() 支持元数据"""
    r = TaskExecutionResult(
        ask_active=False,
        task_active=False,
    )
    r.add_utterance("hello", level="info", emotion="happy", priority=1)
    
    assert r.utterances[0].meta.get("emotion") == "happy"
    assert r.utterances[0].meta.get("priority") == 1


def test_multiple_utterances_in_result():
    """测试：TaskExecutionResult 可以包含多条 utterances"""
    r = TaskExecutionResult(
        ask_active=False,
        task_active=False,
    )
    r.add_utterance("first", level="info")
    r.add_utterance("second", level="warning")
    r.add_utterance("third", level="error")
    
    assert len(r.utterances) == 3
    assert r.utterances[0].text == "first"
    assert r.utterances[1].text == "second"
    assert r.utterances[2].text == "third"
    
    d = r.to_dict()
    assert len(d["utterances"]) == 3


if __name__ == "__main__":
    unittest.main()












