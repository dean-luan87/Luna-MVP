#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 Orchestrator 完整流程

验证从用户输入到任务执行的完整流程
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from orchestrator import Orchestrator


def test_full_pipeline():
    """测试完整流程"""
    print("=" * 60)
    print("测试 Orchestrator 完整流程")
    print("=" * 60)
    
    o = Orchestrator()
    
    test_cases = [
        {
            "name": "完整流程 - 导航任务",
            "input": "Luna，请带我去虹口医院",
            "expected_intent": "START_TASK",
            "expected_source": "command_layer"
        },
        {
            "name": "完整流程 - 参数补全",
            "input": "Luna，请带我去医院",
            "expected_intent": "START_TASK",
            "expected_source": "command_layer"
        },
        {
            "name": "完整流程 - 非命令拦截",
            "input": "我想出去走走",
            "expected_type": "NON_COMMAND_RESPONSE"
        },
        {
            "name": "完整流程 - 取消任务",
            "input": "Luna，取消任务",
            "expected_intent": "CANCEL_TASK",
            "expected_source": "command_layer"
        },
        {
            "name": "完整流程 - 替换任务",
            "input": "Luna，我要换成去瑞金医院",
            "expected_intent": "CHANGE_DESTINATION",
            "expected_source": "command_layer"
        },
        {
            "name": "完整流程 - 帮助中心",
            "input": "Luna，打开帮助中心",
            "expected_type": "HELP_CENTER_STUB"
        },
    ]
    
    passed = 0
    for test in test_cases:
        result = o.simulate_user_input(test["input"])
        
        is_pass = False
        if "expected_intent" in test:
            is_pass = (
                "parsed_intent" in result and
                result["parsed_intent"].intent_name == test["expected_intent"] and
                result["parsed_intent"].source == test.get("expected_source", "command_layer")
            )
        elif "expected_type" in test:
            is_pass = result.get("type") == test["expected_type"]
        
        status = "✅" if is_pass else "❌"
        print(f"{status} {test['name']}")
        print(f"   输入: {test['input']}")
        if "parsed_intent" in result:
            print(f"   意图: {result['parsed_intent'].intent_name}")
            print(f"   来源: {result['parsed_intent'].source}")
            print(f"   决策: {result['decision_output'].action.value}")
        elif "type" in result:
            print(f"   类型: {result['type']}")
        if is_pass:
            passed += 1
        print()
    
    print(f"通过: {passed}/{len(test_cases)}")
    return passed == len(test_cases)


def test_pipeline_stages():
    """测试流程各阶段"""
    print("=" * 60)
    print("测试流程各阶段")
    print("=" * 60)
    
    o = Orchestrator()
    
    # 测试完整流程的每个阶段
    result = o.simulate_user_input("Luna，请带我去医院")
    
    stages_passed = []
    
    # 阶段 1: 命令检测
    if "parsed_intent" in result and result["parsed_intent"].source == "command_layer":
        stages_passed.append("命令检测")
        print("✅ 阶段 1: 命令检测通过")
    
    # 阶段 2: 语义归一化
    if "parsed_intent" in result and result["parsed_intent"].intent_name:
        stages_passed.append("语义归一化")
        print("✅ 阶段 2: 语义归一化通过")
    
    # 阶段 3: 参数补全
    if "parsed_intent" in result and "_resolution_source" in result["parsed_intent"].slots:
        stages_passed.append("参数补全")
        print("✅ 阶段 3: 参数补全通过")
    
    # 阶段 4: 决策生成
    if "decision_output" in result:
        stages_passed.append("决策生成")
        print("✅ 阶段 4: 决策生成通过")
    
    # 阶段 5: 任务应用
    if "taskchain_state" in result:
        stages_passed.append("任务应用")
        print("✅ 阶段 5: 任务应用通过")
    
    print(f"\n通过阶段: {len(stages_passed)}/5")
    return len(stages_passed) == 5


def main():
    """运行所有测试"""
    print("\n" + "=" * 60)
    print("Luna Badge v1.4.4 - Orchestrator 流程测试")
    print("=" * 60 + "\n")
    
    results = []
    
    results.append(("完整流程", test_full_pipeline()))
    results.append(("流程各阶段", test_pipeline_stages()))
    
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

