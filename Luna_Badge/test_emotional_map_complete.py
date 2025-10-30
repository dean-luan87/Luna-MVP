#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
情绪地图完整流程测试
测试情绪地图系统的所有模块
"""

import sys
import json
import logging
from pathlib import Path

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# 添加core到路径
sys.path.insert(0, str(Path(__file__).parent))

from core.emotional_tagger import EmotionalTagger
from core.node_layer_manager import NodeLayerManager
from core.adjacency_graph_builder import AdjacencyGraphBuilder
from core.emotional_map_card_generator import EmotionalMapCardGenerator

def create_test_data():
    """创建测试数据"""
    test_data = {
        "paths": [
            {
                "path_id": "test_emotional_path",
                "path_name": "测试情绪路径",
                "nodes": [
                    {
                        "node_id": "node1", 
                        "label": "医院入口", 
                        "type": "entrance",
                        "note": "人很多很拥挤，入口处有点嘈杂"
                    },
                    {
                        "node_id": "node2", 
                        "label": "一楼大厅", 
                        "type": "building",
                        "note": "宽敞明亮推荐使用，环境温馨"
                    },
                    {
                        "node_id": "node3", 
                        "label": "一楼东侧卫生间", 
                        "type": "toilet",
                        "note": "很安静干净整洁，推荐"
                    },
                    {
                        "node_id": "node4", 
                        "label": "电梯间", 
                        "type": "elevator",
                        "note": "需要等待一段时间"
                    },
                    {
                        "node_id": "node5", 
                        "label": "三楼候诊区", 
                        "type": "building",
                        "note": "空间较狭窄，有点拥挤"
                    },
                    {
                        "node_id": "node6", 
                        "label": "目的地", 
                        "type": "destination",
                        "note": "温馨舒适的诊室"
                    },
                ]
            }
        ]
    }
    
    # 保存测试数据
    test_file = "data/test_memory_emotional.json"
    with open(test_file, 'w', encoding='utf-8') as f:
        json.dump(test_data, f, ensure_ascii=False, indent=2)
    
    logger.info(f"✅ 创建测试数据: {test_file}")
    return test_file

def main():
    print("=" * 70)
    print("🎨 情绪地图完整流程测试")
    print("=" * 70)
    
    # 创建测试数据
    test_file = create_test_data()
    
    try:
        # 步骤1: 分配层级
        print("\n" + "=" * 70)
        print("1️⃣ 节点层级分配")
        print("=" * 70)
        manager = NodeLayerManager()
        stats = manager.update_all_levels(test_file)
        print(f"\n✅ 层级分配完成: {stats}")
        
        # 步骤2: 构建邻接图
        print("\n" + "=" * 70)
        print("2️⃣ 构建邻接图")
        print("=" * 70)
        builder = AdjacencyGraphBuilder()
        stats = builder.build_adjacency_graph(test_file)
        print(f"\n✅ 邻接图构建完成: {stats}")
        
        # 步骤3: 标注情绪
        print("\n" + "=" * 70)
        print("3️⃣ 情绪标签标注")
        print("=" * 70)
        tagger = EmotionalTagger()
        stats = tagger.tag_nodes_with_emotion(test_file)
        print(f"\n✅ 情绪标注完成: {stats}")
        
        # 步骤4: 生成情绪地图
        print("\n" + "=" * 70)
        print("4️⃣ 生成情绪地图")
        print("=" * 70)
        generator = EmotionalMapCardGenerator(memory_store_path=test_file)
        result = generator.generate_emotional_map("test_emotional_path")
        
        if result:
            print(f"\n✅ 情绪地图生成成功: {result}")
        else:
            print("\n❌ 情绪地图生成失败")
        
        # 显示最终数据
        print("\n" + "=" * 70)
        print("📊 最终数据预览")
        print("=" * 70)
        with open(test_file, 'r', encoding='utf-8') as f:
            final_data = json.load(f)
        
        for path in final_data["paths"]:
            print(f"\n路径: {path.get('path_name')}")
            for i, node in enumerate(path.get("nodes", [])):
                level = node.get("level", "未分类")
                emotion = node.get("emotion", [])
                adjacent = node.get("adjacent", [])
                
                print(f"\n  节点 {i+1}: {node.get('label')}")
                print(f"    层级: {level}")
                print(f"    情绪: {emotion}")
                print(f"    相邻: {adjacent}")
        
        print("\n" + "=" * 70)
        print("🎉 测试完成！")
        print("=" * 70)
        
    except Exception as e:
        logger.error(f"测试失败: {e}")
        import traceback
        traceback.print_exc()
        print("\n" + "=" * 70)
        print("❌ 测试失败")
        print("=" * 70)

if __name__ == "__main__":
    main()

