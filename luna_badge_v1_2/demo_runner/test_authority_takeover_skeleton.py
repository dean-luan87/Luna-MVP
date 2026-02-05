"""
Authority Takeover Skeleton Test (v1.4.8 Step 6)

最小自测：验证 Step 6 插桩功能
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
from navigation.authority_takeover_fsm import AuthorityTakeoverFSM, TakeoverState
from navigation.evidence_models import AuthorityConfidenceSnapshot
from navigation.events import (
    AuthorityConfidenceSnapshotEvent,
    SceneDecisionEvent,
    TOPIC_CONFIDENCE_SNAPSHOT,
    TOPIC_SCENE_DECISION,
)


def test_scenario_1_indoor_visual_takeover():
    """测试场景 1: 室内 Visual 接管（应该快速锁定）"""
    print("=" * 60)
    print("测试场景 1: 室内 Visual 接管")
    print("=" * 60)
    
    event_bus = EventBus()
    logger = get_logger("test_takeover")
    probe = AuthorityTakeoverProbe(event_bus=event_bus, logger=logger, enable_fsm=True)
    
    # 模拟场景决策（INDOOR）
    scene_event = SceneDecisionEvent(
        ts=time.time(),
        scene_type="INDOOR",
        confidence=0.9,
        reason="indoor_detected"
    )
    event_bus.publish(TOPIC_SCENE_DECISION, scene_event)
    time.sleep(0.1)
    
    # 模拟多个快照（Visual 高分且稳定）
    base_time = time.time()
    for i in range(10):
        snapshot_event = AuthorityConfidenceSnapshotEvent(
            ts=base_time + i * 0.2,
            visual_score=0.75 + i * 0.01,  # 持续上升
            map_vision_score=0.3,
            gps_score=0.0,
            dominant_candidate="VISUAL",
            confidence_gap=0.35,
            stability=0.8,
            decay_state={"VISUAL_STABILITY": 0.8},
            reason_trace=[],
            window_s=10.0
        )
        event_bus.publish(TOPIC_CONFIDENCE_SNAPSHOT, snapshot_event)
        time.sleep(0.2)
    
    print(f"\n✅ 测试场景 1 完成")
    print(f"   最终状态: {probe.fsm.current_state.value}")
    print(f"   目标主权: {probe.fsm.context.target_authority}")


def test_scenario_2_map_vision_landmark_boost():
    """测试场景 2: Map Vision 地标匹配 boost（应该触发接管）"""
    print("\n" + "=" * 60)
    print("测试场景 2: Map Vision 地标匹配 boost")
    print("=" * 60)
    
    event_bus = EventBus()
    logger = get_logger("test_takeover")
    probe = AuthorityTakeoverProbe(event_bus=event_bus, logger=logger, enable_fsm=True)
    
    # 模拟场景决策（OUTDOOR）
    scene_event = SceneDecisionEvent(
        ts=time.time(),
        scene_type="OUTDOOR",
        confidence=0.85,
        reason="outdoor_detected"
    )
    event_bus.publish(TOPIC_SCENE_DECISION, scene_event)
    time.sleep(0.1)
    
    # 模拟快照（Map Vision 高分，地标匹配强）
    base_time = time.time()
    for i in range(15):  # 需要超过 lock_s=2.0 秒
        snapshot_event = AuthorityConfidenceSnapshotEvent(
            ts=base_time + i * 0.2,
            visual_score=0.5,
            map_vision_score=0.85,  # 高分
            gps_score=0.4,
            dominant_candidate="MAP_VISION",
            confidence_gap=0.35,  # 大差距
            stability=0.9,
            decay_state={"LANDMARK_MATCH": 0.9},
            reason_trace=["boost_map_vision_due_to_strong_landmark"],
            window_s=10.0
        )
        event_bus.publish(TOPIC_CONFIDENCE_SNAPSHOT, snapshot_event)
        time.sleep(0.2)
    
    print(f"\n✅ 测试场景 2 完成")
    print(f"   最终状态: {probe.fsm.current_state.value}")
    print(f"   目标主权: {probe.fsm.context.target_authority}")


def test_scenario_3_gps_not_allowed_indoor():
    """测试场景 3: 室内不允许 GPS 接管"""
    print("\n" + "=" * 60)
    print("测试场景 3: 室内不允许 GPS 接管")
    print("=" * 60)
    
    event_bus = EventBus()
    logger = get_logger("test_takeover")
    probe = AuthorityTakeoverProbe(event_bus=event_bus, logger=logger, enable_fsm=True)
    
    # 模拟场景决策（INDOOR）
    scene_event = SceneDecisionEvent(
        ts=time.time(),
        scene_type="INDOOR",
        confidence=0.9,
        reason="indoor_detected"
    )
    event_bus.publish(TOPIC_SCENE_DECISION, scene_event)
    time.sleep(0.1)
    
    # 模拟快照（GPS 高分，但室内场景）
    base_time = time.time()
    for i in range(20):
        snapshot_event = AuthorityConfidenceSnapshotEvent(
            ts=base_time + i * 0.2,
            visual_score=0.3,
            map_vision_score=0.3,
            gps_score=0.9,  # GPS 高分
            dominant_candidate="GPS",
            confidence_gap=0.6,  # 大差距
            stability=0.9,
            decay_state={"GPS_STABILITY": 0.9},
            reason_trace=[],
            window_s=10.0
        )
        event_bus.publish(TOPIC_CONFIDENCE_SNAPSHOT, snapshot_event)
        time.sleep(0.2)
    
    print(f"\n✅ 测试场景 3 完成")
    print(f"   最终状态: {probe.fsm.current_state.value} (应该保持 IDLE)")
    print(f"   目标主权: {probe.fsm.context.target_authority} (应该为 None)")


def test_scenario_4_cooldown_prevention():
    """测试场景 4: 冷却期防止频繁切换"""
    print("\n" + "=" * 60)
    print("测试场景 4: 冷却期防止频繁切换")
    print("=" * 60)
    
    event_bus = EventBus()
    logger = get_logger("test_takeover")
    probe = AuthorityTakeoverProbe(event_bus=event_bus, logger=logger, enable_fsm=True)
    
    # 模拟场景决策（OUTDOOR）
    scene_event = SceneDecisionEvent(
        ts=time.time(),
        scene_type="OUTDOOR",
        confidence=0.85,
        reason="outdoor_detected"
    )
    event_bus.publish(TOPIC_SCENE_DECISION, scene_event)
    time.sleep(0.1)
    
    # 第一次接管：Map Vision
    base_time = time.time()
    for i in range(15):
        snapshot_event = AuthorityConfidenceSnapshotEvent(
            ts=base_time + i * 0.2,
            visual_score=0.4,
            map_vision_score=0.85,
            gps_score=0.3,
            dominant_candidate="MAP_VISION",
            confidence_gap=0.45,
            stability=0.9,
            decay_state={},
            reason_trace=[],
            window_s=10.0
        )
        event_bus.publish(TOPIC_CONFIDENCE_SNAPSHOT, snapshot_event)
        time.sleep(0.2)
    
    print(f"\n   第一次接管后状态: {probe.fsm.current_state.value}")
    
    # 即使快照改变，也应该在冷却期内
    time.sleep(0.5)
    snapshot_event = AuthorityConfidenceSnapshotEvent(
        ts=time.time(),
        visual_score=0.9,  # Visual 突然变高
        map_vision_score=0.3,
        gps_score=0.2,
        dominant_candidate="VISUAL",
        confidence_gap=0.6,
        stability=0.9,
        decay_state={},
        reason_trace=[],
        window_s=10.0
    )
    event_bus.publish(TOPIC_CONFIDENCE_SNAPSHOT, snapshot_event)
    time.sleep(0.1)
    
    print(f"   快照改变后状态: {probe.fsm.current_state.value} (应该仍在 COOLDOWN)")
    print(f"\n✅ 测试场景 4 完成")


def main():
    """主函数"""
    print("=" * 60)
    print("Authority Takeover Skeleton Test")
    print("=" * 60)
    
    try:
        # 测试场景 1
        test_scenario_1_indoor_visual_takeover()
        
        # 测试场景 2
        test_scenario_2_map_vision_landmark_boost()
        
        # 测试场景 3
        test_scenario_3_gps_not_allowed_indoor()
        
        # 测试场景 4
        test_scenario_4_cooldown_prevention()
        
        print("\n" + "=" * 60)
        print("✅ 所有测试完成")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()






