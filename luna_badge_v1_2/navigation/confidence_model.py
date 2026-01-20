"""
Confidence Model (v1.4.8 Step 5)

重要禁令：
- 本模块当前为 Skeleton 插桩版，不得修改现有导航控制逻辑
- ConfidenceModel 不是融合器，只提供"态势快照"
- Step3 仍是裁决者
"""

import math
from typing import List, Dict
import time
from navigation.evidence_models import (
    Evidence, AuthorityConfidenceSnapshot, EvidenceKind
)


class ConfidenceModel:
    """
    置信度模型：规则+衰减+冲突惩罚
    
    职责：
    - 计算 AuthorityConfidenceSnapshot
    - 实现证据衰减
    - 实现冲突惩罚
    """
    
    def __init__(self, window_s: float = 10.0):
        """
        初始化置信度模型
        
        Args:
            window_s: 时间窗口大小（秒）
        """
        self.window_s = window_s
        
        # 权重表（硬编码，可解释）
        self.weights = {
            "map_vision": {
                "landmark_match": 0.70,
                "visual_stability": 0.20,
                "path_consistency": 0.10,
            },
            "visual": {
                "visual_stability": 0.60,
                "path_consistency": 0.25,
                "landmark_match": 0.15,
            },
            "gps": {
                "gps_stability": 0.70,
                "path_consistency": 0.30,
            },
        }
    
    def compute(self, now_ts: float, evidences: List[Evidence]) -> AuthorityConfidenceSnapshot:
        """
        计算 AuthorityConfidenceSnapshot
        
        Args:
            now_ts: 当前时间戳
            evidences: 证据列表
            
        Returns:
            AuthorityConfidenceSnapshot: 置信度快照
        """
        # 1. 对证据做衰减并按 kind 聚合
        decay_state = self._aggregate_evidences(now_ts, evidences)
        
        # 2. 计算各分数
        map_vision_score = self._compute_map_vision_score(decay_state)
        visual_score = self._compute_visual_score(decay_state)
        gps_score = self._compute_gps_score(decay_state)
        
        # 3. 应用冲突惩罚
        reason_trace = []
        map_vision_score, visual_score, gps_score, penalty_reasons = self._apply_conflict_penalties(
            map_vision_score, visual_score, gps_score, decay_state
        )
        reason_trace.extend(penalty_reasons)
        
        # 4. 计算 dominant_candidate 和 confidence_gap
        scores = {
            "VISUAL": visual_score,
            "MAP_VISION": map_vision_score,
            "GPS": gps_score,
        }
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        dominant_candidate = sorted_scores[0][0] if sorted_scores[0][1] > 0 else None
        confidence_gap = sorted_scores[0][1] - sorted_scores[1][1] if len(sorted_scores) > 1 else 0.0
        
        # 5. 计算稳定性
        top1_score = sorted_scores[0][1]
        stability = self._compute_stability(top1_score, confidence_gap)
        
        # 6. 构建快照
        snapshot = AuthorityConfidenceSnapshot(
            visual_score=visual_score,
            map_vision_score=map_vision_score,
            gps_score=gps_score,
            dominant_candidate=dominant_candidate,
            confidence_gap=confidence_gap,
            stability=stability,
            decay_state=decay_state,
            reason_trace=reason_trace,
            ts=now_ts,
            window_s=self.window_s,
        )
        
        # 7. 日志
        self._log_snapshot(snapshot)
        
        return snapshot
    
    def _aggregate_evidences(self, now_ts: float, evidences: List[Evidence]) -> Dict[str, float]:
        """
        对证据做衰减并按 kind 聚合（取 max）
        
        Args:
            now_ts: 当前时间戳
            evidences: 证据列表
            
        Returns:
            聚合后的证据值字典
        """
        aggregated = {}
        
        for evidence in evidences:
            # 计算衰减后的值
            age = now_ts - evidence.ts
            if age <= evidence.ttl_s:
                # 指数衰减
                decay_factor = math.exp(-age / max(evidence.ttl_s, 1e-6))
                effective_value = evidence.value * decay_factor
            else:
                effective_value = 0.0
            
            # 按 kind 聚合（取 max）
            kind_key = evidence.kind.value
            if kind_key not in aggregated:
                aggregated[kind_key] = effective_value
            else:
                aggregated[kind_key] = max(aggregated[kind_key], effective_value)
        
        return aggregated
    
    def _compute_map_vision_score(self, decay_state: Dict[str, float]) -> float:
        """计算 map_vision_score"""
        weights = self.weights["map_vision"]
        score = (
            weights["landmark_match"] * decay_state.get("LANDMARK_MATCH", 0.0) +
            weights["visual_stability"] * decay_state.get("VISUAL_STABILITY", 0.0) +
            weights["path_consistency"] * decay_state.get("PATH_CONSISTENCY", 0.0)
        )
        return max(0.0, min(1.0, score))  # clamp to [0, 1]
    
    def _compute_visual_score(self, decay_state: Dict[str, float]) -> float:
        """计算 visual_score"""
        weights = self.weights["visual"]
        score = (
            weights["visual_stability"] * decay_state.get("VISUAL_STABILITY", 0.0) +
            weights["path_consistency"] * decay_state.get("PATH_CONSISTENCY", 0.0) +
            weights["landmark_match"] * decay_state.get("LANDMARK_MATCH", 0.0)
        )
        return max(0.0, min(1.0, score))  # clamp to [0, 1]
    
    def _compute_gps_score(self, decay_state: Dict[str, float]) -> float:
        """计算 gps_score"""
        weights = self.weights["gps"]
        score = (
            weights["gps_stability"] * decay_state.get("GPS_STABILITY", 0.0) +
            weights["path_consistency"] * decay_state.get("PATH_CONSISTENCY", 0.0)
        )
        return max(0.0, min(1.0, score))  # clamp to [0, 1]
    
    def _apply_conflict_penalties(
        self,
        map_vision_score: float,
        visual_score: float,
        gps_score: float,
        decay_state: Dict[str, float]
    ) -> tuple[float, float, float, List[str]]:
        """
        应用冲突惩罚
        
        规则：
        - 若 visual_stability > 0.7 且 gps_stability < 0.4：惩罚 GPS
        - 若 landmark_match > 0.75：加速锁定 MAP_VISION
        """
        reasons = []
        
        visual_stability = decay_state.get("VISUAL_STABILITY", 0.0)
        gps_stability = decay_state.get("GPS_STABILITY", 0.0)
        landmark_match = decay_state.get("LANDMARK_MATCH", 0.0)
        
        # 规则 1: Visual 稳定但 GPS 不稳定 → 惩罚 GPS
        if visual_stability > 0.7 and gps_stability < 0.4:
            gps_score *= 0.7
            reasons.append("penalize_gps_due_to_visual_stable_gps_unstable")
        
        # 规则 2: 强地标匹配 → 加速锁定 MAP_VISION
        if landmark_match > 0.75:
            map_vision_score = max(map_vision_score, 0.85)
            reasons.append("boost_map_vision_due_to_strong_landmark")
        
        # 限制范围
        map_vision_score = max(0.0, min(1.0, map_vision_score))
        visual_score = max(0.0, min(1.0, visual_score))
        gps_score = max(0.0, min(1.0, gps_score))
        
        return map_vision_score, visual_score, gps_score, reasons
    
    def _compute_stability(self, top1_score: float, confidence_gap: float) -> float:
        """
        计算稳定性
        
        stability = clamp(top1, 0..1) * clamp(gap*2, 0..1)
        """
        top1_clamped = max(0.0, min(1.0, top1_score))
        gap_clamped = max(0.0, min(1.0, confidence_gap * 2))
        return top1_clamped * gap_clamped
    
    def _log_snapshot(self, snapshot: AuthorityConfidenceSnapshot) -> None:
        """记录快照日志"""
        reasons_str = ",".join(snapshot.reason_trace) if snapshot.reason_trace else "none"
        print(
            f"[CONF_SNAPSHOT] vis={snapshot.visual_score:.3f} "
            f"map={snapshot.map_vision_score:.3f} gps={snapshot.gps_score:.3f} "
            f"dom={snapshot.dominant_candidate} gap={snapshot.confidence_gap:.3f} "
            f"stability={snapshot.stability:.3f} reasons=[{reasons_str}]"
        )






