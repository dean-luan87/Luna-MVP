"""
Authority Lock Hint (v1.4.8 Step 7)

重要禁令：
- 本模块当前为 Skeleton 插桩版，不得修改现有导航控制逻辑
- Hint 不得触发任何主权切换
- Hint 默认不接入 TTS
- 所有 Hint 必须可关闭

核心抽象：Authority Lock Hint
- 在"真正接管发生之前"，向上层系统发布可解释、可撤销、非强制的"接管预期信号"
- 不做接管、不做裁决、不做控制，只做一件事：提前让系统"知道接下来可能要发生什么"
"""

from dataclasses import dataclass
from typing import Optional, List
import time
from navigation.events import TOPIC_AUTHORITY_LOCK_HINT
from navigation.authority_lock_hint_rules import (
    get_hint_rule,
    calculate_eta_s,
)


class HintSeverity:
    """Hint 严重程度（工程语义，不是情绪）"""
    LOW = "LOW"          # 只给系统内部模块用
    MEDIUM = "MEDIUM"    # 允许 TTS 做轻提示
    HIGH = "HIGH"        # 允许 UI / 强提示（未来）


@dataclass
class AuthorityLockHint:
    """
    Authority Lock Hint 数据结构
    
    注意：
    - Hint 不是 Decision，不是 Event，而是 Hint（提示）
    - 可以被忽略、可以被撤销、可以被不同模块不同方式消费
    - 不具备强制语义
    """
    ts: float
    target_authority: str            # VISUAL / MAP_VISION / GPS
    confidence: float                # 当前 snapshot 分数
    eta_s: Optional[float]           # 预计多久后完成接管（体验层最重要的字段）
    scene: str                       # 当前场景
    severity: str                    # LOW / MEDIUM / HIGH
    reason_trace: List[str]          # 原因追踪


class AuthorityLockHintEmitter:
    """
    主权锁定提示发射器
    
    职责：
    1. 监听 FSM
    2. 生成 Hint
    3. 发布事件
    """
    
    def __init__(self, event_bus=None, logger=None, enable_hint: bool = True):
        """
        初始化 Hint 发射器
        
        Args:
            event_bus: 事件总线（可选）
            logger: 日志记录器（可选）
            enable_hint: 是否启用 Hint（Feature Flag，默认 True）
        """
        self.event_bus = event_bus
        self.logger = logger
        self.enable_hint = enable_hint
        
        # 状态追踪
        self.last_hint_ts: Optional[float] = None
        self.last_hint_authority: Optional[str] = None
    
    def evaluate_and_emit(
        self,
        fsm_state: str,
        target_authority: Optional[str],
        lock_start_ts: float,
        lock_s: float,
        current_confidence: float,
        scene: str,
        hint_delay_s: float = 0.5
    ) -> Optional[AuthorityLockHint]:
        """
        评估并发射 Hint
        
        触发条件：
        - FSM 状态 == LOCKING
        - target_authority 与当前主权不同（或首次）
        - LOCKING 已持续 > hint_delay_s
        
        Args:
            fsm_state: FSM 当前状态
            target_authority: 目标主权
            lock_start_ts: LOCKING 状态开始时间
            lock_s: 锁定时间要求（秒）
            current_confidence: 当前置信度
            scene: 当前场景
            hint_delay_s: Hint 延迟时间（秒，默认 0.5）
            
        Returns:
            AuthorityLockHint: 如果满足条件，返回 Hint；否则返回 None
        """
        if not self.enable_hint:
            return None
        
        # 只在 LOCKING 状态发 Hint
        if fsm_state != "LOCKING":
            # 如果状态改变，重置追踪
            if fsm_state != "LOCKING":
                self.last_hint_ts = None
                self.last_hint_authority = None
            return None
        
        if not target_authority:
            return None
        
        now_ts = time.time()
        lock_duration = now_ts - lock_start_ts
        
        # 检查是否满足延迟要求
        if lock_duration < hint_delay_s:
            return None
        
        # 检查是否已经发过 Hint（LOCKING 稳定期间只发一次）
        if (self.last_hint_authority == target_authority and 
            self.last_hint_ts is not None and 
            now_ts - self.last_hint_ts < lock_s):
            return None  # 已经发过，不再重复
        
        # 获取 Hint 规则
        rule = get_hint_rule(target_authority)
        min_lock_progress = rule.get("min_lock_progress", 0.3)
        default_severity = rule.get("default_severity", "LOW")
        
        # 计算锁定进度
        lock_progress = lock_duration / lock_s if lock_s > 0 else 0.0
        
        # 检查是否满足最小进度要求
        if lock_progress < min_lock_progress:
            return None
        
        # 计算 ETA
        eta_s = calculate_eta_s(lock_start_ts, lock_s, now_ts)
        
        # 生成 Hint
        hint = AuthorityLockHint(
            ts=now_ts,
            target_authority=target_authority,
            confidence=current_confidence,
            eta_s=eta_s,
            scene=scene,
            severity=default_severity,
            reason_trace=[
                f"fsm_state=LOCKING",
                f"lock_progress={lock_progress:.2f}",
                f"lock_duration={lock_duration:.2f}s",
                f"eta_s={eta_s:.2f}s" if eta_s else "eta_s=None"
            ]
        )
        
        # 更新追踪
        self.last_hint_ts = now_ts
        self.last_hint_authority = target_authority
        
        # 发布事件
        self._publish_hint(hint)
        
        # 记录日志
        self._log_hint(hint)
        
        return hint
    
    def _publish_hint(self, hint: AuthorityLockHint) -> None:
        """发布 Hint 事件"""
        if self.event_bus:
            # 导入事件类（避免循环依赖）
            from navigation.events import AuthorityLockHintEvent
            event = AuthorityLockHintEvent(
                ts=hint.ts,
                hint=hint
            )
            self.event_bus.publish(TOPIC_AUTHORITY_LOCK_HINT, event)
    
    def _log_hint(self, hint: AuthorityLockHint) -> None:
        """记录 Hint 日志"""
        eta_str = f"{hint.eta_s:.2f}s" if hint.eta_s is not None else "None"
        log_msg = (
            f"[LOCK_HINT] target={hint.target_authority} "
            f"eta={eta_str} confidence={hint.confidence:.2f} "
            f"severity={hint.severity} scene={hint.scene}"
        )
        if self.logger:
            if hasattr(self.logger, 'info'):
                self.logger.info("AuthorityLockHintEmitter", "lock_hint", {
                    "target_authority": hint.target_authority,
                    "confidence": hint.confidence,
                    "eta_s": hint.eta_s,
                    "scene": hint.scene,
                    "severity": hint.severity,
                    "reason_trace": hint.reason_trace
                })
            else:
                self.logger(log_msg)
        else:
            print(log_msg)
    
    def reset(self) -> None:
        """重置状态追踪"""
        self.last_hint_ts = None
        self.last_hint_authority = None






