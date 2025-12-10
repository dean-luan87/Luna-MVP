from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class OnExceedAction(str, Enum):
    """
    What to do when retry_limit is exceeded.

    - ABORT: stop the current task chain.
    - FALLBACK: hand over to a fallback handler (e.g. human_assist).
    - CLARIFY: switch to a clarification chain.
    - ASK_RESTART: restart the whole ask sequence (for future adaptive behavior).
    """

    ABORT = "abort"
    FALLBACK = "fallback"
    CLARIFY = "clarify"
    ASK_RESTART = "ask_restart"


@dataclass(frozen=True)
class RetryPolicy:
    """
    Retry policy for ask/clarify chains.

    interval:
        Time (in seconds) between two retries. Used by higher-level scheduling
        to decide when to trigger the next ask.

    limit:
        Maximum number of retries. When exceeded, `on_exceed` is used.

    on_exceed:
        Strategy when the retry limit is exceeded.

    adaptive:
        Whether this policy can be adjusted dynamically (emotion / context / LLM).
        1.4.6a: not used yet, but we keep it to preserve the contract.

    ai_adjust_hook:
        A symbolic hook name, indicating how adaptive logic will adjust this policy
        in the future, e.g. "emotion", "context", "llm".
    """

    interval: float = 5.0
    limit: int = 3
    on_exceed: OnExceedAction = OnExceedAction.ABORT

    adaptive: bool = False
    ai_adjust_hook: Optional[str] = None

    @classmethod
    def default(cls) -> "RetryPolicy":
        """Default global retry policy for ask chains."""
        return cls(
            interval=5.0,
            limit=3,
            on_exceed=OnExceedAction.ABORT,
            adaptive=False,
            ai_adjust_hook=None,
        )

    def with_overrides(
        self,
        *,
        interval: Optional[float] = None,
        limit: Optional[int] = None,
        on_exceed: Optional[OnExceedAction] = None,
        adaptive: Optional[bool] = None,
        ai_adjust_hook: Optional[str] = None,
    ) -> "RetryPolicy":
        """
        Return a new RetryPolicy with some fields overridden.
        Useful for task-level customisation on top of a global default.
        """
        return RetryPolicy(
            interval=self.interval if interval is None else interval,
            limit=self.limit if limit is None else limit,
            on_exceed=self.on_exceed if on_exceed is None else on_exceed,
            adaptive=self.adaptive if adaptive is None else adaptive,
            ai_adjust_hook=self.ai_adjust_hook if ai_adjust_hook is None else ai_adjust_hook,
        )

