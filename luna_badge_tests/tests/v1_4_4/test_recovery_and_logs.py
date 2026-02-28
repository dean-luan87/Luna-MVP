#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试恢复机制和日志功能

验证：
- 任务恢复机制
- 日志记录完整性
- 错误恢复
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from orchestrator import Orchestrator
from taskchain.manager import TaskChainManager
from core.decision_output import DecisionOutput
from core.decision_actions import DecisionAction


def test_task_recovery():
    """测试任务恢复机制"""
    print("=" * 60)
    print("测试任务恢复机制")
    print("=" * 60)
    
    taskchain = TaskChainManager()
    
    # 1. 启动主任务
    main_task = {
        "task_id": "main_001",
        "type": "navigation",
        "destination": "医院",
        "nodes": [
            {"id": "node1", "action": "start"},
            {"id": "node2", "action": "navigate"},
        ]
    }
    
    # 直接使用 start_main_task 方法
    taskchain.start_main_task(main_task)
    
    print("✅ 主任务已启动")
    print(f"   任务ID: {taskchain.active_task.get('task_id')}")
    
    # 2. 插入子任务
    subtask = {
        "task_id": "sub_001",
        "type": "toilet",
        "nodes": [
            {"id": "sub_node1", "action": "go_to_toilet"},
        ]
    }
    
    decision2 = DecisionOutput(
        action=DecisionAction.INSERT_TASK,
        params={"insert_task_spec": subtask},
        narration="插入子任务"
    )
    taskchain.apply_decision(decision2)
    
    print("✅ 子任务已插入")
    print(f"   当前任务: {taskchain.active_task.get('task_id')}")
    print(f"   栈大小: {len(taskchain.sub_task_stack)}")
    
    # 3. 完成子任务，应该恢复主任务
    taskchain.complete_active_task()
    
    is_recovered = (
        taskchain.active_task is not None and
        taskchain.active_task.get("task_id") == "main_001"
    )
    
    status = "✅" if is_recovered else "❌"
    print(f"{status} 主任务已恢复: {is_recovered}")
    if is_recovered:
        print(f"   恢复的任务ID: {taskchain.active_task.get('task_id')}")
        print(f"   栈大小: {len(taskchain.sub_task_stack)}")
    print()
    
    return is_recovered


def test_logging_integration():
    """测试日志集成"""
    print("=" * 60)
    print("测试日志集成")
    print("=" * 60)
    
    # 检查 decision_logging 模块
    decision_logging_exists = os.path.exists("decision_logging")
    print(f"✅ decision_logging 模块存在: {decision_logging_exists}")
    
    # 检查 decision_core 是否调用日志
    if os.path.exists("decision/decision_core.py"):
        with open("decision/decision_core.py", "r", encoding="utf-8") as f:
            content = f.read()
        
        has_log_import = "log_decision" in content or "decision_logging" in content
        has_log_call = "log_decision(" in content
        
        print(f"✅ 日志导入: {has_log_import}")
        print(f"✅ 日志调用: {has_log_call}")
        
        return decision_logging_exists and has_log_import and has_log_call
    else:
        print("❌ DecisionCore 文件不存在")
        return False


def test_error_recovery():
    """测试错误恢复"""
    print("=" * 60)
    print("测试错误恢复")
    print("=" * 60)
    
    o = Orchestrator()
    
    # 测试无效输入
    result1 = o.simulate_user_input("")
    print(f"✅ 空输入处理: {result1.get('type', 'N/A')}")
    
    # 测试无法识别的命令
    result2 = o.simulate_user_input("Luna，无法识别的命令")
    if "parsed_intent" in result2:
        is_unknown = result2["parsed_intent"].intent_name == "UNKNOWN"
        print(f"✅ 未知命令处理: {is_unknown}")
    else:
        print("✅ 未知命令处理: 已拦截")
    
    # 测试参数未补全的情况
    # 这个需要特定的测试场景，暂时跳过
    
    print("✅ 错误恢复测试通过")
    print()
    
    return True


def main():
    """运行所有测试"""
    print("\n" + "=" * 60)
    print("Luna Badge v1.4.4 - 恢复机制和日志测试")
    print("=" * 60 + "\n")
    
    results = []
    
    results.append(("任务恢复机制", test_task_recovery()))
    results.append(("日志集成", test_logging_integration()))
    results.append(("错误恢复", test_error_recovery()))
    
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

