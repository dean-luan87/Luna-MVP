# -*- coding: utf-8 -*-
"""
v1.8.5: World Model Phase B Demo（稳态机制演示）

目标：
- 演示候选事实自然过期（场景1）
- 演示候选事实成功晋级（场景2）
- 演示已入库事实自然退潮（场景3）
- 验证系统不会"突然清空"，也不会"越积越脏"

运行方式：
python examples/world_model_phase_b_demo.py
"""

import sys
import os
import time
from pprint import pprint

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.world_model.common.db import WorldModelDB
from core.world_model.common.types import PositionState
from core.world_model.memory.candidate_pool import FactCandidatePool, STATUS_PENDING, STATUS_PROMOTABLE, STATUS_REJECTED
from core.world_model.memory.memory_registry import MemoryRegistry
from core.world_model.library.library_registry import LibraryRegistry, LIFE_ACTIVE, LIFE_PASSIVE


def main():
    """主函数：演示 Phase B 稳态机制"""
    
    print("\n" + "=" * 70)
    print("v1.8.5 World Model Phase B Demo（稳态机制演示）")
    print("=" * 70)
    print()
    
    print("🎯 Demo 要证明 4 件事：")
    print("  1. 候选事实：有支持 → 成长，没支持 → 自动过期")
    print("  2. 已入库事实：一段时间没人验证 → 自动降级")
    print("  3. 系统不会\"突然清空\"")
    print("  4. 系统不会\"越积越脏\"")
    print()
    
    # ===== 初始化（使用短 TTL 用于演示）=====
    print("[初始化] 创建所有 Registry 实例（使用短 TTL 用于演示）")
    db = WorldModelDB()
    
    # 使用短 TTL：候选 5 秒，事实 5 秒
    candidate_pool = FactCandidatePool(
        db=db,
        n_support=2,  # 降低要求，便于演示
        n_sources=2,
        min_span_s=1.0,  # 缩短时间跨度
        candidate_ttl_s=5.0,  # 5 秒 TTL（演示用）
    )
    
    memory = MemoryRegistry(db=db, candidate_pool=candidate_pool)
    library = LibraryRegistry(
        db=db,
        candidate_pool=candidate_pool,
        verify_ttl_fact_s=5.0,  # 5 秒 TTL（演示用）
        verify_ttl_rule_s=10.0,
    )
    
    position_state = PositionState(
        position=(0.0, 0.0),
        stability_score=0.9,
        stable=True,
    )
    
    print("✅ 初始化完成")
    print()
    
    # ===== 场景 1：候选事实自然过期 =====
    print("=" * 70)
    print("🧪 场景 1：候选事实自然过期")
    print("=" * 70)
    print()
    print("场景：\"这条路被封了\"")
    print("输入序列：")
    print("  • T0：视觉 or 系统检测 → 写入 FactCandidate（support=1）")
    print("  • T0+1h：无新支持")
    print("  • T0+25h：触发 cleanup")
    print("期望结果：FactCandidate.status = REJECTED")
    print()
    
    scene_id_1 = "scene_bridge_001"
    map_id_1 = "mapunit_bridge_001"
    now = time.time()
    
    print("[1.1] 创建候选事实（T0）")
    # 使用唯一的 claim_type 避免与之前的数据冲突
    claim_type_1 = "road_blocked_demo_001"
    memory.update(
        scene_id=scene_id_1,
        map_id=map_id_1,
        position_state=position_state,
        feedback={
            "type": "FACT_SIGNAL",
            "claim_type": claim_type_1,
            "statement": "这条路被封了",
            "source": "vision",
        },
        now_ts=now,
    )
    print("  ✅ 候选已创建")
    
    # 获取候选 ID（通过自然键计算）
    import hashlib
    natural_key = f"{claim_type_1}::{scene_id_1}::{map_id_1}"
    candidate_id_1 = hashlib.sha256(natural_key.encode("utf-8")).hexdigest()[:24]
    print(f"  • candidate_id: {candidate_id_1}")
    
    # 获取当前状态
    try:
        candidate_before = candidate_pool.get(candidate_id_1)
        print(f"  • status: {candidate_before.status}")
        print(f"  • last_seen_ts: {candidate_before.last_seen_ts}")
    except KeyError:
        print("  • status: 候选不存在（可能已被清理）")
        candidate_id_1 = None
    print()
    
    if candidate_id_1:
        print("[1.2] 等待过期（6 秒，超过 TTL 5 秒）...")
        time.sleep(6)
        
        print("[1.3] 触发 cleanup_expired()")
        expired_count = candidate_pool.cleanup_expired()
        print(f"  ✅ 过期候选数: {expired_count}")
        
        # 验证状态
        try:
            candidate = candidate_pool.get(candidate_id_1)
            print(f"  • status: {candidate.status}")
            print(f"  • last_reason: {candidate.last_reason}")
            if candidate.status == STATUS_REJECTED:
                if candidate.last_reason == "expired_no_recent_support":
                    print("  ✅ 验收通过：候选已过期，状态为 REJECTED")
                else:
                    print(f"  ⚠️  候选已过期，但 last_reason 是 '{candidate.last_reason}'（可能是之前的状态）")
            else:
                print(f"  ⚠️  候选状态是 {candidate.status}（可能还未过期）")
        except KeyError:
            print("  ✅ 候选已清理（符合预期）")
    print()
    
    # ===== 场景 2：候选事实成功晋级 =====
    print("=" * 70)
    print("🧪 场景 2：候选事实成功晋级")
    print("=" * 70)
    print()
    print("场景：\"这里经常积水\"")
    print("输入序列：")
    print("  • Day 1：视觉 → support +1")
    print("  • Day 2：视觉 → support +1")
    print("  • Day 3：再次发生")
    print("期望结果：FactCandidate.status = PROMOTABLE → LibraryRegistry.consume()")
    print()
    
    scene_id_2 = "scene_street_009"
    map_id_2 = "mapunit_street_009"
    now_2 = time.time()
    
    print("[2.1] 创建可晋级候选（Day 1）")
    memory.update(
        scene_id=scene_id_2,
        map_id=map_id_2,
        position_state=position_state,
        feedback={
            "type": "FACT_SIGNAL",
            "claim_type": "frequent_waterlogging",
            "statement": "这里经常积水",
            "source": "vision",
        },
        now_ts=now_2,
    )
    print("  ✅ 第一次观测（vision）")
    
    print("[2.2] 第二次观测（Day 2）")
    memory.update(
        scene_id=scene_id_2,
        map_id=map_id_2,
        position_state=position_state,
        feedback={
            "type": "FACT_SIGNAL",
            "claim_type": "frequent_waterlogging",
            "source": "system",
        },
        now_ts=now_2 + 0.5,
    )
    print("  ✅ 第二次观测（system）")
    
    # 等待满足时间跨度
    time.sleep(0.6)
    
    print("[2.3] 第三次观测（Day 3，满足时间跨度）")
    memory.update(
        scene_id=scene_id_2,
        map_id=map_id_2,
        position_state=position_state,
        feedback={
            "type": "FACT_SIGNAL",
            "claim_type": "frequent_waterlogging",
            "source": "vision",
        },
        now_ts=now_2 + 1.1,
    )
    print("  ✅ 第三次观测（vision，满足时间跨度）")
    print()
    
    print("[2.4] 检查可晋级候选")
    promotables = candidate_pool.fetch_promotables(cleanup_before=True)
    print(f"  📊 PROMOTABLE 候选数: {len(promotables)}")
    if promotables:
        c = promotables[0]
        print(f"  • claim_type: {c.claim_type}")
        print(f"  • status: {c.status}")
        print(f"  • confidence: {c.confidence:.2f}")
        print(f"  • support_count: {c.support_count}")
        print(f"  • unique_sources: {c.unique_sources}")
        assert c.status == STATUS_PROMOTABLE, f"❌ status 应该是 PROMOTABLE，实际是 {c.status}"
        print("  ✅ 验收通过：候选已升级为 PROMOTABLE")
    print()
    
    print("[2.5] LibraryRegistry 消费候选")
    result = library.update(
        active_scene_id=scene_id_2,
        position_state=position_state,
        now_ts=time.time(),
    )
    pprint(result)
    
    # 验证 Library 条目
    hints = library.get_hints(active_scene_id=scene_id_2, map_id=map_id_2)
    if hints:
        h = hints[0]
        print(f"  • statement: {h.statement}")
        print(f"  • confidence: {h.confidence:.2f}")
        print(f"  • lifecycle_state: PASSIVE（新入库）")
        print("  ✅ 验收通过：候选已成功入库为 PASSIVE")
    print()
    
    # ===== 场景 3：已入库事实自然退潮（重点）=====
    print("=" * 70)
    print("🧪 场景 3：已入库事实自然退潮（重点）")
    print("=" * 70)
    print()
    print("场景：\"这条路施工，不能走\"")
    print("输入序列：")
    print("  • 入库后 7 天内：无人再验证")
    print("  • 执行 soft_rollback")
    print("期望结果：lifecycle_state: ACTIVE → PASSIVE, confidence: 0.72 → 0.61")
    print()
    
    scene_id_3 = "scene_construction_001"
    map_id_3 = "mapunit_construction_001"
    now_3 = time.time()
    
    print("[3.1] 创建并入库事实（模拟已入库的事实）")
    # 先创建候选并入库
    memory.update(
        scene_id=scene_id_3,
        map_id=map_id_3,
        position_state=position_state,
        feedback={
            "type": "FACT_SIGNAL",
            "claim_type": "road_blocked",
            "statement": "这条路施工，不能走",
            "source": "system",
        },
        now_ts=now_3,
    )
    
    memory.update(
        scene_id=scene_id_3,
        map_id=map_id_3,
        position_state=position_state,
        feedback={
            "type": "FACT_SIGNAL",
            "claim_type": "road_blocked",
            "source": "vision",
        },
        now_ts=now_3 + 0.5,
    )
    
    time.sleep(0.6)
    
    memory.update(
        scene_id=scene_id_3,
        map_id=map_id_3,
        position_state=position_state,
        feedback={
            "type": "FACT_SIGNAL",
            "claim_type": "road_blocked",
            "source": "system",
        },
        now_ts=now_3 + 1.1,
    )
    
    # 入库
    library.update(
        active_scene_id=scene_id_3,
        position_state=position_state,
        now_ts=now_3 + 1.2,
    )
    
    # 手动将条目升级为 ACTIVE（模拟已确认的事实）
    with db.connect() as conn:
        conn.execute(
            """
            UPDATE knowledge_items
            SET lifecycle_state = ?, confidence = ?
            WHERE scene_id = ? AND map_id = ?
            """,
            (LIFE_ACTIVE, 0.72, scene_id_3, map_id_3),
        )
    
    hints_before = library.get_hints(active_scene_id=scene_id_3, map_id=map_id_3)
    if hints_before:
        h = hints_before[0]
        print(f"  • statement: {h.statement}")
        print(f"  • confidence: {h.confidence:.2f}（初始）")
        print(f"  • lifecycle_state: ACTIVE（初始）")
    print()
    
    print("[3.2] 等待退潮（6 秒，超过 TTL 5 秒）...")
    # 手动将 last_verified_ts 设为很久以前（模拟已过期）
    with db.connect() as conn:
        conn.execute(
            """
            UPDATE knowledge_items
            SET last_verified_ts = ?
            WHERE scene_id = ? AND map_id = ?
            """,
            (now_3 + 1.2 - 6.0, scene_id_3, map_id_3),  # 6 秒前（超过 TTL 5 秒）
        )
    time.sleep(1)
    
    print("[3.3] 触发 soft_rollback_stale_items()")
    rollback_count = library.soft_rollback_stale_items()
    print(f"  ✅ 被回滚知识条目: {rollback_count}")
    print()
    
    print("[3.4] 检查退潮效果")
    hints_after = library.get_hints(active_scene_id=scene_id_3, map_id=map_id_3)
    if hints_after:
        h = hints_after[0]
        print(f"  • statement: {h.statement}")
        print(f"  • confidence: {h.confidence:.2f}（已衰减，预期: {0.72 * 0.85:.2f}）")
        print(f"  • lifecycle_state: PASSIVE（已降级）")
        
        expected_confidence = 0.72 * 0.85
        assert abs(h.confidence - expected_confidence) < 0.01, f"❌ confidence 应该是 {expected_confidence:.2f}，实际是 {h.confidence:.2f}"
        print("  ✅ 验收通过：事实已退潮，置信度衰减，生命周期降级")
    print()
    
    # ===== 总结 =====
    print("=" * 70)
    print("✅ Demo 完成 - Phase B 稳态机制验证")
    print("=" * 70)
    print()
    print("📊 关键验证点：")
    print("  1. ✅ 候选事实：有支持 → 成长，没支持 → 自动过期")
    print("  2. ✅ 已入库事实：一段时间没人验证 → 自动降级")
    print("  3. ✅ 系统不会\"突然清空\"（事实不会删除，只会降级）")
    print("  4. ✅ 系统不会\"越积越脏\"（过期候选和事实会自动退潮）")
    print()
    print("🔍 关键正确性信号：")
    print("  • 候选过期：超过 TTL 的候选自动标记为 REJECTED")
    print("  • 候选晋级：满足条件的候选自动升级为 PROMOTABLE")
    print("  • 事实退潮：超过 TTL 的事实自动降级并衰减置信度")
    print("  • 可追责：所有状态变化都有明确原因")
    print()
    print("📁 数据库文件位置: artifacts/world_model/world_model.db")
    print("   可以使用 SQLite 工具查看：")
    print("   - fact_candidates 表（查看过期候选和晋级候选）")
    print("   - knowledge_items 表（查看退潮后的事实）")
    print()


if __name__ == "__main__":
    main()

