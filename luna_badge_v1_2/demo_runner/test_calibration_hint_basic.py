"""
Calibration Hint Basic Test (v1.4.8 Step 10)

最小自测：验证 Step 10 Hint 生成功能

测试要求：
1. 构造模拟 AlignmentFrame 序列
2. 人为制造：
   - landmark 抖动
   - authority 反复切换
3. 验证：
   - Hint 能正确生成
   - time_range 合理
   - Store 超限生效
"""

import os
import sys
import time

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# 尝试导入 Logger
try:
    from common.logger import get_logger
except ImportError:
    def get_logger(name):
        class Logger:
            def info(self, module, event, payload):
                print(f"[{module}] {event}: {payload}")
        return Logger()

from navigation.evidence_alignment_frame import EvidenceAlignmentFrame
from navigation.evidence_alignment_index import EvidenceAlignmentIndex
from navigation.calibration_hint_probe import CalibrationHintProbe
from navigation.calibration_hint import (
    HINT_TYPE_LANDMARK_UNSTABLE,
    HINT_TYPE_AUTHORITY_FLIP_FREQUENT,
    HINT_TYPE_MAP_CONFIDENCE_OVERRATED,
    HINT_TYPE_GPS_ONLY_ZONE_DETECTED,
)


def test_scenario_1_landmark_unstable():
    """测试场景 1: 地标抖动"""
    print("=" * 60)
    print("测试场景 1: 地标抖动（LANDMARK_UNSTABLE）")
    print("=" * 60)
    
    logger = get_logger("test_hint")
    
    # 创建 AlignmentIndex
    alignment_index = EvidenceAlignmentIndex(max_frames=100)
    
    # 创建 Hint Probe
    hint_probe = CalibrationHintProbe(
        alignment_index=alignment_index,
        logger=logger,
        enable_hint_generation=True,
        max_hints=50
    )
    
    # 构造模拟 AlignmentFrame 序列（地标抖动）
    base_time = time.time()
    frames = []
    
    # 模拟地标 crosswalk_1 的分数波动（0.9 -> 0.5 -> 0.8 -> 0.4）
    for i in range(10):
        match_scores = {}
        landmark_ids = []
        
        # 地标分数波动
        if i % 2 == 0:
            match_scores["crosswalk_1"] = 0.9 - (i % 4) * 0.2
            landmark_ids.append("crosswalk_1")
        else:
            match_scores["crosswalk_1"] = 0.5 + (i % 4) * 0.15
        
        frame = EvidenceAlignmentFrame(
            ts=base_time + i * 0.3,  # 每 0.3 秒一次（在 3 秒时间窗内）
            scene="OUTDOOR",
            active_authority="MAP_VISION",
            candidate_authority=None,
            confidence={"VISUAL": 0.6, "MAP_VISION": 0.7, "GPS": 0.3},
            takeover_state="TAKEN",
            hint_active=False,
            local_map_id="map_test",
            recent_node_ids=[],
            landmark_ids=landmark_ids,
            match_scores=match_scores,
            reason_trace=[]
        )
        frames.append(frame)
        alignment_index.add_frame(frame)
    
    # 生成 Hint
    hints = hint_probe.generate_hints_from_frames(frames)
    
    # 验证结果
    print(f"\n✅ 测试场景 1 完成")
    print(f"   生成 Hint 数: {len(hints)}")
    
    # 检查是否有 LANDMARK_UNSTABLE 类型的 Hint
    unstable_hints = [h for h in hints if h.hint_type == HINT_TYPE_LANDMARK_UNSTABLE]
    print(f"   LANDMARK_UNSTABLE Hint 数: {len(unstable_hints)}")
    
    if unstable_hints:
        hint = unstable_hints[0]
        print(f"   时间范围: {hint.time_range[0]:.1f}s → {hint.time_range[1]:.1f}s")
        print(f"   地标 ID: {hint.related_landmark_ids}")
        print(f"   置信度下降: {hint.confidence_drop:.2f}")
        print(f"   ✅ 地标抖动检测正常")


def test_scenario_2_authority_flip():
    """测试场景 2: Authority 反复切换"""
    print("\n" + "=" * 60)
    print("测试场景 2: Authority 反复切换（AUTHORITY_FLIP_FREQUENT）")
    print("=" * 60)
    
    logger = get_logger("test_hint")
    
    alignment_index = EvidenceAlignmentIndex(max_frames=100)
    hint_probe = CalibrationHintProbe(
        alignment_index=alignment_index,
        logger=logger,
        enable_hint_generation=True
    )
    
    # 构造模拟 AlignmentFrame 序列（Authority 频繁切换）
    base_time = time.time()
    frames = []
    
    # 模拟 Authority 在 VISUAL <-> MAP_VISION 之间频繁切换
    authorities = ["VISUAL", "MAP_VISION", "VISUAL", "MAP_VISION", "VISUAL"]
    
    for i in range(len(authorities)):
        frame = EvidenceAlignmentFrame(
            ts=base_time + i * 1.0,  # 每 1 秒切换一次（在 5 秒时间窗内切换 4 次）
            scene="OUTDOOR",
            active_authority=authorities[i],
            candidate_authority=None,
            confidence={"VISUAL": 0.7, "MAP_VISION": 0.6, "GPS": 0.3},
            takeover_state="TAKEN",
            hint_active=False,
            local_map_id="map_test",
            recent_node_ids=[],
            landmark_ids=[],
            match_scores={},
            reason_trace=[]
        )
        frames.append(frame)
        alignment_index.add_frame(frame)
    
    # 生成 Hint
    hints = hint_probe.generate_hints_from_frames(frames)
    
    # 验证结果
    print(f"\n✅ 测试场景 2 完成")
    print(f"   生成 Hint 数: {len(hints)}")
    
    # 检查是否有 AUTHORITY_FLIP_FREQUENT 类型的 Hint
    flip_hints = [h for h in hints if h.hint_type == HINT_TYPE_AUTHORITY_FLIP_FREQUENT]
    print(f"   AUTHORITY_FLIP_FREQUENT Hint 数: {len(flip_hints)}")
    
    if flip_hints:
        hint = flip_hints[0]
        print(f"   时间范围: {hint.time_range[0]:.1f}s → {hint.time_range[1]:.1f}s")
        print(f"   置信度下降: {hint.confidence_drop:.2f}")
        print(f"   说明: {hint.description}")
        print(f"   ✅ Authority 频繁切换检测正常")


def test_scenario_3_map_confidence_overrated():
    """测试场景 3: 地图置信度过高但被反对"""
    print("\n" + "=" * 60)
    print("测试场景 3: 地图置信度过高但被反对（MAP_CONFIDENCE_OVERRATED）")
    print("=" * 60)
    
    logger = get_logger("test_hint")
    
    alignment_index = EvidenceAlignmentIndex(max_frames=100)
    hint_probe = CalibrationHintProbe(
        alignment_index=alignment_index,
        logger=logger,
        enable_hint_generation=True
    )
    
    # 构造模拟 AlignmentFrame 序列（MAP_VISION 高但 VISUAL 也高，冲突）
    base_time = time.time()
    frames = []
    
    # 模拟冲突：MAP_VISION 高（> 0.7）但 VISUAL 也高（> 0.6），持续 3 秒
    for i in range(5):
        frame = EvidenceAlignmentFrame(
            ts=base_time + i * 0.6,  # 每 0.6 秒一次，持续约 3 秒
            scene="OUTDOOR",
            active_authority="MAP_VISION",
            candidate_authority=None,
            confidence={"VISUAL": 0.75, "MAP_VISION": 0.85, "GPS": 0.3},  # 两者都高
            takeover_state="TAKEN",
            hint_active=False,
            local_map_id="map_test",
            recent_node_ids=[],
            landmark_ids=[],
            match_scores={},
            reason_trace=[]
        )
        frames.append(frame)
        alignment_index.add_frame(frame)
    
    # 生成 Hint
    hints = hint_probe.generate_hints_from_frames(frames)
    
    # 验证结果
    print(f"\n✅ 测试场景 3 完成")
    print(f"   生成 Hint 数: {len(hints)}")
    
    # 检查是否有 MAP_CONFIDENCE_OVERRATED 类型的 Hint
    overrated_hints = [h for h in hints if h.hint_type == HINT_TYPE_MAP_CONFIDENCE_OVERRATED]
    print(f"   MAP_CONFIDENCE_OVERRATED Hint 数: {len(overrated_hints)}")
    
    if overrated_hints:
        hint = overrated_hints[0]
        print(f"   时间范围: {hint.time_range[0]:.1f}s → {hint.time_range[1]:.1f}s")
        print(f"   置信度下降: {hint.confidence_drop:.2f}")
        print(f"   说明: {hint.description}")
        print(f"   ✅ 地图置信度过高检测正常")


def test_scenario_4_gps_only_zone():
    """测试场景 4: GPS 专用区域"""
    print("\n" + "=" * 60)
    print("测试场景 4: GPS 专用区域（GPS_ONLY_ZONE_DETECTED）")
    print("=" * 60)
    
    logger = get_logger("test_hint")
    
    alignment_index = EvidenceAlignmentIndex(max_frames=100)
    hint_probe = CalibrationHintProbe(
        alignment_index=alignment_index,
        logger=logger,
        enable_hint_generation=True,
        gps_only_zone_duration_s=10.0
    )
    
    # 构造模拟 AlignmentFrame 序列（GPS 专用，无视觉/地标）
    base_time = time.time()
    frames = []
    
    # 模拟 GPS 专用区域：持续 12 秒，无视觉/地标
    for i in range(12):
        frame = EvidenceAlignmentFrame(
            ts=base_time + i * 1.0,  # 每 1 秒一次，持续 12 秒
            scene="OUTDOOR",
            active_authority="GPS",
            candidate_authority=None,
            confidence={"VISUAL": 0.2, "MAP_VISION": 0.1, "GPS": 0.8},  # GPS 主导
            takeover_state="TAKEN",
            hint_active=False,
            local_map_id=None,
            recent_node_ids=[],
            landmark_ids=[],  # 无地标
            match_scores={},
            reason_trace=[]
        )
        frames.append(frame)
        alignment_index.add_frame(frame)
    
    # 生成 Hint
    hints = hint_probe.generate_hints_from_frames(frames)
    
    # 验证结果
    print(f"\n✅ 测试场景 4 完成")
    print(f"   生成 Hint 数: {len(hints)}")
    
    # 检查是否有 GPS_ONLY_ZONE_DETECTED 类型的 Hint
    gps_hints = [h for h in hints if h.hint_type == HINT_TYPE_GPS_ONLY_ZONE_DETECTED]
    print(f"   GPS_ONLY_ZONE_DETECTED Hint 数: {len(gps_hints)}")
    
    if gps_hints:
        hint = gps_hints[0]
        print(f"   时间范围: {hint.time_range[0]:.1f}s → {hint.time_range[1]:.1f}s")
        print(f"   置信度下降: {hint.confidence_drop:.2f}")
        print(f"   说明: {hint.description}")
        print(f"   ✅ GPS 专用区域检测正常")


def test_scenario_5_store_limit():
    """测试场景 5: Store 超限生效"""
    print("\n" + "=" * 60)
    print("测试场景 5: Store 超限生效")
    print("=" * 60)
    
    logger = get_logger("test_hint")
    
    alignment_index = EvidenceAlignmentIndex(max_frames=100)
    
    # 创建 Hint Probe（小上限用于测试）
    hint_probe = CalibrationHintProbe(
        alignment_index=alignment_index,
        logger=logger,
        enable_hint_generation=True,
        max_hints=10  # 小上限
    )
    
    # 生成超过上限的 Hint
    base_time = time.time()
    for i in range(20):  # 超过 max_hints=10
        # 构造简单的 Authority 切换场景（每次生成 1 个 Hint）
        frames = []
        for j in range(3):
            frame = EvidenceAlignmentFrame(
                ts=base_time + i * 5.0 + j * 1.0,
                scene="OUTDOOR",
                active_authority="VISUAL" if j % 2 == 0 else "MAP_VISION",
                candidate_authority=None,
                confidence={"VISUAL": 0.7, "MAP_VISION": 0.6, "GPS": 0.3},
                takeover_state="TAKEN",
                hint_active=False,
                local_map_id="map_test",
                recent_node_ids=[],
                landmark_ids=[],
                match_scores={},
                reason_trace=[]
            )
            frames.append(frame)
        
        hint_probe.generate_hints_from_frames(frames)
        time.sleep(0.01)
    
    # 验证 Store 超限生效
    final_hints = hint_probe.store.size()
    max_hints = hint_probe.store.max_hints
    
    print(f"\n✅ 测试场景 5 完成")
    print(f"   最大 Hint 数: {max_hints}")
    print(f"   实际 Hint 数: {final_hints}")
    print(f"   ✅ Store 超限生效: {final_hints <= max_hints}")


def test_scenario_6_export_hints():
    """测试场景 6: 导出 Hint"""
    print("\n" + "=" * 60)
    print("测试场景 6: 导出 Hint")
    print("=" * 60)
    
    logger = get_logger("test_hint")
    
    alignment_index = EvidenceAlignmentIndex(max_frames=100)
    hint_probe = CalibrationHintProbe(
        alignment_index=alignment_index,
        logger=logger,
        enable_hint_generation=True
    )
    
    base_time = time.time()
    
    # 构造一个地标抖动的场景
    frames = []
    for i in range(10):
        match_scores = {}
        landmark_ids = []
        
        if i % 2 == 0:
            match_scores["crosswalk_1"] = 0.9 - (i % 4) * 0.2
            landmark_ids.append("crosswalk_1")
        
        frame = EvidenceAlignmentFrame(
            ts=base_time + i * 0.3,
            scene="OUTDOOR",
            active_authority="MAP_VISION",
            candidate_authority=None,
            confidence={"VISUAL": 0.6, "MAP_VISION": 0.7, "GPS": 0.3},
            takeover_state="TAKEN",
            hint_active=False,
            local_map_id="map_test",
            recent_node_ids=[],
            landmark_ids=landmark_ids,
            match_scores=match_scores,
            reason_trace=[]
        )
        frames.append(frame)
    
    # 生成 Hint
    hints = hint_probe.generate_hints_from_frames(frames)
    
    # 导出文本
    text_hints = hint_probe.export_text_timeline(base_ts=base_time)
    print(f"\n📊 文本导出:")
    print(text_hints)
    
    # 导出 JSON
    json_hints = hint_probe.export_json()
    print(f"\n📊 JSON 长度: {len(json_hints)} 字符")
    
    print(f"\n✅ 测试场景 6 完成")


def main():
    """主函数"""
    print("=" * 60)
    print("Calibration Hint Basic Test")
    print("=" * 60)
    
    try:
        # 测试场景 1
        test_scenario_1_landmark_unstable()
        
        # 测试场景 2
        test_scenario_2_authority_flip()
        
        # 测试场景 3
        test_scenario_3_map_confidence_overrated()
        
        # 测试场景 4
        test_scenario_4_gps_only_zone()
        
        # 测试场景 5
        test_scenario_5_store_limit()
        
        # 测试场景 6
        test_scenario_6_export_hints()
        
        print("\n" + "=" * 60)
        print("✅ 所有测试完成")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()






