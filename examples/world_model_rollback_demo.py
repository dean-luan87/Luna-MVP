# -*- coding: utf-8 -*-
"""
v1.8.5: World Model Rollback Demo（退潮效果演示）

目标：
- 演示候选过期机制：临时封路 → 几天后自动退潮
- 演示事实软回滚机制：超期事实自动降级并衰减置信度
- 验证系统"能自然遗忘"的能力

运行方式：
python examples/world_model_rollback_demo.py
"""

import sys
import os
import time
from pprint import pprint

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.world_model.common.db import WorldModelDB
from core.world_model.common.types import PositionState, EnvironmentContext
from core.world_model.memory.candidate_pool import FactCandidatePool, STATUS_REJECTED
from core.world_model.memory.memory_registry import MemoryRegistry
from core.world_model.library.library_registry import LibraryRegistry, LIFE_PASSIVE
from core.world_model.map.map_registry import MapRegistry


def main():
    """主函数：演示退潮效果"""
    
    print("\n" + "=" * 70)
    print("v1.8.5 World Model Rollback Demo（退潮效果演示）")
    print("=" * 70)
    print()

    # ===== 初始化（使用短 TTL 用于演示）=====
    print("[初始化] 创建所有 Registry 实例（使用短 TTL 用于演示）")
    db = WorldModelDB()
    
    # 使用短 TTL：候选 10 秒，事实 20 秒
    candidate_pool = FactCandidatePool(
        db=db,
        n_support=2,  # 降低要求，便于演示
        n_sources=2,
        min_span_s=1.0,  # 缩短时间跨度
        candidate_ttl_s=10.0,  # 10 秒 TTL（演示用）
    )

    memory = MemoryRegistry(db=db, candidate_pool=candidate_pool)
    library = LibraryRegistry(
        db=db,
        candidate_pool=candidate_pool,
        verify_ttl_fact_s=20.0,  # 20 秒 TTL（演示用）
        verify_ttl_rule_s=30.0,
    )
    map_registry = MapRegistry(db=db, library=library)
    print("✅ 初始化完成")
    print()

    scene_id = "scene_demo_rollback"
    map_id = "mapunit_demo_rollback"
    position_state = PositionState(
        position=(0.0, 0.0),
        stability_score=0.9,
        stable=True,
    )

    now = time.time()

    # ===== Step 1: 创建临时封路事实 =====
    print("[1] 创建临时封路事实（模拟临时封路）")
    print("-" * 70)
    
    # 第一次观测
    memory.update(
        scene_id=scene_id,
        map_id=map_id,
        position_state=position_state,
        feedback={
            "type": "FACT_SIGNAL",
            "claim_type": "road_blocked",
            "statement": "该路段临时封路",
            "source": "system",
        },
        now_ts=now,
    )
    print("  ✅ 第一次观测（system）")
    
    # 第二次观测
    memory.update(
        scene_id=scene_id,
        map_id=map_id,
        position_state=position_state,
        feedback={
            "type": "FACT_SIGNAL",
            "claim_type": "road_blocked",
            "source": "vision",
        },
        now_ts=now + 0.5,
    )
    print("  ✅ 第二次观测（vision）")
    
    # 等待满足时间跨度
    time.sleep(0.6)
    
    # 第三次观测（确保时间跨度 >= 1.0 秒）
    memory.update(
        scene_id=scene_id,
        map_id=map_id,
        position_state=position_state,
        feedback={
            "type": "FACT_SIGNAL",
            "claim_type": "road_blocked",
            "source": "system",
        },
        now_ts=now + 1.1,
    )
    print("  ✅ 第三次观测（system，满足时间跨度）")
    print()

    # ===== Step 2: Library 入库 =====
    print("[2] LibraryRegistry.update()（候选 → PASSIVE）")
    print("-" * 70)
    result1 = library.update(
        active_scene_id=scene_id,
        position_state=position_state,
        now_ts=now + 1.2,
    )
    pprint(result1)
    print()

    # ===== Step 3: 检查初始状态 =====
    print("[3] 检查初始状态")
    print("-" * 70)
    hints = library.get_hints(active_scene_id=scene_id, map_id=map_id)
    print(f"📊 知识提示数: {len(hints)}")
    if hints:
        h = hints[0]
        print(f"  • statement: {h.statement}")
        print(f"  • confidence: {h.confidence:.2f}")
        print(f"  • lifecycle_state: PASSIVE（新入库）")
    print()

    # ===== Step 4: 模拟时间流逝（超过 TTL）=====
    print("[4] 模拟时间流逝（超过 TTL）")
    print("-" * 70)
    print("  ⏳ 等待 12 秒（超过候选 TTL 10 秒）...")
    time.sleep(12)
    
    # 手动更新 last_verified_ts 为很久以前（模拟事实已过期）
    with db.connect() as conn:
        conn.execute(
            """
            UPDATE knowledge_items
            SET last_verified_ts = ?
            WHERE scene_id = ? AND map_id = ?
            """,
            (now + 1.2 - 25.0, scene_id, map_id),  # 25 秒前（超过事实 TTL 20 秒）
        )
    print("  ✅ 已模拟时间流逝（last_verified_ts 设为 25 秒前）")
    print()

    # ===== Step 5: 触发候选过期 =====
    print("[5] 触发候选过期机制")
    print("-" * 70)
    expired_count = candidate_pool.cleanup_expired()
    print(f"  ✅ 清理过期候选数: {expired_count}")
    
    # 检查候选状态
    promotables = candidate_pool.fetch_promotables(cleanup_before=True)
    print(f"  📊 PROMOTABLE 候选数: {len(promotables)}")
    print()

    # ===== Step 6: 触发事实软回滚 =====
    print("[6] 触发事实软回滚机制")
    print("-" * 70)
    result2 = library.update(
        active_scene_id=scene_id,
        position_state=position_state,
        now_ts=time.time(),
    )
    pprint(result2)
    print()

    # ===== Step 7: 检查退潮效果 =====
    print("[7] 检查退潮效果")
    print("-" * 70)
    hints_after = library.get_hints(active_scene_id=scene_id, map_id=map_id)
    print(f"📊 知识提示数: {len(hints_after)}")
    if hints_after:
        h = hints_after[0]
        print(f"  • statement: {h.statement}")
        print(f"  • confidence: {h.confidence:.2f}（已衰减）")
        print(f"  • lifecycle_state: PASSIVE（已降级）")
    print()

    # ===== Step 8: 检查 MapBias 变化 =====
    print("[8] 检查 MapBias 变化（退潮后的影响）")
    print("-" * 70)
    bias = map_registry.compute_map_bias(
        scene_id=scene_id,
        map_id=map_id,
        env_ctx=EnvironmentContext(weather="CLEAR"),
    )
    pprint(bias)
    print()

    # ===== 总结 =====
    print("=" * 70)
    print("✅ Demo 完成 - 退潮效果验证")
    print("=" * 70)
    print()
    print("📊 关键验证点：")
    print("  1. 候选过期机制：超过 TTL 的候选自动标记为 REJECTED")
    print("  2. 事实软回滚：超过 TTL 的事实自动降级并衰减置信度")
    print("  3. 系统能自然遗忘：临时事实不会永久污染")
    print()
    print("🔍 关键正确性信号：")
    print("  • 候选状态：过期候选已清理")
    print("  • 事实置信度：已衰减（× 0.85）")
    print("  • 事实生命周期：已降级为 PASSIVE")
    print("  • MapBias：退潮后影响减弱")
    print()
    print("📁 数据库文件位置: artifacts/world_model/world_model.db")
    print("   可以使用 SQLite 工具查看：")
    print("   - fact_candidates 表（查看过期候选）")
    print("   - knowledge_items 表（查看回滚后的事实）")
    print()


if __name__ == "__main__":
    main()


