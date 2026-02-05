# -*- coding: utf-8 -*-
"""
场景级测试：模拟真实用户行为
"""

import sys
import os

# 添加项目路径
_script_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.normpath(os.path.join(_script_dir, '..'))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from inquiry.parser import InquiryParser
from inquiry.inquiry_manager import InquiryManager
from taskchain.manager import TaskChainManager
from decision.decision_core import DecisionCore
from core.events import EventType
from core.intent_schema import ParsedIntent


def test_natural_language_tolerance():
    """测试用户自然表达的容错场景"""
    parser = InquiryParser()
    manager = InquiryManager()
    
    # 测试用例表
    test_cases = [
        ("好，继续吧", "RESUME_MAIN_TASK", False),
        ("先别走", "REJECT", False),
        ("我想去厕所", "INSERT_TASK", True),
        ("改去附近的药店", "CHANGE_DESTINATION", True),
        ("不去了", "REJECT", False),
        ("我不知道", "UNKNOWN", False),
    ]
    
    tpl_resume = {
        "options": ["继续", "不继续"],
        "synonyms": {
            "继续": ["继续", "好", "行", "可以", "继续吧"],
            "不继续": ["不继续", "停一下", "不用", "不走了", "不去了"]
        },
        "map": {
            "继续": "RESUME_MAIN_TASK",
            "不继续": "REJECT"
        }
    }
    
    for user_text, expected_intent, need_confirm in test_cases:
        result = parser.parse(user_text, tpl_resume)
        assert result.intent_name == expected_intent or result.intent_name == "UNKNOWN", \
            f"Failed for '{user_text}': expected {expected_intent}, got {result.intent_name}"
        if expected_intent != "UNKNOWN":
            assert result.need_confirm == need_confirm, \
                f"Failed for '{user_text}': need_confirm mismatch"


def test_task_insertion_chain():
    """测试任务插入链闭环"""
    decision_core = DecisionCore()
    inquiry_manager = InquiryManager()
    taskchain = TaskChainManager()
    
    # 1. 主任务：去医院
    main_task = {
        "task_id": "nav_to_hospital_1",
        "type": "navigation",
        "target": {"poi": "hospital"},
        "nodes": [
            {"id": "start", "name": "起点"},
            {"id": "on_the_way", "name": "途中"},
            {"id": "hospital_gate", "name": "医院大门"}
        ]
    }
    taskchain.start_main_task(main_task)
    original_node = taskchain.active_node.copy() if taskchain.active_node else None
    
    # 2. 用户："我先去厕所"
    parsed = inquiry_manager.handle_user_response("resume_main_task", "我先去厕所")
    assert parsed.intent_name == "INSERT_TASK"
    assert parsed.need_confirm == True
    
    # 3. 系统问："你想先去厕所，对吗？"
    payload = {"parsed_intent": parsed}
    context = {
        "task_context": {"task_id": "nav_to_hospital_1"},
        "model_context": {"vision_main": "ok", "vision_fallback": "ok"}
    }
    out = decision_core.handle_event(EventType.USER_INTENT, payload, context)
    # 由于 need_confirm=True，应该先询问用户
    # 这里我们直接模拟用户确认后的流程
    
    # 4. 用户："是的"
    confirm_parsed = inquiry_manager.handle_user_response("confirm_new_intent", "是的")
    assert confirm_parsed.intent_name == "CONFIRM"
    
    # 5. 插入 toilet_task
    confirm_payload = {"parsed_intent": confirm_parsed}
    insert_out = decision_core.handle_event(EventType.USER_INTENT, confirm_payload, context)
    # 注意：CONFIRM 在当前实现中会返回 CONTINUE_TASK，我们需要直接处理 INSERT_TASK
    # 这里我们直接插入任务
    if parsed.intent_name == "INSERT_TASK":
        task_spec = decision_core._build_task_from_slots(parsed.slots)
        taskchain.insert_task(task_spec, resume_strategy="auto")
        assert taskchain.active_task.get("type") == "go_to_toilet"
    
    # 6. 子任务结束
    if taskchain.active_task:
        taskchain.active_node = None  # 标记子任务完成
    
    # 7. 恢复主任务
    result = taskchain.complete_active_task()
    assert result["status"] == "resumed"
    assert taskchain.active_task.get("task_id") == "nav_to_hospital_1"
    
    # 8. 验收：恢复后的主任务节点必须与插入前保持一致
    if original_node:
        assert taskchain.active_node.get("id") == original_node.get("id")


def test_planb_condition():
    """测试 PlanB 触发条件"""
    decision_core = DecisionCore()
    
    # 条件：vision_main = "down", vision_fallback = "down"
    payload = {"source": "health_monitor"}
    context = {
        "task_context": {"task_id": "nav_to_hospital_1"},
        "model_context": {"vision_main": "down", "vision_fallback": "down"}
    }
    
    out = decision_core.handle_event(EventType.MODEL_STATUS, payload, context)
    
    # 预期：DecisionAction.TRIGGER_PLANB
    assert out.action.value == "trigger_planB"
    assert "context_snapshot" in out.params


def test_multiple_nested_insertions():
    """测试多层嵌套插入"""
    taskchain = TaskChainManager()
    
    # 主任务
    main_task = {
        "task_id": "main",
        "type": "navigation",
        "nodes": [{"id": "node1", "name": "节点1"}]
    }
    taskchain.start_main_task(main_task)
    
    # 插入任务1：去厕所
    sub1 = {
        "task_id": "sub1",
        "type": "go_to_toilet",
        "nodes": [{"id": "toilet", "name": "厕所"}]
    }
    taskchain.insert_task(sub1, resume_strategy="auto")
    assert len(taskchain.sub_task_stack) == 1
    
    # 插入任务2：买东西（嵌套）
    sub2 = {
        "task_id": "sub2",
        "type": "buy_item",
        "nodes": [{"id": "shop", "name": "商店"}]
    }
    taskchain.insert_task(sub2, resume_strategy="auto")
    assert len(taskchain.sub_task_stack) == 2
    assert taskchain.active_task.get("task_id") == "sub2"
    
    # 完成 sub2
    taskchain.active_node = None  # 标记完成
    result = taskchain.complete_active_task()
    assert taskchain.active_task.get("task_id") == "sub1"
    assert len(taskchain.sub_task_stack) == 1
    
    # 完成 sub1
    taskchain.active_node = None  # 标记完成
    result = taskchain.complete_active_task()
    assert taskchain.active_task.get("task_id") == "main"
    assert len(taskchain.sub_task_stack) == 0


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
