"""
C1 功能测试（单元级）

测试 C1 的核心功能：
- 晃动暂停
- 隐私关闭
- 状态切换
- 决策逻辑
"""

import sys
import os
import time

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from c1_controller import C1Controller, C1Input, C1State


def test_c1_suspended_on_heavy_motion():
    """
    测试：晃动暂停
    
    当 motion_score 超过阈值时，应该暂停视觉。
    """
    print("\n[测试] 晃动暂停")
    c1 = C1Controller()
    
    input_signal = C1Input(
        timestamp=time.time(),
        motion_score=0.95,  # 超过阈值 0.85
        frame_diff_score=0.1,
        privacy_zone=None,
        user_camera_override=False,
    )
    
    decision = c1.decide(input_signal)
    
    assert decision.allow_frame is False, "❌ 严重晃动应该禁止抽帧"
    assert decision.target_fps == 0, "❌ 严重晃动 fps 应该是 0"
    assert decision.reason == "suspended", "❌ 原因应该是 suspended"
    
    print("  ✅ 测试通过")


def test_c1_privacy_block():
    """
    测试：隐私关闭
    
    当 privacy_zone 为 Class C 时，应该关闭视觉。
    """
    print("\n[测试] 隐私关闭（Class C）")
    c1 = C1Controller()
    
    input_signal = C1Input(
        timestamp=time.time(),
        motion_score=0.1,
        frame_diff_score=0.3,
        privacy_zone="C",  # Class C
        user_camera_override=False,
    )
    
    decision = c1.decide(input_signal)
    
    assert decision.allow_frame is False, "❌ Class C 隐私区域应该禁止抽帧"
    assert decision.target_fps == 0, "❌ Class C 隐私区域 fps 应该是 0"
    assert decision.reason == "privacy_guard", "❌ 原因应该是 privacy_guard"
    
    print("  ✅ 测试通过")


def test_c1_privacy_block_class_b():
    """
    测试：隐私关闭（Class B，用户不可强开）
    
    当 privacy_zone 为 Class B 时，即使 user_camera_override=True，也应该关闭视觉。
    """
    print("\n[测试] 隐私关闭（Class B，用户不可强开）")
    c1 = C1Controller()
    
    input_signal = C1Input(
        timestamp=time.time(),
        motion_score=0.1,
        frame_diff_score=0.3,
        privacy_zone="B",  # Class B
        user_camera_override=True,  # 即使用户强制开启，也不允许
    )
    
    decision = c1.decide(input_signal)
    
    assert decision.allow_frame is False, "❌ Class B 隐私区域应该禁止抽帧（即使 user_camera_override=True）"
    assert decision.target_fps == 0, "❌ Class B 隐私区域 fps 应该是 0"
    
    print("  ✅ 测试通过")


def test_c1_alert_state():
    """
    测试：ALERT 状态
    
    当 risk_hint 存在时，应该进入 ALERT 状态。
    """
    print("\n[测试] ALERT 状态")
    c1 = C1Controller()
    
    input_signal = C1Input(
        timestamp=time.time(),
        motion_score=0.2,
        frame_diff_score=0.6,
        risk_hint="检测到水边",
    )
    
    decision = c1.decide(input_signal)
    
    assert decision.allow_frame is True, "❌ ALERT 状态应该允许抽帧"
    assert decision.target_fps > 0, "❌ ALERT 状态应该有 fps"
    assert decision.priority == "safety", "❌ ALERT 状态优先级应该是 safety"
    assert decision.reason == "alert", "❌ 原因应该是 alert"
    
    print("  ✅ 测试通过")


def test_c1_transition_state():
    """
    测试：TRANSITION 状态
    
    当 next_scene_hint 存在时，应该进入 TRANSITION 状态。
    """
    print("\n[测试] TRANSITION 状态")
    c1 = C1Controller()
    
    input_signal = C1Input(
        timestamp=time.time(),
        motion_score=0.2,
        frame_diff_score=0.6,
        next_scene_hint="即将进入商场",
    )
    
    decision = c1.decide(input_signal)
    
    assert decision.allow_frame is True, "❌ TRANSITION 状态应该允许抽帧"
    assert decision.target_fps > 0, "❌ TRANSITION 状态应该有 fps"
    assert decision.priority == "navigation", "❌ TRANSITION 状态优先级应该是 navigation"
    assert decision.reason == "transition", "❌ 原因应该是 transition"
    
    print("  ✅ 测试通过")


def test_c1_stable_state():
    """
    测试：STABLE 状态
    
    默认状态应该是 STABLE。
    """
    print("\n[测试] STABLE 状态")
    c1 = C1Controller()
    
    input_signal = C1Input(
        timestamp=time.time(),
        motion_score=0.1,
        frame_diff_score=0.3,
    )
    
    decision = c1.decide(input_signal)
    
    assert decision.allow_frame is True, "❌ STABLE 状态应该允许抽帧"
    assert decision.target_fps > 0, "❌ STABLE 状态应该有 fps"
    assert decision.priority == "environment", "❌ STABLE 状态优先级应该是 environment"
    assert decision.reason == "stable", "❌ 原因应该是 stable"
    
    print("  ✅ 测试通过")


def run_all_tests():
    """
    运行所有功能测试
    """
    print("=" * 70)
    print("C1 功能测试（单元级）")
    print("=" * 70)
    
    test_c1_suspended_on_heavy_motion()
    test_c1_privacy_block()
    test_c1_privacy_block_class_b()
    test_c1_alert_state()
    test_c1_transition_state()
    test_c1_stable_state()
    
    print("\n" + "=" * 70)
    print("✅ 所有功能测试通过")
    print("=" * 70)


if __name__ == "__main__":
    run_all_tests()


