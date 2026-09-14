# -*- coding: utf-8 -*-
"""
v1.8.5: World Model Library 最小可跑示例

目标：
- 验证 FactCandidatePool → LibraryRegistry 闭环
- 验证可追责、可回归的事实链路

运行方式：
python examples/world_model_library_demo.py
"""

import sys
import os
import time

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.world_model.common.db import WorldModelDB
from core.world_model.common.types import PositionState
from core.world_model.memory.candidate_pool import FactCandidatePool
from core.world_model.library.library_registry import LibraryRegistry


def main():
    """主函数：演示 FactCandidatePool → LibraryRegistry 闭环"""
    
    print("=" * 70)
    print("World Model Library 闭环演示")
    print("=" * 70)
    print()
    
    # 初始化
    db = WorldModelDB()
    # demo 缩短时间（实际应为 30 分钟）
    pool = FactCandidatePool(db=db, n_support=3, n_sources=2, min_span_s=1.0)
    lib = LibraryRegistry(db=db, candidate_pool=pool)
    
    scene_id = "scene_crossing_001"
    map_id = "map_unit_001"
    scope = {"scene_id": scene_id, "map_id": map_id}
    
    print("1️⃣ 三次观测：system + vision（满足 sources=2, support=3），span=1s")
    print("-" * 70)
    
    # 第一次观测（system）
    first_ts = time.time()
    pool.upsert_observation(
        "road_blocked",
        scene_id,
        map_id,
        scope,
        source="system",
        statement="该路段疑似封闭",
        now_ts=first_ts
    )
    print("  ✅ 第一次观测（system）")
    
    # 第二次观测（vision）- 间隔 0.4 秒
    second_ts = first_ts + 0.4
    pool.upsert_observation(
        "road_blocked",
        scene_id,
        map_id,
        scope,
        source="vision",
        now_ts=second_ts
    )
    print("  ✅ 第二次观测（vision）")
    
    # 第三次观测（system）- 间隔 0.4 秒（总跨度 0.8 秒，仍不够 1.0 秒）
    third_ts = first_ts + 0.8
    pool.upsert_observation(
        "road_blocked",
        scene_id,
        map_id,
        scope,
        source="system",
        now_ts=third_ts
    )
    print("  ✅ 第三次观测（system）")
    
    # 等待满足时间跨度要求（1.0 秒）
    time.sleep(0.3)
    
    # 第四次观测（确保时间跨度 >= 1.0 秒）
    fourth_ts = first_ts + 1.1
    pool.upsert_observation(
        "road_blocked",
        scene_id,
        map_id,
        scope,
        source="system",
        now_ts=fourth_ts
    )
    print("  ✅ 第四次观测（system，满足时间跨度）")
    print()
    
    # 检查候选状态
    promotables = pool.fetch_promotables()
    print(f"  📊 PROMOTABLE 候选数: {len(promotables)}")
    if promotables:
        c = promotables[0]
        print(f"  📊 候选状态: {c.status}")
        print(f"  📊 confidence: {c.confidence:.2f}")
        print(f"  📊 support_count: {c.support_count}")
        print(f"  📊 unique_sources: {c.unique_sources}")
    print()
    
    print("2️⃣ LibraryRegistry 消费候选并入库")
    print("-" * 70)
    
    ps = PositionState(position=(0.0, 0.0), stability_score=0.9, stable=True)
    result = lib.update(active_scene_id=scene_id, position_state=ps)
    print(f"  ✅ 更新结果: {result}")
    print()
    
    print("3️⃣ 知识唤醒（获取 LibraryHints）")
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
    print("   可以使用 SQLite 工具查看 fact_candidates 和 knowledge_items 表")


if __name__ == "__main__":
    main()

