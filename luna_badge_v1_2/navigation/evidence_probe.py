"""
Evidence Probe (v1.4.8 Step 5)

重要禁令：
- 本模块当前为 Skeleton 插桩版，不得修改现有导航控制逻辑
- 只做桥接：把 Step1-4 输出变成 Evidence
- 不参与导航决策
"""

import time
from collections import deque
from typing import Optional
from navigation.evidence_bus import EvidenceBus
from navigation.confidence_model import ConfidenceModel
from navigation.evidence_models import (
    Evidence, EvidenceSource, EvidenceKind, AuthorityConfidenceSnapshot
)
from navigation.events import (
    SceneDecisionEvent,
    LandmarkMatchEvent,
    PositionUpdateEvent,
    EvidenceIngestEvent,
    AuthorityConfidenceSnapshotEvent,
    TOPIC_SCENE_DECISION,
    TOPIC_LANDMARK_MATCH,
    TOPIC_POSITION_UPDATE,
    TOPIC_EVIDENCE_INGEST,
    TOPIC_CONFIDENCE_SNAPSHOT,
)


class EvidenceProbe:
    """
    证据探针：桥接器
    
    功能：
    - 订阅 Step1-4 相关事件
    - 将它们转成 EvidenceIngestEvent 并送入 EvidenceBus
    - 周期性触发 compute，发布 SnapshotEvent
    """
    
    def __init__(self, event_bus=None, logger=None, window_s: float = 10.0, 
                 enable_debug_log: bool = False):
        """
        初始化证据探针
        
        Args:
            event_bus: 事件总线（可选）
            logger: 日志记录器（可选）
            window_s: 时间窗口大小（秒）
            enable_debug_log: 是否启用调试日志
        """
        self.event_bus = event_bus
        self.logger = logger
        self.window_s = window_s
        
        # 初始化 EvidenceBus 和 ConfidenceModel
        self.evidence_bus = EvidenceBus(window_s=window_s, enable_debug_log=enable_debug_log)
        self.confidence_model = ConfidenceModel(window_s=window_s)
        
        # 用于计算 visual_stability 的滑动窗口
        self._visual_confidence_history: deque = deque(maxlen=10)  # 最近 10 个值
        
        # 订阅事件
        if self.event_bus:
            self._subscribe_events()
    
    def _subscribe_events(self) -> None:
        """订阅 Step1-4 相关事件"""
        if self.event_bus:
            self.event_bus.subscribe(TOPIC_SCENE_DECISION, self._on_scene_decision)
            self.event_bus.subscribe(TOPIC_LANDMARK_MATCH, self._on_landmark_match)
            self.event_bus.subscribe(TOPIC_POSITION_UPDATE, self._on_position_update)
    
    def _on_scene_decision(self, event: SceneDecisionEvent) -> None:
        """处理场景决策事件"""
        # 映射规则：SceneDecisionEvent -> Evidence
        scene_type_name = event.scene_type.name if hasattr(event.scene_type, 'name') else str(event.scene_type)
        
        if scene_type_name == "INDOOR":
            kind = EvidenceKind.SCENE_INDOOR
        elif scene_type_name == "OUTDOOR":
            kind = EvidenceKind.SCENE_OUTDOOR
        elif scene_type_name == "TRANSITION":
            kind = EvidenceKind.SCENE_TRANSITION
        else:
            return
        
        evidence = Evidence(
            source=EvidenceSource.SYSTEM,
            kind=kind,
            value=event.confidence,
            ts=event.ts,
            ttl_s=5.0,  # 场景证据 TTL = 5s
            meta={"reason": event.reason}
        )
        
        self._ingest_evidence(evidence)
    
    def _on_landmark_match(self, event: LandmarkMatchEvent) -> None:
        """处理地标匹配事件"""
        # 映射规则：LandmarkMatchEvent -> Evidence
        evidence = Evidence(
            source=EvidenceSource.MAP,
            kind=EvidenceKind.LANDMARK_MATCH,
            value=event.match_score,
            ts=event.ts,
            ttl_s=8.0,  # 地标匹配证据 TTL = 8s
            meta={
                "label": event.label,
                "matched_node_id": event.matched_node_id,
                "reason": event.reason
            }
        )
        
        self._ingest_evidence(evidence)
    
    def _on_position_update(self, event: PositionUpdateEvent) -> None:
        """处理位置更新事件（用于计算 visual_stability）"""
        # 添加到滑动窗口
        self._visual_confidence_history.append(event.visual_confidence)
        
        # 计算滑动均值作为 VISUAL_STABILITY
        if len(self._visual_confidence_history) >= 3:  # 至少 3 个值
            visual_stability = sum(self._visual_confidence_history) / len(self._visual_confidence_history)
            
            evidence = Evidence(
                source=EvidenceSource.VISUAL,
                kind=EvidenceKind.VISUAL_STABILITY,
                value=visual_stability,
                ts=event.ts,
                ttl_s=5.0,  # 视觉稳定性证据 TTL = 5s
                meta={"window_size": len(self._visual_confidence_history)}
            )
            
            self._ingest_evidence(evidence)
    
    def _ingest_evidence(self, evidence: Evidence) -> None:
        """摄入证据"""
        self.evidence_bus.add(evidence)
        
        # 发布 EvidenceIngestEvent
        if self.event_bus:
            ingest_event = EvidenceIngestEvent(
                ts=evidence.ts,
                source=evidence.source.value,
                kind=evidence.kind.value,
                value=evidence.value,
                ttl_s=evidence.ttl_s,
                meta=evidence.meta
            )
            self.event_bus.publish(TOPIC_EVIDENCE_INGEST, ingest_event)
        
        # 触发快照计算
        self._compute_and_publish_snapshot()
    
    def _compute_and_publish_snapshot(self) -> None:
        """计算并发布快照"""
        now_ts = time.time()
        
        # 获取窗口内证据
        evidences = self.evidence_bus.get_window(now_ts)
        
        # 计算快照
        snapshot = self.confidence_model.compute(now_ts, evidences)
        
        # 发布快照事件
        if self.event_bus:
            snapshot_event = AuthorityConfidenceSnapshotEvent(
                ts=snapshot.ts,
                visual_score=snapshot.visual_score,
                map_vision_score=snapshot.map_vision_score,
                gps_score=snapshot.gps_score,
                dominant_candidate=snapshot.dominant_candidate,
                confidence_gap=snapshot.confidence_gap,
                stability=snapshot.stability,
                decay_state=snapshot.decay_state,
                reason_trace=snapshot.reason_trace,
                window_s=snapshot.window_s
            )
            self.event_bus.publish(TOPIC_CONFIDENCE_SNAPSHOT, snapshot_event)
    
    def ingest_gps_stability(self, value: float, ttl_s: float = 5.0) -> None:
        """
        手动摄入 GPS 稳定性证据（骨架版可留空，但代码要支持 future ingest）
        
        Args:
            value: GPS 稳定性值（0..1）
            ttl_s: Time To Live（秒）
        """
        evidence = Evidence(
            source=EvidenceSource.GPS,
            kind=EvidenceKind.GPS_STABILITY,
            value=value,
            ts=time.time(),
            ttl_s=ttl_s,
            meta={}
        )
        self._ingest_evidence(evidence)
    
    def get_snapshot(self) -> Optional[AuthorityConfidenceSnapshot]:
        """
        获取当前快照（手动调用）
        
        Returns:
            当前快照，如果无证据则返回 None
        """
        now_ts = time.time()
        evidences = self.evidence_bus.get_window(now_ts)
        
        if not evidences:
            return None
        
        return self.confidence_model.compute(now_ts, evidences)






