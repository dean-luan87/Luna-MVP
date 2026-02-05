#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge 完整路径规划测试
测试路径解析、路径增长、断点追加
"""

import sys
import os
import cv2
import numpy as np
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

def test_path_resolver():
    """测试路径解析器"""
    print("=" * 60)
    print("测试1: 路径解析器")
    print("=" * 60)
    
    from core.path_resolver import PathResolver
    
    resolver = PathResolver()
    
    # 测试节点查找
    print("\n1. 测试节点查找:")
    test_nodes = ["挂号处（已修正）", "Elevator", "Exit"]
    for node in test_nodes:
        path_id = resolver.find_path_for_node(node)
        print(f"   节点 '{node}' 在路径: {path_id or '未找到'}")
    
    # 测试路径判断
    print("\n2. 测试路径创建判断:")
    result = resolver.should_create_new_path("挂号处（已修正）", "Exit")
    print(f"   判断结果: {result['should_create']}")
    print(f"   原因: {result['reason']}")
    print(f"   消息: {result['message']}")
    
    # 测试连续性
    print("\n3. 测试路径连续性:")
    result = resolver.get_path_continuity("test_hospital_path", "挂号处（已修正）")
    print(f"   连续性: {result.get('continuous', False)}")
    if result.get('continuous'):
        print(f"   索引: {result.get('index')}/{result.get('total_nodes')}")
        print(f"   下一个: {result.get('next_node')}")

def test_path_growth():
    """测试路径增长管理器"""
    print("\n" + "=" * 60)
    print("测试2: 路径增长管理器")
    print("=" * 60)
    
    from core.path_growth import PathGrowthManager
    from core.scene_memory_system import SceneNode
    from datetime import datetime
    
    manager = PathGrowthManager(distance_threshold=50.0)
    
    # 创建测试节点
    test_node = SceneNode(
        node_id="test_new",
        label="New Location",
        image_path="data/scene_images/test.jpg",
        timestamp=datetime.now().isoformat()
    )
    
    # 测试扩展判断
    print("\n1. 测试路径扩展判断:")
    result = manager.should_extend_path("test_hospital_path", test_node)
    print(f"   应该扩展: {result['should_extend']}")
    print(f"   原因: {result['reason']}")
    print(f"   指标: 距离={result['metrics'].get('distance', 0):.1f}m, "
          f"相似度={result['metrics'].get('visual_similarity', 0):.2f}")
    
    # 测试中断处理
    print("\n2. 测试路径中断处理:")
    result = manager.handle_path_interruption("test_hospital_path", test_node, user_override=False)
    print(f"   执行动作: {result['action']}")
    print(f"   消息: {result['message']}")
    
    # 测试用户重置
    print("\n3. 测试用户重置:")
    result = manager.handle_path_interruption("test_hospital_path", test_node, user_override=True)
    print(f"   执行动作: {result['action']}")
    print(f"   新路径ID: {result.get('path_id')}")

def test_memory_mapper_enhancement():
    """测试记忆映射器增强功能"""
    print("\n" + "=" * 60)
    print("测试3: 记忆映射器增强")
    print("=" * 60)
    
    from core.scene_memory_system import get_scene_memory_system
    
    system = get_scene_memory_system()
    
    # 测试路径统计
    print("\n1. 测试路径统计:")
    stats = system.memory_mapper.get_path_statistics("test_hospital_path")
    if stats:
        print(f"   路径: {stats['path_name']}")
        print(f"   节点数: {stats['total_nodes']}")
        print(f"   节点类型: {stats['node_types']}")
    
    # 测试断点追加
    print("\n2. 测试断点追加:")
    node_data = {
        "label": "附加节点",
        "image_path": "data/scene_images/test.jpg",
        "confidence": 0.95
    }
    
    result = system.memory_mapper.append_node_to_path("test_hospital_path", node_data)
    print(f"   追加结果: {'成功' if result else '失败'}")
    
    # 显示更新后的统计
    print("\n3. 更新后的路径统计:")
    stats = system.memory_mapper.get_path_statistics("test_hospital_path")
    if stats:
        print(f"   节点数: {stats['total_nodes']}")

def test_complete_workflow():
    """测试完整工作流"""
    print("\n" + "=" * 60)
    print("测试4: 完整工作流")
    print("=" * 60)
    
    from core.path_resolver import PathResolver
    from core.path_growth import PathGrowthManager
    from core.scene_memory_system import get_scene_memory_system
    
    resolver = PathResolver()
    manager = PathGrowthManager()
    system = get_scene_memory_system()
    
    print("\n场景: 从已知路径扩展到新节点")
    print("-" * 60)
    
    # 步骤1: 检查当前路径
    current_path = "test_hospital_path"
    next_destination = "New Destination"
    
    # 步骤2: 判断是否需要创建新路径
    path_decision = resolver.should_create_new_path("Exit", next_destination)
    print(f"\n步骤1: 路径决策")
    print(f"   需要创建新路径: {path_decision['should_create']}")
    print(f"   原因: {path_decision['reason']}")
    
    # 步骤3: 如果决定扩展，测试扩展逻辑
    if not path_decision['should_create']:
        print(f"\n步骤2: 将扩展现有路径")
    else:
        print(f"\n步骤2: 将创建新路径")
        
        # 创建测试节点
        from core.scene_memory_system import SceneNode
        from datetime import datetime
        
        new_node = SceneNode(
            node_id="new_dest_node",
            label=next_destination,
            image_path="data/scene_images/new.jpg",
            timestamp=datetime.now().isoformat()
        )
        
        # 决定是扩展还是创建
        growth_decision = manager.should_extend_path(current_path, new_node)
        print(f"   扩展判断: {growth_decision['should_extend']}")
        
        if growth_decision['should_extend']:
            print(f"   执行: 扩展现有路径")
            manager.extend_existing_path(current_path, new_node)
        else:
            print(f"   执行: 创建新路径")
            manager.create_new_path(new_node, "新路径")

def main():
    """主函数"""
    print("\n")
    print("🗺️ Luna Badge 完整路径规划测试")
    print("=" * 60)
    print()
    
    # 运行所有测试
    test_path_resolver()
    test_path_growth()
    test_memory_mapper_enhancement()
    test_complete_workflow()
    
    print("\n" + "=" * 60)
    print("✅ 所有测试完成")
    print("=" * 60)
    print()
    print("📊 新增模块总结:")
    print("  1. PathResolver - 路径解析 ✅")
    print("  2. PathGrowthManager - 路径增长管理 ✅")
    print("  3. MemoryMapper增强 - 断点追加 ✅")
    print()
    print("🎯 关键功能:")
    print("  - 智能判断节点归属")
    print("  - 自动决定路径扩展/创建")
    print("  - 支持断点恢复")
    print("  - 路径统计和分析")
    print()

if __name__ == "__main__":
    main()

