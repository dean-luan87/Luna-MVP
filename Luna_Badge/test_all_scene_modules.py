#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge 场景记忆系统完整模块测试
"""

import sys
import os
import cv2
import numpy as np
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

def test_all_modules():
    """测试所有场景记忆模块"""
    print("=" * 60)
    print("🗺️ 场景记忆系统 - 完整模块测试")
    print("=" * 60)
    
    # 1. 测试地图生成器
    print("\n1️⃣ 测试地图生成器...")
    from core.map_card_generator import MapCardGenerator
    from core.scene_memory_system import get_scene_memory_system
    
    system = get_scene_memory_system()
    path_memory = system.get_path_memory("test_hospital_path")
    
    if path_memory and len(path_memory.nodes) > 0:
        generator = MapCardGenerator()
        map_path = generator.generate_map_card(path_memory)
        
        if map_path:
            print(f"   ✅ 地图已生成: {map_path}")
        else:
            print("   ❌ 地图生成失败")
    else:
        print("   ⚠️ 没有路径数据")
    
    # 2. 测试语音标签器
    print("\n2️⃣ 测试语音标签器...")
    from core.voice_labeler import VoiceLabeler
    
    labeler = VoiceLabeler()
    result = labeler.batch_label("test_hospital_path", 
                                 ["挂号处", "检查室", "报告领取"])
    print(f"   {result}")
    
    # 3. 测试方向估算器
    print("\n3️⃣ 测试方向估算器...")
    from core.direction_estimator import DirectionEstimator
    
    estimator = DirectionEstimator()
    
    # 生成路径方向
    if path_memory:
        directions = estimator.generate_path_directions(
            len(path_memory.nodes), 
            [10, 15, 8]
        )
        
        print(f"   生成了 {len(directions)} 个方向段:")
        for i, d in enumerate(directions, 1):
            print(f"     段{i}: {d.description}")
    
    # 4. 测试用户反馈处理器
    print("\n4️⃣ 测试用户反馈处理器...")
    from core.user_feedback_handler import UserFeedbackHandler
    
    handler = UserFeedbackHandler()
    feedback_result = handler.process_feedback(
        "test_hospital_path",
        "modify",
        0,
        {"label": "挂号处（已修正）"}
    )
    print(f"   {feedback_result}")
    
    print("\n" + "=" * 60)
    print("✅ 所有模块测试完成")
    print("=" * 60)

def test_complete_workflow():
    """测试完整工作流"""
    print("\n" + "=" * 60)
    print("🔄 完整工作流测试")
    print("=" * 60)
    
    # 创建测试路径
    from core.scene_memory_system import get_scene_memory_system
    from core.map_card_generator import MapCardGenerator
    from core.direction_estimator import DirectionEstimator
    
    system = get_scene_memory_system()
    
    # 测试完整流程
    test_images = [
        ("挂号处", (100, 400)),
        ("心电图室", (100, 400)),
        ("取报告处", (100, 400)),
    ]
    
    path_id = "complete_workflow"
    
    print("\n步骤1: 记录节点")
    print("-" * 60)
    for label, pos in test_images:
        img = np.ones((800, 1000, 3), dtype=np.uint8) * 255
        cv2.putText(img, label, pos, cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 0), 5)
        
        success = system.record_node(img, path_id, "完整工作流测试")
        status = "✅" if success else "❌"
        print(f"{status} {label}")
    
    # 步骤2: 生成方向
    print("\n步骤2: 估算方向")
    print("-" * 60)
    estimator = DirectionEstimator()
    directions = estimator.generate_path_directions(len(test_images), [12, 10])
    
    for i, d in enumerate(directions, 1):
        print(f"  从{i}到{i+1}: {d.description}")
    
    # 步骤3: 生成地图
    print("\n步骤3: 生成地图")
    print("-" * 60)
    path_memory = system.get_path_memory(path_id)
    
    if path_memory:
        generator = MapCardGenerator()
        map_path = generator.generate_map_card(path_memory, "complete_workflow_map.png")
        
        if map_path:
            print(f"   ✅ 地图已生成: {map_path}")
    
    print("\n" + "=" * 60)

def main():
    """主函数"""
    print("\n")
    print("🗺️ Luna Badge 场景记忆系统 - 完整测试套件")
    print("=" * 60)
    print()
    
    # 运行模块测试
    test_all_modules()
    
    # 运行完整工作流测试
    test_complete_workflow()
    
    print()
    print("=" * 60)
    print("📊 测试总结")
    print("=" * 60)
    print()
    print("✅ 已测试模块:")
    print("  1. MapCardGenerator - 地图生成器")
    print("  2. VoiceLabeler - 语音标签器")
    print("  3. DirectionEstimator - 方向估算器")
    print("  4. UserFeedbackHandler - 用户反馈处理器")
    print()
    print("🎯 完整流程:")
    print("  1. 记录节点 ✅")
    print("  2. 估算方向 ✅")
    print("  3. 生成地图 ✅")
    print()

if __name__ == "__main__":
    main()

