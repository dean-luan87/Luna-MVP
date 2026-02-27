import json
import logging
import os
import time
from typing import Any, Optional

from config import LOG_CONFIG
from intervention.eligibility import (
    infer_task_state,
    compute_intervention_eligibility,
)
from intervention.task_state_override import TaskStateOverride
from intervention.engagement_v0 import get_engagement_v0
from intervention.rhythm_v0 import get_rhythm_v0
from pal.lookahead_modulation import apply_pal_lookahead
from pal.v0 import compute_pal_horizon_difficulty
from intervention.action_mapper_m_v0 import (
    ActionType,
    map_winner_to_action_plan,
    IntentInfo,
    SlotInfo,
    _winner_type_to_enum,
)

log = logging.getLogger("A3")
_LAST_TS = 0.0
_LAST_RHYTHM_STATE: Optional[str] = None
_LAST_ENGAGEMENT_LEVEL: Optional[str] = None

# 记录层 determinism：trace 写入使用与 A3 驱动同一时间源（run_video 注入 now_ms/1000）
_trace_time_sec: Optional[float] = None


def set_trace_time_sec(sec: Optional[float]) -> None:
    """设置 trace 写入用的固定时间（如 run_video 的 now_ms/1000）。不设置时用墙钟。"""
    global _trace_time_sec
    _trace_time_sec = sec


def _get_ts_for_trace() -> float:
    """trace 用时间戳：有注入则用注入，否则用墙钟。"""
    global _trace_time_sec
    if _trace_time_sec is not None:
        return _trace_time_sec
    return time.time()


def get_system_time_s() -> float:
    """
    唯一系统时间轴（秒）。
    实时模式 → time.time()；replay 模式 → 上层注入时间（set_trace_time_sec）。
    决策路径应只使用此接口，禁止直接 time.time()。
    """
    return _get_ts_for_trace()


# 阶段 1：trace 量化，消除浮点尾差，使 diff 字节级一致
TRACE_FLOAT_NDIGITS = 3


def _round_float(v: Any, ndigits: int = TRACE_FLOAT_NDIGITS) -> Any:
    """单值：仅对 float  round 到 ndigits 位小数。"""
    if isinstance(v, float):
        return round(v, ndigits)
    return v


def _quantize_floats(obj: Any, ndigits: int = TRACE_FLOAT_NDIGITS) -> Any:
    """递归：对 dict/list 内所有 float 统一 round，用于 trace 写入前。"""
    if isinstance(obj, float):
        return round(obj, ndigits)
    if isinstance(obj, dict):
        return {k: _quantize_floats(v, ndigits) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_quantize_floats(x, ndigits) for x in obj]
    return obj


def _write_trace_line(payload: dict) -> None:
    """统一写入 a3_trace.jsonl：先量化浮点再 dump，避免写失败阻塞。"""
    payload = _quantize_floats(payload)
    log_dir = LOG_CONFIG["log_dir"]
    os.makedirs(log_dir, exist_ok=True)
    path = os.path.join(log_dir, "a3_trace.jsonl")
    try:
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(payload, ensure_ascii=False) + "\n")
    except OSError:
        pass


def _serialize_mode(mode: Any) -> dict:
    """只序列化，不采样不推断。"""
    if mode is None:
        return {}
    out = {
        "complexity_score": round(getattr(mode, "complexity_score", 0), 3),
        "safety_level": getattr(getattr(mode, "safety_level", None), "value", None),
        "control_mode": getattr(getattr(mode, "control_mode", None), "value", None),
        "advice_budget_scale": round(getattr(mode, "advice_budget_scale", 0), 2),
        "pal_lookahead_m": round(getattr(mode, "pal_lookahead_m", 0), 1),
    }
    if getattr(mode, "debug", None):
        out["debug"] = {k: round(v, 3) for k, v in mode.debug.items()}
    return out


def log_a3(obs_or_mode: Any, decision_or_signals: Any = None) -> None:
    """
    补丁 v1：若第一参数为 ObservationFrame，则只记录 obs + decision，不调用 pipeline/rhythm/engagement。
    否则走 legacy log_a3(mode, signals)。
    """
    if hasattr(obs_or_mode, "sampled") and hasattr(obs_or_mode, "seq"):
        _log_a3_v1(obs_or_mode, decision_or_signals)
    else:
        _log_a3_legacy(obs_or_mode, decision_or_signals)


def _log_a3_v1(obs: Any, decision: Any) -> None:
    """只 dump obs + decision，不做采样、不补值、不推断。"""
    payload = {
        "ts": obs.ts,
        "dt": obs.dt,
        "seq": obs.seq,
        "sampled": obs.sampled,
        "obs": {
            "motion": obs.motion,
            "path": obs.path,
            "branch": obs.branch,
            "roi": obs.roi,
            "pal": obs.pal,
            "complexity": obs.complexity,
            "vc": obs.vc,
            "frame_quality": obs.frame_quality,
            "control_mode": obs.control_mode,
        },
        "decision": _serialize_mode(decision),
    }
    _write_trace_line(payload)


def _log_a3_legacy(mode, signals=None) -> None:
    if mode is None:
        return
    payload = {
        "tag": "A3",
        "complexity": round(mode.complexity_score, 3),
        "safety": mode.safety_level,
        "control": mode.control_mode,
        "advice_scale": round(mode.advice_budget_scale, 2),
        "pal_lookahead_m": round(mode.pal_lookahead_m, 1),
    }
    if mode.debug:
        payload["components"] = {
            k: round(v, 3)
            for k, v in mode.debug.items()
            if k not in ("raw", "ema")
        }
        payload["raw"] = round(mode.debug.get("raw", 0), 3)
    if signals is not None:
        payload["signals"] = {
            "risk": round(signals.risk_density, 2),
            "redline": signals.redline_hit,
            "occlusion": round(signals.occlusion_ratio, 2),
            "roi_count": signals.roi_count,
            "path_stability": round(signals.path_stability, 2),
            "branch": signals.branch_count,
            "speak": round(signals.recent_speak_rate, 2),
            "reject": round(signals.rejected_rate, 2),
            "has_goal": signals.has_goal,
            "perception": getattr(signals, "perception_state", None).value if getattr(signals, "perception_state", None) else None,
        }
    log.info(payload)


def log_a3_timeseries(
    mode,
    signals=None,
    frame_context=None,
    interval_sec: float = 1.0,
    runtime_ctx=None,
    speech_gate=None,
    pipeline_result: Optional[dict] = None,
):
    if mode is None or signals is None:
        return

    global _LAST_TS, _LAST_RHYTHM_STATE, _LAST_ENGAGEMENT_LEVEL
    now = _get_ts_for_trace()

    def _enum_value(x):
        return getattr(x, "value", x)

    frame_id = None
    if isinstance(frame_context, dict):
        frame_id = frame_context.get("frame_id")

    payload = {
        "ts": now,
        "frame_id": frame_id,
        "view": {
            "frame_quality": str(getattr(signals, "frame_quality", "GOOD")),
            "view_confidence": float(getattr(signals, "view_confidence", 1.0)),
            "motion_instability": float(getattr(signals, "motion_instability", 0.0)),
        },
        "a3": {
            "complexity_raw": float(mode.debug.get("raw", 0.0)) if mode.debug else 0.0,
            "complexity_effective": float(mode.debug.get("raw_effective", 0.0)) if mode.debug else 0.0,
            "safety_level": _enum_value(mode.safety_level),
            "control_mode": _enum_value(mode.control_mode),
        },
    }
    if mode.debug:
        payload["a3"]["components"] = {
            "motion": float(mode.debug.get("motion_instability", 0.0)),
            "path": float(mode.debug.get("path_instability", 0.0)),
            "roi": float(mode.debug.get("roi_load", 0.0)),
            "branch": float(mode.debug.get("branch_load", 0.0)),
        }
    path_in = getattr(signals, "path_instability", None)
    branch_in = getattr(signals, "branch_load", None)
    payload["a3"]["inputs"] = {
        "roi_count": int(getattr(signals, "roi_count", 0)),
        "path_instability": float(path_in) if path_in is not None else None,
        "branch_load": float(branch_in) if branch_in is not None else None,
    }

    # 主线 A：介入资格门禁（v0）- A3 之后、策略之前
    complexity_effective = float(mode.debug.get("raw_effective", 0.0)) if mode.debug else 0.0
    has_goal = bool(getattr(signals, "has_goal", False))
    explore_mode = bool(getattr(signals, "explore_mode", False))
    task_state = TaskStateOverride.get() or infer_task_state(has_goal, explore_mode)
    eligibility = compute_intervention_eligibility(task_state, complexity_effective)
    payload["intervention"] = {
        "eligible": eligibility["allowed"],
        "reason": eligibility["reason"],
        "task_state": task_state.value,
    }

    # PAL v0：只读前瞻，A3/Eligibility 之后，不反向影响
    motion_c = float(mode.debug.get("motion_instability", 0.0)) if mode.debug else 0.0
    path_c = float(mode.debug.get("path_instability", 0.0)) if mode.debug else 0.0
    branch_c = float(mode.debug.get("branch_load", 0.0)) if mode.debug else 0.0
    roi_c = float(mode.debug.get("roi_load", 0.0)) if mode.debug else 0.0
    vc = float(getattr(signals, "view_confidence", 1.0))
    pal_diff = compute_pal_horizon_difficulty(motion_c, path_c, branch_c, roi_c, vc)
    payload["pal"] = {"horizon_difficulty": round(pal_diff, 3)}

    # ACTIVE × PAL 节律 v0：何时进入/退出介入态（只读，不影响 eligibility/safety）
    rhythm_state = get_rhythm_v0().tick(
        now=now,
        pal=pal_diff,
        eligible=eligibility["allowed"],
        vc=vc,
        task_state=task_state.value,
    )
    payload["rhythm"] = {"state": rhythm_state}

    # ENGAGED 介入强度 v0：仅在 ENGAGED 时计算 L1/L2/L3
    control_mode_str = _enum_value(mode.control_mode)
    eng = get_engagement_v0().tick(
        now=now,
        rhythm_state=rhythm_state,
        pal=pal_diff,
        complexity=complexity_effective,
        vc=vc,
        control_mode=control_mode_str,
    )
    payload["engagement"] = {
        "level": eng.level,
        "advice_scale": round(eng.advice_scale, 2),
        "pal_lookahead_m": round(eng.pal_lookahead_m, 1),
        "speak_cooldown_s": round(eng.speak_cooldown_s, 1),
    }
    # 测试用：ACTIVE override 时强制 ENGAGED + L1，便于在任意视频下验证 arbitration/K/L 写入
    if TaskStateOverride.get() is not None:
        rhythm_state = "ENGAGED"
        payload["rhythm"] = {"state": rhythm_state}
        payload["engagement"]["level"] = "L1"
        payload["engagement"]["advice_scale"] = 0.7
        payload["engagement"]["pal_lookahead_m"] = 8.0
        payload["engagement"]["speak_cooldown_s"] = 8.0
    if runtime_ctx is not None:
        runtime_ctx.engagement = payload["engagement"]
        runtime_ctx.rhythm_state = rhythm_state
        runtime_ctx.eligibility = eligibility
        runtime_ctx.view_confidence = vc
        runtime_ctx.frame_quality = str(getattr(signals, "frame_quality", "GOOD"))

    # C) PAL 前瞻只读调制：ENGAGED 时用 engagement.pal_lookahead_m
    pal_base = getattr(mode, "pal_lookahead_m", 6.0)
    effective_lookahead = apply_pal_lookahead(
        pal_base_lookahead_m=pal_base,
        engagement=payload["engagement"],
        control_mode=control_mode_str,
    )
    payload["pal"]["lookahead_m"] = round(effective_lookahead, 1)
    if runtime_ctx is not None and runtime_ctx.engagement is not None:
        runtime_ctx.engagement["effective_pal_lookahead_m"] = round(effective_lookahead, 1)

    # 有效 tick 门禁：仅当 B2/C1 重算或 rhythm/engagement 状态变化时写 trace，避免空转循环撑爆日志
    if pipeline_result is not None:
        b2_recomputed = bool(pipeline_result.get("b2_recomputed", False))
        c1_recomputed = bool(pipeline_result.get("c1_recomputed", False))
        rhythm_changed = rhythm_state != _LAST_RHYTHM_STATE
        engagement_changed = eng.level != _LAST_ENGAGEMENT_LEVEL
        should_log = b2_recomputed or c1_recomputed or rhythm_changed or engagement_changed
    else:
        should_log = True

    if not should_log:
        return

    _LAST_TS = now
    _LAST_RHYTHM_STATE = rhythm_state
    _LAST_ENGAGEMENT_LEVEL = eng.level

    # J) ENGAGED 事实信号：改在 main「最终决定不说」处调用 log_engaged_signal（signal-only，解释交给 N 层）
    _write_trace_line(payload)


def log_multimodal_conflict(multimodal_conflict: dict) -> None:
    """
    K) 多模态输入冲突 v0：记录冲突解决到 trace。
    """
    payload = {"ts": _get_ts_for_trace(), "multimodal_conflict": multimodal_conflict}
    _write_trace_line(payload)


def log_shadow_decision(shadow_decision: dict, shadow_reason: str = "SHADOW_MODE_ENABLED") -> None:
    """
    L) 影子运行模式 v0：记录"如果真运行会发生什么"到 trace。
    """
    payload = {
        "ts": _get_ts_for_trace(),
        "shadow_decision": shadow_decision,
        "shadow_reason": shadow_reason,
    }
    _write_trace_line(payload)


def build_arbitration_payload(
    arbitration: dict,
    k: Optional[dict] = None,
    l: Optional[dict] = None,
    context: Optional[dict] = None,
) -> dict:
    """
    构建 arbitration tick 的 payload（含 m），不写 trace。
    P v0 接线：main 在此之后执行 P、写 outcome，再调用 write_arbitration_payload。
    """
    payload = {"ts": _get_ts_for_trace(), "arbitration": arbitration}
    if k is not None:
        payload["k"] = k
    if l is not None:
        payload["l"] = l

    ctx = context or {}
    winner_type_enum = _winner_type_to_enum(arbitration.get("winner_type"))
    intent_info = IntentInfo(intent=k.get("intent", "NONE") if k else "NONE")
    slot_info = SlotInfo(
        slot_type=l.get("slot_type", "NONE") if l else "NONE",
        slot=l.get("slot") if l else None,
    )
    action_plan = map_winner_to_action_plan(
        winner_type_enum,
        intent_info,
        slot_info,
        context={
            "pal": ctx.get("pal"),
            "engagement_level": ctx.get("level"),
            "view_confidence": ctx.get("vc"),
        },
    )
    payload["m"] = action_plan.to_trace_dict()

    # apply_now：仅 L2/L3 允许（P1：L1 只准备不执行，由 main 中 P1 策略最终决定是否执行）
    if (
        ctx.get("rhythm_state") == "ENGAGED"
        and ctx.get("level") in ("L2", "L3")
        and (arbitration.get("winner_type") or arbitration.get("winner"))
        and action_plan.action_type == ActionType.SAY
    ):
        payload["m"] = {**payload["m"], "apply_now": True}

    return payload


def write_arbitration_payload(payload: dict) -> None:
    """将 arbitration payload（可含 outcome）写入 trace。"""
    _write_trace_line(payload)


def log_arbitration_event(
    arbitration: dict,
    k: Optional[dict] = None,
    l: Optional[dict] = None,
    context: Optional[dict] = None,
):
    """
    G) 多任务介入仲裁 v0：记录 arbitration 决策到 trace。
    K/L/M 同条；不包含 outcome（outcome 由 P 接线点在 main 写入）。
    无 P 接线的 call site 可直接调用本函数；有 P 接线的 call site 应使用 build_arbitration_payload → P → outcome → write_arbitration_payload。
    """
    payload = build_arbitration_payload(arbitration, k=k, l=l, context=context)
    write_arbitration_payload(payload)
    return payload


def log_advice_rhythm_event(advice_rhythm: dict) -> None:
    """
    E) Advice 内容类型节律 v0：记录 advice_rhythm 决策到 trace。
    在 AdviceEngine → Decision 之间调用，仅当 gate 检查时写入。
    """
    payload = {"ts": _get_ts_for_trace(), "advice_rhythm": advice_rhythm}
    _write_trace_line(payload)


def log_advice_rhythm_record_spoken(
    ts_sec: float,
    advice_type: str,
    window_stats: dict,
    events_len: int,
) -> None:
    """
    行为路径 trace：record_spoken 调用点。
    用于 diff 两遍 replay，定位第一处分叉（ts、window_stats、events_len、类型计数）。
    """
    payload = {
        "ts": _get_ts_for_trace(),
        "advice_rhythm_record": {
            "ts": ts_sec,
            "advice_type": advice_type,
            "window_stats": dict(window_stats),
            "events_len": events_len,
        },
    }
    _write_trace_line(payload)


def log_engaged_signal(
    signal_payload: dict,
    outcome_payload: Optional[dict] = None,
    q_payload: Optional[dict] = None,
    r_payload: Optional[dict] = None,
    s_payload: Optional[dict] = None,
) -> None:
    """
    J) ENGAGED 事实信号 v0：写入 engaged_signal（signal-only）。
    N) Outcome v0：同条 trace 写入 outcome。
    Q/R/S：同条写入执行回执与观测（有则写），使 P→Q→R→S 整链在 J 路径也可观测。
    """
    payload = {"ts": _get_ts_for_trace(), "engaged_signal": signal_payload}
    if outcome_payload is not None:
        payload["outcome"] = outcome_payload
    if q_payload is not None:
        payload["q"] = q_payload
    if r_payload is not None:
        payload["r"] = r_payload
    if s_payload is not None:
        payload["s"] = s_payload
    _write_trace_line(payload)
