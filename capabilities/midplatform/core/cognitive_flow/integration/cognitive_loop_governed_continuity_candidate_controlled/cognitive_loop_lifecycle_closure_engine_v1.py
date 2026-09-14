"""Deterministic candidate-only lifecycle closure engine."""

from __future__ import annotations

from typing import Dict, Iterable, Optional, Tuple

from .cognitive_loop_continuity_candidate_engine_v1 import run_loop_scenario
from .cognitive_loop_continuity_candidate_fixture_v1 import build_loop_scenario_specs_v1
from .cognitive_loop_continuity_candidate_types_v1 import (
    CognitiveOutcomeCandidateV1,
    LoopClosureRecordCandidateV1,
    LoopPackageReservationCandidateV1,
)
from .cognitive_loop_lifecycle_closure_fixture_v1 import LifecycleClosureScenarioSpecV1
from .cognitive_loop_lifecycle_closure_types_v1 import (
    ASSIMILATION_DISPOSITIONS,
    CLOSURE_LIFECYCLE_DISPOSITIONS,
    CLOSURE_REASONS,
    BrainAssimilationCandidateV1,
    ClosureAssessmentCandidateV1,
    ClosureDecisionCandidateV1,
    ClosureScenarioResultV1,
    FinalStateFreezeCandidateV1,
    HistoryBoundaryCandidateV1,
    LifecycleClosureCandidateV1,
    LoopPackageCandidateV1,
)


PHASE = "Phase-Luna-Cognitive-Loop-Lifecycle-Closure-And-Assimilation-Bridge-Controlled-Implementation-v1-001"

NEGATIVE_GUARDS: Dict[str, bool] = {
    "runtime_execution": False,
    "provider_invocation": False,
    "model_inference": False,
    "yolo": False,
    "camera": False,
    "ocr": False,
    "action_execution": False,
    "learning": False,
    "memory_mutation": False,
    "experience_mutation": False,
    "semantic_compression": False,
    "hive_runtime": False,
    "autonomous_scheduling": False,
    "autonomous_loop_spawning": False,
    "loop_self_authorized_closure": False,
    "loop_self_assimilation": False,
    "brain_provider_selection": False,
    "world_truth_declaration": False,
    "stale_requirement_direct_invocation": False,
    "post_closure_requirement_invocation": False,
    "cross_loop_local_state_mutation": False,
    "new_cognitive_owner": False,
    "loop_manager": False,
    "loop_planner": False,
}


CLOSURE_DISPOSITION_BY_REASON = {
    "STOP_SUFFICIENT": "COMPLETED",
    "COGNITIVE_CONCERN_RESOLVED": "COMPLETED",
    "INTENT_SUPERSEDED": "SUPERSEDED",
    "TASK_OR_BEHAVIOR_COMPLETED": "COMPLETED",
    "CONTEXT_INVALIDATED_CONCERN": "STOPPED",
    "BRAIN_GOVERNED_STOP": "STOPPED",
    "RESOURCE_VALUE_TOO_LOW": "ABANDONED_BY_VALUE",
    "CONTINUITY_STALE": "SUPERSEDED",
    "UNRECOVERABLE_CAPABILITY_GAP": "FAILED",
    "SAFETY_GOVERNED_TERMINATION": "STOPPED",
    "PARENT_SUPERSEDED_BY_BRANCH_OR_MERGE": "SUPERSEDED",
}


def _check(name: str, actual: bool) -> Tuple[str, bool]:
    return name, actual


def _base_result(spec: LifecycleClosureScenarioSpecV1):
    base_spec = next(item for item in build_loop_scenario_specs_v1() if item.scenario_id == spec.base_scenario_id)
    return run_loop_scenario(base_spec)


def _requirement_dispositions(spec: LifecycleClosureScenarioSpecV1, loop) -> Tuple[Tuple[str, str], ...]:
    refs = spec.outstanding_requirements or loop.requirement_refs
    disposition = "CLOSED_STALE" if spec.stale_requirement else (
        "NOT_REQUIRED_AFTER_SUFFICIENCY" if spec.closure_reason == "STOP_SUFFICIENT" else "CLOSED"
    )
    return tuple((ref, disposition) for ref in refs)


def _observation_dispositions(spec: LifecycleClosureScenarioSpecV1, loop) -> Tuple[Tuple[str, str], ...]:
    refs = spec.outstanding_observations or loop.observation_refs
    disposition = "NOT_REQUIRED_AFTER_SUFFICIENCY" if spec.closure_reason == "STOP_SUFFICIENT" else "CLOSED"
    return tuple((ref, disposition) for ref in refs)


def _pending_candidate_dispositions(spec: LifecycleClosureScenarioSpecV1, loop) -> Tuple[Tuple[str, str], ...]:
    refs = spec.skipped_candidates or loop.pending_candidate_refs
    disposition = "NOT_REQUIRED_AFTER_SUFFICIENCY" if spec.closure_reason == "STOP_SUFFICIENT" else "DEFERRED"
    return tuple((ref, disposition) for ref in refs)


def _build_package(
    spec: LifecycleClosureScenarioSpecV1,
    loop,
    closure: LoopClosureRecordCandidateV1,
    outcome: CognitiveOutcomeCandidateV1,
    base_result,
) -> LoopPackageCandidateV1:
    reservation = LoopPackageReservationCandidateV1(
        loop_id=loop.loop_id,
        runtime_trace_refs=loop.trace_refs,
        closure_record_ref=f"closure:{loop.loop_id}",
        loop_package_ref=f"loop-package:{loop.loop_id}",
        experience_candidate_ref=f"experience-candidate:{loop.loop_id}",
        future_cognitive_prior_ref=f"future-prior:{loop.loop_id}",
    )
    continuity_refs = tuple(
        getattr(item, "assessment_ref", None)
        or getattr(item, "next_need_reassessment_ref", None)
        or getattr(getattr(item, "resume_candidate", None), "trace_ref", "")
        for item in base_result.continuity_assessments + base_result.resume_assessments
    )
    continuity_refs = (f"continuity-assessment:{loop.loop_id}",) + tuple(ref for ref in continuity_refs if ref)
    pause_refs = tuple(
        ref
        for state in base_result.local_states
        for ref in (state.pause_reason, state.waiting_reason)
        if ref
    )
    return LoopPackageCandidateV1(
        package_ref=reservation.loop_package_ref,
        reservation=reservation,
        loop_id=loop.loop_id,
        cognitive_concern_ref=loop.cognitive_concern_ref,
        parent_loop_ref=f"parent-loop:{spec.scenario_id}" if spec.branch_reservation else None,
        derived_from_ref=f"derived-from:{loop.cognitive_concern_ref}" if spec.branch_reservation else None,
        final_lifecycle_disposition=closure.final_disposition,
        final_state_version_ref=closure.final_state_version_ref,
        need_lineage_refs=closure.need_lineage_refs,
        hypothesis_lineage_refs=closure.hypothesis_lineage_refs,
        evidence_lineage_refs=closure.evidence_refs,
        capability_path_refs=tuple(path.requirement_ref for path in base_result.capability_paths),
        context_refs=loop.context_refs,
        field_refs=loop.field_refs,
        current_world_refs=loop.current_world_refs,
        intent_refs=loop.intent_refs,
        task_behavior_refs=loop.task_behavior_refs,
        role_refs=loop.role_refs,
        perspective_refs=loop.perspective_refs,
        continuity_history_refs=tuple(ref for ref in continuity_refs if ref),
        pause_wait_resume_refs=pause_refs,
        closure_reason=spec.closure_reason,
        cognitive_outcome_ref=outcome.outcome_ref,
        trace_refs=closure.trace_refs,
        provenance_refs=closure.provenance_refs,
    )


def run_lifecycle_closure_scenario(spec: LifecycleClosureScenarioSpecV1) -> ClosureScenarioResultV1:
    base_result = _base_result(spec)
    loop = base_result.loops[0]
    local = base_result.local_states[0]
    reason = spec.closure_reason
    suggested = spec.lifecycle_disposition
    closure_ref = f"closure:{loop.loop_id}"
    assessment = ClosureAssessmentCandidateV1(
        assessment_ref=f"closure-assessment:{loop.loop_id}",
        loop_id=loop.loop_id,
        cognitive_concern_ref=loop.cognitive_concern_ref,
        local_closure_state="OPEN",
        local_state_version_ref=loop.current_state_version_ref,
        current_need_ref=local.current_minimum_need_ref,
        closure_reason=reason,
        local_sufficiency_ref=local.local_sufficiency_ref,
        evidence_refs=loop.evidence_refs,
        outstanding_requirement_refs=tuple(ref for ref, _ in _requirement_dispositions(spec, loop)),
        outstanding_observation_refs=tuple(ref for ref, _ in _observation_dispositions(spec, loop)),
        suggested_lifecycle_disposition=suggested,
        eligible_for_governance=spec.closure_candidate_created,
        closure_candidate_created=spec.closure_candidate_created,
        reason_refs=(f"closure-reason:{reason}",),
    )
    accepted = spec.closure_candidate_created and spec.lifecycle_closure_accepted
    decision = ClosureDecisionCandidateV1(
        decision_ref=f"closure-decision:{loop.loop_id}",
        loop_id=loop.loop_id,
        assessment_ref=assessment.assessment_ref,
        governing_owner_ref="brain:cognitive-flow-governance",
        accepted=accepted,
        lifecycle_disposition=suggested,
        closure_reason=reason,
        acceptance_state_version_ref=loop.current_state_version_ref,
        decision_reason_refs=(f"closure-reason:{reason}",),
    )
    requirements = _requirement_dispositions(spec, loop)
    observations = _observation_dispositions(spec, loop)
    pending_candidates = _pending_candidate_dispositions(spec, loop)
    freeze = None
    if accepted:
        freeze = FinalStateFreezeCandidateV1(
            freeze_ref=f"final-state-freeze:{loop.loop_id}",
            loop_id=loop.loop_id,
            final_state_version_ref=loop.current_state_version_ref,
            current_need_ref=local.current_minimum_need_ref,
            need_lineage_refs=(local.current_minimum_need_ref,) if local.current_minimum_need_ref else (),
            hypothesis_lineage_refs=local.hypothesis_lineage_refs,
            evidence_refs=loop.evidence_refs,
            context_refs=loop.context_refs,
            field_refs=loop.field_refs,
            current_world_refs=loop.current_world_refs,
            intent_refs=loop.intent_refs,
            task_behavior_refs=loop.task_behavior_refs,
            role_refs=loop.role_refs,
            perspective_refs=loop.perspective_refs,
            capability_path_refs=tuple(path.requirement_ref for path in base_result.capability_paths),
            trace_refs=loop.trace_refs,
            provenance_refs=loop.provenance_refs,
            requirement_dispositions=requirements,
            observation_dispositions=observations,
            pending_candidate_dispositions=pending_candidates,
            final_state_frozen=True,
        )
    lifecycle = LifecycleClosureCandidateV1(
        lifecycle_closure_ref=f"lifecycle-closure:{loop.loop_id}",
        loop_id=loop.loop_id,
        source_closure_state="OPEN",
        target_closure_state="CLOSED" if accepted else "OPEN",
        accepted=accepted,
        lifecycle_disposition=suggested,
        closure_reason=reason,
        closure_decision_ref=decision.decision_ref,
        final_state_version_ref=loop.current_state_version_ref,
        final_state_freeze_ref=freeze.freeze_ref if freeze else None,
        outstanding_requirements_disposed=not requirements if not accepted else True,
        outstanding_observations_disposed=not observations if not accepted else True,
    )
    closure = LoopClosureRecordCandidateV1(
        loop_id=loop.loop_id,
        cognitive_concern_ref=loop.cognitive_concern_ref,
        final_disposition=suggested,
        final_state_version_ref=loop.current_state_version_ref,
        need_lineage_refs=(local.current_minimum_need_ref,) if local.current_minimum_need_ref else (),
        hypothesis_lineage_refs=local.hypothesis_lineage_refs,
        evidence_refs=loop.evidence_refs,
        current_world_refs=loop.current_world_refs,
        closure_reason_ref=f"closure-reason:{reason}",
        trace_refs=loop.trace_refs,
        provenance_refs=loop.provenance_refs,
    ) if spec.closure_candidate_created else None
    outcome = None
    package = None
    assimilation = None
    if accepted and closure is not None:
        outcome = CognitiveOutcomeCandidateV1(
            outcome_ref=f"cognitive-outcome:{loop.loop_id}",
            loop_id=loop.loop_id,
            cognitive_concern_ref=loop.cognitive_concern_ref,
            final_disposition=suggested,
            final_state_version_ref=loop.current_state_version_ref,
            closure_record_ref=closure_ref,
            evidence_refs=closure.evidence_refs,
            sufficiency_reason_ref=closure.closure_reason_ref,
            current_world_refs=closure.current_world_refs,
            trace_refs=closure.trace_refs,
            provenance_refs=closure.provenance_refs,
        )
        package = _build_package(spec, loop, closure, outcome, base_result)
        assimilation = BrainAssimilationCandidateV1(
            assimilation_ref=f"brain-assimilation:{loop.loop_id}",
            brain_subject_ref="brain:subject",
            loop_id=loop.loop_id,
            cognitive_outcome_ref=outcome.outcome_ref,
            closure_record_ref=closure_ref,
            disposition=spec.assimilation_disposition or "KEEP_AS_LOCAL_RESULT",
            source_state_version_ref=outcome.final_state_version_ref,
            trace_refs=outcome.trace_refs,
            provenance_refs=outcome.provenance_refs,
        )
    history = HistoryBoundaryCandidateV1(
        history_ref=f"history-boundary:{loop.loop_id}",
        loop_id=loop.loop_id,
        runtime_trace_refs=loop.trace_refs,
        closure_record_ref=closure_ref,
        loop_package_ref=package.package_ref if package else f"loop-package:{loop.loop_id}",
        future_experience_candidate_ref=f"experience-candidate:{loop.loop_id}" if accepted else None,
        runtime_history_preserved=True,
        package_is_bounded_handoff=accepted,
        future_reference_prefers_package=accepted,
        deep_audit_may_reference_trace=True,
    )
    parent_closed_by_reservation = spec.parent_supersede_governed and accepted
    checks = (
        _check("closure_reason_mapped", reason in CLOSURE_REASONS and suggested == CLOSURE_DISPOSITION_BY_REASON.get(reason)),
        _check("closure_candidate_created", assessment.closure_candidate_created),
        _check("closure_record_is_not_acceptance", assessment.candidate_only and not assessment.lifecycle_closure_accepted),
        _check("governance_owns_acceptance", decision.governing_owner_ref == "brain:cognitive-flow-governance"),
        _check("accepted_closure_target", lifecycle.target_closure_state == ("CLOSED" if accepted else "OPEN")),
        _check("accepted_freezes_final_state", (freeze is not None and freeze.final_state_frozen) == accepted),
        _check("final_state_version_preserved", freeze is None or freeze.final_state_version_ref == loop.current_state_version_ref),
        _check("pending_candidates_explicitly_disposed", not accepted or bool(freeze and freeze.pending_candidate_dispositions)),
        _check("requirements_disposed_after_acceptance", not accepted or lifecycle.outstanding_requirements_disposed),
        _check("observations_disposed_after_acceptance", not accepted or lifecycle.outstanding_observations_disposed),
        _check("outcome_requires_accepted_closure", (outcome is not None) == accepted),
        _check("package_requires_accepted_closure", (package is not None) == accepted),
        _check("outcome_candidate_only", outcome is None or outcome.candidate_only),
        _check("outcome_not_world_truth", outcome is None or not outcome.world_truth_declared),
        _check("assimilation_candidate_only", assimilation is None or assimilation.candidate_only),
        _check("assimilation_disposition_mapped", assimilation is None or assimilation.disposition in ASSIMILATION_DISPOSITIONS),
        _check("assimilation_no_mutation", assimilation is None or not any((assimilation.memory_mutation, assimilation.experience_mutation, assimilation.learning_executed, assimilation.intent_mutation))),
        _check("package_traceable", package is None or bool(package.trace_refs and package.provenance_refs and package.cognitive_outcome_ref)),
        _check("history_preserved_without_compression", history.runtime_history_preserved and not history.semantic_compression and not history.history_deleted),
        _check("stale_requirement_not_invocable", not spec.stale_requirement or not accepted or all(disposition == "CLOSED_STALE" for _, disposition in requirements)),
        _check("skipped_candidates_not_failures", not spec.skipped_candidates or suggested == "COMPLETED"),
        _check("branch_reservation_does_not_spawn", not spec.branch_reservation or not base_result.autonomous_loop_spawn),
        _check("branch_reservation_does_not_close_parent", not spec.branch_reservation or spec.parent_supersede_governed or not parent_closed_by_reservation),
        _check("parent_supersede_is_governed", not spec.parent_supersede_governed or parent_closed_by_reservation),
        _check("no_runtime_path", spec.no_runtime and not base_result.runtime_execution),
        _check("no_new_owner", spec.no_new_owner),
    )
    negative_guards = tuple(NEGATIVE_GUARDS.items())
    return ClosureScenarioResultV1(
        scenario_id=spec.scenario_id,
        title=spec.title,
        closure_assessment=assessment,
        closure_decision=decision,
        lifecycle_closure=lifecycle,
        closure_record=closure,
        cognitive_outcome=outcome,
        final_state_freeze=freeze,
        loop_package=package,
        assimilation=assimilation,
        history_boundary=history,
        branch_reservation_present=spec.branch_reservation,
        parent_closed_by_reservation=parent_closed_by_reservation,
        child_loop_runtime_created=False,
        checks=checks,
        negative_guards=negative_guards,
    )


def build_lifecycle_closure_results_v1(
    specs: Iterable[LifecycleClosureScenarioSpecV1],
) -> Tuple[ClosureScenarioResultV1, ...]:
    return tuple(run_lifecycle_closure_scenario(spec) for spec in specs)


__all__ = [
    "PHASE",
    "NEGATIVE_GUARDS",
    "CLOSURE_DISPOSITION_BY_REASON",
    "run_lifecycle_closure_scenario",
    "build_lifecycle_closure_results_v1",
]
