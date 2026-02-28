# -*- coding: utf-8 -*-
"""
v1.8.5: World Model Memory 完整闭环演示

目标：
- 验证 MemoryRegistry → FactCandidatePool → LibraryRegistry 完整闭环
- 验证体验记忆、偏好、事实候选的分流

运行方式：
python examples/world_model_memory_demo.py
"""

import sys
import os
import time

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.world_model.common.db import WorldModelDB
from core.world_model.common.types import PositionState
from core.world_model.memory.candidate_pool import FactCandidatePool
from core.world_model.memory.memory_registry import MemoryRegistry
from core.world_model.library.library_registry import LibraryRegistry


def main():
    """主函数：演示 MemoryRegistry → FactCandidatePool → LibraryRegistry 完整闭环"""
    
    print("=" * 70)
    print("World Model Memory 完整闭环演示")
    print("=" * 70)
    print()
    
    # 初始化
    db = WorldModelDB()
    pool = FactCandidatePool(db=db, n_support=3, n_sources=2, min_span_s=1.0, candidate_ttl_s=24 * 3600)
    memory = MemoryRegistry(db=db, candidate_pool=pool)
    lib = LibraryRegistry(db=db, candidate_pool=pool)
    
    scene_id = "scene_crossing_001"
    map_id = "map_unit_001"
    ps = PositionState(position=(0.0, 0.0), stability_score=0.9, stable=True)
    
    print("1️⃣ MemoryRegistry：写入体验记忆")
    print("-" * 70)
    
    memory.update(
        scene_id=scene_id,
        map_id=map_id,
        position_state=ps,
        feedback={
            "type": "EXPERIENCE",
            "tags": ["slippery", "crowded"],
            "valence": "NEGATIVE",
            "intensity": 0.8,
            "source": "user",
        },
    )
    print("  ✅ 体验记忆已写入（slippery, crowded, NEGATIVE）")
    print()
    
    print("2️⃣ MemoryRegistry：写入偏好")
    print("-" * 70)
    
    memory.update(
        scene_id=scene_id,
        map_id=map_id,
        position_state=ps,
        feedback={
            "type": "PREFERENCE",
            "pref_type": "avoid",
            "tags": ["crowded"],
            "weight": 0.9,
        },
    )
    print("  ✅ 偏好已写入（avoid crowded, weight=0.9）")
    print()
    
    print("3️⃣ MemoryRegistry：发出事实候选信号")
    print("-" * 70)
    
    first_ts = time.time()
    
    # 第一次观测（system）
    memory.update(
        scene_id=scene_id,
        map_id=map_id,
        position_state=ps,
        feedback={
            "type": "FACT_SIGNAL",
            "claim_type": "road_blocked",
            "source": "system",
            "statement": "该路段疑似封闭",
        },
        now_ts=first_ts,
    )
    print("  ✅ 第一次事实信号（system）")
    
    # 第二次观测（vision）
    memory.update(
        scene_id=scene_id,
        map_id=map_id,
        position_state=ps,
        feedback={
            "type": "FACT_SIGNAL",
            "claim_type": "road_blocked",
            "source": "vision",
        },
        now_ts=first_ts + 0.4,
    )
    print("  ✅ 第二次事实信号（vision）")
    
    # 第三次观测（system）
    memory.update(
        scene_id=scene_id,
        map_id=map_id,
        position_state=ps,
        feedback={
            "type": "FACT_SIGNAL",
            "claim_type": "road_blocked",
            "source": "system",
        },
        now_ts=first_ts + 0.8,
    )
    print("  ✅ 第三次事实信号（system）")
    
    # 等待满足时间跨度要求
    time.sleep(0.3)
    
    # 第四次观测（确保时间跨度 >= 1.0 秒）
    memory.update(
        scene_id=scene_id,
        map_id=map_id,
        position_state=ps,
        feedback={
            "type": "FACT_SIGNAL",
            "claim_type": "road_blocked",
            "source": "system",
        },
        now_ts=first_ts + 1.1,
    )
    print("  ✅ 第四次事实信号（system，满足时间跨度）")
    print()
    
    print("4️⃣ FactCandidatePool：清理过期候选")
    print("-" * 70)
    
    expired_count = pool.cleanup_expired()
    print(f"  📊 清理过期候选数: {expired_count}")
    print()
    
    print("5️⃣ FactCandidatePool：获取 PROMOTABLE 候选")
    print("-" * 70)
    
    promotables = pool.fetch_promotables(cleanup_before=True)
    print(f"  📊 PROMOTABLE 候选数: {len(promotables)}")
    if promotables:
        c = promotables[0]
        print(f"  📊 候选状态: {c.status}")
        print(f"  📊 confidence: {c.confidence:.2f}")
        print(f"  📊 support_count: {c.support_count}")
        print(f"  📊 unique_sources: {c.unique_sources}")
    print()
    
    print("6️⃣ LibraryRegistry：消费候选并入库")
    print("-" * 70)
    
    result = lib.update(active_scene_id=scene_id, position_state=ps)
    print(f"  ✅ 更新结果: {result}")
    print()
    
    print("7️⃣ LibraryRegistry：知识唤醒")
    print("-" * 70)
    
    hints = lib.get_hints(active_scene_id=scene_id, map_id=map_id)
    print(f"  📊 知识提示数: {len(hints)}")
    for h in hints:
        print(f"  • {h.statement} (confidence={h.confidence:.2f}, tags={h.tags})")
    print()
    
    print("=" * 70)
    print("✅ 演示完成")
    print("=" * 70)
    print()
    print("📁 数据库文件位置: artifacts/world_model/world_model.db")
    print("   可以使用 SQLite 工具查看：")
    print("   - experience_memories 表（体验记忆）")
    print("   - preferences 表（偏好）")
    print("   - fact_candidates 表（事实候选）")
    print("   - knowledge_items 表（知识条目）")


if __name__ == "__main__":
    main()


