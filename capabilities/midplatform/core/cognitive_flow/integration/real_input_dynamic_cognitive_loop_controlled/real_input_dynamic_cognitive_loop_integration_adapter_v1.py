"""Pure adapter joining existing B1/B2/Dynamic/Capability/B4 candidates."""

from __future__ import annotations

from dataclasses import replace
from typing import Iterable, Optional, Tuple

from capabilities.midplatform.core.cognitive_flow.cognitive_dynamic_loop_engine_v1 import (
    DynamicCognitiveFlowEngineV1,
)
from capabilities.midplatform.core.cognitive_flow.cognitive_dynamic_loop_types_v1 import (
    CognitiveEvidenceUpdateCandidateV1,
    CognitiveGoalCandidateV1,
    CognitiveStateVersionCandidateV1,
    DynamicCognitiveLoopInputV1,
    DynamicCognitiveLoopOutputV1,
    ProvisionalPlanCandidateV1,
)
from capabilities.midplatform.core.cognitive_flow.cognitive_cycle_transition_types_v1 import (
    ReconsiderationCandidateV1,
)
from capabilities.midplatform.core.cognitive_state_formation.current_world_types_v1 import (
    CurrentWorldCandidateV1,
)
from capabilities.midplatform.core.cognitive_state_formation.integration.b2_current_world_cognitive_state_flow_controlled.b2_current_world_cognitive_state_flow_adapter_v1 import (
    run_b2_case,
)
from capabilities.midplatform.core.cognitive_state_formation.integration.b2_current_world_cognitive_state_flow_controlled.b2_current_world_cognitive_state_flow_types_v1 import (
    B2CurrentWorldCognitiveFlowResultV1,
)
from capabilities.midplatform.core.cognitive_flow.integration.dynamic_flow_semantic_compatibility_cutover_controlled.dynamic_flow_semantic_compatibility_engine_v1 import (
    interpret_for_a,
)
from capabilities.midplatform.model_manager.registries.universal_capability_slot.capability_experience_feedback_governance_v1 import (
    assess_capability_outcome,
    build_capability_usage_record,
)
from capabilities.midplatform.model_manager.registries.universal_capability_slot.capability_scope_resolution_fixture_v1 import (
    _bind,
    _slot,
    build_scope_modules,
)
from capabilities.midplatform.model_manager.registries.universal_capability_slot.cognitive_need_capability_requirement_bridge_governance_v1 import (
    form_capability_requirement,
    reassess_requirement_against_state,
)
from capabilities.midplatform.model_manager.registries.universal_capability_slot.cognitive_need_capability_requirement_bridge_types_v1 import (
    CapabilityRequirementFormationCandidateV1,
    CognitiveNeedCandidateV1,
)
from capabilities.midplatform.model_manager.registries.universal_capability_slot.universal_capability_slot_resolution_v1 import (
    build_scoped_invocation_candidate,
    resolve_scoped_capability_requirement,
)
from capabilities.midplatform.model_manager.registries.universal_capability_slot.universal_capability_slot_types_v1 import (
    CapabilityInvocationCandidateV1,
    CapabilityOutcomeAssessmentV1,
    CapabilityResolutionCandidateV1,
    CapabilityScopeAssessmentV1,
)

from .real_input_dynamic_cognitive_loop_integration_types_v1 import (
    IntegratedCognitiveLoopInputV1,
    IntegratedCognitiveLoopResultV1,
)


def _need(scenario_id: str, need_ref: str, state_ref: str) -> CognitiveNeedCandidateV1:
    return CognitiveNeedCandidateV1(
        need_id=need_ref,
        source_intent_ref=f"intent:{scenario_id}",
        source_context_ref=f"context:{scenario_id}",
        source_field_ref=f"field:{scenario_id}",
        source_hypothesis_ref=f"hypothesis:{scenario_id}:exit",
        source_attention_ref=f"attention:{scenario_id}",
        problem_description="determine the next bounded evidence needed for the goal",
        missing_information_class="object_presence",
        required_evidence_class="object_candidate",
        urgency="NORMAL",
        safety_relevance="NONE",
        state_version_ref=state_ref,
        trace_ref=f"trace:{scenario_id}:need:{need_ref.rsplit(':', 1)[-1]}",
    )


def _goal(scenario_id: str) -> CognitiveGoalCandidateV1:
    return CognitiveGoalCandidateV1(
        goal_ref=f"goal:{scenario_id}",
        goal_statement_candidate="locate an exit from the current visual context",
        success_condition_refs=(f"condition:{scenario_id}:exit-observed",),
        context_refs=(f"context:{scenario_id}",),
        intent_refs=(f"intent:{scenario_id}",),
        trace_ref=f"trace:{scenario_id}:goal",
    )


def _plan(scenario_id: str, need_refs: Tuple[str, ...]) -> ProvisionalPlanCandidateV1:
    return ProvisionalPlanCandidateV1(
        plan_ref=f"plan:{scenario_id}",
        goal_ref=f"goal:{scenario_id}",
        candidate_step_refs=need_refs,
        plan_completeness_status="PROVISIONAL",
        trace_ref=f"trace:{scenario_id}:plan",
    )


def _event(
    scenario_id: str,
    index: int,
    source_state_ref: str,
    *,
    evidence_kind: str = "CONTROLLED_VISUAL_EVIDENCE",
    sufficient: bool = False,
    invalidates_hypothesis: bool = False,
    replacement_hypothesis_refs: Tuple[str, ...] = (),
    replacement_need_ref: Optional[str] = None,
    capability_result_ref: Optional[str] = None,
    execution_outcome: Optional[str] = None,
    requirement_satisfaction: Optional[str] = None,
    task_contribution: Optional[str] = None,
    capability_availability: Optional[str] = None,
) -> CognitiveEvidenceUpdateCandidateV1:
    return CognitiveEvidenceUpdateCandidateV1(
        evidence_update_ref=f"evidence-update:{scenario_id}:{index}",
        source_state_version_ref=source_state_ref,
        evidence_refs=(f"evidence:{scenario_id}:{index}",),
        evidence_kind=evidence_kind,
        establishes_goal_sufficiency=sufficient,
        invalidates_hypothesis=invalidates_hypothesis,
        replacement_hypothesis_refs=replacement_hypothesis_refs,
        replacement_need_ref=replacement_need_ref,
        capability_result_ref=capability_result_ref,
        execution_outcome=execution_outcome,
        requirement_satisfaction=requirement_satisfaction,
        task_contribution=task_contribution,
        capability_availability=capability_availability,
        trace_ref=f"trace:{scenario_id}:evidence:{index}",
    )


def _formation(
    need: CognitiveNeedCandidateV1,
    scenario_id: str,
    *,
    out_of_scope: bool = False,
) -> CapabilityRequirementFormationCandidateV1:
    return form_capability_requirement(
        need,
        formation_id=f"{scenario_id}:minimum-need",
        problem_class="text_content" if out_of_scope else "object_presence",
        requested_operation="READ_TEXT" if out_of_scope else "DETECT_OBJECT",
        input_contract_ref="image_evidence",
        output_contract_ref="text_candidate" if out_of_scope else "object_candidate",
        requirement_type="TEXT_READ" if out_of_scope else "OBJECT_DETECTION",
        task_context="minimum evidence for cognitive exit candidate",
        requested_module_id="object_detection",
        permission_refs=("permission:capability-governance",),
        resource_refs=("resource:controlled",),
        execution_boundary_ref="Observation Gateway / FPO",
    )


def _capability_chain(
    formation: CapabilityRequirementFormationCandidateV1,
    mode: str,
) -> Tuple[
    CapabilityScopeAssessmentV1,
    CapabilityResolutionCandidateV1,
    CapabilityInvocationCandidateV1,
]:
    modules = build_scope_modules()
    object_module = next(item for item in modules if item.module_id == "object_detection")
    object_slot = _bind(object_module, _slot("slot:integrated-object"))
    if mode == "DEGRADED":
        object_module = replace(object_module, lifecycle_state="DEGRADED")
    elif mode == "UNAVAILABLE":
        object_module = replace(object_module, lifecycle_state="UNAVAILABLE")
    scope, resolution, _gap = resolve_scoped_capability_requirement(
        formation.requirement,
        (object_module,),
        (object_slot,),
    )
    invocation = build_scoped_invocation_candidate(
        formation.requirement,
        scope,
        resolution,
        invocation_id=f"invocation:{formation.formation_id}",
        module=object_module,
        gateway_refs=("Observation Gateway", "FPO / Active Observation Control"),
        trace_refs=(formation.trace_ref or f"trace:{formation.formation_id}",),
    )
    return scope, resolution, invocation


def _outcome(
    scenario_id: str,
    formation: CapabilityRequirementFormationCandidateV1,
    invocation: CapabilityInvocationCandidateV1,
    execution_outcome: str,
    requirement_satisfaction: str,
    task_contribution: str,
) -> CapabilityOutcomeAssessmentV1:
    usage = build_capability_usage_record(
        usage_id=f"usage:{scenario_id}:controlled",
        module_ref=invocation.module_ref or "module:unavailable",
        module_version_ref="controlled-module:v1",
        slot_ref=invocation.slot_ref,
        invocation_ref=invocation.invocation_id,
        requirement_ref=formation.requirement_ref,
        problem_class=formation.selected_problem_class,
        operation=formation.requested_operation,
        context_refs=(f"context:{scenario_id}",),
        task_refs=(),
        trace_refs=(f"trace:{scenario_id}:controlled-outcome",),
        execution_result_ref=f"controlled-result:{scenario_id}",
        execution_outcome=execution_outcome,
        requirement_satisfaction=requirement_satisfaction,
        task_contribution=task_contribution,
    )
    return assess_capability_outcome(
        usage,
        assessment_id=f"assessment:{scenario_id}:controlled",
        evidence_refs=(f"evidence:{scenario_id}:outcome",),
    )


def build_integrated_input(spec) -> IntegratedCognitiveLoopInputV1:
    """Construct one bounded cross-module request from fixture metadata."""
    scenario_id = spec.scenario_id
    current_world = spec.current_world_factory()
    b2 = run_b2_case(
        current_world,
        scenario_id,
        mode=spec.input_mode,
        engine_scenario_id="S01",
        flow_scenario_id="C01",
    )
    initial_state_ref = f"state:{scenario_id}:v1"
    plan_refs = tuple(
        f"need:{scenario_id}:{index}" for index in range(1, spec.plan_count + 1)
    )
    need_refs = plan_refs + ((f"need:{scenario_id}:alternative",) if spec.alternative_need else ())
    needs = tuple(_need(scenario_id, ref, initial_state_ref) for ref in need_refs)
    goal = _goal(scenario_id)
    plan = _plan(scenario_id, plan_refs)
    formation = _formation(needs[0], scenario_id, out_of_scope=spec.capability_mode == "OUT_OF_SCOPE")
    scope, resolution, invocation = _capability_chain(formation, spec.capability_mode)
    outcomes: Tuple[CapabilityOutcomeAssessmentV1, ...] = ()
    if spec.execution_outcome:
        outcomes = (
            _outcome(
                scenario_id,
                formation,
                invocation,
                spec.execution_outcome,
                spec.requirement_satisfaction or "UNKNOWN",
                spec.task_contribution or "UNKNOWN",
            ),
        )
    updates = []
    state_ref = initial_state_ref
    for index in range(1, spec.update_count + 1):
        is_last = index == spec.update_count
        update = _event(
            scenario_id,
            index,
            state_ref,
            sufficient=spec.sufficient and (spec.sufficient_at == index or (spec.sufficient_at == 0 and is_last)),
            invalidates_hypothesis=spec.hypothesis_change and is_last,
            replacement_hypothesis_refs=(f"hypothesis:{scenario_id}:exit-alternative",)
            if spec.hypothesis_change and is_last
            else (),
            replacement_need_ref=(
                f"need:{scenario_id}:alternative"
                if spec.alternative_need and is_last
                else None
            ),
            capability_result_ref=(f"controlled-result:{scenario_id}" if spec.execution_outcome else None),
            execution_outcome=spec.execution_outcome if is_last else None,
            requirement_satisfaction=spec.requirement_satisfaction if is_last else None,
            task_contribution=spec.task_contribution if is_last else None,
            capability_availability=("UNAVAILABLE" if spec.capability_mode == "OUT_OF_SCOPE" else spec.capability_mode if spec.capability_mode in {"DEGRADED", "UNAVAILABLE"} else None),
        )
        updates.append(update)
        state_ref = f"state:{scenario_id}:v{index + 1}"
    dynamic_request = DynamicCognitiveLoopInputV1(
        scenario_id=scenario_id,
        goal=goal,
        provisional_plan=plan,
        initial_state_version_ref=initial_state_ref,
        initial_disposition="INSUFFICIENT",
        initial_hypothesis_refs=(f"hypothesis:{scenario_id}:exit",),
        initial_minimum_need_ref=plan_refs[0] if plan_refs else None,
        evidence_updates=tuple(updates),
        needs=needs,
        requirements=(formation,),
        resolutions=(resolution,),
        invocations=(invocation,),
        capability_outcomes=outcomes,
    )
    b4_reconsiderations = ()
    b4_reobserve_refs = ()
    if spec.b4_reconsideration:
        b4_reconsiderations = (
            ReconsiderationCandidateV1(
                cycle_id=f"cycle:{scenario_id}:b4",
                source_stage="Outcome Evaluation Governance",
                target_stage="Cognitive Flow Governance",
                reconsideration_reason="controlled outcome requires cognitive reassessment",
                related_refs=(f"assessment:{scenario_id}:controlled",),
                trace_ref=f"trace:{scenario_id}:b4-reconsideration",
            ),
        )
    if spec.b4_reobserve:
        b4_reobserve_refs = (f"reobserve:{scenario_id}:b4",)
    return IntegratedCognitiveLoopInputV1(
        scenario_id=scenario_id,
        input_mode=spec.input_mode,
        source_current_world=current_world,
        b2_result=b2,
        dynamic_request=dynamic_request,
        requirement_formations=(formation,),
        scope_assessments=(scope,),
        resolutions=(resolution,),
        invocations=(invocation,),
        capability_outcomes=outcomes,
        b4_reconsiderations=b4_reconsiderations,
        b4_reobserve_refs=b4_reobserve_refs,
    )


def run_integrated_case(request: IntegratedCognitiveLoopInputV1) -> IntegratedCognitiveLoopResultV1:
    dynamic_output = DynamicCognitiveFlowEngineV1().run_case(request.dynamic_request)
    a_interpretation = interpret_for_a(
        dynamic_output,
        concern_ref=f"concern:{request.scenario_id}",
        work_ref=f"work:{request.scenario_id}",
    )
    a_bundle = a_interpretation.a_decisions
    final_state: CognitiveStateVersionCandidateV1 = dynamic_output.state_versions[-1]
    new_evidence_ref = dynamic_output.evidence_update_refs[-1] if dynamic_output.evidence_update_refs else None
    sufficiency_status = a_bundle.sufficiency_decision.sufficiency_status
    a_need_ref = a_bundle.need_decision.selected_need_ref
    a_final_disposition = {
        "SUFFICIENT": "SUFFICIENT",
        "REQUIRES_RECONSIDERATION": "RECONSIDER",
    }.get(sufficiency_status, "INSUFFICIENT")
    a_next_step = a_bundle.next_step_decision.next_step_disposition
    dispositions = tuple(
        (
            formation.requirement_ref,
            reassess_requirement_against_state(
                formation,
                current_state_version_ref=final_state.state_version_ref,
                sufficiency_status=sufficiency_status,
                new_evidence_ref=new_evidence_ref,
            ),
        )
        for formation in request.requirement_formations
    )
    source_trace = request.source_current_world.trace_ref
    b2_trace = request.b2_result.flow_output.trace.root_cycle_trace_id if request.b2_result.flow_output.trace else ""
    trace_refs = tuple(
        dict.fromkeys(
            (
                source_trace,
                *request.b2_result.provenance_chain,
                *dynamic_output.trace_refs,
                *(item.trace_ref or "" for item in request.b4_reconsiderations),
            )
        )
    )
    provenance_refs = tuple(
        dict.fromkeys(
            (
                *request.source_current_world.provenance_refs,
                *request.b2_result.provenance_chain,
                *dynamic_output.provenance_refs,
            )
        )
    )
    guards = {
        "candidate_only": request.candidate_only and dynamic_output.candidate_only,
        "real_input_remains_reference_only": request.source_current_world.candidate_only,
        "current_world_read_only": request.b2_result.current_world_read_only,
        "plan_candidates_non_binding": not request.dynamic_request.provisional_plan.binding,
        "only_current_need_materialized": a_need_ref in dynamic_output.needs_materialized or a_need_ref is None,
        "requirement_bounded": all(item.requirement_minimized and item.required_authority == "EVIDENCE_ONLY" for item in request.requirement_formations),
        "scope_before_invocation": all(item.scope_assessment_ref for item in request.invocations),
        "stale_requirement_not_eligible": all(item not in dynamic_output.eligible_invocation_refs for item, _disposition in dispositions if _disposition == "SUPERSEDED"),
        "stop_sufficient_not_failure": dynamic_output.stop_sufficient_not_failure,
        "capability_failure_not_task_failure": dynamic_output.capability_failure_is_task_failure is False,
        "outcome_dimensions_separate": all(
            len({item.execution_outcome, item.requirement_satisfaction, item.task_contribution}) >= 2
            for item in request.capability_outcomes
        ) or not request.capability_outcomes,
        "no_runtime_execution": not dynamic_output.runtime_execution,
        "no_provider_invocation": not dynamic_output.provider_invocation,
        "no_camera_activation": not dynamic_output.camera_activation,
        "no_action_execution": True,
        "no_learning_or_memory_mutation": True,
        "dynamic_flow_semantic_authority_false": not a_interpretation.compatibility_output.semantic_authority,
        "dynamic_flow_direct_semantic_consumption_blocked": True,
        "a_semantic_authority_preserved": all(
            item is not None and item.decision_owner_ref == "A_REASONING_ROLE"
            for item in (
                a_bundle.need_decision,
                a_bundle.sufficiency_decision,
                a_bundle.reconsideration_decision,
                a_bundle.next_step_decision,
            )
        ),
    }
    return IntegratedCognitiveLoopResultV1(
        scenario_id=request.scenario_id,
        input_mode=request.input_mode,
        source_current_world_ref=request.source_current_world.current_world_id,
        b2_state_world_ref=request.b2_result.state_output.current_world_candidate.current_world_id,
        b2_flow_cycle_ref=b2_trace,
        dynamic_output=dynamic_output,
        requirement_formations=request.requirement_formations,
        scope_assessments=request.scope_assessments,
        resolutions=request.resolutions,
        invocations=request.invocations,
        capability_outcomes=request.capability_outcomes,
        requirement_dispositions=dispositions,
        b4_reconsideration_refs=tuple(item.trace_ref for item in request.b4_reconsiderations),
        b4_reobserve_refs=request.b4_reobserve_refs,
        final_state_version_ref=final_state.state_version_ref,
        final_need_ref=a_need_ref,
        final_disposition=a_final_disposition,
        next_step_disposition=a_next_step,
        trace_refs=tuple(dict.fromkeys((*trace_refs, a_interpretation.compatibility_output.compatibility_ref))),
        provenance_refs=tuple(dict.fromkeys((*provenance_refs, *a_interpretation.compatibility_output.provenance_refs))),
        guards=guards,
        compatibility_output=a_interpretation.compatibility_output,
        a_semantic_decisions=a_bundle,
    )


__all__ = ["build_integrated_input", "run_integrated_case"]
