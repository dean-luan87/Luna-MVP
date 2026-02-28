# -*- coding: utf-8 -*-
"""
TaskChainManager 单元测试
"""

import sys
import os

# 添加项目路径
_script_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.normpath(os.path.join(_script_dir, '..'))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from taskchain.manager import TaskChainManager


def test_insert_task():
    """测试插入任务"""
    t = TaskChainManager()
    t.main_task = {"task_id": "main", "type": "nav"}
    t.active_task = t.main_task
    t.active_node = {"id": "node1"}
    
    insert_task = {"task_id": "sub1", "type": "toilet"}
    
    result = t.insert_task(insert_task, resume_strategy="auto")
    
    assert result["status"] == "ok"
    assert t.active_task["task_id"] == "sub1"
    assert len(t.sub_task_stack) == 1
    assert t.main_task_state is not None  # 主任务状态已保存


def test_subtask_complete_auto_resume():
    """测试子任务完成自动恢复"""
    t = TaskChainManager()
    
    # 主任务准备
    t.main_task = {"task_id": "main", "type": "nav"}
    t.main_task_state = {"node": {"id": "node2"}, "task": t.main_task}
    
    # 压入子任务
    t.sub_task_stack = [{"task": {"task_id": "sub1"}, "resume_strategy": "auto"}]
    t.active_task = {"task_id": "sub1"}
    
    result = t.complete_active_task()
    
    assert result["status"] == "resumed"
    assert t.active_task["task_id"] == "main"
    assert len(t.sub_task_stack) == 0


def test_subtask_complete_ask_resume():
    """测试子任务完成询问恢复"""
    t = TaskChainManager()
    
    t.main_task = {"task_id": "main", "type": "nav"}
    t.main_task_state = {"node": {"id": "node2"}, "task": t.main_task}
    t.sub_task_stack = [{"task": {"task_id": "sub1"}, "resume_strategy": "ask"}]
    t.active_task = {"task_id": "sub1"}
    
    result = t.complete_active_task()
    
    assert result["action"] == "ASK_USER"
    assert "question" in result
    assert "resume_context" in result


def test_multiple_nested_subtasks():
    """测试多层嵌套子任务"""
    t = TaskChainManager()
    
    t.main_task = {"task_id": "main", "type": "nav"}
    t.active_task = t.main_task
    t.active_node = {"id": "node1"}
    
    # 插入第一个子任务
    sub1 = {"task_id": "sub1", "type": "toilet"}
    t.insert_task(sub1, resume_strategy="auto")
    assert len(t.sub_task_stack) == 1
    
    # 插入第二个子任务（嵌套）
    sub2 = {"task_id": "sub2", "type": "buy"}
    t.insert_task(sub2, resume_strategy="auto")
    assert len(t.sub_task_stack) == 2
    assert t.active_task["task_id"] == "sub2"
    
    # 完成第二个子任务
    result = t.complete_active_task()
    assert t.active_task["task_id"] == "sub1"
    assert len(t.sub_task_stack) == 1
    
    # 完成第一个子任务
    result = t.complete_active_task()
    assert t.active_task["task_id"] == "main"
    assert len(t.sub_task_stack) == 0


def test_replace_task_clears_stack():
    """测试替换任务时清空子任务栈"""
    t = TaskChainManager()
    
    t.main_task = {"task_id": "main", "type": "nav"}
    t.active_task = t.main_task
    t.sub_task_stack = [
        {"task": {"task_id": "sub1"}, "resume_strategy": "auto"},
        {"task": {"task_id": "sub2"}, "resume_strategy": "auto"}
    ]
    
    new_task = {"task_id": "new_main", "type": "nav"}
    result = t.replace_task("main", new_task)
    
    assert result["status"] == "replaced"
    assert len(t.sub_task_stack) == 0
    assert t.main_task["task_id"] == "new_main"
    assert t.active_task["task_id"] == "new_main"


def test_resume_main_task_no_state():
    """测试恢复主任务但状态丢失"""
    t = TaskChainManager()
    
    t.main_task = {"task_id": "main", "type": "nav"}
    t.main_task_state = None  # 状态丢失
    t.sub_task_stack = [{"task": {"task_id": "sub1"}, "resume_strategy": "auto"}]
    t.active_task = {"task_id": "sub1"}
    
    result = t.complete_active_task()
    
    assert result["status"] == "error"
    assert "reason" in result


def test_pause_for_planb():
    """测试 PlanB 暂停"""
    t = TaskChainManager()
    
    t.main_task = {"task_id": "main", "type": "nav"}
    t.active_task = t.main_task
    t.active_node = {"id": "node1"}
    t.sub_task_stack = [{"task": {"task_id": "sub1"}, "resume_strategy": "auto"}]
    
    result = t.pause_for_planb()
    
    assert result["status"] == "paused"
    assert "active_task_state" in result
    assert "sub_task_stack" in result
    assert "main_task_state" in result


def test_get_active_task():
    """测试获取当前活动任务"""
    t = TaskChainManager()
    
    t.main_task = {"task_id": "main", "type": "nav"}
    t.active_task = t.main_task
    
    active = t.get_active_task()
    assert active["task_id"] == "main"


def test_is_main_task_active():
    """测试判断主任务是否活动"""
    t = TaskChainManager()
    
    t.main_task = {"task_id": "main", "type": "nav"}
    t.active_task = t.main_task
    
    assert t.is_main_task_active() == True
    
    t.active_task = {"task_id": "sub1", "type": "toilet"}
    assert t.is_main_task_active() == False


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])

