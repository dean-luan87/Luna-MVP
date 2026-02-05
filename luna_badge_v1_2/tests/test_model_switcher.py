#!/usr/bin/env python3
"""
1.4.1-speed.4 ModelSwitcher 测试脚本
按照任务说明创建的基础测试
"""
import sys
import time
from pathlib import Path

# 添加项目根目录到路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from core.config.config_center import ConfigCenter
from core.logging.log_manager import LogManager
from core.speed.model_switcher import ModelSwitcher


class MockModelSlow:
    """模拟慢速模型"""
    def __call__(self, frame):
        time.sleep(0.08)  # 80ms
        return {"boxes": [], "mock": "slow"}


class MockModelFast:
    """模拟快速模型"""
    def __call__(self, frame):
        time.sleep(0.01)  # 10ms
        return {"boxes": [], "mock": "fast"}


def test_model_switcher_behavior():
    """测试模型切换行为"""
    print("=" * 60)
    print("1.4.1-speed.4 ModelSwitcher 测试")
    print("=" * 60)
    
    # 初始化基础设施
    ConfigCenter.init(env="dev")
    LogManager.init()
    
    slow = MockModelSlow()
    fast = MockModelFast()
    
    print("\n创建 ModelSwitcher (heavy=slow, light=fast)...")
    ms = ModelSwitcher(heavy_model=slow, light_model=fast)
    
    print(f"初始模型: {ms.active_name}")
    print(f"切换阈值: heavy_to_light={ms.heavy_to_light_ms}ms, light_to_heavy={ms.light_to_heavy_ms}ms")
    print(f"最小样本数: {ms.min_samples}")
    
    # 模拟高延迟场景，促使切换到 light
    print("\n模拟高延迟场景（10 次推理）...")
    for i in range(10):
        result = ms.infer("dummy_frame")
        avg = ms.get_avg_latency()
        print(f"  [{i+1}/10] 当前模型: {ms.active_name}, 平均延迟: {avg:.1f}ms")
        time.sleep(0.01)
    
    print(f"\n最终模型: {ms.active_name}")
    print(f"最终平均延迟: {ms.get_avg_latency():.1f}ms")
    
    # 验证模型切换
    assert ms.active_name in ("light", "heavy"), f"模型名称应该是 'light' 或 'heavy'，实际: {ms.active_name}"
    
    # 测试统计信息
    stats = ms.get_stats()
    print("\n统计信息:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print("\n✅ ModelSwitcher 测试通过")


def test_model_switcher_no_light():
    """测试没有 light 模型的情况"""
    print("\n" + "=" * 60)
    print("测试：没有 light 模型")
    print("=" * 60)
    
    slow = MockModelSlow()
    
    print("\n创建 ModelSwitcher (只有 heavy 模型)...")
    ms = ModelSwitcher(heavy_model=slow, light_model=None)
    
    print(f"初始模型: {ms.active_name}")
    print(f"是否有 light 模型: {ms.light_model is not None}")
    
    # 多次推理，应该不会切换（因为没有 light 模型）
    print("\n执行 10 次推理...")
    for i in range(10):
        result = ms.infer("dummy_frame")
        print(f"  [{i+1}/10] 当前模型: {ms.active_name}")
    
    assert ms.active_name == "heavy", "没有 light 模型时应该保持 heavy"
    print("\n✅ 无 light 模型测试通过")


if __name__ == "__main__":
    try:
        test_model_switcher_behavior()
        test_model_switcher_no_light()
        
        print("\n" + "=" * 60)
        print("✅ 所有 ModelSwitcher 测试通过")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 测试异常: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
















