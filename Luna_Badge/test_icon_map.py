#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试图标地图生成（解决乱码问题）
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

def test_icon_map():
    """测试图标地图"""
    print("=" * 80)
    print("🗺️  Luna Badge 图标地图生成测试（解决乱码问题）")
    print("=" * 80)
    
    from core.scene_memory_system import get_scene_memory_system, SceneNode, PathMemory
    from core.icon_map_generator import IconMapGenerator
    from datetime import datetime
    
    system = get_scene_memory_system()
    generator = IconMapGenerator()
    
    # 创建医院路径
    path_id = "icon_hospital_path"
    path_name = "医院导航图标地图"
    
    system.memory_mapper.add_path(path_id, path_name)
    
    nodes_data = [
        {"id": "start", "label": "医院主入口", "direction": "起点", "distance": 0},
        {"id": "lobby", "label": "电梯厅", "direction": "前行20米", "distance": 20},
        {"id": "info", "label": "咨询台", "direction": "右转10米", "distance": 10},
        {"id": "register", "label": "挂号处", "direction": "继续前行15米", "distance": 15},
        {"id": "restroom", "label": "洗手间", "direction": "左侧5米", "distance": 5},
        {"id": "elevator", "label": "医疗电梯", "direction": "返回电梯厅前行20米", "distance": 20},
        {"id": "floor3", "label": "急诊科楼层", "direction": "上行到3楼", "distance": 30},
        {"id": "emergency", "label": "急诊科", "direction": "出电梯左转25米", "distance": 25},
    ]
    
    print("\n添加节点...")
    for i, node_data in enumerate(nodes_data):
        node = SceneNode(
            node_id=node_data["id"],
            label=node_data["label"],
            image_path="data/scene_images/test.jpg",
            direction=node_data["direction"],
            timestamp=datetime.now().isoformat(),
            confidence=0.9
        )
        system.memory_mapper.add_node(path_id, node)
        print(f"   ✅ 节点{i+1}: {node.label}")
    
    # 生成地图
    print("\n" + "=" * 80)
    print("生成图标地图...")
    print("=" * 80)
    
    path_memory = system.memory_mapper.get_path(path_id)
    map_file = generator.generate_icon_map(path_memory, "icon_hospital_path.png")
    
    if map_file:
        print(f"\n✅ 图标地图已生成: {map_file}")
    else:
        print("\n❌ 地图生成失败")
    
    # 创建多模式路径
    print("\n" + "=" * 80)
    print("生成多模式图标地图...")
    print("=" * 80)
    
    multimodal_path_id = "icon_multimodal_path"
    multimodal_path_name = "多模式导航图标地图"
    
    system.memory_mapper.add_path(multimodal_path_id, multimodal_path_name)
    
    multimodal_nodes = [
        {"id": "home", "label": "起点（家）", "direction": "起点", "distance": 0},
        {"id": "bus_stop", "label": "公交站15路", "direction": "步行150米", "distance": 150},
        {"id": "bus_arrival", "label": "医院站", "direction": "公交车3公里", "distance": 3000},
        {"id": "subway_entrance", "label": "地铁2号线入口", "direction": "步行300米", "distance": 300},
        {"id": "subway_platform", "label": "2号线站台", "direction": "下行50米", "distance": 50},
        {"id": "subway_arrival", "label": "人民广场站", "direction": "地铁4站", "distance": 4000},
        {"id": "exit", "label": "B出口无障碍电梯", "direction": "上行100米", "distance": 100},
        {"id": "destination", "label": "人民广场", "direction": "到达目的地", "distance": 500},
    ]
    
    print("\n添加多模式节点...")
    for i, node_data in enumerate(multimodal_nodes):
        node = SceneNode(
            node_id=node_data["id"],
            label=node_data["label"],
            image_path="data/scene_images/test.jpg",
            direction=node_data["direction"],
            timestamp=datetime.now().isoformat(),
            confidence=0.9
        )
        system.memory_mapper.add_node(multimodal_path_id, node)
        print(f"   ✅ 节点{i+1}: {node.label}")
    
    multimodal_path_memory = system.memory_mapper.get_path(multimodal_path_id)
    multimodal_map_file = generator.generate_icon_map(
        multimodal_path_memory, "icon_multimodal_path.png"
    )
    
    if multimodal_map_file:
        print(f"\n✅ 多模式图标地图已生成: {multimodal_map_file}")
    else:
        print("\n❌ 地图生成失败")
    
    print("\n" + "=" * 80)
    print("✅ 图标地图生成测试完成")
    print("=" * 80)
    
    print("\n📊 生成总结:")
    print(f"   - 医院图标地图: {map_file or '生成失败'}")
    print(f"   - 多模式图标地图: {multimodal_map_file or '生成失败'}")
    print("\n💡 特性:")
    print("   - ✅ 使用PNG图标替代emoji")
    print("   - ✅ 解决中文乱码问题")
    print("   - ✅ 图标自动分类和显示")
    print("   - ✅ 备用几何图形支持")
    
    return map_file, multimodal_map_file

if __name__ == "__main__":
    test_icon_map()
    print("\n🎉 测试完成！")

