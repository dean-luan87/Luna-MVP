"""
C1 Active Controller (v0.2 Stable)

设计原则：
- observe() 每帧调用，但：
  - ❌ 不每帧产生日志
  - ❌ 不每帧产生 decision
  - 只有两种情况才产出 decision + 日志：
    1. 发生强制事件（状态切换 / protection 触发/解除）
    2. 心跳事件（低频，如 2s）
- log_frequency 只统计 decision 日志
- Modeling 是否执行，只由 decision 决定

核心修复：
- C1 决策 = 状态变化 / 强制干预事件，不是每帧 observe 一次就算一次决策
- 绝大多数帧 emit_event = False，不会产生决策日志
"""

import time
from typing import Optional, Dict, Any
from .c1_config import (
    DECISION_INTERVAL_SEC,
    HEARTBEAT_INTERVAL_SEC,
    MOTION_SCORE_THRESHOLD,
    RECOVERY_MOTION_THRESHOLD,
    RECOVERY_STABLE_TIME_SEC,
    STATIC_DIFF_THRESHOLD,
    STATIC_FRAMES_THRESHOLD,
    FLICKER_COUNT_THRESHOLD,
    PROTECTION_MODE_DURATION_SEC,
)
from .c1_state_machine import C1StateMachine, C1State, OcclusionState
from .c1_decision_logger import C1DecisionLogger
from .b2_decision_gate import B2DecisionGate
from .c1_context_hints import CContextHints
from .c_runtime_profile import CRuntimeProfile, ControlMode, ControlLevel


class C1ActiveController:
    """
    C1 Active Mode v0.2（稳定版）
    
    核心改进：
    1. 决策语义修正：C1 决策 = 状态变化 / 强制干预事件，不是每帧 observe 一次就算一次决策
    2. 节律闸门：只在强制事件或心跳时才产出 decision
    3. 日志口径统一：只在产出 decision 时记录日志
    """
    
    def __init__(
        self,
        decision_logger: Optional[C1DecisionLogger] = None,
        state_machine: Optional[C1StateMachine] = None,
        b2_gate: Optional[B2DecisionGate] = None,
        enable_b2: bool = False,
        trace_writer=None,  # v0.5: Trace writer for C RuntimeProfile
    ):
        """
        初始化 C1 Active Controller
        
        Args:
            decision_logger: C1 决策日志记录器（如果为 None，会创建新的）
            state_machine: C1 状态机（如果为 None，会创建新的）
            b2_gate: B2 决策闸门（如果为 None 且 enable_b2=True，会创建新的）
            enable_b2: 是否启用 B2 决策闸门（默认 False，保持 v0.2 行为）
        """
        # C1 决策日志记录器（用于 log_frequency 验证）
        self.decision_logger = decision_logger or C1DecisionLogger()
        
        # C1 状态机
        self.state_machine = state_machine or C1StateMachine(decision_logger=self.decision_logger)
        
        # B2 决策闸门（可选）
        self.enable_b2 = enable_b2
        self.b2_gate = b2_gate or (B2DecisionGate() if enable_b2 else None)
        
        # A5.3: C 上下文提示（用于理解 B2，不是执行）
        self.context_hints = CContextHints()
        
        # v0.5: Trace writer for C RuntimeProfile
        self.trace_writer = trace_writer
        
        # 上一次"决策事件"的时间戳（不是帧）
        self._last_decision_ts = 0.0
        
        # 当前稳定状态缓存
        self._current_state = C1State.STABLE
        self._protection_active = False
        self._protection_reason: Optional[str] = None
        
        # Recovery 相关
        self._recover_start_ts: Optional[float] = None
        
        # Protection 检测相关（用于检测状态变化）
        self._last_protection_active = False
        
        # 上一次决策（用于 B2 冗余抑制）
        self._last_decision: Optional[Dict[str, Any]] = None
        
        # 当前帧的 motion_score 和 frame_diff（用于 B2）
        self._current_motion_score: float = 0.0
        self._current_frame_diff: float = 0.0
        self._current_occlusion_state: Optional[OcclusionState] = None
    
    # =========================
    # 节律闸门
    # =========================
    def _should_emit_heartbeat(self, ts: float, effective_heartbeat: Optional[float] = None) -> bool:
        """
        判断是否应该产出心跳决策
        
        Args:
            ts: 当前时间戳
            effective_heartbeat: 有效心跳间隔（如果启用 B2，可能被调整）
        
        Returns:
            True 如果应该产出心跳决策
        """
        if self._last_decision_ts <= 0:
            return True
        
        heartbeat_interval = effective_heartbeat or HEARTBEAT_INTERVAL_SEC
        return (ts - self._last_decision_ts) >= heartbeat_interval
    
    # =========================
    # 主入口：每帧调用
    # =========================
    def observe(
        self,
        motion_score: float,
        frame_diff: float,
        timestamp: Optional[float] = None,
        occlusion_state: Optional[OcclusionState] = None,
        scene_class: str = "allow_camera",
        b2_advisory: Optional[Any] = None,  # A5.2: B2 建议（可选，保留兼容）
        advisory_queue: Optional[Any] = None,  # B2 → C 对接方案：Advisory Queue
    ) -> Optional[Dict[str, Any]]:
        """
        观察当前状态并生成决策（每帧调用）
        
        A5.2: C 侧的接入方式（最关键）
        - 默认路径下，C 不依赖 B2 也能工作
        - B2 只是可选的情报源
        
        Args:
            motion_score: 运动评分
            frame_diff: 帧差异评分
            timestamp: 时间戳（如果为 None，使用当前时间）
            scene_class: 场景类别（用于隐私判断）
            b2_advisory: B2 建议（可选，A5.2）
        
        Returns:
            Decision 字典，如果不需要产出 decision 则返回 None
        """
        ts = timestamp or time.time()
        
        # B2 → C 对接方案：从 Advisory Queue 获取活跃的 Advisory
        advisories = []
        if advisory_queue:
            advisories = advisory_queue.get_active(ts)
        
        # A5.3: 如果提供了 B2 建议（旧接口，保留兼容），先"理解"它（不是执行）
        if b2_advisory is not None:
            self.context_hints.ingest_b2_advisory(b2_advisory, ts)
        
        # B2 → C 对接方案：处理 Advisory Queue 中的 Advisory
        for adv in advisories:
            self.context_hints.ingest_b2_advisory(adv, ts)
        
        # 衰减上下文提示（随时间降低影响）
        self.context_hints.decay(ts)
        
        # 保存当前帧的 motion_score / frame_diff / occlusion_state（用于 B2 & 运行态快照）
        self._current_motion_score = motion_score
        self._current_frame_diff = frame_diff
        self._current_occlusion_state = occlusion_state
        
        # v0.5: 生成并写入 C RuntimeProfile（每帧都写，类似 B）
        # 注意：在状态更新之前写入，以便捕获当前状态
        self._write_c_runtime_profile(ts, frame_id=None)
        
        # ─────────────────────────────
        # 1. 每帧更新内部状态（不记录日志）
        # ─────────────────────────────
        update = self._update_state(motion_score, frame_diff, ts, occlusion_state)
        # update 示例：
        # {
        #   "emit_event": True/False,  # 关键：是否应该产出决策事件
        #   "state_transition": True/False,
        #   "reason": "severe motion" / "static occlusion detected" / None,
        # }
        
        # ─────────────────────────────
        # 2. 强制事件（状态变化 / protection 触发/解除）
        # ⚠️ 关键：只有这里才更新 _last_decision_ts（强制事件）
        # ─────────────────────────────
        if update.get("emit_event"):
            # C1 节律闸门已通过，准备生成 decision
            # 在 _make_decision() 之前接入 B2
            scene_hash = self._compute_scene_hash(motion_score, frame_diff)
            scene_stats = {
                "scene_hash": scene_hash,
                "objects": [],  # 简化：暂时为空，后续从 world_update 获取
                "obstacles": [],  # 简化：暂时为空，后续从 world_update 获取
            }
            motion_stats = {"motion_score": motion_score, "frame_diff": frame_diff}
            
            if self.enable_b2 and self.b2_gate:
                b2_emit, b2_meta = self.b2_gate.should_emit(
                    ts=ts,
                    state=str(self._current_state),
                    decision_type="forced_event",
                    scene_stats=scene_stats,
                    motion_stats=motion_stats,
                    base_heartbeat=HEARTBEAT_INTERVAL_SEC,
                )
                if not b2_emit:
                    # B2 主动抑制（理论上强制事件不应该被抑制，但为了安全）
                    return None
            else:
                b2_meta = {}
            
            # B2 → C 对接方案：计算 advisory_count
            advisory_count = len(advisories) if advisories else 0
            
            decision = self._make_decision(
                reason=update.get("reason", "unknown"),
                force=True,
                ts=ts,
                advisory_count=advisory_count,
            )
            
            # 附加 B2 元数据（如果启用）
            if self.enable_b2 and self.b2_gate:
                decision["b2"] = b2_meta
            
            self._record_decision(decision, ts)
            # ⚠️ 只有强制事件才更新 _last_decision_ts
            self._last_decision_ts = decision["timestamp"]
            self._last_decision = decision
            return decision
        
        # ─────────────────────────────
        # 3. 心跳事件（低频）
        # ─────────────────────────────
        # 先检查节律闸门
        if not self._should_emit_heartbeat(ts):
            return None
        
        # C1 节律闸门已通过，准备生成 decision
        # 在 _make_decision() 之前接入 B2
        scene_hash = self._compute_scene_hash(motion_score, frame_diff)
        scene_stats = {
            "scene_hash": scene_hash,
            "objects": [],  # 简化：暂时为空，后续从 world_update 获取
            "obstacles": [],  # 简化：暂时为空，后续从 world_update 获取
        }
        motion_stats = {"motion_score": motion_score, "frame_diff": frame_diff}
        
        if self.enable_b2 and self.b2_gate:
            b2_emit, b2_meta = self.b2_gate.should_emit(
                ts=ts,
                state=str(self._current_state),
                decision_type="heartbeat",
                scene_stats=scene_stats,
                motion_stats=motion_stats,
                base_heartbeat=HEARTBEAT_INTERVAL_SEC,
            )
            if not b2_emit:
                # B2 主动抑制
                return None
            
            # B2 可能调整了有效心跳间隔，需要重新检查
            effective_heartbeat = b2_meta.get("effective_heartbeat", HEARTBEAT_INTERVAL_SEC)
            if not self._should_emit_heartbeat(ts, effective_heartbeat):
                return None
        else:
            b2_meta = {}
        
        # B2 → C 对接方案：计算 advisory_count
        advisory_count = len(advisories) if advisories else 0
        
        decision = self._make_decision(
            reason="heartbeat",
            force=False,
            ts=ts,
            advisory_count=advisory_count,
        )
        
        # 附加 B2 元数据（如果启用）
        if self.enable_b2 and self.b2_gate:
            decision["b2"] = b2_meta
        
        self._record_decision(decision, ts)
        # ⚠️ 心跳也更新，但频率受控
        self._last_decision_ts = decision["timestamp"]
        self._last_decision = decision
        return decision
        
        # ─────────────────────────────
        # 4. 普通帧：不产生任何决策事件
        # ─────────────────────────────
        return None
    
    def _compute_scene_hash(self, motion_score: float, frame_diff: float) -> str:
        """
        计算场景 hash（粗粒度，用于 B2 场景稳定度感知）
        
        Args:
            motion_score: 运动评分
            frame_diff: 帧差异评分
        
        Returns:
            场景 hash 字符串
        """
        # 将 motion_score 和 frame_diff 量化到 0.1 精度
        motion_quantized = round(motion_score * 10) / 10
        diff_quantized = round(frame_diff * 10) / 10
        
        # 组合成 hash（包含状态信息）
        return f"{self._current_state.value}_{motion_quantized:.1f}_{diff_quantized:.1f}"
    
    # ==========================================================
    # 决策生成（标准口径，供验证脚本 / Pipeline 使用）
    # ==========================================================
    def _make_decision(
        self,
        reason: str,
        force: bool = False,
        ts: Optional[float] = None,
        advisory_count: int = 0,  # B2 → C 对接方案：advisory_count
    ) -> Dict[str, Any]:
        """
        标准 C1 决策结构（唯一合法口径）
        
        Args:
            reason: 决策原因（human-readable）
            force: 是否强制事件
            ts: 时间戳（如果为 None，使用当前时间）
        
        Returns:
            决策字典
        """
        if ts is None:
            ts = time.time()
        
        # 决策原则：SUSPENDED / Protection → 跳过 Modeling
        allow_modeling = True
        skip_reason = None
        
        if self._protection_active:
            allow_modeling = False
            skip_reason = f"protection_mode={self._protection_reason}"
        elif self._current_state == C1State.SUSPENDED:
            allow_modeling = False
            skip_reason = "motion_unstable"
        elif self._current_state == C1State.RECOVERING:
            allow_modeling = False
            skip_reason = "recovering"
        
        decision = {
            # === 时间与身份 ===
            "ts": ts,
            "timestamp": ts,  # 兼容字段
            "source": "C1",
            "decision_type": "C1_DECISION",  # ✅ 唯一合法标识
            
            # === 状态信息 ===
            "c1_state": self._current_state,
            "state": self._current_state,  # 兼容字段
            "state_transition": False,  # 由 _update_state 返回
            
            # === Protection ===
            "protection_active": self._protection_active,
            "protection_reason": self._protection_reason,
            
            # === 执行决策（Pipeline 只看这里）===
            "allow_modeling": allow_modeling,
            "skip_reason": skip_reason,
            "decision": "SKIP_MODELING" if not allow_modeling else "ALLOW_MODELING",
            
            # === 元数据 ===
            "reason": reason,
            "force": force,
        }
        
        return decision
    
    # ==========================================================
    # 状态更新（核心修复点）
    # 关键：只有状态变化或强制事件时才 emit_event = True
    # ==========================================================
    def _update_state(
        self,
        motion_score: float,
        frame_diff: float,
        timestamp: float,
        occlusion_state: Optional[OcclusionState] = None,
    ) -> Dict[str, Any]:
        """
        更新状态（A5.4: C 真正用 B2 的地方）
        
        只允许在「状态评估」阶段使用 B2 信息
        
        ⚠️ 关键点：
        - 不是 if → 强制切状态
        - 而是 调参数、调阈值、调节律
        
        这正是：人不是看到坑才反应，而是提前改变"行走策略"。
        """
        """
        只负责状态机推进，不负责日志
        
        关键：绝大多数帧 emit_event = False，不会产生决策日志
        
        Returns:
            状态更新结果字典，包含 emit_event 标志
        """
        prev_state = self._current_state
        prev_protection_active = self._protection_active
        emit_event = False  # ⚠️ 关键：默认 False，只有真正变化时才置 True
        reason = None
        
        # A5.4: 在状态评估阶段使用 B2 信息（克制式使用）
        # B2 → C 对接方案：只能作为"风险权重修正项"
        # ⚠️ 不是 if / else 控制
        # ⚠️ 只能作为 "风险权重修正项"
        
        # 计算未来风险（从 Advisory Queue）
        future_risk = 0.0
        if hasattr(self, 'context_hints'):
            # 使用已有的 context_hints（已从 Advisory Queue 更新）
            future_risk = self.context_hints.future_risk_level
        
        # 调整后的运动评分（考虑未来风险）
        # 示例：effective_risk = current_risk * (1 + future_risk * 0.5)
        # 不是强制，不是切状态，只是"人类提前看见危险"的那一点点倾向
        adjusted_motion_score = motion_score
        if future_risk > 0.6:
            # 提高内部风险权重（未来可能有风险）
            adjusted_motion_score *= (1.0 + future_risk * 0.5)  # 0.5 是修正系数
        
        # 如果 B2 建议降级警惕，可以降低敏感度
        if hasattr(self, 'context_hints') and self.context_hints.recommended_calm:
            adjusted_motion_score *= 0.8
        
        # 使用 C1StateMachine 更新状态（使用调整后的评分，但不记录决策日志）
        state_result = self.state_machine.update(
            motion_score=adjusted_motion_score,
            frame_diff=frame_diff,
            timestamp=timestamp,
            occlusion_state=occlusion_state,
        )
        
        # 更新当前状态（无论是否有变化）
        new_state = state_result.get("state", self._current_state)
        
        # 检查状态切换（关键：只有状态真正变化时才 emit_event = True）
        state_transition = state_result.get("state_transition") is not None
        if state_transition:
            emit_event = True
            reason = state_result.get("state_transition")
            self._current_state = new_state
        else:
            # 没有状态切换，同步当前状态（但不触发事件）
            self._current_state = new_state
        
        # 检查 Protection 状态变化（关键：只有 Protection 状态变化时才 emit_event = True）
        new_protection_active = state_result.get("protection_trigger_reason") is not None
        if new_protection_active != prev_protection_active:
            emit_event = True
            if new_protection_active:
                reason = f"protection_triggered={state_result.get('protection_trigger_reason')}"
            else:
                reason = "protection_cleared"
        self._protection_active = new_protection_active
        self._protection_reason = state_result.get("protection_trigger_reason")
        
        # ⚠️ 关键：确保不会"无事也 emit_event=True"
        # 如果 emit_event=True 但 reason=None，说明逻辑有问题
        if emit_event and reason is None:
            # 这种情况不应该发生，但为了安全，降级为 False
            emit_event = False
        
        return {
            "emit_event": emit_event,
            "state_transition": state_transition,
            "reason": reason,
        }
    
    def _record_decision(self, decision: Dict[str, Any], ts: float):
        """
        记录决策（确保只记录真正事件）
        
        Args:
            decision: 决策字典
            ts: 时间戳
        """
        # 记录 C1_DECISION 时间戳
        self.decision_logger.record_decision(ts)
        
        # 如果发生状态切换，记录状态切换日志
        if decision.get("state_transition"):
            self.decision_logger.record_state_transition(ts)
        
        # 如果 Protection 触发，记录 Protection 事件日志
        if decision.get("protection_active") and decision.get("protection_reason"):
            self.decision_logger.record_protection_event(ts)
    
    def should_run_modeling(self) -> bool:
        """
        最终决策函数（唯一出口）
        
        Returns:
            是否应该执行 ModelingExecutor
        """
        return self.state_machine.should_run_modeling()
    
    def _write_c_runtime_profile(self, ts: float, frame_id: Optional[int] = None):
        """
        v0.5: 生成并写入 C RuntimeProfile（每帧都写，类似 B）
        
        这是"驾驶员状态监控"，不是"驾驶行为"。
        """
        if not self.trace_writer:
            return
        
        try:
            # 根据当前状态确定 ControlMode
            if self._current_state == C1State.SUSPENDED:
                mode = ControlMode.SUSPENDED
            elif self._current_state == C1State.RECOVERING or self._protection_active:
                mode = ControlMode.DEGRADED
            else:
                mode = ControlMode.ACTIVE
            
            # 根据状态确定 ControlLevel
            if mode == ControlMode.SUSPENDED:
                control_level = ControlLevel.NONE
            elif mode == ControlMode.DEGRADED:
                control_level = ControlLevel.ASSIST
            else:
                control_level = ControlLevel.FULL
            
            # 确定 blocked_by
            blocked_by = None
            human_reason = ""
            if mode == ControlMode.SUSPENDED:
                blocked_by = "severe_motion"
                human_reason = "严重晃动，C 暂停运行"
            elif mode == ControlMode.DEGRADED:
                if self._protection_active:
                    blocked_by = "protection_mode"
                    human_reason = f"保护模式激活: {self._protection_reason or 'unknown'}"
                else:
                    blocked_by = "recovering"
                    human_reason = "恢复中，C 降级运行"
            else:
                human_reason = "C 正常运行"
            
            # 构建 C RuntimeProfile
            profile = CRuntimeProfile(
                version="v0.5",
                mode=mode,
                control_level=control_level,
                update_interval_ms=int(HEARTBEAT_INTERVAL_SEC * 1000),  # 使用心跳间隔
                blocked_by=blocked_by,
                human_reason=human_reason,
                meta={
                    "state": self._current_state.value,
                    "protection_active": self._protection_active,
                    "motion_score": self._current_motion_score,
                "frame_diff": self._current_frame_diff,
                "occlusion_state": self._current_occlusion_state.value if self._current_occlusion_state else None,
                }
            )
            
            # 写入 trace
            self.trace_writer.write({
                "event_type": "C_RUNTIME_PROFILE",
                "time": {"ts": ts, "frame_id": frame_id},
                "c_runtime_profile": profile.to_dict(),
            })
        except Exception:
            # Never block runtime due to trace failures
            pass
    
    def get_current_state(self) -> C1State:
        """获取当前状态"""
        return self.state_machine.get_current_state()
