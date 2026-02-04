#!/usr/bin/env python3
"""
B2 v0.2 缓存逻辑测试

测试目标：
1. WorldSignature 是否稳定
2. FutureCache 是否复用
3. AdvisoryCache 是否抑制重复输出

使用方法：
    python3 examples/b2_v02_cache_test.py > b2_log.txt 2>&1
    python3 -m vision_pipeline.b2.b2_cache_observer b2_log.txt
"""

import sys
import time
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

# 直接导入 B2 模块（避免经过 vision_pipeline.__init__）
import importlib.util
b2_controller_path = Path(__file__).parent.parent / "vision_pipeline" / "b2" / "b2_controller_v02.py"
spec = importlib.util.spec_from_file_location("b2_controller_v02", b2_controller_path)
b2_controller_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b2_controller_module)
B2Controller = b2_controller_module.B2Controller

world_snapshot_path = Path(__file__).parent.parent / "vision_pipeline" / "b2" / "world_snapshot.py"
spec2 = importlib.util.spec_from_file_location("world_snapshot", world_snapshot_path)
world_snapshot_module = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(world_snapshot_module)
WorldSnapshot = world_snapshot_module.WorldSnapshot
EgoPose = world_snapshot_module.EgoPose
WorldObject = world_snapshot_module.WorldObject


def main():
    print("=" * 70)
    print("B2 v0.2 缓存逻辑测试")
    print("=" * 70)
    print()
    
    # 初始化 B2 Controller（使用默认 TTL）
    controller = B2Controller(
        ttl_sec=10.0,
        min_interval_sec=3.0,
        horizon_sec=8.0,
    )
    
    print("✅ B2Controller 初始化成功")
    print()
    
    base_time = time.time()
    
    # 测试场景 1：稳定场景（相同 WorldSignature，应该复用缓存）
    print("📋 测试场景 1: 稳定场景（相同 WorldSignature）")
    print("   期望: future_cache=reused, advisory suppressed")
    print()
    
    for i in range(5):
        snapshot = WorldSnapshot(
            timestamp=base_time + i * 0.5,  # 每 0.5 秒一次
            ego=EgoPose(heading=0.0, speed=1.0),
            objects=[
                WorldObject(obj_id="obj_1", cls="person", pos=[5.0, 0.0], vel=[0.0, 0.0]),
            ],
            texts=["test"],
        )
        
        advisory = controller.observe(snapshot)
        time.sleep(0.1)  # 短暂延迟
    
    print()
    time.sleep(2.0)  # 等待一下
    
    # 测试场景 2：世界变化（WorldSignature 变化，应该重算）
    print("📋 测试场景 2: 世界变化（WorldSignature 变化）")
    print("   期望: future_cache=expired recompute, 产出新 advisory")
    print()
    
    snapshot2 = WorldSnapshot(
        timestamp=base_time + 5.0,
        ego=EgoPose(heading=90.0, speed=2.0),  # heading 和 speed 都变了
        objects=[
            WorldObject(obj_id="obj_1", cls="person", pos=[5.0, 0.0], vel=[0.0, 0.0]),
            WorldObject(obj_id="obj_2", cls="car", pos=[10.0, 0.0], vel=[1.0, 0.0]),  # 新增对象
        ],
        texts=["test", "another"],
    )
    
    advisory2 = controller.observe(snapshot2)
    if advisory2:
        print(f"   ✅ 产出 Advisory: {advisory2.advisory_type}")
    print()
    time.sleep(2.0)
    
    # 测试场景 3：相同世界，但 TTL 过期（应该重算）
    print("📋 测试场景 3: TTL 过期（相同 WorldSignature，但超过 TTL）")
    print("   期望: future_cache=expired recompute（TTL 过期）")
    print()
    
    time.sleep(11.0)  # 等待 TTL 过期（10 秒）
    
    snapshot3 = WorldSnapshot(
        timestamp=base_time + 18.0,
        ego=EgoPose(heading=90.0, speed=2.0),  # 相同
        objects=[
            WorldObject(obj_id="obj_1", cls="person", pos=[5.0, 0.0], vel=[0.0, 0.0]),
            WorldObject(obj_id="obj_2", cls="car", pos=[10.0, 0.0], vel=[1.0, 0.0]),  # 相同
        ],
        texts=["test", "another"],
    )
    
    advisory3 = controller.observe(snapshot3)
    if advisory3:
        print(f"   ✅ 产出 Advisory: {advisory3.advisory_type}")
    print()
    
    # 测试场景 4：重复相同 advisory（应该被抑制）
    print("📋 测试场景 4: 重复相同 advisory（相同 WorldSignature + 相同类型）")
    print("   期望: advisory suppressed")
    print()
    
    snapshot4 = WorldSnapshot(
        timestamp=base_time + 19.0,
        ego=EgoPose(heading=90.0, speed=2.0),  # 相同
        objects=[
            WorldObject(obj_id="obj_1", cls="person", pos=[5.0, 0.0], vel=[0.0, 0.0]),
            WorldObject(obj_id="obj_2", cls="car", pos=[10.0, 0.0], vel=[1.0, 0.0]),  # 相同
        ],
        texts=["test", "another"],
    )
    
    advisory4 = controller.observe(snapshot4)
    if advisory4 is None:
        print("   ✅ 正确被抑制")
    else:
        print(f"   ⚠️  未正确抑制，产出: {advisory4.advisory_type}")
    print()
    
    print("=" * 70)
    print("✅ B2 v0.2 缓存逻辑测试完成")
    print("=" * 70)
    print()
    print("📋 下一步:")
    print("   1. 查看上面的日志输出")
    print("   2. 使用观测工具分析:")
    print("      python3 -m vision_pipeline.b2.b2_cache_observer b2_log.txt")
    print()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

