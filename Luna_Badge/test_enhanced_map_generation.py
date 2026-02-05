#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge 增强地图生成测试
展示分层、距离、设施信息功能
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

def test_enhanced_map_generation():
    """测试增强地图生成"""
    print("=" * 80)
    print("🗺️  Luna Badge 增强地图生成测试")
    print("=" * 80)
    
    from core.scene_memory_system import get_scene_memory_system, SceneNode, PathMemory
    from core.enhanced_map_generator import EnhancedMapGenerator
    from datetime import datetime
    
    # 获取系统和生成器
    system = get_scene_memory_system()
    generator = EnhancedMapGenerator()
    
    print("\n" + "=" * 80)
    print("创建完整的医院导航地图（含分层、距离、设施信息）")
    print("=" * 80)
    
    # 创建增强路径
    path_id = "enhanced_hospital_path"
    path_name = "医院增强导航地图"
    
    system.memory_mapper.add_path(path_id, path_name)
    
    # 定义完整的医院路径
    enhanced_nodes = [
        {
            "node_id": "entrance",
            "label": "医院主入口",
            "direction": "起点",
            "node_type": "outdoor",
            "layer": "outdoor"
        },
        {
            "node_id": "elevator_lobby",
            "label": "电梯厅",
            "direction": "前行20米",
            "node_type": "walkway",
            "layer": "indoor",
            "distance": 20
        },
        {
            "node_id": "info_desk",
            "label": "咨询台",
            "direction": "右转10米",
            "node_type": "facility",
            "layer": "indoor",
            "distance": 10,
            "facility_info": {"type": "information", "services": ["咨询", "导诊"]}
        },
        {
            "node_id": "registration",
            "label": "挂号处",
            "direction": "继续前行15米",
            "node_type": "facility",
            "layer": "indoor",
            "distance": 15,
            "facility_info": {"type": "registration", "hours": "8:00-17:00"}
        },
        {
            "node_id": "restroom",
            "label": "洗手间（无障碍）",
            "direction": "左侧5米",
            "node_type": "facility",
            "layer": "indoor",
            "distance": 5,
            "facility_info": {"type": "restroom", "accessibility": "wheelchair_accessible"}
        },
        {
            "node_id": "elevator",
            "label": "医疗电梯",
            "direction": "返回电梯厅前行20米",
            "node_type": "facility",
            "layer": "indoor",
            "distance": 20,
            "facility_info": {"type": "elevator", "capacity": "13人", "usage": "医疗专用"}
        },
        {
            "node_id": "emergency_floor",
            "label": "急诊科楼层",
            "direction": "上行到3楼",
            "node_type": "indoor",
            "layer": "indoor",
            "distance": 30,
            "facility_info": {"type": "department", "floor": 3, "hours": "24小时"}
        },
        {
            "node_id": "emergency_room",
            "label": "急诊科",
            "direction": "出电梯左转25米",
            "node_type": "facility",
            "layer": "indoor",
            "distance": 25,
            "facility_info": {"type": "emergency", "priority": "high", "hours": "24小时"}
        }
    ]
    
    print("\n添加增强节点...")
    for i, node_data in enumerate(enhanced_nodes):
        node = SceneNode(
            node_id=node_data["node_id"],
            label=node_data["label"],
            image_path="data/scene_images/test.jpg",
            direction=node_data["direction"],
            timestamp=datetime.now().isoformat(),
            confidence=0.9
        )
        
        system.memory_mapper.add_node(path_id, node)
        print(f"   ✅ 节点{i+1}: {node.label}")
    
    # 生成增强地图
    print("\n" + "=" * 80)
    print("生成增强地图...")
    print("=" * 80)
    
    path_memory = system.memory_mapper.get_path(path_id)
    map_file = generator.generate_enhanced_map_card(
        path_memory, 
        "enhanced_hospital_map.png"
    )
    
    if map_file:
        print(f"\n✅ 增强地图已生成: {map_file}")
    else:
        print("\n❌ 地图生成失败")
    
    print("\n" + "=" * 80)
    print("创建完整的多模式导航地图（室内+室外+公共交通）")
    print("=" * 80)
    
    # 创建跨模式路径
    multimodal_path_id = "enhanced_multimodal_path"
    multimodal_path_name = "多模式增强导航地图"
    
    system.memory_mapper.add_path(multimodal_path_id, multimodal_path_name)
    
    multimodal_nodes = [
        {
            "node_id": "home",
            "label": "起点（家）",
            "direction": "起点",
            "node_type": "outdoor",
            "layer": "outdoor"
        },
        {
            "node_id": "bus_stop",
            "label": "公交站（15路）",
            "direction": "步行150米",
            "node_type": "transit",
            "layer": "outdoor",
            "distance": 150,
            "transit_info": {"type": "bus", "route": "15", "frequency": "5-10分钟"}
        },
        {
            "node_id": "hospital_entrance_bus",
            "label": "医院站",
            "direction": "乘坐15路公交车约3公里",
            "node_type": "transit",
            "layer": "outdoor",
            "distance": 3000,
            "transit_info": {"type": "bus", "distance": "3km", "time": "8分钟"}
        },
        {
            "node_id": "subway_entrance",
            "label": "地铁2号线入口",
            "direction": "步行300米到达地铁站",
            "node_type": "transit",
            "layer": "outdoor",
            "distance": 300,
            "transit_info": {"type": "subway", "line": "2", "status": "operational"}
        },
        {
            "node_id": "subway_platform",
            "label": "2号线站台",
            "direction": "下行到站台层",
            "node_type": "transit",
            "layer": "indoor",
            "distance": 50,
            "transit_info": {"type": "subway", "direction": "往人民广场", "frequency": "3-5分钟"}
        },
        {
            "node_id": "destination_station",
            "label": "人民广场站",
            "direction": "乘坐2号线4站",
            "node_type": "transit",
            "layer": "indoor",
            "distance": 4000,
            "transit_info": {"type": "subway", "stations": 4, "time": "10分钟"}
        },
        {
            "node_id": "exit",
            "label": "B出口（无障碍电梯）",
            "direction": "出站上行",
            "node_type": "facility",
            "layer": "indoor",
            "distance": 100,
            "facility_info": {"type": "elevator", "accessibility": "wheelchair_accessible"}
        },
        {
            "node_id": "destination",
            "label": "人民广场（目的地）",
            "direction": "到达目的地",
            "node_type": "outdoor",
            "layer": "outdoor",
            "distance": 500
        }
    ]
    
    print("\n添加多模式节点...")
    for i, node_data in enumerate(multimodal_nodes):
        node = SceneNode(
            node_id=node_data["node_id"],
            label=node_data["label"],
            image_path="data/scene_images/test.jpg",
            direction=node_data["direction"],
            timestamp=datetime.now().isoformat(),
            confidence=0.9
        )
        
        system.memory_mapper.add_node(multimodal_path_id, node)
        print(f"   ✅ 节点{i+1}: {node.label}")
    
    # 生成多模式地图
    print("\n" + "=" * 80)
    print("生成多模式增强地图...")
    print("=" * 80)
    
    multimodal_path_memory = system.memory_mapper.get_path(multimodal_path_id)
    multimodal_map_file = generator.generate_enhanced_map_card(
        multimodal_path_memory,
        "enhanced_multimodal_map.png"
    )
    
    if multimodal_map_file:
        print(f"\n✅ 多模式地图已生成: {multimodal_map_file}")
    else:
        print("\n❌ 地图生成失败")
    
    print("\n" + "=" * 80)
    print("✅ 增强地图生成测试完成")
    print("=" * 80)
    
    print("\n📊 生成总结:")
    print(f"   - 医院增强地图: {map_file or '生成失败'}")
    print(f"   - 多模式地图: {multimodal_map_file or '生成失败'}")
    
    return map_file, multimodal_map_file

if __name__ == "__main__":
    success = test_enhanced_map_generation()
    print("\n🎉 测试完成！")

