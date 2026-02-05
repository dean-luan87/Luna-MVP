#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 DecisionCore 功能

验证 DecisionCore 正确处理来自 Command Layer 的意图
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from decision.decision_core import DecisionCore
from core.events import EventType
from core.intent_schema import ParsedIntent
from core.decision_actions import DecisionAction


def test_decision_core_with_command_intents():
    """测试 DecisionCore 处理 Command Layer 的意图"""
    print("=" * 60)
    print("测试 DecisionCore 处理 Command Layer 意图")
    print("=" * 60)
    
    decision_core = DecisionCore()
    
    test_cases = [
        {
            "name": "START_TASK 意图",
            "intent": ParsedIntent(
                intent_name="START_TASK",
                slots={"destination": "虹口医院"},
                source="command_layer",
                need_confirm=True
            ),
            "expected_action": DecisionAction.NO_OP  # DecisionCore 当前未处理 START_TASK，返回 NO_OP
        },
        {
            "name": "CANCEL_TASK 意图",
            "intent": ParsedIntent(
                intent_name="CANCEL_TASK",
                slots={},
                source="command_layer",
                need_confirm=False
            ),
            "expected_action": DecisionAction.NO_OP
        },
        {
            "name": "INSERT_TASK 意图（需要确认）",
            "intent": ParsedIntent(
                intent_name="INSERT_TASK",
                slots={"task_type": "toilet"},
                source="command_layer",
                need_confirm=True
            ),
            "expected_action": DecisionAction.ASK_USER  # 需要确认时返回 ASK_USER
        },
        {
            "name": "CHANGE_DESTINATION 意图（需要确认）",
            "intent": ParsedIntent(
                intent_name="CHANGE_DESTINATION",
                slots={"destination": "瑞金医院"},
                source="command_layer",
                need_confirm=True
            ),
            "expected_action": DecisionAction.ASK_USER  # 需要确认时返回 ASK_USER
        },
    ]
    
    passed = 0
    for test in test_cases:
        payload = {"parsed_intent": test["intent"]}
        context = {
            "task_context": {"task_id": "", "task_type": ""},
            "model_context": {"vision_main": "ok", "vision_fallback": "ok"}
        }
        
        decision_output = decision_core.handle_event(
            EventType.USER_INTENT,
            payload,
            context
        )
        
        is_pass = decision_output.action == test["expected_action"]
        status = "✅" if is_pass else "❌"
        print(f"{status} {test['name']}")
        print(f"   意图: {test['intent'].intent_name}")
        print(f"   决策动作: {decision_output.action.value} (期望: {test['expected_action'].value})")
        print(f"   播报: {decision_output.narration[:50]}...")
        if is_pass:
            passed += 1
        print()
    
    print(f"通过: {passed}/{len(test_cases)}")
    return passed == len(test_cases)


def test_decision_core_logging():
    """测试 DecisionCore 是否正确调用日志"""
    print("=" * 60)
    print("测试 DecisionCore 日志调用")
    print("=" * 60)
    
    # 检查 decision_core.py 是否包含 log_decision 调用
    decision_core_file = "decision/decision_core.py"
    if os.path.exists(decision_core_file):
        with open(decision_core_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        has_log_import = "log_decision" in content or "decision_logging" in content
        has_log_call = "log_decision(" in content
        
        print(f"✅ 日志导入: {has_log_import}")
        print(f"✅ 日志调用: {has_log_call}")
        
        return has_log_import and has_log_call
    else:
        print("❌ DecisionCore 文件不存在")
        return False


def main():
    """运行所有测试"""
    print("\n" + "=" * 60)
    print("Luna Badge v1.4.4 - DecisionCore 测试")
    print("=" * 60 + "\n")
    
    results = []
    
    results.append(("DecisionCore 意图处理", test_decision_core_with_command_intents()))
    results.append(("DecisionCore 日志调用", test_decision_core_logging()))
    
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print(f"\n总计: {passed}/{total} 通过")
    
    if passed == total:
        print("\n🎉 所有测试通过！")
        return 0
    else:
        print("\n⚠️  部分测试失败")
        return 1


if __name__ == "__main__":
    sys.exit(main())

