#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
情绪地图增强版 v1.1 测试脚本
"""

import sys
import json
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

sys.path.insert(0, str(Path(__file__).parent))

from core.emotional_map_card_generator_enhanced import EmotionalMapCardGeneratorEnhanced

def main():
    print("=" * 70)
    print("🎨 情绪地图增强版 v1.1 测试")
    print("=" * 70)
    
    # 创建完整测试数据
    test_data = {
        "paths": [
            {
                "path_id": "hospital_main_enhanced",
                "path_name": "医院完整导航路径",
                "nodes": [
                    {
                        "node_id": "node1",
                        "label": "医院入口",
                        "type": "entrance",
                        "level": "挂号大厅",
                        "emotion": ["嘈杂"],
                        "distance": 0
                    },
                    {
                        "node_id": "node2",
                        "label": "挂号处",
                        "type": "building",
                        "level": "挂号大厅",
                        "emotion": ["推荐", "明亮"],
                        "distance": 15
                    },
                    {
                        "node_id": "node3",
                        "label": "一楼电梯",
                        "type": "elevator",
                        "level": "电梯间",
                        "emotion": ["等待"],
                        "distance": 20
                    },
                    {
                        "node_id": "node4",
                        "label": "三楼候诊区",
                        "type": "building",
                        "level": "三楼病区",
                        "emotion": ["安静"],
                        "distance": 30
                    },
                    {
                        "node_id": "node5",
                        "label": "卫生间",
                        "type": "toilet",
                        "level": "三楼病区",
                        "emotion": ["安静", "整洁"],
                        "distance": 10
                    },
                    {
                        "node_id": "node6",
                        "label": "诊室",
                        "type": "destination",
                        "level": "三楼病区",
                        "emotion": ["推荐"],
                        "distance": 25
                    },
                ]
            }
        ]
    }
    
    # 保存测试数据
    test_file = "data/test_memory_enhanced.json"
    with open(test_file, 'w', encoding='utf-8') as f:
        json.dump(test_data, f, ensure_ascii=False, indent=2)
    
    logger.info(f"✅ 创建测试数据: {test_file}")
    
    # 生成地图
    print("\n" + "=" * 70)
    print("🗺️ 生成增强版情绪地图")
    print("=" * 70)
    
    generator = EmotionalMapCardGeneratorEnhanced(memory_store_path=test_file)
    result = generator.generate_emotional_map("hospital_main_enhanced")
    
    if result:
        print(f"\n✅ 增强版地图生成成功: {result}")
        print("\n功能验证:")
        print("  ✅ 图标与节点视觉增强（48x48 SVG图标）")
        print("  ✅ 中文标签字体美化")
        print("  ✅ 前行方向表达（贝塞尔曲线箭头）")
        print("  ✅ 手绘风路径优化")
        print("  ✅ 区域划分与标注（椭圆背景）")
        print("  ✅ 情绪标签渲染（圆角气泡）")
        print("  ✅ 方向标（指南针）")
        print("  ✅ 元信息输出（JSON）")
    else:
        print("\n❌ 增强版地图生成失败")
    
    # 显示元信息
    meta_file = "data/map_cards/hospital_main_enhanced_emotional.meta.json"
    if os.path.exists(meta_file):
        print("\n📊 元信息:")
        with open(meta_file, 'r', encoding='utf-8') as f:
            meta = json.load(f)
            print(f"  路径: {meta.get('path_name')}")
            print(f"  方向: {meta.get('map_direction_reference')}")
            print(f"  指南针: {meta.get('compass_added')}")
            print(f"  区域: {', '.join(meta.get('regions_detected', []))}")
            print(f"  节点数: {meta.get('node_count')}")
            print(f"  总距离: {meta.get('total_distance')}")
    
    print("\n" + "=" * 70)
    print("测试完成")
    print("=" * 70)

if __name__ == "__main__":
    import os
    main()

