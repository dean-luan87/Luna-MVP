"""
测试 TaskChainManager × TTS 自动播报

验证：
1. TaskChainManager.pause_task() 自动注入播报内容
2. TaskChainManager.resume_task() 自动注入播报内容
3. TaskChainManager.cancel_task() 自动注入播报内容
4. TaskChainManager.switch_task() 自动注入播报内容
"""

import sys
import os
import unittest

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from task_chain.task_chain_manager import TaskChainManager, TaskStatus
from core.flow_engine.runtime import FlowRuntime
from core.flow_engine.flow_types import FlowInstance, FlowDefinition, FlowContext, FlowNode, FlowNodeType
from task_engine.tts import tts_manager


def test_task_chain_manager_pause_injects_utterance():
    """测试：TaskChainManager.pause_task() 自动注入播报内容"""
    tts_manager.clear()
    
    runtime = FlowRuntime()
    mgr = TaskChainManager(runtime)
    
    # 创建一个简单的任务实例
    ctx = FlowContext(
        task_id="test_task_1",
        user_id="test_user",
        scene_type="test",
        intent="test_intent",
    )
    
    flow_def = FlowDefinition(
        id="test_flow",
        nodes={"node1": FlowNode(id="node1", node_type=FlowNodeType.CUSTOM)},
        edges=[],
        entry_node_id="node1",
    )
    
    instance = FlowInstance(
        definition=flow_def,
        context=ctx,
        current_node_id="node1",
    )
    
    # 注册任务
    record = mgr.register_task(instance)
    
    # 暂停任务
    mgr.pause_task(record.task_id)
    
    # 验证 TTS 队列中有内容
    q = tts_manager.get_queue()
    assert len(q) > 0
    assert any("暂停" in u.text for u in q)


def test_task_chain_manager_resume_injects_utterance():
    """测试：TaskChainManager.resume_task() 自动注入播报内容"""
    tts_manager.clear()
    
    runtime = FlowRuntime()
    mgr = TaskChainManager(runtime)
    
    # 创建任务实例
    ctx = FlowContext(
        task_id="test_task_2",
        user_id="test_user",
        scene_type="test",
        intent="test_intent",
    )
    
    flow_def = FlowDefinition(
        id="test_flow",
        nodes={"node1": FlowNode(id="node1", node_type=FlowNodeType.CUSTOM)},
        edges=[],
        entry_node_id="node1",
    )
    
    instance = FlowInstance(
        definition=flow_def,
        context=ctx,
        current_node_id="node1",
    )
    
    # 注册任务并暂停
    record = mgr.register_task(instance)
    mgr.pause_task(record.task_id)
    tts_manager.clear()  # 清空暂停时的 TTS
    
    # 恢复任务
    mgr.resume_task(record.task_id)
    
    # 验证 TTS 队列中有内容
    q = tts_manager.get_queue()
    assert len(q) > 0
    assert any("继续" in u.text for u in q)


def test_task_chain_manager_cancel_injects_utterance():
    """测试：TaskChainManager.cancel_task() 自动注入播报内容"""
    tts_manager.clear()
    
    runtime = FlowRuntime()
    mgr = TaskChainManager(runtime)
    
    # 创建任务实例
    ctx = FlowContext(
        task_id="test_task_3",
        user_id="test_user",
        scene_type="test",
        intent="test_intent",
    )
    
    flow_def = FlowDefinition(
        id="test_flow",
        nodes={"node1": FlowNode(id="node1", node_type=FlowNodeType.CUSTOM)},
        edges=[],
        entry_node_id="node1",
    )
    
    instance = FlowInstance(
        definition=flow_def,
        context=ctx,
        current_node_id="node1",
    )
    
    # 注册任务
    record = mgr.register_task(instance)
    
    # 取消任务
    mgr.cancel_task(record.task_id)
    
    # 验证 TTS 队列中有内容
    q = tts_manager.get_queue()
    assert len(q) > 0
    assert any("取消" in u.text for u in q)


def test_task_chain_manager_switch_injects_utterance():
    """测试：TaskChainManager.switch_task() 自动注入播报内容"""
    tts_manager.clear()
    
    runtime = FlowRuntime()
    mgr = TaskChainManager(runtime)
    
    # 创建旧任务实例
    ctx1 = FlowContext(
        task_id="old_task",
        user_id="test_user",
        scene_type="test",
        intent="old_intent",
    )
    
    flow_def1 = FlowDefinition(
        id="old_flow",
        nodes={"node1": FlowNode(id="node1", node_type=FlowNodeType.CUSTOM)},
        edges=[],
        entry_node_id="node1",
    )
    
    old_instance = FlowInstance(
        definition=flow_def1,
        context=ctx1,
        current_node_id="node1",
    )
    
    # 注册旧任务
    old_record = mgr.register_task(old_instance)
    tts_manager.clear()  # 清空注册时的 TTS
    
    # 创建新任务实例
    ctx2 = FlowContext(
        task_id="new_task",
        user_id="test_user",
        scene_type="test",
        intent="new_intent",
    )
    
    flow_def2 = FlowDefinition(
        id="new_flow",
        nodes={"node1": FlowNode(id="node1", node_type=FlowNodeType.CUSTOM)},
        edges=[],
        entry_node_id="node1",
    )
    
    new_instance = FlowInstance(
        definition=flow_def2,
        context=ctx2,
        current_node_id="node1",
    )
    
    # 切换任务
    new_record = mgr.switch_task(old_record.task_id, new_instance)
    
    # 验证 TTS 队列中有内容
    q = tts_manager.get_queue()
    assert len(q) > 0
    assert any("切换" in u.text for u in q)


if __name__ == "__main__":
    unittest.main()












