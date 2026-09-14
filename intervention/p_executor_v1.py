# intervention/p_executor_v1.py
from dataclasses import dataclass
from typing import Optional, Dict, Any, Callable
import time

from intervention.p_policy_v1 import P1Config, decide_p1_apply_now


@dataclass
class P1Outcome:
    ts: float
    executed: bool
    outcome_type: str         # ACTION_EXECUTED / NO_ACTION
    reason: str               # OK_* / BLOCKED_* / FAILED_*
    action_type: str          # SAY / NONE
    text_len: int
    debug: Dict[str, Any]
    apply_now: bool = False   # P1 门禁通过时 True；与 executed 分离以便 P2 在 main 中接棒

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ts": self.ts,
            "executed": self.executed,
            "outcome_type": self.outcome_type,
            "reason": self.reason,
            "action_type": self.action_type,
            "text_len": self.text_len,
            "debug": self.debug,
            "apply_now": self.apply_now,
        }


class P1Executor:
    """
    P1：真正执行 SAY 的最小执行器
    - 输入：arbitration payload（含 m/engagement/rhythm/s/text）
    - 输出：outcome（给 Q/R/S 统计）
    """

    def __init__(
        self,
        cfg: Optional[P1Config] = None,
        speak_fn: Optional[Callable[[str], None]] = None,
    ):
        self.cfg = cfg or P1Config()
        self.speak_fn = speak_fn  # 由 main.py 传入：tts_manager.speak 或等价函数
        self.last_say_ts: Optional[float] = None
        self._rhythm_state_prev: Optional[str] = None
        self._rhythm_entered_ts: Optional[float] = None

    def _update_rhythm_entered_ts(self, now_ts: float, rhythm_state: str):
        if self._rhythm_state_prev != rhythm_state:
            self._rhythm_state_prev = rhythm_state
            self._rhythm_entered_ts = now_ts

    def execute(
        self,
        *,
        payload: Dict[str, Any],
        now_ts: Optional[float] = None,
    ) -> P1Outcome:
        now = now_ts or time.time()

        m = payload.get("m") or {}
        engagement = payload.get("engagement") or {}
        rhythm = payload.get("rhythm") or {}
        s_report = payload.get("s")  # 可能 None
        text = payload.get("text") or ""

        action_type = m.get("action_type") or "NONE"
        rhythm_state = rhythm.get("state", "IDLE")
        self._update_rhythm_entered_ts(now, rhythm_state)

        # 先做门禁判定
        dec = decide_p1_apply_now(
            cfg=self.cfg,
            now_ts=now,
            m=m,
            engagement=engagement,
            rhythm=rhythm,
            s_report=s_report,
            last_say_ts=self.last_say_ts,
            rhythm_entered_ts=self._rhythm_entered_ts,
        )

        if not dec.apply_now:
            return P1Outcome(
                ts=now,
                executed=False,
                outcome_type="NO_ACTION",
                reason=dec.reason,
                action_type=action_type,
                text_len=len(text),
                debug={"p1": dec.to_dict()},
                apply_now=False,
            )

        # 允许执行但 text 为空：视为失败（可追责）
        if not text.strip():
            return P1Outcome(
                ts=now,
                executed=False,
                outcome_type="NO_ACTION",
                reason="FAILED_EMPTY_TEXT",
                action_type=action_type,
                text_len=0,
                debug={"p1": dec.to_dict()},
                apply_now=False,
            )

        # 若调用方启用 P2，则不在此执行 SAY，由 main 经 P2 后再执行
        defer_speak = payload.get("_defer_speak_to_p2") is True
        if defer_speak:
            return P1Outcome(
                ts=now,
                executed=False,
                outcome_type="NO_ACTION",
                reason=dec.reason,
                action_type=action_type,
                text_len=len(text),
                debug={"p1": dec.to_dict()},
                apply_now=True,
            )

        # 执行 SAY（无 P2 或未 defer 时）
        try:
            if self.speak_fn is None:
                return P1Outcome(
                    ts=now,
                    executed=False,
                    outcome_type="NO_ACTION",
                    reason="FAILED_NO_SPEAK_FN",
                    action_type=action_type,
                    text_len=len(text),
                    debug={"p1": dec.to_dict()},
                    apply_now=False,
                )

            self.speak_fn(text)
            self.last_say_ts = now

            return P1Outcome(
                ts=now,
                executed=True,
                outcome_type="ACTION_EXECUTED",
                reason="SAY_OK",
                action_type=action_type,
                text_len=len(text),
                debug={"p1": dec.to_dict()},
                apply_now=True,
            )

        except Exception as e:
            return P1Outcome(
                ts=now,
                executed=False,
                outcome_type="NO_ACTION",
                reason="FAILED_EXCEPTION",
                action_type=action_type,
                text_len=len(text),
                debug={"p1": dec.to_dict(), "exc": repr(e)},
                apply_now=False,
            )
