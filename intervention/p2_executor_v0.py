# intervention/p2_executor_v0.py
"""
P2 v0 执行器：内容价值过滤。
仅在 P1.apply_now=True 时调用；不执行 SAY，只决定是否允许继续。
"""
from dataclasses import dataclass
from typing import Dict, Any, Optional
import time

from intervention.p2_policy_v0 import (
    P2Config,
    P2Decision,
    RecentTextCache,
    decide_p2_allow,
)


@dataclass
class P2Outcome:
    ts: float
    allowed: bool
    outcome_type: str          # PASS / NO_ACTION
    reason: str                # OK_CONTENT / BLOCKED_LOW_VALUE
    debug: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ts": self.ts,
            "allowed": self.allowed,
            "outcome_type": self.outcome_type,
            "reason": self.reason,
            "debug": self.debug,
        }


class P2Executor:
    """
    P2：内容价值过滤
    - 仅在 P1.apply_now=True 时调用
    - 不执行 SAY，只决定是否允许继续
    """

    def __init__(self, cfg: Optional[P2Config] = None):
        self.cfg = cfg or P2Config()
        self.recent_cache = RecentTextCache()

    def evaluate(
        self,
        *,
        text: str,
        now_ts: Optional[float] = None,
    ) -> P2Outcome:
        now = now_ts or time.time()

        dec: P2Decision = decide_p2_allow(
            cfg=self.cfg,
            now_ts=now,
            text=text,
            recent_cache=self.recent_cache,
        )

        if not dec.allow:
            return P2Outcome(
                ts=now,
                allowed=False,
                outcome_type="NO_ACTION",
                reason=dec.reason,
                debug={"p2": dec.to_dict()},
            )

        # 通过：将本次文本 hash 记入去重缓存（避免重复计算，使用 policy 返回的 text_hash）
        if dec.text_hash is not None:
            self.recent_cache.add(now, dec.text_hash)
        return P2Outcome(
            ts=now,
            allowed=True,
            outcome_type="PASS",
            reason=dec.reason,
            debug={"p2": dec.to_dict()},
        )
