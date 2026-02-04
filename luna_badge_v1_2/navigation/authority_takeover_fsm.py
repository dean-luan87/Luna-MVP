"""
Authority Takeover FSM (v1.4.8 Step 6)

重要禁令：
- 本模块当前为 Skeleton 插桩版，不得修改现有导航控制逻辑
- FSM 只输出"接管建议事件"，不直接切换主权
- FSM 必须可关闭（Feature Flag）
- 所有状态迁移必须有 reason_trace

核心抽象：Authority Takeover FSM
- 它不算分，不算路，只做三件事：
  1. 是否允许接管
  2. 是否正在接管
  3. 是否需要回退

关键设计原则：
- 时间 > 分数
- 连续稳定 > 单次高分
- 接管慢，回退更慢
- 室内优先级永远最高
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Optional, List
import time
from navigation.evidence_models import AuthorityConfidenceSnapshot
from navigation.authority_takeover_rules import (
    get_takeover_rule,
    is_scene_allowed,
    check_distance_requirement,
    check_score_requirements,
)
from navigation.events import TakeoverDecisionEvent


class TakeoverState(Enum):
    """接管状态枚举"""
    IDLE = "IDLE"              # 空闲
    CANDIDATE = "CANDIDATE"    # 满足接管条件，但未确认
    LOCKING = "LOCKING"        # 锁定观察窗口，防抖
    TAKEN = "TAKEN"            # 完成接管
    COOLDOWN = "COOLDOWN"      # 冷却期，防止频繁切换


@dataclass
class TakeoverContext:
    """接管上下文"""
    target_authority: Optional[str] = None  # "VISUAL" / "MAP_VISION" / "GPS"
    enter_ts: float = 0.0                   # 进入当前状态的时间戳
    last_update_ts: float = 0.0             # 最后更新时间戳
    reason_trace: List[str] = field(default_factory=list)  # 原因追踪


class AuthorityTakeoverFSM:
    """
    主权接管状态机
    
    职责：
    - 管理「主权迁移过程」本身
    - 不是融合算法，不是重新写 PositionAuthorityManager
    - 只输出"接管建议事件"
    """
    
    def __init__(self, enable_fsm: bool = False):
        """
        初始化 FSM
        
        Args:
            enable_fsm: 是否启用 FSM（Feature Flag，默认 False）
        """
        self.enable_fsm = enable_fsm
        self.current_state = TakeoverState.IDLE
        self.context = TakeoverContext()
    
    def update(
        self,
        now_ts: float,
        snapshot: AuthorityConfidenceSnapshot,
        scene: str,
        distance_m: Optional[float] = None
    ) -> Optional[TakeoverDecisionEvent]:
        """
        更新 FSM
        
        Args:
            now_ts: 当前时间戳
            snapshot: 置信度快照
            scene: 当前场景（"INDOOR" / "OUTDOOR" / "TRANSITION"）
            distance_m: 当前距离（米，可选）
            
        Returns:
            TakeoverDecisionEvent: 如果完成接管，返回事件；否则返回 None
        """
        if not self.enable_fsm:
            return None
        
        # 更新上下文
        self.context.last_update_ts = now_ts
        
        # 根据当前状态执行状态迁移
        new_state = self._decide_next_state(now_ts, snapshot, scene, distance_m)
        
        # 检查状态变化
        if new_state != self.current_state:
            old_state = self.current_state
            self.current_state = new_state
            
            # 记录状态进入时间
            self.context.enter_ts = now_ts
            
            # 记录状态迁移日志
            self._log_state_transition(old_state, new_state)
            
            # 如果进入 TAKEN 状态，生成接管决策事件
            if new_state == TakeoverState.TAKEN:
                return self._create_takeover_decision(now_ts, snapshot)
        
        return None
    
    def _decide_next_state(
        self,
        now_ts: float,
        snapshot: AuthorityConfidenceSnapshot,
        scene: str,
        distance_m: Optional[float]
    ) -> TakeoverState:
        """
        决定下一个状态
        
        状态迁移规则：
        - IDLE → CANDIDATE: 满足接管条件
        - CANDIDATE → LOCKING: 连续满足条件
        - LOCKING → TAKEN: 锁定时间到达
        - TAKEN → COOLDOWN: 输出接管决策
        - COOLDOWN → IDLE: 冷却期结束
        """
        current = self.current_state
        state_age = now_ts - self.context.enter_ts
        
        # IDLE → CANDIDATE
        if current == TakeoverState.IDLE:
            candidate = self._check_candidate_conditions(snapshot, scene, distance_m)
            if candidate:
                self.context.target_authority = snapshot.dominant_candidate
                self.context.reason_trace.append(
                    f"candidate_qualified_{snapshot.dominant_candidate}_score_{snapshot.visual_score:.2f}"
                )
                return TakeoverState.CANDIDATE
            return TakeoverState.IDLE
        
        # CANDIDATE → LOCKING
        elif current == TakeoverState.CANDIDATE:
            # 检查是否仍然满足条件（连续稳定）
            if self._check_candidate_conditions(snapshot, scene, distance_m):
                # 检查目标是否改变（防止抖动）
                if snapshot.dominant_candidate == self.context.target_authority:
                    return TakeoverState.LOCKING
                else:
                    # 目标改变，回到 IDLE
                    self.context.reason_trace.append(
                        f"candidate_changed_{self.context.target_authority}_to_{snapshot.dominant_candidate}"
                    )
                    self._reset_context()
                    return TakeoverState.IDLE
            else:
                # 不再满足条件，回到 IDLE
                self.context.reason_trace.append("candidate_conditions_no_longer_met")
                self._reset_context()
                return TakeoverState.IDLE
        
        # LOCKING → TAKEN
        elif current == TakeoverState.LOCKING:
            rule = get_takeover_rule(self.context.target_authority or "")
            lock_s = rule.get("lock_s", 2.0)
            
            if state_age >= lock_s:
                # 锁定时间到达，进入 TAKEN
                self.context.reason_trace.append(f"locking_complete_lock_s_{lock_s}")
                return TakeoverState.TAKEN
            else:
                # 仍在锁定中，检查是否仍然满足条件
                if self._check_candidate_conditions(snapshot, scene, distance_m):
                    if snapshot.dominant_candidate == self.context.target_authority:
                        return TakeoverState.LOCKING
                
                # 条件不再满足，回退到 IDLE
                self.context.reason_trace.append("locking_conditions_no_longer_met")
                self._reset_context()
                return TakeoverState.IDLE
        
        # TAKEN → COOLDOWN
        elif current == TakeoverState.TAKEN:
            # TAKEN 状态会在外部生成事件后立即进入 COOLDOWN
            rule = get_takeover_rule(self.context.target_authority or "")
            cooldown_s = rule.get("cooldown_s", 3.0)
            return TakeoverState.COOLDOWN
        
        # COOLDOWN → IDLE
        elif current == TakeoverState.COOLDOWN:
            rule = get_takeover_rule(self.context.target_authority or "")
            cooldown_s = rule.get("cooldown_s", 3.0)
            
            if state_age >= cooldown_s:
                # 冷却期结束
                self.context.reason_trace.append(f"cooldown_complete_cooldown_s_{cooldown_s}")
                self._reset_context()
                return TakeoverState.IDLE
            else:
                return TakeoverState.COOLDOWN
        
        return current
    
    def _check_candidate_conditions(
        self,
        snapshot: AuthorityConfidenceSnapshot,
        scene: str,
        distance_m: Optional[float]
    ) -> bool:
        """
        检查是否满足 CANDIDATE 条件
        
        IDLE → CANDIDATE 的条件：
        - snapshot.dominant_candidate 存在
        - 满足 min_score + min_gap
        - scene 符合
        - GPS 额外检查 distance
        """
        # 检查 dominant_candidate 是否存在
        if not snapshot.dominant_candidate:
            return False
        
        target = snapshot.dominant_candidate
        
        # 检查场景是否允许
        if not is_scene_allowed(target, scene):
            return False
        
        # 获取对应分数和差距
        if target == "VISUAL":
            score = snapshot.visual_score
        elif target == "MAP_VISION":
            score = snapshot.map_vision_score
        elif target == "GPS":
            score = snapshot.gps_score
        else:
            return False
        
        gap = snapshot.confidence_gap
        
        # 检查分数要求
        if not check_score_requirements(target, score, gap):
            return False
        
        # 检查距离要求（GPS 需要）
        if not check_distance_requirement(target, distance_m):
            return False
        
        return True
    
    def _reset_context(self) -> None:
        """重置上下文"""
        self.context.target_authority = None
        self.context.enter_ts = 0.0
        self.context.last_update_ts = 0.0
        self.context.reason_trace = []
    
    def _create_takeover_decision(
        self,
        now_ts: float,
        snapshot: AuthorityConfidenceSnapshot
    ) -> TakeoverDecisionEvent:
        """
        创建接管决策事件
        
        Args:
            now_ts: 当前时间戳
            snapshot: 置信度快照
            
        Returns:
            TakeoverDecisionEvent: 接管决策事件
        """
        target = self.context.target_authority or ""
        
        # 获取对应分数
        if target == "VISUAL":
            confidence = snapshot.visual_score
        elif target == "MAP_VISION":
            confidence = snapshot.map_vision_score
        elif target == "GPS":
            confidence = snapshot.gps_score
        else:
            confidence = 0.0
        
        return TakeoverDecisionEvent(
            ts=now_ts,
            target_authority=target,
            confidence=confidence,
            state=TakeoverState.TAKEN.value,
            reason_trace=self.context.reason_trace.copy()
        )
    
    def _log_state_transition(self, old_state: TakeoverState, new_state: TakeoverState) -> None:
        """记录状态迁移日志"""
        target = self.context.target_authority or "None"
        reasons = ", ".join(self.context.reason_trace[-3:]) if self.context.reason_trace else "none"
        print(
            f"[TAKEOVER_FSM] {old_state.value} → {new_state.value} "
            f"target={target} reason={reasons}"
        )






