from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from .retry_policy import RetryPolicy, OnExceedAction


@dataclass
class AskSessionState:
    """
    Runtime state for a single ask session.

    We intentionally keep this structure small and serialisable.

    slot_id:
        Logical identifier for what we are asking for, e.g. "destination".
        This is used mainly for logging / debugging.

    retry_count:
        How many retries have already been attempted.

    next_retry_at:
        A logical timestamp (float, seconds) at or after which the next retry
        may be triggered. It is up to the caller to choose the time source
        (e.g. time.monotonic()).

    exceeded:
        True if the retry limit defined by the policy has been exceeded.

    policy:
        The effective retry policy for this session.
    """

    slot_id: str
    retry_count: int = 0
    next_retry_at: float = 0.0
    exceeded: bool = False
    policy: RetryPolicy = field(default_factory=RetryPolicy.default)

    # Optional bag for additional metadata (future use).
    meta: Dict[str, Any] = field(default_factory=dict)


class AskManager:
    """
    Central manager to handle retry logic for ask/clarify flows.

    Responsibilities in 1.4.6a:
    - Provide a default RetryPolicy.
    - Resolve per-task RetryPolicy overrides.
    - Track retry_count / next_retry_at / exceeded for each AskSessionState.
    - Decide when a retry is allowed and when on_exceed should be triggered.

    Higher-level components (AskChain, ClarifyChain, DecisionCore) will:
    - Call `should_retry_now(...)` to decide if a re-ask should be sent.
    - Call `register_retry(...)` when a retry is actually performed.
    - Check `session.exceeded` and `policy.on_exceed` to route control flow.
    """

    def __init__(self, default_policy: Optional[RetryPolicy] = None) -> None:
        self._default_policy = default_policy or RetryPolicy.default()

    @property
    def default_policy(self) -> RetryPolicy:
        return self._default_policy

    def resolve_policy_for_task(
        self,
        task_meta: Optional[Dict[str, Any]] = None,
    ) -> RetryPolicy:
        """
        Resolve the effective RetryPolicy for a given task / ask-schema.

        `task_meta` is expected to be a dict that may contain a `retry_policy`
        sub-dict in the future, e.g.:

            {
                "retry_policy": {
                    "interval": 4,
                    "limit": 2,
                    "on_exceed": "clarify",
                    "adaptive": True,
                    "ai_adjust_hook": "emotion",
                }
            }

        1.4.6a:
            - We support a simple dict with these keys.
            - We do not yet integrate with concrete TaskDefinition classes.
        """
        if not task_meta:
            return self._default_policy

        raw = task_meta.get("retry_policy")
        if not raw:
            return self._default_policy

        # Start from default and override known fields.
        policy = self._default_policy
        interval = raw.get("interval")
        limit = raw.get("limit")
        on_exceed_raw = raw.get("on_exceed")
        adaptive = raw.get("adaptive")
        ai_adjust_hook = raw.get("ai_adjust_hook")

        on_exceed = None
        if on_exceed_raw is not None:
            try:
                on_exceed = OnExceedAction(on_exceed_raw)
            except ValueError:
                # Unknown value, fall back to default.
                on_exceed = None

        return policy.with_overrides(
            interval=interval,
            limit=limit,
            on_exceed=on_exceed,
            adaptive=adaptive,
            ai_adjust_hook=ai_adjust_hook,
        )

    def create_session(
        self,
        slot_id: str,
        *,
        policy: Optional[RetryPolicy] = None,
        now: float = 0.0,
    ) -> AskSessionState:
        """
        Create a new ask-session state for a given slot.

        `now` is a logical timestamp (seconds), used to set the initial
        `next_retry_at`. Callers are free to decide the time source.
        """
        effective_policy = policy or self._default_policy
        return AskSessionState(
            slot_id=slot_id,
            retry_count=0,
            next_retry_at=now,
            exceeded=False,
            policy=effective_policy,
        )

    def should_retry_now(self, session: AskSessionState, *, now: float) -> bool:
        """
        Decide whether we are allowed to trigger a new retry at `now`.

        - Returns False if the session has already exceeded its limit.
        - Returns False if `now < next_retry_at`.
        - Otherwise returns True.
        """
        if session.exceeded:
            return False
        return now >= session.next_retry_at

    def register_retry(self, session: AskSessionState, *, now: float) -> None:
        """
        Record that we have actually performed a retry at `now`.

        - Increments retry_count.
        - Updates next_retry_at based on policy.interval.
        - Marks exceeded flag when retry_count > limit.
        """
        if session.exceeded:
            return

        session.retry_count += 1
        session.next_retry_at = now + session.policy.interval

        if session.retry_count > session.policy.limit:
            session.exceeded = True

    def reset_session(self, session: AskSessionState, *, now: float = 0.0) -> None:
        """
        Reset retry state (e.g. when user has answered sufficiently
        and we want to reuse the same session object for another slot).
        """
        session.retry_count = 0
        session.exceeded = False
        session.next_retry_at = now












