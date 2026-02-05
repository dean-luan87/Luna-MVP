"""
Map Consistency Checker Test (v1.4.8 StepB-4)

测试地图一致性检查器
"""

import os
import sys
import time

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from navigation.map_consistency_checker import MapConsistencyChecker, ConsistencyResult


def test_scenario_1_turn_consistent():
    """测试场景 1: 拐向一致 → 高分"""
    print("=" * 60)
    print("测试场景 1: 拐向一致 → 高分")
    print("=" * 60)
    
    events_received = []
    
    class MockEventBus:
        def subscribe(self, topic, handler):
            pass
        def publish(self, topic, event):
            events_received.append((topic, event))
    
    event_bus = MockEventBus()
    checker = MapConsistencyChecker(event_bus=event_bus)
    
    # 设置路线步进（预期左转）
    checker._current_route_step = {
        "step_id": "step_001",
        "expected_turn": "left",
        "expected_distance_m": 50.0
    }
    
    # 设置最后确认的地标（方向为左）
    checker._last_confirmed_landmark = {
        "landmark_type": "intersection",
        "direction_hint": "left",
        "confidence": 0.9
    }
    
    # 执行一致性检查
    result = checker._evaluate_consistency()
    
    print(f"  一致性分数: {result.score:.2f}")
    print(f"  失配标志: {result.mismatch}")
    print(f"  原因: {result.reasons}")
    
    assert result.score >= 0.7, "拐向一致应该高分"
    assert not result.mismatch, "不应该失配"
    
    print("\n✅ 测试场景 1 通过")


def test_scenario_2_turn_inconsistent():
    """测试场景 2: 拐向不一致 → 低分 + mismatch"""
    print("\n" + "=" * 60)
    print("测试场景 2: 拐向不一致 → 低分 + mismatch")
    print("=" * 60)
    
    events_received = []
    
    class MockEventBus:
        def subscribe(self, topic, handler):
            pass
        def publish(self, topic, event):
            events_received.append((topic, event))
    
    event_bus = MockEventBus()
    checker = MapConsistencyChecker(event_bus=event_bus, mismatch_threshold=0.6)
    
    # 设置路线步进（预期左转）
    checker._current_route_step = {
        "step_id": "step_001",
        "expected_turn": "left",
        "expected_distance_m": 50.0
    }
    
    # 设置最后确认的地标（方向为右，不一致）
    checker._last_confirmed_landmark = {
        "landmark_type": "intersection",
        "direction_hint": "right",  # 与预期不一致
        "confidence": 0.9
    }
    
    # 执行一致性检查
    result = checker._evaluate_consistency()
    
    print(f"  一致性分数: {result.score:.2f}")
    print(f"  失配标志: {result.mismatch}")
    print(f"  原因: {result.reasons}")
    
    assert result.score < 0.6, "拐向不一致应该低分"
    assert result.mismatch, "应该失配"
    assert "turn_mismatch" in result.reasons, "应该包含 turn_mismatch 原因"
    
    print("\n✅ 测试场景 2 通过")


def test_scenario_3_distance_deviation():
    """测试场景 3: 距离偏差过大 → 降分"""
    print("\n" + "=" * 60)
    print("测试场景 3: 距离偏差过大 → 降分")
    print("=" * 60)
    
    events_received = []
    
    class MockEventBus:
        def subscribe(self, topic, handler):
            pass
        def publish(self, topic, event):
            events_received.append((topic, event))
    
    event_bus = MockEventBus()
    checker = MapConsistencyChecker(
        event_bus=event_bus,
        distance_error_window_pct=0.2,
        distance_error_window_m=10.0
    )
    
    # 设置路线步进（预期距离 50m）
    checker._current_route_step = {
        "step_id": "step_001",
        "expected_turn": "left",
        "expected_distance_m": 50.0
    }
    
    # 设置最后确认的地标（距离偏差大：实际 70m，预期 50m，偏差 20m > 误差窗 10m）
    checker._last_confirmed_landmark = {
        "landmark_type": "intersection",
        "direction_hint": "left",
        "distance_m": 70.0,  # 偏差 20m
        "confidence": 0.9
    }
    
    # 执行一致性检查
    result = checker._evaluate_consistency()
    
    print(f"  一致性分数: {result.score:.2f}")
    print(f"  失配标志: {result.mismatch}")
    print(f"  原因: {result.reasons}")
    
    # 距离偏差大应该降分
    assert result.score < 0.8, "距离偏差大应该降分"
    if "distance_mismatch" in result.reasons:
        print("  包含 distance_mismatch 原因")
    
    print("\n✅ 测试场景 3 通过")


def test_scenario_4_missing_structure_evidence():
    """测试场景 4: 长时间无结构证据 → mismatch"""
    print("\n" + "=" * 60)
    print("测试场景 4: 长时间无结构证据 → mismatch")
    print("=" * 60)
    
    events_received = []
    
    class MockEventBus:
        def subscribe(self, topic, handler):
            pass
        def publish(self, topic, event):
            events_received.append((topic, event))
    
    event_bus = MockEventBus()
    checker = MapConsistencyChecker(event_bus=event_bus, mismatch_threshold=0.6)
    
    # 设置路线步进（预期右转，应该有结构证据）
    checker._current_route_step = {
        "step_id": "step_001",
        "expected_turn": "right",
        "expected_distance_m": 50.0
    }
    
    # 设置最后确认的地标（非结构性地标）
    checker._last_confirmed_landmark = {
        "landmark_type": "sign",  # 非结构性地标
        "direction_hint": "right",
        "confidence": 0.9
    }
    
    # 设置 LocalMap 节点（无结构节点）
    checker._local_map_nodes = []
    
    # 执行一致性检查
    result = checker._evaluate_consistency()
    
    print(f"  一致性分数: {result.score:.2f}")
    print(f"  失配标志: {result.mismatch}")
    print(f"  原因: {result.reasons}")
    
    # 无结构证据应该降分
    assert result.score < 0.7, "无结构证据应该降分"
    if "missing_intersection" in result.reasons:
        print("  包含 missing_intersection 原因")
    
    print("\n✅ 测试场景 4 通过")


def test_scenario_5_consistency_event():
    """测试场景 5: 一致性事件发布"""
    print("\n" + "=" * 60)
    print("测试场景 5: 一致性事件发布")
    print("=" * 60)
    
    events_received = []
    
    class MockEventBus:
        def subscribe(self, topic, handler):
            pass
        def publish(self, topic, event):
            events_received.append((topic, event))
    
    event_bus = MockEventBus()
    checker = MapConsistencyChecker(event_bus=event_bus)
    
    # 设置路线步进
    checker._current_route_step = {
        "step_id": "step_001",
        "expected_turn": "left",
        "expected_distance_m": 50.0
    }
    
    # 设置最后确认的地标
    checker._last_confirmed_landmark = {
        "landmark_type": "intersection",
        "direction_hint": "left",
        "confidence": 0.9
    }
    
    # 触发一致性检查（通过事件）
    checker._check_consistency()
    
    # 验证事件发布
    assert len(events_received) == 1, "应该发布 1 个一致性事件"
    assert events_received[0][0] == "nav.map.consistency.updated", "应该是一致性更新事件"
    event_data = events_received[0][1]
    assert "score" in event_data, "应该包含 score"
    assert "mismatch" in event_data, "应该包含 mismatch"
    assert "reasons" in event_data, "应该包含 reasons"
    assert "evidence" in event_data, "应该包含 evidence"
    
    print(f"  事件数据: score={event_data['score']:.2f}, mismatch={event_data['mismatch']}")
    print("\n✅ 测试场景 5 通过")


def main():
    """主函数"""
    print("=" * 60)
    print("Map Consistency Checker Test")
    print("=" * 60)
    
    try:
        test_scenario_1_turn_consistent()
        test_scenario_2_turn_inconsistent()
        test_scenario_3_distance_deviation()
        test_scenario_4_missing_structure_evidence()
        test_scenario_5_consistency_event()
        
        print("\n" + "=" * 60)
        print("✅ 所有测试完成")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()






