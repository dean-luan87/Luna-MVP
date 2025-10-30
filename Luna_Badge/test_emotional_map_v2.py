#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
情绪地图 v2.0 测试脚本
测试全面升级后的情绪地图生成功能
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

from core.emotional_map_card_generator_v2 import EmotionalMapCardGeneratorV2

def main():
    print("=" * 70)
    print("🎨 情绪地图 v2.0 测试")
    print("=" * 70)
    
    # 创建测试数据
    test_data = {
        "paths": [
            {
                "path_id": "test_v2_path",
                "path_name": "医院主路径",
                "nodes": [
                    {"node_id": "node1", "label": "医院入口", "type": "entrance", 
                     "level": "入口区", "emotion": ["嘈杂", "拥挤"]},
                    {"node_id": "node2", "label": "挂号大厅", "type": "building", 
                     "level": "挂号大厅", "emotion": ["宽敞", "明亮"]},
                    {"node_id": "node3", "label": "一楼西侧电梯", "type": "elevator", 
                     "level": "电梯间", "emotion": ["等待"]},
                    {"node_id": "node4", "label": "三楼候诊区", "type": "building", 
                     "level": "医院三楼", "emotion": ["拥挤"]},
                    {"node_id": "node5", "label": "卫生间", "type": "toilet", 
                     "level": "医院三楼", "emotion": ["安静", "整洁"]},
                    {"node_id": "node6", "label": "目的地", "type": "destination", 
                     "level": "医院三楼", "emotion": ["温馨"]},
                ]
            }
        ]
    }
    
    # 保存测试数据
    test_file = "data/test_memory_v2.json"
    with open(test_file, 'w', encoding='utf-8') as f:
        json.dump(test_data, f, ensure_ascii=False, indent=2)
    
    logger.info(f"✅ 创建测试数据: {test_file}")
    
    # 生成地图
    print("\n" + "=" * 70)
    print("🗺️ 生成情绪地图 v2.0")
    print("=" * 70)
    
    generator = EmotionalMapCardGeneratorV2(memory_store_path=test_file)
    result = generator.generate_emotional_map("test_v2_path")
    
    if result:
        print(f"\n✅ 情绪地图 v2.0 生成成功: {result}")
        print("\n特性:")
        print("  ✅ 中文字体支持")
        print("  ✅ SVG图标加载")
        print("  ✅ 手绘虚线路径")
        print("  ✅ 方向箭头指示")
        print("  ✅ 情绪标签emoji")
        print("  ✅ 纸张纹理背景")
    else:
        print("\n❌ 情绪地图 v2.0 生成失败")
    
    print("\n" + "=" * 70)
    print("测试完成")
    print("=" * 70)

if __name__ == "__main__":
    main()

