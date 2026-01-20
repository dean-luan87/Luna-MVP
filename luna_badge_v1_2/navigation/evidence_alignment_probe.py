"""
Evidence Alignment Probe (v1.4.8 Step 9)

对齐探针：桥接器

职责：
- 监听 TimelineFrame（Step 8）
- 监听 LocalMap 更新/landmark match（Step 4）
- 调用 Builder 构建对齐帧
- 调用 Index 存储对齐帧
- 提供导出接口
"""

from typing import Optional
import time
from navigation.evidence_alignment_builder import EvidenceAlignmentBuilder
from navigation.evidence_alignment_index import EvidenceAlignmentIndex
from navigation.evidence_alignment_exporter import EvidenceAlignmentExporter
from navigation.authority_confidence_timeline import AuthorityConfidenceFrame
from navigation.authority_confidence_timeline_probe import AuthorityConfidenceTimelineProbe
from navigation.events import (
    LocalMapUpdatedEvent,
    LandmarkMatchEvent,
    TOPIC_LOCAL_MAP_UPDATED,
    TOPIC_LANDMARK_MATCH,
)


class EvidenceAlignmentProbe:
    """
    证据对齐探针：桥接器
    
    功能：
    - 监听 Step 4 / Step 8 事件
    - 构建对齐帧
    - 存储对齐帧
    - 提供导出接口
    """
    
    def __init__(
        self,
        timeline_probe: Optional[AuthorityConfidenceTimelineProbe] = None,
        event_bus=None,
        logger=None,
        enable_alignment: bool = True,
        max_frames: int = 300,
        alignment_window_sec: float = 0.75,
        node_lookback_sec: float = 2.0
    ):
        """
        初始化对齐探针
        
        Args:
            timeline_probe: Timeline 探针（用于获取 Timeline Frame）
            event_bus: 事件总线（可选）
            logger: 日志记录器（可选）
            enable_alignment: 是否启用对齐（Feature Flag，默认 True）
            max_frames: 最大帧数（默认 300）
            alignment_window_sec: 对齐时间窗（秒，默认 0.75）
            node_lookback_sec: 节点回看时间（秒，默认 2.0）
        """
        self.timeline_probe = timeline_probe
        self.event_bus = event_bus
        self.logger = logger
        self.enable_alignment = enable_alignment
        
        # 初始化 Builder、Index、Exporter
        self.builder = EvidenceAlignmentBuilder(
            alignment_window_sec=alignment_window_sec,
            node_lookback_sec=node_lookback_sec
        )
        self.index = EvidenceAlignmentIndex(max_frames=max_frames)
        self.exporter = EvidenceAlignmentExporter()
        
        # 状态缓存
        self.last_scene: str = "OUTDOOR"
        
        # 订阅事件
        if self.event_bus:
            self._subscribe_events()
    
    def _subscribe_events(self) -> None:
        """订阅相关事件"""
        if self.event_bus:
            self.event_bus.subscribe(TOPIC_LOCAL_MAP_UPDATED, self._on_local_map_updated)
            self.event_bus.subscribe(TOPIC_LANDMARK_MATCH, self._on_landmark_matched)
    
    def _on_local_map_updated(self, event: LocalMapUpdatedEvent) -> None:
        """处理本地地图更新事件"""
        if not self.enable_alignment:
            return
        
        self.builder.on_local_map_updated(event)
    
    def _on_landmark_matched(self, event: LandmarkMatchEvent) -> None:
        """处理地标匹配事件"""
        if not self.enable_alignment:
            return
        
        self.builder.on_landmark_matched(event)
    
    def on_timeline_frame(
        self,
        timeline_frame: AuthorityConfidenceFrame
    ) -> None:
        """
        处理 Timeline 帧（来自 Step 8）
        
        Args:
            timeline_frame: Timeline 帧
        """
        if not self.enable_alignment:
            return
        
        # 构建对齐帧
        alignment_frame = self.builder.build_alignment_frame(
            timeline_frame=timeline_frame,
            scene=self.last_scene
        )
        
        if alignment_frame:
            # 存储对齐帧
            self.index.add_frame(alignment_frame)
            
            # 日志（低频）
            if self.logger and self.index.size() % 10 == 0:
                stats = self.index.get_stats()
                log_msg = (
                    f"[ALIGN] frames={stats['frame_count']} "
                    f"maps={stats['map_count']} "
                    f"authorities={','.join(stats['authority_count'].keys())}"
                )
                if hasattr(self.logger, 'info'):
                    self.logger.info("EvidenceAlignmentProbe", "alignment_frame_added", stats)
                else:
                    self.logger(log_msg)
    
    def set_scene(self, scene: str) -> None:
        """设置当前场景"""
        self.last_scene = scene
    
    def export_json(
        self,
        start_ts: Optional[float] = None,
        end_ts: Optional[float] = None
    ) -> str:
        """导出为 JSON"""
        if start_ts is not None or end_ts is not None:
            frames = self.index.get_by_time_range(
                t0=start_ts or 0.0,
                t1=end_ts or float('inf')
            )
        else:
            frames = self.index.get_all()
        
        return self.exporter.export_json(frames)
    
    def export_text_timeline(
        self,
        start_ts: Optional[float] = None,
        end_ts: Optional[float] = None
    ) -> str:
        """导出为 ASCII 文本时间轴"""
        if start_ts is not None or end_ts is not None:
            frames = self.index.get_by_time_range(
                t0=start_ts or 0.0,
                t1=end_ts or float('inf')
            )
        else:
            frames = self.index.get_all()
        
        return self.exporter.export_text_timeline(frames)
    
    def get_stats(self) -> dict:
        """获取统计信息"""
        return self.index.get_stats()






