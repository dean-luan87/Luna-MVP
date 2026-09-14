# vision_pipeline/b2/v03/b2_v03.py

import time
# Runtime invariants (optional)
try:
    from luna_badge_v1_2.governance.invariants import assert_b_invariants
except Exception:  # pragma: no cover - optional dependency
    assert_b_invariants = None
from collections import deque
from typing import Dict, Any, List, Optional
from enum import Enum, auto

from vision_pipeline.b2.v03.factors import (
    build_factor_evidences,
    FactorType,
    FactorEvidence
)
from vision_pipeline.b2.v03.b2_health_logger import B2HealthLogger, B2HealthEvent
from vision_pipeline.b2.v03.log_utils import B2Logger
from vision_pipeline.b2.v03.trace.trace_writer import TraceWriter
from vision_pipeline.b2.v03.runtime_state_machine import (
    B2RuntimeStateMachine,
    B2RuntimeState
)
from vision_pipeline.b2.v03.gate import (
    compute_stability_score,
    compute_view_state,
    B2GateMode,
    get_confidence_dict
)
from vision_pipeline.b2.v03.dcs_guard import dcs_check, calculate_dcs_penalty
from vision_pipeline.b2.v03.trace_writer_v043 import TraceWriterV043
from vision_pipeline.b2.v03.time_utils import format_video_time
# v0.5: Gate Runtime Profile 和 Scheduler
from vision_pipeline.b2.v03.gate_runtime_profile import GateRuntimeProfile, GateMode, ComputeLevel
from vision_pipeline.b2.v03.scheduler_v05 import B2SchedulerV05


# ============================================================
# Gate Authority Table (v0.4.2 Minimal Integration)
# ------------------------------------------------------------
# Gate 是 B2 主循环的"最高裁决者"，它只裁决【是否允许 B2 在本帧产出新判断/写回】。
# Gate 不改变因子算法，不引入新能力，只控制 B2 的运行模式与写回权限。
#
# Inputs (来自 view_state/evidence_state 的抽象)：
#   - stability_score: 镜头稳定性评分 (0~1)
#   - range_m: 当前有效观测距离（米）
#   - evidence_ok: 证据是否达到最小连续性要求（bool / score）
#   - (optional) occlusion_score / pose_ok / fps_ok ...
#
# Outputs (Gate Mode)：
#   1) SUSPENDED  (Hard Gate Fail)
#      - 权限：完全禁止 B2 产出"新结论/新建议"
#      - 行为：tick() 立即返回 None（SILENT）
#      - 写回：禁止 timeline / memory / health 写入
#      - 目的：抗视角污染、避免把抖动/近距/失真当"世界变化"
#
#   2) READ_ONLY  (Soft Gate Fail)
#      - 权限：允许计算（factors/impact），但禁止"写回新事实"
#      - 行为：tick() 可返回 summary（供 C 参考），但必须标记 readonly=True
#      - 写回：禁止 timeline / memory（可允许 health/trace 记录）
#      - 目的：证据未稳定时，允许观察但不固化，不污染世界模型
#
#   3) ACTIVE     (All Pass)
#      - 权限：允许正常产出 + 写回（timeline/memory/health）
#      - 行为：tick() 正常运行
#
# Non-negotiables:
#   - Gate=SUSPENDED => B2 必须 SILENT（返回 None）
#   - Gate=READ_ONLY => 不能写 timeline/memory（只能 trace/health）
#   - Gate=ACTIVE    => 允许写回，但仍受 NO_OP/SILENT 规则约束
# ============================================================

class B2v03:
    """
    B2 v0.3
    - 只负责：未来窗口内的"变化判定"
    - 不做决策、不做语言、不直接干预 C
    
    v0.4.2: Gate 作为第一裁判，控制 B2 运行模式与写回权限
    """

    def __init__(
        self,
        future_window_start: float = 1.0,
        future_window_end: float = 8.0,
        max_buffer: int = 32,
        debug: bool = False,
        log_mode: str = "video",
        log_base_ts: Optional[float] = None,
        enable_trace: bool = True,
        trace_file: Optional[str] = None,
        fps: float = 30.0,
    ):
        self.future_window_start = future_window_start
        self.future_window_end = future_window_end
        self.debug = debug

        # 保存未来状态（时间有序）
        self._future_buffer: deque = deque(maxlen=max_buffer)
        
        # 健康日志记录器
        self.health_logger = B2HealthLogger(enable=True)
        
        # B2 日志记录器（人类可读）
        self.logger = B2Logger(mode=log_mode, base_ts=log_base_ts, enable=True)
        
        # B2 Runtime Trace 记录器（v0.4）
        if enable_trace:
            if trace_file is None:
                trace_file = "traces/b2_runtime_trace_v04.jsonl"
            self.trace_writer = TraceWriter(path=trace_file)
        else:
            self.trace_writer = None
        
        self.fps = fps
        self.log_base_ts = log_base_ts
        
        # B2 Runtime State Machine v0.5
        self.state_machine = B2RuntimeStateMachine(
            n_frames_min=90,  # 约 3 秒
            window_min_seconds=self.future_window_end - self.future_window_start,
            stable_time_seconds=1.5
        )
        
        # v0.5: Test mode flag for video regression (force evidence_ok=True without YOLO)
        self._test_mode_assume_evidence_ok = False
        
        # v0.4.3 trace writer (JSONL, 统一 Schema)
        trace_path_v043 = getattr(self, "trace_path", None) or "traces/b2_trace_v043.jsonl"
        self.trace_writer_v043 = TraceWriterV043(
            out_path=trace_path_v043,
            enabled=enable_trace
        )
        
        # v0.4.2: Gate trace path (separate from main trace, for auditability)
        import os
        self._gate_trace_path = os.environ.get(
            "B2_GATE_TRACE_PATH",
            "traces/b2_gate_trace_v042.jsonl"
        )
        
        # B runtime state 相关（用于 trace，v0.4 兼容）
        self.camera_unstable = False  # 可以从外部设置
        self.distance_to_front = 10.0  # 可以从外部设置
        
        # Gate 输入（可以从外部设置）
        self.imu_data: Optional[Dict[str, float]] = None
        self.range_m: Optional[float] = None
        self.c_runtime_state: Optional[Dict[str, Any]] = None
        self.system_fps: Optional[float] = None
        self.occlusion_ratio: Optional[float] = None
        self.context: Optional[Dict[str, Any]] = None

        # 最近一次有效输出（用于节流 / 对比）
        self._last_emit_ts: Optional[float] = None
        self._last_evidences: Optional[Dict[FactorType, FactorEvidence]] = None
        self._last_summary: Optional[Dict[str, Any]] = None
        
        # 用于跟踪因子变化（用于 FACTOR 日志）
        self._last_factor_evidences: Dict[FactorType, FactorEvidence] = {}
        
        # 用于跟踪 timeline 写入计数
        self._timeline_index = 0
        
        # v0.5: scheduler is used for trace pacing (no gating in B)
        self._sched = B2SchedulerV05()
        self.scheduler_v05 = self._sched  # 别名，用于兼容

    def _build_runtime_profile_v05(
        self,
        gate_mode: str,
        gate_reason: str,
        gate_eval: Dict[str, Any],
        frame_ts: float,
        perception: Dict[str, Any],
        frame_id: Optional[int],
        hysteresis_info: Optional[Dict[str, Any]] = None,
        transition_info: Optional[Dict[str, Any]] = None,
    ) -> GateRuntimeProfile:
        """
        v0.5: Convert gate result → runtime scheduling profile.
        The profile is the ONLY authority that decides whether/how B2 runs this tick.
        """
        # Extract view_state presence for observability
        view_state = (perception or {}).get("view_state") if isinstance(perception, dict) else None
        has_view_state = isinstance(view_state, dict) and len(view_state) > 0

        # GateMode mapping
        if gate_mode == "SUSPENDED":
            gm = GateMode.SUSPENDED
        elif gate_mode == "READ_ONLY":
            gm = GateMode.READ_ONLY
        else:
            gm = GateMode.ACTIVE

        # Scheduling defaults (conservative)
        # ACTIVE: run normally but still rate-limited
        # READ_ONLY: do NOT compute new evidence (LIGHT), do NOT emit B→C output
        # SUSPENDED: NONE
        if gm == GateMode.SUSPENDED:
            compute = ComputeLevel.NONE
            tick_ms = 250
        elif gm == GateMode.READ_ONLY:
            compute = ComputeLevel.LIGHT
            tick_ms = 150
        else:
            compute = ComputeLevel.FULL
            tick_ms = 100

        blocked_by = None
        try:
            blocked_by = gate_eval.get("blocked_by") or gate_eval.get("details", {}).get("blocked_by")
        except Exception:
            blocked_by = None

        # v0.5: future probe is OFF by design
        allow_future_probe = False

        # v0.5: B is advisory-only (frozen)
        authority_scope = "ADVISORY_ONLY"

        # v0.5 Patch D-2: 将 Hysteresis 和 Transition 信息写入 meta
        meta = {
            "frame_ts": float(frame_ts),
            "frame_id": int(frame_id) if frame_id is not None else None,
            "has_view_state": bool(has_view_state),
            "gate_eval": gate_eval,
        }
        
        if hysteresis_info:
            meta["hysteresis"] = hysteresis_info
        
        # v0.5: 写入 transition 信息（用于 Viewer 可视化）
        if transition_info:
            meta["transition"] = transition_info
        elif isinstance(gate_eval, dict):
            # 从 gate_eval 中提取 transition 信息
            runtime_profile = gate_eval.get("runtime_profile", {})
            if runtime_profile:
                meta["transition"] = runtime_profile.get("transition", {})
                meta["counters"] = runtime_profile.get("counters", {})
        
        # TEMP: 提取临时证据信息（如果存在）
        if isinstance(gate_eval, dict) and "evidence" in gate_eval:
            meta["evidence"] = gate_eval["evidence"]
        
        return GateRuntimeProfile(
            version="v0.5",
            gate_mode=gm,
            compute_level=compute,
            tick_interval_ms=tick_ms,
            allow_future_probe=allow_future_probe,
            authority_scope=authority_scope,
            blocked_by=blocked_by,
            human_reason=gate_reason,
            meta=meta,
        )

    # ------------------------------------------------------------
    # 对外主入口：PipelineController 每帧调用
    # ------------------------------------------------------------
    def tick(
        self,
        frame_ts: float,
        perception: Dict[str, Any],
        frame_id: Optional[int] = None
    ) -> Optional[Dict[str, Any]]:
        """
        frame_ts: seconds (human time)
        
        v0.4.2:
        Gate is the first-class authority of B runtime.
        
        v0.4.3:
        Every frame writes trace (even NO_OP / SUSPENDED).
        
        # ============================================================
        # Gate Authority Table — B2 v0.4.2 (Frozen)
        # ============================================================
        # Gate 是 B2 Runtime 的唯一"发声裁判"
        # Gate 不参与任何业务判断，只裁决：B 能不能说话、能不能写、能不能影响 C
        #
        # 核心原则：
        # 1) 缺少关键视角信息（view_state） ⇒ 永远不允许 ACTIVE
        # 2) B 永远只能"提醒"，不能"确认风险"
        # 3) Gate=SUSPENDED / READ_ONLY 必须硬性拦截输出
        #
        # ------------------------------------------------------------
        # Gate Mode 权限表
        #
        # | Gate Mode  | 运行状态说明              | Timeline | B→C Message | Memory |
        # |------------|---------------------------|----------|-------------|--------|
        # | SUSPENDED  | 视角不可用 / 高污染       | ❌ NO    | ❌ NO       | ❌ NO  |
        # | READ_ONLY  | 证据不足 / 视角不完整     | ❌ NO    | ❌ NO       | ✅ YES |
        # | ACTIVE     | 视角稳定 + 距离合规       | ✅ YES   | ✅ YES      | ✅ YES |
        #
        # ------------------------------------------------------------
        # 强制规则（不可违反）：
        #
        # R1. Gate=SUSPENDED  → tick() 必须返回 None
        # R2. Gate=READ_ONLY  → 禁止 timeline / 禁止 B→C
        # R3. perception 中缺少 view_state → 最高只能 READ_ONLY
        # R4. Gate 决策必须写入 trace（gate_eval）
        #
        # ------------------------------------------------------------
        # Block Reasons（示例）：
        # - missing_view_state
        # - camera_shake
        # - unstable_pose
        # - bad_fov
        # - too_close
        # - insufficient_evidence
        # ============================================================
        """
        # =====================================================
        # v0.4.3 baseline trace (always)
        # =====================================================
        if frame_id is None:
            if self.log_base_ts is not None:
                frame_id = int((frame_ts - self.log_base_ts) * self.fps)
            else:
                frame_id = int(frame_ts * self.fps)
        
        t_str = format_video_time(frame_ts)
        trace_rec: Dict[str, Any] = {
            "event_type": "tick",  # v0.5: 显式标记决策事件（与 GATE_RUNTIME_PROFILE 区分）
            "time": {
                "t_video_s": round(frame_ts, 3),
                "t_str": t_str,
                "frame_id": frame_id,
                "fps": self.fps
            },
            "runtime": {
                "module": "B2",
                "version": "0.4.3",
                "state": "ACTIVE",
                "reason": ""
            },
            "gate": {},
            "factors": {
                "scores": {},
                "reasons": {},
                "evidences_present": [],
                "main_factor": None
            },
            "impact": {
                "impact": "NO_OP",
                "level": "NOTICE",
                "confidence": 0.0,
                "intervention_level": "SOFT",
                "advisory_only": True
            },
            "to_c": {
                "send": False,
                "msg": {},
                "suppressed_reason": ""
            },
            "writeback": {
                "timeline": False,
                "health": False,
                "memory": False,
                "evidence_pack": False,
                "paths": {}
            },
            "dcs": {
                "score": 100,
                "grade": "GREEN",
                "violations": [],
                "notes": {}
            }
        }
        
        # =====================================================
        # v0.4.2 Gate FIRST — runtime authority
        # =====================================================
        
        # 从 perception 中提取 Gate 所需的最小信息
        stability_score = None
        range_m = None
        pitch_deg = 0.0
        roll_deg = 0.0
        visibility_score = 0.75
        
        if isinstance(perception, dict):
            view_state = perception.get("view_state", {})
            stability_score = view_state.get("stability_score")
            range_m = view_state.get("range_m")
            visibility_score = view_state.get("visibility_score", 0.75)
        
        # 如果没有从 perception 获取，使用实例变量或默认值
        if stability_score is None:
            # 使用现有的计算逻辑（如果 imu_data 存在）
            if self.imu_data:
                angular_velocity = self.imu_data.get("angular_velocity_deg_s", 0.0)
                accel_variance = self.imu_data.get("accel_variance", 0.0)
                stability_score = compute_stability_score(
                    angular_velocity_deg_s=angular_velocity,
                    accel_variance=accel_variance
                )
                pitch_deg = self.imu_data.get("pitch_deg", 0.0)
                roll_deg = self.imu_data.get("roll_deg", 0.0)
            else:
                stability_score = 1.0  # 默认稳定
        
        if range_m is None:
            range_m = self.range_m if self.range_m is not None else 10.0
        
        # ============================================================
        # v1.0: B does not run Gate; keep runtime profile informational only.
        # ============================================================
        system_ts = time.time()
        gate_mode_str = "ACTIVE"
        gate_reason = "B_NO_GATE"
        gate_trace = {}
        hysteresis_info = {}
        profile = self._build_runtime_profile_v05(
            gate_mode=gate_mode_str,
            gate_reason=gate_reason,
            gate_eval={},
            frame_ts=frame_ts,
            perception=perception,
            frame_id=frame_id,
            hysteresis_info=hysteresis_info,
        )
        
        # Trace: always write runtime profile (even if silent)
        try:
            if hasattr(self, "trace_writer_v043") and self.trace_writer_v043:
                self.trace_writer_v043.write({
                    "event_type": "GATE_RUNTIME_PROFILE",
                    "time": {"ts": frame_ts, "frame_id": frame_id},
                    "gate_runtime_profile": profile.to_dict(),
                })
        except Exception:
            # Never block runtime due to trace failures
            pass
        
        # ============================================================
        # v1.0: B must always produce candidates; no early returns here.
        # ============================================================
        
        # ACTIVE + FULL: fall through to existing v0.4.x pipeline
        gate_mode_str = profile.gate_mode.value  # 更新 gate_mode_str 用于后续逻辑
        
        # 更新 trace_rec 的 gate 字段（包含完整 runtime_profile）
        trace_rec["gate"] = profile.to_dict()
        trace_rec["runtime"]["state"] = gate_mode_str
        trace_rec["runtime"]["reason"] = profile.blocked_by or ""
        
        # v0.4.2: Always write gate trace for auditability (does NOT write timeline)
        view_state_dict = {}
        if isinstance(perception, dict):
            view_state_dict = perception.get("view_state", {}) or {}
        
        # 使用 profile 中的信息构建 gate_trace
        gate_trace_dict = profile.meta.get("gate_eval", {}) if profile.meta else {}
        self._write_gate_trace(
            frame_ts=frame_ts,
            frame_id=frame_id,
            gate_mode=gate_mode_str,
            gate_reason=profile.human_reason,
            gate_trace=gate_trace_dict,
            view_state=view_state_dict,
        )
        
        # =========================
        # v0.4.1 Patch 3: 系统时间唯一性
        # =========================
        self._current_frame_id = frame_id
        
        # 初始化 trace 字典（用于后续的旧 trace_writer）
        trace = {}
        
        # =========================
        # 0. Meta 信息（v0.5 新增）
        # =========================
        trace["meta"] = {
            "b_version": "0.5.0",
            "trace_version": "0.5",
            "video_id": None,
            "camera_id": None,
            "build_hash": None
        }
        
        # =========================
        # 1. 时间信息（人类视角，v0.5 格式：MM:SS.mmm）
        # =========================
        if frame_id is None:
            if self.log_base_ts is not None:
                frame_id = int((frame_ts - self.log_base_ts) * self.fps)
            else:
                frame_id = int(frame_ts * self.fps)
        
        # 格式化 human_time 为 MM:SS.mmm
        if self.log_base_ts is not None:
            elapsed = frame_ts - self.log_base_ts
        else:
            elapsed = frame_ts
        
        minutes = int(elapsed // 60)
        seconds = int(elapsed % 60)
        milliseconds = int((elapsed % 1) * 1000)
        human_time_str = f"{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
        
        trace["time"] = {
            "ts": round(frame_ts, 3),
            "frame_id": frame_id,
            "fps": self.fps,
            "human_time": human_time_str,
        }
        
        # 从 profile 中提取 gate_trace 信息用于 trace 字典
        gate_trace_from_profile = profile.meta.get("gate_eval", {}) if profile.meta else {}
        trace["gate_eval"] = {
            "mode": gate_mode_str,
            "blocked_by": profile.blocked_by or "",
            "details": gate_trace_from_profile.get("details", {}),
            "human_readable": profile.human_reason or "",
            "stability_score": gate_trace_from_profile.get("stability_score", 0.0),
            "can_trigger": gate_mode_str == "ACTIVE"
        }
        
        # 计算 view_state（用于 trace 字典）
        angular_velocity = 0.0
        accel_variance = 0.0
        linear_velocity = 0.0
        pitch_deg = 0.0
        roll_deg = 0.0
        
        if self.imu_data:
            angular_velocity = self.imu_data.get("angular_velocity_deg_s", 0.0)
            accel_variance = self.imu_data.get("accel_variance", 0.0)
            linear_velocity = self.imu_data.get("linear_velocity_m_s", 0.0)
            pitch_deg = self.imu_data.get("pitch_deg", 0.0)
            roll_deg = self.imu_data.get("roll_deg", 0.0)
        
        view_state = compute_view_state(
            angular_velocity_deg_s=angular_velocity,
            linear_velocity_m_s=linear_velocity,
            accel_variance=accel_variance,
            pitch=pitch_deg,
            roll=roll_deg,
            yaw_delta=0.0,
            zoom_level=1.0,
            fov_change=False
        )
        trace["view_state"] = view_state
        
        # 4. 继续执行（Gate=ACTIVE 或 READ_ONLY，使用已定义的 profile）
        # READ_ONLY：允许内部观察，但禁止任何对外输出（timeline / B→C / summary）
        # 1. 写入未来 buffer（B2 只记录，不解释）
        self._append_future_state(frame_ts, perception)
        
        # 2. 提取 [now+1s, now+8s] 窗口
        future_states = self._collect_future_window(frame_ts)
        window_size = len(future_states) * (1.0 / self.fps) if future_states else 0.0
        
        # =========================
        # v0.5: 根据 compute_level 获取计算预算（在感知之前）
        # =========================
        # 确保 profile 已定义（防御性检查）
        if 'profile' not in locals():
            raise RuntimeError("profile not defined before compute_budget calculation")
        compute_budget = self.scheduler_v05.get_compute_budget(profile)
        
        # =========================
        # 2. B2 Runtime State Machine v0.5（状态机先于判断）
        # =========================
        # 更新状态机（基于窗口大小和是否有 evidences）
        has_evidences = len(future_states) >= 2
        state_gate = self.state_machine.tick(
            frame_ts=frame_ts,
            window_size=window_size,
            has_evidences=has_evidences
        )
        
        # 写入 runtime_state 和 state_gate（v0.5 强制字段）
        trace["runtime_state"] = self.state_machine.get_runtime_state_dict(frame_ts)
        trace["state_gate"] = self.state_machine.get_state_gate_dict(state_gate)
        
        # v0.4 兼容字段（使用 GateEvaluatorV05 的结果）
        gate_mode_enum = B2GateMode.ACTIVE if gate_mode_str == "ACTIVE" else (
            B2GateMode.READ_ONLY if gate_mode_str == "READ_ONLY" else B2GateMode.SUSPENDED
        )
        b_active = state_gate.can_trigger and gate_mode_str == "ACTIVE"
        b_mode = gate_mode_str
        b_reason = gate_trace.get("blocked_by") or state_gate.reason
        
        trace["b_runtime_state"] = {
            "active": b_active,
            "mode": b_mode,
            "reason": b_reason
        }
        
        # v1.0: B does not suppress output based on runtime state_gate
        
        # 写入 runtime_state 和 state_gate（v0.5 强制字段）
        trace["runtime_state"] = self.state_machine.get_runtime_state_dict(frame_ts)
        trace["state_gate"] = self.state_machine.get_state_gate_dict(state_gate)
        
        # v0.4 兼容字段（使用 GateEvaluatorV05 的结果）
        b_active = state_gate.can_trigger and gate_mode_str == "ACTIVE"
        b_mode = gate_mode_str
        b_reason = gate_trace.get("blocked_by") or state_gate.reason
        
        trace["b_runtime_state"] = {
            "active": b_active,
            "mode": b_mode,
            "reason": b_reason
        }
        
        # v1.0: B does not suppress output based on runtime state_gate or future_states

    def _write_gate_trace(
        self,
        frame_ts: float,
        frame_id: Optional[int],
        gate_mode: str,
        gate_reason: str,
        gate_trace: Dict[str, Any],
        view_state: Dict[str, Any],
    ) -> None:
        """
        v0.4.2: Gate trace is ALWAYS written for auditability.
        This is NOT timeline. This is per-frame diagnostic jsonl.
        """
        try:
            import os
            import json
            os.makedirs(os.path.dirname(self._gate_trace_path), exist_ok=True)
            rec = {
                "ts": float(frame_ts),
                "frame_id": frame_id,
                "gate_mode": gate_mode,
                "gate_reason": gate_reason,
                "gate": gate_trace,
                "view_state": view_state,
            }
            with open(self._gate_trace_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        except Exception:
            # Never break runtime due to tracing
            return

    # ------------------------------------------------------------
    # 内部方法
    # ------------------------------------------------------------

    def _append_future_state(self, ts: float, perception: Dict[str, Any]):
        self._future_buffer.append({
            "ts": ts,
            "perception": perception
        })

    def _collect_future_window(self, now_ts: float) -> List[Dict[str, Any]]:
        """
        收集未来窗口内的状态
        注意：实际实现中，我们收集的是"从现在往前回溯"的状态
        因为这些状态会延续到未来窗口
        """
        # 收集过去窗口内的状态（用于预测未来）
        # 窗口大小 = future_window_end
        window_start = now_ts - self.future_window_end
        window_end = now_ts

        return [
            s for s in self._future_buffer
            if window_start <= s["ts"] <= window_end
        ]

    def _summarize_world_change(
        self,
        evidences: Dict[FactorType, FactorEvidence],
        ts: float,
        read_only: bool = False  # v0.4.2: Gate READ_ONLY 标志（接受但不改逻辑）
    ) -> Dict[str, Any]:
        """
        B2 v0.4+
        核心原则：
        - 不描述世界
        - 只回答：是否需要 C 改变行为
        
        v0.4.2: read_only 参数用于标记 Gate=READ_ONLY 状态，
        但不改变决策逻辑（Gate 只裁决资格，不干预行为）。
        """

        # =========================
        # 1. 选择主因子（仅用于假设，不做裁决）
        # =========================
        main_factor = None

        if FactorType.EVENT in evidences:
            main_factor = FactorType.EVENT
        elif FactorType.PATH in evidences:
            main_factor = FactorType.PATH
        elif FactorType.PEOPLE in evidences:
            main_factor = FactorType.PEOPLE

        # =========================
        # 2. 汇总输出（结构化，不讲故事）
        # =========================
        scores = {k.value: v.score for k, v in evidences.items()}
        reasons = {k.value: v.reason for k, v in evidences.items()}

        # main confidence：取 main_factor 对应的 score（没有则 0）
        main_score = 0.0
        if main_factor is not None:
            main_score = float(evidences.get(main_factor).score) if evidences.get(main_factor) else 0.0
        
        # 浮点稳定化：round 到 2 位小数，避免浮点误差导致去重误判
        main_score = round(main_score, 2)

        # v0.5: 生成 reason 描述
        reason = None
        if main_factor and main_factor in evidences:
            ev = evidences[main_factor]
            reason = ev.reason
        
        # =========================
        # v0.4.1 Patch 3: 系统时间唯一性
        # =========================
        system_ts = time.time()
        # 禁止在 summary 中混用时间源（只允许 system_ts）
        # 注意：frame_ts 是函数参数，perception_ts 不在这个作用域
        
        # =========================
        # v0.4.1 Patch 7: B/C 边界不可反转（结构声明）
        # =========================
        
        return {
            "ts": ts,
            "system_ts": system_ts,                 # ← v0.4.1: 系统时间
            "window": [self.future_window_start, self.future_window_end],
            "main_factor": main_factor,              # ← FactorType enum
            "confidence": main_score,               # ← main_factor 的 score，用于去重判断
            "scores": scores,
            "reasons": reasons,
            "reason": reason,                        # ← v0.5 新增：原因描述
            "assumptions": {
                "evidence_type": main_factor.value if main_factor else None,
                "evidence_score": main_score,
            },
            "cost_estimate": {
                "risk_proxy": main_score
            },
            "explanation": reason,
            "role": "B",
        }

    def _is_duplicate(self, summary: Dict[str, Any]) -> bool:
        """
        v0.4+ 去重规则（核心修复）：
        - 以 impact 为主语义，而不是 level（level 太粗，会吞变化）
        - 同时考虑 main_factor 与 confidence 变化，避免"同类建议"在强度变化时被吞
        """
        # @future_evolution_candidate: 去重逻辑冻结，当前版本不生效
        return False

        # 兼容：老 summary 可能没有 impact（但你现在已经有了）
        impact = summary.get("impact", "")
        last_impact = self._last_summary.get("impact", "")

        # confidence 缺失时默认 0
        conf = float(summary.get("confidence", 0.0)) if summary.get("confidence") is not None else 0.0
        last_conf = float(self._last_summary.get("confidence", 0.0)) if self._last_summary.get("confidence") is not None else 0.0

        # 允许同一 impact 在强度变化时重新输出（避免"越来越危险但不再说话"）
        CONF_EPS = 0.12

        return (
            summary.get("main_factor") == self._last_summary.get("main_factor")
            and impact == last_impact
            and abs(conf - last_conf) < CONF_EPS
        )

    def _log_factor_changes(self, ts: float, evidences: Dict[FactorType, FactorEvidence]):
        """检测因子变化并记录 FACTOR 日志"""
        for factor_type, evidence in evidences.items():
            factor_name = factor_type.value
            
            # 检查是否是新变化
            if factor_type not in self._last_factor_evidences:
                # 新因子出现
                self.logger.factor(ts, factor_name, evidence.reason, direction="↑")
            else:
                # 检查是否有显著变化
                last_evidence = self._last_factor_evidences[factor_type]
                if evidence.score > last_evidence.score + 0.1:  # 阈值可调
                    self.logger.factor(ts, factor_name, evidence.reason, direction="↑")
                elif evidence.score < last_evidence.score - 0.1:
                    self.logger.factor(ts, factor_name, evidence.reason, direction="↓")
            
            # 更新因子状态
            self._last_factor_evidences[factor_type] = evidence
    
    def _log_decision(
        self,
        summary: Dict[str, Any],
        evidences: Dict[FactorType, FactorEvidence]
    ):
        """记录 DECISION 日志：关键输出（最重要）"""
        decision_type = summary['level']
        main_factor = summary['main_factor']
        
        # 计算置信度（使用最高分因子的 score）
        confidence = max([v.score for v in evidences.values()]) if evidences else 0.0
        
        # 构建人类可读的原因描述
        reason_parts = []
        for factor_type, evidence in evidences.items():
            if factor_type.value == main_factor:
                reason_parts.append(evidence.reason)
        
        if not reason_parts:
            reason = "multiple factors changed"
        else:
            reason = " / ".join(reason_parts)
        
        # 提取所有因子分数
        scores = {k.value: v.score for k, v in evidences.items()}
        
        # 构建组合因子描述
        combined_factors = ", ".join([k.value for k in evidences.keys()])
        
        # 使用更详细的日志格式
        self.logger.decision(
            ts=summary['ts'],
            decision_type=decision_type,
            main_factor=main_factor,
            confidence=confidence,
            reason=reason
        )
        
        # 额外输出分数信息（用于审计）
        scores_str = " ".join([f"{k}={v:.2f}" for k, v in scores.items()])
        print(f"[B2-v0.3][DECISION][{self.logger.format_ts(summary['ts'])}] "
              f"main_factor: {main_factor} combined: {combined_factors} "
              f"confidence: {confidence:.2f} scores: {scores_str}")
    
    def _log_health_event(
        self, 
        summary: Dict[str, Any], 
        evidences: Dict[FactorType, FactorEvidence],
        gate_mode_str: str = None,  # v0.4.2: Gate 模式
        gate_trace: Dict[str, Any] = None  # v0.4.2: Gate trace 信息
    ):
        """记录健康事件（只记录有决策输出的情况）"""
        # 提取 factor scores 和 reasons
        scores = {k.value: v.score for k, v in evidences.items()}
        reasons = {k.value: v.reason for k, v in evidences.items()}
        
        # 计算总体 confidence（使用最高分因子的 score）
        confidence = max([v.score for v in evidences.values()]) if evidences else 0.0
        
        # 记录事件
        self.health_logger.log(
            B2HealthEvent(
                ts=summary['ts'],
                decision=summary['level'],
                impact=summary.get('impact'),  # 真实语义：NEED_STOP / NEED_DETOUR / PATH_UNCERTAIN / NEED_SLOW_DOWN / NO_OP
                scores=scores,
                reasons=reasons,
                confidence=confidence,
                main_factor=summary['main_factor'],
                # v0.4.2: Gate 信息（可追溯）
                gate_mode=gate_mode_str,
                gate_blocked_by=gate_trace.get("blocked_by") if gate_trace else None
            )
        )

    def _debug_print(self, summary, evidences):
        print("\n[B2-v0.3] WORLD CHANGE DETECTED")
        print(f" ts: {summary['ts']:.2f}")
        print(f" level: {summary['level']}")
        print(f" main_factor: {summary['main_factor']}")
        print(f" window: [{summary['window'][0]:.1f}s, {summary['window'][1]:.1f}s]")
        for k, v in evidences.items():
            print(f"  - {k.value}: score={v.score:.2f} reason={v.reason}")
    
    # =========================
    # Trace 辅助函数（v0.4）
    # =========================
    
    def _get_b_runtime_state(self, perception: Dict[str, Any]):
        """1️⃣ B 是否运行"""
        if self.camera_unstable:
            return False, "GATED", "camera unstable"
        if self.distance_to_front < 3.0:
            return False, "READ_ONLY", "delegated to C (<3m)"
        return True, "ACTIVE", "normal operation"
    
    def _check_trigger(self, evidences: Dict[FactorType, FactorEvidence]):
        """2️⃣ Trigger 判断（跨阈值，v0.5 格式）"""
        if not evidences:
            return {
                "triggered": False,
                "reason": "no_effective_factors"
            }
        
        # 阈值定义
        thresholds = {
            FactorType.EVENT: 0.65,
            FactorType.PATH: 0.6,
            FactorType.PEOPLE: 0.75,
            FactorType.ENV: 0.0  # ENV 不触发
        }
        
        for k, v in evidences.items():
            threshold = thresholds.get(k, 1.0)
            if v.score >= threshold:
                return {
                    "triggered": True,
                    "trigger_factor": k.value,
                    "trigger_reason": f"{k.value}_factor_above_threshold"
                }
        
        return {
            "triggered": False,
            "reason": "no_effective_factors"
        }
    
    def _to_human_readable(self, summary: Dict[str, Any]):
        """4️⃣ 人类可读转译（只给审计看）"""
        impact = summary.get("impact")
        
        if impact == "NEED_SLOW_DOWN":
            return {
                "summary": "前方路面发生变化，继续前进可能不太舒适。",
                "urgency": "soft",
                "risk": "low"
            }
        if impact == "NEED_STOP":
            return {
                "summary": "前方存在高风险事件，继续前进可能不安全。",
                "urgency": "high",
                "risk": "high"
            }
        if impact == "PATH_UNCERTAIN":
            return {
                "summary": "前方路径不确定，需要谨慎前进。",
                "urgency": "medium",
                "risk": "medium"
            }
        if impact == "NEED_DETOUR":
            return {
                "summary": "前方路径不可行，建议绕行。",
                "urgency": "high",
                "risk": "high"
            }
        return {
            "summary": "当前情况对行走无明显影响。",
            "urgency": "none",
            "risk": "none"
        }
    
    def _build_message_to_c(self, summary: Dict[str, Any], final_confidence: float):
        """5️⃣ B → C 消息（v0.5 格式：使用 payload）"""
        impact_obj = summary.get("impact")
        if hasattr(impact_obj, "name"):
            impact_str = impact_obj.name
        elif hasattr(impact_obj, "value"):
            impact_str = impact_obj.value
        else:
            impact_str = str(impact_obj)
        
        if impact_str == "NO_OP":
            return {"sent": False, "reason": "impact_is_no_op"}
        
        # =========================
        # v0.4.1 Patch 3: 系统时间唯一性
        # =========================
        system_ts = summary.get("system_ts", time.time())
        
        # 计算 valid_until（建议有效期窗口，非承诺时间）
        # P2 约束：不允许"未来必然发生"的时间承诺
        # valid_until 只是"建议在此时间前考虑此预警"，不是"承诺在此时间前有效"
        valid_until_ts = system_ts + 3.0
        
        # 格式化 valid_until 为 human_time
        if self.log_base_ts is not None:
            elapsed = valid_until_ts - self.log_base_ts
        else:
            elapsed = valid_until_ts
        
        minutes = int(elapsed // 60)
        seconds = int(elapsed % 60)
        milliseconds = int((elapsed % 1) * 1000)
        valid_until_str = f"{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
        
        result = {
            "sent": True,
            "payload": {
                "header": {
                    "system_ts": system_ts,  # ← v0.4.1 Patch 3: 系统时间
                    "frame_id": self._current_frame_id if hasattr(self, "_current_frame_id") else None
                },
                "impact": impact_str,
                "confidence": round(final_confidence, 3),
                "valid_until": valid_until_str,  # ← 建议有效期窗口（非承诺时间）
                "advisory_only": True,  # ← v0.4.1 Patch 1: 强制语义
                "intervention_level": summary.get("intervention_level", "SOFT")  # ← v0.4.1 Patch 2
            }
        }

        if assert_b_invariants:
            assert_b_invariants(result.get("payload", {}))
        return result
    
    def _write_outputs(self, summary: Dict[str, Any]):
        """写入情况（有没有打标，v0.5 简化格式）"""
        impact = summary.get("impact")
        timeline_written = impact not in ("NO_OP", None)
        
        if timeline_written:
            self._timeline_index += 1
        
        return {
            "timeline_written": timeline_written,
            "health_log_written": timeline_written,
            "memory_written": False
        }

