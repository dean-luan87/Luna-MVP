# -*- coding: utf-8 -*-
"""
v1.8.5: LibraryRegistry 软回滚测试

验收点：
- 插入一个 ACTIVE item，last_verified_ts 很久以前
- 调 soft_rollback_stale_items()
- lifecycle 变 PASSIVE，confidence *0.85
"""

import sys
import os
import time
import json

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from core.world_model.common.db import WorldModelDB
from core.world_model.memory.candidate_pool import FactCandidatePool
from core.world_model.library.library_registry import LibraryRegistry, LIFE_ACTIVE, LIFE_PASSIVE
from core.world_model.library.schemas import ITEM_FACT, SCHEMA_VERSION


def test_library_rollback():
    """测试 Library 软回滚机制"""
    
    print("=" * 70)
    print("LibraryRegistry 软回滚测试")
    print("=" * 70)
    print()
    
    # 初始化
    db = WorldModelDB()
    pool = FactCandidatePool(db=db)
    library = LibraryRegistry(db=db, candidate_pool=pool, verify_ttl_fact_s=10.0)  # 10 秒 TTL（测试用）
    
    scene_id = "test_scene_001"
    map_id = "test_map_001"
    scope = {"scene_id": scene_id, "map_id": map_id}
    
    # Step 1: 插入一个 ACTIVE item，last_verified_ts 很久以前
    print("[1] 插入一个 ACTIVE item，last_verified_ts 很久以前")
    old_ts = time.time() - 20.0  # 20 秒前（超过 10 秒 TTL）
    item_id = "test_item_001"
    original_confidence = 0.8
    
    with db.connect() as conn:
        conn.execute(
            """
            INSERT OR REPLACE INTO knowledge_items(
              item_id, item_type, scene_id, map_id, scope_json, statement,
              tags_json, confidence, lifecycle_state, source_set_json, evidence_refs_json,
              valid_from_ts, valid_to_ts, last_verified_ts, schema_version
            ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """,
            (
                item_id, ITEM_FACT, scene_id, map_id,
                json.dumps(scope, ensure_ascii=False),
                "测试事实",
                json.dumps(["test_tag"], ensure_ascii=False),
                original_confidence,
                LIFE_ACTIVE,
                json.dumps(["system"], ensure_ascii=False),
                json.dumps([], ensure_ascii=False),
                old_ts, None, old_ts, SCHEMA_VERSION,
            ),
        )
    print(f"  ✅ 知识条目已创建: {item_id}")
    print(f"  • lifecycle_state: {LIFE_ACTIVE}")
    print(f"  • confidence: {original_confidence}")
    print(f"  • last_verified_ts: {old_ts}")
    print()
    
    # Step 2: 调 soft_rollback_stale_items()
    print("[2] 调用 soft_rollback_stale_items()")
    rollback_count = library.soft_rollback_stale_items()
    print(f"  ✅ 回滚条目数: {rollback_count}")
    print()
    
    # Step 3: 验证状态
    print("[3] 验证状态")
    with db.connect() as conn:
        row = conn.execute(
            "SELECT lifecycle_state, confidence FROM knowledge_items WHERE item_id=?",
            (item_id,),
        ).fetchone()
    
    new_lifecycle = row["lifecycle_state"]
    new_confidence = float(row["confidence"])
    expected_confidence = original_confidence * 0.85
    
    print(f"  • lifecycle_state: {new_lifecycle}")
    print(f"  • confidence: {new_confidence:.2f} (原始: {original_confidence:.2f}, 预期: {expected_confidence:.2f})")
    print()
    
    # 验收点
    assert new_lifecycle == LIFE_PASSIVE, f"❌ lifecycle_state 应该是 PASSIVE，实际是 {new_lifecycle}"
    assert abs(new_confidence - expected_confidence) < 0.01, f"❌ confidence 应该是 {expected_confidence:.2f}，实际是 {new_confidence:.2f}"
    
    print("=" * 70)
    print("✅ 测试通过：Library 软回滚机制正常工作")
    print("=" * 70)
    print()


if __name__ == "__main__":
    test_library_rollback()


