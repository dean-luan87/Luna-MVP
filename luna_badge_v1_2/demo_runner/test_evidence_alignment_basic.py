"""
Evidence Alignment Basic Test (v1.4.8 Step 9)

最小自测：验证 Step 9 对齐功能

测试要求：
1. 构造模拟 TimelineFrame（2Hz）
2. 构造模拟 LocalMap 更新（不规则）
3. 验证：
   - Frame 能成功对齐
   - local_map_id 可为空
   - landmark_ids 正确收集
4. RingBuffer 生效（超过 MAX 后长度不增长）
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

from navigation.authority_confidence_timeline import AuthorityConfidenceFrame
from navigation.authority_confidence_timeline_probe import AuthorityConfidenceTimelineProbe
from navigation.evidence_alignment_probe import EvidenceAlignmentProbe
from navigation.events import (
    LocalMapUpdatedEvent,
    LandmarkMatchEvent,
    TOPIC_LOCAL_MAP_UPDATED,
    TOPIC_LANDMARK_MATCH,
)


def test_scenario_1_basic_alignment():
    """测试场景 1: 基础对齐功能"""
    print("=" * 60)
    print("测试场景 1: 基础对齐功能")
    print("=" * 60)
    
    event_bus = EventBus()
    logger = get_logger("test_alignment")
    
    # 创建 Timeline Probe（简化版，只用于测试）
    timeline_probe = AuthorityConfidenceTimelineProbe(
        event_bus=event_bus,
        logger=logger,
        enable_timeline=True,
        max_frames=100
    )
    
    # 创建 Alignment Probe
    alignment_probe = EvidenceAlignmentProbe(
        timeline_probe=timeline_probe,
        event_bus=event_bus,
        logger=logger,
        enable_alignment=True,
        max_frames=50
    )
    alignment_probe.set_scene("OUTDOOR")
    
    # 模拟 LocalMap 更新
    base_time = time.time()
    map_event_1 = LocalMapUpdatedEvent(
        ts=base_time + 0.5,
        map_id="map_001",
        node_count=5,
        edge_count=4
    )
    event_bus.publish(TOPIC_LOCAL_MAP_UPDATED, map_event_1)
    time.sleep(0.1)
    
    # 模拟地标匹配
    landmark_event_1 = LandmarkMatchEvent(
        ts=base_time + 1.0,
        label="crosswalk_1",
        match_score=0.82,
        matched_node_id="node_5",
        reason="strong_match"
    )
    event_bus.publish(TOPIC_LANDMARK_MATCH, landmark_event_1)
    time.sleep(0.1)
    
    # 模拟 Timeline Frame（2Hz，即每 0.5 秒一次）
    for i in range(5):
        timeline_frame = AuthorityConfidenceFrame(
            ts=base_time + i * 0.5,
            scene="OUTDOOR",
            active_authority="VISUAL",
            candidate_authority="MAP_VISION",
            confidence={"VISUAL": 0.7 + i * 0.02, "MAP_VISION": 0.6, "GPS": 0.3},
            takeover_state="LOCKING" if i >= 2 else "IDLE",
            hint_active=(i >= 2)
        )
        
        alignment_probe.on_timeline_frame(timeline_frame)
        time.sleep(0.1)
    
    # 验证对齐结果
    stats = alignment_probe.get_stats()
    print(f"\n✅ 测试场景 1 完成")
    print(f"   对齐帧数: {stats['frame_count']}")
    print(f"   地图数量: {stats['map_count']}")
    print(f"   主权分布: {stats['authority_count']}")
    
    # 验证 local_map_id 可为空（第一个帧可能在 map 更新之前）
    all_frames = alignment_probe.index.get_all()
    if all_frames:
        first_frame = all_frames[0]
        print(f"   第一个帧 local_map_id: {first_frame.local_map_id}")
        print(f"   ✅ local_map_id 可为空: {first_frame.local_map_id is None or first_frame.local_map_id == 'map_001'}")


def test_scenario_2_landmark_collection():
    """测试场景 2: 地标收集"""
    print("\n" + "=" * 60)
    print("测试场景 2: 地标收集")
    print("=" * 60)
    
    event_bus = EventBus()
    logger = get_logger("test_alignment")
    
    timeline_probe = AuthorityConfidenceTimelineProbe(
        event_bus=event_bus,
        logger=logger,
        enable_timeline=True
    )
    
    alignment_probe = EvidenceAlignmentProbe(
        timeline_probe=timeline_probe,
        event_bus=event_bus,
        logger=logger,
        enable_alignment=True
    )
    alignment_probe.set_scene("INDOOR")
    
    base_time = time.time()
    
    # 模拟多个地标匹配
    landmarks = [
        ("crosswalk_1", 0.82, base_time + 1.0),
        ("door_frame_2", 0.75, base_time + 1.5),
        ("elevator_1", 0.90, base_time + 2.0),
    ]
    
    for label, score, ts in landmarks:
        landmark_event = LandmarkMatchEvent(
            ts=ts,
            label=label,
            match_score=score,
            matched_node_id=f"node_{label}",
            reason="match"
        )
        event_bus.publish(TOPIC_LANDMARK_MATCH, landmark_event)
        time.sleep(0.1)
    
    # 模拟 Timeline Frame（在地标匹配期间）
    for i in range(5):
        timeline_frame = AuthorityConfidenceFrame(
            ts=base_time + i * 0.5,
            scene="INDOOR",
            active_authority="VISUAL",
            candidate_authority=None,
            confidence={"VISUAL": 0.8, "MAP_VISION": 0.4, "GPS": 0.0},
            takeover_state="IDLE",
            hint_active=False
        )
        alignment_probe.on_timeline_frame(timeline_frame)
        time.sleep(0.1)
    
    # 验证地标收集
    all_frames = alignment_probe.index.get_all()
    print(f"\n✅ 测试场景 2 完成")
    
    # 检查是否有帧包含地标
    frames_with_landmarks = [
        frame for frame in all_frames
        if frame.landmark_ids
    ]
    
    print(f"   总帧数: {len(all_frames)}")
    print(f"   包含地标的帧数: {len(frames_with_landmarks)}")
    
    if frames_with_landmarks:
        sample_frame = frames_with_landmarks[0]
        print(f"   地标 ID 列表: {sample_frame.landmark_ids}")
        print(f"   匹配分数: {sample_frame.match_scores}")
        print(f"   ✅ 地标收集正常")


def test_scenario_3_ring_buffer_limit():
    """测试场景 3: RingBuffer 上限测试"""
    print("\n" + "=" * 60)
    print("测试场景 3: RingBuffer 上限测试")
    print("=" * 60)
    
    event_bus = EventBus()
    logger = get_logger("test_alignment")
    
    timeline_probe = AuthorityConfidenceTimelineProbe(
        event_bus=event_bus,
        logger=logger,
        enable_timeline=True
    )
    
    # 创建 Alignment Probe（小上限用于测试）
    alignment_probe = EvidenceAlignmentProbe(
        timeline_probe=timeline_probe,
        event_bus=event_bus,
        logger=logger,
        enable_alignment=True,
        max_frames=10  # 小上限
    )
    alignment_probe.set_scene("OUTDOOR")
    
    # 生成超过上限的帧
    base_time = time.time()
    for i in range(20):  # 超过 max_frames=10
        timeline_frame = AuthorityConfidenceFrame(
            ts=base_time + i * 0.2,
            scene="OUTDOOR",
            active_authority="VISUAL",
            candidate_authority=None,
            confidence={"VISUAL": 0.7, "MAP_VISION": 0.5, "GPS": 0.3},
            takeover_state="IDLE",
            hint_active=False
        )
        alignment_probe.on_timeline_frame(timeline_frame)
        time.sleep(0.05)
    
    # 验证 RingBuffer 生效
    final_frames = alignment_probe.index.size()
    max_frames = alignment_probe.index.max_frames
    
    print(f"\n✅ 测试场景 3 完成")
    print(f"   最大帧数: {max_frames}")
    print(f"   实际帧数: {final_frames}")
    print(f"   ✅ RingBuffer 生效: {final_frames <= max_frames}")


def test_scenario_4_export_timeline():
    """测试场景 4: 导出时间轴"""
    print("\n" + "=" * 60)
    print("测试场景 4: 导出时间轴")
    print("=" * 60)
    
    event_bus = EventBus()
    logger = get_logger("test_alignment")
    
    timeline_probe = AuthorityConfidenceTimelineProbe(
        event_bus=event_bus,
        logger=logger,
        enable_timeline=True
    )
    
    alignment_probe = EvidenceAlignmentProbe(
        timeline_probe=timeline_probe,
        event_bus=event_bus,
        logger=logger,
        enable_alignment=True
    )
    alignment_probe.set_scene("OUTDOOR")
    
    base_time = time.time()
    
    # 模拟 LocalMap 更新
    map_event = LocalMapUpdatedEvent(
        ts=base_time + 0.5,
        map_id="map_test",
        node_count=3,
        edge_count=2
    )
    event_bus.publish(TOPIC_LOCAL_MAP_UPDATED, map_event)
    time.sleep(0.1)
    
    # 模拟 Timeline Frame
    for i in range(5):
        timeline_frame = AuthorityConfidenceFrame(
            ts=base_time + i * 0.5,
            scene="OUTDOOR",
            active_authority="MAP_VISION" if i >= 2 else "VISUAL",
            candidate_authority="MAP_VISION" if i < 2 else None,
            confidence={"VISUAL": 0.7 - i * 0.05, "MAP_VISION": 0.6 + i * 0.07, "GPS": 0.3},
            takeover_state="TAKEN" if i >= 3 else "LOCKING",
            hint_active=(i >= 2)
        )
        alignment_probe.on_timeline_frame(timeline_frame)
        time.sleep(0.1)
    
    # 导出文本时间轴
    text_timeline = alignment_probe.export_text_timeline()
    print(f"\n📊 文本时间轴:")
    print(text_timeline)
    
    # 导出 JSON
    json_timeline = alignment_probe.export_json()
    print(f"\n📊 JSON 长度: {len(json_timeline)} 字符")
    
    print(f"\n✅ 测试场景 4 完成")


def main():
    """主函数"""
    print("=" * 60)
    print("Evidence Alignment Basic Test")
    print("=" * 60)
    
    try:
        # 测试场景 1
        test_scenario_1_basic_alignment()
        
        # 测试场景 2
        test_scenario_2_landmark_collection()
        
        # 测试场景 3
        test_scenario_3_ring_buffer_limit()
        
        # 测试场景 4
        test_scenario_4_export_timeline()
        
        print("\n" + "=" * 60)
        print("✅ 所有测试完成")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()






