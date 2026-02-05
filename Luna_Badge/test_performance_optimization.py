#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
性能优化测试脚本
快速验证各种优化措施的效果
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import time
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)

def test_step_detector_optimization():
    """测试台阶检测器优化"""
    print("\n" + "=" * 70)
    print("🧪 测试1: StepDetector性能优化")
    print("=" * 70)
    
    from core.step_detector import StepDetector
    
    # 创建检测器
    detector = StepDetector(use_cache=True, cache_ttl=3.0)
    
    # 创建测试图像
    test_frame = np.random.randint(0, 255, (640, 480, 3), dtype=np.uint8)
    
    # 第一次检测（应该会实际推理）
    start = time.time()
    result1 = detector.detect_step(test_frame)
    time1 = (time.time() - start) * 1000
    
    # 第二次检测（应该从缓存获取）
    start = time.time()
    result2 = detector.detect_step(test_frame)
    time2 = (time.time() - start) * 1000
    
    print(f"\n  首次检测耗时: {time1:.2f}ms")
    print(f"  缓存命中耗时: {time2:.2f}ms")
    
    if time2 < time1:
        speedup = time1 / time2 if time2 > 0 else 999
        print(f"  ✅ 缓存加速: {speedup:.1f}x")
    else:
        print(f"  ⚠️ 缓存效果不明显")
    
    print(f"  缓存大小: {len(detector.cache)}")

def test_navigation_optimizer():
    """测试导航优化器"""
    print("\n" + "=" * 70)
    print("🧪 测试2: NavigationOptimizer性能优化")
    print("=" * 70)
    
    from core.navigation_optimizer import NavigationOptimizer
    
    optimizer = NavigationOptimizer(max_cache_size=50)
    
    print(f"\n  常用路径预计算: {len(optimizer.common_paths)}个")
    
    # 模拟路径缓存
    class MockPath:
        def __init__(self, name):
            self.name = name
    
    # 缓存几条路径
    for i in range(20):
        optimizer.cache_path("start", f"dest_{i}", MockPath(f"path_{i}"))
    
    # 获取缓存统计
    stats = optimizer.get_stats()
    print(f"  缓存大小: {stats['cache_size']}/50")
    print(f"  命中率: {stats['hit_rate']}%")
    print(f"  平均响应时间: {stats['avg_response_time_ms']}ms")

def test_vision_pipeline_cache():
    """测试视觉管道缓存"""
    print("\n" + "=" * 70)
    print("🧪 测试3: VisionPipeline缓存优化")
    print("=" * 70)
    
    from core.vision_pipeline import VisionPipeline
    
    # 创建管道（启用缓存）
    pipeline = VisionPipeline(target_fps=10.0, enable_preprocess_cache=True)
    
    # 测试缓存功能
    test_frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
    hash1 = pipeline._image_hash(test_frame)
    
    print(f"\n  图像哈希: {hash1}")
    print(f"  缓存状态: {'启用' if pipeline.enable_preprocess_cache else '禁用'}")
    print(f"  TTL: {pipeline.cache_ttl}秒")

def test_performance_comparison():
    """性能对比测试"""
    print("\n" + "=" * 70)
    print("🧪 测试4: 性能对比（优化前后）")
    print("=" * 70)
    
    from core.step_detector import StepDetector
    
    # 测试无缓存
    detector_no_cache = StepDetector(use_cache=False)
    test_frame = np.random.randint(0, 255, (640, 480, 3), dtype=np.uint8)
    
    # 多次检测测试
    times_no_cache = []
    for _ in range(5):
        start = time.time()
        detector_no_cache.detect_step(test_frame)
        times_no_cache.append((time.time() - start) * 1000)
    
    # 测试有缓存
    detector_cache = StepDetector(use_cache=True, cache_ttl=5.0)
    times_with_cache = []
    for _ in range(5):
        start = time.time()
        detector_cache.detect_step(test_frame)
        times_with_cache.append((time.time() - start) * 1000)
    
    avg_no_cache = sum(times_no_cache) / len(times_no_cache)
    avg_with_cache = sum(times_with_cache) / len(times_with_cache)
    
    print(f"\n  无缓存平均: {avg_no_cache:.2f}ms")
    print(f"  有缓存平均: {avg_with_cache:.2f}ms")
    
    if avg_with_cache < avg_no_cache:
        improvement = (avg_no_cache - avg_with_cache) / avg_no_cache * 100
        print(f"  ✅ 性能提升: {improvement:.1f}%")
    else:
        print(f"  ⚠️ 缓存效果不明显")

def run_all_tests():
    """运行所有测试"""
    print("\n" + "╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "🚀 性能优化测试套件" + " " * 30 + "║")
    print("╚" + "=" * 68 + "╝")
    
    try:
        test_step_detector_optimization()
    except Exception as e:
        print(f"  ❌ 测试1失败: {e}")
    
    try:
        test_navigation_optimizer()
    except Exception as e:
        print(f"  ❌ 测试2失败: {e}")
    
    try:
        test_vision_pipeline_cache()
    except Exception as e:
        print(f"  ❌ 测试3失败: {e}")
    
    try:
        test_performance_comparison()
    except Exception as e:
        print(f"  ❌ 测试4失败: {e}")
    
    print("\n" + "=" * 70)
    print("✅ 所有测试完成")
    print("=" * 70)

if __name__ == "__main__":
    run_all_tests()

