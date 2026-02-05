#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge v1.6 完整系统集成测试
测试所有新增路径规划模块与现有系统的集成
"""

import sys
import os
import logging
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

def test_import_all_modules():
    """测试1: 导入所有新增模块"""
    print("=" * 80)
    print("测试1: 导入所有新增模块")
    print("=" * 80)
    
    modules = [
        "core.path_resolver",
        "core.path_growth",
        "core.scene_memory_system",
        "core.config",
        "core.system_control",
        "core.startup_manager"
    ]
    
    results = []
    for module_name in modules:
        try:
            __import__(module_name)
            print(f"   ✅ {module_name}")
            results.append(True)
        except ImportError as e:
            print(f"   ❌ {module_name}: {e}")
            results.append(False)
    
    return all(results)

def test_path_resolver_integration():
    """测试2: PathResolver与场景记忆系统集成"""
    print("\n" + "=" * 80)
    print("测试2: PathResolver集成测试")
    print("=" * 80)
    
    try:
        from core.path_resolver import PathResolver
        from core.scene_memory_system import get_scene_memory_system
        
        resolver = PathResolver()
        system = get_scene_memory_system()
        
        # 测试节点查找
        print("\n1. 测试节点查找:")
        test_nodes = ["挂号处（已修正）", "Exit"]
        for node in test_nodes:
            path_id = resolver.find_path_for_node(node)
            print(f"   节点 '{node}': {path_id or '未找到'}")
        
        # 测试路径判断
        print("\n2. 测试路径创建判断:")
        decision = resolver.should_create_new_path("挂号处（已修正）", "Exit")
        print(f"   应该创建新路径: {decision['should_create']}")
        print(f"   原因: {decision['reason']}")
        
        # 测试连续性检查
        print("\n3. 测试路径连续性:")
        continuity = resolver.get_path_continuity("test_hospital_path", "挂号处（已修正）")
        print(f"   连续性: {continuity.get('continuous', False)}")
        
        print("\n   ✅ PathResolver集成测试通过")
        return True
        
    except Exception as e:
        print(f"\n   ❌ PathResolver集成测试失败: {e}")
        logger.exception(e)
        return False

def test_path_growth_integration():
    """测试3: PathGrowthManager集成测试"""
    print("\n" + "=" * 80)
    print("测试3: PathGrowthManager集成测试")
    print("=" * 80)
    
    try:
        from core.path_growth import PathGrowthManager
        from core.scene_memory_system import SceneNode
        from datetime import datetime
        
        manager = PathGrowthManager(distance_threshold=50.0)
        
        # 创建测试节点
        test_node = SceneNode(
            node_id="integration_test_node",
            label="集成测试节点",
            image_path="data/scene_images/test.jpg",
            timestamp=datetime.now().isoformat()
        )
        
        # 测试扩展判断
        print("\n1. 测试路径扩展判断:")
        decision = manager.should_extend_path("test_hospital_path", test_node)
        print(f"   应该扩展: {decision['should_extend']}")
        print(f"   原因: {decision['reason']}")
        print(f"   指标: 距离={decision['metrics'].get('distance', 0):.1f}m, "
              f"相似度={decision['metrics'].get('visual_similarity', 0):.2f}")
        
        # 测试中断处理
        print("\n2. 测试路径中断处理:")
        result = manager.handle_path_interruption("test_hospital_path", test_node)
        print(f"   动作: {result['action']}")
        print(f"   消息: {result['message']}")
        
        print("\n   ✅ PathGrowthManager集成测试通过")
        return True
        
    except Exception as e:
        print(f"\n   ❌ PathGrowthManager集成测试失败: {e}")
        logger.exception(e)
        return False

def test_memory_mapper_enhancement():
    """测试4: MemoryMapper增强功能"""
    print("\n" + "=" * 80)
    print("测试4: MemoryMapper增强功能测试")
    print("=" * 80)
    
    try:
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
            "label": "集成测试附加节点",
            "image_path": "data/scene_images/test.jpg",
            "confidence": 0.95
        }
        
        success = system.memory_mapper.append_node_to_path("test_hospital_path", node_data)
        print(f"   追加结果: {'成功' if success else '失败'}")
        
        # 显示更新后的统计
        stats = system.memory_mapper.get_path_statistics("test_hospital_path")
        print(f"   更新后节点数: {stats['total_nodes']}")
        
        print("\n   ✅ MemoryMapper增强测试通过")
        return True
        
    except Exception as e:
        print(f"\n   ❌ MemoryMapper增强测试失败: {e}")
        logger.exception(e)
        return False

def test_complete_path_planning_workflow():
    """测试5: 完整路径规划工作流"""
    print("\n" + "=" * 80)
    print("测试5: 完整路径规划工作流")
    print("=" * 80)
    
    try:
        from core.path_resolver import PathResolver
        from core.path_growth import PathGrowthManager
        from core.scene_memory_system import get_scene_memory_system, SceneNode
        from datetime import datetime
        
        resolver = PathResolver()
        manager = PathGrowthManager()
        system = get_scene_memory_system()
        
        print("\n场景: 从A点到C点的导航规划")
        print("-" * 80)
        
        # 模拟场景
        current_location = "挂号处（已修正）"
        target_location = "NewDestination"
        
        print(f"\n当前位置: {current_location}")
        print(f"目标位置: {target_location}")
        
        # 步骤1: 路径解析
        print("\n步骤1: 路径解析")
        decision = resolver.should_create_new_path(current_location, target_location)
        print(f"   决策: {'需要创建新路径' if decision['should_create'] else '使用现有路径'}")
        print(f"   原因: {decision['reason']}")
        
        # 步骤2: 路径增长判断
        if decision['should_create']:
            print("\n步骤2: 路径增长判断")
            test_node = SceneNode(
                node_id="workflow_test_node",
                label=target_location,
                image_path="data/scene_images/workflow.jpg",
                timestamp=datetime.now().isoformat()
            )
            
            growth_decision = manager.should_extend_path("test_hospital_path", test_node)
            print(f"   扩展判断: {'适合扩展' if growth_decision['should_extend'] else '不适合扩展'}")
            
            # 步骤3: 执行决策
            print("\n步骤3: 执行路径决策")
            if growth_decision['should_extend']:
                success = manager.extend_existing_path("test_hospital_path", test_node)
                print(f"   结果: {'扩展成功' if success else '扩展失败'}")
            else:
                new_path_id = manager.create_new_path(test_node, "工作流测试路径")
                print(f"   结果: 新路径已创建 ({new_path_id})")
        
        print("\n   ✅ 完整工作流测试通过")
        return True
        
    except Exception as e:
        print(f"\n   ❌ 完整工作流测试失败: {e}")
        logger.exception(e)
        return False

def test_system_health():
    """测试6: 系统健康检查"""
    print("\n" + "=" * 80)
    print("测试6: 系统健康检查")
    print("=" * 80)
    
    try:
        from core.scene_memory_system import get_scene_memory_system
        
        system = get_scene_memory_system()
        
        # 检查路径数量
        paths = system.memory_mapper.list_paths()
        print(f"\n📊 系统统计:")
        print(f"   路径数量: {len(paths)}")
        
        # 检查每个路径的状态
        print(f"\n路径详情:")
        for path_id in paths:
            stats = system.memory_mapper.get_path_statistics(path_id)
            print(f"   - {stats['path_name']}: {stats['total_nodes']} 个节点")
        
        # 检查图像文件
        import os
        image_dir = "data/scene_images"
        if os.path.exists(image_dir):
            images = [f for f in os.listdir(image_dir) if f.endswith('.jpg')]
            print(f"\n图像文件: {len(images)} 个")
        
        print("\n   ✅ 系统健康检查通过")
        return True
        
    except Exception as e:
        print(f"\n   ❌ 系统健康检查失败: {e}")
        logger.exception(e)
        return False

def main():
    """主函数"""
    print("\n")
    print("🚀 Luna Badge v1.6 完整系统集成测试")
    print("=" * 80)
    print()
    
    test_results = []
    
    # 运行所有测试
    test_results.append(("模块导入", test_import_all_modules()))
    test_results.append(("PathResolver集成", test_path_resolver_integration()))
    test_results.append(("PathGrowthManager集成", test_path_growth_integration()))
    test_results.append(("MemoryMapper增强", test_memory_mapper_enhancement()))
    test_results.append(("完整工作流", test_complete_path_planning_workflow()))
    test_results.append(("系统健康", test_system_health()))
    
    # 输出测试总结
    print("\n" + "=" * 80)
    print("📊 测试总结")
    print("=" * 80)
    
    passed = sum(1 for _, result in test_results if result)
    total = len(test_results)
    
    for name, result in test_results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {status}: {name}")
    
    print(f"\n总计: {passed}/{total} 测试通过")
    
    if passed == total:
        print("\n🎉 所有测试通过！系统集成成功！")
    else:
        print(f"\n⚠️  有 {total - passed} 个测试未通过")
    
    print("=" * 80)
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

