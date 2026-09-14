"""
测试 SceneChain × TTS 自动播报系统

验证：
1. SceneRuntime.handle_enter() 触发进入场景 TTS
2. SceneRuntime.handle_events() 播报场景事件（去重）
3. SceneRuntime.handle_exit() 触发退出场景 TTS
"""

import sys
import os
import time
import unittest

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from task_engine.tts import tts_manager
from task_engine.scene.scene_runtime import SceneRuntime, SceneRuntimeOutput
from task_engine.scene.scene_integration import SceneIntegrationResult
from task_engine.scene.scene_context import SceneContext
from task_engine.scene.scene_classifier import SceneGuess
from task_engine.scene.scene_registry import ScenePackRef, SceneKey


def test_scene_enter_triggers_tts():
    """测试：SceneRuntime.handle_enter() 触发进入场景 TTS"""
    tts_manager.clear()
    
    ctx = SceneContext(
        scene="hospital",
        tag="虹口医院",
        confidence=0.9,
        history_tags=[],
    )
    
    guess = SceneGuess(scene="hospital", tag="虹口医院", confidence=0.9)
    
    result = SceneIntegrationResult(
        context=ctx,
        guess=guess,
        pack_ref=None,
        enter_voice="您现在处于 虹口医院 环境。",
        hints=[],
        exit_voice=None,
    )
    
    runtime = SceneRuntime()
    output = runtime.handle_enter(result)
    
    q = tts_manager.pop_all()
    assert len(q) == 1
    assert "医院" in q[0].text
    assert output.enter_voice == "您现在处于 虹口医院 环境。"


def test_scene_event_voice_hint_once():
    """测试：SceneRuntime.handle_events() 播报场景事件（去重）"""
    tts_manager.clear()
    
    ctx = SceneContext(
        scene="hospital",
        tag="虹口医院",
        confidence=0.9,
        history_tags=[],
    )
    
    guess = SceneGuess(scene="hospital", tag="虹口医院", confidence=0.9)
    
    result = SceneIntegrationResult(
        context=ctx,
        guess=guess,
        pack_ref=None,
        enter_voice=None,
        hints=["前方有服务台"],
        exit_voice=None,
    )
    
    runtime = SceneRuntime()
    
    # 第一次触发
    output1 = runtime.handle_events(result)
    q1 = tts_manager.pop_all()
    assert len(q1) == 1
    assert "服务台" in q1[0].text
    assert len(output1.hints) == 1
    
    # 再触发一次，应不会重复播报
    output2 = runtime.handle_events(result)
    q2 = tts_manager.pop_all()
    assert len(q2) == 0
    assert len(output2.hints) == 0


def test_scene_exit_triggers_tts():
    """测试：SceneRuntime.handle_exit() 触发退出场景 TTS"""
    tts_manager.clear()
    
    ctx = SceneContext(
        scene="hospital",
        tag="虹口医院",
        confidence=0.9,
        history_tags=[],
    )
    
    guess = SceneGuess(scene="hospital", tag="虹口医院", confidence=0.9)
    
    result = SceneIntegrationResult(
        context=ctx,
        guess=guess,
        pack_ref=None,
        enter_voice=None,
        hints=[],
        exit_voice="您已离开医院。",
    )
    
    runtime = SceneRuntime()
    output = runtime.handle_exit(result)
    
    q = tts_manager.pop_all()
    assert len(q) == 1
    assert "离开" in q[0].text
    assert output.exit_voice == "您已离开医院。"


def test_scene_multiple_hints():
    """测试：多个 hints 的播报"""
    tts_manager.clear()
    
    ctx = SceneContext(
        scene="hospital",
        tag="虹口医院",
        confidence=0.9,
        history_tags=[],
    )
    
    guess = SceneGuess(scene="hospital", tag="虹口医院", confidence=0.9)
    
    result = SceneIntegrationResult(
        context=ctx,
        guess=guess,
        pack_ref=None,
        enter_voice=None,
        hints=["前方有服务台", "附近有安检口", "这是候诊区"],
        exit_voice=None,
    )
    
    runtime = SceneRuntime()
    output = runtime.handle_events(result)
    
    q = tts_manager.pop_all()
    assert len(q) == 3
    assert len(output.hints) == 3
    
    # 再次触发，应该都不播报（已去重）
    output2 = runtime.handle_events(result)
    q2 = tts_manager.pop_all()
    assert len(q2) == 0


if __name__ == "__main__":
    unittest.main()












