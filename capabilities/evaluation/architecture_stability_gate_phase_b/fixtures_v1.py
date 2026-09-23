"""Owner-issued controlled world fixtures for Phase B temporal scenarios.

This module deliberately builds the world through existing production owner
APIs.  It does not write an owner store, choose currentness, or construct a
positive grant/authorization result directly.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from itertools import count
from typing import Any, Tuple

from capabilities.evaluation.provider_binding_runtime_preparation_responsibility_controlled.fixtures_v1 import (
    PROBLEM,
    STATE,
)
from capabilities.evaluation.perception_provider_runtime_target_preparation_controlled.fixtures_v1 import (
    build_provider_runtime_target_preparation_cases_v1,
)
from capabilities.midplatform.core.action_governance.action_admission_governance_v1 import (
    ACTION_ADMISSION_PROFILE_CONTROLLED_EVALUATION_V1,
    admit_action_v1,
)
from capabilities.midplatform.core.action_governance.action_governance_engine_v1 import (
    ActionGovernanceEngineV1,
    form_runtime_safety_prerequisite_v1,
)
from capabilities.midplatform.core.action_governance.action_io_types_v1 import (
    ActionGovernanceInputV1,
)
from capabilities.midplatform.core.brain_governance.concern_governance_v1 import (
    BRAIN_CONTROLLED_PROFILE_REF,
    admit_concern,
)
from capabilities.midplatform.core.brain_governance.cognitive_grant_governance_v1 import (
    issue_cognitive_grant,
)
from capabilities.midplatform.core.cognitive_flow.integration.a_working_envelope_cognitive_requirement_bridge_controlled.a_working_envelope_cognitive_requirement_engine_v1 import (
    build_working_envelope,
)
from capabilities.midplatform.core.cognitive_flow.integration.a_working_envelope_cognitive_requirement_bridge_controlled.working_envelope_governance_v1 import (
    WORKING_ENVELOPE_PROFILE_CONTROLLED_EVALUATION_V1,
    admit_working_envelope_v1,
)
from capabilities.midplatform.core.cognitive_flow.integration.decision_to_task_manager_controlled_handoff.engine_v1 import (
    build_decision_task_run_v1,
)
from capabilities.midplatform.core.cognitive_flow.integration.task_to_action_boundary_controlled_handoff.engine_v1 import (
    _action_request,
    _build_task_to_action_handoff,
)
from capabilities.midplatform.core.cognitive_state_formation import (
    issue_cognitive_state_version_v1,
)
from capabilities.midplatform.core.cognitive_state_formation.cognitive_state_formation_core_types_v1 import (
    SourceRefV1,
)
from capabilities.midplatform.core.cognitive_state_formation.cognitive_state_formation_engine_v1 import (
    CognitiveStateFormationEngineV1,
)
from capabilities.midplatform.core.cognitive_state_formation.cognitive_state_formation_io_types_v1 import (
    CognitiveStateFormationInputV1,
)
from capabilities.midplatform.core.cognitive_state_formation.cognitive_state_formation_registry_v1 import (
    COGNITIVE_STATE_PROFILE_CONTROLLED_EVALUATION_V1,
)
from capabilities.midplatform.core.runtime_executor.runtime_allocation_preparation_candidate_v1 import (
    ExecutionInstancePreparationInputV1,
    RuntimeAllocationPreparationInputV1,
    form_execution_instance_preparation_candidates,
    form_runtime_allocation_preparation_candidates,
)
from capabilities.midplatform.permission_and_admission_manager.module.runtime_execution_grant_v1 import (
    AUTHORITY_REF,
    OWNER,
    RESPONSIBILITY_REF,
    RuntimeExecutionGrantInputV1,
    build_pregrant_authority_binding_key,
    form_runtime_execution_grants,
)
from capabilities.midplatform.provider_runtime_governance.provider_binding_candidate_v1 import (
    ProviderBindingCandidateInputV1,
    form_provider_binding_candidates,
)
from capabilities.midplatform.provider_runtime_governance.provider_binding_runtime_preparation_v1 import (
    ProviderBindingRuntimePreparationInputV1,
    form_provider_binding_runtime_preparation_candidates,
)
from capabilities.midplatform.provider_runtime_governance.provider_runtime_target_preparation_v1 import (
    form_provider_runtime_target_candidates,
)
from capabilities.midplatform.protocol_manager.module.governance_verification_backbone_v1 import (
    PROTOCOL_SOURCE_REF,
)


_BUILD_COUNTER = count(1)

_CSTATE_SCENARIO_ID_BY_PHASE_B = {
    "B01_STABLE_AUTHORIZED_EFFECT": "S01",
    "B02_ACTION_REVOKED_AFTER_AUTHORIZATION": "S02",
    "B03_WORKING_ENVELOPE_INVALIDATED_AFTER_AUTHORIZATION": "S03",
    "B04_COGNITIVE_GRANT_REVOKED_AFTER_AUTHORIZATION": "S04",
    "B05_CONCERN_SUPERSEDED_AFTER_AUTHORIZATION": "S05",
    "B06_SAFETY_INVALIDATED_AFTER_AUTHORIZATION": "S06",
    "B07_RUNTIME_AUTHORIZATION_INVALIDATED": "S07",
}


@dataclass(frozen=True)
class TemporalAuthorityFixtureV1:
    scenario_id: str
    concern: Any
    cognitive_grant: Any
    state_version: Any
    envelope: Any
    admitted_action: Any
    target: Any
    binding: Any
    allocation: Any
    execution: Any
    runtime_safety_binding_key: Tuple[str, ...]
    runtime_safety: Any
    grant: Any

    @property
    def runtime_scope(self) -> Tuple[str, str, str]:
        return (
            self.admitted_action.admitted_action_ref,
            self.envelope.envelope_ref,
            self.envelope.envelope_version_ref,
        )


def _required(value: Any, label: str) -> Any:
    if value is None:
        raise RuntimeError(f"Phase B owner-issued fixture failed: {label}")
    return value


def _source_ref(owner: str, value: str) -> SourceRefV1:
    return SourceRefV1(owner, value, "v1", f"trace:{value}", f"provenance:{value}")


def _cstate_scenario_id(phase_b_scenario_id: str) -> str:
    phase_b_id = phase_b_scenario_id.split(":instance:", 1)[0]
    try:
        return _CSTATE_SCENARIO_ID_BY_PHASE_B[phase_b_id]
    except KeyError as exc:
        raise RuntimeError(
            f"Phase B CState scenario mapping missing: {phase_b_id}"
        ) from exc


def _owner_issued_canonical_records(scenario_id: str) -> tuple[Any, Any, Any, Any, Any]:
    concern = _required(
        admit_concern(
            request_ref=f"phase-b:request:{scenario_id}",
            goal_ref=f"phase-b:goal:{scenario_id}",
            intent_ref=f"phase-b:intent:{scenario_id}",
            scope_ref=f"phase-b:scope:{scenario_id}",
            basis_refs=(f"phase-b:basis:{scenario_id}",),
            policy_refs=(f"phase-b:policy:{scenario_id}",),
            profile_ref=BRAIN_CONTROLLED_PROFILE_REF,
        ),
        "Concern",
    )
    cognitive_grant = _required(
        issue_cognitive_grant(
            concern_ref=concern.concern_ref,
            receiver_ref=f"phase-b:receiver:{scenario_id}",
            receiver_role="A_REASONING_ROLE",
            granted_authority_refs=("REALITY_REASONING",),
            work_ref=f"phase-b:work:{scenario_id}",
            scope_ref=f"phase-b:scope:{scenario_id}",
            expiry_ref=f"phase-b:expiry:{scenario_id}",
            basis_refs=(f"phase-b:grant-basis:{scenario_id}",),
            policy_refs=(f"phase-b:grant-policy:{scenario_id}",),
            profile_ref=BRAIN_CONTROLLED_PROFILE_REF,
        ),
        "Cognitive Grant",
    )
    state = CognitiveStateFormationEngineV1().run_case(
        CognitiveStateFormationInputV1(
            scenario_id=_cstate_scenario_id(scenario_id),
            context_refs=(_source_ref("Context", f"phase-b:context:{scenario_id}"),),
            pcn_refs=(_source_ref("PCN", f"phase-b:pcn:{scenario_id}"),),
            intent_refs=(_source_ref("Intent", f"phase-b:intent:{scenario_id}"),),
            field_refs=(_source_ref("Field", f"phase-b:field:{scenario_id}"),),
            observation_refs=(_source_ref("Observation", f"phase-b:observation:{scenario_id}"),),
            evidence_refs=(_source_ref("Evidence", f"phase-b:evidence:{scenario_id}"),),
            goal_refs=(_source_ref("Goal", f"phase-b:goal:{scenario_id}"),),
            concern_refs=(_source_ref("Concern", concern.concern_ref),),
            information_need_refs=(_source_ref("Need", f"phase-b:need:{scenario_id}"),),
            task_refs=(_source_ref("Task", f"phase-b:task:{scenario_id}"),),
            role_refs=(_source_ref("Role", f"phase-b:role:{scenario_id}"),),
            relation_refs=(_source_ref("Field", f"phase-b:relation:{scenario_id}"),),
            candidate_only=True,
            synthetic_only=True,
        )
    )
    state_version = _required(
        issue_cognitive_state_version_v1(
            state,
            profile_ref=COGNITIVE_STATE_PROFILE_CONTROLLED_EVALUATION_V1,
        ),
        "Cognitive State Version",
    )
    envelope = _required(
        admit_working_envelope_v1(
            build_working_envelope(
                work_ref=f"phase-b:work:{scenario_id}",
                concern_ref=concern.concern_ref,
                authority_grant_ref=cognitive_grant.grant_ref,
                source_state_version_ref=state_version.version_ref,
                goal_refs=(f"phase-b:goal:{scenario_id}",),
                context_refs=(f"phase-b:context:{scenario_id}",),
                current_world_refs=(f"phase-b:world:{scenario_id}:v1",),
                field_refs=(f"phase-b:field:{scenario_id}",),
            ),
            profile_ref=WORKING_ENVELOPE_PROFILE_CONTROLLED_EVALUATION_V1,
        ),
        "Working Envelope",
    )
    task_summary = build_decision_task_run_v1(
        f"phase-b:action-runtime:{scenario_id}",
        working_envelope=envelope,
    )
    task_case = next(
        item for item in task_summary["cases"] if item["case_id"] == "CASE_A_SUFFICIENT_STOP"
    )
    task_handoff, errors = _build_task_to_action_handoff(
        {**task_case, "resource_state": "available"}
    )
    if errors or task_handoff is None:
        raise RuntimeError(f"Phase B owner-issued fixture failed: Task→Action ({errors})")
    action_request = _action_request(task_handoff)
    action_request["scenario_id"] = f"phase-b:action-runtime:{scenario_id}"
    action_output = ActionGovernanceEngineV1().run_case(
        ActionGovernanceInputV1(**action_request)
    )
    action_safety = form_runtime_safety_prerequisite_v1(
        binding_key=(
            action_output.action_candidate.action_candidate_id,
            task_handoff.task_state_ref,
            task_handoff.decision_candidate_ref,
            envelope.envelope_ref,
            envelope.envelope_version_ref,
            "controlled-observation",
        ),
        effect_class="controlled-observation",
        scope_kind="ACTION_ADMISSION",
    )
    admitted_action = _required(
        admit_action_v1(
            action_output,
            task_handoff=task_handoff,
            working_envelope_ref=envelope.envelope_ref,
            working_envelope_version_ref=envelope.envelope_version_ref,
            safety_prerequisite=action_safety,
            profile_ref=ACTION_ADMISSION_PROFILE_CONTROLLED_EVALUATION_V1,
        ),
        "Canonical Admitted Action",
    )
    return concern, cognitive_grant, state_version, envelope, admitted_action


def build_temporal_authority_fixture(scenario_id: str) -> TemporalAuthorityFixtureV1:
    """Build one complete owner-issued runtime chain for one scenario."""

    public_scenario_id = scenario_id
    scenario_id = f"{scenario_id}:instance:{next(_BUILD_COUNTER)}"
    concern, cognitive_grant, state_version, envelope, admitted_action = (
        _owner_issued_canonical_records(scenario_id)
    )
    target_source_case = build_provider_runtime_target_preparation_cases_v1()[0]
    admitted_action_ref, envelope_ref, envelope_version_ref = (
        admitted_action.admitted_action_ref,
        envelope.envelope_ref,
        envelope.envelope_version_ref,
    )
    target_request = replace(
        target_source_case.request,
        preparation_ref=f"phase-b-target:{scenario_id}",
        trace_ref=f"trace:phase-b-target:{scenario_id}",
        provenance_refs=(f"provenance:phase-b-target:{scenario_id}",),
        admitted_action_ref=admitted_action_ref,
        working_envelope_ref=envelope_ref,
        working_envelope_version_ref=envelope_version_ref,
    )
    target_preparation = form_provider_runtime_target_candidates(target_request)
    if not target_preparation.targets:
        raise RuntimeError(
            "Phase B target preparation failed: "
            f"{target_preparation.validation_errors}"
        )
    target = form_provider_binding_runtime_preparation_candidates(
        ProviderBindingRuntimePreparationInputV1(
            preparation_ref=f"phase-b-binding-prep:{scenario_id}",
            parent_cognitive_problem_ref=target_preparation.parent_cognitive_problem_ref,
            source_state_ref=target_preparation.source_state_ref,
            provider_target_candidates=target_preparation.targets,
            context_refs=target_preparation.context_refs,
            trace_ref=f"trace:phase-b-binding-prep:{scenario_id}",
            provenance_refs=(f"provenance:phase-b-binding-prep:{scenario_id}",),
            admitted_action_ref=admitted_action_ref,
            working_envelope_ref=envelope_ref,
            working_envelope_version_ref=envelope_version_ref,
        )
    )
    if not target.candidates:
        raise RuntimeError(f"Phase B binding preparation failed: {target.validation_errors}")
    target = replace(
        target,
        candidates=tuple(
            replace(
                item,
                provider_candidate_ref="provider_openvins",
                capability_candidate_ref="spatial_mapping",
                capability_class_ref="capability-class:spatial-mapping",
            )
            for item in target.candidates
        ),
    )
    binding = form_provider_binding_candidates(
        ProviderBindingCandidateInputV1(
            preparation_ref=f"phase-b-binding:{scenario_id}",
            parent_cognitive_problem_ref=target.parent_cognitive_problem_ref,
            source_state_ref=target.source_state_ref,
            preparation_candidates=target.candidates,
            context_refs=target.context_refs,
            trace_ref=f"trace:phase-b-binding:{scenario_id}",
            provenance_refs=(f"provenance:phase-b-binding:{scenario_id}",),
            runtime_requirement_refs=(f"phase-b:runtime-requirement:{scenario_id}",),
            resource_class_refs=(f"phase-b:resource-class:{scenario_id}",),
            execution_class_refs=(f"phase-b:execution-class:{scenario_id}",),
            admitted_action_ref=admitted_action_ref,
            working_envelope_ref=envelope_ref,
            working_envelope_version_ref=envelope_version_ref,
        )
    )
    if not binding.candidates:
        raise RuntimeError(f"Phase B binding preparation failed: {binding.validation_errors}")
    binding_candidate = replace(
        binding.candidates[0],
        provider_candidate_ref="provider_openvins",
        capability_candidate_ref="spatial_mapping",
        capability_class_ref="capability-class:spatial-mapping",
        admitted_action_ref=admitted_action_ref,
        working_envelope_ref=envelope_ref,
        working_envelope_version_ref=envelope_version_ref,
    )
    binding = replace(binding, candidates=(binding_candidate,))
    allocation = form_runtime_allocation_preparation_candidates(
        RuntimeAllocationPreparationInputV1(
            preparation_ref=f"phase-b-allocation:{scenario_id}",
            parent_cognitive_problem_ref=binding.parent_cognitive_problem_ref,
            source_state_ref=binding.source_state_ref,
            provider_binding_candidates=(binding_candidate,),
            context_refs=target.context_refs,
            trace_ref=f"trace:phase-b-allocation:{scenario_id}",
            provenance_refs=(f"provenance:phase-b-allocation:{scenario_id}",),
            admitted_action_ref=admitted_action_ref,
            working_envelope_ref=envelope_ref,
            working_envelope_version_ref=envelope_version_ref,
        )
    )
    if not allocation.candidates:
        raise RuntimeError(f"Phase B allocation preparation failed: {allocation.validation_errors}")
    allocation_candidate = replace(
        allocation.candidates[0],
        provider_candidate_ref=binding_candidate.provider_candidate_ref,
        capability_candidate_ref=binding_candidate.capability_candidate_ref,
        capability_class_ref=binding_candidate.capability_class_ref,
        admitted_action_ref=admitted_action_ref,
        working_envelope_ref=envelope_ref,
        working_envelope_version_ref=envelope_version_ref,
    )
    allocation = replace(allocation, candidates=(allocation_candidate,))
    execution = form_execution_instance_preparation_candidates(
        ExecutionInstancePreparationInputV1(
            preparation_ref=f"phase-b-execution:{scenario_id}",
            parent_cognitive_problem_ref=allocation.parent_cognitive_problem_ref,
            source_state_ref=allocation.source_state_ref,
            runtime_allocation_candidates=(allocation_candidate,),
            runtime_envelope_shape_refs=(f"phase-b:runtime-envelope:{scenario_id}",),
            context_refs=target.context_refs,
            trace_ref=f"trace:phase-b-execution:{scenario_id}",
            provenance_refs=(f"provenance:phase-b-execution:{scenario_id}",),
            admitted_action_ref=admitted_action_ref,
            working_envelope_ref=envelope_ref,
            working_envelope_version_ref=envelope_version_ref,
        )
    )
    if not execution.candidates:
        raise RuntimeError(f"Phase B execution preparation failed: {execution.validation_errors}")
    execution_candidate = replace(
        execution.candidates[0],
        provider_candidate_ref=binding_candidate.provider_candidate_ref,
        capability_candidate_ref=binding_candidate.capability_candidate_ref,
        capability_class_ref=binding_candidate.capability_class_ref,
        admitted_action_ref=admitted_action_ref,
        working_envelope_ref=envelope_ref,
        working_envelope_version_ref=envelope_version_ref,
    )
    execution = replace(execution, candidates=(execution_candidate,))
    binding_key = build_pregrant_authority_binding_key(
        execution_instance_preparation_candidate_ref=execution_candidate.execution_instance_preparation_candidate_ref,
        provider_candidate_ref=binding_candidate.provider_candidate_ref,
        capability_candidate_ref=binding_candidate.capability_candidate_ref,
        admitted_action_ref=admitted_action_ref,
        working_envelope_ref=envelope_ref,
        working_envelope_version_ref=envelope_version_ref,
    )
    effect_class = "runtime-execution"
    runtime_safety_binding_key = (*binding_key, effect_class)
    runtime_safety = form_runtime_safety_prerequisite_v1(
        binding_key=runtime_safety_binding_key,
        effect_class=effect_class,
    )
    grant_result = form_runtime_execution_grants(
        RuntimeExecutionGrantInputV1(
            grant_request_ref=f"phase-b-grant:{scenario_id}",
            parent_cognitive_problem_ref=execution.parent_cognitive_problem_ref,
            source_state_ref=execution.source_state_ref,
            provider_binding_candidates=(binding_candidate,),
            runtime_allocation_candidates=(allocation_candidate,),
            execution_instance_preparation_candidates=(execution_candidate,),
            permission_refs=(f"phase-b:permission:{scenario_id}",),
            safety_refs=(f"phase-b:safety:{scenario_id}",),
            protocol_refs=(PROTOCOL_SOURCE_REF,),
            governance_refs=(f"phase-b:governance:{scenario_id}",),
            constraint_refs=(f"phase-b:constraint:{scenario_id}",),
            validity_scope=(f"phase-b:scope:{scenario_id}",),
            expiry_boundary_ref=f"phase-b:expiry:{scenario_id}",
            safety_prerequisite_ref=runtime_safety.result_ref,
            effect_class=effect_class,
            context_refs=target.context_refs,
            lineage_refs=tuple(
                dict.fromkeys(
                    ref
                    for candidate in (binding_candidate,)
                    for ref in candidate.lineage_refs
                )
            ),
            provenance_refs=(f"provenance:phase-b-grant:{scenario_id}",),
            trace_ref=f"trace:phase-b-grant:{scenario_id}",
            grant_authority_ref=AUTHORITY_REF,
            grant_responsibility_ref=RESPONSIBILITY_REF,
            admitted_action_ref=admitted_action_ref,
            working_envelope_ref=envelope_ref,
            working_envelope_version_ref=envelope_version_ref,
        )
    )
    grant = next(
        (item for item in grant_result.decisions if item.decision == "GRANTED"),
        None,
    )
    if grant is None:
        raise RuntimeError(
            f"Phase B runtime grant formation failed: {grant_result.validation_errors}"
        )
    return TemporalAuthorityFixtureV1(
        scenario_id=public_scenario_id,
        concern=concern,
        cognitive_grant=cognitive_grant,
        state_version=state_version,
        envelope=envelope,
        admitted_action=admitted_action,
        target=target,
        binding=binding,
        allocation=allocation,
        execution=execution,
        runtime_safety_binding_key=runtime_safety_binding_key,
        runtime_safety=runtime_safety,
        grant=grant,
    )


__all__ = ["TemporalAuthorityFixtureV1", "build_temporal_authority_fixture"]
