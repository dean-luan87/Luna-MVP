"""
Authority Confidence Timeline Probe (v1.4.8 Step 8)

Timeline 探针：桥接器

职责：
- 监听 Step5 / Step6 / Step7 事件
- 触发采样
- 提供导出接口
"""

from typing import Optional
import time
from navigation.authority_confidence_store import AuthorityConfidenceStore
from navigation.authority_confidence_sampler import AuthorityConfidenceSampler
from navigation.authority_confidence_exporter import AuthorityConfidenceExporter
from navigation.authority_takeover_fsm import AuthorityTakeoverFSM
from navigation.events import (
    AuthorityConfidenceSnapshotEvent,
    TakeoverDecisionEvent,
    AuthorityLockHintEvent,
    TOPIC_CONFIDENCE_SNAPSHOT,
    TOPIC_AUTHORITY_TAKEOVER_DECISION,
    TOPIC_AUTHORITY_LOCK_HINT,
)


class AuthorityConfidenceTimelineProbe:
    """
    主权置信度时间轴探针：桥接器
    
    功能：
    - 监听 Step5 / Step6 / Step7 事件
    - 触发采样
    - 提供导出接口
    """
    
    def __init__(
        self,
        fsm: Optional[AuthorityTakeoverFSM] = None,
        event_bus=None,
        logger=None,
        enable_timeline: bool = True,
        max_frames: int = 300,
        sample_rate_hz: float = 2.0
    ):
        """
        初始化 Timeline 探针
        
        Args:
            fsm: FSM 实例（可选）
            event_bus: 事件总线（可选）
            logger: 日志记录器（可选）
            enable_timeline: 是否启用 Timeline（Feature Flag，默认 True）
            max_frames: 最大帧数（默认 300）
            sample_rate_hz: 采样频率（Hz，默认 2.0）
        """
        self.fsm = fsm
        self.event_bus = event_bus
        self.logger = logger
        self.enable_timeline = enable_timeline
        
        # 初始化存储、采样器、导出器
        self.store = AuthorityConfidenceStore(max_frames=max_frames)
        self.sampler = AuthorityConfidenceSampler(
            store=self.store,
            fsm=fsm,
            sample_rate_hz=sample_rate_hz,
            enable_sampling=enable_timeline
        )
        self.exporter = AuthorityConfidenceExporter(store=self.store)
        
        # 状态缓存
        self.last_snapshot: Optional[AuthorityConfidenceSnapshotEvent] = None
        self.last_active_authority: str = "UNKNOWN"
        self.last_scene: str = "OUTDOOR"
        self.hint_active: bool = False
        
        # 订阅事件
        if self.event_bus:
            self._subscribe_events()
    
    def _subscribe_events(self) -> None:
        """订阅相关事件"""
        if self.event_bus:
            self.event_bus.subscribe(TOPIC_CONFIDENCE_SNAPSHOT, self._on_snapshot)
            self.event_bus.subscribe(TOPIC_AUTHORITY_TAKEOVER_DECISION, self._on_takeover_decision)
            self.event_bus.subscribe(TOPIC_AUTHORITY_LOCK_HINT, self._on_lock_hint)
    
    def _on_snapshot(self, event: AuthorityConfidenceSnapshotEvent) -> None:
        """处理快照事件"""
        self.last_snapshot = event
        
        # 触发采样
        self._trigger_sample()
    
    def _on_takeover_decision(self, event: TakeoverDecisionEvent) -> None:
        """处理接管决策事件"""
        # 更新活动主权
        self.last_active_authority = event.target_authority
        
        # 强制采样（Authority 变化）
        self._trigger_sample(force=True)
    
    def _on_lock_hint(self, event: AuthorityLockHintEvent) -> None:
        """处理锁定提示事件"""
        self.hint_active = True
        
        # 触发采样
        self._trigger_sample()
    
    def _trigger_sample(self, force: bool = False) -> None:
        """触发采样"""
        if not self.enable_timeline or not self.last_snapshot:
            return
        
        # 构建置信度字典
        confidence = {
            "VISUAL": self.last_snapshot.visual_score,
            "MAP_VISION": self.last_snapshot.map_vision_score,
            "GPS": self.last_snapshot.gps_score,
        }
        
        # 确定候选主权
        candidate_authority = self.last_snapshot.dominant_candidate
        
        # 采样
        now_ts = time.time()
        if force:
            self.sampler.force_sample(
                now_ts=now_ts,
                active_authority=self.last_active_authority,
                candidate_authority=candidate_authority,
                scene=self.last_scene,
                confidence=confidence,
                hint_active=self.hint_active
            )
        else:
            self.sampler.sample(
                now_ts=now_ts,
                active_authority=self.last_active_authority,
                candidate_authority=candidate_authority,
                scene=self.last_scene,
                confidence=confidence,
                hint_active=self.hint_active
            )
        
        # 重置 Hint 标志（下次采样时如果无 Hint 则自动设为 False）
        self.hint_active = False
    
    def set_scene(self, scene: str) -> None:
        """设置当前场景"""
        self.last_scene = scene
    
    def set_active_authority(self, authority: str) -> None:
        """设置当前活动主权"""
        self.last_active_authority = authority
    
    def export_json(self, start_ts: Optional[float] = None, end_ts: Optional[float] = None) -> str:
        """导出为 JSON"""
        return self.exporter.export_json(start_ts=start_ts, end_ts=end_ts)
    
    def export_text_timeline(self, start_ts: Optional[float] = None, end_ts: Optional[float] = None) -> str:
        """导出为 ASCII 文本时间轴"""
        return self.exporter.export_text_timeline(start_ts=start_ts, end_ts=end_ts)
    
    def get_stats(self) -> dict:
        """获取统计信息"""
        stats = self.store.get_stats()
        
        # 记录日志（低频）
        if self.logger and stats["frame_count"] > 0:
            log_msg = (
                f"[TIMELINE] frames={stats['frame_count']} "
                f"oldest_ts={stats['oldest_ts']:.2f} "
                f"newest_ts={stats['newest_ts']:.2f} "
                f"duration={stats['duration_s']:.1f}s"
            )
            if hasattr(self.logger, 'info'):
                self.logger.info("AuthorityConfidenceTimelineProbe", "timeline_stats", stats)
            else:
                self.logger(log_msg)
        
        return stats






