# intervention/p_policy_v1.py
from dataclasses import dataclass
from typing import Optional, Dict, Any
import time


@dataclass
class P1Decision:
    apply_now: bool
    reason: str
    cooldown_remaining_s: float = 0.0
    debug: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "apply_now": self.apply_now,
            "reason": self.reason,
            "cooldown_remaining_s": round(self.cooldown_remaining_s, 3),
            "debug": self.debug or {},
        }


@dataclass
class P1Config:
    # 执行门禁
    require_action_type: str = "SAY"
    require_engagement_levels: tuple = ("L2", "L3")
    require_rhythm_state: str = "ENGAGED"

    # ENGAGED 稳定时间门槛（秒）
    engaged_stable_s: float = 3.0

    # SAY 冷却（秒）
    say_cooldown_s: float = 15.0

    # 当 S=SATURATED 时禁止突然开口
    block_when_s_saturated: bool = True


def decide_p1_apply_now(
    *,
    cfg: P1Config,
    now_ts: float,
    m: Dict[str, Any],
    engagement: Dict[str, Any],
    rhythm: Dict[str, Any],
    s_report: Optional[Dict[str, Any]],
    last_say_ts: Optional[float],
    rhythm_entered_ts: Optional[float],
) -> P1Decision:
    """
    P1 只做：决定 apply_now 是否可以 True
    所有 reason 冻结为 BLOCKED_* / OK_* 形式，便于 Q/R/S 统计。
    """

    action_type = (m or {}).get("action_type") or (m or {}).get("action") or "NONE"
    if action_type != cfg.require_action_type:
        return P1Decision(False, "BLOCKED_NOT_SAY", debug={"action_type": action_type})

    level = (engagement or {}).get("level", "L0")
    if level not in cfg.require_engagement_levels:
        return P1Decision(False, "BLOCKED_LOW_ENGAGEMENT", debug={"level": level})

    r_state = (rhythm or {}).get("state", "IDLE")
    if r_state != cfg.require_rhythm_state:
        return P1Decision(False, "BLOCKED_NOT_ENGAGED", debug={"rhythm_state": r_state})

    # ENGAGED 稳定门槛：防止刚 ENGAGED 就说话
    if rhythm_entered_ts is None:
        # 没有 entered_ts 时，保守处理：不执行
        return P1Decision(False, "BLOCKED_NO_RHYTHM_TIMING", debug={"entered_ts": None})

    engaged_age = now_ts - rhythm_entered_ts
    if engaged_age < cfg.engaged_stable_s:
        return P1Decision(
            False,
            "BLOCKED_ENGAGED_NOT_STABLE",
            debug={"engaged_age": round(engaged_age, 3), "need": cfg.engaged_stable_s},
        )

    # S=SATURATED 禁止突然开口（避免“憋太久突然爆发”）
    if cfg.block_when_s_saturated and s_report is not None:
        s_level = s_report.get("stress_level")
        if s_level == "SATURATED":
            return P1Decision(False, "BLOCKED_S_SATURATED", debug={"s_level": s_level})

    # SAY 冷却
    if last_say_ts is not None:
        dt = now_ts - last_say_ts
        if dt < cfg.say_cooldown_s:
            return P1Decision(
                False,
                "BLOCKED_SAY_COOLDOWN",
                cooldown_remaining_s=max(0.0, cfg.say_cooldown_s - dt),
                debug={"since_last_say": round(dt, 3), "cooldown": cfg.say_cooldown_s},
            )

    return P1Decision(True, "OK_EXECUTE_SAY", debug={"level": level, "rhythm_state": r_state})
