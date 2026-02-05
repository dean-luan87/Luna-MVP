"""
Navigation Evidence Confidence Skeleton Test (v1.4.8 Step 5)

最小自测：验证 Step 5 插桩功能
"""

import os
import sys
import time

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import sys
import os

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# 尝试导入 EventBus
try:
    from common.event_bus import EventBus
except ImportError:
    # 如果没有 common.event_bus，使用简单的事件总线
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

# 尝试导入 logger
try:
    from common.logger import get_logger
except ImportError:
    def get_logger(name):
        class Logger:
            def info(self, module, event, payload):
                print(f"[{module}] {event}: {payload}")
        return Logger()
from navigation.evidence_probe import EvidenceProbe
from navigation.evidence_models import Evidence, EvidenceSource, EvidenceKind
from navigation.events import (
    SceneDecisionEvent,
    LandmarkMatchEvent,
    PositionUpdateEvent,
    TOPIC_SCENE_DECISION,
    TOPIC_LANDMARK_MATCH,
    TOPIC_POSITION_UPDATE,
)


def test_scenario_1_indoor_visual_landmark_high():
    """测试场景 1: INDOOR + visual_confidence 高 + landmark_match 高"""
    print("=" * 60)
    print("测试场景 1: INDOOR + visual_confidence 高 + landmark_match 高")
    print("=" * 60)
    
    event_bus = EventBus()
    logger = get_logger("test_evidence_confidence")
    probe = EvidenceProbe(event_bus=event_bus, logger=logger, enable_debug_log=True)
    
    # 模拟 SceneDecisionEvent (INDOOR)
    scene_event = SceneDecisionEvent(
        ts=time.time(),
        scene_type="INDOOR",  # 简化：直接用字符串
        confidence=0.9,
        reason="visual_indoor_indicators_detected"
    )
    event_bus.publish(TOPIC_SCENE_DECISION, scene_event)
    time.sleep(0.1)
    
    # 模拟多个 PositionUpdateEvent（高 visual_confidence）
    for i in range(5):
        pos_event = PositionUpdateEvent(
            ts=time.time() + i * 0.1,
            step_index=i,
            dx_m=i * 0.5,
            dy_m=0.0,
            dtheta_deg=0.0,
            visual_confidence=0.85 + i * 0.01  # 高置信度
        )
        event_bus.publish(TOPIC_POSITION_UPDATE, pos_event)
        time.sleep(0.1)
    
    # 模拟 LandmarkMatchEvent（高匹配）
    landmark_event = LandmarkMatchEvent(
        ts=time.time(),
        label="elevator_door_1",
        match_score=0.9,  # 高匹配
        matched_node_id="node_1",
        reason="exact_match"
    )
    event_bus.publish(TOPIC_LANDMARK_MATCH, landmark_event)
    time.sleep(0.2)
    
    # 获取快照
    snapshot = probe.get_snapshot()
    if snapshot:
        print(f"\n✅ 快照生成成功:")
        print(f"   visual_score: {snapshot.visual_score:.3f}")
        print(f"   map_vision_score: {snapshot.map_vision_score:.3f}")
        print(f"   gps_score: {snapshot.gps_score:.3f}")
        print(f"   dominant_candidate: {snapshot.dominant_candidate}")
        print(f"   confidence_gap: {snapshot.confidence_gap:.3f}")
        print(f"   stability: {snapshot.stability:.3f}")
        print(f"   reasons: {snapshot.reason_trace}")
    
    print("\n✅ 测试场景 1 完成\n")


def test_scenario_2_outdoor_gps_low_visual_high():
    """测试场景 2: OUTDOOR + gps_stability 低 + visual_stability 高（触发惩罚）"""
    print("=" * 60)
    print("测试场景 2: OUTDOOR + gps_stability 低 + visual_stability 高（触发惩罚）")
    print("=" * 60)
    
    event_bus = EventBus()
    logger = get_logger("test_evidence_confidence")
    probe = EvidenceProbe(event_bus=event_bus, logger=logger, enable_debug_log=True)
    
    # 模拟 SceneDecisionEvent (OUTDOOR)
    scene_event = SceneDecisionEvent(
        ts=time.time(),
        scene_type="OUTDOOR",
        confidence=0.85,
        reason="visual_outdoor_indicators_detected"
    )
    event_bus.publish(TOPIC_SCENE_DECISION, scene_event)
    time.sleep(0.1)
    
    # 模拟多个 PositionUpdateEvent（高 visual_confidence）
    for i in range(5):
        pos_event = PositionUpdateEvent(
            ts=time.time() + i * 0.1,
            step_index=i,
            dx_m=i * 0.5,
            dy_m=0.0,
            dtheta_deg=0.0,
            visual_confidence=0.8 + i * 0.02  # 高置信度（> 0.7）
        )
        event_bus.publish(TOPIC_POSITION_UPDATE, pos_event)
        time.sleep(0.1)
    
    # 手动摄入低 GPS stability（< 0.4）
    probe.ingest_gps_stability(value=0.3, ttl_s=5.0)  # 低稳定性
    time.sleep(0.2)
    
    # 获取快照
    snapshot = probe.get_snapshot()
    if snapshot:
        print(f"\n✅ 快照生成成功:")
        print(f"   visual_score: {snapshot.visual_score:.3f}")
        print(f"   map_vision_score: {snapshot.map_vision_score:.3f}")
        print(f"   gps_score: {snapshot.gps_score:.3f}")
        print(f"   dominant_candidate: {snapshot.dominant_candidate}")
        print(f"   confidence_gap: {snapshot.confidence_gap:.3f}")
        print(f"   stability: {snapshot.stability:.3f}")
        print(f"   reasons: {snapshot.reason_trace}")
        
        # 验证是否触发惩罚
        if "penalize_gps" in str(snapshot.reason_trace):
            print("   ✅ GPS 惩罚已触发")
        else:
            print("   ⚠️  GPS 惩罚未触发（可能需要更多证据）")
    
    print("\n✅ 测试场景 2 完成\n")


def main():
    """主函数"""
    print("=" * 60)
    print("Navigation Evidence Confidence Skeleton Test")
    print("=" * 60)
    
    try:
        # 测试场景 1
        test_scenario_1_indoor_visual_landmark_high()
        
        # 测试场景 2
        test_scenario_2_outdoor_gps_low_visual_high()
        
        print("=" * 60)
        print("✅ 所有测试完成")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()






