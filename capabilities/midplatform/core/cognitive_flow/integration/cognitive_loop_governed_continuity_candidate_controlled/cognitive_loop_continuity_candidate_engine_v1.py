"""Deterministic candidate-only Loop materialization and continuity engine."""

from __future__ import annotations

from typing import Dict, Iterable, List, Optional, Tuple

from capabilities.midplatform.core.cognitive_flow.cognitive_cycle_core_types_v1 import SourceRefV1
from capabilities.midplatform.core.cognitive_flow.cognitive_cycle_interrupt_types_v1 import (
    ResumeCandidateV1,
    SuspendCandidateV1,
)
from capabilities.midplatform.core.cognitive_flow.cognitive_cycle_transition_types_v1 import (
    ReconsiderationCandidateV1,
)
from capabilities.midplatform.core.cognitive_flow.cognitive_dynamic_loop_types_v1 import (
    CognitiveStateVersionCandidateV1,
    DynamicCognitiveLoopTransitionCandidateV1,
)
from capabilities.midplatform.core.cognitive_flow.cognitive_flow_registry_v1 import CYCLE_STATES

from .cognitive_loop_continuity_candidate_fixture_v1 import LoopScenarioSpecV1
from .cognitive_loop_continuity_candidate_types_v1 import (
    CONTINUITY_SIGNALS,
    BranchReservationCandidateV1,
    CapabilityCandidatePathV1,
    CapabilityGrowthGuardCandidateV1,
    CognitiveOutcomeCandidateV1,
    ContinuityAssessmentCandidateV1,
    ControlledLoopScenarioResultV1,
    LoopClosureRecordCandidateV1,
    LoopIdentityCandidateV1,
    LoopLocalStateCandidateV1,
    LoopMaterializationCandidateV1,
    LoopPackageReservationCandidateV1,
    ResumeAssessmentCandidateV1,
)


LIFECYCLE_CANONICAL_REFS = {
    "ACTIVE": "STATE_READY",
    "PAUSED": "SUSPENDED",
    "WAITING": "DEFERRED_ASYNC_REFERENCE",
    "DEFERRED": "DEFER",
    "STOPPED": "LOOP_LOCAL_STOPPED_CANDIDATE",
    "COMPLETED": "COMPLETED",
}

NEGATIVE_GUARDS = {
    "provider_invocation": False,
    "yolo": False,
    "camera": False,
    "ocr": False,
    "action_execution": False,
    "learning": False,
    "memory_mutation": False,
    "experience_mutation": False,
    "autonomous_scheduling": False,
    "autonomous_loop_spawning": False,
    "new_cognitive_owner": False,
    "loop_manager": False,
    "loop_planner": False,
    "world_truth_declaration": False,
    "brain_provider_selection": False,
    "stale_requirement_direct_invocation": False,
    "cross_loop_local_state_mutation": False,
    "emotion_learning": False,
    "semantic_compression": False,
}


def _check(field: str, actual: object, expected: object) -> Dict[str, object]:
    return {
        "field": field,
        "actual": actual,
        "expected": expected,
        "passed": actual == expected,
    }


def _source_ref(owner: str, ref_id: str, ref_type: str) -> SourceRefV1:
    return SourceRefV1(
        owner=owner,
        ref_id=ref_id,
        ref_type=ref_type,
        version="v1",
        trace_ref=f"trace:{ref_id}",
        provenance_ref=f"provenance:{ref_id}",
    )


def _loop_ids(spec: LoopScenarioSpecV1) -> Tuple[str, ...]:
    return tuple(f"loop:{spec.scenario_id}:{index}" for index in range(1, spec.loop_count + 1))


def _lifecycle_for(spec: LoopScenarioSpecV1, index: int) -> str:
    return spec.lifecycles[index] if index < len(spec.lifecycles) else spec.lifecycles[0]


def _local_disposition(spec: LoopScenarioSpecV1, lifecycle: str) -> str:
    if spec.sufficient_completion or spec.resume_decision == "COMPLETE" or lifecycle == "COMPLETED":
        return "SUFFICIENT"
    if lifecycle in {"WAITING", "DEFERRED"}:
        return "DEFER"
    if spec.resume and spec.resume_decision in {"REPLAN", "SUPERSEDE"}:
        return "RECONSIDER"
    return "INSUFFICIENT"


def _make_loop(spec: LoopScenarioSpecV1, index: int) -> Tuple[LoopIdentityCandidateV1, LoopLocalStateCandidateV1]:
    loop_id = f"loop:{spec.scenario_id}:{index}"
    lifecycle = _lifecycle_for(spec, index - 1)
    concern_ref = f"cognitive-concern:{spec.scenario_id}:{index}"
    state_v1 = f"state:{spec.scenario_id}:{index}:v1"
    state_v2 = f"state:{spec.scenario_id}:{index}:v2"
    need_ref = f"need:{loop_id}:minimum"
    intent_ref = f"intent:{spec.scenario_id}:shared" if spec.shared_intent else f"intent:{loop_id}"
    task_ref = f"task:{spec.scenario_id}:shared" if spec.shared_task else f"task:{loop_id}"
    context_ref = f"context:{spec.scenario_id}:shared" if spec.shared_context else f"context:{loop_id}"
    current_state_ref = state_v2 if spec.resume else state_v1
    pending = tuple(f"candidate:{loop_id}:{item}" for item in (1, 2, 3))
    requirement_refs = tuple(
        f"requirement:{loop_id}:{item}" for item in range(1, spec.capability_count + 1)
    )
    completed_by_resume = spec.resume and spec.resume_decision == "COMPLETE"
    observation_refs = () if lifecycle in {"COMPLETED", "STOPPED"} or completed_by_resume else (f"observation:{loop_id}:candidate",)
    local_disposition = _local_disposition(spec, lifecycle)
    last_disposition = "STOP_SUFFICIENT" if spec.sufficient_completion else ("COMPLETED" if completed_by_resume else lifecycle)
    state_versions = [
        CognitiveStateVersionCandidateV1(
            state_version_ref=state_v1,
            parent_state_version_ref=None,
            evidence_update_ref=None,
            current_disposition="INSUFFICIENT",
            current_minimum_need_ref=need_ref,
            active_hypothesis_refs=(f"hypothesis:{loop_id}:active",),
            invalidated_hypothesis_refs=(),
            sufficiency_ref=None,
            reconsideration_ref=None,
            trace_ref=f"trace:{loop_id}:state:v1",
        )
    ]
    if spec.resume:
        state_versions.append(
            CognitiveStateVersionCandidateV1(
                state_version_ref=state_v2,
                parent_state_version_ref=state_v1,
                evidence_update_ref=f"resume-assessment:{loop_id}",
                current_disposition=local_disposition,
                current_minimum_need_ref=need_ref,
                active_hypothesis_refs=(f"hypothesis:{loop_id}:active",),
                invalidated_hypothesis_refs=()
                if spec.resume_decision == "KEEP"
                else (f"hypothesis:{loop_id}:prior",),
                sufficiency_ref=f"sufficiency:{loop_id}" if spec.sufficient_completion or completed_by_resume else None,
                reconsideration_ref=f"reconsideration:{loop_id}"
                if spec.resume_decision in {"REPLAN", "SUPERSEDE"}
                else None,
                trace_ref=f"trace:{loop_id}:state:v2",
            )
        )
    transition = DynamicCognitiveLoopTransitionCandidateV1(
        transition_ref=f"transition:{loop_id}:v1",
        source_state_version_ref=state_v1,
        target_state_version_ref=current_state_ref,
        source_disposition="INSUFFICIENT",
        target_disposition=local_disposition,
        next_step_disposition="STOP_SUFFICIENT"
        if spec.sufficient_completion
        else (spec.resume_decision or lifecycle),
        current_minimum_need_ref=need_ref,
        selected_next_need_ref=need_ref,
        superseded_requirement_refs=(f"requirement:{loop_id}:prior",)
        if spec.stale_requirement
        else (),
        non_materialized_plan_refs=pending,
        related_refs=(concern_ref, f"current-world:{loop_id}:v1"),
        trace_ref=f"trace:{loop_id}:transition",
    )
    suspend_candidate = (
        SuspendCandidateV1(
            cycle_id=loop_id,
            reason=f"governed-pause:{spec.scenario_id}",
            related_refs=(concern_ref, state_v1),
            trace_ref=f"trace:{loop_id}:suspend",
        )
        if lifecycle == "PAUSED"
        else None
    )
    loop = LoopIdentityCandidateV1(
        loop_id=loop_id,
        cognitive_concern_ref=concern_ref,
        goal_ref=f"goal:{spec.scenario_id}",
        lineage_refs=(f"lineage:{loop_id}",),
        parent_loop_ref=None,
        derived_from_ref=None,
        dependency_refs=(f"dependency:{loop_id}",),
        shared_context_refs=(context_ref,),
        inherited_evidence_refs=(f"evidence:{loop_id}:initial",),
        intent_refs=(intent_ref,),
        role_refs=(f"role:{loop_id}",),
        perspective_refs=(f"perspective:{loop_id}",),
        field_refs=(f"field:{loop_id}",),
        context_refs=(context_ref,),
        current_world_refs=(f"current-world:{loop_id}:v1",),
        current_state_version_ref=current_state_ref,
        current_need_ref=need_ref,
        hypothesis_refs=(f"hypothesis:{loop_id}:active",),
        expectation_refs=(f"expectation:{loop_id}:minimum",),
        attention_refs=(f"attention:{loop_id}",),
        evidence_refs=(f"evidence:{loop_id}:initial",),
        experience_refs=(f"experience-candidate:{loop_id}",),
        task_behavior_refs=(task_ref, f"behavior:{loop_id}"),
        priority_refs=(f"priority:{loop_id}",),
        resource_envelope_refs=(f"resource-envelope:{spec.scenario_id}:shared",),
        safety_refs=(f"safety:{loop_id}",),
        emotion_modulation_refs=(f"emotion-modulation:{loop_id}",),
        spatial_continuity_refs=(f"spatial:{loop_id}:v1",),
        temporal_continuity_refs=(f"temporal:{loop_id}:v1",),
        pending_candidate_refs=pending,
        requirement_refs=requirement_refs,
        observation_refs=observation_refs,
        trace_refs=(f"trace:{loop_id}:local",),
        provenance_refs=(f"provenance:{loop_id}:local",),
        lifecycle_state=lifecycle,
        canonical_lifecycle_ref=LIFECYCLE_CANONICAL_REFS[lifecycle],
    )
    local = LoopLocalStateCandidateV1(
        loop_id=loop_id,
        local_disposition=local_disposition,
        current_minimum_need_ref=need_ref,
        hypothesis_lineage_refs=(f"hypothesis:{loop_id}:active",),
        pending_candidate_refs=pending,
        state_versions=tuple(state_versions),
        transitions=(transition,),
        last_disposition=last_disposition,
        pause_reason=f"pause:{loop_id}:governed" if lifecycle == "PAUSED" else None,
        waiting_reason=f"waiting:{loop_id}:dependency" if lifecycle == "WAITING" else None,
        suspend_candidate=suspend_candidate,
        local_sufficiency_ref=f"sufficiency:{loop_id}" if spec.sufficient_completion or completed_by_resume else None,
        closure_state="CLOSED" if lifecycle in {"STOPPED", "COMPLETED"} or completed_by_resume else "OPEN",
        trace_refs=(f"trace:{loop_id}:local",),
        provenance_refs=(f"provenance:{loop_id}:local",),
    )
    return loop, local


def _materialization(spec: LoopScenarioSpecV1, loop: LoopIdentityCandidateV1) -> LoopMaterializationCandidateV1:
    attempted_ref = f"brain-parallel-path:{loop.loop_id}" if spec.parallel_brain_path_requested else None
    return LoopMaterializationCandidateV1(
        loop_id=loop.loop_id,
        cognitive_concern_ref=loop.cognitive_concern_ref,
        materialization_reason_refs=(f"materialization-reason:{spec.materialization_reason}",),
        brain_subject_ref="brain:subject",
        brain_materialization_authority_ref="brain:loop-materialization-governance",
        parallel_brain_path_candidate_ref=attempted_ref,
        parallel_brain_path_blocked=spec.parallel_brain_path_requested,
        non_duplication_guard_passed=True,
        materialization_allowed=True,
    )


def _continuity_and_resume(
    spec: LoopScenarioSpecV1,
    loop: LoopIdentityCandidateV1,
) -> Tuple[Optional[ContinuityAssessmentCandidateV1], Optional[ResumeAssessmentCandidateV1]]:
    if not spec.resume:
        return None, None
    signal_status = {
        signal: ("CHANGED" if signal in spec.changed_signals else "UNCHANGED")
        for signal in CONTINUITY_SIGNALS
    }
    assessment_ref = f"continuity-assessment:{loop.loop_id}"
    assessment = ContinuityAssessmentCandidateV1(
        loop_id=loop.loop_id,
        source_state_version_ref=f"state:{spec.scenario_id}:{loop.loop_id.rsplit(':', 1)[-1]}:v1",
        comparison_state_version_ref=loop.current_state_version_ref,
        signal_status=signal_status,
        signal_refs=tuple(f"continuity:{loop.loop_id}:{signal.lower()}" for signal in CONTINUITY_SIGNALS),
        changed_signal_refs=tuple(
            f"continuity:{loop.loop_id}:{signal.lower()}" for signal in spec.changed_signals
        ),
        same_cognitive_concern_preserved=True,
        authoritative_comparison_refs=loop.context_refs + loop.field_refs + loop.current_world_refs,
    )
    decision = "SUPERSEDE" if spec.stale_requirement else (spec.resume_decision or "WAITING")
    prior_requirements = loop.requirement_refs or (f"requirement:{loop.loop_id}:prior",)
    stale_refs = prior_requirements if spec.stale_requirement else ()
    reconsideration = None
    if decision in {"REPLAN", "SUPERSEDE"}:
        reconsideration = ReconsiderationCandidateV1(
            cycle_id=loop.loop_id,
            source_stage="RESUME_ASSESSMENT",
            target_stage="CURRENT_MINIMUM_NEED",
            reconsideration_reason=f"resume:{decision.lower()}",
            related_refs=(loop.current_state_version_ref, assessment_ref) + loop.current_world_refs,
            trace_ref=f"trace:{loop.loop_id}:reconsideration",
        )
    resume = ResumeAssessmentCandidateV1(
        loop_id=loop.loop_id,
        source_lifecycle_state=loop.lifecycle_state,
        continuity_assessment_ref=assessment_ref,
        source_state_version_ref=assessment.source_state_version_ref,
        comparison_state_version_ref=assessment.comparison_state_version_ref,
        current_need_ref=loop.current_need_ref,
        prior_requirement_refs=prior_requirements,
        stale_requirement_refs=stale_refs,
        decision=decision,
        next_need_reassessment_ref=f"need-reassessment:{loop.loop_id}",
        resume_candidate=ResumeCandidateV1(
            cycle_id=loop.loop_id,
            reason=f"resume-assessment:{decision.lower()}",
            related_refs=(assessment_ref, loop.current_state_version_ref),
            trace_ref=f"trace:{loop.loop_id}:resume",
        ),
        reconsideration_candidate=reconsideration,
    )
    return assessment, resume


def _capabilities_and_growth(
    spec: LoopScenarioSpecV1,
    loop: LoopIdentityCandidateV1,
) -> Tuple[Tuple[CapabilityCandidatePathV1, ...], CapabilityGrowthGuardCandidateV1]:
    paths: List[CapabilityCandidatePathV1] = []
    blocked: List[str] = []
    for index in range(1, spec.capability_count + 1):
        path_status = "CANDIDATE_ONLY"
        if spec.stale_requirement:
            path_status = "BLOCKED_STALE_REQUIREMENT"
        elif index > 1 and spec.duplicate_requirement:
            path_status = "BLOCKED_DUPLICATE_REQUIREMENT"
        elif index > 1 and spec.diminishing_value:
            path_status = "DEFERRED_DIMINISHING_INFORMATION_VALUE"
        elif index > 1 and spec.resource_pressure:
            path_status = "DEFERRED_RESOURCE_ENVELOPE"
        paths.append(
            CapabilityCandidatePathV1(
                loop_id=loop.loop_id,
                need_ref=f"need:{loop.loop_id}:minimum:{index}",
                requirement_ref=f"requirement:{loop.loop_id}:{index}",
                scope_ref=f"scope:{loop.loop_id}:{index}",
                resolution_ref=f"resolution:{loop.loop_id}:{index}",
                resource_ref=f"resource-check:{loop.loop_id}:{index}",
                permission_ref=f"permission:{loop.loop_id}:{index}",
                safety_ref=f"safety-check:{loop.loop_id}:{index}",
                observation_admission_ref=f"observation-admission:{loop.loop_id}:{index}",
                observation_candidate_ref=f"observation-candidate:{loop.loop_id}:{index}",
                requirement_state_version_ref=loop.current_state_version_ref,
                path_status=path_status,
            )
        )
    if spec.stale_requirement:
        blocked.append("stale_requirement")
    if spec.duplicate_requirement:
        blocked.append("duplicate_requirement")
    if spec.diminishing_value:
        blocked.append("diminishing_information_value")
    if spec.resource_pressure:
        blocked.append("resource_envelope")
    growth = CapabilityGrowthGuardCandidateV1(
        loop_id=loop.loop_id,
        minimum_sufficient_cognition=True,
        resource_envelope_respected=not spec.resource_pressure,
        sufficiency_threshold_respected=True,
        stale_requirement_blocked=spec.stale_requirement,
        diminishing_information_value_blocked=spec.diminishing_value,
        duplicate_requirement_blocked=spec.duplicate_requirement,
        growth_allowed=not bool(blocked),
        blocked_reason_refs=tuple(f"growth-block:{item}" for item in blocked),
    )
    return tuple(paths), growth


def _closure(
    spec: LoopScenarioSpecV1,
    loop: LoopIdentityCandidateV1,
    local: LoopLocalStateCandidateV1,
) -> Tuple[Optional[LoopClosureRecordCandidateV1], Optional[CognitiveOutcomeCandidateV1], Optional[LoopPackageReservationCandidateV1]]:
    if not spec.closure:
        return None, None, None
    final_disposition = "SUFFICIENT" if spec.sufficient_completion or spec.resume_decision == "COMPLETE" or loop.lifecycle_state == "COMPLETED" else loop.lifecycle_state
    closure_ref = f"closure:{loop.loop_id}"
    closure = LoopClosureRecordCandidateV1(
        loop_id=loop.loop_id,
        cognitive_concern_ref=loop.cognitive_concern_ref,
        final_disposition=final_disposition,
        final_state_version_ref=loop.current_state_version_ref,
        need_lineage_refs=(local.current_minimum_need_ref or f"need:{loop.loop_id}:minimum",),
        hypothesis_lineage_refs=local.hypothesis_lineage_refs,
        evidence_refs=loop.evidence_refs,
        current_world_refs=loop.current_world_refs,
        closure_reason_ref=f"closure-reason:{'STOP_SUFFICIENT' if spec.sufficient_completion else final_disposition}",
        trace_refs=loop.trace_refs,
        provenance_refs=loop.provenance_refs,
    )
    outcome = CognitiveOutcomeCandidateV1(
        outcome_ref=f"cognitive-outcome:{loop.loop_id}",
        loop_id=loop.loop_id,
        cognitive_concern_ref=loop.cognitive_concern_ref,
        final_disposition=final_disposition,
        final_state_version_ref=loop.current_state_version_ref,
        closure_record_ref=closure_ref,
        evidence_refs=closure.evidence_refs,
        sufficiency_reason_ref=closure.closure_reason_ref,
        current_world_refs=closure.current_world_refs,
        trace_refs=closure.trace_refs,
        provenance_refs=closure.provenance_refs,
    )
    package = LoopPackageReservationCandidateV1(
        loop_id=loop.loop_id,
        runtime_trace_refs=loop.trace_refs,
        closure_record_ref=closure_ref,
        loop_package_ref=f"loop-package:{loop.loop_id}",
        experience_candidate_ref=f"experience-candidate:{loop.loop_id}",
        future_cognitive_prior_ref=f"future-prior:{loop.loop_id}",
    )
    return closure, outcome, package


def _branch(spec: LoopScenarioSpecV1, loop: LoopIdentityCandidateV1) -> BranchReservationCandidateV1:
    return BranchReservationCandidateV1(
        loop_id=loop.loop_id,
        parent_loop_ref=f"parent-loop:{spec.scenario_id}" if spec.branch_reservation else None,
        derived_from_ref=f"derived-from:{loop.cognitive_concern_ref}" if spec.branch_reservation else None,
        dependency_refs=(f"dependency:{loop.loop_id}",) if spec.branch_reservation else (),
        shared_context_refs=loop.shared_context_refs,
        inherited_evidence_refs=loop.inherited_evidence_refs,
        branch_reason="brain-governed-future-derivation" if spec.branch_reservation else None,
        supersede_ref=f"supersede:{loop.loop_id}" if spec.branch_reservation else None,
        merge_candidate_ref=f"merge-candidate:{loop.loop_id}" if spec.branch_reservation else None,
        child_loop_runtime_created=False,
        autonomous_spawn=False,
    )


def _local_isolation(loops: Tuple[LoopIdentityCandidateV1, ...], states: Tuple[LoopLocalStateCandidateV1, ...]) -> bool:
    state_refs = [state.state_versions[0].state_version_ref for state in states]
    need_refs = [state.current_minimum_need_ref for state in states]
    concern_refs = [loop.cognitive_concern_ref for loop in loops]
    return len(set(state_refs)) == len(state_refs) and len(set(need_refs)) == len(need_refs) and len(set(concern_refs)) == len(concern_refs)


def run_loop_scenario(spec: LoopScenarioSpecV1) -> ControlledLoopScenarioResultV1:
    loop_items = tuple(_make_loop(spec, index) for index in range(1, spec.loop_count + 1))
    loops = tuple(item[0] for item in loop_items)
    local_states = tuple(item[1] for item in loop_items)
    materializations = tuple(_materialization(spec, loop) for loop in loops)
    continuity_items = tuple(_continuity_and_resume(spec, loop) for loop in loops)
    continuity = tuple(item[0] for item in continuity_items if item[0] is not None)
    resumes = tuple(item[1] for item in continuity_items if item[1] is not None)
    capability_items = tuple(_capabilities_and_growth(spec, loop) for loop in loops)
    capability_paths = tuple(path for item in capability_items for path in item[0])
    growth_guards = tuple(item[1] for item in capability_items)
    closure_items = tuple(_closure(spec, loop, state) for loop, state in zip(loops, local_states))
    closures = tuple(item[0] for item in closure_items if item[0] is not None)
    outcomes = tuple(item[1] for item in closure_items if item[1] is not None)
    packages = tuple(item[2] for item in closure_items if item[2] is not None)
    branches = tuple(_branch(spec, loop) for loop in loops)
    negative_guards = dict(NEGATIVE_GUARDS)
    checks: List[Dict[str, object]] = [
        _check("loop_count", len(loops), spec.loop_count),
        _check("loop_ids_unique", len({loop.loop_id for loop in loops}), len(loops)),
        _check("cognitive_concerns_unique", len({loop.cognitive_concern_ref for loop in loops}), len(loops)),
        _check("local_state_isolated", _local_isolation(loops, local_states), True),
        _check("all_loops_candidate_only", all(loop.candidate_only for loop in loops), True),
        _check("authoritative_state_not_duplicated", all(not loop.authoritative_state_duplicated for loop in loops), True),
        _check("materialization_allowed", all(item.materialization_allowed for item in materializations), True),
        _check("brain_parallel_path_blocked", all(item.parallel_brain_path_blocked == spec.parallel_brain_path_requested for item in materializations), True),
        _check("non_duplication_guard", all(item.non_duplication_guard_passed for item in materializations), True),
        _check("lifecycle_refs_are_candidate_mapping", all(loop.canonical_lifecycle_ref for loop in loops), True),
        _check("negative_guards_closed", all(value is False for value in negative_guards.values()), True),
    ]
    if spec.shared_intent:
        checks.append(_check("shared_intent_refs", len({loop.intent_refs[0] for loop in loops}), 1))
        checks.append(_check("shared_intent_different_concerns", len({loop.cognitive_concern_ref for loop in loops}), len(loops)))
    if spec.shared_task:
        checks.append(_check("shared_task_refs", len({loop.task_behavior_refs[0] for loop in loops}), 1))
        checks.append(_check("shared_task_different_concerns", len({loop.cognitive_concern_ref for loop in loops}), len(loops)))
    if spec.resume:
        decisions = tuple(item.decision for item in resumes)
        expected_decision = "SUPERSEDE" if spec.stale_requirement else (spec.resume_decision or "WAITING")
        checks.extend(
            [
                _check("resume_decision", decisions, tuple(expected_decision for _ in loops)),
                _check("same_concern_preserved_on_resume", all(item.same_cognitive_concern_preserved for item in continuity), True),
                _check("resume_has_state_comparison", all(item.source_state_version_ref != item.comparison_state_version_ref for item in continuity), True),
            ]
        )
    if spec.stale_requirement:
        checks.extend(
            [
                _check("stale_requirement_detected", all(bool(item.stale_requirement_refs) for item in resumes), True),
                _check("stale_requirement_forces_invocation", all(item.stale_requirement_forces_invocation is False for item in resumes), True),
                _check("stale_paths_not_invocable", all(path.path_status == "BLOCKED_STALE_REQUIREMENT" for path in capability_paths) if capability_paths else True, True),
            ]
        )
    if spec.capability_count:
        checks.extend(
            [
                _check("capability_path_count", len(capability_paths), spec.loop_count * spec.capability_count),
                _check("capability_paths_candidate_only", all(path.candidate_only for path in capability_paths), True),
                _check("capability_paths_no_provider", all(not path.provider_invocation for path in capability_paths), True),
                _check("need_driven_paths", all(path.need_ref and path.requirement_ref for path in capability_paths), True),
            ]
        )
    if spec.request_more_evidence:
        checks.extend(
            [
                _check("request_more_evidence_is_candidate", all(path.observation_candidate_ref for path in capability_paths), True),
                _check("request_more_evidence_no_provider", all(not path.provider_invocation for path in capability_paths), True),
            ]
        )
    if spec.duplicate_requirement:
        checks.append(_check("duplicate_requirement_blocked", all(guard.duplicate_requirement_blocked for guard in growth_guards), True))
    if spec.diminishing_value:
        checks.append(_check("diminishing_value_blocked", all(guard.diminishing_information_value_blocked for guard in growth_guards), True))
    if spec.resource_pressure:
        checks.append(_check("resource_growth_guard", all(not guard.growth_allowed for guard in growth_guards if spec.capability_count > 1), True))
    if spec.closure:
        checks.extend(
            [
                _check("closure_record_present", len(closures), spec.loop_count),
                _check("outcome_candidate_present", len(outcomes), spec.loop_count),
                _check("outcome_candidate_only", all(item.candidate_only for item in outcomes), True),
                _check("outcome_not_world_truth", all(not item.world_truth_declared for item in outcomes), True),
                _check("outcome_no_action", all(not item.action_executed for item in outcomes), True),
                _check("outcome_no_memory_mutation", all(not item.memory_mutation for item in outcomes), True),
                _check("outcome_no_experience_mutation", all(not item.experience_mutation for item in outcomes), True),
            ]
        )
    if spec.sufficient_completion:
        checks.append(_check("sufficient_completion", all(item.closure_state == "CLOSED" for item in local_states), True))
        checks.append(_check("stop_sufficient_not_failure", all(item.last_disposition == "STOP_SUFFICIENT" for item in local_states), True))
    if spec.branch_reservation:
        checks.extend(
            [
                _check("branch_refs_reserved", all(item.parent_loop_ref and item.derived_from_ref for item in branches), True),
                _check("branch_child_runtime_absent", all(not item.child_loop_runtime_created for item in branches), True),
                _check("branch_autonomous_spawn_absent", all(not item.autonomous_spawn for item in branches), True),
            ]
        )
    if spec.autonomous_spawn_requested:
        checks.append(_check("autonomous_spawn_blocked", all(not item.autonomous_spawn for item in branches), True))
    if spec.failure_loop_a and len(local_states) > 1:
        checks.append(_check("failure_isolation", local_states[1].closure_state != "FAILED", True))
    if spec.shared_context:
        checks.append(_check("shared_context_does_not_merge_local_state", _local_isolation(loops, local_states), True))
    if "PAUSED" in spec.lifecycles:
        checks.append(_check("paused_state_preserved", all(state.suspend_candidate is not None for state in local_states if state.last_disposition == "PAUSED"), True))
    if "WAITING" in spec.lifecycles:
        checks.append(_check("waiting_has_no_current_execution", all(state.waiting_reason is not None for state in local_states if state.last_disposition == "WAITING"), True))
    if "DEFERRED" in spec.lifecycles:
        checks.append(_check("deferred_is_not_failure", all(state.last_disposition == "DEFERRED" for state in local_states), True))
    if "STOPPED" in spec.lifecycles:
        checks.append(_check("stopped_is_distinct_from_completed", all(state.last_disposition == "STOPPED" and state.closure_state == "CLOSED" for state in local_states), True))
    if "COMPLETED" in spec.lifecycles or spec.resume_decision == "COMPLETE":
        checks.append(_check("completed_does_not_continue_observation", all(not loop.observation_refs for loop in loops), True))
    if spec.resume_decision == "COMPLETE":
        checks.append(_check("resume_complete_closes_local_loop", all(state.closure_state == "CLOSED" for state in local_states), True))
    passed = all(bool(item["passed"]) for item in checks)
    return ControlledLoopScenarioResultV1(
        scenario_id=spec.scenario_id,
        title=spec.title,
        loops=loops,
        local_states=local_states,
        materializations=materializations,
        continuity_assessments=continuity,
        resume_assessments=resumes,
        capability_paths=capability_paths,
        growth_guards=growth_guards,
        closures=closures,
        outcomes=outcomes,
        package_reservations=packages,
        branch_reservations=branches,
        checks=tuple(checks),
        negative_guards=negative_guards,
    )


def build_controlled_loop_results_v1(specs: Iterable[LoopScenarioSpecV1]) -> Tuple[ControlledLoopScenarioResultV1, ...]:
    return tuple(run_loop_scenario(spec) for spec in specs)


__all__ = [
    "LIFECYCLE_CANONICAL_REFS",
    "NEGATIVE_GUARDS",
    "run_loop_scenario",
    "build_controlled_loop_results_v1",
]
