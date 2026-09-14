# -*- coding: utf-8 -*-
"""Task Manager skeleton v1 - pure functions and candidate generators only."""

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
    HealthSignalCandidate,
    ModuleHealthReviewCandidate,
    RecoveryRecommendationCandidate,
    RequiredObservationCandidate,
    WatchdogHandoffCandidate,
)
from capabilities.midplatform.core.micro_os_common_types_v1 import ValidationResult
from capabilities.midplatform.core.micro_os_static_validators_v1 import validate_candidate_not_fact
from capabilities.midplatform.core.task_manager_types_v1 import (
    TaskBlockCandidate,
    TaskCandidate,
    TaskHandoffCandidate,
    TaskPlanCandidate,
    TaskReadiness,
    TaskReadinessCandidate,
    TaskState,
    TaskStepCandidate,
)

FROZEN_DECISION_CENTER_OUTPUT_TYPES = (
    DecisionCandidate,
    DecisionReadinessCandidate,
    DecisionBlockCandidate,
    DecisionExplanationCandidate,
    DownstreamDecisionHandoffCandidate,
)

FROZEN_HEALTH_WATCHDOG_OUTPUT_TYPES = (
    HealthSignalCandidate,
    DegradationCandidate,
    RecoveryRecommendationCandidate,
    RequiredObservationCandidate,
    ModuleHealthReviewCandidate,
    WatchdogHandoffCandidate,
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
    return str(_value(obj, "candidate_id", "unknown"))


def _trace_ref(obj: Any) -> str:
    return str(_value(obj, "trace_ref", _value(obj, "trace_id", "")) or "")


def validate_task_manager_input(input_candidate: Any, guards: Optional[Mapping[str, Any]] = None) -> ValidationResult:
    issues = []
    if not _trace_ref(input_candidate):
        issues.append("missing_trace")
    if _value(input_candidate, "health_tag", "task_candidate_health") is None:
        issues.append("missing_health_tag")
    if not validate_candidate_not_fact(input_candidate).valid:
        issues.append("candidate_not_fact_false")
    if _value(input_candidate, "fact_status", "not_fact") != "not_fact":
        issues.append("fact_status_not_candidate")
    if not _value(input_candidate, "source_chain", _candidate_id(input_candidate)):
        issues.append("missing_source_chain")
    guard_map = guards or {}
    high_risk = bool(_value(input_candidate, "high_risk", False) or guard_map.get("high_risk"))
    governance_ref = _value(input_candidate, "governance_ref", _value(input_candidate, "governance_check_ref", None))
    if high_risk and not governance_ref:
        issues.append("governance_ref_missing_for_high_risk_task")
    return ValidationResult(valid=len(issues) == 0, issues=tuple(issues), blocked=bool(issues))


def classify_task_readiness(
    input_candidate: Any,
    health_refs: Optional[Sequence[str]] = None,
    decision_refs: Optional[Sequence[str]] = None,
    governance_ref: Optional[str] = None,
) -> TaskReadinessCandidate:
    health_gate_refs = tuple(health_refs if health_refs is not None else _tuple_value(input_candidate, "health_gate_refs"))
    decision_block_refs = tuple(decision_refs if decision_refs is not None else _tuple_value(input_candidate, "decision_block_refs"))
    observation_refs = _tuple_value(input_candidate, "required_observation_refs")
    blocker_refs = list(_tuple_value(input_candidate, "blocker_refs"))
    readiness = TaskReadiness.READY.value
    reason = "task_candidate_ready_for_candidate_progression"
    governance_pending = False
    if _value(input_candidate, "high_risk", False) and not (governance_ref or _value(input_candidate, "governance_ref", None)):
        readiness = TaskReadiness.BLOCKED.value
        reason = "high_risk_task_missing_governance_ref"
        governance_pending = True
        blocker_refs.append("governance_pending")
    elif health_gate_refs:
        readiness = TaskReadiness.HOLD.value
        reason = "health_gate_or_hold_blocks_task_candidate"
        blocker_refs.extend(health_gate_refs)
    elif decision_block_refs:
        readiness = TaskReadiness.BLOCKED.value
        reason = "decision_block_prevents_task_candidate"
        blocker_refs.extend(decision_block_refs)
    elif observation_refs:
        readiness = TaskReadiness.REQUIRES_OBSERVATION.value
        reason = "required_observation_before_task_candidate"
    return TaskReadinessCandidate(
        candidate_id=f"tm_ready_{_candidate_id(input_candidate)}",
        task_candidate_ref=_candidate_id(input_candidate),
        readiness=readiness,
        readiness_reason=reason,
        blocker_refs=tuple(blocker_refs),
        health_gate_refs=health_gate_refs,
        required_observation_refs=observation_refs,
        governance_pending=governance_pending,
        trace_ref=_trace_ref(input_candidate),
    )


def evaluate_health_gate_block_candidate(input_candidate: Any, health_refs: Sequence[str]) -> Optional[TaskBlockCandidate]:
    refs = tuple(str(r) for r in health_refs)
    if not refs:
        return None
    return TaskBlockCandidate(
        candidate_id=f"tm_block_health_{_candidate_id(input_candidate)}",
        block_type="health_gate_active",
        block_reason="health hold/block/safety refs prevent ready task candidate",
        blocked_refs=refs,
        forbidden_route="ignore_health_gate",
        hold_or_reobserve_candidate="task_hold_candidate",
        trace_ref=_trace_ref(input_candidate),
    )


def evaluate_required_observation_candidate(input_candidate: Any, observation_refs: Sequence[str]) -> Dict[str, Any]:
    refs = tuple(str(r) for r in observation_refs)
    return {
        "readiness": TaskReadiness.REQUIRES_OBSERVATION.value if refs else TaskReadiness.READY.value,
        "required_observation_refs": refs,
        "required_observation_handoff_candidate": f"tm_obs_handoff_{_candidate_id(input_candidate)}" if refs else None,
        "task_execution": False,
        "direct_mount": False,
    }


def evaluate_governance_task_candidate(input_candidate: Any, governance_ref: Optional[str] = None) -> Optional[TaskBlockCandidate]:
    if not _value(input_candidate, "high_risk", False) or governance_ref or _value(input_candidate, "governance_ref", None):
        return None
    return TaskBlockCandidate(
        candidate_id=f"tm_block_gov_{_candidate_id(input_candidate)}",
        block_type="governance_pending",
        block_reason="high-risk task missing governance_ref",
        blocked_refs=(_candidate_id(input_candidate),),
        forbidden_route="bypass_governance_gate",
        hold_or_reobserve_candidate="governance_review_candidate",
        trace_ref=_trace_ref(input_candidate),
    )


def build_task_candidate(
    input_candidate: Any,
    readiness_candidate: TaskReadinessCandidate,
    governance_ref: Optional[str] = None,
) -> Optional[TaskCandidate]:
    if readiness_candidate.readiness != TaskReadiness.READY.value:
        return None
    return TaskCandidate(
        candidate_id=f"tm_task_{_candidate_id(input_candidate)}",
        source_decision_ref=_value(input_candidate, "source_decision_ref", _candidate_id(input_candidate)),
        source_health_refs=_tuple_value(input_candidate, "source_health_refs"),
        task_context_refs=_tuple_value(input_candidate, "task_context_refs"),
        readiness=readiness_candidate.readiness,
        task_state=TaskState.TASK_CANDIDATE_GENERATED.value,
        task_summary=_value(input_candidate, "task_summary", "task candidate generated without execution"),
        governance_ref=governance_ref or _value(input_candidate, "governance_ref", None),
        health_gate_refs=readiness_candidate.health_gate_refs,
        blocker_refs=readiness_candidate.blocker_refs,
        trace_ref=readiness_candidate.trace_ref,
        task_execution=False,
        user_output=False,
    )


def build_task_plan_candidate(task_candidate: TaskCandidate, context: Optional[Mapping[str, Any]] = None) -> TaskPlanCandidate:
    ctx = context or {}
    return TaskPlanCandidate(
        candidate_id=f"tm_plan_{task_candidate.candidate_id}",
        task_candidate_ref=task_candidate.candidate_id,
        plan_summary=ctx.get("plan_summary", "candidate task plan without execution"),
        planned_step_refs=tuple(ctx.get("planned_step_refs") or ("candidate_step_1",)),
        dependency_refs=tuple(ctx.get("dependency_refs") or ()),
        blocker_refs=task_candidate.blocker_refs,
        trace_ref=task_candidate.trace_ref,
        task_execution=False,
    )


def build_task_step_candidate(
    task_candidate: TaskCandidate,
    plan_candidate: Optional[TaskPlanCandidate] = None,
    step_context: Optional[Mapping[str, Any]] = None,
) -> TaskStepCandidate:
    ctx = step_context or {}
    return TaskStepCandidate(
        candidate_id=f"tm_step_{task_candidate.candidate_id}_{ctx.get('step_order', 1)}",
        task_candidate_ref=task_candidate.candidate_id,
        step_order=int(ctx.get("step_order", 1)),
        step_summary=ctx.get("step_summary", "candidate task step without execution"),
        required_capability_refs=tuple(ctx.get("required_capability_refs") or ()),
        required_observation_refs=tuple(ctx.get("required_observation_refs") or ()),
        blocker_refs=plan_candidate.blocker_refs if plan_candidate else task_candidate.blocker_refs,
        trace_ref=task_candidate.trace_ref,
        executed_step=False,
    )


def build_task_handoff_candidate(
    task_candidate: TaskCandidate,
    readiness_candidate: TaskReadinessCandidate,
    routes: Optional[Mapping[str, Sequence[str]]] = None,
) -> TaskHandoffCandidate:
    route_map = routes or {}
    handoff_allowed = readiness_candidate.readiness == TaskReadiness.READY.value and not route_map.get("direct_mount_requested")
    return TaskHandoffCandidate(
        candidate_id=f"tm_handoff_{task_candidate.candidate_id}",
        task_candidate_ref=task_candidate.candidate_id,
        module_adapter_refs=tuple(route_map.get("module_adapter_refs") or ()),
        output_gate_refs=tuple(route_map.get("output_gate_refs") or ()),
        worldmodel_memory_bridge_refs=tuple(route_map.get("worldmodel_memory_bridge_refs") or ()),
        decision_center_refs=tuple(route_map.get("decision_center_refs") or (task_candidate.source_decision_ref,)),
        health_watchdog_refs=task_candidate.source_health_refs,
        governance_refs=tuple(route_map.get("governance_refs") or (() if not task_candidate.governance_ref else (task_candidate.governance_ref,))),
        handoff_allowed=handoff_allowed,
        direct_mount=False,
        trace_ref=task_candidate.trace_ref,
    )


def validate_task_manager_candidate(obj: Any) -> ValidationResult:
    issues = []
    if not validate_candidate_not_fact(obj).valid:
        issues.append("candidate_not_fact_false")
    if getattr(obj, "fact_status", "not_fact") != "not_fact":
        issues.append("fact_status_not_candidate")
    if not getattr(obj, "trace_ref", None):
        issues.append("missing_trace")
    if getattr(obj, "task_execution", False):
        issues.append("task_execution_not_allowed")
    if getattr(obj, "executed_step", False):
        issues.append("executed_step_not_allowed")
    if getattr(obj, "tool_call", False):
        issues.append("tool_call_not_allowed")
    if getattr(obj, "user_output", False):
        issues.append("user_output_not_allowed")
    if getattr(obj, "memory_write_allowed", False) or getattr(obj, "worldmodel_write_allowed", False):
        issues.append("memory_worldmodel_write_not_allowed")
    if getattr(obj, "direct_mount", False):
        issues.append("direct_mount_not_allowed")
    return ValidationResult(valid=len(issues) == 0, issues=tuple(issues), blocked=bool(issues))
