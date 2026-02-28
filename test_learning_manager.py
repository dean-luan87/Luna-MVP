#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
学习系统管理器测试脚本
测试统一管理器的功能
"""

import sys
import logging
import importlib.util
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 动态导入模块（因为目录名包含连字符）
def load_module(module_path, module_name):
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

learning_manager_mod = load_module(project_root / "Luna-mid" / "core" / "learning_manager.py", "learning_manager")
LearningSystemManager = learning_manager_mod.LearningSystemManager

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_unified_interface():
    """测试统一接口"""
    print("\n" + "="*60)
    print("测试学习系统统一管理器")
    print("="*60)
    
    manager = LearningSystemManager()
    
    # 测试错误学习接口
    print("\n--- 测试错误学习接口 ---")
    error_id = manager.record_error(
        error_type="navigation",
        context={"test": "unified_test"},
        user_input="测试输入",
        system_response="错误响应",
        expected_response="正确响应"
    )
    print(f"✓ 记录错误: {error_id}")
    
    manager.record_correction(
        error_id=error_id,
        correction_source="user",
        correction="用户纠正"
    )
    print(f"✓ 记录纠正")
    
    # 测试任务优化接口
    print("\n--- 测试任务优化接口 ---")
    task_id = manager.record_task_execution(
        task_type="navigation",
        task_description="测试导航任务",
        original_plan={"route": "test_route"},
        execution_steps=[{"step": 1}],
        success=True,
        execution_time=100.0,
        user_satisfaction=0.9
    )
    print(f"✓ 记录任务执行: {task_id}")
    
    manager.optimize_task(
        task_id=task_id,
        optimized_plan={"route": "optimized_route"},
        optimization_source="user_feedback",
        optimization_notes="优化说明"
    )
    print(f"✓ 优化任务")
    
    # 测试用户习惯分析接口
    print("\n--- 测试用户习惯分析接口 ---")
    user_id = "test_user_unified"
    session_id = manager.record_walking_session(
        user_id=user_id,
        start_location={"name": "起点"},
        end_location={"name": "终点"},
        route=[],
        duration=300.0,
        distance=500.0
    )
    print(f"✓ 记录行走会话: {session_id}")
    
    profile = manager.get_user_profile(user_id)
    if profile:
        print(f"✓ 获取用户画像: {profile.get('total_sessions', 0)} 次会话")
    
    estimated_time = manager.estimate_walking_time(user_id, 1000.0)
    print(f"✓ 估算行走时间: {estimated_time:.1f}秒")
    
    # 测试视觉学习接口
    print("\n--- 测试视觉学习接口 ---")
    object_id = manager.record_visual_recognition(
        category="building",
        name="测试建筑",
        confidence=0.9,
        bbox={"x": 0, "y": 0, "width": 100, "height": 100},
        features={"test": True}
    )
    print(f"✓ 记录视觉识别: {object_id}")
    
    knowledge = manager.get_visual_knowledge()
    print(f"✓ 获取视觉知识库: {len(knowledge)} 条知识")
    
    # 测试统一统计接口
    print("\n--- 测试统一统计接口 ---")
    all_stats = manager.get_all_statistics()
    print(f"✓ 获取所有统计信息:")
    print(f"  - 错误学习: {all_stats['error_learning'].get('total_errors', 0)} 个错误")
    print(f"  - 任务优化: {all_stats['task_optimization'].get('total_tasks', 0)} 个任务")
    print(f"  - 视觉学习: {all_stats['visual_learning'].get('total_knowledge', 0)} 条知识")
    
    return True


def test_data_export():
    """测试数据导出"""
    print("\n" + "="*60)
    print("测试数据导出功能")
    print("="*60)
    
    manager = LearningSystemManager()
    
    # 导出所有数据
    output_dir = Path(__file__).parent / "test_exports"
    success = manager.export_all_data(output_dir)
    
    if success:
        print(f"✓ 数据导出成功: {output_dir}")
        # 检查导出文件
        files = list(output_dir.glob("*.json"))
        print(f"✓ 导出文件数: {len(files)}")
        for f in files:
            print(f"  - {f.name}")
    else:
        print("✗ 数据导出失败")
    
    return success


def test_backend_sync():
    """测试后台同步"""
    print("\n" + "="*60)
    print("测试后台同步功能")
    print("="*60)
    
    manager = LearningSystemManager()
    
    # 准备同步数据
    sync_data = manager.prepare_backend_sync()
    print(f"✓ 准备同步数据:")
    print(f"  - 错误记录: {len(sync_data.get('error_learning', []))} 条")
    print(f"  - 任务记录: {len(sync_data.get('task_optimization', []))} 条")
    print(f"  - 视觉记录: {len(sync_data.get('visual_learning', []))} 条")
    
    # 测试从后台同步（模拟数据）
    backend_data = {
        "error_learning": [
            {
                "error_type": "navigation",
                "context": {"test": "sync"},
                "user_input": "同步测试"
            }
        ]
    }
    
    success = manager.sync_from_backend(backend_data)
    if success:
        print(f"✓ 从后台同步数据成功")
    else:
        print(f"✗ 从后台同步数据失败")
    
    return success


def main():
    """主函数"""
    print("\n" + "="*60)
    print("开始测试学习系统管理器")
    print("="*60)
    
    results = []
    
    try:
        # 测试统一接口
        results.append(("统一接口测试", test_unified_interface()))
    except Exception as e:
        logger.error(f"统一接口测试失败: {e}", exc_info=True)
        results.append(("统一接口测试", False))
    
    try:
        # 测试数据导出
        results.append(("数据导出测试", test_data_export()))
    except Exception as e:
        logger.error(f"数据导出测试失败: {e}", exc_info=True)
        results.append(("数据导出测试", False))
    
    try:
        # 测试后台同步
        results.append(("后台同步测试", test_backend_sync()))
    except Exception as e:
        logger.error(f"后台同步测试失败: {e}", exc_info=True)
        results.append(("后台同步测试", False))
    
    # 输出测试结果
    print("\n" + "="*60)
    print("测试结果汇总")
    print("="*60)
    
    for name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{name}: {status}")
    
    total = len(results)
    passed = sum(1 for _, r in results if r)
    
    print(f"\n总计: {passed}/{total} 通过")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

