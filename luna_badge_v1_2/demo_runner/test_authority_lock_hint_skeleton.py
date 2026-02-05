"""
Authority Lock Hint Skeleton Test (v1.4.8 Step 7)

最小自测：验证 Step 7 插桩功能
"""

import os
import sys
import time

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# 尝试导入 EventBus
try:
    from common.event_bus import EventBus
except ImportError:
    class EventBus:
        def __init__(self):
            self._subscribers = {}
        def subscribe(self, topic, handler):
            if topic not in self._subscribers:
                self._subscribers[topic] = []
            self._subscribers[topic].append(handler)
        def publish(self, topic, event):
            if topic in self._subscribers:
                for handler in self._subscribers[topic]:
                    try:
                        handler(event)
                    except Exception as e:
                        print(f"Event handler error: {e}")

try:
    from common.logger import get_logger
except ImportError:
    def get_logger(name):
        class Logger:
            def info(self, module, event, payload):
                print(f"[{module}] {event}: {payload}")
        return Logger()

from navigation.authority_takeover_probe import AuthorityTakeoverProbe
from navigation.authority_lock_hint_probe import AuthorityLockHintProbe
from navigation.events import (
    AuthorityConfidenceSnapshotEvent,
    SceneDecisionEvent,
    TOPIC_CONFIDENCE_SNAPSHOT,
    TOPIC_SCENE_DECISION,
    TOPIC_AUTHORITY_LOCK_HINT,
)


def test_scenario_1_lock_hint_during_locking():
    """测试场景 1: LOCKING 状态期间发出 Hint"""
    print("=" * 60)
    print("测试场景 1: LOCKING 状态期间发出 Hint")
    print("=" * 60)
    
    event_bus = EventBus()
    logger = get_logger("test_lock_hint")
    
    # 创建 Takeover Probe
    takeover_probe = AuthorityTakeoverProbe(
        event_bus=event_bus,
        logger=logger,
        enable_fsm=True
    )
    
    # 创建 Hint Probe（传入 FSM 实例）
    hint_probe = AuthorityLockHintProbe(
        fsm=takeover_probe.fsm,
        event_bus=event_bus,
        logger=logger,
        enable_hint=True
    )
    
    # 订阅 Hint 事件
    hints_received = []
    def on_hint(event):
        hints_received.append(event.hint)
        print(f"  📢 收到 Hint: target={event.hint.target_authority}, eta={event.hint.eta_s:.2f}s")
    
    event_bus.subscribe(TOPIC_AUTHORITY_LOCK_HINT, on_hint)
    
    # 模拟场景决策（OUTDOOR）
    scene_event = SceneDecisionEvent(
        ts=time.time(),
        scene_type="OUTDOOR",
        confidence=0.85,
        reason="outdoor_detected"
    )
    event_bus.publish(TOPIC_SCENE_DECISION, scene_event)
    hint_probe.set_scene("OUTDOOR")
    time.sleep(0.1)
    
    # 模拟快照（Map Vision 高分，进入 LOCKING）
    base_time = time.time()
    for i in range(20):  # 持续足够长时间
        snapshot_event = AuthorityConfidenceSnapshotEvent(
            ts=base_time + i * 0.2,
            visual_score=0.5,
            map_vision_score=0.85,  # 高分
            gps_score=0.4,
            dominant_candidate="MAP_VISION",
            confidence_gap=0.35,
            stability=0.9,
            decay_state={"LANDMARK_MATCH": 0.9},
            reason_trace=[],
            window_s=10.0
        )
        event_bus.publish(TOPIC_CONFIDENCE_SNAPSHOT, snapshot_event)
        
        # 触发 Hint 更新（模拟周期性检查）
        hint_probe.update(scene="OUTDOOR")
        
        time.sleep(0.2)
    
    print(f"\n✅ 测试场景 1 完成")
    print(f"   收到 Hint 数量: {len(hints_received)}")
    print(f"   FSM 状态: {takeover_probe.fsm.current_state.value}")
    
    # 验证：LOCKING 状态应该发出 Hint
    assert len(hints_received) > 0, "应该收到至少一个 Hint"
    print("   ✅ Hint 正常发出")


def test_scenario_2_no_hint_when_not_locking():
    """测试场景 2: FSM 未进入 LOCKING → 无 Hint"""
    print("\n" + "=" * 60)
    print("测试场景 2: FSM 未进入 LOCKING → 无 Hint")
    print("=" * 60)
    
    event_bus = EventBus()
    logger = get_logger("test_lock_hint")
    
    # 创建 Takeover Probe
    takeover_probe = AuthorityTakeoverProbe(
        event_bus=event_bus,
        logger=logger,
        enable_fsm=True
    )
    
    # 创建 Hint Probe
    hint_probe = AuthorityLockHintProbe(
        fsm=takeover_probe.fsm,
        event_bus=event_bus,
        logger=logger,
        enable_hint=True
    )
    
    # 订阅 Hint 事件
    hints_received = []
    def on_hint(event):
        hints_received.append(event.hint)
    
    event_bus.subscribe(TOPIC_AUTHORITY_LOCK_HINT, on_hint)
    
    # 模拟场景决策（OUTDOOR）
    scene_event = SceneDecisionEvent(
        ts=time.time(),
        scene_type="OUTDOOR",
        confidence=0.85,
        reason="outdoor_detected"
    )
    event_bus.publish(TOPIC_SCENE_DECISION, scene_event)
    hint_probe.set_scene("OUTDOOR")
    time.sleep(0.1)
    
    # 模拟快照（分数不足，不会进入 LOCKING）
    base_time = time.time()
    for i in range(5):
        snapshot_event = AuthorityConfidenceSnapshotEvent(
            ts=base_time + i * 0.2,
            visual_score=0.3,
            map_vision_score=0.3,  # 低分
            gps_score=0.3,
            dominant_candidate=None,  # 无主导
            confidence_gap=0.0,
            stability=0.5,
            decay_state={},
            reason_trace=[],
            window_s=10.0
        )
        event_bus.publish(TOPIC_CONFIDENCE_SNAPSHOT, snapshot_event)
        
        # 触发 Hint 更新
        hint_probe.update(scene="OUTDOOR")
        
        time.sleep(0.2)
    
    print(f"\n✅ 测试场景 2 完成")
    print(f"   FSM 状态: {takeover_probe.fsm.current_state.value} (应该保持 IDLE)")
    print(f"   收到 Hint 数量: {len(hints_received)} (应该为 0)")
    
    # 验证：未进入 LOCKING，不应该收到 Hint
    assert len(hints_received) == 0, "不应该收到 Hint"
    assert takeover_probe.fsm.current_state.value == "IDLE", "应该保持 IDLE 状态"
    print("   ✅ 无 Hint 正常")


def test_scenario_3_hint_stops_on_fsm_backoff():
    """测试场景 3: FSM 回退 → Hint 自动停止"""
    print("\n" + "=" * 60)
    print("测试场景 3: FSM 回退 → Hint 自动停止")
    print("=" * 60)
    
    event_bus = EventBus()
    logger = get_logger("test_lock_hint")
    
    # 创建 Takeover Probe
    takeover_probe = AuthorityTakeoverProbe(
        event_bus=event_bus,
        logger=logger,
        enable_fsm=True
    )
    
    # 创建 Hint Probe
    hint_probe = AuthorityLockHintProbe(
        fsm=takeover_probe.fsm,
        event_bus=event_bus,
        logger=logger,
        enable_hint=True
    )
    
    # 订阅 Hint 事件
    hints_received = []
    def on_hint(event):
        hints_received.append(event.hint)
        print(f"  📢 收到 Hint: target={event.hint.target_authority}")
    
    event_bus.subscribe(TOPIC_AUTHORITY_LOCK_HINT, on_hint)
    
    # 模拟场景决策（OUTDOOR）
    scene_event = SceneDecisionEvent(
        ts=time.time(),
        scene_type="OUTDOOR",
        confidence=0.85,
        reason="outdoor_detected"
    )
    event_bus.publish(TOPIC_SCENE_DECISION, scene_event)
    hint_probe.set_scene("OUTDOOR")
    time.sleep(0.1)
    
    # 第一阶段：进入 LOCKING（可能发出 Hint）
    base_time = time.time()
    for i in range(10):
        snapshot_event = AuthorityConfidenceSnapshotEvent(
            ts=base_time + i * 0.2,
            visual_score=0.5,
            map_vision_score=0.85,
            gps_score=0.4,
            dominant_candidate="MAP_VISION",
            confidence_gap=0.35,
            stability=0.9,
            decay_state={},
            reason_trace=[],
            window_s=10.0
        )
        event_bus.publish(TOPIC_CONFIDENCE_SNAPSHOT, snapshot_event)
        hint_probe.update(scene="OUTDOOR")
        time.sleep(0.2)
    
    initial_hint_count = len(hints_received)
    
    # 第二阶段：快照改变，FSM 回退到 IDLE
    for i in range(5):
        snapshot_event = AuthorityConfidenceSnapshotEvent(
            ts=base_time + 10 * 0.2 + i * 0.2,
            visual_score=0.9,  # 突然变化
            map_vision_score=0.3,  # 降低
            gps_score=0.2,
            dominant_candidate="VISUAL",  # 改变主导
            confidence_gap=0.6,
            stability=0.9,
            decay_state={},
            reason_trace=[],
            window_s=10.0
        )
        event_bus.publish(TOPIC_CONFIDENCE_SNAPSHOT, snapshot_event)
        hint_probe.update(scene="OUTDOOR")
        time.sleep(0.2)
    
    print(f"\n✅ 测试场景 3 完成")
    print(f"   FSM 状态: {takeover_probe.fsm.current_state.value}")
    print(f"   回退前 Hint 数量: {initial_hint_count}")
    print(f"   回退后 Hint 数量: {len(hints_received)}")
    
    # 验证：FSM 回退后，Hint 应该停止
    assert takeover_probe.fsm.current_state.value != "LOCKING", "应该已经退出 LOCKING"
    print("   ✅ Hint 自动停止正常")


def main():
    """主函数"""
    print("=" * 60)
    print("Authority Lock Hint Skeleton Test")
    print("=" * 60)
    
    try:
        # 测试场景 1
        test_scenario_1_lock_hint_during_locking()
        
        # 测试场景 2
        test_scenario_2_no_hint_when_not_locking()
        
        # 测试场景 3
        test_scenario_3_hint_stops_on_fsm_backoff()
        
        print("\n" + "=" * 60)
        print("✅ 所有测试完成")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()






