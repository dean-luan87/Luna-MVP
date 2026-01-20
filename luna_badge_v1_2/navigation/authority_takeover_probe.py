"""
Authority Takeover Probe (v1.4.8 Step 6)

重要禁令：
- 本模块当前为 Skeleton 插桩版，不得修改现有导航控制逻辑
- 只做桥接：Step5 → FSM
- FSM 只输出"接管建议事件"，不直接切换主权
"""

from typing import Optional
from navigation.authority_takeover_fsm import AuthorityTakeoverFSM
from navigation.evidence_models import AuthorityConfidenceSnapshot
from navigation.events import (
    AuthorityConfidenceSnapshotEvent,
    SceneDecisionEvent,
    TakeoverDecisionEvent,
    TOPIC_CONFIDENCE_SNAPSHOT,
    TOPIC_SCENE_DECISION,
    TOPIC_AUTHORITY_TAKEOVER_DECISION,
)


class AuthorityTakeoverProbe:
    """
    主权接管探针：桥接器
    
    功能：
    - 订阅 Step5 快照事件
    - 订阅场景决策事件
    - 调用 FSM.update
    - 若返回 TakeoverDecisionEvent → 发布
    """
    
    def __init__(
        self,
        event_bus=None,
        logger=None,
        enable_fsm: bool = False
    ):
        """
        初始化接管探针
        
        Args:
            event_bus: 事件总线（可选）
            logger: 日志记录器（可选）
            enable_fsm: 是否启用 FSM（Feature Flag，默认 False）
        """
        self.event_bus = event_bus
        self.logger = logger
        self.enable_fsm = enable_fsm
        
        # 初始化 FSM
        self.fsm = AuthorityTakeoverFSM(enable_fsm=enable_fsm)
        
        # 缓存最新场景和距离
        self.last_scene: Optional[str] = None
        self.last_distance_m: Optional[float] = None
        
        # 订阅事件
        if self.event_bus:
            self._subscribe_events()
    
    def _subscribe_events(self) -> None:
        """订阅相关事件"""
        if self.event_bus:
            self.event_bus.subscribe(TOPIC_CONFIDENCE_SNAPSHOT, self._on_snapshot)
            self.event_bus.subscribe(TOPIC_SCENE_DECISION, self._on_scene_decision)
    
    def _on_snapshot(self, event: AuthorityConfidenceSnapshotEvent) -> None:
        """处理快照事件"""
        if not self.enable_fsm:
            return
        
        # 重建 AuthorityConfidenceSnapshot（从事件字段）
        snapshot = AuthorityConfidenceSnapshot(
            visual_score=event.visual_score,
            map_vision_score=event.map_vision_score,
            gps_score=event.gps_score,
            dominant_candidate=event.dominant_candidate,
            confidence_gap=event.confidence_gap,
            stability=event.stability,
            decay_state=event.decay_state,
            reason_trace=event.reason_trace,
            ts=event.ts,
            window_s=event.window_s
        )
        
        # 调用 FSM.update
        import time
        decision = self.fsm.update(
            now_ts=time.time(),
            snapshot=snapshot,
            scene=self.last_scene or "OUTDOOR",  # 默认 OUTDOOR
            distance_m=self.last_distance_m
        )
        
        # 如果返回接管决策，发布事件
        if decision:
            self._publish_takeover_decision(decision)
        
        # 触发 Hint 更新（如果 Hint Probe 已注册）
        # 注意：这里不直接调用 Hint，而是通过事件机制
        # 如果外部注册了 Hint Probe，它可以通过定期检查 FSM 状态来生成 Hint
    
    def _on_scene_decision(self, event: SceneDecisionEvent) -> None:
        """处理场景决策事件"""
        # 缓存最新场景
        scene_name = event.scene_type.name if hasattr(event.scene_type, 'name') else str(event.scene_type)
        self.last_scene = scene_name
    
    def update_distance(self, distance_m: float) -> None:
        """
        更新距离（手动调用或通过事件）
        
        Args:
            distance_m: 当前距离（米）
        """
        self.last_distance_m = distance_m
    
    def _publish_takeover_decision(self, decision: TakeoverDecisionEvent) -> None:
        """发布接管决策事件"""
        if self.event_bus:
            self.event_bus.publish(TOPIC_AUTHORITY_TAKEOVER_DECISION, decision)
        
        # 日志
        reasons_str = ", ".join(decision.reason_trace) if decision.reason_trace else "none"
        log_msg = (
            f"[TAKEOVER_DECISION] authority={decision.target_authority} "
            f"score={decision.confidence:.3f} state={decision.state} reasons=[{reasons_str}]"
        )
        if self.logger:
            if hasattr(self.logger, 'info'):
                self.logger.info("AuthorityTakeoverProbe", "takeover_decision", {
                    "target_authority": decision.target_authority,
                    "confidence": decision.confidence,
                    "state": decision.state,
                    "reason_trace": decision.reason_trace
                })
            else:
                self.logger(log_msg)
        else:
            print(log_msg)






