#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Luna Badge v1.4 - 完整集成测试脚本
"""

import sys
import time

print("🚀 Luna Badge v1.4 完整集成测试")
print("=" * 70)

test_results = []

def test(name, test_func):
    """统一的测试函数"""
    try:
        print(f"\n📋 测试: {name}")
        result = test_func()
        if result:
            print(f"   ✅ 通过")
            test_results.append((name, True))
        else:
            print(f"   ❌ 失败")
            test_results.append((name, False))
    except Exception as e:
        print(f"   ❌ 异常: {e}")
        test_results.append((name, False))

# 导入所有模块
import sys
sys.path.insert(0, '.')

# 测试1
def test1():
    from task_engine.task_graph_loader import TaskGraphLoader
    loader = TaskGraphLoader(base_path='task_engine/task_graphs')
    graph = loader.load_from_file('hospital_visit.json')
    return graph.graph_id == "hospital_visit" and len(graph.nodes) == 13

# 测试2
def test2():
    from task_engine.task_state_manager import TaskStateManager
    m = TaskStateManager()
    m.init_task_state("test", ["n1"])
    m.update_node_status("test", "n1", "complete")
    return m.get_node_status("test", "n1") == "complete"

# 测试3
def test3():
    from task_engine.task_cache_manager import TaskCacheManager
    c = TaskCacheManager()
    c.set_cache("k", "v")
    return c.get_cache("k") == "v"

# 测试4
def test4():
    from task_engine.inserted_task_queue import InsertedTaskQueue
    q = InsertedTaskQueue()
    q.register_inserted_task("main", "ins", "resume")
    return q.is_inserted_task_active()

# 测试5
def test5():
    from task_engine.failsafe_trigger import FailsafeTrigger
    f = FailsafeTrigger()
    f.monitor_heartbeat("test")
    return True

# 测试6
def test6():
    from task_engine.restart_recovery_flow import RestartRecoveryFlow
    r = RestartRecoveryFlow()
    return True

test("任务图加载器", test1)
test("状态管理器", test2)
test("缓存管理器", test3)
test("插入任务队列", test4)
test("故障安全触发器", test5)
test("重启恢复引导", test6)

# 总结
print("\n" + "=" * 70)
print("📊 测试总结")
print("=" * 70)

passed = sum(1 for _, r in test_results if r)
total = len(test_results)

for name, r in test_results:
    print(f"   {name:<20} {'✅ 通过' if r else '❌ 失败'}")

print(f"\n总计: {passed}/{total} 测试通过 ({passed*100//total}%)")
print("=" * 70)

sys.exit(0 if passed == total else 1)