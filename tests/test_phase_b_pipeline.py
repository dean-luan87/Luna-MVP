# -*- coding: utf-8 -*-
"""
v1.8.5 Phase B Pipeline 工程级测试

目标：
1. 系统是否能完整跑通
2. Pipeline 各阶段是否被正确调用
3. 输入 / 输出是否结构正确
4. 性能是否在可接受范围内（不爆炸）

测试策略：
- Layer 1: 系统冒烟测试（能不能跑）
- Layer 2: Pipeline 链路测试（每一段都跑了吗）
- Layer 3: 性能 & 观测测试（慢在哪、卡在哪）

⚠️ 不验证识别准不准、不评估模型效果、不引入新功能、不调参、不优化
"""

import time
import cv2
import numpy as np
import sys
import os
from typing import Optional, Dict, Any

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from vision_pipeline.pipeline_controller import PipelineController
from vision_pipeline.lv4_executors.navigation_executor import NavigationExecutor
from vision_pipeline.lv4_executors.modeling_executor import ModelingExecutor
from core.scene_state_builder import SceneStateBuilder
from core.world_model.common.types import WorldUpdate


def create_test_frame(width: int = 640, height: int = 480) -> np.ndarray:
    """
    创建测试帧（如果无法加载真实图片）
    
    Args:
        width: 图像宽度
        height: 图像高度
    
    Returns:
        np.ndarray: 测试图像帧
    """
    # 创建一个简单的测试图像（彩色噪声）
    frame = np.random.randint(0, 255, (height, width, 3), dtype=np.uint8)
    return frame


def load_test_frame(path: str) -> Optional[np.ndarray]:
    """
    加载测试图片
    
    Args:
        path: 图片路径
    
    Returns:
        np.ndarray: 图像帧，如果加载失败则返回 None
    """
    if not os.path.exists(path):
        return None
    frame = cv2.imread(path)
    return frame


def test_pipeline_single_frame():
    """
    Layer 1: 系统冒烟测试（能不能跑）
    
    验证：
    - PipelineController.process_frame() 是否可正常运行
    - 是否抛出异常
    - 返回结果结构是否正确
    """
    print("\n" + "=" * 70)
    print("=== Layer 1: 系统冒烟测试（能不能跑）===")
    print("=" * 70)
    
    try:
        # 初始化 PipelineController（需要传入 ModelingExecutor）
        print("\n[1/5] 初始化 PipelineController...")
        # v1.8.5 Phase B: 需要传入 ModelingExecutor，否则不会执行
        modeling_executor = ModelingExecutor()
        pipeline = PipelineController(modeling_executor=modeling_executor)
        print("  ✅ PipelineController 初始化成功（包含 ModelingExecutor）")
        
        # 初始化 SceneStateBuilder
        print("\n[2/5] 初始化 SceneStateBuilder...")
        scene_builder = SceneStateBuilder()
        print("  ✅ SceneStateBuilder 初始化成功")
        
        # 加载或创建测试帧
        print("\n[3/5] 准备测试帧...")
        test_image_paths = [
            "tests/assets/test_frame.jpg",
            "data/scene_images/test.jpg",
            "营业执照.jpg",
        ]
        frame = None
        for path in test_image_paths:
            frame = load_test_frame(path)
            if frame is not None:
                print(f"  ✅ 加载测试图片: {path}")
                break
        
        if frame is None:
            print("  ⚠️  未找到测试图片，创建随机测试帧")
            frame = create_test_frame()
            print("  ✅ 测试帧创建成功")
        
        # 执行 Pipeline 处理
        print("\n[4/5] 执行 PipelineController.process_frame()...")
        start_time = time.time()
        pipeline_result = pipeline.process_frame(
            frame=frame,
            frame_id="test_frame_001",
            task_state=None,
            context=None,
            user_position=None,
        )
        elapsed = time.time() - start_time
        print(f"  ✅ pipeline.process_frame() 完成，耗时: {elapsed:.3f}s")
        
        # 验证返回结果
        print("\n[5/5] 验证返回结果结构...")
        assert pipeline_result is not None, "❌ pipeline_result 为 None"
        print("  ✅ pipeline_result 不为 None")
        
        # 检查 quality_result
        assert "quality_result" in pipeline_result, "❌ 缺少 quality_result"
        quality_result = pipeline_result["quality_result"]
        assert hasattr(quality_result, "passed"), "❌ QualityResult 缺少 passed 字段"
        print(f"  ✅ quality_result.passed = {quality_result.passed}")
        
        # 检查 route_result
        assert "route_result" in pipeline_result, "❌ 缺少 route_result"
        route_result = pipeline_result["route_result"]
        assert hasattr(route_result, "route"), "❌ RouteResult 缺少 route 字段"
        print(f"  ✅ route_result.route = {route_result.route}")
        
        # 检查 navigation_result（如果路由到 navigation）
        navigation_result = pipeline_result.get("navigation_result")
        if navigation_result is not None:
            print("\n  检查 NavigationResult...")
            assert hasattr(navigation_result, "objects"), "❌ NavigationResult 缺少 objects 字段"
            objects = navigation_result.objects
            print(f"    ✅ NavigationResult.objects: {len(objects) if objects else 0} 个对象")
            if objects:
                print(f"      示例对象: {objects[0] if len(objects) > 0 else 'N/A'}")
        else:
            print("  ⚠️  navigation_result 为 None（可能路由到 non_navigation）")
        
        # 检查 modeling_result（应该总是存在，因为 Step 2.3 后总是执行 ModelingExecutor）
        modeling_result = pipeline_result.get("modeling_result")
        assert modeling_result is not None, "❌ modeling_result 为 None（应该总是存在）"
        print("\n  检查 ModelingResult...")
        assert hasattr(modeling_result, "content_candidates"), "❌ ModelingResult 缺少 content_candidates 字段"
        content_candidates = modeling_result.content_candidates
        print(f"    ✅ ModelingResult.content_candidates: {len(content_candidates)} 个候选")
        
        # 提取 texts（从 content_candidates 中提取 raw_text）
        texts = []
        for candidate in content_candidates:
            if hasattr(candidate, "raw_text") and candidate.raw_text:
                texts.append({
                    "text": candidate.raw_text,
                    "confidence": candidate.confidence,
                })
        print(f"    提取的 texts: {len(texts)} 个")
        
        # 提取 description（从 content_candidates 中查找 scene_description）
        description = None
        for candidate in content_candidates:
            if hasattr(candidate, "content_type") and candidate.content_type == "scene_description":
                if hasattr(candidate, "description") and candidate.description:
                    description = candidate.description
                    break
        if description:
            print(f"    场景描述: {description[:50]}...")
        else:
            print("    场景描述: 无")
        
        # 构建 WorldUpdate
        print("\n  构建 WorldUpdate...")
        objects_for_world = navigation_result.objects if navigation_result and navigation_result.objects else []
        world_update = WorldUpdate(
            update_type="content",
            structured_data={
                "objects": objects_for_world,
                "texts": texts,
            },
            confidence=1.0 if (objects_for_world or texts) else 0.0,
            source="modeling_executor",
        )
        print("    ✅ WorldUpdate 构建成功")
        print(f"      - objects: {len(world_update.structured_data['objects'])} 个")
        print(f"      - texts: {len(world_update.structured_data['texts'])} 个")
        print(f"      - confidence: {world_update.confidence}")
        
        # 构建 SceneState
        print("\n  构建 SceneState...")
        scene_state = scene_builder.build_state(
            world_update=world_update,
            risk_level=None,
        )
        assert scene_state is not None, "❌ SceneState 构建失败"
        print("    ✅ SceneState 构建成功")
        print(f"      - scene_id: {scene_state.scene_id}")
        print(f"      - objects: {len(scene_state.objects)} 个")
        print(f"      - signs: {len(scene_state.signs)} 个")
        print(f"      - risk_level: {scene_state.risk_level}")
        print(f"      - stability: {scene_state.stability}")
        
        print("\n" + "=" * 70)
        print("✅ Layer 1: 系统冒烟测试 PASSED")
        print("=" * 70)
        return True
        
    except Exception as e:
        print("\n" + "=" * 70)
        print(f"❌ Layer 1: 系统冒烟测试 FAILED")
        print(f"错误: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        print("=" * 70)
        return False


def test_pipeline_multiple_frames(n: int = 10):
    """
    Layer 3: 性能 & 观测测试（慢在哪、卡在哪）
    
    验证：
    - 连续 N 帧的执行时间
    - 是否有性能指数恶化
    - 平均耗时是否在可接受范围内
    """
    print("\n" + "=" * 70)
    print(f"=== Layer 3: 性能 & 观测测试（{n} 帧）===")
    print("=" * 70)
    
    try:
        # 初始化 PipelineController（需要传入 ModelingExecutor）
        print("\n初始化 PipelineController...")
        # v1.8.5 Phase B: 需要传入 ModelingExecutor，否则不会执行
        modeling_executor = ModelingExecutor()
        pipeline = PipelineController(modeling_executor=modeling_executor)
        
        # 加载或创建测试帧
        test_image_paths = [
            "tests/assets/test_frame.jpg",
            "data/scene_images/test.jpg",
            "营业执照.jpg",
        ]
        frame = None
        for path in test_image_paths:
            frame = load_test_frame(path)
            if frame is not None:
                break
        
        if frame is None:
            frame = create_test_frame()
        
        # 执行连续 N 帧
        print(f"\n执行连续 {n} 帧处理...")
        times = []
        for i in range(n):
            start = time.time()
            pipeline_result = pipeline.process_frame(
                frame=frame,
                frame_id=f"test_frame_{i+1:03d}",
                task_state=None,
                context=None,
                user_position=None,
            )
            cost = time.time() - start
            times.append(cost)
            
            # 检查结果
            if pipeline_result is None:
                print(f"  ⚠️  Frame {i+1}: pipeline_result 为 None")
            else:
                nav = pipeline_result.get("navigation_result")
                mod = pipeline_result.get("modeling_result")
                nav_ok = nav is not None
                mod_ok = mod is not None
                status = "✅" if (nav_ok and mod_ok) else "⚠️"
                print(f"  {status} Frame {i+1}: {cost:.3f}s (nav={nav_ok}, mod={mod_ok})")
        
        # 统计分析
        print("\n性能统计:")
        total_time = sum(times)
        avg_time = total_time / n
        min_time = min(times)
        max_time = max(times)
        
        print(f"  总耗时: {total_time:.3f}s")
        print(f"  平均耗时: {avg_time:.3f}s")
        print(f"  最小耗时: {min_time:.3f}s")
        print(f"  最大耗时: {max_time:.3f}s")
        
        # 检查性能恶化
        if len(times) >= 3:
            first_third = times[:len(times)//3]
            last_third = times[-len(times)//3:]
            first_avg = sum(first_third) / len(first_third)
            last_avg = sum(last_third) / len(last_third)
            if last_avg > first_avg * 2.0:
                print(f"  ⚠️  性能恶化检测: 前1/3平均 {first_avg:.3f}s, 后1/3平均 {last_avg:.3f}s")
                print(f"     可能存在缓存/状态泄漏")
            else:
                print(f"  ✅ 性能稳定: 前1/3平均 {first_avg:.3f}s, 后1/3平均 {last_avg:.3f}s")
        
        # 性能提示（非硬约束）
        if avg_time > 1.0:
            print(f"\n  ⚠️  警告: 平均帧处理时间 > 1s ({avg_time:.3f}s)")
            print(f"     建议检查是否有性能瓶颈")
        else:
            print(f"\n  ✅ 平均帧处理时间在可接受范围内 ({avg_time:.3f}s)")
        
        print("\n" + "=" * 70)
        print("✅ Layer 3: 性能 & 观测测试 DONE")
        print("=" * 70)
        return True
        
    except Exception as e:
        print("\n" + "=" * 70)
        print(f"❌ Layer 3: 性能 & 观测测试 FAILED")
        print(f"错误: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        print("=" * 70)
        return False


def test_pipeline_linkage():
    """
    Layer 2: Pipeline 链路测试（每一段都跑了吗）
    
    验证：
    - LV2 Quality Gate 是否被调用
    - LV3 Semantic Router 是否被调用
    - LV4.1 Navigation Executor 是否被调用（如果路由到 navigation）
    - LV4.2 Modeling Executor 是否被调用
    - WorldUpdate → SceneStateBuilder 链路是否完整
    """
    print("\n" + "=" * 70)
    print("=== Layer 2: Pipeline 链路测试（每一段都跑了吗）===")
    print("=" * 70)
    
    try:
        # 初始化 PipelineController（需要传入 ModelingExecutor）
        print("\n初始化 PipelineController...")
        # v1.8.5 Phase B: 需要传入 ModelingExecutor，否则不会执行
        modeling_executor = ModelingExecutor()
        pipeline = PipelineController(modeling_executor=modeling_executor)
        
        # 加载或创建测试帧
        test_image_paths = [
            "tests/assets/test_frame.jpg",
            "data/scene_images/test.jpg",
            "营业执照.jpg",
        ]
        frame = None
        for path in test_image_paths:
            frame = load_test_frame(path)
            if frame is not None:
                break
        
        if frame is None:
            frame = create_test_frame()
        
        # 执行 Pipeline 处理
        print("\n执行 PipelineController.process_frame()...")
        pipeline_result = pipeline.process_frame(
            frame=frame,
            frame_id="test_linkage_001",
            task_state=None,
            context=None,
            user_position=None,
        )
        
        # 验证链路完整性
        print("\n验证 Pipeline 链路完整性...")
        
        # LV2: Quality Gate
        assert "quality_result" in pipeline_result, "❌ LV2 Quality Gate 未执行"
        quality_result = pipeline_result["quality_result"]
        assert hasattr(quality_result, "passed"), "❌ QualityResult 结构不完整"
        print(f"  ✅ LV2 Quality Gate: passed={quality_result.passed}")
        
        # LV3: Semantic Router
        assert "route_result" in pipeline_result, "❌ LV3 Semantic Router 未执行"
        route_result = pipeline_result["route_result"]
        assert hasattr(route_result, "route"), "❌ RouteResult 结构不完整"
        print(f"  ✅ LV3 Semantic Router: route={route_result.route}")
        
        # LV4: Executors
        if quality_result.passed:
            # LV4.1: Navigation Executor（如果路由到 navigation）
            navigation_result = pipeline_result.get("navigation_result")
            if route_result.route == "navigation":
                assert navigation_result is not None, "❌ LV4.1 Navigation Executor 未执行（路由到 navigation）"
                print(f"  ✅ LV4.1 Navigation Executor: 已执行")
                print(f"      - objects: {len(navigation_result.objects) if navigation_result.objects else 0} 个")
            else:
                print(f"  ⚠️  LV4.1 Navigation Executor: 未执行（路由到 non_navigation）")
            
            # LV4.2: Modeling Executor（应该总是执行）
            modeling_result = pipeline_result.get("modeling_result")
            assert modeling_result is not None, "❌ LV4.2 Modeling Executor 未执行（应该总是执行）"
            print(f"  ✅ LV4.2 Modeling Executor: 已执行")
            print(f"      - content_candidates: {len(modeling_result.content_candidates)} 个")
            
            # WorldUpdate → SceneStateBuilder 链路
            print("\n验证 WorldUpdate → SceneStateBuilder 链路...")
            objects_for_world = navigation_result.objects if navigation_result and navigation_result.objects else []
            texts_for_world = []
            for candidate in modeling_result.content_candidates:
                if hasattr(candidate, "raw_text") and candidate.raw_text:
                    texts_for_world.append({
                        "text": candidate.raw_text,
                        "confidence": candidate.confidence,
                    })
            
            world_update = WorldUpdate(
                update_type="content",
                structured_data={
                    "objects": objects_for_world,
                    "texts": texts_for_world,
                },
                confidence=1.0 if (objects_for_world or texts_for_world) else 0.0,
                source="modeling_executor",
            )
            print(f"  ✅ WorldUpdate 构建成功")
            
            scene_builder = SceneStateBuilder()
            scene_state = scene_builder.build_state(
                world_update=world_update,
                risk_level=None,
            )
            assert scene_state is not None, "❌ SceneState 构建失败"
            print(f"  ✅ SceneState 构建成功")
            print(f"      - scene_id: {scene_state.scene_id}")
            print(f"      - objects: {len(scene_state.objects)} 个")
            print(f"      - signs: {len(scene_state.signs)} 个")
        else:
            print("  ⚠️  质量检查未通过，跳过 LV4 验证")
        
        print("\n" + "=" * 70)
        print("✅ Layer 2: Pipeline 链路测试 PASSED")
        print("=" * 70)
        return True
        
    except Exception as e:
        print("\n" + "=" * 70)
        print(f"❌ Layer 2: Pipeline 链路测试 FAILED")
        print(f"错误: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        print("=" * 70)
        return False


def test_degradation_paths():
    """
    测试降级路径（空 WorldUpdate 等边界情况）
    
    验证：
    - 当 pipeline_result 为 None 时的处理
    - 当 navigation_result 或 modeling_result 为空时的处理
    - 当 objects 或 texts 为空时的处理
    """
    print("\n" + "=" * 70)
    print("=== 降级路径测试 ===")
    print("=" * 70)
    
    try:
        scene_builder = SceneStateBuilder()
        
        # 测试 1: 空的 WorldUpdate（objects 和 texts 都为空）
        print("\n测试 1: 空的 WorldUpdate...")
        empty_world_update = WorldUpdate(
            update_type="content",
            structured_data={
                "objects": [],
                "texts": [],
            },
            confidence=0.0,
            source="modeling_executor",
        )
        scene_state = scene_builder.build_state(
            world_update=empty_world_update,
            risk_level=None,
        )
        assert scene_state is not None, "❌ 空 WorldUpdate 导致 SceneState 构建失败"
        assert len(scene_state.objects) == 0, "❌ 空 objects 未正确处理"
        assert len(scene_state.signs) == 0, "❌ 空 texts 未正确处理"
        print("  ✅ 空 WorldUpdate 处理成功")
        
        # 测试 2: 只有 objects 的 WorldUpdate
        print("\n测试 2: 只有 objects 的 WorldUpdate...")
        objects_only_world_update = WorldUpdate(
            update_type="content",
            structured_data={
                "objects": [{"label": "person", "confidence": 0.9}],
                "texts": [],
            },
            confidence=1.0,
            source="modeling_executor",
        )
        scene_state = scene_builder.build_state(
            world_update=objects_only_world_update,
            risk_level=None,
        )
        assert scene_state is not None, "❌ 只有 objects 的 WorldUpdate 导致 SceneState 构建失败"
        assert len(scene_state.objects) > 0, "❌ objects 未正确提取"
        print("  ✅ 只有 objects 的 WorldUpdate 处理成功")
        
        # 测试 3: 只有 texts 的 WorldUpdate
        print("\n测试 3: 只有 texts 的 WorldUpdate...")
        texts_only_world_update = WorldUpdate(
            update_type="content",
            structured_data={
                "objects": [],
                "texts": [{"text": "测试文字", "confidence": 0.8}],
            },
            confidence=1.0,
            source="modeling_executor",
        )
        scene_state = scene_builder.build_state(
            world_update=texts_only_world_update,
            risk_level=None,
        )
        assert scene_state is not None, "❌ 只有 texts 的 WorldUpdate 导致 SceneState 构建失败"
        assert len(scene_state.signs) > 0, "❌ texts 未正确提取"
        print("  ✅ 只有 texts 的 WorldUpdate 处理成功")
        
        print("\n" + "=" * 70)
        print("✅ 降级路径测试 PASSED")
        print("=" * 70)
        return True
        
    except Exception as e:
        print("\n" + "=" * 70)
        print(f"❌ 降级路径测试 FAILED")
        print(f"错误: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        print("=" * 70)
        return False


def main():
    """
    主测试函数
    """
    print("\n" + "=" * 70)
    print("v1.8.5 Phase B Pipeline 工程级测试")
    print("=" * 70)
    print("\n测试目标:")
    print("  1. 系统是否能完整跑通")
    print("  2. Pipeline 各阶段是否被正确调用")
    print("  3. 输入 / 输出是否结构正确")
    print("  4. 性能是否在可接受范围内（不爆炸）")
    print("\n⚠️  不验证识别准不准、不评估模型效果、不引入新功能、不调参、不优化")
    
    results = []
    
    # Layer 1: 系统冒烟测试
    results.append(("Layer 1: 系统冒烟测试", test_pipeline_single_frame()))
    
    # Layer 2: Pipeline 链路测试
    results.append(("Layer 2: Pipeline 链路测试", test_pipeline_linkage()))
    
    # Layer 3: 性能 & 观测测试
    results.append(("Layer 3: 性能 & 观测测试", test_pipeline_multiple_frames(n=10)))
    
    # 降级路径测试
    results.append(("降级路径测试", test_degradation_paths()))
    
    # 汇总结果
    print("\n" + "=" * 70)
    print("测试结果汇总")
    print("=" * 70)
    for name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"  {status}: {name}")
    
    all_passed = all(result[1] for result in results)
    print("\n" + "=" * 70)
    if all_passed:
        print("✅ 所有测试 PASSED")
        print("=" * 70)
        return 0
    else:
        print("❌ 部分测试 FAILED")
        print("=" * 70)
        return 1


if __name__ == "__main__":
    exit(main())

