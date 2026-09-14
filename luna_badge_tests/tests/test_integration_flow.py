# -*- coding: utf-8 -*-
"""
集成测试：完整事件流测试
"""

import sys
import os

# 添加项目路径
_script_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.normpath(os.path.join(_script_dir, '..'))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from decision.decision_core import DecisionCore
from core.events import EventType
from core.decision_actions import DecisionAction
from inquiry.inquiry_manager import InquiryManager
from taskchain.manager import TaskChainManager
from core.intent_schema import ParsedIntent


def test_hospital_gate_ask_confirm():
    """场景：到达医院门口 → 询问是否进入医院流程"""
    decision_core = DecisionCore()
    inquiry_manager = InquiryManager()
    
    # Step1: Node 完成事件
    payload = {"node_id": "gate"}
    context = {
        "scene_context": {"location": "hospital_gate"},
        "task_context": {
            "task_id": "nav_to_hospital_1",
            "active_node": {"id": "gate", "requires_user_confirmation": True}
        },
        "model_context": {"vision_main": "ok", "vision_fallback": "ok"}
    }
    
    out = decision_core.handle_event(EventType.TASK_NODE_COMPLETE, payload, context)
    assert out.action == DecisionAction.ASK_USER
    assert "question_type" in out.params
    
    # Step2: 构建问句
    inquiry = inquiry_manager.build_question(
        question_type="enter_hospital_flow",
        context=out.params.get("context", {})
    )
    assert inquiry["type"] == "inquiry"
    assert "question" in inquiry
    
    # Step3: 用户回答 "是"
    parsed = inquiry_manager.handle_user_response("enter_hospital_flow", "是")
    assert parsed.intent_name == "CONFIRM"
    assert parsed.need_confirm == False


def test_insert_task_flow():
    """场景：导航中用户说"先去厕所" → 插入任务"""
    decision_core = DecisionCore()
    inquiry_manager = InquiryManager()
    taskchain = TaskChainManager()
    
    # 初始化主任务
    main_task = {
        "task_id": "nav_to_hospital_1",
        "type": "navigation",
        "nodes": [{"id": "on_the_way", "name": "途中"}]
    }
    taskchain.start_main_task(main_task)
    
    # Step1: 用户给出非模板回答（指令）
    parsed = inquiry_manager.handle_user_response("resume_main_task", "我先去厕所")
    assert parsed.intent_name == "INSERT_TASK"
    assert parsed.need_confirm == True
    assert parsed.slots == {"task_type": "toilet"}
    
    # Step2: 决策层要求二次确认（如果 need_confirm=True）
    if parsed.need_confirm:
        # 构建确认问句
        inquiry = inquiry_manager.build_question(
            "confirm_new_intent",
            {"intent_desc": "先去厕所"}
        )
        assert inquiry["type"] == "inquiry"
        
        # Step3: 用户确认
        confirm_parsed = inquiry_manager.handle_user_response(
            "confirm_new_intent",
            "是的"
        )
        assert confirm_parsed.intent_name == "CONFIRM"
        
        # Step4: 决策层执行插入任务
        # 需要在 payload 中传递待确认的原始意图
        payload = {
            "parsed_intent": confirm_parsed,
            "pending_intent": parsed  # 传递原始意图
        }
        context = {
            "task_context": {"task_id": "nav_to_hospital_1"},
            "model_context": {"vision_main": "ok", "vision_fallback": "ok"}
        }
        
        insert_out = decision_core.handle_event(EventType.USER_INTENT, payload, context)
        assert insert_out.action == DecisionAction.INSERT_TASK
        assert "insert_task_spec" in insert_out.params
        
        # Step5: TaskChain 插入任务
        taskchain.apply_decision(insert_out)
        assert taskchain.active_task.get("type") == "go_to_toilet"
        assert len(taskchain.sub_task_stack) == 1


def test_subtask_complete_resume():
    """场景：子任务完成 → 恢复主任务"""
    decision_core = DecisionCore()
    taskchain = TaskChainManager()
    
    # 设置主任务和子任务
    main_task = {
        "task_id": "nav_to_hospital_1",
        "type": "navigation",
        "nodes": [{"id": "on_the_way", "name": "途中"}]
    }
    taskchain.start_main_task(main_task)
    taskchain.main_task_state = {
        "task": main_task,
        "node": {"id": "on_the_way"}
    }
    
    # 插入子任务
    sub_task = {
        "task_id": "go_to_toilet_1",
        "type": "go_to_toilet",
        "nodes": [{"id": "toilet_reached", "name": "到达厕所"}]
    }
    taskchain.insert_task(sub_task, resume_strategy="auto")
    taskchain.active_node = {"id": "toilet_reached"}
    
    # Step1: 子任务完成事件
    payload = {"node_id": "toilet_reached"}
    context = {
        "task_context": {
            "task_id": "go_to_toilet_1",
            "is_subtask": True,
            "main_task_id": "nav_to_hospital_1"
        },
        "model_context": {}
    }
    
    out = decision_core.handle_event(EventType.TASK_NODE_COMPLETE, payload, context)
    # 子任务完成，应该继续任务（由 TaskChain 处理恢复）
    assert out.action == DecisionAction.CONTINUE_TASK
    
    # Step2: TaskChain 完成并恢复
    result = taskchain.complete_active_task()
    assert result["status"] == "resumed"
    assert taskchain.active_task.get("task_id") == "nav_to_hospital_1"
    assert len(taskchain.sub_task_stack) == 0


def test_planb_trigger_integration():
    """场景：模型故障 → PlanB 触发"""
    decision_core = DecisionCore()
    taskchain = TaskChainManager()
    
    # 设置活动任务
    main_task = {
        "task_id": "nav_to_hospital_1",
        "type": "navigation",
        "nodes": [{"id": "on_the_way", "name": "途中"}]
    }
    taskchain.start_main_task(main_task)
    
    # Step1: 模型状态更新（全部失败）
    payload = {"source": "health_monitor"}
    context = {
        "task_context": {"task_id": "nav_to_hospital_1"},
        "model_context": {"vision_main": "down", "vision_fallback": "down"}
    }
    
    out = decision_core.handle_event(EventType.MODEL_STATUS, payload, context)
    assert out.action == DecisionAction.TRIGGER_PLANB
    assert "context_snapshot" in out.params
    
    # Step2: TaskChain 进入暂停状态
    pause_result = taskchain.pause_for_planb()
    assert pause_result["status"] == "paused"
    assert "active_task_state" in pause_result


def test_unknown_response_fallback():
    """场景：用户回答未知 → fallback 再问"""
    decision_core = DecisionCore()
    inquiry_manager = InquiryManager()
    
    # Step1: 用户回答无法识别
    parsed = inquiry_manager.handle_user_response("enter_hospital_flow", "我也不知道")
    assert parsed.intent_name == "UNKNOWN"
    
    # Step2: 决策层处理 UNKNOWN
    payload = {"parsed_intent": parsed}
    context = {
        "task_context": {"task_id": "nav_to_hospital_1"},
        "model_context": {}
    }
    
    out = decision_core.handle_event(EventType.USER_INTENT, payload, context)
    # UNKNOWN 应该返回 NO_OP
    assert out.action == DecisionAction.NO_OP


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
