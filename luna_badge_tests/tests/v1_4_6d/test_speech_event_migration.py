"""
测试 speech_event 迁移到 NavigationVoiceAdapter（v1.4.6d）

验证：
1. handle_speech_event() 能正确处理字典格式的 speech_event
2. 能正确处理字符串格式的 speech_event（向后兼容）
3. 根据 decision 类型正确映射到对应的适配器方法
4. 根据文本内容自动分类（安全 vs 导航）
"""

import sys
import os
import pytest

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from task_engine.tts import tts_manager
from task_engine.navigation import NavigationVoiceAdapter


@pytest.fixture
def voice():
    """创建 NavigationVoiceAdapter 实例"""
    return NavigationVoiceAdapter()


def setup_module(module):
    """避免其他测试残留"""
    tts_manager.clear()


def test_handle_speech_event_stop_decision(voice):
    """测试 STOP decision → SAFETY 类别"""
    tts_manager.clear()
    speech_event = {
        "speak": True,
        "decision": "STOP",
        "text": "前方无法通行，请原地停下。",
        "style": "alert",
        "priority": 3,
        "interruptible": False,
        "category": "navigation",
    }
    voice.handle_speech_event(speech_event)

    q = tts_manager.get_queue()
    assert len(q) == 1
    u = q[0]

    assert "障碍物" in u.text or "无法通行" in u.text
    assert u.meta["ttscategory"] == "safety"
    assert u.priority == 90
    assert u.interrupt is True


def test_handle_speech_event_turn_decision(voice):
    """测试转向 decision → NAVIGATION 类别"""
    tts_manager.clear()
    speech_event = {
        "speak": True,
        "decision": "SLIGHT_RIGHT",
        "text": "右侧稍微更通畅，请向右一点",
        "style": "calm",
        "priority": 1,
        "interruptible": True,
        "category": "navigation",
    }
    voice.handle_speech_event(speech_event)

    q = tts_manager.get_queue()
    assert len(q) == 1
    u = q[0]

    assert "右转" in u.text
    assert u.meta["ttscategory"] == "navigation"
    assert u.priority == 75


def test_handle_speech_event_forward_decision(voice):
    """测试 FORWARD decision → NAVIGATION 类别"""
    tts_manager.clear()
    speech_event = {
        "speak": True,
        "decision": "FORWARD",
        "text": "请继续直行",
        "style": "calm",
        "priority": 0,
        "interruptible": True,
        "category": "navigation",
    }
    voice.handle_speech_event(speech_event)

    q = tts_manager.get_queue()
    assert len(q) == 1
    u = q[0]

    assert "直行" in u.text
    assert u.meta["ttscategory"] == "navigation"
    assert u.priority == 75


def test_handle_speech_event_text_based_safety(voice):
    """测试根据文本内容自动分类为 SAFETY"""
    tts_manager.clear()
    speech_event = {
        "speak": True,
        "text": "前方人多，请减速并注意避让",
        "decision": "UNKNOWN",
    }
    voice.handle_speech_event(speech_event)

    q = tts_manager.get_queue()
    assert len(q) == 1
    u = q[0]

    assert u.meta["ttscategory"] == "safety"
    assert u.priority == 90
    assert u.interrupt is True


def test_handle_speech_event_text_based_navigation(voice):
    """测试根据文本内容自动分类为 NAVIGATION"""
    tts_manager.clear()
    speech_event = {
        "speak": True,
        "text": "前方50米，请向左转",
        "decision": "UNKNOWN",
    }
    voice.handle_speech_event(speech_event)

    q = tts_manager.get_queue()
    assert len(q) == 1
    u = q[0]

    assert u.meta["ttscategory"] == "navigation"
    assert u.priority == 75
    assert u.interrupt is False


def test_handle_speech_event_string_compatibility(voice):
    """测试字符串类型的 speech_event（向后兼容）"""
    tts_manager.clear()
    voice.handle_speech_event("前方50米，请向左转")

    q = tts_manager.get_queue()
    assert len(q) == 1
    u = q[0]

    assert "左转" in u.text
    assert u.meta["ttscategory"] == "navigation"


def test_handle_speech_event_preserves_meta(voice):
    """测试 handle_speech_event 保留原始 meta 数据"""
    tts_manager.clear()
    speech_event = {
        "speak": True,
        "decision": "SLIGHT_LEFT",
        "text": "请向左转",
        "style": "calm",
        "priority": 1,
        "custom_field": "custom_value",
    }
    voice.handle_speech_event(speech_event, meta={"extra": "value"})

    q = tts_manager.get_queue()
    u = q[0]

    # 应该保留原始字段
    assert u.meta.get("decision") == "SLIGHT_LEFT"
    assert u.meta.get("style") == "calm"
    assert u.meta.get("original_priority") == 1
    assert u.meta.get("source") == "speech_event"
    # 应该保留自定义 meta
    assert u.meta.get("extra") == "value"


def test_handle_speech_event_skip_if_not_speak(voice):
    """测试 speak=False 时跳过播报"""
    tts_manager.clear()
    speech_event = {
        "speak": False,
        "text": "这条消息不应该被播报",
    }
    voice.handle_speech_event(speech_event)

    q = tts_manager.get_queue()
    assert len(q) == 0


def test_handle_speech_event_empty_text(voice):
    """测试空文本时跳过播报"""
    tts_manager.clear()
    speech_event = {
        "speak": True,
        "text": "",
    }
    voice.handle_speech_event(speech_event)

    q = tts_manager.get_queue()
    assert len(q) == 0


def test_handle_speech_event_none(voice):
    """测试 None 输入时安全处理"""
    tts_manager.clear()
    voice.handle_speech_event(None)

    q = tts_manager.get_queue()
    assert len(q) == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])












