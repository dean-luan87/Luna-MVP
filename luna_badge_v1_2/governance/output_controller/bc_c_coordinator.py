from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Optional

from .ability_matrix import AuthorityLevel

C_STOP = "STOP"
C_HOLD = "HOLD"
C_REQUEST_TAKEOVER = "REQUEST_TAKEOVER"
C_NONE = "NONE"


class BCAction(str, Enum):
    FORCE_STOP = "FORCE_STOP"
    HOLD = "HOLD"
    EXECUTE = "EXECUTE"
    FALLBACK = "FALLBACK"
    REQUEST_TAKEOVER = "REQUEST_TAKEOVER"


@dataclass(frozen=True)
class CoopDecision:
    c_decision: str
    authority: AuthorityLevel
    bc_action: BCAction
    allow_execute_b: bool
    allow_output: bool
    can_recover: bool
    note: str = ""


def normalize_c_decision(c_decision: Optional[Dict[str, Any]] | Optional[str]) -> str:
    if c_decision is None:
        return C_NONE
    if isinstance(c_decision, str):
        return c_decision
    if isinstance(c_decision, dict):
        decision = c_decision.get("decision")
        return decision if isinstance(decision, str) else C_NONE
    return C_NONE


def decide_bc_c_cooperation(
    *,
    authority: AuthorityLevel,
    c_decision: Optional[Dict[str, Any]] | Optional[str],
) -> CoopDecision:
    c = normalize_c_decision(c_decision).upper()

    if c == C_STOP:
        return CoopDecision(
            c_decision=C_STOP,
            authority=authority,
            bc_action=BCAction.FORCE_STOP,
            allow_execute_b=False,
            allow_output=False,
            can_recover=False,
            note="C_STOP: force stop",
        )

    if c == C_REQUEST_TAKEOVER:
        return CoopDecision(
            c_decision=C_REQUEST_TAKEOVER,
            authority=authority,
            bc_action=BCAction.REQUEST_TAKEOVER,
            allow_execute_b=False,
            allow_output=False,
            can_recover=False,
            note="C_REQUEST_TAKEOVER: clear outputs",
        )

    if c == C_HOLD:
        if authority in (AuthorityLevel.A4, AuthorityLevel.A5):
            return CoopDecision(
                c_decision=C_HOLD,
                authority=authority,
                bc_action=BCAction.FALLBACK,
                allow_execute_b=False,
                allow_output=False,
                can_recover=False,
                note="C_HOLD + A4/A5: fallback",
            )
        return CoopDecision(
            c_decision=C_HOLD,
            authority=authority,
            bc_action=BCAction.HOLD,
            allow_execute_b=False,
            allow_output=False,
            can_recover=True,
            note="C_HOLD + A1-A3: hold",
        )

    if authority in (AuthorityLevel.A4, AuthorityLevel.A5):
        return CoopDecision(
            c_decision=C_NONE,
            authority=authority,
            bc_action=BCAction.FALLBACK,
            allow_execute_b=False,
            allow_output=False,
            can_recover=False,
            note="C_NONE + A4/A5: fallback",
        )

    return CoopDecision(
        c_decision=C_NONE,
        authority=authority,
        bc_action=BCAction.EXECUTE,
        allow_execute_b=True,
        allow_output=True,
        can_recover=True,
        note="C_NONE + A1-A3: execute B",
    )
