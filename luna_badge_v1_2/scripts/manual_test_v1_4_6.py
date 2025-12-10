#!/usr/bin/env python3
"""
v1.4.6 手工验收场景测试脚本

包含 3 个代表性场景：
1. 医院挂号 + 追问链 + 任务链
2. 安全播报打断普通播报
3. 任务链暂停/恢复 + TTS 提示
"""

import sys
import os

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from task_engine.tts import tts_manager, TTSRuntimeDriver
from task_chain.task_chain_manager import TaskChainManager
from core.flow_engine.runtime import FlowRuntime
from task_engine.ask import AskSchema, AskSlot, AskSlotKind, RetryPolicy, OnExceedAction
from core.flow_engine.flow_types import FlowInstance, FlowDefinition, FlowContext, FlowNode, FlowNodeType


def scenario_1_hospital_registration():
    """
    场景 1：医院挂号 + 追问链 + 任务链
    
    验证 Scene → AskChain → TaskChain 三段式融合 + Retry 上限
    """
    print("\n" + "="*60)
    print("场景 1：医院挂号 + 追问链 + 任务链")
    print("="*60)
    
    # 1. 创建 AskSchema
    schema = AskSchema(
        task_id="hospital_registration",
        slots=[
            AskSlot(
                name="hospital_name",
                kind=AskSlotKind.REQUIRED,
                prompt_template="请确认你要挂的医院名称？",
            ),
        ],
        retry_policy=RetryPolicy(
            interval=0.0,
            limit=2,
            on_exceed=OnExceedAction.ABORT,
        ),
    )
    
    # 2. 创建 TaskChainManager
    runtime = FlowRuntime()
    mgr = TaskChainManager(runtime)
    
    # 3. 创建任务实例（带 AskSchema）
    ctx = FlowContext(
        task_id="hospital_task",
        user_id="test_user",
        scene_type="hospital",
        intent="go_hospital",
    )
    
    flow_def = FlowDefinition(
        id="hospital_flow",
        nodes={"node1": FlowNode(id="node1", node_type=FlowNodeType.CUSTOM)},
        edges=[],
        entry_node_id="node1",
    )
    
    instance = FlowInstance(
        definition=flow_def,
        context=ctx,
        current_node_id="node1",
    )
    
    # 4. 注册任务（带 AskSchema）
    # 注意：TaskChainManager 需要 AskSchema 对象，不是字典
    task_meta = {
        "ask_schema": schema,  # 直接传对象
    }
    record = mgr.register_task(instance, task_meta=task_meta)
    
    print(f"\n✓ 任务已注册: {record.task_id}")
    
    # 5. 首轮 handle_user_turn（应该触发 Ask）
    print("\n--- Round 1: 首次提问 ---")
    result1 = mgr.handle_user_turn("我要去医院挂牙科")
    print(f"Phase: {result1.phase}")
    print(f"Ask Active: {result1.ask_active}")
    print(f"Task Active: {result1.task_active}")
    print(f"Ask Output: {result1.ask_output}")
    print(f"Utterances: {[u.text for u in result1.utterances]}")
    
    assert result1.phase == "ask", "首轮应该是 ask 阶段"
    assert result1.ask_active is True, "Ask 应该处于活跃状态"
    assert len(result1.utterances) > 0, "应该有 TTS 输出"
    
    # 6. 故意给两次无效回答，触发 Retry
    print("\n--- Round 2: 无效回答（触发 Retry） ---")
    result2 = mgr.handle_user_turn("   ")  # 空回答
    print(f"Ask Output: {result2.ask_output}")
    print(f"Utterances: {[u.text for u in result2.utterances]}")
    
    print("\n--- Round 3: 再次无效回答（触发 Retry） ---")
    result3 = mgr.handle_user_turn("   ")  # 再次空回答
    print(f"Ask Output: {result3.ask_output}")
    print(f"Utterances: {[u.text for u in result3.utterances]}")
    
    # 7. 第三次无效回答应该触发 ABORT
    print("\n--- Round 4: 第三次无效回答（应该触发 ABORT） ---")
    result4 = mgr.handle_user_turn("   ")  # 第三次空回答
    print(f"Phase: {result4.phase}")
    print(f"Status: {result4.status}")
    print(f"Ask Output: {result4.ask_output}")
    print(f"Task Finished: {result4.task_finished}")
    
    assert result4.status == "ask_failed" or result4.task_finished, "应该触发 ABORT"
    
    print("\n✓ 场景 1 验收通过：Retry 行为符合预期")


def scenario_2_tts_interrupt():
    """
    场景 2：安全播报打断普通播报
    
    验证 TTS priority + interrupt 语义
    """
    print("\n" + "="*60)
    print("场景 2：安全播报打断普通播报")
    print("="*60)
    
    tts_manager.clear()
    driver = TTSRuntimeDriver(manager=tts_manager)
    
    # 1. 测试 interrupt=True 的情况
    print("\n--- 测试 1: interrupt=True 打断其他项 ---")
    tts_manager.speak("今天天气不错", priority=30, interrupt=False)  # 闲聊
    tts_manager.speak("前方 50 米左转", priority=70, interrupt=False)  # 导航
    tts_manager.speak("前方有障碍物，小心！", priority=90, interrupt=True)  # 安全
    
    print("\n队列内容（插入顺序）:")
    for i, u in enumerate(tts_manager.get_queue(), 1):
        print(f"  {i}. {u.text} (priority={u.priority}, interrupt={u.interrupt})")
    
    print("\n执行 process_once()...")
    driver.process_once()
    
    queue_after = tts_manager.get_queue()
    print(f"\n队列剩余: {len(queue_after)} 项")
    assert len(queue_after) == 0, "队列应该被清空"
    
    # 2. 测试无 interrupt 的情况
    print("\n--- 测试 2: 无 interrupt，按优先级排序 ---")
    tts_manager.speak("闲聊 A", priority=30)
    tts_manager.speak("导航 B", priority=70)
    tts_manager.speak("闲聊 C", priority=30)
    
    calls = []
    import types
    original_speak = driver._speak_utterance
    
    def mock_speak(self, utter):
        calls.append(utter.text)
        print(f"  [播报] {utter.text} (priority={utter.priority})")
    
    driver._speak_utterance = types.MethodType(mock_speak, driver)
    
    print("\n执行 process_once()...")
    driver.process_once()
    
    print(f"\n播报顺序: {calls}")
    assert calls == ["导航 B", "闲聊 A", "闲聊 C"], "应该按优先级排序"
    
    print("\n✓ 场景 2 验收通过：TTS 优先级和打断语义正确")


def scenario_3_pause_resume():
    """
    场景 3：任务链暂停/恢复 + TTS 提示
    
    验证 TaskChainManager 的 pause/resume 路径
    """
    print("\n" + "="*60)
    print("场景 3：任务链暂停/恢复 + TTS 提示")
    print("="*60)
    
    runtime = FlowRuntime()
    mgr = TaskChainManager(runtime)
    
    # 1. 创建任务
    ctx = FlowContext(
        task_id="test_pause_task",
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
    
    record = mgr.register_task(instance)
    print(f"\n✓ 任务已注册: {record.task_id}")
    
    # 2. 暂停任务
    print("\n--- 暂停任务 ---")
    tts_manager.clear()
    mgr.pause_lifecycle(reason="用户请求暂停")
    
    pause_result = mgr.handle_user_turn("test")
    print(f"Paused: {pause_result.paused}")
    print(f"Pause Type: {pause_result.pause_type}")
    print(f"Utterances: {[u.text for u in pause_result.utterances]}")
    
    assert pause_result.paused is True, "任务应该处于暂停状态"
    assert len(pause_result.utterances) > 0, "应该有暂停相关的 TTS 提示"
    
    # 3. 恢复任务
    print("\n--- 恢复任务 ---")
    tts_manager.clear()
    mgr.resume_lifecycle(reason="用户请求继续")
    
    resume_result = mgr.handle_user_turn("test")
    print(f"Paused: {resume_result.paused}")
    print(f"Utterances: {[u.text for u in resume_result.utterances]}")
    
    assert resume_result.paused is False, "任务应该已恢复"
    assert len(resume_result.utterances) > 0, "应该有恢复相关的 TTS 提示"
    
    print("\n✓ 场景 3 验收通过：暂停/恢复功能正常")


def main():
    """运行所有手工验收场景"""
    print("\n" + "="*60)
    print("v1.4.6 手工验收场景测试")
    print("="*60)
    
    try:
        scenario_1_hospital_registration()
        scenario_2_tts_interrupt()
        scenario_3_pause_resume()
        
        print("\n" + "="*60)
        print("✓ 所有手工验收场景通过！")
        print("="*60)
        
    except AssertionError as e:
        print(f"\n❌ 验收失败: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ 执行错误: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())

