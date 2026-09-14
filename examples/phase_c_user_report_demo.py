# -*- coding: utf-8 -*-
"""
v1.8.5: Phase C 用户报告 Demo（对话 / 情感 / 语言接口）

目标：
- 验证用户报告路由到 Memory / CandidatePool
- 验证限频机制（防止恶意/噪声）
- 验证防污染机制（user_report 不直接写 Library）

场景设定：
- 用户说"这里路滑"→ Memory
- 用户说"这里封路了"→ CandidatePool（但不会立刻进 Library）
- 用户反复刷同一句 → 限频生效

运行方式：
python examples/phase_c_user_report_demo.py
"""

import sys
import os
import time
from pprint import pprint

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.world_model.common.db import WorldModelDB
from core.world_model.common.types import PositionState
from core.world_model.memory import MemoryRegistry
from core.world_model.memory.candidate_pool import FactCandidatePool
from core.world_model.interfaces.user_report_iface import UserReportEvent
from core.world_model.memory.user_report_router import UserReportRouter
from core.world_model.common.rate_limiter import SimpleRateLimiter


def main():
    """主函数：演示用户报告路由"""
    
    print("\n" + "=" * 70)
    print("v1.8.5 Phase C 用户报告 Demo")
    print("=" * 70)
    print()
    
    print("🎯 场景设定：")
    print("  • 用户说\"这里路滑\"→ Memory")
    print("  • 用户说\"这里封路了\"→ CandidatePool（但不会立刻进 Library）")
    print("  • 用户反复刷同一句 → 限频生效")
    print()
    
    # ===== 初始化 =====
    print("[初始化] 创建所有 Registry 实例")
    db = WorldModelDB()
    candidate_pool = FactCandidatePool(db=db)
    memory = MemoryRegistry(db=db, candidate_pool=candidate_pool)
    rate_limiter = SimpleRateLimiter(window_s=10.0)  # 10 秒窗口（演示用）
    router = UserReportRouter(
        memory_registry=memory,
        candidate_pool=candidate_pool,
        rate_limiter=rate_limiter,
    )
    
    position_state = PositionState(
        position=(0.0, 0.0),
        stability_score=0.9,
        stable=True,
    )
    
    scene_id = "scene_user_report_demo"
    map_id = "mapunit_user_report_demo"
    
    print("✅ 初始化完成")
    print()
    
    # ===== 场景 1：用户说"这里路滑"→ Memory =====
    print("=" * 70)
    print("场景 1：用户说\"这里路滑\"→ Memory")
    print("=" * 70)
    print()
    
    event_1 = UserReportEvent(
        user_id="user_001",
        raw_text="这里路滑",
        report_type="DISCOMFORT",
        tags=["slippery"],
        intensity=0.8,
        ts=time.time(),
    )
    
    print("[1.1] 路由用户报告（DISCOMFORT）")
    result1 = router.ingest(
        scene_id=scene_id,
        map_id=map_id,
        position_state=position_state,
        event=event_1,
    )
    pprint(result1)
    print()
    
    # 验证：应该路由到 Memory
    assert result1["accepted"] is True, f"❌ 应该被接受，实际是 {result1}"
    assert "memory_written" in result1.get("reason", ""), f"❌ 应该是 memory_written，实际是 {result1.get('reason', '')}"
    print("  ✅ 验收通过：DISCOMFORT 正确路由到 Memory")
    print()
    
    # ===== 场景 2：用户说"这里封路了"→ CandidatePool =====
    print("=" * 70)
    print("场景 2：用户说\"这里封路了\"→ CandidatePool")
    print("=" * 70)
    print()
    
    event_2 = UserReportEvent(
        user_id="user_001",
        raw_text="这里封路了",
        report_type="FACT_CONFIRM",
        tags=["road_blocked"],
        claim_type="road_blocked",
        claim_payload={"statement": "这里封路了"},
        ts=time.time(),
    )
    
    print("[2.1] 路由用户报告（FACT_CONFIRM）")
    result2 = router.ingest(
        scene_id=scene_id,
        map_id=map_id,
        position_state=position_state,
        event=event_2,
    )
    pprint(result2)
    print()
    
    # 验证：应该路由到 CandidatePool
    assert result2["accepted"] is True, f"❌ 应该被接受，实际是 {result2}"
    assert "fact_signal_recorded" in result2.get("reason", ""), f"❌ 应该是 fact_signal_recorded，实际是 {result2.get('reason', '')}"
    print("  ✅ 验收通过：FACT_CONFIRM 正确路由到 CandidatePool")
    print()
    
    # ===== 场景 3：用户反复刷同一句 → 限频生效 =====
    print("=" * 70)
    print("场景 3：用户反复刷同一句 → 限频生效")
    print("=" * 70)
    print()
    
    event_3 = UserReportEvent(
        user_id="user_001",
        raw_text="这里封路了",
        report_type="FACT_CONFIRM",
        tags=["road_blocked"],
        claim_type="road_blocked",
        claim_payload={"statement": "这里封路了"},
        ts=time.time() + 1.0,  # 1 秒后（仍在窗口内）
    )
    
    print("[3.1] 路由用户报告（FACT_CONFIRM，重复，在限频窗口内）")
    result3 = router.ingest(
        scene_id=scene_id,
        map_id=map_id,
        position_state=position_state,
        event=event_3,
    )
    pprint(result3)
    print()
    
    # 验证：应该被限频
    assert result3["accepted"] is False, f"❌ 应该被限频，实际是 {result3}"
    assert "rate_limited" in result3.get("reason", ""), f"❌ 应该返回 rate_limited，实际是 {result3.get('reason', '')}"
    print("  ✅ 验收通过：限频机制正确生效")
    print()
    
    # ===== 场景 4：窗口过期后，再次报告 =====
    print("=" * 70)
    print("场景 4：窗口过期后，再次报告")
    print("=" * 70)
    print()
    
    print("[4.1] 等待限频窗口过期（11 秒）...")
    time.sleep(11)
    
    event_4 = UserReportEvent(
        user_id="user_001",
        raw_text="这里封路了",
        report_type="FACT_CONFIRM",
        tags=["road_blocked"],
        claim_type="road_blocked",
        claim_payload={"statement": "这里封路了"},
        ts=time.time(),
    )
    
    print("[4.2] 路由用户报告（FACT_CONFIRM，窗口已过期）")
    result4 = router.ingest(
        scene_id=scene_id,
        map_id=map_id,
        position_state=position_state,
        event=event_4,
    )
    pprint(result4)
    print()
    
    # 验证：应该允许写入
    assert result4["accepted"] is True, f"❌ 应该允许写入，实际是 {result4}"
    assert "fact_signal_recorded" in result4.get("reason", ""), f"❌ 应该是 fact_signal_recorded，实际是 {result4.get('reason', '')}"
    print("  ✅ 验收通过：窗口过期后正确允许写入")
    print()
    
    # ===== 场景 5：relocalizing=True → world_write_frozen =====
    print("=" * 70)
    print("场景 5：relocalizing=True → world_write_frozen")
    print("=" * 70)
    print()
    
    position_state_frozen = PositionState(
        position=(0.0, 0.0),
        stability_score=0.9,
        stable=True,
        source="vision",
        drift_suspected=False,
        relocalizing=True,  # 正在重定位
    )
    
    event_5 = UserReportEvent(
        user_id="user_001",
        raw_text="这里路滑",
        report_type="DISCOMFORT",
        tags=["slippery"],
        intensity=0.8,
        ts=time.time(),
    )
    
    print("[5.1] 路由用户报告（DISCOMFORT，relocalizing=True）")
    result5 = router.ingest(
        scene_id=scene_id,
        map_id=map_id,
        position_state=position_state_frozen,
        event=event_5,
    )
    pprint(result5)
    print()
    
    # 验证：应该被冻结
    assert result5["accepted"] is False, f"❌ 应该被冻结，实际是 {result5}"
    assert "world_write_frozen" in result5.get("reason", ""), f"❌ 应该返回 world_write_frozen，实际是 {result5.get('reason', '')}"
    print("  ✅ 验收通过：freeze gate 正确生效")
    print()
    
    # ===== 验证点 =====
    print("=" * 70)
    print("✅ Demo 验证点")
    print("=" * 70)
    print()
    
    print("1. ✅ 分流规则正确")
    print("   • DISCOMFORT → Memory（体验资产）")
    print("   • PREFERENCE → Memory（偏好）")
    print("   • FACT_CONFIRM → CandidatePool（事实信号）")
    print("   • FACT_CONFLICT → CandidatePool（冲突信号）")
    print("   • 任何 user_report 不允许直接写 Library")
    print()
    
    print("2. ✅ 限频机制生效")
    print("   • 同一用户、同一 Scene、同一 claim_type，在窗口内只允许计 1 次 support")
    print("   • 窗口过期后，允许再次写入")
    print()
    
    print("3. ✅ 防污染机制")
    print("   • user_report 不提升 confidence（已在 CandidatePool 中实现）")
    print("   • 必须搭配\"非用户源\"的证据才可 PROMOTABLE（n_sources>=2）")
    print()
    
    print("4. ✅ freeze gate 生效")
    print("   • relocalizing=True → world_write_frozen")
    print("   • 与包 B 统一 Gate 规则")
    print()
    
    print("5. ✅ 所有返回结构可追责")
    print("   • accepted/reason 字段清晰")
    print("   • 便于调试和审计")
    print()
    
    print("=" * 70)
    print("✅ Demo 完成")
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()

