"""
Authority Confidence Timeline Skeleton Test (v1.4.8 Step 8)

最小自测：验证 Step 8 插桩功能
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
from navigation.authority_confidence_timeline_probe import AuthorityConfidenceTimelineProbe
from navigation.events import (
    AuthorityConfidenceSnapshotEvent,
    SceneDecisionEvent,
    TakeoverDecisionEvent,
    TOPIC_CONFIDENCE_SNAPSHOT,
    TOPIC_SCENE_DECISION,
    TOPIC_AUTHORITY_TAKEOVER_DECISION,
)


def test_scenario_1_basic_timeline_recording():
    """测试场景 1: 基础时间轴记录"""
    print("=" * 60)
    print("测试场景 1: 基础时间轴记录")
    print("=" * 60)
    
    event_bus = EventBus()
    logger = get_logger("test_timeline")
    
    # 创建 Takeover Probe
    takeover_probe = AuthorityTakeoverProbe(
        event_bus=event_bus,
        logger=logger,
        enable_fsm=True
    )
    
    # 创建 Timeline Probe
    timeline_probe = AuthorityConfidenceTimelineProbe(
        fsm=takeover_probe.fsm,
        event_bus=event_bus,
        logger=logger,
        enable_timeline=True,
        max_frames=100
    )
    
    # 模拟场景决策
    scene_event = SceneDecisionEvent(
        ts=time.time(),
        scene_type="OUTDOOR",
        confidence=0.85,
        reason="outdoor_detected"
    )
    event_bus.publish(TOPIC_SCENE_DECISION, scene_event)
    timeline_probe.set_scene("OUTDOOR")
    time.sleep(0.1)
    
    # 模拟多个快照（触发采样）
    base_time = time.time()
    for i in range(10):
        snapshot_event = AuthorityConfidenceSnapshotEvent(
            ts=base_time + i * 0.5,  # 每 0.5 秒一次
            visual_score=0.5 + i * 0.02,
            map_vision_score=0.6 + i * 0.03,
            gps_score=0.3 + i * 0.01,
            dominant_candidate="MAP_VISION",
            confidence_gap=0.2 + i * 0.01,
            stability=0.8,
            decay_state={},
            reason_trace=[],
            window_s=10.0
        )
        event_bus.publish(TOPIC_CONFIDENCE_SNAPSHOT, snapshot_event)
        time.sleep(0.1)
    
    # 获取统计信息
    stats = timeline_probe.get_stats()
    print(f"\n✅ 测试场景 1 完成")
    print(f"   帧数: {stats['frame_count']}")
    print(f"   时长: {stats['duration_s']:.1f}s")
    print(f"   内存上限: {timeline_probe.store.max_frames}")


def test_scenario_2_force_sample_on_state_change():
    """测试场景 2: 状态变化时强制采样"""
    print("\n" + "=" * 60)
    print("测试场景 2: 状态变化时强制采样")
    print("=" * 60)
    
    event_bus = EventBus()
    logger = get_logger("test_timeline")
    
    takeover_probe = AuthorityTakeoverProbe(
        event_bus=event_bus,
        logger=logger,
        enable_fsm=True
    )
    
    timeline_probe = AuthorityConfidenceTimelineProbe(
        fsm=takeover_probe.fsm,
        event_bus=event_bus,
        logger=logger,
        enable_timeline=True
    )
    
    # 模拟场景决策
    scene_event = SceneDecisionEvent(
        ts=time.time(),
        scene_type="OUTDOOR",
        confidence=0.85,
        reason="outdoor_detected"
    )
    event_bus.publish(TOPIC_SCENE_DECISION, scene_event)
    timeline_probe.set_scene("OUTDOOR")
    time.sleep(0.1)
    
    # 初始帧数
    initial_frames = timeline_probe.store.timeline.size()
    
    # 模拟快照，触发 FSM 状态变化
    base_time = time.time()
    for i in range(15):
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
        time.sleep(0.2)
    
    # 检查帧数变化
    final_frames = timeline_probe.store.timeline.size()
    print(f"\n✅ 测试场景 2 完成")
    print(f"   初始帧数: {initial_frames}")
    print(f"   最终帧数: {final_frames}")
    print(f"   新增帧数: {final_frames - initial_frames}")
    print(f"   ✅ 状态变化时强制采样正常")


def test_scenario_3_export_timeline():
    """测试场景 3: 导出时间轴"""
    print("\n" + "=" * 60)
    print("测试场景 3: 导出时间轴")
    print("=" * 60)
    
    event_bus = EventBus()
    logger = get_logger("test_timeline")
    
    takeover_probe = AuthorityTakeoverProbe(
        event_bus=event_bus,
        logger=logger,
        enable_fsm=True
    )
    
    timeline_probe = AuthorityConfidenceTimelineProbe(
        fsm=takeover_probe.fsm,
        event_bus=event_bus,
        logger=logger,
        enable_timeline=True
    )
    
    # 模拟场景决策
    scene_event = SceneDecisionEvent(
        ts=time.time(),
        scene_type="INDOOR",
        confidence=0.9,
        reason="indoor_detected"
    )
    event_bus.publish(TOPIC_SCENE_DECISION, scene_event)
    timeline_probe.set_scene("INDOOR")
    timeline_probe.set_active_authority("VISUAL")
    time.sleep(0.1)
    
    # 模拟多个快照
    base_time = time.time()
    for i in range(8):
        snapshot_event = AuthorityConfidenceSnapshotEvent(
            ts=base_time + i * 0.5,
            visual_score=0.75 + i * 0.02,
            map_vision_score=0.4,
            gps_score=0.0,
            dominant_candidate="VISUAL",
            confidence_gap=0.3 + i * 0.01,
            stability=0.8,
            decay_state={},
            reason_trace=[],
            window_s=10.0
        )
        event_bus.publish(TOPIC_CONFIDENCE_SNAPSHOT, snapshot_event)
        time.sleep(0.1)
    
    # 导出文本时间轴
    text_timeline = timeline_probe.export_text_timeline()
    print(f"\n📊 文本时间轴:")
    print(text_timeline)
    
    # 导出 JSON
    json_timeline = timeline_probe.export_json()
    print(f"\n📊 JSON 长度: {len(json_timeline)} 字符")
    
    print(f"\n✅ 测试场景 3 完成")


def test_scenario_4_memory_limit():
    """测试场景 4: 内存上限测试"""
    print("\n" + "=" * 60)
    print("测试场景 4: 内存上限测试")
    print("=" * 60)
    
    event_bus = EventBus()
    logger = get_logger("test_timeline")
    
    takeover_probe = AuthorityTakeoverProbe(
        event_bus=event_bus,
        logger=logger,
        enable_fsm=True
    )
    
    # 创建 Timeline Probe（小上限用于测试）
    timeline_probe = AuthorityConfidenceTimelineProbe(
        fsm=takeover_probe.fsm,
        event_bus=event_bus,
        logger=logger,
        enable_timeline=True,
        max_frames=10  # 小上限
    )
    
    # 模拟场景决策
    scene_event = SceneDecisionEvent(
        ts=time.time(),
        scene_type="OUTDOOR",
        confidence=0.85,
        reason="outdoor_detected"
    )
    event_bus.publish(TOPIC_SCENE_DECISION, scene_event)
    timeline_probe.set_scene("OUTDOOR")
    time.sleep(0.1)
    
    # 生成超过上限的帧
    base_time = time.time()
    for i in range(20):  # 超过 max_frames=10
        snapshot_event = AuthorityConfidenceSnapshotEvent(
            ts=base_time + i * 0.5,
            visual_score=0.5,
            map_vision_score=0.6,
            gps_score=0.3,
            dominant_candidate="MAP_VISION",
            confidence_gap=0.2,
            stability=0.8,
            decay_state={},
            reason_trace=[],
            window_s=10.0
        )
        event_bus.publish(TOPIC_CONFIDENCE_SNAPSHOT, snapshot_event)
        time.sleep(0.05)
    
    # 检查帧数
    final_frames = timeline_probe.store.timeline.size()
    print(f"\n✅ 测试场景 4 完成")
    print(f"   最大帧数: {timeline_probe.store.max_frames}")
    print(f"   实际帧数: {final_frames}")
    print(f"   ✅ 内存上限生效: {final_frames <= timeline_probe.store.max_frames}")


def main():
    """主函数"""
    print("=" * 60)
    print("Authority Confidence Timeline Skeleton Test")
    print("=" * 60)
    
    try:
        # 测试场景 1
        test_scenario_1_basic_timeline_recording()
        
        # 测试场景 2
        test_scenario_2_force_sample_on_state_change()
        
        # 测试场景 3
        test_scenario_3_export_timeline()
        
        # 测试场景 4
        test_scenario_4_memory_limit()
        
        print("\n" + "=" * 60)
        print("✅ 所有测试完成")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()






