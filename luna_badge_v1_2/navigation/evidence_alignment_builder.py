"""
Evidence Alignment Builder (v1.4.8 Step 9)

对齐构建器：监听 TimelineFrame 和 LocalMap 更新，按时间窗进行对齐

关键参数（必须可配置）：
- ALIGNMENT_WINDOW_SEC = 0.75
- NODE_LOOKBACK_SEC = 2.0

核心逻辑：
- on TimelineFrame(ts): 找最近 LocalMapSnapshot，收集时间窗内的节点和地标匹配
- 构建 EvidenceAlignmentFrame
- 发送给 EvidenceAlignmentIndex

要求：
- Builder 不负责存储
- Builder 不维护历史
- Builder 不做任何判断/过滤
"""

from typing import Optional, List, Dict
import time
from navigation.evidence_alignment_frame import EvidenceAlignmentFrame
from navigation.authority_confidence_timeline import AuthorityConfidenceFrame
from navigation.events import (
    LocalMapUpdatedEvent,
    LandmarkMatchEvent,
)


class EvidenceAlignmentBuilder:
    """
    证据对齐构建器
    
    职责：
    - 监听 TimelineFrame（Step 8）
    - 监听 LocalMap 更新/landmark match（Step 4）
    - 按时间窗进行最近邻对齐
    - 构建 EvidenceAlignmentFrame
    """
    
    def __init__(
        self,
        alignment_window_sec: float = 0.75,
        node_lookback_sec: float = 2.0
    ):
        """
        初始化对齐构建器
        
        Args:
            alignment_window_sec: 对齐时间窗（秒，默认 0.75）
            node_lookback_sec: 节点回看时间（秒，默认 2.0）
        """
        self.alignment_window_sec = alignment_window_sec
        self.node_lookback_sec = node_lookback_sec
        
        # 缓存最近的地图更新和地标匹配事件（用于时间对齐）
        self._local_map_updates: List[LocalMapUpdatedEvent] = []
        self._landmark_matches: List[LandmarkMatchEvent] = []
        
        # 清理阈值（避免内存无限增长）
        self._max_cached_events = 100
    
    def on_local_map_updated(self, event: LocalMapUpdatedEvent) -> None:
        """
        处理本地地图更新事件
        
        Args:
            event: 本地地图更新事件
        """
        self._local_map_updates.append(event)
        
        # 清理过期事件（保留最近 N 个）
        if len(self._local_map_updates) > self._max_cached_events:
            self._local_map_updates.pop(0)
    
    def on_landmark_matched(self, event: LandmarkMatchEvent) -> None:
        """
        处理地标匹配事件
        
        Args:
            event: 地标匹配事件
        """
        self._landmark_matches.append(event)
        
        # 清理过期事件（保留最近 N 个）
        if len(self._landmark_matches) > self._max_cached_events:
            self._landmark_matches.pop(0)
    
    def build_alignment_frame(
        self,
        timeline_frame: AuthorityConfidenceFrame,
        scene: str
    ) -> Optional[EvidenceAlignmentFrame]:
        """
        构建对齐帧
        
        Args:
            timeline_frame: Timeline 帧（来自 Step 8）
            scene: 当前场景
            
        Returns:
            EvidenceAlignmentFrame: 如果成功构建，返回对齐帧；否则返回 None
        """
        ts = timeline_frame.ts
        
        # 1. 找最近 LocalMapSnapshot（<= ts）
        local_map_id = None
        recent_node_ids: List[str] = []
        
        # 找到最近的地图更新（时间 <= ts）
        recent_map_update: Optional[LocalMapUpdatedEvent] = None
        for event in reversed(self._local_map_updates):
            if event.ts <= ts:
                recent_map_update = event
                local_map_id = event.map_id
                break
        
        # 2. 收集时间窗内的节点和地标匹配
        # 时间窗：[ts - node_lookback_sec, ts + alignment_window_sec]
        window_start = ts - self.node_lookback_sec
        window_end = ts + self.alignment_window_sec
        
        # 收集地标匹配事件
        landmark_ids: List[str] = []
        match_scores: Dict[str, float] = {}
        
        for match_event in self._landmark_matches:
            if window_start <= match_event.ts <= window_end:
                landmark_ids.append(match_event.label)
                match_scores[match_event.label] = match_event.match_score
        
        # 收集节点 ID（简化版：假设地图更新事件包含节点信息）
        # 注意：由于 Step 4 可能没有直接提供节点 ID 列表，
        # 这里使用占位逻辑（实际实现需要根据 Step 4 的接口调整）
        if recent_map_update:
            # 简化：使用 map_id 作为节点标识（实际应从 LocalMap 获取节点列表）
            # 这里假设有节点，但具体 ID 需要从 LocalMap 数据获取
            # 为了不侵入 Step 4，这里暂时留空或使用占位值
            pass
        
        # 3. 构建 EvidenceAlignmentFrame
        alignment_frame = EvidenceAlignmentFrame(
            ts=ts,
            scene=scene,
            active_authority=timeline_frame.active_authority,
            candidate_authority=timeline_frame.candidate_authority,
            confidence=timeline_frame.confidence.copy(),
            takeover_state=timeline_frame.takeover_state,
            hint_active=timeline_frame.hint_active,
            local_map_id=local_map_id,
            recent_node_ids=recent_node_ids,
            landmark_ids=landmark_ids,
            match_scores=match_scores.copy(),
            reason_trace=[]
        )
        
        return alignment_frame
    
    def clear_cache(self) -> None:
        """清空缓存（用于测试）"""
        self._local_map_updates.clear()
        self._landmark_matches.clear()






