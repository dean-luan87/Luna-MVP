"""Compact synthetic scenarios for the candidate-only Loop skeleton."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from .cognitive_loop_continuity_candidate_types_v1 import CONTINUITY_SIGNALS


@dataclass(frozen=True)
class LoopScenarioSpecV1:
    scenario_id: str
    title: str
    loop_count: int = 1
    lifecycles: Tuple[str, ...] = ("ACTIVE",)
    shared_intent: bool = False
    shared_task: bool = False
    shared_context: bool = False
    resume: bool = False
    resume_decision: str | None = None
    changed_signals: Tuple[str, ...] = ()
    changed_world_same_concern: bool = False
    stale_requirement: bool = False
    capability_count: int = 0
    request_more_evidence: bool = False
    duplicate_requirement: bool = False
    diminishing_value: bool = False
    resource_pressure: bool = False
    sufficient_completion: bool = False
    materialization_reason: str = "persistent_cognitive_concern"
    parallel_brain_path_requested: bool = False
    closure: bool = False
    outcome_guard_focus: str = ""
    branch_reservation: bool = False
    failure_loop_a: bool = False
    autonomous_spawn_requested: bool = False


def _spec(
    scenario_id: str,
    title: str,
    *,
    loop_count: int = 1,
    lifecycles: Tuple[str, ...] = ("ACTIVE",),
    shared_intent: bool = False,
    shared_task: bool = False,
    shared_context: bool = False,
    resume: bool = False,
    resume_decision: str | None = None,
    changed_signals: Tuple[str, ...] = (),
    changed_world_same_concern: bool = False,
    stale_requirement: bool = False,
    capability_count: int = 0,
    request_more_evidence: bool = False,
    duplicate_requirement: bool = False,
    diminishing_value: bool = False,
    resource_pressure: bool = False,
    sufficient_completion: bool = False,
    materialization_reason: str = "persistent_cognitive_concern",
    parallel_brain_path_requested: bool = False,
    closure: bool = False,
    outcome_guard_focus: str = "",
    branch_reservation: bool = False,
    failure_loop_a: bool = False,
    autonomous_spawn_requested: bool = False,
) -> LoopScenarioSpecV1:
    return LoopScenarioSpecV1(
        scenario_id,
        title,
        loop_count,
        lifecycles,
        shared_intent,
        shared_task,
        shared_context,
        resume,
        resume_decision,
        changed_signals,
        changed_world_same_concern,
        stale_requirement,
        capability_count,
        request_more_evidence,
        duplicate_requirement,
        diminishing_value,
        resource_pressure,
        sufficient_completion,
        materialization_reason,
        parallel_brain_path_requested,
        closure,
        outcome_guard_focus,
        branch_reservation,
        failure_loop_a,
        autonomous_spawn_requested,
    )


def build_loop_scenario_specs_v1() -> Tuple[LoopScenarioSpecV1, ...]:
    """Reuse the original 32 planning cases and add only implementation gaps."""

    return (
        _spec("ML-01", "two independent Loops coexist", loop_count=2),
        _spec("ML-02", "three Loops coexist", loop_count=3),
        _spec("ML-03", "one Loop ACTIVE while another WAITING", loop_count=2, lifecycles=("ACTIVE", "WAITING")),
        _spec("ML-04", "one Loop PAUSED", lifecycles=("PAUSED",)),
        _spec("ML-05", "paused Loop preserves state version", lifecycles=("PAUSED",)),
        _spec("ML-06", "paused Loop preserves current Need", lifecycles=("PAUSED",)),
        _spec("ML-07", "resume with unchanged world KEEP", resume=True, resume_decision="KEEP"),
        _spec("ML-08", "resume with changed world REPLAN", resume=True, resume_decision="REPLAN", changed_signals=("FIELD",)),
        _spec("ML-09", "stale Requirement SUPERSEDE", resume=True, resume_decision="SUPERSEDE", stale_requirement=True),
        _spec("ML-10", "waiting for user response", lifecycles=("WAITING",)),
        _spec("ML-11", "waiting for capability recovery", lifecycles=("WAITING",)),
        _spec("ML-12", "resource pressure pauses optional Loop", lifecycles=("PAUSED",), resource_pressure=True),
        _spec("ML-13", "Safety Loop preempts normal Loop", loop_count=2, lifecycles=("PAUSED", "ACTIVE")),
        _spec("ML-14", "normal Loop is not auto-resumed blindly", lifecycles=("PAUSED",), resume=True, resume_decision="WAITING"),
        _spec("ML-15", "resume COMPLETE closes the Loop without continuing observations", lifecycles=("PAUSED",), resume=True, resume_decision="COMPLETE", closure=True),
        _spec("ML-16", "STOP_SUFFICIENT completes only its own Loop", lifecycles=("COMPLETED",), closure=True, sufficient_completion=True),
        _spec("ML-17", "one Loop failure does not terminate another", loop_count=2, failure_loop_a=True),
        _spec("ML-18", "remaining candidates are Loop-local", loop_count=2),
        _spec("ML-19", "trace and provenance are isolated by loop_id", loop_count=2),
        _spec("ML-20", "REQUEST_MORE_EVIDENCE does not invoke Provider", capability_count=1, request_more_evidence=True),
        _spec("ML-21", "second Observation Candidate requires new state assessment", capability_count=1, resume=True, resume_decision="KEEP"),
        _spec("ML-22", "paused candidates are not capability failures", lifecycles=("PAUSED",)),
        _spec("ML-23", "same Context supports independent state versions", loop_count=2, shared_context=True),
        _spec("ML-24", "resume preserves Intent refs without recreating Intent", resume=True, resume_decision="KEEP", shared_intent=True),
        _spec("ML-25", "Need is reassessed before new Requirement", resume=True, resume_decision="REPLAN", changed_signals=("FIELD",)),
        _spec("ML-26", "continuation rechecks Scope and Resolution", capability_count=1, resume=True, resume_decision="KEEP"),
        _spec("ML-27", "shared resource refs remain read-only", loop_count=2, resource_pressure=True),
        _spec("ML-28", "Safety priority cannot bypass Scope or Truth", capability_count=1),
        _spec("ML-29", "WAITING becomes ACTIVE only after dependency resolution", lifecycles=("WAITING",), resume=True, resume_decision="KEEP"),
        _spec("ML-30", "STOPPED remains distinct from COMPLETED", lifecycles=("STOPPED",), closure=True),
        _spec("ML-31", "DEFERRED has no forced next step", lifecycles=("DEFERRED",)),
        _spec("ML-32", "evidence update cannot cross Loop boundaries", loop_count=2, shared_context=True),
        _spec("ML-33", "same Intent with different cognitive concerns", loop_count=2, shared_intent=True),
        _spec("ML-34", "same Task with different cognitive concerns", loop_count=2, shared_task=True),
        _spec("ML-35", "all six continuity signals are assessed", resume=True, resume_decision="KEEP", changed_signals=CONTINUITY_SIGNALS),
        _spec("ML-36", "changed Current World preserves cognitive concern identity", resume=True, resume_decision="REPLAN", changed_world_same_concern=True, changed_signals=("SPATIAL", "FIELD")),
        _spec("ML-37", "Brain and Loop do not duplicate a materialized concern", parallel_brain_path_requested=True, materialization_reason="cross_time_continuity"),
        _spec("ML-38", "Need-driven multi-capability reservation", capability_count=2),
        _spec("ML-39", "duplicate and diminishing-value growth are blocked", capability_count=2, duplicate_requirement=True, diminishing_value=True),
        _spec("ML-40", "resource envelope blocks optional growth", capability_count=2, resource_pressure=True),
        _spec("ML-41", "Loop closure produces Cognitive Outcome Candidate", closure=True, outcome_guard_focus="closure"),
        _spec("ML-42", "branch and assimilation boundaries remain candidate-only", closure=True, branch_reservation=True, autonomous_spawn_requested=True, outcome_guard_focus="assimilation"),
    )


__all__ = ["LoopScenarioSpecV1", "build_loop_scenario_specs_v1"]
