from typing import Literal

from .ability_matrix import AuthorityLevel


BCAction = Literal["FORCE_STOP", "HOLD", "EXECUTE", "FALLBACK", "REQUEST_TAKEOVER"]


def resolve_bc_action(authority: AuthorityLevel, c_decision: str) -> BCAction:
    decision = str(c_decision).upper()
    if decision == "STOP":
        return "FORCE_STOP"
    if decision == "REQUEST_TAKEOVER":
        return "REQUEST_TAKEOVER"
    if decision == "HOLD":
        if authority in {AuthorityLevel.A4, AuthorityLevel.A5}:
            return "FALLBACK"
        return "HOLD"

    # NONE or no instinct trigger
    if authority in {AuthorityLevel.A4, AuthorityLevel.A5}:
        return "FALLBACK"
    return "EXECUTE"


def can_execute_b_candidates(authority: AuthorityLevel, c_decision: str) -> bool:
    return resolve_bc_action(authority, c_decision) == "EXECUTE"
