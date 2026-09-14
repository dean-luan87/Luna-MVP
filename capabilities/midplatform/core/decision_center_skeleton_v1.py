# -*- coding: utf-8 -*-
"""Decision Center skeleton v1 — pure functions only, candidate generators."""

from __future__ import annotations

from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

from capabilities.midplatform.core.decision_center_types_v1 import (
    DecisionBlockCandidate,
    DecisionCandidate,
    DecisionExplanationCandidate,
    DecisionReadiness,
    DecisionReadinessCandidate,
    DecisionState,
    DownstreamDecisionHandoffCandidate,
)
from capabilities.midplatform.core.information_integration_types_v1 import (
    ConflictCandidate,
    DecisionContextCandidate,
    GapCandidate,
)
from capabilities.midplatform.core.micro_os_common_types_v1 import ValidationResult
from capabilities.midplatform.core.micro_os_static_validators_v1 import (
    validate_candidate_not_fact,
    validate_governance_guard,
)


def _trace_ref(decision_context: DecisionContextCandidate) -> str:
    return decision_context.trace_ref or ""


def _unresolved_conflicts(conflicts: Optional[Sequence[ConflictCandidate]]) -> List[ConflictCandidate]:
    if not conflicts:
        return []
    return [
        c
        for c in conflicts
        if c.decision_readiness != "resolved" or c.requires_confirmation
    ]


def _unresolved_gaps(gaps: Optional[Sequence[GapCandidate]]) -> List[GapCandidate]:
    return list(gaps or ())


def validate_decision_context_input(
    decision_context: DecisionContextCandidate,
    guards: Optional[Mapping[str, Any]] = None,
) -> ValidationResult:
    issues: List[str] = []
    if not decision_context.trace_ref:
        issues.append("missing_trace")
    if not decision_context.candidate_not_fact:
        issues.append("candidate_not_fact_false")
    if decision_context.fact_status != "not_fact":
        issues.append("fact_status_not_candidate")
    if decision_context.high_risk and not decision_context.governance_check_ref:
        issues.append("governance_ref_missing_for_high_risk")
    if guards and guards.get("governance_invalid"):
        issues.append("governance_invalid")
    if guards and guards.get("health_fault"):
        if not decision_context.health_refs:
            issues.append("health_refs_missing")
    blocked = bool(issues)
    return ValidationResult(valid=len(issues) == 0, issues=tuple(issues), blocked=blocked)


def classify_decision_readiness(
    decision_context: DecisionContextCandidate,
    conflicts: Optional[Sequence[ConflictCandidate]] = None,
    gaps: Optional[Sequence[GapCandidate]] = None,
    health_refs: Optional[Sequence[str]] = None,
    governance_ref: Optional[str] = None,
) -> DecisionReadinessCandidate:
    trace = _trace_ref(decision_context)
    blocker_refs: List[str] = []
    obs_refs: List[str] = list(decision_context.required_observation_refs)
    health_review_refs: List[str] = []
    governance_pending = False
    readiness = DecisionReadiness.READY.value
    reason = "decision_context_ready_for_candidate_decision"

    gov = governance_ref or decision_context.governance_check_ref
    if decision_context.high_risk and not gov:
        readiness = DecisionReadiness.BLOCKED.value
        reason = "high_risk_missing_governance_ref"
        governance_pending = True
        blocker_refs.append("governance_pending")
    elif _unresolved_conflicts(conflicts):
        readiness = DecisionReadiness.BLOCKED.value
        reason = "unresolved_conflict_blocks_readiness"
        blocker_refs.extend(c.candidate_id for c in _unresolved_conflicts(conflicts))
    elif health_refs is not None and len(health_refs) == 0:
        readiness = DecisionReadiness.NEEDS_HEALTH_REVIEW.value
        reason = "missing_health_refs"
        health_review_refs.append("health_review_required")
    elif decision_context.health_refs == () and decision_context.readiness_status == "not_ready":
        readiness = DecisionReadiness.NEEDS_HEALTH_REVIEW.value
        reason = "health_fault_or_missing_health"
        health_review_refs.append("health_fault")
    elif _unresolved_gaps(gaps):
        readiness = DecisionReadiness.NEEDS_OBSERVATION.value
        reason = "unresolved_gap_requires_observation"
        obs_refs.extend(
            g.required_observation_candidate_ref
            for g in _unresolved_gaps(gaps)
            if g.required_observation_candidate_ref
        )
    elif decision_context.blocked or decision_context.readiness_status == "not_ready":
        readiness = DecisionReadiness.NOT_READY.value
        reason = "decision_context_not_ready"
    elif decision_context.readiness_status == "hold":
        readiness = DecisionReadiness.NOT_READY.value
        reason = "decision_context_on_hold"

    return DecisionReadinessCandidate(
        candidate_id=f"drc_{decision_context.candidate_id}",
        decision_context_ref=decision_context.candidate_id,
        readiness=readiness,
        readiness_reason=reason,
        blocker_refs=tuple(blocker_refs),
        required_observation_refs=tuple(obs_refs),
        health_review_refs=tuple(health_review_refs),
        governance_pending=governance_pending,
        trace_ref=trace,
        fact_status="not_fact",
        candidate_not_fact=True,
    )


def evaluate_conflict_block_candidate(
    decision_context: DecisionContextCandidate,
    conflicts: Sequence[ConflictCandidate],
) -> Optional[DecisionBlockCandidate]:
    unresolved = _unresolved_conflicts(conflicts)
    if not unresolved:
        return None
    return DecisionBlockCandidate(
        candidate_id=f"dbc_conflict_{decision_context.candidate_id}",
        block_type="unresolved_conflict",
        block_reason="unresolved conflict prevents ready decision_candidate",
        blocked_refs=tuple(c.candidate_id for c in unresolved),
        forbidden_route="decision_candidate_as_final_action",
        recovery_or_hold_candidate="decision_readiness_candidate",
        trace_ref=_trace_ref(decision_context),
        fact_status="not_fact",
        candidate_not_fact=True,
    )


def evaluate_gap_observation_candidate(
    decision_context: DecisionContextCandidate,
    gaps: Sequence[GapCandidate],
) -> Dict[str, Any]:
    unresolved = _unresolved_gaps(gaps)
    if not unresolved:
        return {
            "needs_observation": False,
            "readiness": DecisionReadiness.READY.value,
            "required_observation_handoff_candidate": None,
            "required_observation_refs": (),
        }
    obs_refs = tuple(
        g.required_observation_candidate_ref
        for g in unresolved
        if g.required_observation_candidate_ref
    )
    handoff_id = f"rohc_{decision_context.candidate_id}"
    return {
        "needs_observation": True,
        "readiness": DecisionReadiness.NEEDS_OBSERVATION.value,
        "required_observation_handoff_candidate": handoff_id,
        "required_observation_refs": obs_refs,
        "module_adapter_refs": obs_refs,
        "task_execution": False,
    }


def evaluate_health_review_candidate(
    decision_context: DecisionContextCandidate,
    health_refs: Optional[Sequence[str]] = None,
) -> Dict[str, Any]:
    refs = tuple(health_refs if health_refs is not None else decision_context.health_refs)
    fault = len(refs) == 0 or any("fault" in r for r in refs)
    if not fault:
        return {
            "needs_health_review": False,
            "readiness": DecisionReadiness.READY.value,
            "health_review_candidate": None,
            "recovery_executed": False,
        }
    review_id = f"hrc_{decision_context.candidate_id}"
    return {
        "needs_health_review": True,
        "readiness": DecisionReadiness.NEEDS_HEALTH_REVIEW.value,
        "health_review_candidate": review_id,
        "health_watchdog_handoff_later": True,
        "recovery_executed": False,
    }


def evaluate_governance_pending_candidate(
    decision_context: DecisionContextCandidate,
    governance_ref: Optional[str] = None,
) -> Optional[DecisionBlockCandidate]:
    gov = governance_ref or decision_context.governance_check_ref
    if not decision_context.high_risk or gov:
        return None
    return DecisionBlockCandidate(
        candidate_id=f"dbc_gov_{decision_context.candidate_id}",
        block_type="governance_pending",
        block_reason="high_risk decision missing governance_check_ref",
        blocked_refs=(decision_context.candidate_id,),
        forbidden_route="bypass_governance_gate",
        recovery_or_hold_candidate="governance_pending_candidate",
        trace_ref=_trace_ref(decision_context),
        fact_status="not_fact",
        candidate_not_fact=True,
    )


def build_decision_candidate(
    decision_context: DecisionContextCandidate,
    readiness_candidate: DecisionReadinessCandidate,
    governance_ref: Optional[str] = None,
) -> Optional[DecisionCandidate]:
    if readiness_candidate.readiness != DecisionReadiness.READY.value:
        return None
    gov = governance_ref or decision_context.governance_check_ref
    state = DecisionState.DECISION_CANDIDATE_GENERATED.value
    return DecisionCandidate(
        candidate_id=f"dc_{decision_context.candidate_id}",
        decision_context_ref=decision_context.candidate_id,
        readiness=DecisionReadiness.READY.value,
        decision_state=state,
        decision_summary=f"candidate decision for {decision_context.candidate_id}",
        recommended_handoff="downstream_decision_handoff_candidate",
        governance_check_ref=gov,
        health_refs=decision_context.health_refs,
        conflict_refs=decision_context.conflict_refs,
        gap_refs=decision_context.gap_refs,
        trace_ref=_trace_ref(decision_context),
        fact_status="not_fact",
        final_action=False,
        user_output=False,
        candidate_not_fact=True,
    )


def build_decision_explanation_candidate(
    decision_candidate: DecisionCandidate,
    context: Optional[Mapping[str, Any]] = None,
) -> DecisionExplanationCandidate:
    ctx = context or {}
    return DecisionExplanationCandidate(
        candidate_id=f"dex_{decision_candidate.candidate_id}",
        decision_candidate_ref=decision_candidate.candidate_id,
        explanation_summary=ctx.get("explanation_summary", "skeleton explanation candidate without model"),
        evidence_refs=tuple(ctx.get("evidence_refs") or ()),
        conflict_summary=ctx.get("conflict_summary", ""),
        gap_summary=ctx.get("gap_summary", ""),
        health_summary=ctx.get("health_summary", ""),
        governance_summary=ctx.get("governance_summary", ""),
        trace_ref=decision_candidate.trace_ref,
        fact_status="not_fact",
        candidate_not_fact=True,
    )


def build_downstream_decision_handoff_candidate(
    decision_candidate: DecisionCandidate,
    readiness_candidate: DecisionReadinessCandidate,
    routes: Optional[Mapping[str, Any]] = None,
) -> DownstreamDecisionHandoffCandidate:
    route_map = routes or {}
    handoff_allowed = readiness_candidate.readiness == DecisionReadiness.READY.value
    if route_map.get("output_before_gate"):
        handoff_allowed = False
    return DownstreamDecisionHandoffCandidate(
        candidate_id=f"ddhc_{decision_candidate.candidate_id}",
        decision_candidate_ref=decision_candidate.candidate_id,
        task_manager_refs=tuple(route_map.get("task_manager_refs") or ()),
        output_gate_refs=tuple(route_map.get("output_gate_refs") or ()),
        health_watchdog_refs=tuple(route_map.get("health_watchdog_refs") or ()),
        module_adapter_refs=tuple(route_map.get("module_adapter_refs") or ()),
        worldmodel_memory_bridge_refs=tuple(route_map.get("worldmodel_memory_bridge_refs") or ()),
        governance_refs=tuple(route_map.get("governance_refs") or ()),
        handoff_allowed=handoff_allowed,
        direct_mount=False,
        trace_ref=decision_candidate.trace_ref,
        fact_status="not_fact",
        candidate_not_fact=True,
    )


def evaluate_output_before_gate_block(
    decision_context: DecisionContextCandidate,
    routes: Optional[Mapping[str, Any]] = None,
) -> Optional[DecisionBlockCandidate]:
    route_map = routes or {}
    if not route_map.get("output_before_gate") and not route_map.get("output_handoff_candidate"):
        return None
    return DecisionBlockCandidate(
        candidate_id=f"dbc_output_{decision_context.candidate_id}",
        block_type="output_before_gate",
        block_reason="output route attempted before Output Gate mount",
        blocked_refs=(decision_context.candidate_id,),
        forbidden_route="output_before_gate",
        recovery_or_hold_candidate="decision_block_candidate",
        trace_ref=_trace_ref(decision_context),
        fact_status="not_fact",
        candidate_not_fact=True,
    )


def validate_decision_center_candidate(obj: Any) -> ValidationResult:
    issues: List[str] = []
    if not validate_candidate_not_fact(obj).valid:
        issues.append("candidate_not_fact_false")
    trace_ref = getattr(obj, "trace_ref", None)
    if not trace_ref:
        issues.append("missing_trace")
    fact_status = getattr(obj, "fact_status", None)
    if fact_status and fact_status != "not_fact":
        issues.append("fact_status_not_candidate")
    if hasattr(obj, "final_action") and getattr(obj, "final_action") is True:
        issues.append("final_action_not_allowed")
    if hasattr(obj, "user_output") and getattr(obj, "user_output") is True:
        issues.append("user_output_not_allowed")
    if hasattr(obj, "direct_mount") and getattr(obj, "direct_mount") is True:
        issues.append("direct_mount_not_allowed")
    if hasattr(obj, "write_allowed") and getattr(obj, "write_allowed") is True:
        issues.append("write_not_allowed")
    if hasattr(obj, "task_execution") and getattr(obj, "task_execution") is True:
        issues.append("task_execution_not_allowed")
    gov_result = validate_governance_guard(obj)
    if not gov_result.valid:
        issues.extend(gov_result.issues)
    return ValidationResult(
        valid=len(issues) == 0,
        issues=tuple(issues),
        blocked=bool(issues),
    )
