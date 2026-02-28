"""
测试 TaskLifecycleState：统一的任务生命周期状态模型

验证状态管理、序列化/反序列化、状态转换等功能
"""

import sys
import os

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import pytest
from task_engine.task_lifecycle_state import (
    TaskLifecyclePhase,
    TaskLifecycleStatus,
    TaskLifecycleState,
)


def test_lifecycle_defaults_active_idle():
    """测试：默认状态为 IDLE + ACTIVE"""
    state = TaskLifecycleState()
    assert state.phase == TaskLifecyclePhase.IDLE
    assert state.status == TaskLifecycleStatus.ACTIVE
    assert state.is_active is True
    assert state.is_paused is False
    assert state.is_finished is False
    assert state.is_aborted is False


def test_mark_pause_and_resume():
    """测试：状态标记和暂停/恢复"""
    state = TaskLifecycleState()

    state.mark(
        phase=TaskLifecyclePhase.TASK,
        status=TaskLifecycleStatus.PAUSED,
        reason="user_said_pause",
        source="user",
    )
    assert state.phase == TaskLifecyclePhase.TASK
    assert state.status == TaskLifecycleStatus.PAUSED
    assert state.is_paused is True
    assert state.is_active is False

    # 恢复
    state.mark(status=TaskLifecycleStatus.ACTIVE, reason="user_resume")
    assert state.status == TaskLifecycleStatus.ACTIVE
    assert state.is_active is True
    assert state.is_paused is False
    assert state.reason == "user_resume"


def test_serialize_and_restore():
    """测试：序列化和反序列化"""
    state = TaskLifecycleState(
        phase=TaskLifecyclePhase.ASK,
        status=TaskLifecycleStatus.PAUSED,
        reason="waiting_for_answer",
        source="system",
    )
    state.meta["slot"] = "hospital_name"

    data = state.to_dict()
    restored = TaskLifecycleState.from_dict(data)

    assert restored.phase == TaskLifecyclePhase.ASK
    assert restored.status == TaskLifecycleStatus.PAUSED
    assert restored.reason == "waiting_for_answer"
    assert restored.source == "system"
    assert restored.meta["slot"] == "hospital_name"


def test_is_paused_property():
    """测试：is_paused 属性覆盖所有暂停状态"""
    state1 = TaskLifecycleState(status=TaskLifecycleStatus.PAUSED)
    assert state1.is_paused is True

    state2 = TaskLifecycleState(status=TaskLifecycleStatus.SUSPENDED_TEMP)
    assert state2.is_paused is True

    state3 = TaskLifecycleState(status=TaskLifecycleStatus.ACTIVE)
    assert state3.is_paused is False


def test_is_finished_and_is_aborted():
    """测试：完成和终止状态"""
    state1 = TaskLifecycleState(status=TaskLifecycleStatus.FINISHED)
    assert state1.is_finished is True
    assert state1.is_aborted is False

    state2 = TaskLifecycleState(status=TaskLifecycleStatus.ABORTED)
    assert state2.is_finished is False
    assert state2.is_aborted is True


def test_mark_with_extra_meta():
    """测试：mark 方法支持 extra_meta"""
    state = TaskLifecycleState()
    
    state.mark(
        phase=TaskLifecyclePhase.TASK,
        status=TaskLifecycleStatus.ACTIVE,
        extra_meta={"task_id": "test_123", "user_id": "user_456"},
    )
    
    assert state.meta["task_id"] == "test_123"
    assert state.meta["user_id"] == "user_456"
    assert state.phase == TaskLifecyclePhase.TASK


def test_updated_at_timestamp():
    """测试：状态更新时自动更新时间戳"""
    import time
    
    state = TaskLifecycleState()
    initial_time = state.updated_at
    
    # 等待一小段时间
    time.sleep(0.01)
    
    state.mark(status=TaskLifecycleStatus.PAUSED)
    
    assert state.updated_at > initial_time

