"""
测试 Ultra: TaskLifecycleState 暂停统计功能

验证：
1. pause_count 正确累加
2. total_pause_duration 正确累积
3. last_paused_at 和 last_resumed_at 正确记录
"""

import sys
import os

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import pytest
from task_engine.task_lifecycle_state import (
    TaskLifecycleState,
    TaskLifecycleStatus,
)


def test_pause_and_resume_updates_stats():
    """测试：暂停和恢复正确更新统计信息"""
    state = TaskLifecycleState()
    assert state.pause_count == 0
    assert state.total_pause_duration == 0.0
    assert state.last_paused_at is None
    assert state.last_resumed_at is None

    t0 = 1000.0
    t1 = 1005.0
    t2 = 1010.0

    # 进入 ACTIVE
    state.mark(status=TaskLifecycleStatus.ACTIVE, now=t0)
    assert state.status == TaskLifecycleStatus.ACTIVE

    # 第一次暂停
    state.mark(status=TaskLifecycleStatus.PAUSED, now=t1)
    assert state.status == TaskLifecycleStatus.PAUSED
    assert state.pause_count == 1
    assert state.last_paused_at == t1
    assert state.total_pause_duration == 0.0  # 还没恢复，时长仍为 0

    # 恢复
    state.mark(status=TaskLifecycleStatus.ACTIVE, now=t2)
    assert state.status == TaskLifecycleStatus.ACTIVE
    assert state.total_pause_duration == (t2 - t1)  # 5.0 秒
    assert state.last_resumed_at == t2

    # 第二次暂停
    t3 = 1020.0
    t4 = 1030.0
    state.mark(status=TaskLifecycleStatus.PAUSED, now=t3)
    assert state.pause_count == 2
    assert state.last_paused_at == t3

    state.mark(status=TaskLifecycleStatus.ACTIVE, now=t4)
    assert state.pause_count == 2
    assert state.total_pause_duration == (t2 - t1) + (t4 - t3)  # 5.0 + 10.0 = 15.0 秒
    assert state.last_resumed_at == t4


def test_multiple_pause_cycles():
    """测试：多次暂停/恢复循环"""
    state = TaskLifecycleState()
    
    base_time = 1000.0
    
    # 第一次暂停/恢复
    state.mark(status=TaskLifecycleStatus.ACTIVE, now=base_time)
    state.mark(status=TaskLifecycleStatus.PAUSED, now=base_time + 1.0)
    state.mark(status=TaskLifecycleStatus.ACTIVE, now=base_time + 3.0)
    assert state.pause_count == 1
    assert state.total_pause_duration == 2.0
    
    # 第二次暂停/恢复
    state.mark(status=TaskLifecycleStatus.PAUSED, now=base_time + 5.0)
    state.mark(status=TaskLifecycleStatus.ACTIVE, now=base_time + 8.0)
    assert state.pause_count == 2
    assert state.total_pause_duration == 2.0 + 3.0  # 5.0 秒
    
    # 第三次暂停/恢复
    state.mark(status=TaskLifecycleStatus.PAUSED, now=base_time + 10.0)
    state.mark(status=TaskLifecycleStatus.ACTIVE, now=base_time + 12.0)
    assert state.pause_count == 3
    assert state.total_pause_duration == 2.0 + 3.0 + 2.0  # 7.0 秒


def test_pause_stats_serialization():
    """测试：暂停统计信息正确序列化和反序列化"""
    state = TaskLifecycleState()
    
    # 执行一些暂停/恢复操作
    state.mark(status=TaskLifecycleStatus.ACTIVE, now=1000.0)
    state.mark(status=TaskLifecycleStatus.PAUSED, now=1005.0)
    state.mark(status=TaskLifecycleStatus.ACTIVE, now=1010.0)
    
    # 序列化
    data = state.to_dict()
    assert data["pause_count"] == 1
    assert data["total_pause_duration"] == 5.0
    assert data["last_paused_at"] == 1005.0
    assert data["last_resumed_at"] == 1010.0
    
    # 反序列化
    restored = TaskLifecycleState.from_dict(data)
    assert restored.pause_count == 1
    assert restored.total_pause_duration == 5.0
    assert restored.last_paused_at == 1005.0
    assert restored.last_resumed_at == 1010.0


def test_from_dict_compatibility_with_old_paused_status():
    """测试：from_dict 兼容旧的 PAUSED_USER/PAUSED_SYSTEM 状态"""
    # 模拟旧数据格式
    old_data = {
        "status": "paused_user",
        "phase": "task",
        "pause_count": 1,
        "total_pause_duration": 5.0,
    }
    
    restored = TaskLifecycleState.from_dict(old_data)
    assert restored.status == TaskLifecycleStatus.PAUSED
    assert restored.pause_count == 1
    assert restored.total_pause_duration == 5.0
    
    # 测试 PAUSED_SYSTEM
    old_data2 = {
        "status": "paused_system",
        "phase": "ask",
    }
    
    restored2 = TaskLifecycleState.from_dict(old_data2)
    assert restored2.status == TaskLifecycleStatus.PAUSED


def test_pause_stats_only_track_paused_status():
    """测试：只有 PAUSED 状态才计入统计，SUSPENDED_TEMP 不计入"""
    state = TaskLifecycleState()
    
    base_time = 1000.0
    
    # ACTIVE -> PAUSED -> ACTIVE（计入统计）
    state.mark(status=TaskLifecycleStatus.ACTIVE, now=base_time)
    state.mark(status=TaskLifecycleStatus.PAUSED, now=base_time + 1.0)
    state.mark(status=TaskLifecycleStatus.ACTIVE, now=base_time + 3.0)
    assert state.pause_count == 1
    assert state.total_pause_duration == 2.0
    
    # ACTIVE -> SUSPENDED_TEMP -> ACTIVE（不计入统计）
    state.mark(status=TaskLifecycleStatus.SUSPENDED_TEMP, now=base_time + 5.0)
    state.mark(status=TaskLifecycleStatus.ACTIVE, now=base_time + 7.0)
    assert state.pause_count == 1  # 没有增加
    assert state.total_pause_duration == 2.0  # 没有增加












