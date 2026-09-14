#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速测试 Gate Hysteresis 修复是否生效
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from vision_pipeline.b2.v03.gate.gate_evaluator_v05 import GateEvaluatorV05

def test_hysteresis():
    """测试 Hysteresis 逻辑"""
    evaluator = GateEvaluatorV05()
    
    print("=== Gate Hysteresis 修复验证测试 ===\n")
    
    # 测试 1: 从 READ_ONLY 进入 ACTIVE（需要连续满足条件）
    print("测试 1: READ_ONLY → ACTIVE (需要连续满足条件)")
    evaluator.state.last_mode = "READ_ONLY"
    evaluator.state.residence_frames = 0
    evaluator.state.cooldown_remaining = 0
    
    for i in range(10):
        mode, reason, trace = evaluator.evaluate(
            stability_score=0.70,  # 高于 enter_threshold (0.65)
            range_m=5.0,
            visibility_score=0.8,
            evidence_ok=True,
            frame_id=i
        )
        transition = trace.get("runtime_profile", {}).get("transition", {})
        print(f"  帧 {i}: mode={mode}, switched={transition.get('switched')}, "
              f"residence={transition.get('residence_frames')}, "
              f"cooldown={transition.get('cooldown_remaining')}, "
              f"blocked_by={transition.get('blocked_by')}")
        if mode == "ACTIVE":
            print(f"  ✅ 成功进入 ACTIVE (第 {i+1} 帧)")
            break
    
    print()
    
    # 测试 2: 从 ACTIVE 退出（需要连续不满足条件）
    print("测试 2: ACTIVE → READ_ONLY (需要连续不满足条件)")
    evaluator.state.last_mode = "ACTIVE"
    evaluator.state.residence_frames = 25  # 已满足 min_hold
    evaluator.state.cooldown_remaining = 0
    
    for i in range(15):
        mode, reason, trace = evaluator.evaluate(
            stability_score=0.50,  # 低于 exit_threshold (0.55)
            range_m=5.0,
            visibility_score=0.8,
            evidence_ok=True,
            frame_id=i+10
        )
        transition = trace.get("runtime_profile", {}).get("transition", {})
        print(f"  帧 {i+10}: mode={mode}, switched={transition.get('switched')}, "
              f"residence={transition.get('residence_frames')}, "
              f"blocked_by={transition.get('blocked_by')}")
        if mode == "READ_ONLY":
            print(f"  ✅ 成功退出 ACTIVE (第 {i+11} 帧)")
            break
    
    print()
    
    # 测试 3: Min-hold 阻止切换
    print("测试 3: Min-hold 阻止切换")
    evaluator.state.last_mode = "ACTIVE"
    evaluator.state.residence_frames = 5  # 未满足 min_hold (需要 20 帧)
    evaluator.state.cooldown_remaining = 0
    
    mode, reason, trace = evaluator.evaluate(
        stability_score=0.50,  # 应该退出 ACTIVE
        range_m=5.0,
        visibility_score=0.8,
        evidence_ok=True,
        frame_id=25
    )
    transition = trace.get("runtime_profile", {}).get("transition", {})
    counters = trace.get("runtime_profile", {}).get("counters", {})
    
    print(f"  期望: READ_ONLY, 实际: {mode}")
    print(f"  switched: {transition.get('switched')}")
    print(f"  blocked_by: {transition.get('blocked_by')}")
    print(f"  min_hold_hits: {counters.get('min_hold_hits', 0)}")
    
    if transition.get('blocked_by') == 'min_hold':
        print(f"  ✅ Min-hold 机制正常工作")
    else:
        print(f"  ⚠️  Min-hold 未生效")
    
    print()
    
    # 测试 4: Cooldown 阻止切换
    print("测试 4: Cooldown 阻止切换")
    evaluator.state.last_mode = "ACTIVE"
    evaluator.state.residence_frames = 25  # 已满足 min_hold
    evaluator.state.cooldown_remaining = 10  # 仍有冷却
    
    mode, reason, trace = evaluator.evaluate(
        stability_score=0.50,  # 应该退出 ACTIVE
        range_m=5.0,
        visibility_score=0.8,
        evidence_ok=True,
        frame_id=26
    )
    transition = trace.get("runtime_profile", {}).get("transition", {})
    counters = trace.get("runtime_profile", {}).get("counters", {})
    
    print(f"  期望: READ_ONLY, 实际: {mode}")
    print(f"  switched: {transition.get('switched')}")
    print(f"  blocked_by: {transition.get('blocked_by')}")
    print(f"  cooldown_remaining: {transition.get('cooldown_remaining')}")
    print(f"  cooldown_hits: {counters.get('cooldown_hits', 0)}")
    
    if transition.get('blocked_by') == 'cooldown':
        print(f"  ✅ Cooldown 机制正常工作")
    else:
        print(f"  ⚠️  Cooldown 未生效")
    
    print()
    print("=== 测试完成 ===")
    print(f"最终 counters:")
    print(f"  hysteresis_hold_hits: {counters.get('hysteresis_hold_hits', 0)}")
    print(f"  min_hold_hits: {counters.get('min_hold_hits', 0)}")
    print(f"  cooldown_hits: {counters.get('cooldown_hits', 0)}")

if __name__ == "__main__":
    test_hysteresis()
