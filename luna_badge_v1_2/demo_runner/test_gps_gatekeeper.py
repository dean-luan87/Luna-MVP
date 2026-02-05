"""
GPS Gatekeeper Test (v1.4.8 StepB-1)

测试 GPS 门控器：场景 × 距离门控
"""

import os
import sys

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from navigation.gps_gatekeeper import GPSGatekeeper, GPSMode


def test_scenario_1_indoor_always_off():
    """测试场景 1: 室内场景 → GPS 关闭"""
    print("=" * 60)
    print("测试场景 1: 室内场景 → GPS 关闭")
    print("=" * 60)
    
    gatekeeper = GPSGatekeeper()
    
    # 室内场景，无论距离如何，GPS 都应该关闭
    mode_10m = gatekeeper.resolve_mode("indoor", 10.0)
    mode_100m = gatekeeper.resolve_mode("indoor", 100.0)
    
    print(f"  距离 10m: {mode_10m.value}")
    print(f"  距离 100m: {mode_100m.value}")
    
    assert mode_10m == GPSMode.OFF, "室内 10m 应该关闭 GPS"
    assert mode_100m == GPSMode.OFF, "室内 100m 应该关闭 GPS"
    
    print("\n✅ 测试场景 1 通过")


def test_scenario_2_outdoor_distance_threshold():
    """测试场景 2: 室外场景 → 距离阈值"""
    print("\n" + "=" * 60)
    print("测试场景 2: 室外场景 → 距离阈值（49m / 50m / 51m）")
    print("=" * 60)
    
    gatekeeper = GPSGatekeeper()
    
    # 49m（≤50m）
    mode_49m = gatekeeper.resolve_mode("outdoor", 49.0)
    print(f"  距离 49m: {mode_49m.value}")
    assert mode_49m == GPSMode.VERIFY_ONLY, "室外 49m 应该是 VERIFY_ONLY"
    
    # 50m（=50m）
    mode_50m = gatekeeper.resolve_mode("outdoor", 50.0)
    print(f"  距离 50m: {mode_50m.value}")
    assert mode_50m == GPSMode.VERIFY_ONLY, "室外 50m 应该是 VERIFY_ONLY"
    
    # 51m（>50m）
    mode_51m = gatekeeper.resolve_mode("outdoor", 51.0)
    print(f"  距离 51m: {mode_51m.value}")
    assert mode_51m == GPSMode.ACTIVE, "室外 51m 应该是 ACTIVE"
    
    print("\n✅ 测试场景 2 通过")


def test_scenario_3_transition_verify_only():
    """测试场景 3: 过渡场景 → 仅验证"""
    print("\n" + "=" * 60)
    print("测试场景 3: 过渡场景 → 仅验证")
    print("=" * 60)
    
    gatekeeper = GPSGatekeeper()
    
    # 过渡场景，无论距离如何，都应该是 VERIFY_ONLY
    mode_10m = gatekeeper.resolve_mode("transition", 10.0)
    mode_100m = gatekeeper.resolve_mode("transition", 100.0)
    
    print(f"  距离 10m: {mode_10m.value}")
    print(f"  距离 100m: {mode_100m.value}")
    
    assert mode_10m == GPSMode.VERIFY_ONLY, "过渡 10m 应该是 VERIFY_ONLY"
    assert mode_100m == GPSMode.VERIFY_ONLY, "过渡 100m 应该是 VERIFY_ONLY"
    
    print("\n✅ 测试场景 3 通过")


def test_scenario_4_mode_change_event():
    """测试场景 4: 模式变化事件"""
    print("\n" + "=" * 60)
    print("测试场景 4: 模式变化事件")
    print("=" * 60)
    
    events_received = []
    
    class MockEventBus:
        def publish(self, topic, event):
            events_received.append((topic, event))
    
    event_bus = MockEventBus()
    gatekeeper = GPSGatekeeper(event_bus=event_bus)
    
    # 第一次设置（应该触发事件）
    mode1 = gatekeeper.resolve_mode("indoor", 10.0)
    
    # 相同模式（不应该触发事件）
    mode2 = gatekeeper.resolve_mode("indoor", 20.0)
    
    # 不同模式（应该触发事件）
    mode3 = gatekeeper.resolve_mode("outdoor", 100.0)
    
    print(f"  事件数量: {len(events_received)}")
    assert len(events_received) == 2, "应该有 2 个模式变化事件"
    assert events_received[0][0] == "nav.gps.mode.changed", "第一个事件应该是模式变化"
    assert events_received[1][0] == "nav.gps.mode.changed", "第二个事件应该是模式变化"
    
    print("\n✅ 测试场景 4 通过")


def main():
    """主函数"""
    print("=" * 60)
    print("GPS Gatekeeper Test")
    print("=" * 60)
    
    try:
        test_scenario_1_indoor_always_off()
        test_scenario_2_outdoor_distance_threshold()
        test_scenario_3_transition_verify_only()
        test_scenario_4_mode_change_event()
        
        print("\n" + "=" * 60)
        print("✅ 所有测试完成")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()






