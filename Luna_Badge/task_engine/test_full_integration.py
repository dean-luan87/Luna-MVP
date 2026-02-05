#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Luna Badge v1.4 - 完整集成测试
测试所有模块的功能和集成
"""

import sys
import time
from task_engine import (
    get_task_engine, get_graph_loader, get_report_uploader,
    TaskStateManager, TaskCacheManager, InsertedTaskQueue,
    FailsafeTrigger, RestartRecoveryFlow
)

def test_all_modules():
    """测试所有模块"""
    print("🚀 Luna Badge v1.4 全量集成测试")
    print("=" * 70)
    
    results = []
    
    # 测试1: 任务图加载器
    print("\n📄 测试1: 任务图加载器")
    try:
        loader = get_graph_loader("task_engine/task_graphs")
        graph = loader.load_from_file("hospital_visit.json")
        assert graph.graph_id == "hospital_visit"
        assert len(graph.nodes) > 0
        print("   ✅ 任务图加载成功")
        results.append(("任务图加载", True))
    except Exception as e:
        print(f"   ❌ 失败: {e}")
        results.append(("任务图加载", False))
    
    # 测试2: 状态管理器
    print("\n📊 测试2: 状态管理器")
    try:
        state_manager = TaskStateManager()
        state_manager.init_task_state("test_task", ["node1", "node2", "node3"])
        state_manager.update_node_status("test_task", "node1", "complete")
        status = state_manager.get_node_status("test_task", "node1")
        assert status == "complete"
        print("   ✅ 状态管理正常")
        results.append(("状态管理", True))
    except Exception as e:
        print(f"   ❌ 失败: {e}")
        results.append(("状态管理", False))
    
    # 测试3: 缓存管理器
    print("\n💾 测试3: 缓存管理器")
    try:
        cache = TaskCacheManager(default_ttl=60)
        cache.set_cache("test_key", "test_value", ttl=60)
        value = cache.get_cache("test_key")
        assert value == "test_value"
        assert cache.has_cache("test_key")
        print("   ✅ 缓存管理正常")
        results.append(("缓存管理", True))
    except Exception as e:
        print(f"   ❌ 失败: {e}")
        results.append(("缓存管理", False))
    
    # 测试4: 插入任务队列
    print("\n💉 测试4: 插入任务队列")
    try:
        queue = InsertedTaskQueue(state_manager=state_manager)
        queue.register_inserted_task("main_task", "inserted_task", "resume_node")
        assert queue.is_inserted_task_active()
        resume_point = queue.complete_inserted_task("inserted_task")
        assert resume_point == "resume_node"
        print("   ✅ 插入任务管理正常")
        results.append(("插入任务", True))
    except Exception as e:
        print(f"   ❌ 失败: {e}")
        results.append(("插入任务", False))
    
    # 测试5: 故障安全触发器
    print("\n🔐 测试5: 故障安全触发器")
    try:
        failsafe = FailsafeTrigger(state_manager=state_manager, cache_manager=cache)
        failsafe.monitor_heartbeat("test_module")
        failsafe.record_heartbeat("test_module")
        failsafe.trigger_failsafe("测试故障", module_name="test_module")
        assert failsafe.failsafe_mode == True
        print("   ✅ 故障安全机制正常")
        results.append(("故障安全", True))
    except Exception as e:
        print(f"   ❌ 失败: {e}")
        results.append(("故障安全", False))
    
    # 测试6: 重启恢复引导
    print("\n🔄 测试6: 重启恢复引导")
    try:
        recovery = RestartRecoveryFlow(state_manager=state_manager, cache_manager=cache)
        # 创建恢复上下文
        import json
        import os
        os.makedirs("data", exist_ok=True)
        with open("data/restart_context.json", "w") as f:
            json.dump({
                "task_id": "test_task",
                "last_node_id": "node2",
                "timestamp": "2025-10-30T10:00:00",
                "reason": "测试",
                "valid": True
            }, f)
        has_context = recovery.check_restart_context()
        assert has_context == True
        print("   ✅ 恢复引导正常")
        results.append(("恢复引导", True))
    except Exception as e:
        print(f"   ❌ 失败: {e}")
        results.append(("恢复引导", False))
    
    # 测试7: 任务引擎
    print("\n🎯 测试7: 任务引擎")
    try:
        engine = get_task_engine()
        graph = engine.load_task_graph("task_engine/task_graphs/hospital_visit.json")
        assert graph is not None
        print("   ✅ 任务引擎正常")
        results.append(("任务引擎", True))
    except Exception as e:
        print(f"   ❌ 失败: {e}")
        results.append(("任务引擎", False))
    
    # 测试8: 报告上传器
    print("\n📤 测试8: 报告上传器")
    try:
        uploader = get_report_uploader()
        success = uploader.upload_task_report({
            "task_id": "test",
            "user_id": "test_user",
            "graph_name": "测试",
            "execution_path": [],
            "duration": 60,
            "status": "completed"
        })
        print(f"   ✅ 报告上传器正常 (成功: {success})")
        results.append(("报告上传", True))
    except Exception as e:
        print(f"   ❌ 失败: {e}")
        results.append(("报告上传", False))
    
    # 总结
    print("\n" + "=" * 70)
    print("📊 测试总结")
    print("=" * 70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"   {name:<20} {status}")
    
    print(f"\n总计: {passed}/{total} 测试通过 ({passed*100//total}%)")
    
    return passed == total


if __name__ == "__main__":
    success = test_all_modules()
    sys.exit(0 if success else 1)

