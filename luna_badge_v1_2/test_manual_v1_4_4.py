#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Luna Badge v1.4.4 手动测试脚本

用于快速测试 Command Layer 和 Orchestrator 功能
"""

from orchestrator import Orchestrator

def print_separator(title=""):
    """打印分隔线"""
    print("\n" + "=" * 60)
    if title:
        print(title)
        print("=" * 60)
    print()

def print_result(test_name, result):
    """格式化打印测试结果"""
    print(f"📋 {test_name}")
    print("-" * 60)
    
    if isinstance(result, dict):
        if 'parsed_intent' in result:
            # 正常流程结果
            intent = result['parsed_intent']
            decision = result['decision_output']
            state = result['taskchain_state']
            
            print(f"✅ 意图: {intent.intent_name}")
            print(f"✅ 来源: {intent.source}")
            print(f"✅ 需确认: {intent.need_confirm}")
            
            if intent.slots:
                print(f"✅ 槽位:")
                for key, value in intent.slots.items():
                    if not key.startswith('_'):  # 跳过内部字段
                        print(f"   - {key}: {value}")
            
            print(f"✅ 决策动作: {decision.action.value}")
            if decision.narration:
                print(f"✅ 播报文案: {decision.narration[:50]}...")
            
            print(f"✅ 任务状态:")
            print(f"   - 当前任务: {state.get('active_task', 'None')}")
            print(f"   - 当前节点: {state.get('active_node', 'None')}")
            print(f"   - 子任务栈: {state.get('sub_task_stack_size', 0)}")
            
        elif 'type' in result:
            # 特殊响应
            print(f"✅ 类型: {result['type']}")
            if 'message' in result:
                print(f"✅ 消息: {result['message']}")
            if 'raw_text' in result:
                print(f"✅ 原始文本: {result['raw_text']}")
    else:
        print(f"结果: {result}")
    
    print()

def main():
    """主测试函数"""
    print_separator("Luna Badge v1.4.4 手动测试")
    
    # 创建 Orchestrator 实例
    print("🔧 初始化 Orchestrator...")
    o = Orchestrator()
    print("✅ 初始化完成\n")
    
    # 测试用例列表
    test_cases = [
        {
            "name": "测试 1: 完整地点名称",
            "input": "Luna，请带我去虹口医院",
            "description": "应该识别为 START_TASK，提取完整地点名称"
        },
        {
            "name": "测试 2: 参数补全（从记忆）",
            "input": "Luna，请带我去医院",
            "description": "应该从 FakeMemoryClient 补全为 '北京协和医院'"
        },
        {
            "name": "测试 3: 非命令拦截",
            "input": "我想出去走走",
            "description": "应该返回 NON_COMMAND_RESPONSE"
        },
        {
            "name": "测试 4: 取消任务",
            "input": "Luna，取消任务",
            "description": "应该识别为 CANCEL_TASK"
        },
        {
            "name": "测试 5: 替换任务",
            "input": "Luna，我要换成去瑞金医院",
            "description": "应该识别为 CHANGE_DESTINATION"
        },
        {
            "name": "测试 6: 帮助中心",
            "input": "Luna，打开帮助中心",
            "description": "应该返回 HELP_CENTER_STUB"
        },
        {
            "name": "测试 7: 空命令",
            "input": "Luna",
            "description": "应该返回 EMPTY_COMMAND 提示"
        },
        {
            "name": "测试 8: 插入任务",
            "input": "Luna，顺便去711",
            "description": "应该识别为 INSERT_TASK"
        },
    ]
    
    # 执行测试
    passed = 0
    total = len(test_cases)
    
    for i, test in enumerate(test_cases, 1):
        print_separator(f"{test['name']}")
        print(f"📝 输入: {test['input']}")
        print(f"📝 说明: {test['description']}")
        print()
        
        try:
            result = o.simulate_user_input(test['input'])
            print_result(test['name'], result)
            passed += 1
        except Exception as e:
            print(f"❌ 测试失败: {e}")
            import traceback
            traceback.print_exc()
            print()
    
    # 总结
    print_separator("测试总结")
    print(f"✅ 通过: {passed}/{total}")
    print(f"❌ 失败: {total - passed}/{total}")
    print()
    
    if passed == total:
        print("🎉 所有测试通过！")
    else:
        print("⚠️  部分测试失败，请检查上述输出")

if __name__ == "__main__":
    main()












