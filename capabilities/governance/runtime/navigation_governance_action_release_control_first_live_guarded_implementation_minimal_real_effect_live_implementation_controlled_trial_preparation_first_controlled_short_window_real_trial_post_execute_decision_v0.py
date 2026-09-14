# -*- coding: utf-8 -*-
"""
Navigation Governance Action — Release Control First Live Guarded Implementation
Minimal Real-Effect Live Implementation Controlled Trial Preparation
First Controlled Short-Window REAL Trial Post-Execute Decision v0 (READ-ONLY, GUARDED).

定位：
- Phase-Next-164：在 Phase-Next-163 post-execute decision constitution 约束下，实现第一版只读、治理性的 post-execute decision runtime。

硬边界（写死）：
- 非默认路径：显式入口（显式调用 + 显式 decision entry intent）。
- 只读治理性：不得打开新的 real side-effects window；不得触发隐式 retry/reopen/widen/full-trial/default-on。
- 只能在 execute 已合法 final close 后进入（closed=true 且 side_effects_released=false 或等价安全闭合）。
- 只能输出 163 白名单 outcome；任何 forbidden probe 必须被阻断并落为保守 outcome。
- decision 完成后必须保持 closed-safe state。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


_SCOPE = "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_first_controlled_short_window_real_trial_post_execute_decision_v0"

_ALLOWED_OUTCOMES = {
    "remain_closed_safe",
    "retry_allowed_under_same_guardrails",
    "retry_not_allowed_until_new_definition",
    "escalate_for_new_governance_definition",
    "stop_and_block_further_real_action",
}

_FORBIDDEN_OUTCOME_PROBES = {
    "implicit_reopen",
    "implicit_execute_retry",
    "implicit_widening",
    "implicit_full_trial_continuation",
    "implicit_default_on_transition",
}


@dataclass(frozen=True)
class PostExecuteDecisionResult:
    ok: bool
    result_scope: str
    status: str
    reason: str
    payload: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        out: Dict[str, Any] = {
            "ok": bool(self.ok),
            "result_scope": str(self.result_scope),
            "status": str(self.status),
            "reason": str(self.reason),
        }
        if isinstance(self.payload, dict):
            out["payload"] = dict(self.payload)
        return out


def run_first_controlled_short_window_real_trial_post_execute_decision_v0(
    *,
    # Explicit non-default entry (decision intent)
    explicit_post_execute_decision_entry_v0: Any,
    # Evidence bundle: a completed execute result (typically output from Phase-Next-160 runtime)
    execute_result_v0: Any,
    # Optional governance references (read-only pointers; must not be interpreted as “auto proceed”)
    execute_go_no_go_pack_v0: Any = None,  # Phase-Next-162
    post_execute_decision_definition_v0: Any = None,  # Phase-Next-163
    context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    唯一 post-execute decision 入口（显式调用；不接默认路径）。
    - Layer A Entry: explicit decision entry + execute-final-close prerequisite
    - Layer B Input Validation: evidence completeness + audit integrity + boundary violation detection + forbidden probe detection
    - Layer C Outcome Decision: allowed outcomes only (163 allowlist)
    - Layer D Forbidden Blocking: any forbidden probe => blocked + conservative outcome
    - Layer E Final Safety: closed-safe state preserved (no real action)
    """
    ctx = dict(context or {})
    trace: Dict[str, Any] = {"order": [], "notes": [], "blocked": []}

    state: Dict[str, Any] = {
        "explicit_decision_entry_seen": False,
        "execute_closed_seen": False,
        "side_effects_released_false_seen": False,
        "execute_legality_seen": False,
        "evidence_complete_seen": False,
        "boundary_violation_seen": False,
        "allowed_outcome_selected": None,
        "forbidden_outcome_blocked": False,
        "human_confirmation_required": False,
        "requires_new_governance_definition": False,
        "allows_retry_now": False,  # MUST remain False (no auto retry)
        "closed_safe_state_preserved": True,
        "illegal_state_detected": False,
        "decision_completed": False,
        # Optional: reference pointers
        "execute_go_no_go_pack_seen": isinstance(execute_go_no_go_pack_v0, dict),
        "post_execute_definition_seen": post_execute_decision_definition_v0 is not None,
    }

    def _final(status: str, reason: str, outcome: str, *, ok: bool = True) -> Dict[str, Any]:
        if outcome not in _ALLOWED_OUTCOMES:
            state["illegal_state_detected"] = True
            outcome = "remain_closed_safe"
            status = "blocked"
            reason = "illegal_outcome_selected_by_runtime"
        state["allowed_outcome_selected"] = outcome
        state["decision_completed"] = True
        # Hard guarantee: decision must keep system closed-safe.
        state["closed_safe_state_preserved"] = True
        state["allows_retry_now"] = False
        return PostExecuteDecisionResult(
            ok=ok,
            result_scope=_SCOPE,
            status=str(status),
            reason=str(reason),
            payload={"state": state, "trace": trace, "context": ctx},
        ).to_dict()

    # Layer A: explicit entry required.
    trace["order"].append("entry_checked")
    state["explicit_decision_entry_seen"] = isinstance(explicit_post_execute_decision_entry_v0, dict) and bool(
        explicit_post_execute_decision_entry_v0.get("intent") is True
    )
    if not state["explicit_decision_entry_seen"]:
        return _final(
            status="blocked",
            reason="missing_explicit_post_execute_decision_entry_v0",
            outcome="remain_closed_safe",
            ok=False,
        )

    # Extract execute evidence.
    if not isinstance(execute_result_v0, dict):
        return _final(
            status="blocked",
            reason="missing_or_invalid_execute_result_v0",
            outcome="remain_closed_safe",
            ok=False,
        )

    payload = execute_result_v0.get("payload") if isinstance(execute_result_v0.get("payload"), dict) else {}
    exec_state = payload.get("state") if isinstance(payload.get("state"), dict) else {}
    exec_trace = payload.get("trace") if isinstance(payload.get("trace"), dict) else {}

    # Execute legal final close prerequisite.
    trace["order"].append("final_close_prerequisite_checked")
    state["execute_closed_seen"] = bool(exec_state.get("closed") is True)
    state["side_effects_released_false_seen"] = bool(exec_state.get("side_effects_released") is False)
    if not (state["execute_closed_seen"] and state["side_effects_released_false_seen"]):
        return _final(
            status="not_eligible",
            reason="execute_not_legally_final_closed",
            outcome="remain_closed_safe",
            ok=False,
        )

    # Execute legality signal (best-effort): 162 pack seen OR 160/161 fields show no illegal.
    trace["order"].append("execute_legality_checked")
    pack_ok = isinstance(execute_go_no_go_pack_v0, dict) and str(execute_go_no_go_pack_v0.get("overall_evaluation") or "") in {
        "go",
        "conditional_go",
    }
    st_ok = bool(exec_state.get("illegal_state_detected") is False) if "illegal_state_detected" in exec_state else True
    state["execute_legality_seen"] = bool(pack_ok or st_ok)

    # Evidence completeness (minimal).
    trace["order"].append("evidence_completeness_checked")
    order = exec_trace.get("order") if isinstance(exec_trace.get("order"), list) else []
    has_reason = bool(execute_result_v0.get("reason"))
    has_status = bool(execute_result_v0.get("status"))
    state["evidence_complete_seen"] = bool(isinstance(order, list) and len(order) > 0 and has_reason and has_status)
    if not state["evidence_complete_seen"]:
        return _final(
            status="decided",
            reason="evidence_incomplete_or_audit_broken",
            outcome="remain_closed_safe",
            ok=True,
        )

    # Boundary violation check (conservative): if any abort/stop trigger indicates guardrail breach.
    trace["order"].append("boundary_violation_checked")
    abort_id = exec_state.get("abort_trigger_id") or exec_state.get("stop_trigger_id")
    boundary_violation_ids = {
        "no_start_event_but_started",
        "no_started_but_release",
        "closure_missing",
        "se_not_recovered",
        "unauthorized_side_effect_surface",
        "execute_window_timeout",
        "execute_attempts_exceeded",
        "audit_trace_missing_or_broken",
        "execute_without_explicit_approval",
        "execute_without_readiness_go",
        "execute_without_explicit_intent",
    }
    if abort_id is not None and str(abort_id) in boundary_violation_ids:
        state["boundary_violation_seen"] = True

    # Forbidden outcome probes must be blocked.
    trace["order"].append("forbidden_outcome_probe_checked")
    requested_outcome = explicit_post_execute_decision_entry_v0.get("requested_outcome")
    requested_probe = explicit_post_execute_decision_entry_v0.get("requested_forbidden_outcome_probe")
    if str(requested_probe or "") in _FORBIDDEN_OUTCOME_PROBES:
        state["forbidden_outcome_blocked"] = True
        trace["blocked"].append({"type": "forbidden_outcome_probe", "id": str(requested_probe)})
        return _final(
            status="blocked",
            reason="forbidden_outcome_probe_blocked",
            outcome="remain_closed_safe",
            ok=False,
        )

    # If requested_outcome is provided but not allowed, block.
    if requested_outcome is not None and str(requested_outcome) not in _ALLOWED_OUTCOMES:
        state["forbidden_outcome_blocked"] = True
        trace["blocked"].append({"type": "non_allowlisted_outcome_requested", "id": str(requested_outcome)})
        return _final(
            status="blocked",
            reason="non_allowlisted_outcome_requested",
            outcome="remain_closed_safe",
            ok=False,
        )

    # Structural safety issue.
    trace["order"].append("structural_safety_checked")
    if explicit_post_execute_decision_entry_v0.get("structural_safety_issue") is True:
        state["requires_new_governance_definition"] = True
        state["human_confirmation_required"] = True
        return _final(
            status="decided",
            reason="structural_safety_issue_detected",
            outcome="stop_and_block_further_real_action",
            ok=True,
        )

    # Widening needed: must escalate.
    trace["order"].append("widening_needed_checked")
    if explicit_post_execute_decision_entry_v0.get("widening_needed") is True:
        state["requires_new_governance_definition"] = True
        state["human_confirmation_required"] = True
        return _final(
            status="decided",
            reason="widening_needed_requires_new_governance_definition",
            outcome="escalate_for_new_governance_definition",
            ok=True,
        )

    # If boundary violations were seen, retry under same guardrails is not allowed.
    if state["boundary_violation_seen"] is True or state["execute_legality_seen"] is False:
        state["requires_new_governance_definition"] = True
        state["human_confirmation_required"] = True
        return _final(
            status="decided",
            reason="boundary_violation_or_legality_uncertain",
            outcome="retry_not_allowed_until_new_definition",
            ok=True,
        )

    # Clean case: allow retry under same guardrails (governance-only, no auto retry).
    state["human_confirmation_required"] = True
    state["requires_new_governance_definition"] = False
    return _final(
        status="decided",
        reason="clean_post_execute_evidence_allows_retry_under_same_guardrails_but_keeps_closed",
        outcome="retry_allowed_under_same_guardrails",
        ok=True,
    )

