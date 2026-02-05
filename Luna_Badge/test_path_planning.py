#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge 路径规划测试
测试多目的地导航和路径合并
"""

import sys
import os
import cv2
import numpy as np
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

def create_test_paths():
    """创建测试路径"""
    from core.scene_memory_system import get_scene_memory_system
    
    system = get_scene_memory_system()
    
    print("创建测试路径...")
    
    # 路径1: A -> B
    path_a_to_b = []
    for label in ["Start", "Elevator", "Room B"]:
        img = np.ones((800, 1000, 3), dtype=np.uint8) * 255
        cv2.putText(img, label, (100, 400), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 0), 5)
        path_a_to_b.append((label, img))
    
    for label, img in path_a_to_b:
        system.record_node(img, "path_a_to_b", "路径A到B")
    
    # 路径2: A -> C
    path_a_to_c = []
    for label in ["Start", "Hallway", "Room C"]:
        img = np.ones((800, 1000, 3), dtype=np.uint8) * 255
        cv2.putText(img, label, (100, 400), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 0), 5)
        path_a_to_c.append((label, img))
    
    for label, img in path_a_to_c:
        system.record_node(img, "path_a_to_c", "路径A到C")
    
    print(f"✅ 创建了2条路径")
    
    # 显示路径
    print("\n路径详情:")
    for path_id in ["path_a_to_b", "path_a_to_c"]:
        path_memory = system.get_path_memory(path_id)
        if path_memory:
            nodes = [n.label for n in path_memory.nodes]
            print(f"  {path_id}: {' -> '.join(nodes)}")

def test_multiple_destinations():
    """测试多目的地导航"""
    print("\n" + "=" * 60)
    print("测试1: 多目的地路径规划")
    print("=" * 60)
    
    from core.scene_memory_system import get_scene_memory_system
    from core.path_planner import PathPlanner
    
    system = get_scene_memory_system()
    planner = PathPlanner(system)
    
    # 场景1: 从A到B再到C
    print("\n场景1: Start -> Room B -> Room C")
    print("-" * 60)
    result = planner.plan_route("Start", ["Room B", "Room C"])
    
    print(f"能否导航: {result['can_navigate']}")
    print(f"策略: {result['strategy']}")
    print(f"消息: {result['message']}")
    print(f"未知段: {result.get('unknown_segments', [])}")
    
    # 场景2: 从A到C（已知路径）
    print("\n场景2: Start -> Room C (已知路径)")
    print("-" * 60)
    result = planner.plan_route("Start", ["Room C"])
    
    print(f"能否导航: {result['can_navigate']}")
    print(f"策略: {result['strategy']}")
    print(f"消息: {result['message']}")
    print(f"路径段数: {len(result['segments'])}")
    
    # 场景3: 从B到C（未知路径）
    print("\n场景3: Room B -> Room C (未知路径)")
    print("-" * 60)
    result = planner.plan_route("Room B", ["Room C"])
    
    print(f"能否导航: {result['can_navigate']}")
    print(f"策略: {result['strategy']}")
    print(f"消息: {result['message']}")
    print(f"未知段: {result.get('unknown_segments', [])}")

def test_path_merge():
    """测试路径合并"""
    print("\n" + "=" * 60)
    print("测试2: 路径合并")
    print("=" * 60)
    
    from core.scene_memory_system import get_scene_memory_system
    from core.path_planner import PathPlanner
    
    system = get_scene_memory_system()
    planner = PathPlanner(system)
    
    # 合并多条路径
    print("\n合并路径A到B和A到C:")
    merged = planner.merge_paths_to_continuous(["path_a_to_b", "path_a_to_c"])
    
    if merged:
        print(f"合并节点数: {merged['total_length']}")
        print(f"来源路径: {merged['source_paths']}")
        
        print("\n合并后的节点序列:")
        for i, node in enumerate(merged['merged_nodes'], 1):
            print(f"  {i}. {node.label}")

def test_different_strategies():
    """测试不同策略"""
    print("\n" + "=" * 60)
    print("测试3: 不同策略对比")
    print("=" * 60)
    
    from core.scene_memory_system import get_scene_memory_system
    from core.path_planner import PathPlanner
    
    system = get_scene_memory_system()
    
    strategies = ["smart_merge", "fallback", "ask_user"]
    unknown_segments = [{"from": "Room B", "to": "Room C", "index": 0}]
    
    for strategy in strategies:
        print(f"\n策略: {strategy}")
        planner = PathPlanner(system)
        planner.preferred_strategy = strategy
        
        result = planner._handle_unknown_paths(unknown_segments)
        print(f"  能否导航: {result['can_navigate']}")
        print(f"  消息: {result.get('message', 'N/A')}")

def main():
    """主函数"""
    print("\n")
    print("🗺️ Luna Badge 路径规划测试")
    print("=" * 60)
    
    # 创建测试数据
    create_test_paths()
    
    # 运行测试
    test_multiple_destinations()
    test_path_merge()
    test_different_strategies()
    
    print("\n" + "=" * 60)
    print("📊 测试总结")
    print("=" * 60)
    print()
    print("✅ 路径规划功能测试完成")
    print()
    print("🎯 关键功能:")
    print("  1. 多目的地路径规划")
    print("  2. 智能路径合并")
    print("  3. 多种策略支持")
    print("  4. 未知路径处理")
    print()

if __name__ == "__main__":
    main()

