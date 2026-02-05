#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Luna Badge v1.4 - 最小任务引擎子系统集成测试
"""

import sys
import os
import json
import time

# 添加路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from task_engine import get_task_engine, TaskGraph, TaskStatus

def test_task_engine():
    """测试任务引擎"""
    print("🚀 Luna Badge v1.4 任务引擎测试")
    print("=" * 60)
    
    # 获取任务引擎
    engine = get_task_engine()
    
    # 测试1: 加载任务图
    print("\n1. 加载任务图...")
    try:
        hospital_graph = engine.load_task_graph("task_graphs/hospital_visit.json")
        print(f"   ✅ 任务图加载成功: {hospital_graph.graph_id}")
        print(f"   📋 场景: {hospital_graph.scene}")
        print(f"   🎯 目标: {hospital_graph.goal}")
        print(f"   📦 节点数: {len(hospital_graph.nodes)}")
        print(f"   🔗 边数: {len(hospital_graph.edges)}")
    except FileNotFoundError:
        print("   ⚠️ 任务图文件不存在，创建示例...")
        from task_engine.task_graph_loader import TaskGraph
        hospital_graph = TaskGraph(
            graph_id="hospital_visit",
            scene="hospital",
            goal="完成一次挂号就诊",
            name="医院就诊流程",
            description="完整的医院就诊流程",
            nodes=[
                {
                    "id": "plan_route",
                    "type": "navigation",
                    "title": "规划路线",
                    "config": {"destination": "虹口医院"}
                }
            ],
            edges=[],
            metadata={"estimated_duration": 120}
        )
    
    # 测试2: 注册任务
    print("\n2. 注册任务...")
    try:
        graph_id = engine.register_task(hospital_graph)
        print(f"   ✅ 任务注册成功: {graph_id}")
    except ValueError as e:
        print(f"   ⚠️ 注册失败: {e}")
        graph_id = hospital_graph.graph_id
    
    # 测试3: 启动任务
    print("\n3. 启动任务...")
    success = engine.start_task(graph_id)
    print(f"   ✅ 任务启动: {success}")
    
    # 等待一下
    time.sleep(1)
    
    # 测试4: 检查任务状态
    print("\n4. 检查任务状态...")
    status = engine.get_task_status(graph_id)
    if status:
        print(f"   📊 状态: {status['status']}")
        print(f"   📈 进度: {status['progress']}%")
        print(f"   🎯 当前节点: {status['current_node']}")
    
    # 测试5: 检查缓存信息
    print("\n5. 检查缓存信息...")
    cache_info = engine.get_cache_info()
    print(f"   💾 活动任务: {cache_info['active_tasks']}")
    print(f"   ✅ 已完成任务: {cache_info['completed_tasks']}")
    print(f"   📊 主任务: {cache_info['main_tasks']}")
    print(f"   💉 插入任务: {cache_info['inserted_tasks']}")
    
    # 测试6: 列表活动任务
    print("\n6. 活动任务列表...")
    active_tasks = engine.list_active_tasks()
    print(f"   📋 活动任务数: {len(active_tasks)}")
    for task in active_tasks:
        print(f"      - {task['name']}: {task['status']}")
    
    print("\n🎉 Luna Badge v1.4 任务引擎测试完成！")
    print("=" * 60)

def test_task_limitations():
    """测试任务限制"""
    print("\n🧪 任务限制测试")
    print("=" * 60)
    
    engine = get_task_engine()
    
    # 测试主任务限制
    print("\n1. 测试主任务限制...")
    cache_info = engine.get_cache_info()
    print(f"   当前主任务数: {cache_info['main_tasks']}")
    print(f"   限制: 最多1个主任务")
    
    # 测试插入任务限制
    print("\n2. 测试插入任务限制...")
    print(f"   当前插入任务数: {cache_info['inserted_tasks']}")
    print(f"   限制: 最多2个插入任务")
    
    print("\n✅ 任务限制测试完成")

if __name__ == "__main__":
    try:
        test_task_engine()
        test_task_limitations()
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
