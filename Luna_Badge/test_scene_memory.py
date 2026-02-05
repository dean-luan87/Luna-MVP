#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge 场景记忆系统测试
"""

import sys
import os
import cv2
import numpy as np
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

def test_scene_memory_system():
    """测试场景记忆系统"""
    print("=" * 60)
    print("🗺️ 场景记忆系统测试")
    print("=" * 60)
    
    try:
        from core.scene_memory_system import get_scene_memory_system
        
        # 初始化系统
        print("\n1. 初始化系统...")
        system = get_scene_memory_system()
        print("   ✅ 系统初始化成功")
        
        # 创建测试图像
        print("\n2. 创建测试图像...")
        test_images = []
        
        # 图像1: 门牌 (使用英文)
        img1 = np.ones((800, 1000, 3), dtype=np.uint8) * 255
        cv2.putText(img1, "Room 305", (100, 400), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 0), 5)
        test_images.append(("Room 305", img1))
        
        # 图像2: 电梯
        img2 = np.ones((800, 1000, 3), dtype=np.uint8) * 255
        cv2.putText(img2, "Elevator", (100, 400), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 0), 5)
        test_images.append(("Elevator", img2))
        
        # 图像3: 出口
        img3 = np.ones((800, 1000, 3), dtype=np.uint8) * 255
        cv2.putText(img3, "Exit", (100, 400), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 0), 5)
        test_images.append(("Exit", img3))
        
        print(f"   创建了 {len(test_images)} 个测试图像")
        
        # 记录节点
        print("\n3. 记录节点...")
        path_id = "test_hospital_path"
        path_name = "医院导航路径"
        
        success_count = 0
        for label, img in test_images:
            success = system.record_node(img, path_id, path_name)
            if success:
                success_count += 1
                print(f"   ✅ 记录: {label}")
            else:
                print(f"   ❌ 失败: {label}")
        
        print(f"\n   成功记录: {success_count}/{len(test_images)} 个节点")
        
        # 获取路径记忆
        print("\n4. 获取路径记忆...")
        path_memory = system.get_path_memory(path_id)
        
        if path_memory:
            print(f"   路径名称: {path_memory.path_name}")
            print(f"   节点数量: {len(path_memory.nodes)}")
            print("\n   节点列表:")
            for i, node in enumerate(path_memory.nodes, 1):
                print(f"   {i}. {node.label}")
                print(f"      ID: {node.node_id}")
                print(f"      置信度: {node.confidence:.2f}")
                print(f"      时间: {node.timestamp}")
        
        # 列出所有路径
        print("\n5. 列出所有路径...")
        all_paths = system.memory_mapper.list_paths()
        print(f"   共有 {len(all_paths)} 条路径:")
        for pid in all_paths:
            pm = system.memory_mapper.get_path(pid)
            print(f"   - {pid}: {pm.path_name} ({len(pm.nodes)}个节点)")
        
        print("\n" + "=" * 60)
        print("✅ 测试完成")
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

def main():
    """主函数"""
    print("\n")
    print("🗺️ Luna Badge 场景记忆系统测试")
    print("=" * 60)
    print()
    
    test_scene_memory_system()
    
    print()
    print("=" * 60)

if __name__ == "__main__":
    main()
