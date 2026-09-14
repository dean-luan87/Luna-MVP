"""Single real YOLO11n invocation plus controlled downstream cognitive cases."""

from __future__ import annotations

from dataclasses import replace
from typing import Any, Iterable, Optional, Tuple

from capabilities.midplatform.core.cognitive_flow.cognitive_dynamic_loop_engine_v1 import (
    DynamicCognitiveFlowEngineV1,
)
from capabilities.midplatform.core.cognitive_flow.cognitive_dynamic_loop_types_v1 import (
    CognitiveEvidenceUpdateCandidateV1,
    CognitiveGoalCandidateV1,
    DynamicCognitiveLoopInputV1,
    ProvisionalPlanCandidateV1,
)
from capabilities.midplatform.core.cognitive_flow.integration.dynamic_flow_semantic_compatibility_cutover_controlled.dynamic_flow_semantic_compatibility_engine_v1 import (
    interpret_for_a,
)
from capabilities.midplatform.core.cognitive_state_formation.current_world_types_v1 import (
    CurrentWorldCandidateV1,
)
from capabilities.midplatform.core.cognitive_state_formation.integration.b2_current_world_cognitive_state_flow_controlled.b2_current_world_cognitive_state_flow_adapter_v1 import (
    run_b2_case,
)
from capabilities.midplatform.core.context_foundation.integration.b1_real_visual_evidence_context_world_controlled.run_b1_real_visual_evidence_context_world_controlled_implementation_v1 import (
    _context_payload,
)
from capabilities.midplatform.core.context_foundation.integration.context_world_state_controlled_integration_engine_v1 import (
    ContextWorldStateControlledIntegrationEngineV1,
)
from capabilities.midplatform.core.observation_gateway.integration.real_visual_evidence_gateway_adapter_v1 import (
    REAL_CONTROLLED_EVIDENCE,
    admit_real_visual_evidence_v1,
)
from capabilities.midplatform.field_perception_orchestrator.integration.field_perception_real_vision_provider_adapter_v1 import (
    build_vision_provider_admission_candidate_v1,
    run_authorized_vision_provider_v1,
)
from capabilities.midplatform.field_perception_orchestrator.integration.yolo11n_single_frame_execution.run_yolo11n_real_single_frame_provider_execution_v1 import (
    ADAPTER_ID,
    DEFAULT_MODEL,
    DEFAULT_SOURCE,
    EVIDENCE_ID,
    GOVERNED_MODEL_PATH,
    MODEL_ASSET_ID,
    _prepare,
)
from capabilities.midplatform.field_perception_orchestrator.integration.yolo11n_single_frame_execution.yolo11n_single_frame_execution_types_v1 import (
    build_single_frame_execution_result_v1,
)
from capabilities.midplatform.model_manager.model_contract_repository.model_contract_repository_resolver_v1 import (
    resolve_model_contract_v1,
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
)
from capabilities.midplatform.model_manager.registries.universal_capability_slot.cognitive_need_capability_requirement_bridge_types_v1 import (
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
from capabilities.midplatform.model_manager.model_contract_repository.yolo11n_external_provisioning.yolo11n_external_provisioning_types_v1 import (
    resolve_yolo11n_external_provisioning_v1,
)

from .real_capability_runtime_admission_compatibility_adapter_v1 import (
    build_runtime_admission_compatibility_v1,
)

from .dynamic_cognitive_flow_real_capability_trial_types_v1 import (
    RealCapabilityInvocationTrialV1,
)


def _need(scenario_id: str, ref: str, state_ref: str) -> CognitiveNeedCandidateV1:
    return CognitiveNeedCandidateV1(
        need_id=ref,
        source_intent_ref=f"intent:{scenario_id}",
        source_context_ref=f"context:{scenario_id}",
        source_field_ref=f"field:{scenario_id}",
        source_hypothesis_ref=f"hypothesis:{scenario_id}:object",
        source_attention_ref=f"attention:{scenario_id}",
        problem_description="detect bounded object evidence in the current frame",
        missing_information_class="object_presence",
        required_evidence_class="object_candidate",
        urgency="NORMAL",
        safety_relevance="NONE",
        state_version_ref=state_ref,
        trace_ref=f"trace:{scenario_id}:need:{ref.rsplit(':', 1)[-1]}",
    )


def _formation(scenario_id: str, need: CognitiveNeedCandidateV1):
    return form_capability_requirement(
        need,
        formation_id=f"{scenario_id}:object-detection",
        problem_class="object_presence",
        requested_operation="DETECT_OBJECT",
        input_contract_ref="image_evidence",
        output_contract_ref="object_candidate",
        requirement_type="OBJECT_DETECTION",
        task_context="current minimum visual evidence need",
        requested_module_id="object_detection",
        permission_refs=("permission:capability-governance",),
        resource_refs=("resource:controlled-real-trial",),
        execution_boundary_ref="Observation Gateway / FPO",
    )


def _capability_chain(formation) -> Tuple[CapabilityScopeAssessmentV1, CapabilityResolutionCandidateV1, CapabilityInvocationCandidateV1]:
    modules = build_scope_modules()
    object_module = next(item for item in modules if item.module_id == "object_detection")
    object_slot = _bind(object_module, _slot("slot:real-trial-object"))
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


def _ensure_b2_cognitive_reference_candidates(
    current_world: CurrentWorldCandidateV1,
    scenario_id: str,
) -> CurrentWorldCandidateV1:
    """Complete the B2 read-only reference envelope without changing B1 evidence.

    B1 Context World output may legitimately omit PCN/Intent references because
    B1 is an evidence-to-world handoff.  The canonical B2 -> Cognitive Flow
    adapter, however, carries both references and the existing Cognitive Flow
    handoff contract requires one of each.  These are candidate references only;
    they do not create or mutate Intent or PCN state.
    """
    pcn_refs = current_world.pcn_refs or (f"pcn:real-trial:{scenario_id}",)
    intent_refs = current_world.intent_refs or (f"intent:real-trial:{scenario_id}",)
    provenance_refs = tuple(
        dict.fromkeys(
            (
                *current_world.provenance_refs,
                f"provenance:b2-reference-bridge:{scenario_id}",
            )
        )
    )
    return replace(
        current_world,
        pcn_refs=pcn_refs,
        intent_refs=intent_refs,
        provenance_refs=provenance_refs,
    )


def build_real_capability_requirement_ref(requirement_ref: str) -> str:
    """Map the governed Need requirement to the provider admission namespace."""
    return f"capability-requirement:{requirement_ref}"


def execute_real_trial_once(
    *,
    requirement_ref: str,
    trial_id: str = "RCT-REAL-01",
    source_ref: str = DEFAULT_SOURCE,
    model_path: str = DEFAULT_MODEL,
    declared_checksum: Optional[str] = None,
    observed_checksum: Optional[str] = None,
    dependency_status: str = "PYTHON_DEPENDENCY_UNRESOLVED",
) -> RealCapabilityInvocationTrialV1:
    """Execute the existing YOLO provider path exactly once."""
    manager, control, raw, frame, _legacy_admission, session = _prepare(
        case_id=trial_id,
        source_ref=source_ref,
        source_mode="REAL",
        model_path=model_path,
        declared_checksum=declared_checksum,
        observed_checksum=observed_checksum,
        dependency_status=dependency_status,
    )
    model_contract = resolve_model_contract_v1(
        {"model_asset_id": MODEL_ASSET_ID},
        deployment_requirements={"dependencies_satisfied": dependency_status == "PYTHON_DEPENDENCY_VERIFIED"},
    )
    need = _need(trial_id, f"need:{trial_id}:1", f"state:real-trial:{trial_id}:v1")
    formation = _formation(trial_id, need)
    runtime_admission = build_runtime_admission_compatibility_v1(
        case_id=trial_id,
        formation=formation,
        source_ref=source_ref,
        model_path=model_path,
        declared_checksum=declared_checksum,
        observed_checksum=observed_checksum,
        dependency_status=dependency_status,
        model_admission=manager,
        model_contract_resolution=model_contract,
    )
    provider_requirement_ref = build_real_capability_requirement_ref(requirement_ref)
    request = control.request
    provider_session = control.provider_session
    provider_admission = build_vision_provider_admission_candidate_v1(
        observation_demand_ref=control.demand.demand_id,
        observation_request_ref=request.request_id if request else "",
        capability_requirement_ref=provider_requirement_ref,
        provider_session_ref=provider_session.session_id if provider_session else "",
        provider_candidate_ref=f"provider-candidate:yolo11n:{trial_id}",
        model_candidate_ref=model_contract.model_asset_id or MODEL_ASSET_ID,
        model_admission_ref=(
            manager.trace_ref
            if runtime_admission.executable is not None
            else ""
        ),
        region_scope_candidate=request.target_region_candidate if request else "",
        expected_evidence=("VISION_DETECTION",),
        bounded=bool(provider_session and provider_session.resource_budget_candidate.get("max_frames") == 1),
        provider_admitted=runtime_admission.executable is not None,
        trace_ref=control.trace.control_trace_ref,
        provenance_refs=tuple(dict.fromkeys((*control.trace.provenance_refs, *manager.provenance_refs, *model_contract.provenance_refs))),
    )
    provider = run_authorized_vision_provider_v1(
        frame,
        provider_admission,
        execute_real_provider=bool(provider_admission.provider_invocation_authorized),
        model_path=model_path,
        seen_inference_ids=(),
    )
    execution = build_single_frame_execution_result_v1(
        manager_admission=manager,
        frame=frame,
        provider=provider,
        provider_adapter_contract_id=ADAPTER_ID,
        evidence_contract_id=EVIDENCE_ID,
        model_load_executed=bool(provider.invocation_performed),
        invocation_count=1 if provider.invocation_performed else 0,
    )
    gateway = None
    b1_context = None
    current_world: Optional[CurrentWorldCandidateV1] = None
    if provider.gateway_handoff is not None and provider.evidence:
        gateway = admit_real_visual_evidence_v1(
            provider.gateway_handoff,
            provider.evidence,
            mode=REAL_CONTROLLED_EVIDENCE,
            observed_at_ref=f"observed:{trial_id}",
            valid_from_ref=f"valid-from:{trial_id}",
        )
        if gateway.gateway_admission and gateway.observation is not None:
            b1_context = ContextWorldStateControlledIntegrationEngineV1().run_case(
                _context_payload(
                    gateway,
                    trial_id,
                    occurred_at=f"occurred:{trial_id}",
                    received_at=f"received:{trial_id}",
                )
            )
            current_world = b1_context.current_world
    trace_refs = tuple(
        dict.fromkeys(
            (
                execution.trace_ref,
                *(execution.provenance_refs or ()),
                *(gateway.trace.reverse_lookup_path if gateway else ()),
                current_world.trace_ref if current_world else "",
            )
        )
    )
    provenance_refs = tuple(
        dict.fromkeys(
            (
                *(execution.provenance_refs or ()),
                *(gateway.trace.provenance_refs if gateway else ()),
                *(current_world.provenance_refs if current_world else ()),
            )
        )
    )
    return RealCapabilityInvocationTrialV1(
        trial_id=trial_id,
        input_source_ref=source_ref,
        requirement_ref=requirement_ref,
        provider_capability_requirement_ref=provider_requirement_ref,
        model_contract_resolution=model_contract,
        model_admission=manager,
        observation_control=control,
        frame=frame,
        provider_admission=provider_admission,
        provider_result=provider,
        execution_result=execution,
        gateway_admission=gateway,
        b1_context_result=b1_context,
        current_world=current_world,
        real_provider_invocation_count=execution.invocation_count,
        single_frame=execution.single_frame,
        evidence_refs=tuple(item.evidence_id for item in provider.evidence),
        trace_refs=trace_refs,
        provenance_refs=provenance_refs,
        logical_resolution_status=runtime_admission.logical_resolution.status,
        runtime_admission_status=runtime_admission.assessment.admission_status,
        executable_capability_created=runtime_admission.executable is not None,
        provider_admission_reached=provider_admission is not None,
        second_provider_invocation=False,
        terminal_readiness_owner=False,
        runtime_admission_bypassed=False,
        executable_candidate_bypassed=runtime_admission.executable is None and provider_admission.provider_invocation_authorized,
        dynamic_flow_semantic_authority=False,
    )


def _goal(scenario_id: str) -> CognitiveGoalCandidateV1:
    return CognitiveGoalCandidateV1(
        goal_ref=f"goal:{scenario_id}",
        goal_statement_candidate="obtain sufficient bounded object evidence from the current visual input",
        success_condition_refs=(f"condition:{scenario_id}:object-evidence",),
        context_refs=(f"context:{scenario_id}",),
        intent_refs=(f"intent:{scenario_id}",),
        trace_ref=f"trace:{scenario_id}:goal",
    )


def _event(scenario_id: str, index: int, source_state: str, evidence_refs: Tuple[str, ...], spec) -> CognitiveEvidenceUpdateCandidateV1:
    sufficient = bool(spec.sufficient_at == index)
    return CognitiveEvidenceUpdateCandidateV1(
        evidence_update_ref=f"evidence-update:{scenario_id}:{index}",
        source_state_version_ref=source_state,
        evidence_refs=evidence_refs or (f"controlled-evidence:{scenario_id}:{index}",),
        evidence_kind="REAL_YOLO11N_VISUAL_DETECTION_CANDIDATE",
        establishes_goal_sufficiency=sufficient,
        invalidates_hypothesis=bool(spec.hypothesis_change and index == spec.update_count),
        replacement_hypothesis_refs=(f"hypothesis:{scenario_id}:alternative",)
        if spec.hypothesis_change and index == spec.update_count
        else (),
        replacement_need_ref=f"need:{scenario_id}:alternative"
        if spec.alternative_need and index == spec.update_count
        else None,
        capability_result_ref=f"controlled-or-real-result:{scenario_id}:{index}",
        execution_outcome="SUCCESS",
        requirement_satisfaction="SATISFIED" if sufficient else "UNSATISFIED",
        task_contribution="CONTRIBUTED" if sufficient else "NO_CONTRIBUTION",
        trace_ref=f"trace:{scenario_id}:evidence:{index}",
    )


def build_dynamic_request(spec, current_world: CurrentWorldCandidateV1, formation, resolution, invocation, evidence_refs: Tuple[str, ...]) -> DynamicCognitiveLoopInputV1:
    state_ref = f"state:{spec.scenario_id}:v1"
    plan_refs = tuple(f"need:{spec.scenario_id}:{index}" for index in range(1, 8))
    need_refs = plan_refs + ((f"need:{spec.scenario_id}:alternative",) if spec.alternative_need else ())
    needs = tuple(_need(spec.scenario_id, ref, state_ref) for ref in need_refs)
    updates = []
    source_state = state_ref
    for index in range(1, spec.update_count + 1):
        updates.append(_event(spec.scenario_id, index, source_state, evidence_refs, spec))
        source_state = f"state:{spec.scenario_id}:v{index + 1}"
    return DynamicCognitiveLoopInputV1(
        scenario_id=spec.scenario_id,
        goal=_goal(spec.scenario_id),
        provisional_plan=ProvisionalPlanCandidateV1(
            plan_ref=f"plan:{spec.scenario_id}",
            goal_ref=f"goal:{spec.scenario_id}",
            candidate_step_refs=plan_refs,
            plan_completeness_status="PROVISIONAL",
            trace_ref=f"trace:{spec.scenario_id}:plan",
        ),
        initial_state_version_ref=state_ref,
        initial_disposition="INSUFFICIENT",
        initial_hypothesis_refs=current_world.active_hypothesis_refs or (f"hypothesis:{spec.scenario_id}:object",),
        initial_minimum_need_ref=plan_refs[0],
        evidence_updates=tuple(updates),
        needs=needs,
        requirements=(formation,),
        resolutions=(resolution,),
        invocations=(invocation,),
    )


def build_scenario_context(spec, trial: RealCapabilityInvocationTrialV1):
    if trial.current_world is None:
        return None
    need = _need(spec.scenario_id, f"need:{spec.scenario_id}:1", f"state:{spec.scenario_id}:v1")
    formation = _formation(spec.scenario_id, need)
    scope, resolution, invocation = _capability_chain(formation)
    b2_input_current_world = _ensure_b2_cognitive_reference_candidates(
        trial.current_world,
        spec.scenario_id,
    )
    b2 = run_b2_case(
        b2_input_current_world,
        spec.scenario_id,
        mode="REAL_B1_CURRENT_WORLD_FROM_YOLO11N",
        engine_scenario_id="S01",
        flow_scenario_id="C01",
    )
    dynamic_request = build_dynamic_request(
        spec,
        b2.state_output.current_world_candidate,
        formation,
        resolution,
        invocation,
        trial.evidence_refs,
    )
    outcome = assess_capability_outcome(
        build_capability_usage_record(
            usage_id=f"usage:{spec.scenario_id}:real-trial",
            module_ref=resolution.module_ref or "object_detection",
            module_version_ref="controlled-resolution:v1",
            slot_ref=resolution.slot_ref,
            invocation_ref=invocation.invocation_id,
            requirement_ref=formation.requirement_ref,
            problem_class=formation.selected_problem_class,
            operation=formation.requested_operation,
            context_refs=tuple(trial.current_world.context_refs),
            task_refs=(),
            trace_refs=trial.trace_refs,
            execution_result_ref=trial.execution_result.trace_ref,
            execution_outcome="SUCCESS" if trial.provider_result.accepted else "FAILURE",
            requirement_satisfaction="SATISFIED" if spec.sufficient_at else "UNSATISFIED",
            task_contribution="CONTRIBUTED" if spec.sufficient_at else "NO_CONTRIBUTION",
        ),
        assessment_id=f"assessment:{spec.scenario_id}:real-trial",
        evidence_refs=trial.evidence_refs,
    )
    dynamic_request = replace(dynamic_request, capability_outcomes=(outcome,))
    dynamic_output = DynamicCognitiveFlowEngineV1().run_case(dynamic_request)
    a_interpretation = interpret_for_a(
        dynamic_output,
        concern_ref=f"concern:{spec.scenario_id}",
        work_ref=f"work:{spec.scenario_id}",
    )
    return {
        "b2": b2,
        "formation": formation,
        "scope": scope,
        "resolution": resolution,
        "invocation": invocation,
        "outcome": outcome,
        "dynamic_request": dynamic_request,
        "dynamic_output": dynamic_output,
        "compatibility_output": a_interpretation.compatibility_output,
        "a_semantic_decisions": a_interpretation.a_decisions,
        "dynamic_flow_semantic_authority": False,
        "dynamic_flow_direct_semantic_consumption": False,
    }


__all__ = [
    "build_real_capability_requirement_ref",
    "build_scenario_context",
    "execute_real_trial_once",
]
