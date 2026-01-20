"""
FSM Policy Hooks (v1.4.8 StepB-5)

FSM 视角优先策略钩子

目标：根据证据快照输出 FSMSuggestion

核心约束：
- 不改 FSM 的状态机实现
- 只在 FSM 输入侧加"策略钩子"
- 输出的是 FSMSuggestion（建议），由调用方选择是否使用
"""

from typing import Optional
import time
from navigation.fsm_policy_models import FSMSuggestion
from navigation.fsm_policy_state_store import FSMPolicyStateStore
from navigation.gps_gatekeeper import GPSMode
from navigation.gps_quality_monitor import GPSQuality


class FSMPolicyHooks:
    """
    FSM 策略钩子
    
    职责：
    - 根据证据快照输出 FSMSuggestion
    - 发布策略建议事件
    """
    
    def __init__(
        self,
        state_store: FSMPolicyStateStore,
        event_bus=None,
        logger=None,
        base_pre_turn_distance_m: float = 8.0,
        vision_confirm_window_s: float = 3.0,
        vision_confirm_threshold: float = 0.85
    ):
        """
        初始化策略钩子
        
        Args:
            state_store: 状态存储
            event_bus: 事件总线（可选）
            logger: 日志记录器（可选）
            base_pre_turn_distance_m: 基础 PRE_TURN 距离（米，默认 8.0）
            vision_confirm_window_s: 视角确认时间窗（秒，默认 3.0）
            vision_confirm_threshold: 视角确认阈值（默认 0.85）
        """
        self.state_store = state_store
        self.event_bus = event_bus
        self.logger = logger
        self.base_pre_turn_distance_m = base_pre_turn_distance_m
        self.vision_confirm_window_s = vision_confirm_window_s
        self.vision_confirm_threshold = vision_confirm_threshold
    
    def evaluate(self) -> FSMSuggestion:
        """
        评估证据快照，生成策略建议
        
        必须实现的规则（第一版写死）：
        1. 视角确认优先（核心）
        2. 一致性差则保守
        3. GPS 质量差必降级
        4. 短距离 GPS 永远不能主导
        
        Returns:
            FSMSuggestion: 策略建议
        """
        snapshot = self.state_store.get_snapshot()
        
        # 初始化建议
        suggestion = FSMSuggestion(
            pre_turn_distance_m=self.base_pre_turn_distance_m,
            allow_gps=None,
            prefer_lock=None,
            reason="",
            evidence=snapshot
        )
        
        reasons = []
        
        # 规则 1：视角确认优先（核心）
        if self._has_recent_vision_confirm(snapshot):
            suggestion.pre_turn_distance_m = 6.0  # 缩短距离
            suggestion.allow_gps = False  # GPS 即便 ACTIVE 也建议暂时不参与
            suggestion.prefer_lock = True  # 锁定当前路线阶段
            reasons.append("vision_confirmed")
        
        # 规则 2：一致性差则保守
        if snapshot.get("map_consistency_mismatch") or \
           (snapshot.get("map_consistency_score") is not None and 
            snapshot.get("map_consistency_score") < 0.6):
            suggestion.prefer_lock = False
            suggestion.pre_turn_distance_m = 10.0  # 提前提醒，留余量
            
            # allow_gps 取决于 GPSMode（ACTIVE 才允许）
            gps_mode_str = snapshot.get("gps_mode")
            if gps_mode_str:
                try:
                    gps_mode = GPSMode(gps_mode_str)
                    suggestion.allow_gps = (gps_mode == GPSMode.ACTIVE)
                except ValueError:
                    suggestion.allow_gps = False
            else:
                suggestion.allow_gps = False
            
            reasons.append("consistency_poor")
        
        # 规则 3：GPS 质量差必降级
        gps_quality_str = snapshot.get("gps_quality")
        if gps_quality_str:
            try:
                gps_quality = GPSQuality(gps_quality_str)
                if gps_quality in {GPSQuality.DEGRADED, GPSQuality.INVALID}:
                    suggestion.allow_gps = False
                    reasons.append("gps_degraded")
            except ValueError:
                pass
        
        # 规则 4：短距离 GPS 永远不能主导
        gps_mode_str = snapshot.get("gps_mode")
        if gps_mode_str:
            try:
                gps_mode = GPSMode(gps_mode_str)
                if gps_mode == GPSMode.VERIFY_ONLY:
                    suggestion.allow_gps = False
                    if "gps_verify_only" not in reasons:
                        reasons.append("gps_verify_only")
            except ValueError:
                pass
        
        # 如果 allow_gps 仍未设置，根据 GPSMode 决定
        if suggestion.allow_gps is None:
            gps_mode_str = snapshot.get("gps_mode")
            if gps_mode_str:
                try:
                    gps_mode = GPSMode(gps_mode_str)
                    suggestion.allow_gps = (gps_mode == GPSMode.ACTIVE)
                except ValueError:
                    suggestion.allow_gps = False
            else:
                suggestion.allow_gps = False
        
        # 如果 prefer_lock 仍未设置，默认 False
        if suggestion.prefer_lock is None:
            suggestion.prefer_lock = False
        
        # 组合原因
        suggestion.reason = "+".join(reasons) if reasons else "default"
        
        # 发布策略建议事件
        self._publish_suggestion(suggestion)
        
        return suggestion
    
    def _has_recent_vision_confirm(self, snapshot: dict) -> bool:
        """
        检查是否有最近的视角确认
        
        条件：
        - 最近 nav.position.confirmed.confidence >= 0.85
        - 且在 3 秒内
        
        Args:
            snapshot: 证据快照
            
        Returns:
            bool: 是否有最近的视角确认
        """
        last_confirm = snapshot.get("last_position_confirmed")
        if not last_confirm:
            return False
        
        # 检查置信度
        confidence = last_confirm.get("confidence", 0.0)
        if confidence < self.vision_confirm_threshold:
            return False
        
        # 检查时间窗
        confirm_ts = last_confirm.get("ts", 0.0)
        now_ts = time.time()
        if now_ts - confirm_ts > self.vision_confirm_window_s:
            return False
        
        # 检查来源（应该包含 vision）
        sources = last_confirm.get("sources", [])
        if "vision" not in sources:
            return False
        
        return True
    
    def _publish_suggestion(self, suggestion: FSMSuggestion) -> None:
        """
        发布策略建议事件
        
        Args:
            suggestion: 策略建议
        """
        event_data = {
            "pre_turn_distance_m": suggestion.pre_turn_distance_m,
            "allow_gps": suggestion.allow_gps,
            "prefer_lock": suggestion.prefer_lock,
            "reason": suggestion.reason,
            "evidence": suggestion.evidence
        }
        
        if self.event_bus:
            self.event_bus.publish("nav.fsm.policy.suggested", event_data)
        
        # 日志输出
        self._log_suggestion(suggestion)
    
    def _log_suggestion(self, suggestion: FSMSuggestion) -> None:
        """
        记录策略建议日志
        
        Args:
            suggestion: 策略建议
        """
        pre_turn_str = f"{suggestion.pre_turn_distance_m:.1f}" if suggestion.pre_turn_distance_m else "None"
        allow_gps_str = str(suggestion.allow_gps) if suggestion.allow_gps is not None else "None"
        prefer_lock_str = str(suggestion.prefer_lock) if suggestion.prefer_lock is not None else "None"
        
        log_msg = (
            f"[FSMPOLICY] "
            f"pre_turn={pre_turn_str} "
            f"allow_gps={allow_gps_str} "
            f"prefer_lock={prefer_lock_str} "
            f"reason={suggestion.reason}"
        )
        
        if self.logger:
            if hasattr(self.logger, 'info'):
                self.logger.info("FSMPolicyHooks", "policy_suggested", {
                    "pre_turn_distance_m": suggestion.pre_turn_distance_m,
                    "allow_gps": suggestion.allow_gps,
                    "prefer_lock": suggestion.prefer_lock,
                    "reason": suggestion.reason
                })
            else:
                self.logger(log_msg)
        else:
            print(log_msg)






