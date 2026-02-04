"""
Authority Lock Hint Probe (v1.4.8 Step 7)

重要禁令：
- 本模块当前为 Skeleton 插桩版，不得修改现有导航控制逻辑
- 不修改 Step 6 FSM
- Hint 不得触发任何主权切换
- Hint 默认不接入 TTS
- 所有 Hint 必须可关闭

核心职责：
- 监听 FSM
- 生成 Hint
- 发布事件

关键点：Step 7 只监听 FSM，不反向控制 FSM（单向依赖，保证系统稳定）
"""

from typing import Optional
import time
from navigation.authority_lock_hint import (
    AuthorityLockHintEmitter,
    AuthorityLockHint
)
from navigation.authority_takeover_fsm import AuthorityTakeoverFSM, TakeoverState
from navigation.authority_takeover_rules import get_takeover_rule
from navigation.events import (
    AuthorityConfidenceSnapshotEvent,
    TOPIC_CONFIDENCE_SNAPSHOT,
)
from navigation.authority_lock_hint_rules import get_hint_rule


class AuthorityLockHintProbe:
    """
    主权锁定提示探针：桥接器
    
    功能：
    - 监听 FSM 状态（通过传入的 FSM 实例或事件）
    - 当 FSM.state == LOCKING → evaluate
    - 发布 AuthorityLockHintEvent
    """
    
    def __init__(
        self,
        fsm: AuthorityTakeoverFSM,
        event_bus=None,
        logger=None,
        enable_hint: bool = True
    ):
        """
        初始化 Hint 探针
        
        Args:
            fsm: AuthorityTakeoverFSM 实例（通过传入，不修改 Step 6）
            event_bus: 事件总线（可选）
            logger: 日志记录器（可选）
            enable_hint: 是否启用 Hint（Feature Flag，默认 True）
        """
        self.fsm = fsm  # 持有 FSM 引用（只读，不修改）
        self.event_bus = event_bus
        self.logger = logger
        self.enable_hint = enable_hint
        
        # 初始化 Hint 发射器
        self.hint_emitter = AuthorityLockHintEmitter(
            event_bus=event_bus,
            logger=logger,
            enable_hint=enable_hint
        )
        
        # 缓存最新快照（用于获取置信度）
        self.last_snapshot: Optional[AuthorityConfidenceSnapshotEvent] = None
        self.last_scene: str = "OUTDOOR"
        
        # 订阅事件
        if self.event_bus:
            self._subscribe_events()
    
    def _subscribe_events(self) -> None:
        """订阅相关事件"""
        if self.event_bus:
            self.event_bus.subscribe(TOPIC_CONFIDENCE_SNAPSHOT, self._on_snapshot)
    
    def _on_snapshot(self, event: AuthorityConfidenceSnapshotEvent) -> None:
        """处理快照事件（用于获取置信度）"""
        self.last_snapshot = event
    
    def update(self, scene: str = None) -> Optional[AuthorityLockHint]:
        """
        更新 Hint（周期性调用或事件触发）
        
        注意：这个方法需要在外部定期调用，或者在 FSM 状态变化时调用
        由于不修改 Step 6，我们需要通过这种方式来检查 FSM 状态
        
        Args:
            scene: 当前场景（可选）
            
        Returns:
            AuthorityLockHint: 如果满足条件，返回 Hint；否则返回 None
        """
        if not self.enable_hint:
            return None
        
        if scene:
            self.last_scene = scene
        
        # 检查 FSM 状态
        current_state = self.fsm.current_state
        context = self.fsm.context
        
        # 只在 LOCKING 状态发 Hint
        if current_state != TakeoverState.LOCKING:
            # 如果状态改变，重置 Hint 发射器
            if current_state != TakeoverState.LOCKING:
                self.hint_emitter.reset()
            return None
        
        # 获取目标主权和锁定时间
        target_authority = context.target_authority
        if not target_authority:
            return None
        
        lock_start_ts = context.enter_ts
        if lock_start_ts <= 0:
            return None
        
        # 获取锁定时间要求
        rule = get_takeover_rule(target_authority)
        lock_s = rule.get("lock_s", 2.0)
        
        # 获取 Hint 规则
        hint_rule = get_hint_rule(target_authority)
        hint_delay_s = hint_rule.get("hint_delay_s", 0.5)
        
        # 获取当前置信度
        confidence = 0.0
        if self.last_snapshot:
            if target_authority == "VISUAL":
                confidence = self.last_snapshot.visual_score
            elif target_authority == "MAP_VISION":
                confidence = self.last_snapshot.map_vision_score
            elif target_authority == "GPS":
                confidence = self.last_snapshot.gps_score
        
        # 评估并发射 Hint
        hint = self.hint_emitter.evaluate_and_emit(
            fsm_state=current_state.value,
            target_authority=target_authority,
            lock_start_ts=lock_start_ts,
            lock_s=lock_s,
            current_confidence=confidence,
            scene=self.last_scene,
            hint_delay_s=hint_delay_s
        )
        
        return hint
    
    def set_scene(self, scene: str) -> None:
        """设置当前场景"""
        self.last_scene = scene






