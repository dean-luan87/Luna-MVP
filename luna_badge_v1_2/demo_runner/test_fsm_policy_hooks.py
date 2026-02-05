"""
FSM Policy Hooks Test (v1.4.8 StepB-5)

测试 FSM 策略钩子
"""

import os
import sys
import time

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from navigation.fsm_policy_hooks import FSMPolicyHooks
from navigation.fsm_policy_state_store import FSMPolicyStateStore
from navigation.gps_gatekeeper import GPSMode
from navigation.gps_quality_monitor import GPSQuality


def test_scenario_1_vision_confirm_strong():
    """测试场景 1: 视角确认强 → pre_turn=6，allow_gps=False，prefer_lock=True"""
    print("=" * 60)
    print("测试场景 1: 视角确认强 → pre_turn=6，allow_gps=False，prefer_lock=True")
    print("=" * 60)
    
    events_received = []
    
    class MockEventBus:
        def subscribe(self, topic, handler):
            pass
        def publish(self, topic, event):
            events_received.append((topic, event))
    
    event_bus = MockEventBus()
    state_store = FSMPolicyStateStore(event_bus=event_bus)
    hooks = FSMPolicyHooks(state_store, event_bus=event_bus)
    
    # 模拟位置确认事件（高置信度，最近）
    state_store._on_position_confirmed({
        "confirmed": True,
        "confidence": 0.9,  # >= 0.85
        "landmark_id": "LM_023",
        "source": ["vision", "local_map"]
    })
    
    # 评估策略
    suggestion = hooks.evaluate()
    
    print(f"  pre_turn_distance_m: {suggestion.pre_turn_distance_m}")
    print(f"  allow_gps: {suggestion.allow_gps}")
    print(f"  prefer_lock: {suggestion.prefer_lock}")
    print(f"  reason: {suggestion.reason}")
    
    assert suggestion.pre_turn_distance_m == 6.0, "视角确认强应该 pre_turn=6"
    assert suggestion.allow_gps is False, "视角确认强应该 allow_gps=False"
    assert suggestion.prefer_lock is True, "视角确认强应该 prefer_lock=True"
    assert "vision_confirmed" in suggestion.reason, "应该包含 vision_confirmed 原因"
    
    # 验证事件发布
    assert len(events_received) == 1, "应该发布 1 个策略建议事件"
    assert events_received[0][0] == "nav.fsm.policy.suggested", "应该是策略建议事件"
    
    print("\n✅ 测试场景 1 通过")


def test_scenario_2_consistency_mismatch():
    """测试场景 2: 一致性 mismatch → pre_turn=10，prefer_lock=False"""
    print("\n" + "=" * 60)
    print("测试场景 2: 一致性 mismatch → pre_turn=10，prefer_lock=False")
    print("=" * 60)
    
    events_received = []
    
    class MockEventBus:
        def subscribe(self, topic, handler):
            pass
        def publish(self, topic, event):
            events_received.append((topic, event))
    
    event_bus = MockEventBus()
    state_store = FSMPolicyStateStore(event_bus=event_bus)
    hooks = FSMPolicyHooks(state_store, event_bus=event_bus)
    
    # 模拟地图一致性更新（mismatch）
    state_store._on_map_consistency_updated({
        "score": 0.4,  # < 0.6
        "mismatch": True,
        "reasons": ["turn_mismatch"]
    })
    
    # 模拟 GPS 模式为 ACTIVE
    state_store._on_gps_mode_changed({"mode": GPSMode.ACTIVE})
    
    # 评估策略
    suggestion = hooks.evaluate()
    
    print(f"  pre_turn_distance_m: {suggestion.pre_turn_distance_m}")
    print(f"  allow_gps: {suggestion.allow_gps}")
    print(f"  prefer_lock: {suggestion.prefer_lock}")
    print(f"  reason: {suggestion.reason}")
    
    assert suggestion.pre_turn_distance_m == 10.0, "一致性差应该 pre_turn=10"
    assert suggestion.prefer_lock is False, "一致性差应该 prefer_lock=False"
    assert suggestion.allow_gps is True, "GPS ACTIVE 时应该 allow_gps=True"
    assert "consistency_poor" in suggestion.reason, "应该包含 consistency_poor 原因"
    
    print("\n✅ 测试场景 2 通过")


def test_scenario_3_gps_quality_degraded():
    """测试场景 3: gps_quality degraded → allow_gps=False"""
    print("\n" + "=" * 60)
    print("测试场景 3: gps_quality degraded → allow_gps=False")
    print("=" * 60)
    
    events_received = []
    
    class MockEventBus:
        def subscribe(self, topic, handler):
            pass
        def publish(self, topic, event):
            events_received.append((topic, event))
    
    event_bus = MockEventBus()
    state_store = FSMPolicyStateStore(event_bus=event_bus)
    hooks = FSMPolicyHooks(state_store, event_bus=event_bus)
    
    # 模拟 GPS 质量降级
    state_store._on_gps_quality_changed({"quality": GPSQuality.DEGRADED})
    
    # 模拟 GPS 模式为 ACTIVE（但质量差）
    state_store._on_gps_mode_changed({"mode": GPSMode.ACTIVE})
    
    # 评估策略
    suggestion = hooks.evaluate()
    
    print(f"  allow_gps: {suggestion.allow_gps}")
    print(f"  reason: {suggestion.reason}")
    
    assert suggestion.allow_gps is False, "GPS 质量差应该 allow_gps=False"
    assert "gps_degraded" in suggestion.reason, "应该包含 gps_degraded 原因"
    
    print("\n✅ 测试场景 3 通过")


def test_scenario_4_gps_mode_verify_only():
    """测试场景 4: gps_mode verify_only → allow_gps=False"""
    print("\n" + "=" * 60)
    print("测试场景 4: gps_mode verify_only → allow_gps=False")
    print("=" * 60)
    
    events_received = []
    
    class MockEventBus:
        def subscribe(self, topic, handler):
            pass
        def publish(self, topic, event):
            events_received.append((topic, event))
    
    event_bus = MockEventBus()
    state_store = FSMPolicyStateStore(event_bus=event_bus)
    hooks = FSMPolicyHooks(state_store, event_bus=event_bus)
    
    # 模拟 GPS 模式为 VERIFY_ONLY
    state_store._on_gps_mode_changed({"mode": GPSMode.VERIFY_ONLY})
    
    # 评估策略
    suggestion = hooks.evaluate()
    
    print(f"  allow_gps: {suggestion.allow_gps}")
    print(f"  reason: {suggestion.reason}")
    
    assert suggestion.allow_gps is False, "GPS VERIFY_ONLY 应该 allow_gps=False"
    assert "gps_verify_only" in suggestion.reason, "应该包含 gps_verify_only 原因"
    
    print("\n✅ 测试场景 4 通过")


def test_scenario_5_pre_turn_distance_variation():
    """测试场景 5: PRE_TURN 距离在不同证据下会变化"""
    print("\n" + "=" * 60)
    print("测试场景 5: PRE_TURN 距离在不同证据下会变化")
    print("=" * 60)
    
    events_received = []
    
    class MockEventBus:
        def subscribe(self, topic, handler):
            pass
        def publish(self, topic, event):
            events_received.append((topic, event))
    
    event_bus = MockEventBus()
    state_store = FSMPolicyStateStore(event_bus=event_bus)
    hooks = FSMPolicyHooks(state_store, event_bus=event_bus)
    
    # 场景 1: 默认情况
    suggestion1 = hooks.evaluate()
    print(f"  默认: pre_turn={suggestion1.pre_turn_distance_m:.1f}m")
    
    # 场景 2: 视角确认
    state_store._on_position_confirmed({
        "confirmed": True,
        "confidence": 0.9,
        "landmark_id": "LM_023",
        "source": ["vision", "local_map"]
    })
    suggestion2 = hooks.evaluate()
    print(f"  视角确认: pre_turn={suggestion2.pre_turn_distance_m:.1f}m")
    
    # 场景 3: 一致性差
    state_store._on_map_consistency_updated({
        "score": 0.4,
        "mismatch": True,
        "reasons": ["turn_mismatch"]
    })
    suggestion3 = hooks.evaluate()
    print(f"  一致性差: pre_turn={suggestion3.pre_turn_distance_m:.1f}m")
    
    # 验证距离变化
    assert suggestion1.pre_turn_distance_m == 8.0, "默认应该是 8.0m"
    assert suggestion2.pre_turn_distance_m == 6.0, "视角确认应该是 6.0m"
    assert suggestion3.pre_turn_distance_m == 10.0, "一致性差应该是 10.0m"
    
    print("\n✅ 测试场景 5 通过")


def main():
    """主函数"""
    print("=" * 60)
    print("FSM Policy Hooks Test")
    print("=" * 60)
    
    try:
        test_scenario_1_vision_confirm_strong()
        test_scenario_2_consistency_mismatch()
        test_scenario_3_gps_quality_degraded()
        test_scenario_4_gps_mode_verify_only()
        test_scenario_5_pre_turn_distance_variation()
        
        print("\n" + "=" * 60)
        print("✅ 所有测试完成")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()






