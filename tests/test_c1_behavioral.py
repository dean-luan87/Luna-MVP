"""
C1 行为测试（连续帧）

测试 C1 的连续行为：
- 恢复机制
- 状态切换
- 决策连续性
"""

import sys
import os
import time

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from c1_controller import C1Controller, C1Input


def test_c1_resume_after_stable_frames():
    """
    测试：恢复机制
    
    连续晃动后，稳定帧应该能够恢复。
    """
    print("\n[测试] 恢复机制（连续晃动 → 稳定帧）")
    c1 = C1Controller()
    
    # 连续晃动
    for i in range(5):
        input_signal = C1Input(
            timestamp=time.time(),
            motion_score=0.9,  # 超过阈值
            frame_diff_score=0.8,
        )
        decision = c1.decide(input_signal)
        print(f"  晃动帧 {i+1}: allow_frame={decision.allow_frame}, reason={decision.reason}")
        assert decision.allow_frame is False, f"❌ 第 {i+1} 次晃动应该禁止抽帧"
    
    # 稳定帧
    decision = None
    for i in range(5):
        input_signal = C1Input(
            timestamp=time.time(),
            motion_score=0.1,  # 低于阈值
            frame_diff_score=0.3,
        )
        decision = c1.decide(input_signal)
        print(f"  稳定帧 {i+1}: allow_frame={decision.allow_frame}, reason={decision.reason}")
    
    assert decision is not None, "❌ 应该有决策结果"
    assert decision.allow_frame is True, "❌ 稳定后应该允许抽帧"
    assert decision.target_fps > 0, "❌ 稳定后应该有 fps"
    
    print("  ✅ 测试通过")


def test_c1_state_transition():
    """
    测试：状态切换
    
    从 STABLE → ALERT → STABLE 的状态切换。
    """
    print("\n[测试] 状态切换（STABLE → ALERT → STABLE）")
    c1 = C1Controller()
    
    # STABLE 状态
    input_1 = C1Input(
        timestamp=time.time(),
        motion_score=0.1,
        frame_diff_score=0.3,
    )
    decision_1 = c1.decide(input_1)
    print(f"  STABLE: allow_frame={decision_1.allow_frame}, priority={decision_1.priority}")
    assert decision_1.reason == "stable", "❌ 应该是 STABLE 状态"
    
    # ALERT 状态
    input_2 = C1Input(
        timestamp=time.time(),
        motion_score=0.2,
        frame_diff_score=0.6,
        risk_hint="检测到水边",
    )
    decision_2 = c1.decide(input_2)
    print(f"  ALERT: allow_frame={decision_2.allow_frame}, priority={decision_2.priority}")
    assert decision_2.reason == "alert", "❌ 应该是 ALERT 状态"
    assert decision_2.priority == "safety", "❌ ALERT 状态优先级应该是 safety"
    
    # 回到 STABLE 状态
    input_3 = C1Input(
        timestamp=time.time(),
        motion_score=0.1,
        frame_diff_score=0.3,
    )
    decision_3 = c1.decide(input_3)
    print(f"  STABLE: allow_frame={decision_3.allow_frame}, priority={decision_3.priority}")
    assert decision_3.reason == "stable", "❌ 应该回到 STABLE 状态"
    assert decision_3.priority == "environment", "❌ STABLE 状态优先级应该是 environment"
    
    print("  ✅ 测试通过")


def test_c1_decision_continuity():
    """
    测试：决策连续性
    
    相同输入应该产生相同的决策（状态机稳定性）。
    """
    print("\n[测试] 决策连续性（相同输入 → 相同决策）")
    c1 = C1Controller()
    
    input_signal = C1Input(
        timestamp=time.time(),
        motion_score=0.1,
        frame_diff_score=0.3,
    )
    
    # 连续 5 次相同输入
    decisions = []
    for i in range(5):
        decision = c1.decide(input_signal)
        decisions.append(decision)
        print(f"  第 {i+1} 次: allow_frame={decision.allow_frame}, target_fps={decision.target_fps}, reason={decision.reason}")
    
    # 所有决策应该相同
    for i in range(1, len(decisions)):
        assert decisions[i].allow_frame == decisions[0].allow_frame, f"❌ 第 {i+1} 次决策应该与第 1 次相同"
        assert decisions[i].target_fps == decisions[0].target_fps, f"❌ 第 {i+1} 次决策应该与第 1 次相同"
        assert decisions[i].reason == decisions[0].reason, f"❌ 第 {i+1} 次决策应该与第 1 次相同"
    
    print("  ✅ 测试通过")


def run_all_tests():
    """
    运行所有行为测试
    """
    print("=" * 70)
    print("C1 行为测试（连续帧）")
    print("=" * 70)
    
    test_c1_resume_after_stable_frames()
    test_c1_state_transition()
    test_c1_decision_continuity()
    
    print("\n" + "=" * 70)
    print("✅ 所有行为测试通过")
    print("=" * 70)


if __name__ == "__main__":
    run_all_tests()


