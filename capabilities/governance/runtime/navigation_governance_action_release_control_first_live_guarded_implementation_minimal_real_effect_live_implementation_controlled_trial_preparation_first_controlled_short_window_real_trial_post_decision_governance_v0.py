"""
Phase-Next-168

First Controlled Short-Window Real Trial
Post-Decision Governance Runtime v0

Hard boundaries (must hold):
- Non-default explicit entry only (explicit_governance_entry_intent_v0 must be True).
- Entry requires: decision_completed + decision_legality_seen + closed_safe_state_preserved + audit trace + evidence available + default path disabled.
- Read-only governance: no real side effects; must not open any release window; must not trigger retry/reopen/execute/long-running.
- Outcomes restricted to Phase-Next-167 allowlist; forbidden outcomes must be blocked.
- Final state must preserve closed-safe; allows_next_runtime_now must be False.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Mapping, Optional


ALLOWED_GOVERNANCE_OUTCOMES_V0 = {
    "remain_closed_safe",
    "escalate_for_new_governance_definition",
    "require_new_evidence_before_any_further_governance",
    "allow_next_governance_preparation_under_same_guardrails",
    "block_further_real_action_until_manual_override",
}

FORBIDDEN_GOVERNANCE_SIGNALS_V0 = {
    # Explicit forbidden outcomes (Phase-Next-167).
    "implicit_reopen",
    "implicit_retry_runtime",
    "implicit_widening",
    "implicit_full_trial_continuation",
    "implicit_default_on_transition",
    "implicit_long_running_enablement",
    # Broader probes we must treat as forbidden intent signals.
    "open_release_window",
    "trigger_execute",
    "trigger_retry",
    "trigger_reopen",
    "enable_default_path",
    "enable_long_running",
}


@dataclass(frozen=True)
class PostDecisionGovernanceInputV0:
    """
    Minimal, read-only governance input bundle.

    This intentionally does NOT depend on internal classes. It accepts the upstream
    post-execute decision result/evidence as a mapping and reads only a small,
    auditable subset of keys.
    """

    post_execute_decision_bundle: Mapping[str, Any]
    explicit_governance_entry_intent_v0: bool
    default_path_enabled: bool = False


def _bool(m: Mapping[str, Any], key: str, default: bool = False) -> bool:
    v = m.get(key, default)
    return bool(v)


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


def run_post_decision_governance_v0(inp: PostDecisionGovernanceInputV0) -> Dict[str, Any]:
    """
    Execute post-decision governance (read-only).

    Returns a structured dict with required visibility fields (Phase-Next-168).
    """

    bundle = inp.post_execute_decision_bundle

    # Layer A: Non-default explicit entry.
    explicit_entry_seen = bool(inp.explicit_governance_entry_intent_v0)

    # Layer A: entry prerequisite signals (read-only).
    decision_completed_seen = _bool(bundle, "decision_completed", False)
    decision_legality_seen = _bool(bundle, "decision_legality_seen", False) or _bool(
        bundle, "decision_legal_complete", False
    )
    closed_safe_state_seen = _bool(bundle, "closed_safe_state_preserved", False) or _bool(
        bundle, "closed_safe_state_seen", False
    )
    evidence_complete_seen = _bool(bundle, "evidence_complete", False) or _bool(
        bundle, "evidence_complete_seen", False
    )
    audit_trace_intact_seen = _bool(bundle, "audit_trace_intact", False) or _bool(
        bundle, "audit_trace_intact_seen", False
    )
    post_execute_pack_recommendation = _get_str(bundle, "post_execute_decision_go_no_go_pack_v0")
    post_execute_pack_ok = post_execute_pack_recommendation in {"go", "conditional_go"}

    default_path_still_disabled = not bool(inp.default_path_enabled)

    # Layer B: boundary violation / probe detection.
    boundary_violation_seen = _bool(bundle, "boundary_violation_seen", False) or _bool(
        bundle, "boundary_violation", False
    )
    structural_risk_seen = _bool(bundle, "structural_risk_seen", False) or _bool(
        bundle, "default_on_risk_seen", False
    )
    widening_needed_seen = _bool(bundle, "widening_needed", False) or _bool(
        bundle, "requires_new_governance_definition", False
    )

    forbidden_probes = set()
    for s in _list(bundle, "forbidden_signals") + _list(bundle, "forbidden_probes"):
        forbidden_probes.add(str(s))
    for s in _list(bundle, "forbidden_governance_signals"):
        forbidden_probes.add(str(s))

    forbidden_governance_outcome_blocked = False
    if forbidden_probes.intersection(FORBIDDEN_GOVERNANCE_SIGNALS_V0):
        forbidden_governance_outcome_blocked = True

    # Layer A gate: if cannot enter, must remain closed-safe / block / require evidence.
    illegal_state_detected = False
    can_enter = (
        explicit_entry_seen
        and decision_completed_seen
        and decision_legality_seen
        and closed_safe_state_seen
        and default_path_still_disabled
        and post_execute_pack_ok
    )

    # Determine outcome with conservative precedence (safe-first).
    allowed_governance_outcome_selected = "remain_closed_safe"
    human_confirmation_required = False
    requires_new_governance_definition = False

    if not explicit_entry_seen:
        illegal_state_detected = True
        allowed_governance_outcome_selected = "remain_closed_safe"
    elif not default_path_still_disabled:
        illegal_state_detected = True
        allowed_governance_outcome_selected = "block_further_real_action_until_manual_override"
        human_confirmation_required = True
        requires_new_governance_definition = True
    elif not decision_completed_seen or not decision_legality_seen or not post_execute_pack_ok:
        # No legal decision completion => must not proceed.
        illegal_state_detected = True
        allowed_governance_outcome_selected = "remain_closed_safe"
    elif not closed_safe_state_seen:
        illegal_state_detected = True
        allowed_governance_outcome_selected = "block_further_real_action_until_manual_override"
        human_confirmation_required = True
        requires_new_governance_definition = True
    elif forbidden_governance_outcome_blocked:
        illegal_state_detected = True
        allowed_governance_outcome_selected = "block_further_real_action_until_manual_override"
        human_confirmation_required = True
        requires_new_governance_definition = True
    elif boundary_violation_seen or structural_risk_seen:
        allowed_governance_outcome_selected = "block_further_real_action_until_manual_override"
        human_confirmation_required = True
        requires_new_governance_definition = True
    elif not audit_trace_intact_seen or not evidence_complete_seen:
        # Evidence incomplete => cannot allow next preparation.
        allowed_governance_outcome_selected = "require_new_evidence_before_any_further_governance"
        human_confirmation_required = True
    elif widening_needed_seen:
        allowed_governance_outcome_selected = "escalate_for_new_governance_definition"
        human_confirmation_required = True
        requires_new_governance_definition = True
    else:
        # Clean governance case: allow next governance preparation (still not runtime).
        allowed_governance_outcome_selected = "allow_next_governance_preparation_under_same_guardrails"
        human_confirmation_required = True

    if allowed_governance_outcome_selected not in ALLOWED_GOVERNANCE_OUTCOMES_V0:
        # Should never happen; treat as illegal and force safe outcome.
        illegal_state_detected = True
        forbidden_governance_outcome_blocked = True
        allowed_governance_outcome_selected = "remain_closed_safe"

    # Layer E: final safety state must remain closed.
    keeps_system_closed = True
    allows_next_runtime_now = False
    closed_safe_state_preserved = True  # This runtime must not alter state; preserve by contract.

    governance_completed = True

    return {
        "explicit_governance_entry_seen": explicit_entry_seen,
        "decision_completed_seen": decision_completed_seen,
        "decision_legality_seen": decision_legality_seen,
        "closed_safe_state_seen": closed_safe_state_seen,
        "evidence_complete_seen": evidence_complete_seen,
        "audit_trace_intact_seen": audit_trace_intact_seen,
        "boundary_violation_seen": boundary_violation_seen or structural_risk_seen,
        "allowed_governance_outcome_selected": allowed_governance_outcome_selected,
        "forbidden_governance_outcome_blocked": forbidden_governance_outcome_blocked,
        "human_confirmation_required": human_confirmation_required,
        "requires_new_governance_definition": requires_new_governance_definition,
        "keeps_system_closed": keeps_system_closed,
        "allows_next_runtime_now": allows_next_runtime_now,
        "closed_safe_state_preserved": closed_safe_state_preserved,
        "illegal_state_detected": illegal_state_detected or (not can_enter),
        "governance_completed": governance_completed,
        "inputs_summary": {
            "default_path_enabled": bool(inp.default_path_enabled),
            "post_execute_pack_recommendation": post_execute_pack_recommendation,
            "forbidden_probes_seen": sorted(forbidden_probes),
        },
    }

