#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
学习系统测试脚本
测试各个学习引擎的功能
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

error_learning = load_module(project_root / "Luna-mid" / "core" / "error_learning.py", "error_learning")
task_optimizer_mod = load_module(project_root / "Luna-mid" / "core" / "task_optimizer.py", "task_optimizer")
user_habit_analyzer_mod = load_module(project_root / "Luna-mid" / "core" / "user_habit_analyzer.py", "user_habit_analyzer")
visual_learning_mod = load_module(project_root / "Luna-mid" / "core" / "visual_learning.py", "visual_learning")

ErrorLearningEngine = error_learning.ErrorLearningEngine
ErrorType = error_learning.ErrorType
CorrectionSource = error_learning.CorrectionSource
TaskOptimizer = task_optimizer_mod.TaskOptimizer
OptimizationSource = task_optimizer_mod.OptimizationSource
UserHabitAnalyzer = user_habit_analyzer_mod.UserHabitAnalyzer
VisualLearningEngine = visual_learning_mod.VisualLearningEngine
RecognitionSource = visual_learning_mod.RecognitionSource
ObjectCategory = visual_learning_mod.ObjectCategory

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_error_learning():
    """测试错误学习引擎"""
    print("\n" + "="*60)
    print("测试错误学习引擎")
    print("="*60)
    
    engine = ErrorLearningEngine()
    
    # 记录一个错误
    error_id = engine.record_error(
        error_type=ErrorType.NAVIGATION,
        context={"location": "test_location", "action": "turn_left"},
        user_input="向左转",
        system_response="向右转",
        expected_response="向左转"
    )
    print(f"✓ 记录错误: {error_id}")
    
    # 记录纠正
    success = engine.correct_error(
        error_id=error_id,
        correction={"solution": "应该向左转", "notes": "用户纠正"},
        correction_source=CorrectionSource.USER,
        correction_notes="用户纠正：应该向左转"
    )
    print(f"✓ 记录纠正: {success}")
    
    # 分析错误
    analysis = engine.analyze_error(error_id)
    if analysis:
        print(f"✓ 错误分析: 根本原因={analysis.root_cause[:50] if analysis.root_cause else 'N/A'}")
    
    # 获取统计（简化版）
    total_errors = len(engine.error_records)
    print(f"✓ 错误统计: 总错误数={total_errors}")
    
    return True


def test_task_optimizer():
    """测试任务优化引擎"""
    print("\n" + "="*60)
    print("测试任务优化引擎")
    print("="*60)
    
    optimizer = TaskOptimizer()
    
    # 记录任务执行
    import uuid
    task_id = f"task_{uuid.uuid4().hex[:8]}"
    execution = optimizer.record_task_execution(
        task_id=task_id,
        task_type="navigation",
        task_description="导航到A点",
        original_plan={"route": "route1", "steps": 5},
        execution_steps=[
            {"step": 1, "action": "start"},
            {"step": 2, "action": "turn_left"},
            {"step": 3, "action": "go_straight"},
            {"step": 4, "action": "turn_right"},
            {"step": 5, "action": "arrive"}
        ],
        success=True,
        execution_time=120.5,
        user_satisfaction=0.8
    )
    print(f"✓ 记录任务执行: {task_id} (执行时间: {execution.execution_time}秒)")
    
    # 优化任务
    optimization_id = optimizer.optimize_task(
        task_id=task_id,
        optimized_plan={"route": "route2", "steps": 3},
        optimization_source=OptimizationSource.USER_FEEDBACK,
        reason="用户反馈路线过长",
        improvements=["减少路径点", "优化转弯次数"],
        optimization_notes="用户反馈：路线更短"
    )
    success = optimization_id is not None
    print(f"✓ 优化任务: {success}")
    
    # 获取统计（简化版）
    total_tasks = len(optimizer.task_executions)
    total_optimizations = len(optimizer.task_optimizations)
    print(f"✓ 任务统计: 总任务数={total_tasks}, 优化记录数={total_optimizations}")
    
    return True


def test_user_habit_analyzer():
    """测试用户习惯分析引擎"""
    print("\n" + "="*60)
    print("测试用户习惯分析引擎")
    print("="*60)
    
    analyzer = UserHabitAnalyzer()
    user_id = "test_user_001"
    
    # 记录行走会话
    session_id = analyzer.record_walking_session(
        user_id=user_id,
        start_location={"name": "起点", "lat": 39.9, "lon": 116.4},
        end_location={"name": "终点", "lat": 39.91, "lon": 116.41},
        route=[
            {"lat": 39.9, "lon": 116.4},
            {"lat": 39.905, "lon": 116.405},
            {"lat": 39.91, "lon": 116.41}
        ],
        duration=600.0,  # 10分钟
        distance=1000.0,  # 1000米
        weather="sunny"
    )
    print(f"✓ 记录行走会话: {session_id}")
    
    # 获取用户画像
    profile = analyzer.get_user_profile(user_id)
    if profile:
        print(f"✓ 用户画像: 总会话数={profile.total_sessions}, 总距离={profile.total_distance:.1f}m")
    
    # 估算行走时间
    estimated_time = analyzer.estimate_walking_time(
        user_id=user_id,
        distance=2000.0  # 2000米
    )
    print(f"✓ 估算行走时间: {estimated_time:.1f}秒 ({estimated_time/60:.1f}分钟)")
    
    # 获取统计
    stats = analyzer.get_statistics(user_id)
    print(f"✓ 用户统计: {stats.get('total_sessions', 0)} 次会话")
    
    return True


def test_visual_learning():
    """测试视觉学习引擎"""
    print("\n" + "="*60)
    print("测试视觉学习引擎")
    print("="*60)
    
    engine = VisualLearningEngine()
    
    # 记录识别结果
    object_id = engine.record_recognition(
        category="building",
        name="办公楼",
        confidence=0.85,
        bbox={"x": 100, "y": 200, "width": 300, "height": 400},
        features={"color": "gray", "shape": "rectangular"},
        source="camera",
        location={"lat": 39.9, "lon": 116.4}
    )
    print(f"✓ 记录识别结果: {object_id}")
    
    # 获取知识
    knowledge = engine.get_knowledge(object_id)
    if knowledge:
        obj_knowledge = list(knowledge.values())[0]
        print(f"✓ 物体知识: {obj_knowledge.name}, 识别次数={obj_knowledge.recognition_count}")
    
    # 获取知识库中的实际ID
    knowledge = engine.get_knowledge()
    if knowledge:
        actual_id = list(knowledge.keys())[0]
        success = engine.correct_recognition(
            object_id=actual_id,
            correct_name="商业大厦",
            user_id="test_user_001"
        )
        print(f"✓ 纠正识别: {success}")
    else:
        print("✓ 纠正识别: 跳过（知识库为空）")
    
    # 获取统计
    stats = engine.get_statistics()
    print(f"✓ 视觉统计: 总物体数={stats['total_objects']}, 知识库大小={stats['total_knowledge']}")
    
    return True


def main():
    """主函数"""
    print("\n" + "="*60)
    print("开始测试学习系统")
    print("="*60)
    
    results = []
    
    try:
        # 测试错误学习
        results.append(("错误学习引擎", test_error_learning()))
    except Exception as e:
        logger.error(f"错误学习引擎测试失败: {e}", exc_info=True)
        results.append(("错误学习引擎", False))
    
    try:
        # 测试任务优化
        results.append(("任务优化引擎", test_task_optimizer()))
    except Exception as e:
        logger.error(f"任务优化引擎测试失败: {e}", exc_info=True)
        results.append(("任务优化引擎", False))
    
    try:
        # 测试用户习惯分析
        results.append(("用户习惯分析引擎", test_user_habit_analyzer()))
    except Exception as e:
        logger.error(f"用户习惯分析引擎测试失败: {e}", exc_info=True)
        results.append(("用户习惯分析引擎", False))
    
    try:
        # 测试视觉学习
        results.append(("视觉学习引擎", test_visual_learning()))
    except Exception as e:
        logger.error(f"视觉学习引擎测试失败: {e}", exc_info=True)
        results.append(("视觉学习引擎", False))
    
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

