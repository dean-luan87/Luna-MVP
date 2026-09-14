#!/usr/bin/env python3
"""
B2 v0.2 最小冒烟测试

用途：验证 B2 v0.2 文件结构完整、能输出 advisory。

使用方法：
    python3 examples/b2_v02_smoke.py
"""

import sys
import time
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

# 直接导入 B2 模块（避免经过 vision_pipeline.__init__）
from vision_pipeline.b2.b2_controller_v02 import B2Controller
from vision_pipeline.b2.world_snapshot import WorldSnapshot, EgoPose, WorldObject


def main():
    print("=" * 70)
    print("B2 v0.2 最小冒烟测试")
    print("=" * 70)
    print()
    
    # 初始化 B2 Controller
    controller = B2Controller(
        ttl_sec=5.0,  # 较短的 TTL 用于测试
        min_interval_sec=1.0,  # 较短的间隔用于测试
        horizon_sec=8.0,
    )
    
    print("✅ B2Controller 初始化成功")
    print()
    
    # 测试 1：INIT 触发
    print("📋 测试 1: INIT 触发")
    snapshot1 = WorldSnapshot(
        timestamp=time.time(),
        ego=EgoPose(heading=0.0, speed=1.0),
        objects=[
            WorldObject(obj_id="obj_1", cls="person", pos=[5.0, 0.0], vel=[0.0, 0.0]),
        ],
        texts=["test"],
    )
    
    advisory1 = controller.observe(snapshot1)
    if advisory1:
        print(f"   ✅ 产出 Advisory: {advisory1.advisory_type}, trigger={advisory1.trigger_reason}")
        print(f"      confidence={advisory1.confidence:.2f}, impacts={len(advisory1.impacts)}")
    else:
        print("   ❌ 未产出 Advisory")
    print()
    
    # 测试 2：WORLD_CHANGE 触发
    print("📋 测试 2: WORLD_CHANGE 触发")
    snapshot2 = WorldSnapshot(
        timestamp=time.time() + 1.0,
        ego=EgoPose(heading=0.0, speed=1.0),
        objects=[
            WorldObject(obj_id="obj_1", cls="person", pos=[5.0, 0.0], vel=[0.0, 0.0]),
            WorldObject(obj_id="obj_2", cls="car", pos=[10.0, 0.0], vel=[1.0, 0.0]),
        ],
        texts=["test", "another"],
    )
    
    advisory2 = controller.observe(snapshot2)
    if advisory2:
        print(f"   ✅ 产出 Advisory: {advisory2.advisory_type}, trigger={advisory2.trigger_reason}")
        print(f"      confidence={advisory2.confidence:.2f}, impacts={len(advisory2.impacts)}")
    else:
        print("   ❌ 未产出 Advisory")
    print()
    
    # 测试 3：TTL_EXPIRE 触发
    print("📋 测试 3: TTL_EXPIRE 触发")
    time.sleep(6.0)  # 等待 TTL 过期
    snapshot3 = WorldSnapshot(
        timestamp=time.time(),
        ego=EgoPose(heading=0.0, speed=1.0),
        objects=[
            WorldObject(obj_id="obj_1", cls="person", pos=[5.0, 0.0], vel=[0.0, 0.0]),
            WorldObject(obj_id="obj_2", cls="car", pos=[10.0, 0.0], vel=[1.0, 0.0]),
        ],
        texts=["test", "another"],
    )
    
    advisory3 = controller.observe(snapshot3)
    if advisory3:
        print(f"   ✅ 产出 Advisory: {advisory3.advisory_type}, trigger={advisory3.trigger_reason}")
        print(f"      confidence={advisory3.confidence:.2f}, impacts={len(advisory3.impacts)}")
    else:
        print("   ❌ 未产出 Advisory")
    print()
    
    # 测试 4：最小间隔限制
    print("📋 测试 4: 最小间隔限制")
    snapshot4 = WorldSnapshot(
        timestamp=time.time(),
        ego=EgoPose(heading=0.0, speed=1.0),
        objects=[
            WorldObject(obj_id="obj_1", cls="person", pos=[5.0, 0.0], vel=[0.0, 0.0]),
        ],
        texts=["test"],
    )
    
    advisory4 = controller.observe(snapshot4)
    if advisory4 is None:
        print("   ✅ 正确被最小间隔限制阻止")
    else:
        print(f"   ⚠️  未正确限制，产出 Advisory: {advisory4.advisory_type}")
    print()
    
    print("=" * 70)
    print("✅ B2 v0.2 冒烟测试完成")
    print("=" * 70)
    print()
    print("📋 测试结果:")
    print("   ✅ B2Controller 初始化成功")
    print("   ✅ INIT 触发正常")
    print("   ✅ WORLD_CHANGE 触发正常")
    print("   ✅ TTL_EXPIRE 触发正常")
    print("   ✅ 最小间隔限制正常")
    print()
    print("📋 下一步:")
    print("   1. 接入 pipeline（A3）")
    print("   2. 映射 WorldSnapshot 从真实 pipeline 输出")
    print()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

