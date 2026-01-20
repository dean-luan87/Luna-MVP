"""
Calibration Hint Builder (v1.4.8 Step 10)

Hint 构建器：从 EvidenceAlignmentIndex 中读取对齐帧，识别"值得反思的模式"

构建时机（v1.4.8）：
1. 一次导航片段结束
2. 或检测到异常片段（Authority 抖动 / 冲突）

Builder 必须支持的 Hint 类型（最小集）：
1. LANDMARK_UNSTABLE - 地标不稳定
2. AUTHORITY_FLIP_FREQUENT - Authority 频繁切换
3. MAP_CONFIDENCE_OVERRATED - 地图置信度过高但被反对
4. GPS_ONLY_ZONE_DETECTED - 长时间无视觉/地标，被迫用 GPS
"""

from typing import List, Optional
from navigation.calibration_hint import (
    CalibrationHint,
    HINT_TYPE_LANDMARK_UNSTABLE,
    HINT_TYPE_AUTHORITY_FLIP_FREQUENT,
    HINT_TYPE_MAP_CONFIDENCE_OVERRATED,
    HINT_TYPE_GPS_ONLY_ZONE_DETECTED,
)
from navigation.evidence_alignment_frame import EvidenceAlignmentFrame
from navigation.evidence_alignment_index import EvidenceAlignmentIndex


class CalibrationHintBuilder:
    """
    校准提示构建器
    
    职责：
    - 从 EvidenceAlignmentIndex 中读取对齐帧
    - 识别"值得反思的模式"
    - 生成 CalibrationHint（候选）
    """
    
    def __init__(
        self,
        landmark_unstable_window_s: float = 3.0,
        authority_flip_window_s: float = 5.0,
        authority_flip_threshold: int = 3,
        gps_only_zone_duration_s: float = 10.0
    ):
        """
        初始化构建器
        
        Args:
            landmark_unstable_window_s: 地标不稳定时间窗（秒，默认 3.0）
            authority_flip_window_s: Authority 切换时间窗（秒，默认 5.0）
            authority_flip_threshold: Authority 切换阈值（次数，默认 3）
            gps_only_zone_duration_s: GPS 专用区域持续时间（秒，默认 10.0）
        """
        self.landmark_unstable_window_s = landmark_unstable_window_s
        self.authority_flip_window_s = authority_flip_window_s
        self.authority_flip_threshold = authority_flip_threshold
        self.gps_only_zone_duration_s = gps_only_zone_duration_s
    
    def build_hints_from_frames(
        self,
        frames: List[EvidenceAlignmentFrame]
    ) -> List[CalibrationHint]:
        """
        从对齐帧列表构建 Hint
        
        Args:
            frames: 对齐帧列表（必须按时间排序）
            
        Returns:
            CalibrationHint 列表
        """
        if not frames:
            return []
        
        hints: List[CalibrationHint] = []
        
        # 1. 检测 LANDMARK_UNSTABLE
        hints.extend(self._detect_landmark_unstable(frames))
        
        # 2. 检测 AUTHORITY_FLIP_FREQUENT
        hints.extend(self._detect_authority_flip_frequent(frames))
        
        # 3. 检测 MAP_CONFIDENCE_OVERRATED
        hints.extend(self._detect_map_confidence_overrated(frames))
        
        # 4. 检测 GPS_ONLY_ZONE_DETECTED
        hints.extend(self._detect_gps_only_zone(frames))
        
        return hints
    
    def _detect_landmark_unstable(
        self,
        frames: List[EvidenceAlignmentFrame]
    ) -> List[CalibrationHint]:
        """
        检测地标不稳定
        
        触发条件：
        - 同一 landmark id
        - 在短时间窗内（≤ 3s）
        - 多次 match / unmatch 或 score 剧烈波动
        """
        hints: List[CalibrationHint] = []
        
        # 按地标分组，检查每个地标的时间序列
        landmark_history: dict[str, List[tuple[float, float]]] = {}  # {landmark_id: [(ts, score), ...]}
        
        for frame in frames:
            for landmark_id in frame.landmark_ids:
                if landmark_id not in landmark_history:
                    landmark_history[landmark_id] = []
                
                score = frame.match_scores.get(landmark_id, 0.0)
                landmark_history[landmark_id].append((frame.ts, score))
        
        # 检查每个地标的不稳定性
        for landmark_id, history in landmark_history.items():
            if len(history) < 2:
                continue
            
            # 检查时间窗内的波动
            for i, (ts1, score1) in enumerate(history):
                window_end = ts1 + self.landmark_unstable_window_s
                
                # 收集时间窗内的分数
                window_scores = [score1]
                for j in range(i + 1, len(history)):
                    ts2, score2 = history[j]
                    if ts2 > window_end:
                        break
                    window_scores.append(score2)
                
                # 检查波动（如果分数差异大，说明不稳定）
                if len(window_scores) >= 2:
                    score_range = max(window_scores) - min(window_scores)
                    if score_range > 0.3:  # 阈值：分数差异超过 0.3
                        # 找到时间范围
                        start_ts = ts1
                        end_ts = min(
                            ts for ts, _ in history[i:i+len(window_scores)]
                        ) + self.landmark_unstable_window_s
                        
                        # 找到相关的 map_id
                        related_map_ids = [
                            frame.local_map_id
                            for frame in frames
                            if start_ts <= frame.ts <= end_ts
                            and frame.local_map_id
                        ]
                        related_map_ids = list(set(related_map_ids))
                        
                        hint = CalibrationHint(
                            hint_type=HINT_TYPE_LANDMARK_UNSTABLE,
                            authority="MAP_VISION",  # 地标不稳定影响 MAP_VISION
                            confidence_drop=score_range,
                            related_map_ids=related_map_ids,
                            related_landmark_ids=[landmark_id],
                            time_range=(start_ts, end_ts),
                            description=f"landmark {landmark_id} matched/unmatched repeatedly, score range {score_range:.2f}"
                        )
                        hints.append(hint)
                        
                        # 只报告第一次检测到的不稳定
                        break
        
        return hints
    
    def _detect_authority_flip_frequent(
        self,
        frames: List[EvidenceAlignmentFrame]
    ) -> List[CalibrationHint]:
        """
        检测 Authority 频繁切换
        
        触发条件：
        - Authority 在短时间窗内（≤ 5s）
        - 多次切换（≥ 3 次）
        """
        hints: List[CalibrationHint] = []
        
        if len(frames) < 2:
            return hints
        
        # 检测切换
        for i in range(len(frames)):
            start_frame = frames[i]
            start_ts = start_frame.ts
            window_end = start_ts + self.authority_flip_window_s
            
            # 收集时间窗内的 authority 变化
            authorities = [start_frame.active_authority]
            for j in range(i + 1, len(frames)):
                frame = frames[j]
                if frame.ts > window_end:
                    break
                if frame.active_authority != authorities[-1]:
                    authorities.append(frame.active_authority)
            
            # 检查切换次数（切换次数 = len(authorities) - 1）
            flip_count = len(authorities) - 1
            if flip_count >= self.authority_flip_threshold:
                # 找到时间范围
                end_ts = min(
                    frame.ts for frame in frames[i:]
                    if frame.ts <= window_end
                )
                
                # 找到相关的 map_id 和 landmark_id
                related_map_ids = list(set([
                    frame.local_map_id
                    for frame in frames[i:]
                    if start_ts <= frame.ts <= end_ts
                    and frame.local_map_id
                ]))
                
                related_landmark_ids = []
                for frame in frames[i:]:
                    if start_ts <= frame.ts <= end_ts:
                        related_landmark_ids.extend(frame.landmark_ids)
                related_landmark_ids = list(set(related_landmark_ids))
                
                # 计算置信度下降（简化：使用切换次数作为指标）
                confidence_drop = min(0.5, flip_count * 0.1)
                
                hint = CalibrationHint(
                    hint_type=HINT_TYPE_AUTHORITY_FLIP_FREQUENT,
                    authority="UNKNOWN",  # 频繁切换涉及多个 authority
                    confidence_drop=confidence_drop,
                    related_map_ids=related_map_ids,
                    related_landmark_ids=related_landmark_ids,
                    time_range=(start_ts, end_ts),
                    description=f"authority flipped {flip_count} times in {end_ts - start_ts:.1f}s"
                )
                hints.append(hint)
                
                # 只报告第一次检测到的频繁切换
                break
        
        return hints
    
    def _detect_map_confidence_overrated(
        self,
        frames: List[EvidenceAlignmentFrame]
    ) -> List[CalibrationHint]:
        """
        检测地图置信度过高但被反对
        
        触发条件：
        - MAP_VISION confidence 高
        - 但 VISUAL / LANDMARK 长时间反对
        """
        hints: List[CalibrationHint] = []
        
        if len(frames) < 3:
            return hints
        
        # 检查连续帧中 MAP_VISION 高但 VISUAL 也高的情况（冲突）
        conflict_start_idx: Optional[int] = None
        
        for i, frame in enumerate(frames):
            map_score = frame.confidence.get("MAP_VISION", 0.0)
            visual_score = frame.confidence.get("VISUAL", 0.0)
            
            # 检测冲突：MAP_VISION 高（> 0.7）但 VISUAL 也高（> 0.6）
            if map_score > 0.7 and visual_score > 0.6:
                if conflict_start_idx is None:
                    conflict_start_idx = i
            else:
                # 冲突结束
                if conflict_start_idx is not None:
                    conflict_duration = frames[i-1].ts - frames[conflict_start_idx].ts
                    if conflict_duration >= 2.0:  # 至少持续 2 秒
                        start_frame = frames[conflict_start_idx]
                        end_frame = frames[i-1]
                        
                        # 计算置信度下降（简化：使用冲突时长）
                        confidence_drop = min(0.3, conflict_duration * 0.05)
                        
                        # 找到相关的 map_id 和 landmark_id
                        related_map_ids = list(set([
                            f.local_map_id
                            for f in frames[conflict_start_idx:i]
                            if f.local_map_id
                        ]))
                        
                        related_landmark_ids = []
                        for f in frames[conflict_start_idx:i]:
                            related_landmark_ids.extend(f.landmark_ids)
                        related_landmark_ids = list(set(related_landmark_ids))
                        
                        hint = CalibrationHint(
                            hint_type=HINT_TYPE_MAP_CONFIDENCE_OVERRATED,
                            authority="MAP_VISION",
                            confidence_drop=confidence_drop,
                            related_map_ids=related_map_ids,
                            related_landmark_ids=related_landmark_ids,
                            time_range=(start_frame.ts, end_frame.ts),
                            description=f"MAP_VISION confidence high but VISUAL also high, conflict duration {conflict_duration:.1f}s"
                        )
                        hints.append(hint)
                    
                    conflict_start_idx = None
        
        return hints
    
    def _detect_gps_only_zone(
        self,
        frames: List[EvidenceAlignmentFrame]
    ) -> List[CalibrationHint]:
        """
        检测 GPS 专用区域
        
        触发条件：
        - 长时间无有效视觉/地标
        - Authority 被迫长期停留在 GPS
        """
        hints: List[CalibrationHint] = []
        
        if len(frames) < 3:
            return hints
        
        # 检查连续帧中 GPS 主导且无视觉/地标的情况
        gps_only_start_idx: Optional[int] = None
        
        for i, frame in enumerate(frames):
            is_gps_only = (
                frame.active_authority == "GPS"
                and not frame.landmark_ids
                and frame.confidence.get("VISUAL", 0.0) < 0.3
                and frame.confidence.get("MAP_VISION", 0.0) < 0.3
            )
            
            if is_gps_only:
                if gps_only_start_idx is None:
                    gps_only_start_idx = i
            else:
                # GPS 专用区域结束
                if gps_only_start_idx is not None:
                    gps_only_duration = frames[i-1].ts - frames[gps_only_start_idx].ts
                    if gps_only_duration >= self.gps_only_zone_duration_s:
                        start_frame = frames[gps_only_start_idx]
                        end_frame = frames[i-1]
                        
                        # 计算置信度下降
                        confidence_drop = min(0.4, gps_only_duration * 0.02)
                        
                        # 找到相关的 map_id（可能为空）
                        related_map_ids = list(set([
                            f.local_map_id
                            for f in frames[gps_only_start_idx:i]
                            if f.local_map_id
                        ]))
                        
                        hint = CalibrationHint(
                            hint_type=HINT_TYPE_GPS_ONLY_ZONE_DETECTED,
                            authority="GPS",
                            confidence_drop=confidence_drop,
                            related_map_ids=related_map_ids,
                            related_landmark_ids=[],
                            time_range=(start_frame.ts, end_frame.ts),
                            description=f"GPS-only zone detected, duration {gps_only_duration:.1f}s, no visual/landmark"
                        )
                        hints.append(hint)
                    
                    gps_only_start_idx = None
        
        return hints






