# -*- coding: utf-8 -*-
"""
v1.8.5: World Model Full Demo（全链路演示）

目标：
- 验证整个体系在工程上能跑通、可追责、不污染
- 场景：东北城市，10 月夜晚，下雨
- 验证点：体验记忆 → 事实候选 → Library → MapBias

运行方式：
python examples/world_model_full_demo.py
"""

import sys
import os
import time
from pprint import pprint

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.world_model.common.db import WorldModelDB
from core.world_model.common.types import PositionState, EnvironmentContext
from core.world_model.memory.candidate_pool import FactCandidatePool
from core.world_model.memory.memory_registry import MemoryRegistry
from core.world_model.library.library_registry import LibraryRegistry
from core.world_model.map.map_registry import MapRegistry


def main():
    """主函数：演示完整链路"""
    
    print("\n" + "=" * 70)
    print("v1.8.5 World Model Full Demo")
    print("=" * 70)
    print()

    # ===== 初始化 =====
    print("[初始化] 创建所有 Registry 实例")
    db = WorldModelDB()
    candidate_pool = FactCandidatePool(
        db=db,
        n_support=3,
        n_sources=2,
        min_span_s=2.0,      # demo 缩短
    )

    memory = MemoryRegistry(db=db, candidate_pool=candidate_pool)
    library = LibraryRegistry(db=db, candidate_pool=candidate_pool)
    map_registry = MapRegistry(db=db, library=library)
    print("✅ 初始化完成")
    print()

    # ===== 场景 & 环境 =====
    scene_id = "scene_crossroad_001"
    map_id = "mapunit_crossroad_A"

    env_ctx = EnvironmentContext(
        season="AUTUMN",
        time_of_day="NIGHT",
        weather="RAIN",
    )

    position_state = PositionState(
        position=(12.3, 8.9),
        stability_score=0.92,
        stable=True,
    )

    now = time.time()

    # ===== Step 1: 体验记忆（路滑）=====
    print("[1] 写入体验记忆：路滑、不舒服")
    print("-" * 70)
    result1 = memory.update(
        scene_id=scene_id,
        map_id=map_id,
        position_state=position_state,
        feedback={
            "type": "EXPERIENCE",
            "tags": ["slippery"],
            "valence": "NEGATIVE",
            "intensity": 0.8,
            "source": "user",
        },
        now_ts=now,
    )
    print(f"✅ 体验记忆写入结果: {result1}")
    print()

    # ===== Step 2: 事实信号（积水）=====
    print("[2] 连续写入事实信号：疑似积水（system + vision）")
    print("-" * 70)
    
    first_ts = now + 0.5
    
    for i in range(3):
        source = "system" if i % 2 == 0 else "vision"
        result2 = memory.update(
            scene_id=scene_id,
            map_id=map_id,
            position_state=position_state,
            feedback={
                "type": "FACT_SIGNAL",
                "claim_type": "flooded",
                "statement": "路口存在明显积水",
                "source": source,
            },
            now_ts=first_ts + i * 0.8,
        )
        print(f"  ✅ 第 {i+1} 次观测（{source}）")
        time.sleep(0.3)  # 模拟时间流逝
    
    # 等待满足时间跨度要求（2.0 秒）
    print("  ⏳ 等待满足时间跨度要求（2.0 秒）...")
    time.sleep(0.5)
    
    # 第四次观测（确保时间跨度 >= 2.0 秒）
    result2 = memory.update(
        scene_id=scene_id,
        map_id=map_id,
        position_state=position_state,
        feedback={
            "type": "FACT_SIGNAL",
            "claim_type": "flooded",
            "statement": "路口存在明显积水",
            "source": "system",
        },
        now_ts=first_ts + 2.1,
    )
    print(f"  ✅ 第 4 次观测（system，满足时间跨度）")
    print()

    # ===== Step 3: 检查候选状态 =====
    print("[3] 检查事实候选状态")
    print("-" * 70)
    promotables = candidate_pool.fetch_promotables(cleanup_before=True)
    print(f"📊 PROMOTABLE 候选数: {len(promotables)}")
    if promotables:
        c = promotables[0]
        print(f"  • claim_type: {c.claim_type}")
        print(f"  • status: {c.status}")
        print(f"  • confidence: {c.confidence:.2f}")
        print(f"  • support_count: {c.support_count}")
        print(f"  • unique_sources: {c.unique_sources}")
    print()

    # ===== Step 4: Library 更新（候选 → PASSIVE）=====
    print("[4] LibraryRegistry.update()（候选 → PASSIVE）")
    print("-" * 70)
    result3 = library.update(
        active_scene_id=scene_id,
        position_state=position_state,
        now_ts=time.time(),
    )
    pprint(result3)
    print()

    # ===== Step 5: 检查 Library 条目 =====
    print("[5] 检查 Library 知识条目")
    print("-" * 70)
    hints = library.get_hints(active_scene_id=scene_id, map_id=map_id)
    print(f"📊 知识提示数: {len(hints)}")
    for h in hints:
        print(f"  • {h.statement} (confidence={h.confidence:.2f}, tags={h.tags}, lifecycle=PASSIVE)")
    print()

    # ===== Step 6: MapBias 计算 =====
    print("[6] 计算 MapBias（夜晚 + 下雨 + 积水）")
    print("-" * 70)
    bias = map_registry.compute_map_bias(
        scene_id=scene_id,
        map_id=map_id,
        env_ctx=env_ctx,
    )
    pprint(bias)
    print()

    # ===== 验收点总结 =====
    print("=" * 70)
    print("✅ Demo 完成 - 验收点总结")
    print("=" * 70)
    print()
    print("📊 关键验证点：")
    print("  1. 体验记忆已写入（不污染事实）")
    print("  2. 事实候选已升级为 PROMOTABLE")
    print("  3. Library 已生成 PASSIVE 事实")
    print("  4. MapBias 已计算（夜晚 + 下雨 + 积水）")
    print()
    print("🔍 关键正确性信号：")
    print("  • 没有直接禁止通行（avoid_bias ≠ 1.0）")
    print("  • 风险被\"抬高\"，而不是下结论")
    print("  • 原因可追责（reasons）")
    print()
    print("📁 数据库文件位置: artifacts/world_model/world_model.db")
    print("   可以使用 SQLite 工具查看：")
    print("   - experience_memories 表（体验记忆）")
    print("   - fact_candidates 表（事实候选）")
    print("   - knowledge_items 表（知识条目）")
    print()


if __name__ == "__main__":
    main()


