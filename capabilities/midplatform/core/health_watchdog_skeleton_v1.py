# -*- coding: utf-8 -*-
"""Health Watchdog skeleton v1 - pure functions and candidate generators only."""

from __future__ import annotations

from typing import Any, Dict, Mapping, Optional, Sequence, Tuple

from capabilities.midplatform.core.decision_center_types_v1 import (
    DecisionBlockCandidate,
    DecisionCandidate,
    DecisionExplanationCandidate,
    DecisionReadinessCandidate,
    DownstreamDecisionHandoffCandidate,
)
from capabilities.midplatform.core.health_watchdog_types_v1 import (
    DegradationCandidate,
    HealthSeverity,
    HealthSignalCandidate,
    HealthWatchdogState,
    ModuleHealthReviewCandidate,
    RecoveryRecommendationCandidate,
    RequiredObservationCandidate,
    WatchdogHandoffCandidate,
)
from capabilities.midplatform.core.micro_os_common_types_v1 import ValidationResult
from capabilities.midplatform.core.micro_os_static_validators_v1 import validate_candidate_not_fact

FROZEN_DECISION_CENTER_OUTPUT_TYPES = (
    DecisionCandidate,
    DecisionReadinessCandidate,
    DecisionBlockCandidate,
    DecisionExplanationCandidate,
    DownstreamDecisionHandoffCandidate,
)


def _value(obj: Any, name: str, default: Any = None) -> Any:
    if isinstance(obj, Mapping):
        return obj.get(name, default)
    return getattr(obj, name, default)


def _tuple_value(obj: Any, name: str) -> Tuple[str, ...]:
    value = _value(obj, name, ())
    if value is None:
        return ()
    if isinstance(value, str):
        return (value,)
    return tuple(str(v) for v in value)


def _candidate_id(obj: Any) -> str:
    return str(_value(obj, "candidate_id", _value(obj, "decision_candidate_ref", "unknown")))


def _trace_ref(obj: Any) -> str:
    return str(_value(obj, "trace_ref", _value(obj, "trace_id", "")) or "")


def validate_health_watchdog_input(
    input_candidate: Any,
    guards: Optional[Mapping[str, Any]] = None,
) -> ValidationResult:
    issues = []
    if not _trace_ref(input_candidate):
        issues.append("missing_trace")
    if _value(input_candidate, "health_tag", "health_watchdog_candidate") is None:
        issues.append("missing_health_tag")
    if not validate_candidate_not_fact(input_candidate).valid:
        issues.append("candidate_not_fact_false")
    if _value(input_candidate, "fact_status", "not_fact") != "not_fact":
        issues.append("fact_status_not_candidate")
    if not _value(input_candidate, "source_chain", _candidate_id(input_candidate)):
        issues.append("missing_source_chain")
    guard_map = guards or {}
    governance_required = bool(
        _value(input_candidate, "governance_required", False)
        or _value(input_candidate, "high_risk", False)
        or guard_map.get("governance_required")
    )
    governance_ref = _value(input_candidate, "governance_ref", _value(input_candidate, "governance_check_ref", None))
    if governance_required and not governance_ref:
        issues.append("governance_ref_missing_for_high_risk")
    return ValidationResult(valid=len(issues) == 0, issues=tuple(issues), blocked=bool(issues))


def classify_health_signal(
    input_candidate: Any,
    severity_rules: Optional[Mapping[str, str]] = None,
) -> HealthSignalCandidate:
    health_refs = _tuple_value(input_candidate, "health_refs")
    stale_refs = _tuple_value(input_candidate, "stale_refs")
    low_confidence_refs = _tuple_value(input_candidate, "low_confidence_refs")
    p0_safety_refs = _tuple_value(input_candidate, "p0_safety_refs")
    governance_refs = _tuple_value(input_candidate, "governance_refs")
    rules = severity_rules or {}
    if p0_safety_refs:
        severity = rules.get("p0_safety", HealthSeverity.CRITICAL.value)
        signal_type = "p0_safety_unresolved"
    elif low_confidence_refs:
        severity = rules.get("low_confidence", HealthSeverity.MEDIUM.value)
        signal_type = "low_confidence"
    elif stale_refs:
        severity = rules.get("stale_context", HealthSeverity.LOW.value)
        signal_type = "stale_context"
    elif not health_refs:
        severity = rules.get("missing_health_refs", HealthSeverity.MEDIUM.value)
        signal_type = "missing_health_refs"
    else:
        severity = rules.get("healthy_candidate", HealthSeverity.INFO.value)
        signal_type = "health_signal_review"
    return HealthSignalCandidate(
        candidate_id=f"hw_signal_{_candidate_id(input_candidate)}",
        source_decision_ref=_candidate_id(input_candidate),
        signal_type=signal_type,
        severity=severity,
        health_refs=health_refs,
        stale_refs=stale_refs,
        low_confidence_refs=low_confidence_refs,
        p0_safety_refs=p0_safety_refs,
        governance_refs=governance_refs,
        trace_ref=_trace_ref(input_candidate),
    )


def evaluate_stale_context_candidate(input_candidate: Any) -> Optional[RequiredObservationCandidate]:
    signal = input_candidate if isinstance(input_candidate, HealthSignalCandidate) else classify_health_signal(input_candidate)
    if not signal.stale_refs:
        return None
    return RequiredObservationCandidate(
        candidate_id=f"hw_obs_stale_{signal.candidate_id}",
        observation_reason="stale_context_requires_observation_candidate",
        target_refs=signal.stale_refs,
        urgency="medium",
        source_health_signal_ref=signal.candidate_id,
        trace_ref=signal.trace_ref,
    )


def evaluate_low_confidence_candidate(input_candidate: Any) -> Dict[str, Any]:
    signal = input_candidate if isinstance(input_candidate, HealthSignalCandidate) else classify_health_signal(input_candidate)
    if not signal.low_confidence_refs:
        return {
            "state": HealthWatchdogState.HEALTH_SIGNAL_REVIEW.value,
            "hold_candidate": False,
            "required_observation_candidate": None,
            "task_execution": False,
            "user_output": False,
        }
    observation = RequiredObservationCandidate(
        candidate_id=f"hw_obs_low_conf_{signal.candidate_id}",
        observation_reason="low_confidence_requires_more_observation",
        target_refs=signal.low_confidence_refs,
        urgency="high",
        source_health_signal_ref=signal.candidate_id,
        trace_ref=signal.trace_ref,
    )
    return {
        "state": HealthWatchdogState.HOLD.value,
        "readiness": HealthWatchdogState.NOT_READY.value,
        "hold_candidate": True,
        "required_observation_candidate": observation,
        "task_execution": False,
        "user_output": False,
    }


def evaluate_p0_safety_candidate(input_candidate: Any) -> Optional[DecisionBlockCandidate]:
    signal = input_candidate if isinstance(input_candidate, HealthSignalCandidate) else classify_health_signal(input_candidate)
    if not signal.p0_safety_refs:
        return None
    return DecisionBlockCandidate(
        candidate_id=f"hw_block_p0_{signal.candidate_id}",
        block_type="p0_safety_unresolved",
        block_reason="P0 safety unresolved; output and task execution remain blocked",
        blocked_refs=signal.p0_safety_refs,
        forbidden_route="output_gate_or_task_manager_before_safety_clearance",
        recovery_or_hold_candidate="health_watchdog_hold_candidate",
        trace_ref=signal.trace_ref,
        fact_status="not_fact",
        candidate_not_fact=True,
    )


def evaluate_degradation_candidate(
    health_signal: HealthSignalCandidate,
    context: Optional[Mapping[str, Any]] = None,
) -> DegradationCandidate:
    ctx = context or {}
    affected = tuple(ctx.get("affected_module_refs") or health_signal.health_refs or (health_signal.source_decision_ref,))
    recommended_hold = health_signal.severity in (HealthSeverity.HIGH.value, HealthSeverity.CRITICAL.value)
    return DegradationCandidate(
        candidate_id=f"hw_deg_{health_signal.candidate_id}",
        degradation_type=ctx.get("degradation_type", health_signal.signal_type),
        degradation_level=ctx.get("degradation_level", health_signal.severity),
        affected_module_refs=affected,
        reason=ctx.get("reason", f"candidate degradation review for {health_signal.signal_type}"),
        recommended_hold=bool(ctx.get("recommended_hold", recommended_hold)),
        trace_ref=health_signal.trace_ref,
        real_degradation=False,
    )


def build_recovery_recommendation_candidate(
    health_signal: HealthSignalCandidate,
    degradation: Optional[DegradationCandidate] = None,
    governance_ref: Optional[str] = None,
) -> RecoveryRecommendationCandidate:
    affected = degradation.affected_module_refs if degradation else (health_signal.source_decision_ref,)
    high_risk = health_signal.severity in (HealthSeverity.HIGH.value, HealthSeverity.CRITICAL.value)
    return RecoveryRecommendationCandidate(
        candidate_id=f"hw_rec_{health_signal.candidate_id}",
        recommendation_type="candidate_reobserve_or_hold",
        recommendation_reason=f"candidate recommendation for {health_signal.signal_type}",
        affected_module_refs=affected,
        governance_required=high_risk,
        governance_ref=governance_ref,
        trace_ref=health_signal.trace_ref,
        recovery_execution=False,
        restart_allowed=False,
        process_control_allowed=False,
    )


def build_module_health_review_candidate(
    health_signal: HealthSignalCandidate,
    module_ref: Optional[str] = None,
) -> ModuleHealthReviewCandidate:
    return ModuleHealthReviewCandidate(
        candidate_id=f"hw_mhr_{health_signal.candidate_id}",
        module_ref=module_ref or health_signal.source_decision_ref,
        issue_type=health_signal.signal_type,
        severity=health_signal.severity,
        evidence_refs=health_signal.health_refs
        + health_signal.stale_refs
        + health_signal.low_confidence_refs
        + health_signal.p0_safety_refs,
        recommended_status="hold" if health_signal.severity != HealthSeverity.INFO.value else "observe",
        trace_ref=health_signal.trace_ref,
    )


def build_watchdog_handoff_candidate(
    health_signal: HealthSignalCandidate,
    degradation: Optional[DegradationCandidate] = None,
    recovery_recommendation: Optional[RecoveryRecommendationCandidate] = None,
    routes: Optional[Mapping[str, Sequence[str]]] = None,
) -> WatchdogHandoffCandidate:
    route_map = routes or {}
    source_refs = [health_signal.candidate_id]
    if degradation is not None:
        source_refs.append(degradation.candidate_id)
    if recovery_recommendation is not None:
        source_refs.append(recovery_recommendation.candidate_id)
    handoff_allowed = not bool(route_map.get("direct_mount_requested"))
    if recovery_recommendation and recovery_recommendation.governance_required and not recovery_recommendation.governance_ref:
        handoff_allowed = False
    return WatchdogHandoffCandidate(
        candidate_id=f"hw_handoff_{health_signal.candidate_id}",
        source_candidate_refs=tuple(source_refs),
        module_adapter_refs=tuple(route_map.get("module_adapter_refs") or ()),
        task_manager_refs=tuple(route_map.get("task_manager_refs") or ()),
        decision_center_refs=tuple(route_map.get("decision_center_refs") or (health_signal.source_decision_ref,)),
        governance_refs=tuple(route_map.get("governance_refs") or ()),
        output_gate_refs=tuple(route_map.get("output_gate_refs") or ()),
        handoff_allowed=handoff_allowed,
        direct_mount=False,
        trace_ref=health_signal.trace_ref,
    )


def validate_health_watchdog_candidate(obj: Any) -> ValidationResult:
    issues = []
    if not validate_candidate_not_fact(obj).valid:
        issues.append("candidate_not_fact_false")
    if getattr(obj, "fact_status", "not_fact") != "not_fact":
        issues.append("fact_status_not_candidate")
    if not getattr(obj, "trace_ref", None):
        issues.append("missing_trace")
    if getattr(obj, "recovery_execution", False):
        issues.append("recovery_execution_not_allowed")
    if getattr(obj, "restart_allowed", False):
        issues.append("restart_not_allowed")
    if getattr(obj, "process_control_allowed", False):
        issues.append("process_control_not_allowed")
    if getattr(obj, "real_degradation", False):
        issues.append("real_degradation_not_allowed")
    if getattr(obj, "direct_mount", False):
        issues.append("direct_mount_not_allowed")
    if getattr(obj, "task_execution", False):
        issues.append("task_execution_not_allowed")
    if getattr(obj, "user_output", False):
        issues.append("user_output_not_allowed")
    if getattr(obj, "memory_write_allowed", False) or getattr(obj, "worldmodel_write_allowed", False):
        issues.append("memory_worldmodel_write_not_allowed")
    return ValidationResult(valid=len(issues) == 0, issues=tuple(issues), blocked=bool(issues))
