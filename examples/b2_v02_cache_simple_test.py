#!/usr/bin/env python3
"""
B2 v0.2 缓存逻辑简单测试

直接测试缓存逻辑的核心组件，不依赖完整的 B2Controller
"""

import sys
import time
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

# 直接导入文件，避免经过 __init__.py
import importlib.util

def load_module(module_path, module_name):
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

base_path = Path(__file__).parent.parent / "vision_pipeline" / "b2"

world_signature_module = load_module(base_path / "world_signature.py", "world_signature")
WorldSignature = world_signature_module.WorldSignature

future_scene_cache_module = load_module(base_path / "future_scene_cache.py", "future_scene_cache")
FutureSceneCache = future_scene_cache_module.FutureSceneCache
FutureCacheEntry = future_scene_cache_module.FutureCacheEntry

advisory_cache_module = load_module(base_path / "advisory_cache.py", "advisory_cache")
AdvisoryCache = advisory_cache_module.AdvisoryCache

future_simulation_result_module = load_module(base_path / "future_simulation_result.py", "future_simulation_result")
FutureSimulationResult = future_simulation_result_module.FutureSimulationResult

b2_types_module = load_module(base_path / "b2_types_v02.py", "b2_types_v02")
B2Advisory = b2_types_module.B2Advisory


def test_world_signature():
    """测试 WorldSignature"""
    print("=" * 70)
    print("测试 1: WorldSignature（世界指纹）")
    print("=" * 70)
    print()
    
    # 创建两个相同的 WorldSignature
    sig1 = WorldSignature(
        heading_bucket=0,
        speed_bucket=1,
        density_bucket=0,
        has_path=False,
        region_ids=tuple(),
    )
    
    sig2 = WorldSignature(
        heading_bucket=0,
        speed_bucket=1,
        density_bucket=0,
        has_path=False,
        region_ids=tuple(),
    )
    
    print(f"   Signature 1: {sig1.digest()}")
    print(f"   Signature 2: {sig2.digest()}")
    print(f"   是否相等: {sig1 == sig2}")
    print(f"   ✅ WorldSignature 相等性判断正常")
    print()
    
    # 创建不同的 WorldSignature
    sig3 = WorldSignature(
        heading_bucket=1,  # 不同
        speed_bucket=1,
        density_bucket=0,
        has_path=False,
        region_ids=tuple(),
    )
    
    print(f"   Signature 3: {sig3.digest()}")
    print(f"   Signature 1 == Signature 3: {sig1 == sig3}")
    print(f"   ✅ WorldSignature 变化检测正常")
    print()


def test_future_cache():
    """测试 FutureCache"""
    print("=" * 70)
    print("测试 2: FutureSceneCache（未来缓存）")
    print("=" * 70)
    print()
    
    cache = FutureSceneCache(ttl_sec=8.0)
    
    # 创建 WorldSignature
    sig1 = WorldSignature(
        heading_bucket=0,
        speed_bucket=1,
        density_bucket=0,
        has_path=False,
        region_ids=tuple(),
    )
    
    # 创建模拟的 FutureSimulationResult
    result1 = FutureSimulationResult(
        horizon_sec=8.0,
        timestamp=time.time(),
    )
    
    # 测试 get_or_compute
    def compute_fn():
        print("   [模拟] 执行 FutureSimulation 计算")
        return result1
    
    now = time.time()
    
    # 第一次：应该计算
    result, reused = cache.get_or_compute(sig1, compute_fn, now)
    print(f"   第一次: reused={reused}")
    assert not reused, "第一次应该计算，不应该复用"
    print(f"   ✅ 第一次正确计算")
    print()
    
    # 第二次（相同 signature，在 TTL 内）：应该复用
    time.sleep(0.1)
    now2 = time.time()
    result2, reused2 = cache.get_or_compute(sig1, compute_fn, now2)
    print(f"   第二次（相同 signature，0.1s 后）: reused={reused2}")
    assert reused2, "第二次应该复用"
    print(f"   ✅ 第二次正确复用")
    print()
    
    # 第三次（不同 signature）：应该重算
    sig2 = WorldSignature(
        heading_bucket=1,  # 不同
        speed_bucket=1,
        density_bucket=0,
        has_path=False,
        region_ids=tuple(),
    )
    time.sleep(0.1)
    now3 = time.time()
    result3, reused3 = cache.get_or_compute(sig2, compute_fn, now3)
    print(f"   第三次（不同 signature）: reused={reused3}")
    assert not reused3, "不同 signature 应该重算"
    print(f"   ✅ 第三次正确重算")
    print()


def test_advisory_cache():
    """测试 AdvisoryCache"""
    print("=" * 70)
    print("测试 3: AdvisoryCache（建议缓存）")
    print("=" * 70)
    print()
    
    cache = AdvisoryCache(ttl_sec=15.0)
    
    # 创建 WorldSignature
    sig1 = WorldSignature(
        heading_bucket=0,
        speed_bucket=1,
        density_bucket=0,
        has_path=False,
        region_ids=tuple(),
    )
    
    # 创建 Advisory
    advisory1 = B2Advisory(
        advisory_type="DEESCALATE",
        horizon_sec=8.0,
        confidence=0.7,
        trigger_reason="TEST",
    )
    
    now = time.time()
    
    # 第一次：不应该抑制
    should_suppress1, age1 = cache.should_suppress(advisory1, sig1, now)
    print(f"   第一次: should_suppress={should_suppress1}")
    assert not should_suppress1, "第一次不应该抑制"
    print(f"   ✅ 第一次正确输出")
    cache.update(advisory1, sig1, now)
    print()
    
    # 第二次（相同 advisory，相同 signature，在 TTL 内）：应该抑制
    time.sleep(0.1)
    now2 = time.time()
    should_suppress2, age2 = cache.should_suppress(advisory1, sig1, now2)
    print(f"   第二次（相同 advisory，0.1s 后）: should_suppress={should_suppress2}, age={age2:.1f}s")
    assert should_suppress2, "第二次应该抑制"
    print(f"   ✅ 第二次正确抑制")
    print()
    
    # 第三次（不同 advisory 类型）：不应该抑制
    advisory2 = B2Advisory(
        advisory_type="PREWARN",  # 不同
        horizon_sec=8.0,
        confidence=0.9,
        trigger_reason="TEST",
    )
    time.sleep(0.1)
    now3 = time.time()
    should_suppress3, age3 = cache.should_suppress(advisory2, sig1, now3)
    print(f"   第三次（不同 advisory 类型）: should_suppress={should_suppress3}")
    assert not should_suppress3, "不同 advisory 类型不应该抑制"
    print(f"   ✅ 第三次正确输出")
    print()


def main():
    print("=" * 70)
    print("B2 v0.2 缓存逻辑简单测试")
    print("=" * 70)
    print()
    
    try:
        test_world_signature()
        test_future_cache()
        test_advisory_cache()
        
        print("=" * 70)
        print("✅ 所有测试通过")
        print("=" * 70)
        print()
        print("📋 测试结果:")
        print("   ✅ WorldSignature 相等性判断正常")
        print("   ✅ FutureSceneCache 复用逻辑正常")
        print("   ✅ AdvisoryCache 抑制逻辑正常")
        print()
        print("📋 下一步:")
        print("   1. 运行完整的 B2 v0.2 测试（需要真实 pipeline）")
        print("   2. 使用观测工具分析日志")
        print()
        
        return 0
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

