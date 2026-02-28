# -*- coding: utf-8 -*-
"""
v1.8.5: FactCandidatePool TTL 测试

验收点：
- 插入一个 PENDING 候选
- 手动把 last_seen_ts 改成很久以前
- cleanup_expired() 后状态变 REJECTED
"""

import sys
import os
import time
import sqlite3

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from core.world_model.common.db import WorldModelDB
from core.world_model.memory.candidate_pool import FactCandidatePool, STATUS_PENDING, STATUS_REJECTED


def test_candidate_ttl():
    """测试候选过期机制"""
    
    print("=" * 70)
    print("FactCandidatePool TTL 测试")
    print("=" * 70)
    print()
    
    # 初始化
    db = WorldModelDB()
    pool = FactCandidatePool(db=db, candidate_ttl_s=10.0)  # 10 秒 TTL（测试用）
    
    scene_id = "test_scene_001"
    map_id = "test_map_001"
    scope = {"scene_id": scene_id, "map_id": map_id}
    
    # Step 1: 插入一个 PENDING 候选
    print("[1] 插入一个 PENDING 候选")
    candidate = pool.upsert_observation(
        claim_type="test_claim",
        scene_id=scene_id,
        map_id=map_id,
        scope=scope,
        source="system",
        statement="测试声明",
        now_ts=time.time(),
    )
    print(f"  ✅ 候选已创建: {candidate.candidate_id}")
    print(f"  • status: {candidate.status}")
    print(f"  • last_seen_ts: {candidate.last_seen_ts}")
    print()
    
    # Step 2: 手动把 last_seen_ts 改成很久以前
    print("[2] 手动把 last_seen_ts 改成很久以前（超过 TTL）")
    old_ts = time.time() - 20.0  # 20 秒前（超过 10 秒 TTL）
    
    with db.connect() as conn:
        conn.execute(
            "UPDATE fact_candidates SET last_seen_ts=? WHERE candidate_id=?",
            (old_ts, candidate.candidate_id),
        )
    print(f"  ✅ last_seen_ts 已更新为: {old_ts}")
    print()
    
    # Step 3: cleanup_expired() 后状态变 REJECTED
    print("[3] 调用 cleanup_expired()")
    expired_count = pool.cleanup_expired()
    print(f"  ✅ 清理过期候选数: {expired_count}")
    print()
    
    # Step 4: 验证状态
    print("[4] 验证状态")
    updated_candidate = pool.get(candidate.candidate_id)
    print(f"  • status: {updated_candidate.status}")
    print(f"  • last_reason: {updated_candidate.last_reason}")
    print()
    
    # 验收点
    assert updated_candidate.status == STATUS_REJECTED, f"❌ status 应该是 REJECTED，实际是 {updated_candidate.status}"
    assert updated_candidate.last_reason == "expired_no_recent_support", f"❌ last_reason 应该是 'expired_no_recent_support'"
    
    print("=" * 70)
    print("✅ 测试通过：候选过期机制正常工作")
    print("=" * 70)
    print()


if __name__ == "__main__":
    test_candidate_ttl()


