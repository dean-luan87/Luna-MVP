"""Focused synthetic lifecycle-closure scenarios."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple

from .cognitive_loop_lifecycle_closure_types_v1 import ASSIMILATION_DISPOSITIONS, CLOSURE_REASONS


@dataclass(frozen=True)
class LifecycleClosureScenarioSpecV1:
    scenario_id: str
    title: str
    closure_reason: str
    lifecycle_disposition: str
    closure_candidate_created: bool = True
    lifecycle_closure_accepted: bool = True
    base_scenario_id: str = "ML-41"
    assimilation_disposition: Optional[str] = None
    branch_reservation: bool = False
    parent_supersede_governed: bool = False
    outstanding_requirements: Tuple[str, ...] = ()
    outstanding_observations: Tuple[str, ...] = ()
    stale_requirement: bool = False
    skipped_candidates: Tuple[str, ...] = ()
    low_value: bool = False
    capability_gap: bool = False
    safety_termination: bool = False
    context_invalidated: bool = False
    no_new_owner: bool = True
    no_runtime: bool = True


def _spec(
    scenario_id: str,
    title: str,
    reason: str,
    disposition: str,
    *,
    accepted: bool = True,
    base: str = "ML-41",
    assimilation: Optional[str] = None,
    branch: bool = False,
    parent_supersede: bool = False,
    requirements: Tuple[str, ...] = (),
    observations: Tuple[str, ...] = (),
    stale: bool = False,
    skipped: Tuple[str, ...] = (),
    low_value: bool = False,
    capability_gap: bool = False,
    safety: bool = False,
    invalidated: bool = False,
) -> LifecycleClosureScenarioSpecV1:
    return LifecycleClosureScenarioSpecV1(
        scenario_id=scenario_id,
        title=title,
        closure_reason=reason,
        lifecycle_disposition=disposition,
        lifecycle_closure_accepted=accepted,
        base_scenario_id=base,
        assimilation_disposition=assimilation,
        branch_reservation=branch,
        parent_supersede_governed=parent_supersede,
        outstanding_requirements=requirements,
        outstanding_observations=observations,
        stale_requirement=stale,
        skipped_candidates=skipped,
        low_value=low_value,
        capability_gap=capability_gap,
        safety_termination=safety,
        context_invalidated=invalidated,
    )


def build_lifecycle_closure_scenario_specs_v1() -> Tuple[LifecycleClosureScenarioSpecV1, ...]:
    """Twenty-eight focused cases; prior ML scenarios remain the reuse baseline."""

    return (
        _spec("LC-01", "STOP_SUFFICIENT becomes COMPLETED", "STOP_SUFFICIENT", "COMPLETED", base="ML-16"),
        _spec("LC-02", "resolved concern becomes COMPLETED", "COGNITIVE_CONCERN_RESOLVED", "COMPLETED"),
        _spec("LC-03", "superseded Intent closes the local concern", "INTENT_SUPERSEDED", "SUPERSEDED"),
        _spec("LC-04", "completed Task need closes the Loop", "TASK_OR_BEHAVIOR_COMPLETED", "COMPLETED"),
        _spec("LC-05", "invalid Context stops the concern", "CONTEXT_INVALIDATED_CONCERN", "STOPPED", invalidated=True),
        _spec("LC-06", "Brain-governed STOPPED is distinct", "BRAIN_GOVERNED_STOP", "STOPPED", base="ML-30"),
        _spec("LC-07", "low value closes without failure", "RESOURCE_VALUE_TOO_LOW", "ABANDONED_BY_VALUE", low_value=True),
        _spec("LC-08", "stale continuity becomes SUPERSEDED", "CONTINUITY_STALE", "SUPERSEDED"),
        _spec("LC-09", "unrecoverable capability gap is explicit", "UNRECOVERABLE_CAPABILITY_GAP", "FAILED", capability_gap=True),
        _spec("LC-10", "Safety termination is governed STOPPED", "SAFETY_GOVERNED_TERMINATION", "STOPPED", safety=True),
        _spec("LC-11", "parent supersede reason maps to SUPERSEDED", "PARENT_SUPERSEDED_BY_BRANCH_OR_MERGE", "SUPERSEDED", branch=True, parent_supersede=True),
        _spec("LC-12", "closure candidate does not close an OPEN Loop", "STOP_SUFFICIENT", "COMPLETED", accepted=False, base="ML-07"),
        _spec("LC-13", "accepted decision changes OPEN to closed", "COGNITIVE_CONCERN_RESOLVED", "COMPLETED", base="ML-07"),
        _spec("LC-14", "accepted closure freezes final state version", "STOP_SUFFICIENT", "COMPLETED", base="ML-16"),
        _spec("LC-15", "outstanding Requirements receive terminal dispositions", "STOP_SUFFICIENT", "COMPLETED", requirements=("requirement:one", "requirement:two")),
        _spec("LC-16", "remaining plan candidates are skipped not failed", "STOP_SUFFICIENT", "COMPLETED", base="ML-16", skipped=("candidate:4", "candidate:5", "candidate:6", "candidate:7")),
        _spec("LC-17", "stale Requirement is closed and not invocable", "STOP_SUFFICIENT", "COMPLETED", stale=True, requirements=("requirement:stale",)),
        _spec("LC-18", "Cognitive Outcome remains candidate-only", "COGNITIVE_CONCERN_RESOLVED", "COMPLETED"),
        _spec("LC-19", "Brain accepts outcome as cognitive reference", "COGNITIVE_CONCERN_RESOLVED", "COMPLETED", assimilation="ACCEPT_AS_COGNITIVE_REFERENCE"),
        _spec("LC-20", "outcome forwards to Experience governance", "COGNITIVE_CONCERN_RESOLVED", "COMPLETED", assimilation="FORWARD_TO_EXPERIENCE_GOVERNANCE"),
        _spec("LC-21", "assimilation does not mutate Memory or Experience", "COGNITIVE_CONCERN_RESOLVED", "COMPLETED", assimilation="DEFER_ASSIMILATION"),
        _spec("LC-22", "Loop Package preserves reverse traceability", "COGNITIVE_CONCERN_RESOLVED", "COMPLETED"),
        _spec("LC-23", "history boundary does not compress trace", "COGNITIVE_CONCERN_RESOLVED", "COMPLETED"),
        _spec("LC-24", "branch reservation does not close parent", "COGNITIVE_CONCERN_RESOLVED", "COMPLETED", branch=True, base="ML-42"),
        _spec("LC-25", "parent supersede requires Brain governance", "PARENT_SUPERSEDED_BY_BRANCH_OR_MERGE", "SUPERSEDED", branch=True, parent_supersede=True),
        _spec("LC-26", "closure does not spawn a child Loop", "COGNITIVE_CONCERN_RESOLVED", "COMPLETED", branch=True),
        _spec("LC-27", "closure uses existing Cognitive Flow owner", "COGNITIVE_CONCERN_RESOLVED", "COMPLETED"),
        _spec("LC-28", "closure phase stays synthetic and runtime-free", "COGNITIVE_CONCERN_RESOLVED", "COMPLETED", base="ML-41"),
    )


__all__ = ["LifecycleClosureScenarioSpecV1", "build_lifecycle_closure_scenario_specs_v1", "CLOSURE_REASONS", "ASSIMILATION_DISPOSITIONS"]
