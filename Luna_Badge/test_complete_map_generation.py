#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge 完整地图生成测试
测试地图的生成、修改、新增功能，并生成可视化地图
"""

import sys
import os
import cv2
import numpy as np
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

def test_map_generation_workflow():
    """完整地图生成工作流测试"""
    print("=" * 80)
    print("🗺️  Luna Badge 完整地图生成测试")
    print("=" * 80)
    
    from core.scene_memory_system import get_scene_memory_system, SceneNode
    from datetime import datetime
    import json
    
    # 获取系统实例
    system = get_scene_memory_system()
    
    # 创建地图生成器
    from core.map_card_generator import MapCardGenerator
    map_generator = MapCardGenerator()
    
    print("\n" + "=" * 80)
    print("步骤1: 创建初始路径并生成地图")
    print("=" * 80)
    
    # 创建路径1: 医院主走廊
    path1_id = "test_map_hospital_main"
    path1_name = "医院主走廊路径"
    
    print(f"\n创建路径: {path1_name}")
    print("-" * 80)
    
    # 清空旧路径
    if path1_id in system.memory_mapper.list_paths():
        print("   清理旧路径...")
        # 实现清理逻辑如果需要
    
    # 添加路径
    system.memory_mapper.add_path(path1_id, path1_name)
    
    # 添加节点1: 医院入口
    node1 = SceneNode(
        node_id="hospital_entrance",
        label="医院主入口",
        image_path="data/scene_images/test.jpg",
        timestamp=datetime.now().isoformat(),
        direction="进入",
        confidence=0.95
    )
    system.memory_mapper.add_node(path1_id, node1)
    print("   ✅ 添加节点1: 医院主入口")
    
    # 添加节点2: 电梯
    node2 = SceneNode(
        node_id="elevator_lobby",
        label="电梯厅",
        image_path="data/scene_images/test.jpg",
        timestamp=datetime.now().isoformat(),
        direction="前行10米",
        confidence=0.92
    )
    system.memory_mapper.add_node(path1_id, node2)
    print("   ✅ 添加节点2: 电梯厅")
    
    # 添加节点3: 挂号处
    node3 = SceneNode(
        node_id="registration_desk",
        label="挂号处",
        image_path="data/scene_images/test.jpg",
        timestamp=datetime.now().isoformat(),
        direction="右转5米",
        confidence=0.88
    )
    system.memory_mapper.add_node(path1_id, node3)
    print("   ✅ 添加节点3: 挂号处")
    
    # 添加节点4: 急诊科
    node4 = SceneNode(
        node_id="emergency_room",
        label="急诊科",
        image_path="data/scene_images/test.jpg",
        timestamp=datetime.now().isoformat(),
        direction="左转8米",
        confidence=0.90
    )
    system.memory_mapper.add_node(path1_id, node4)
    print("   ✅ 添加节点4: 急诊科")
    
    # 生成路径1地图
    print("\n   生成路径1地图...")
    path_memory1 = system.memory_mapper.get_path(path1_id)
    map_card1 = map_generator.generate_map_card(path_memory1)
    if map_card1:
        print(f"   ✅ 路径1地图已生成: {map_card1}")
    
    print("\n" + "=" * 80)
    print("步骤2: 修改现有路径（添加新节点）")
    print("=" * 80)
    
    # 修改路径1，添加洗手间
    print("\n   修改路径1，添加洗手间节点")
    print("-" * 80)
    
    node5 = SceneNode(
        node_id="toilet_near_elevator",
        label="洗手间（电梯旁）",
        image_path="data/scene_images/test.jpg",
        timestamp=datetime.now().isoformat(),
        direction="电梯厅右侧2米",
        confidence=0.93
    )
    
    # 使用断点追加功能
    node_data = {
        "label": "洗手间（电梯旁）",
        "image_path": "data/scene_images/test.jpg",
        "direction": "电梯厅右侧2米",
        "confidence": 0.93
    }
    
    success = system.memory_mapper.append_node_to_path(path1_id, node_data)
    if success:
        print("   ✅ 洗手间节点已追加")
        
        # 重新生成地图
        print("   重新生成修改后的地图...")
        path_memory1 = system.memory_mapper.get_path(path1_id)
        map_card1_updated = map_generator.generate_map_card(path_memory1)
        if map_card1_updated:
            print(f"   ✅ 修改后地图已生成: {map_card1_updated}")
    
    print("\n" + "=" * 80)
    print("步骤3: 创建新路径并生成地图")
    print("=" * 80)
    
    # 创建路径2: 购物中心路线
    path2_id = "test_map_shopping_mall"
    path2_name = "购物中心导航路径"
    
    print(f"\n创建路径: {path2_name}")
    print("-" * 80)
    
    system.memory_mapper.add_path(path2_id, path2_name)
    
    # 添加购物中心节点
    mall_nodes = [
        ("mall_entrance", "购物中心入口"),
        ("information_desk", "咨询台"),
        ("escalator", "扶梯"),
        ("food_court", "美食广场"),
        ("exit_A", "A出口"),
    ]
    
    for i, (node_id, label) in enumerate(mall_nodes):
        node = SceneNode(
            node_id=node_id,
            label=label,
            image_path="data/scene_images/test.jpg",
            timestamp=datetime.now().isoformat(),
            direction=f"继续前行" if i < len(mall_nodes) - 1 else "到达目的地",
            confidence=0.85 + i * 0.02
        )
        system.memory_mapper.add_node(path2_id, node)
        print(f"   ✅ 添加节点{i+1}: {label}")
    
    # 生成路径2地图
    print("\n   生成路径2地图...")
    path_memory2 = system.memory_mapper.get_path(path2_id)
    map_card2 = map_generator.generate_map_card(path_memory2)
    if map_card2:
        print(f"   ✅ 路径2地图已生成: {map_card2}")
    
    print("\n" + "=" * 80)
    print("步骤4: 创建跨路径连接路线")
    print("=" * 80)
    
    # 创建路径3: 从医院到购物中心
    path3_id = "test_map_hospital_to_mall"
    path3_name = "医院到购物中心路线"
    
    print(f"\n创建跨路径连接: {path3_name}")
    print("-" * 80)
    
    system.memory_mapper.add_path(path3_id, path3_name)
    
    # 添加连接节点
    connection_nodes = [
        ("hospital_exit", "医院出口"),
        ("crossing_street", "过街天桥"),
        ("mall_parking", "购物中心停车场"),
        ("mall_side_entrance", "购物中心侧门"),
    ]
    
    for i, (node_id, label) in enumerate(connection_nodes):
        node = SceneNode(
            node_id=node_id,
            label=label,
            image_path="data/scene_images/test.jpg",
            timestamp=datetime.now().isoformat(),
            direction=f"继续前行{(i+1)*50}米",
            confidence=0.88
        )
        system.memory_mapper.add_node(path3_id, node)
        print(f"   ✅ 添加节点{i+1}: {label}")
    
    # 生成路径3地图
    print("\n   生成路径3地图...")
    path_memory3 = system.memory_mapper.get_path(path3_id)
    map_card3 = map_generator.generate_map_card(path_memory3)
    if map_card3:
        print(f"   ✅ 路径3地图已生成: {map_card3}")
    
    print("\n" + "=" * 80)
    print("步骤5: 生成路径统计报告")
    print("=" * 80)
    
    paths_to_check = [path1_id, path2_id, path3_id]
    
    for path_id in paths_to_check:
        stats = system.memory_mapper.get_path_statistics(path_id)
        if stats:
            print(f"\n路径: {stats['path_name']}")
            print("-" * 80)
            print(f"   路径ID: {stats['path_id']}")
            print(f"   节点总数: {stats['total_nodes']}")
            print(f"   节点类型: {stats['node_types']}")
            print(f"   创建时间: {stats['created_at']}")
            print(f"   更新时间: {stats['updated_at']}")
    
    print("\n" + "=" * 80)
    print("步骤6: 生成综合地图可视化")
    print("=" * 80)
    
    # 生成综合地图
    print("\n   生成综合路径地图...")
    combined_map = generate_combined_map(system, paths_to_check)
    
    if combined_map:
        print(f"   ✅ 综合地图已生成: {combined_map}")
    
    print("\n" + "=" * 80)
    print("✅ 地图生成测试完成")
    print("=" * 80)
    
    print("\n📊 测试总结:")
    print(f"   - 创建路径数: 3")
    print(f"   - 修改路径数: 1")
    print(f"   - 生成地图数: 4 (3个路径地图 + 1个综合地图)")
    print(f"   - 总节点数: {sum(system.memory_mapper.get_path_statistics(p).get('total_nodes', 0) for p in paths_to_check)}")
    
    return combined_map

def generate_combined_map(system, path_ids):
    """生成综合地图可视化"""
    try:
        import matplotlib
        matplotlib.use('Agg')  # 使用非交互式后端
        import matplotlib.pyplot as plt
        from matplotlib.patches import Rectangle, Circle, FancyBboxPatch, Arrow
        from matplotlib.patches import FancyArrowPatch
        
        # 配置中文字体
        import platform
        system_os = platform.system()
        if system_os == 'Darwin':  # macOS
            plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'STHeiti', 'SimHei', 'PingFang SC']
        elif system_os == 'Windows':
            plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'SimSun']
        else:  # Linux
            plt.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei', 'DejaVu Sans']
        
        plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        
        # 创建图形
        fig, ax = plt.subplots(figsize=(16, 12))
        ax.set_aspect('equal')
        
        # 设置背景
        ax.set_facecolor('#f5f5f5')
        ax.set_xlim(0, 20)
        ax.set_ylim(0, 16)
        ax.axis('off')
        
        # 定义颜色方案
        colors = {
            'hospital': '#4CAF50',
            'mall': '#2196F3',
            'connection': '#FF9800',
            'text': '#333333',
            'path': '#757575'
        }
        
        # 路径信息
        path_configs = []
        
        for i, path_id in enumerate(path_ids):
            stats = system.memory_mapper.get_path_statistics(path_id)
            if stats:
                path_memory = system.memory_mapper.get_path(path_id)
                nodes = path_memory.nodes
                
                path_configs.append({
                    'id': path_id,
                    'name': stats['path_name'],
                    'nodes': nodes,
                    'color': list(colors.values())[i]
                })
        
        # 绘制每个路径
        y_start = 14
        x_center = 10
        
        for idx, config in enumerate(path_configs):
            y_pos = y_start - idx * 5
            
            # 绘制路径标题
            ax.text(x_center, y_pos + 1.5, config['name'], 
                   fontsize=14, fontweight='bold', 
                   ha='center', va='bottom',
                   color=colors['text'],
                   bbox=dict(boxstyle='round,pad=0.5', 
                           facecolor='white', 
                           edgecolor=config['color'], 
                           linewidth=2))
            
            # 绘制节点
            num_nodes = len(config['nodes'])
            x_spacing = 18 / max(num_nodes, 1)
            x_start = x_center - (num_nodes - 1) * x_spacing / 2
            
            for i, node in enumerate(config['nodes']):
                x = x_start + i * x_spacing
                y = y_pos
                
                # 绘制节点圆圈
                circle = Circle((x, y), 0.3, 
                              color=config['color'], 
                              ec='white', linewidth=2,
                              zorder=3)
                ax.add_patch(circle)
                
                # 添加节点编号
                ax.text(x, y, str(i+1), 
                       fontsize=10, fontweight='bold',
                       ha='center', va='center',
                       color='white', zorder=4)
                
                # 添加节点标签
                label_lines = node.label.split('（') if '（' in node.label else [node.label]
                label = label_lines[0]
                
                ax.text(x, y - 0.7, label,
                       fontsize=8, ha='center', va='top',
                       color=colors['text'],
                       wrap=True,
                       bbox=dict(boxstyle='round,pad=0.3', 
                               facecolor='white', 
                               alpha=0.8,
                               edgecolor=config['color'],
                               linewidth=1))
                
                # 绘制连接线（除了最后一个节点）
                if i < num_nodes - 1:
                    arrow = FancyArrowPatch((x + 0.3, y), 
                                           (x + x_spacing - 0.3, y),
                                           arrowstyle='->', 
                                           mutation_scale=20,
                                           color=config['color'],
                                           linewidth=2,
                                           zorder=2)
                    ax.add_patch(arrow)
        
        # 添加标题
        ax.text(10, 15.5, 'Luna Badge 路径地图系统', 
               fontsize=20, fontweight='bold',
               ha='center', va='top',
               color='#1976D2')
        
        # 添加图例
        legend_elements = [
            plt.Line2D([0], [0], marker='o', color='w', 
                      markerfacecolor=colors['hospital'], 
                      markersize=12, label='医院路线'),
            plt.Line2D([0], [0], marker='o', color='w', 
                      markerfacecolor=colors['mall'], 
                      markersize=12, label='购物中心路线'),
            plt.Line2D([0], [0], marker='o', color='w', 
                      markerfacecolor=colors['connection'], 
                      markersize=12, label='连接路线')
        ]
        
        ax.legend(handles=legend_elements, loc='upper left',
                 fontsize=10, frameon=True, 
                 fancybox=True, shadow=True)
        
        # 添加说明文字
        info_text = (
            "地图说明:\n"
            "• 每个圆圈代表一个导航节点\n"
            "• 圆圈内的数字表示节点顺序\n"
            "• 箭头表示行进方向\n"
            "• 不同颜色区分不同路径"
        )
        
        ax.text(0.5, 0.5, info_text,
               fontsize=9, ha='left', va='bottom',
               color=colors['text'],
               bbox=dict(boxstyle='round,pad=0.8', 
                       facecolor='#FFF9C4', 
                       alpha=0.9,
                       edgecolor='#F57F17',
                       linewidth=2))
        
        # 保存地图
        output_file = "data/map_cards/complete_map_visualization.png"
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"   综合地图已保存: {output_file}")
        return output_file
        
    except Exception as e:
        print(f"   ⚠️ 综合地图生成失败: {e}")
        import traceback
        traceback.print_exc()
        return None

def print_map_summary():
    """打印地图文件总结"""
    print("\n" + "=" * 80)
    print("📁 生成的地图文件")
    print("=" * 80)
    
    map_dir = "data/map_cards"
    if os.path.exists(map_dir):
        map_files = [f for f in os.listdir(map_dir) if f.endswith('.png')]
        
        if map_files:
            print(f"\n共生成 {len(map_files)} 个地图文件:\n")
            for i, map_file in enumerate(sorted(map_files), 1):
                file_path = os.path.join(map_dir, map_file)
                file_size = os.path.getsize(file_path) / 1024  # KB
                print(f"   {i}. {map_file} ({file_size:.1f} KB)")
                print(f"      路径: {file_path}")
        else:
            print("\n   暂无地图文件")
    else:
        print(f"\n   地图目录不存在: {map_dir}")
    
    print("\n" + "=" * 80)

def main():
    """主函数"""
    print("\n")
    print("🚀 启动完整地图生成测试...")
    print()
    
    try:
        # 运行完整测试
        combined_map = test_map_generation_workflow()
        
        # 打印地图文件总结
        print_map_summary()
        
        # 显示最终提示
        if combined_map:
            print("\n" + "=" * 80)
            print("🎉 测试成功完成！")
            print("=" * 80)
            print(f"\n📍 综合地图位置: {combined_map}")
            print("\n💡 提示:")
            print("   - 打开 data/map_cards/ 目录查看所有生成的地图")
            print("   - 综合地图展示了所有路径的整体布局")
            print("   - 每个路径地图展示了详细的节点信息")
            print()
        
        return True
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
