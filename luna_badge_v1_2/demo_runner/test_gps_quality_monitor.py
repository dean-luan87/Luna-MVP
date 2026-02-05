"""
GPS Quality Monitor Test (v1.4.8 StepB-2)

测试 GPS 质量监控器：跳点 / 速度异常 / 精度异常
"""

import os
import sys
import time

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from navigation.gps_quality_monitor import GPSQualityMonitor, GPSQuality, GPSReading


def test_scenario_1_speed_anomaly():
    """测试场景 1: 速度异常检测"""
    print("=" * 60)
    print("测试场景 1: 速度异常检测")
    print("=" * 60)
    
    monitor = GPSQualityMonitor(max_walking_speed_mps=5.0)
    
    base_time = time.time()
    base_lat = 39.9042
    base_lng = 116.4074
    
    # 第一次读数（正常）
    reading1 = GPSReading(
        lat=base_lat,
        lng=base_lng,
        accuracy_m=5.0,
        timestamp=base_time
    )
    quality1 = monitor.update(reading1)
    print(f"  第一次读数质量: {quality1.value}")
    assert quality1 == GPSQuality.GOOD, "第一次读数应该良好"
    
    # 第二次读数（速度异常：1 秒内移动 10 米，速度 10 m/s > 5 m/s）
    reading2 = GPSReading(
        lat=base_lat + 0.0001,  # 约 10 米
        lng=base_lng,
        accuracy_m=5.0,
        timestamp=base_time + 1.0
    )
    quality2 = monitor.update(reading2)
    print(f"  第二次读数质量: {quality2.value}")
    assert quality2 == GPSQuality.DEGRADED, "速度异常应该降级"
    
    print("\n✅ 测试场景 1 通过")


def test_scenario_2_jump_detection():
    """测试场景 2: 跳点检测"""
    print("\n" + "=" * 60)
    print("测试场景 2: 跳点检测（短时间内大位移）")
    print("=" * 60)
    
    monitor = GPSQualityMonitor(
        max_displacement_m=10.0,
        max_displacement_window_s=1.0
    )
    
    base_time = time.time()
    base_lat = 39.9042
    base_lng = 116.4074
    
    # 第一次读数
    reading1 = GPSReading(
        lat=base_lat,
        lng=base_lng,
        accuracy_m=5.0,
        timestamp=base_time
    )
    quality1 = monitor.update(reading1)
    print(f"  第一次读数质量: {quality1.value}")
    
    # 第二次读数（跳点：0.5 秒内移动 15 米 > 10 米阈值）
    reading2 = GPSReading(
        lat=base_lat + 0.00015,  # 约 15 米
        lng=base_lng,
        accuracy_m=5.0,
        timestamp=base_time + 0.5
    )
    quality2 = monitor.update(reading2)
    print(f"  第二次读数质量: {quality2.value}")
    assert quality2 == GPSQuality.DEGRADED, "跳点应该降级"
    
    print("\n✅ 测试场景 2 通过")


def test_scenario_3_accuracy_degradation():
    """测试场景 3: 精度劣化"""
    print("\n" + "=" * 60)
    print("测试场景 3: 精度劣化（accuracy > 15m）")
    print("=" * 60)
    
    monitor = GPSQualityMonitor(max_accuracy_m=15.0)
    
    base_time = time.time()
    
    # 第一次读数（精度正常）
    reading1 = GPSReading(
        lat=39.9042,
        lng=116.4074,
        accuracy_m=10.0,
        timestamp=base_time
    )
    quality1 = monitor.update(reading1)
    print(f"  第一次读数质量（精度 10m）: {quality1.value}")
    assert quality1 == GPSQuality.GOOD, "精度 10m 应该良好"
    
    # 第二次读数（精度劣化：20m > 15m）
    reading2 = GPSReading(
        lat=39.9042,
        lng=116.4074,
        accuracy_m=20.0,
        timestamp=base_time + 1.0
    )
    quality2 = monitor.update(reading2)
    print(f"  第二次读数质量（精度 20m）: {quality2.value}")
    assert quality2 == GPSQuality.DEGRADED, "精度 20m 应该降级"
    
    print("\n✅ 测试场景 3 通过")


def test_scenario_4_continuous_degradation_to_invalid():
    """测试场景 4: 连续异常 → INVALID"""
    print("\n" + "=" * 60)
    print("测试场景 4: 连续异常 → INVALID（连续 3 次 DEGRADED）")
    print("=" * 60)
    
    monitor = GPSQualityMonitor(
        max_accuracy_m=15.0,
        degraded_threshold=3
    )
    
    base_time = time.time()
    
    # 连续 3 次精度异常
    for i in range(3):
        reading = GPSReading(
            lat=39.9042,
            lng=116.4074,
            accuracy_m=20.0,  # 精度异常
            timestamp=base_time + i * 1.0
        )
        quality = monitor.update(reading)
        print(f"  第 {i+1} 次读数质量: {quality.value}")
    
    # 第 3 次应该变成 INVALID
    reading3 = GPSReading(
        lat=39.9042,
        lng=116.4074,
        accuracy_m=20.0,
        timestamp=base_time + 3.0
    )
    quality3 = monitor.update(reading3)
    print(f"  第 4 次读数质量: {quality3.value}")
    assert quality3 == GPSQuality.INVALID, "连续 3 次异常应该变成 INVALID"
    
    print("\n✅ 测试场景 4 通过")


def test_scenario_5_quality_change_event():
    """测试场景 5: 质量变化事件"""
    print("\n" + "=" * 60)
    print("测试场景 5: 质量变化事件")
    print("=" * 60)
    
    events_received = []
    
    class MockEventBus:
        def publish(self, topic, event):
            events_received.append((topic, event))
    
    event_bus = MockEventBus()
    monitor = GPSQualityMonitor(
        event_bus=event_bus,
        max_accuracy_m=15.0
    )
    
    base_time = time.time()
    
    # 第一次读数（应该触发 GOOD 事件）
    reading1 = GPSReading(
        lat=39.9042,
        lng=116.4074,
        accuracy_m=10.0,
        timestamp=base_time
    )
    monitor.update(reading1)
    
    # 第二次读数（精度异常，应该触发 DEGRADED 事件）
    reading2 = GPSReading(
        lat=39.9042,
        lng=116.4074,
        accuracy_m=20.0,
        timestamp=base_time + 1.0
    )
    monitor.update(reading2)
    
    print(f"  事件数量: {len(events_received)}")
    assert len(events_received) == 2, "应该有 2 个质量变化事件"
    assert events_received[0][0] == "nav.gps.quality.changed", "第一个事件应该是质量变化"
    assert events_received[1][0] == "nav.gps.quality.changed", "第二个事件应该是质量变化"
    
    print("\n✅ 测试场景 5 通过")


def main():
    """主函数"""
    print("=" * 60)
    print("GPS Quality Monitor Test")
    print("=" * 60)
    
    try:
        test_scenario_1_speed_anomaly()
        test_scenario_2_jump_detection()
        test_scenario_3_accuracy_degradation()
        test_scenario_4_continuous_degradation_to_invalid()
        test_scenario_5_quality_change_event()
        
        print("\n" + "=" * 60)
        print("✅ 所有测试完成")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()






