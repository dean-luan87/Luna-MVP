# intervention/p3_executor_v0.py
"""
P3 v0 执行器：节律闸门。
仅在 P2 通过后调用；不执行 SAY，只决定当前是否为合适说话时机。
"""
from dataclasses import dataclass
from typing import Dict, Any, Optional
import time

from intervention.p3_policy_v0 import (
    P3Config,
    P3Decision,
    P3State,
    decide_p3_allow,
)


@dataclass
class P3Outcome:
    ts: float
    allowed: bool
    outcome_type: str        # PASS / NO_ACTION
    reason: str
    debug: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ts": self.ts,
            "allowed": self.allowed,
            "outcome_type": self.outcome_type,
            "reason": self.reason,
            "debug": self.debug,
        }


class P3Executor:
    def __init__(self, cfg: Optional[P3Config] = None):
        self.cfg = cfg or P3Config()
        self.state = P3State()

    def evaluate(
        self,
        *,
        rhythm_state: str,
        now_ts: Optional[float] = None,
    ) -> P3Outcome:
        now = now_ts or time.time()

        dec: P3Decision = decide_p3_allow(
            cfg=self.cfg,
            state=self.state,
            now_ts=now,
            rhythm_state=rhythm_state,
        )

        if not dec.allow:
            return P3Outcome(
                ts=now,
                allowed=False,
                outcome_type="NO_ACTION",
                reason=dec.reason,
                debug={"p3": dec.to_dict()},
            )

        return P3Outcome(
            ts=now,
            allowed=True,
            outcome_type="PASS",
            reason=dec.reason,
            debug={"p3": dec.to_dict()},
        )

    def mark_say_executed(self, ts: Optional[float] = None):
        self.state.last_say_ts = ts or time.time()
