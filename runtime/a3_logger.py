import json
import logging
import os
import time
from typing import Optional

from config import LOG_CONFIG
from intervention.eligibility import (
    infer_task_state,
    compute_intervention_eligibility,
)
from intervention.task_state_override import TaskStateOverride
from intervention.action_mapper_m_v0 import (
    map_winner_to_action_plan,
    IntentInfo,
    SlotInfo,
    _winner_type_to_enum,
)
from intervention.engagement_v0 import get_engagement_v0
from intervention.rhythm_v0 import get_rhythm_v0
from pal.lookahead_modulation import apply_pal_lookahead
from pal.v0 import compute_pal_horizon_difficulty

log = logging.getLogger("A3")
_LAST_TS = 0.0


def log_a3(mode, signals=None):
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


def log_a3_timeseries(mode, signals=None, frame_context=None, interval_sec: float = 1.0, runtime_ctx=None, speech_gate=None):
    if mode is None or signals is None:
        return

    global _LAST_TS
    now = time.time()
    if now - _LAST_TS < interval_sec:
        return
    _LAST_TS = now

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

    # J) ENGAGED 事实信号：改在 main「最终决定不说」处调用 log_engaged_signal（signal-only，解释交给 N 层）

    log_dir = LOG_CONFIG["log_dir"]
    os.makedirs(log_dir, exist_ok=True)
    path = os.path.join(log_dir, "a3_trace.jsonl")
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")


def log_multimodal_conflict(multimodal_conflict: dict) -> None:
    """
    K) 多模态输入冲突 v0：记录冲突解决到 trace。
    """
    payload = {"ts": time.time(), "multimodal_conflict": multimodal_conflict}
    log_dir = LOG_CONFIG["log_dir"]
    os.makedirs(log_dir, exist_ok=True)
    path = os.path.join(log_dir, "a3_trace.jsonl")
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")


def log_shadow_decision(shadow_decision: dict, shadow_reason: str = "SHADOW_MODE_ENABLED") -> None:
    """
    L) 影子运行模式 v0：记录"如果真运行会发生什么"到 trace。
    """
    payload = {
        "ts": time.time(),
        "shadow_decision": shadow_decision,
        "shadow_reason": shadow_reason,
    }
    log_dir = LOG_CONFIG["log_dir"]
    os.makedirs(log_dir, exist_ok=True)
    path = os.path.join(log_dir, "a3_trace.jsonl")
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")


def log_arbitration_event(
    arbitration: dict,
    k: Optional[dict] = None,
    l: Optional[dict] = None,
    context: Optional[dict] = None,
) -> None:
    """
    G) 多任务介入仲裁 v0：记录 arbitration 决策到 trace。
    K) 介入意图层 v0：可选写入 k.intent，与 G 同条 trace。
    L) 介入内容规划层 v0：可选写入 l（slot_type + slot），与 G 同条 trace。
    M) 行为绑定层 v0：在写 trace 前在此处调用 mapper，生成 m 并写入；shadow-only。
    """
    payload = {"ts": time.time(), "arbitration": arbitration}
    if k is not None:
        payload["k"] = k
    if l is not None:
        payload["l"] = l

    ctx = context or {}
    # M 层：仲裁结果已确定后、写 trace 前，在此唯一接入点生成 m（即使 winner=None 或 k/l 缺省也写 m）
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

    log_dir = LOG_CONFIG["log_dir"]
    os.makedirs(log_dir, exist_ok=True)
    path = os.path.join(log_dir, "a3_trace.jsonl")
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")


def log_advice_rhythm_event(advice_rhythm: dict) -> None:
    """
    E) Advice 内容类型节律 v0：记录 advice_rhythm 决策到 trace。
    在 AdviceEngine → Decision 之间调用，仅当 gate 检查时写入。
    """
    payload = {"ts": time.time(), "advice_rhythm": advice_rhythm}
    log_dir = LOG_CONFIG["log_dir"]
    os.makedirs(log_dir, exist_ok=True)
    path = os.path.join(log_dir, "a3_trace.jsonl")
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")


def log_engaged_signal(signal_payload: dict, outcome_payload: Optional[dict] = None) -> None:
    """
    J) ENGAGED 事实信号 v0：写入 engaged_signal（signal-only）。
    N) Outcome v0：同条 trace 写入 outcome（outcome_type / reason / confidence / evidence），系统唯一解释层。
    """
    payload = {"ts": time.time(), "engaged_signal": signal_payload}
    if outcome_payload is not None:
        payload["outcome"] = outcome_payload
    log_dir = LOG_CONFIG["log_dir"]
    os.makedirs(log_dir, exist_ok=True)
    path = os.path.join(log_dir, "a3_trace.jsonl")
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")
