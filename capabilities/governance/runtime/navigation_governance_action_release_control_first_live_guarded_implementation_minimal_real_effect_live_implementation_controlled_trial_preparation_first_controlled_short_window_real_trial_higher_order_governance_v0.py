"""
Phase-Next-172

First Controlled Short-Window Real Trial
Higher-Order Governance Runtime v0

Hard boundaries (must hold):
- Non-default explicit entry only (explicit_higher_order_governance_entry_intent_v0 must be True).
- Entry requires: lower-order governance completed + legality seen + closed-safe preserved + audit trace + evidence available + default path disabled.
- Read-only governance: no real side effects; must not open any release window; must not trigger retry/reopen/execute/long-running.
- Outcomes restricted to Phase-Next-171 allowlist; forbidden outcomes must be blocked.
- Final state must preserve closed-safe; allows_next_runtime_now must be False.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Mapping, Optional


ALLOWED_HIGHER_ORDER_GOVERNANCE_OUTCOMES_V0 = {
    "remain_closed_safe",
    "require_new_evidence_before_any_further_governance",
    "escalate_for_new_governance_definition",
    "allow_next_governance_preparation_under_same_guardrails",
    "block_further_real_action_until_manual_override",
}

FORBIDDEN_HIGHER_ORDER_GOVERNANCE_SIGNALS_V0 = {
    "implicit_reopen",
    "implicit_retry_runtime",
    "implicit_widening",
    "implicit_full_trial_continuation",
    "implicit_default_on_transition",
    "implicit_long_running_enablement",
    "open_release_window",
    "trigger_execute",
    "trigger_retry",
    "trigger_reopen",
    "enable_default_path",
    "enable_long_running",
}


@dataclass(frozen=True)
class HigherOrderGovernanceInputV0:
    """
    Minimal, read-only higher-order governance input bundle.

    Accepts the lower-order governance result/evidence as a mapping and reads only a
    small, auditable subset of keys.
    """

    lower_order_governance_bundle: Mapping[str, Any]
    explicit_higher_order_governance_entry_intent_v0: bool
    default_path_enabled: bool = False


def _bool(m: Mapping[str, Any], key: str, default: bool = False) -> bool:
    return bool(m.get(key, default))


def _get_str(m: Mapping[str, Any], key: str) -> Optional[str]:
    v = m.get(key)
    if v is None:
        return None
    return str(v)


def _list(m: Mapping[str, Any], key: str) -> list:
    v = m.get(key)
    if v is None:
        return []
    if isinstance(v, list):
        return v
    return [v]


def run_higher_order_governance_v0(inp: HigherOrderGovernanceInputV0) -> Dict[str, Any]:
    """
    Execute higher-order governance (read-only).

    Returns a structured dict with required visibility fields (Phase-Next-172).
    """

    b = inp.lower_order_governance_bundle

    # Layer A: Non-default explicit entry.
    explicit_entry_seen = bool(inp.explicit_higher_order_governance_entry_intent_v0)

    # Lower-order completion & legality (minimal assumptions; tolerate key variants).
    lower_completed_seen = _bool(b, "governance_completed", False) or _bool(b, "lower_order_governance_completed", False)
    lower_legality_seen = _bool(b, "governance_legality_seen", False) or _bool(
        b, "lower_order_governance_legality_seen", False
    ) or _bool(b, "lower_order_governance_previously_legal", False)

    closed_safe_state_seen = _bool(b, "closed_safe_state_preserved", False) or _bool(b, "closed_safe_state_seen", False)
    evidence_complete_seen = _bool(b, "evidence_complete", False) or _bool(b, "evidence_complete_seen", False)
    audit_trace_intact_seen = _bool(b, "audit_trace_intact", False) or _bool(b, "audit_trace_intact_seen", False)

    # Optional pack prerequisite signal (170 pack result).
    post_decision_pack_recommendation = _get_str(b, "post_decision_governance_go_no_go_pack_v0")
    pack_ok = post_decision_pack_recommendation in {"go", "conditional_go"}

    default_path_still_disabled = not bool(inp.default_path_enabled)

    # Layer B: boundary violation / probe detection.
    boundary_violation_seen = _bool(b, "boundary_violation_seen", False) or _bool(b, "boundary_violation", False)
    structural_risk_seen = _bool(b, "structural_risk_seen", False) or _bool(b, "default_on_risk_seen", False)
    widening_needed_seen = _bool(b, "widening_needed", False) or _bool(b, "requires_new_governance_definition", False)

    forbidden_probes = set()
    for s in _list(b, "forbidden_signals") + _list(b, "forbidden_probes") + _list(b, "forbidden_higher_order_governance_signals"):
        forbidden_probes.add(str(s))

    forbidden_blocked = bool(forbidden_probes.intersection(FORBIDDEN_HIGHER_ORDER_GOVERNANCE_SIGNALS_V0))

    illegal_state_detected = False

    can_enter = (
        explicit_entry_seen
        and lower_completed_seen
        and lower_legality_seen
        and closed_safe_state_seen
        and default_path_still_disabled
        and pack_ok
    )

    allowed_outcome = "remain_closed_safe"
    human_confirmation_required = False
    requires_new_governance_definition = False

    # Conservative precedence (safe-first).
    if not explicit_entry_seen:
        illegal_state_detected = True
        allowed_outcome = "remain_closed_safe"
    elif not default_path_still_disabled:
        illegal_state_detected = True
        allowed_outcome = "block_further_real_action_until_manual_override"
        human_confirmation_required = True
        requires_new_governance_definition = True
    elif not lower_completed_seen or not lower_legality_seen or not pack_ok:
        illegal_state_detected = True
        allowed_outcome = "remain_closed_safe"
    elif not closed_safe_state_seen:
        illegal_state_detected = True
        allowed_outcome = "block_further_real_action_until_manual_override"
        human_confirmation_required = True
        requires_new_governance_definition = True
    elif forbidden_blocked:
        illegal_state_detected = True
        allowed_outcome = "block_further_real_action_until_manual_override"
        human_confirmation_required = True
        requires_new_governance_definition = True
    elif boundary_violation_seen or structural_risk_seen:
        allowed_outcome = "block_further_real_action_until_manual_override"
        human_confirmation_required = True
        requires_new_governance_definition = True
    elif not audit_trace_intact_seen or not evidence_complete_seen:
        allowed_outcome = "require_new_evidence_before_any_further_governance"
        human_confirmation_required = True
    elif widening_needed_seen:
        allowed_outcome = "escalate_for_new_governance_definition"
        human_confirmation_required = True
        requires_new_governance_definition = True
    else:
        allowed_outcome = "allow_next_governance_preparation_under_same_guardrails"
        human_confirmation_required = True

    if allowed_outcome not in ALLOWED_HIGHER_ORDER_GOVERNANCE_OUTCOMES_V0:
        illegal_state_detected = True
        forbidden_blocked = True
        allowed_outcome = "remain_closed_safe"

    keeps_system_closed = True
    allows_next_runtime_now = False
    closed_safe_state_preserved = True
    governance_completed = True

    return {
        "explicit_higher_order_governance_entry_seen": explicit_entry_seen,
        "lower_order_governance_completed_seen": lower_completed_seen,
        "lower_order_governance_legality_seen": lower_legality_seen,
        "closed_safe_state_seen": closed_safe_state_seen,
        "evidence_complete_seen": evidence_complete_seen,
        "audit_trace_intact_seen": audit_trace_intact_seen,
        "boundary_violation_seen": boundary_violation_seen or structural_risk_seen,
        "allowed_higher_order_governance_outcome_selected": allowed_outcome,
        "forbidden_higher_order_governance_outcome_blocked": forbidden_blocked,
        "human_confirmation_required": human_confirmation_required,
        "requires_new_governance_definition": requires_new_governance_definition,
        "keeps_system_closed": keeps_system_closed,
        "allows_next_runtime_now": allows_next_runtime_now,
        "closed_safe_state_preserved": closed_safe_state_preserved,
        "illegal_state_detected": illegal_state_detected or (not can_enter),
        "governance_completed": governance_completed,
        "inputs_summary": {
            "default_path_enabled": bool(inp.default_path_enabled),
            "post_decision_pack_recommendation": post_decision_pack_recommendation,
            "forbidden_probes_seen": sorted(forbidden_probes),
        },
    }

