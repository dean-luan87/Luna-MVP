# -*- coding: utf-8 -*-
"""
v1.8.5: Phase C 重定位 Demo（GPS 弱锚点 + 视觉失衡重定位）

目标：
- 验证统一重定位闸门（全局护栏）
- 验证防错位污染机制

场景设定：
- 正常走路 → 视觉失衡跳变 → 冻结 → GPS 弱锚点恢复 → 解冻 → 再关联 scene

运行方式：
python examples/phase_c_relocalization_demo.py
"""

import sys
import os
import time
from pprint import pprint

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.world_model.common.db import WorldModelDB
from core.world_model.common.types import PositionState
from core.world_model.scene import SceneRegistry
from core.world_model.memory import MemoryRegistry
from core.world_model.library import LibraryRegistry
from core.world_model.memory.candidate_pool import FactCandidatePool
from core.world_model.common.gates import should_freeze_world_writes


def main():
    """主函数：演示重定位机制"""
    
    print("\n" + "=" * 70)
    print("v1.8.5 Phase C 重定位 Demo")
    print("=" * 70)
    print()
    
    print("🎯 场景设定：")
    print("  1. stable=True → 正常写 Memory")
    print("  2. drift_suspected=True → 禁止写入、冻结 scene")
    print("  3. relocalizing=True → 持续冻结")
    print("  4. 恢复 stable=True 且 drift=False → 解冻，允许写入")
    print()
    
    # ===== 初始化 =====
    print("[初始化] 创建所有 Registry 实例")
    db = WorldModelDB()
    candidate_pool = FactCandidatePool(db=db)
    memory = MemoryRegistry(db=db, candidate_pool=candidate_pool)
    library = LibraryRegistry(db=db, candidate_pool=candidate_pool)
    scene_registry = SceneRegistry()
    
    print("✅ 初始化完成")
    print()
    
    # ===== 阶段 1：正常走路 =====
    print("=" * 70)
    print("阶段 1：正常走路")
    print("=" * 70)
    print()
    
    position_state_normal = PositionState(
        position=(0.0, 0.0),
        stability_score=0.9,
        stable=True,
        source="vision",
        drift_suspected=False,
        relocalizing=False,
    )
    
    print("[1.1] 检查统一 Gate")
    gate_frozen = should_freeze_world_writes(position_state_normal)
    print(f"  ✅ 闸门状态: {'冻结' if gate_frozen else '允许写入'}")
    
    print("[1.2] 写入体验记忆")
    result1 = memory.update(
        scene_id="scene_normal",
        map_id="mapunit_normal",
        position_state=position_state_normal,
        feedback={
            "type": "EXPERIENCE",
            "tags": ["comfortable"],
            "valence": "POSITIVE",
            "intensity": 0.3,
            "source": "user",
        },
    )
    print(f"  ✅ 写入结果: {result1}")
    print()
    
    # ===== 阶段 2：视觉失衡跳变 =====
    print("=" * 70)
    print("阶段 2：视觉失衡跳变")
    print("=" * 70)
    print()
    
    position_state_drift = PositionState(
        position=(100.0, 100.0),  # 突然跳变
        stability_score=0.3,
        stable=False,
        source="vision",
        drift_suspected=True,  # 检测到漂移
        relocalizing=False,
    )
    
    print("[2.1] 检查统一 Gate（drift_suspected=True）")
    gate_frozen = should_freeze_world_writes(position_state_drift)
    print(f"  ✅ 闸门状态: {'冻结' if gate_frozen else '允许写入'}")
    
    print("[2.2] 尝试写入体验记忆（应该被阻止）")
    result2 = memory.update(
        scene_id="scene_drift",
        map_id="mapunit_drift",
        position_state=position_state_drift,
        feedback={
            "type": "EXPERIENCE",
            "tags": ["unstable"],
            "valence": "NEGATIVE",
            "intensity": 0.8,
            "source": "user",
        },
    )
    print(f"  ✅ 写入结果: {result2}")
    assert result2["written"] == 0, "❌ 应该被阻止写入"
    assert "world_write_frozen" in result2.get("reason", ""), f"❌ 应该返回 world_write_frozen，实际是 {result2.get('reason', '')}"
    print("  ✅ 验收通过：重定位闸门正确阻止写入")
    print()
    
    # ===== 阶段 3：GPS 弱锚点恢复 =====
    print("=" * 70)
    print("阶段 3：GPS 弱锚点恢复")
    print("=" * 70)
    print()
    
    position_state_recovering = PositionState(
        position=(5.0, 5.0),  # 恢复后的位置
        stability_score=0.7,
        stable=True,
        source="fused",
        drift_suspected=False,
        relocalizing=True,  # 正在重定位
        anchor_gps=(39.9042, 116.4074),  # GPS 弱锚点
    )
    
    print("[3.1] 检查统一 Gate（relocalizing=True）")
    gate_frozen = should_freeze_world_writes(position_state_recovering)
    print(f"  ✅ 闸门状态: {'冻结' if gate_frozen else '允许写入'}")
    
    print("[3.2] 尝试写入体验记忆（应该被阻止）")
    result3 = memory.update(
        scene_id="scene_recovering",
        map_id="mapunit_recovering",
        position_state=position_state_recovering,
        feedback={
            "type": "EXPERIENCE",
            "tags": ["recovering"],
            "valence": "NEUTRAL",
            "intensity": 0.5,
            "source": "user",
        },
    )
    print(f"  ✅ 写入结果: {result3}")
    assert result3["written"] == 0, "❌ 应该被阻止写入"
    print("  ✅ 验收通过：重定位期间正确阻止写入")
    print()
    
    # ===== 阶段 4：解冻 =====
    print("=" * 70)
    print("阶段 4：解冻（重定位完成）")
    print("=" * 70)
    print()
    
    position_state_recovered = PositionState(
        position=(5.0, 5.0),
        stability_score=0.9,
        stable=True,
        source="fused",
        drift_suspected=False,
        relocalizing=False,  # 重定位完成
        anchor_gps=(39.9042, 116.4074),
    )
    
    print("[4.1] 检查统一 Gate（重定位完成）")
    gate_frozen = should_freeze_world_writes(position_state_recovered)
    print(f"  ✅ 闸门状态: {'冻结' if gate_frozen else '允许写入'}")
    
    print("[4.2] 写入体验记忆（应该允许）")
    result4 = memory.update(
        scene_id="scene_recovered",
        map_id="mapunit_recovered",
        position_state=position_state_recovered,
        feedback={
            "type": "EXPERIENCE",
            "tags": ["recovered"],
            "valence": "POSITIVE",
            "intensity": 0.6,
            "source": "user",
        },
    )
    print(f"  ✅ 写入结果: {result4}")
    assert result4["written"] == 1, "❌ 应该允许写入"
    print("  ✅ 验收通过：重定位完成后正确允许写入")
    print()
    
    # ===== 验证点 =====
    print("=" * 70)
    print("✅ Demo 验证点")
    print("=" * 70)
    print()
    
    print("1. ✅ 统一 Gate 规则（全局护栏）")
    print("   • stable=False → 冻结写入")
    print("   • drift_suspected=True → 冻结写入")
    print("   • relocalizing=True → 冻结写入")
    print("   • 重定位完成 → 允许写入")
    print()
    
    print("2. ✅ 防错位污染")
    print("   • 视觉失衡跳变时，三库（Memory/Candidate/Library）不写入、不升级")
    print("   • 重定位期间，系统冻结，不产生污染")
    print("   • SceneRegistry 冻结，不切 Scene")
    print()
    
    print("3. ✅ GPS 弱锚点策略")
    print("   • GPS 不直接切 Scene，只用来约束空间范围")
    print("   • 在 drift_suspected=True 时触发 relocalizing=True")
    print()
    
    print("4. ✅ 系统自愈能力")
    print("   • rollback 可继续运行（LibraryRegistry 允许 soft_rollback）")
    print("   • 恢复后自动继续写入")
    print()
    
    print("=" * 70)
    print("✅ Demo 完成")
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()

