"""Positive regression for the GPT6-G01 provider authorization boundary."""

from dataclasses import replace
from types import SimpleNamespace

from capabilities.midplatform.field_perception_orchestrator.integration.field_perception_real_vision_evidence_types_v1 import (
    CAPABILITY_KIND,
)
from capabilities.midplatform.field_perception_orchestrator.integration.field_perception_real_vision_provider_adapter_v1 import (
    build_vision_provider_admission_candidate_v1,
    run_authorized_vision_provider_v1,
)
import capabilities.midplatform.core.provider_runtime_to_observation_ingress.real_provider_execution_engine_v1 as real_provider_engine_module
from capabilities.midplatform.core.provider_runtime_to_observation_ingress.fixtures_v1 import (
    build_provider_observation_cases_v1,
)
from capabilities.midplatform.core.provider_runtime_to_observation_ingress.real_provider_execution_engine_v1 import (
    RealProviderExecutionEngineV1,
)
from capabilities.midplatform.field_perception_orchestrator.integration.raw_camera_stream_types_v1 import (
    RawFrameRecordV1,
)
from capabilities.evaluation.runtime_grant_pre_execution_authorization_controlled.fixtures_v1 import (
    build_runtime_grant_cases_v1,
)
from capabilities.midplatform.core.runtime_executor.runtime_allocation_preparation_candidate_v1 import (
    ExecutionInstancePreparationInputV1,
    RuntimeAllocationPreparationInputV1,
    form_execution_instance_preparation_candidates,
    form_runtime_allocation_preparation_candidates,
)
from capabilities.midplatform.permission_and_admission_manager.module.runtime_execution_grant_v1 import (
    RuntimeExecutionGrantInputV1,
    build_pregrant_authority_binding_key,
    form_runtime_execution_grants,
    invalidate_runtime_authorization_state,
)
from capabilities.midplatform.core.action_governance.action_governance_engine_v1 import (
    ActionGovernanceEngineV1,
    form_runtime_safety_prerequisite_v1,
)
from capabilities.midplatform.core.action_governance.action_admission_governance_v1 import (
    ACTION_ADMISSION_PROFILE_PRODUCTION_CANONICAL,
    admit_action_v1,
)
from capabilities.midplatform.core.action_governance.action_io_types_v1 import (
    ActionGovernanceInputV1,
)
from capabilities.midplatform.core.brain_governance.concern_governance_v1 import (
    BRAIN_PRODUCTION_PROFILE_REF,
    admit_concern,
)
from capabilities.midplatform.core.brain_governance.cognitive_grant_governance_v1 import (
    issue_cognitive_grant,
)
from capabilities.midplatform.core.cognitive_flow.integration.a_working_envelope_cognitive_requirement_bridge_controlled.a_working_envelope_cognitive_requirement_engine_v1 import (
    build_working_envelope,
)
from capabilities.midplatform.core.cognitive_flow.integration.a_working_envelope_cognitive_requirement_bridge_controlled.working_envelope_governance_v1 import (
    WORKING_ENVELOPE_PROFILE_PRODUCTION_CANONICAL,
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
    COGNITIVE_STATE_PROFILE_PRODUCTION_CANONICAL,
)
from capabilities.midplatform.provider_runtime_governance.provider_binding_candidate_v1 import (
    ProviderBindingCandidateInputV1,
    form_provider_binding_candidates,
)
from capabilities.midplatform.provider_runtime_governance.provider_binding_runtime_preparation_v1 import (
    ProviderBindingRuntimePreparationInputV1,
    form_provider_binding_runtime_preparation_candidates,
)


def _owner_issued_grant_from_public_api():
    """Form one owner-issued grant through production public APIs."""

    case = build_runtime_grant_cases_v1()[0]
    scope = "real-provider-authority"
    concern = admit_concern(
        request_ref=f"request:{scope}",
        goal_ref=f"goal:{scope}",
        intent_ref=f"intent:{scope}",
        scope_ref=f"scope:{scope}",
        basis_refs=(f"basis:{scope}",),
        policy_refs=(f"policy:{scope}",),
        profile_ref=BRAIN_PRODUCTION_PROFILE_REF,
    )
    assert concern is not None
    cognitive_grant = issue_cognitive_grant(
        concern_ref=concern.concern_ref,
        receiver_ref=f"receiver:{scope}",
        receiver_role="A_REASONING_ROLE",
        granted_authority_refs=("REALITY_REASONING",),
        work_ref=f"work:{scope}",
        scope_ref=f"scope:{scope}",
        expiry_ref=f"expiry:{scope}",
        basis_refs=(f"grant-basis:{scope}",),
        policy_refs=(f"grant-policy:{scope}",),
        profile_ref=BRAIN_PRODUCTION_PROFILE_REF,
    )
    assert cognitive_grant is not None

    def _ref(owner: str, value: str) -> SourceRefV1:
        return SourceRefV1(owner, value, "v1", f"trace:{value}", f"provenance:{value}")

    state = CognitiveStateFormationEngineV1().run_case(
        CognitiveStateFormationInputV1(
            scenario_id="F09",
            context_refs=(_ref("Context", f"context:{scope}"),),
            pcn_refs=(_ref("PCN", f"pcn:{scope}"),),
            intent_refs=(_ref("Intent", f"intent:{scope}"),),
            field_refs=(_ref("Field", f"field:{scope}"),),
            observation_refs=(_ref("Observation", f"observation:{scope}"),),
            evidence_refs=(_ref("Evidence", f"evidence:{scope}"),),
            goal_refs=(_ref("Goal", f"goal:{scope}"),),
            concern_refs=(_ref("Concern", f"concern:{scope}"),),
            information_need_refs=(_ref("Need", f"need:{scope}"),),
            task_refs=(_ref("Task", f"task:{scope}"),),
            role_refs=(_ref("Role", f"role:{scope}"),),
            relation_refs=(_ref("Field", f"relation:{scope}"),),
            candidate_only=True,
            synthetic_only=True,
        )
    )
    state_version = issue_cognitive_state_version_v1(
        state,
        profile_ref=COGNITIVE_STATE_PROFILE_PRODUCTION_CANONICAL,
    )
    assert state_version is not None
    envelope = admit_working_envelope_v1(
        build_working_envelope(
            work_ref=f"work:{scope}",
            concern_ref=concern.concern_ref,
            authority_grant_ref=cognitive_grant.grant_ref,
            source_state_version_ref=state_version.version_ref,
            goal_refs=(f"goal:{scope}",),
            context_refs=(f"context:{scope}",),
            current_world_refs=(f"world:{scope}:v1",),
            field_refs=(f"field:{scope}",),
        ),
        profile_ref=WORKING_ENVELOPE_PROFILE_PRODUCTION_CANONICAL,
    )
    assert envelope is not None
    task_summary = build_decision_task_run_v1(
        f"action-runtime:{scope}",
        working_envelope=envelope,
    )
    task_case = next(
        item for item in task_summary["cases"] if item["case_id"] == "CASE_A_SUFFICIENT_STOP"
    )
    task_handoff, errors = _build_task_to_action_handoff(
        {**task_case, "resource_state": "available"}
    )
    assert not errors and task_handoff is not None
    action_request = _action_request(task_handoff)
    action_request["scenario_id"] = f"action-runtime:{scope}"
    action_output = ActionGovernanceEngineV1().run_case(
        ActionGovernanceInputV1(**action_request)
    )
    action_safety_key = (
        action_output.action_candidate.action_candidate_id,
        task_handoff.task_state_ref,
        task_handoff.decision_candidate_ref,
        envelope.envelope_ref,
        envelope.envelope_version_ref,
        "runtime-execution",
    )
    action_safety = form_runtime_safety_prerequisite_v1(
        binding_key=action_safety_key,
        effect_class="runtime-execution",
        scope_kind="ACTION_ADMISSION",
    )
    admitted_action = admit_action_v1(
        action_output,
        task_handoff=task_handoff,
        working_envelope_ref=envelope.envelope_ref,
        working_envelope_version_ref=envelope.envelope_version_ref,
        safety_prerequisite=action_safety,
        profile_ref=ACTION_ADMISSION_PROFILE_PRODUCTION_CANONICAL,
    )
    assert admitted_action is not None
    target_request = ProviderBindingRuntimePreparationInputV1(
        preparation_ref="gpt6-g01-target",
        parent_cognitive_problem_ref=case.target_candidates[0].parent_cognitive_problem_ref,
        source_state_ref=case.target_candidates[0].source_state_ref,
        provider_target_candidates=tuple(case.target_candidates),
        context_refs=case.target_candidates[0].context_refs,
        trace_ref="trace:gpt6-g01-target",
        provenance_refs=("provenance:gpt6-g01-target",),
    )
    target = form_provider_binding_runtime_preparation_candidates(target_request)
    binding = form_provider_binding_candidates(
        ProviderBindingCandidateInputV1(
            preparation_ref="gpt6-g01-binding",
            parent_cognitive_problem_ref=target.parent_cognitive_problem_ref,
            source_state_ref=target.source_state_ref,
            preparation_candidates=target.candidates,
            context_refs=target.context_refs,
            trace_ref="trace:gpt6-g01-binding",
            provenance_refs=("provenance:gpt6-g01-binding",),
            runtime_requirement_refs=("runtime-requirement:gpt6-g01",),
            resource_class_refs=("resource-class:gpt6-g01",),
            execution_class_refs=("execution-class:gpt6-g01",),
        )
    )
    allocation = form_runtime_allocation_preparation_candidates(
        RuntimeAllocationPreparationInputV1(
            preparation_ref="gpt6-g01-allocation",
            parent_cognitive_problem_ref=binding.parent_cognitive_problem_ref,
            source_state_ref=binding.source_state_ref,
            provider_binding_candidates=binding.candidates,
            context_refs=target.context_refs,
            trace_ref="trace:gpt6-g01-allocation",
            provenance_refs=("provenance:gpt6-g01-allocation",),
        )
    )
    execution = form_execution_instance_preparation_candidates(
        ExecutionInstancePreparationInputV1(
            preparation_ref="gpt6-g01-execution",
            parent_cognitive_problem_ref=allocation.parent_cognitive_problem_ref,
            source_state_ref=allocation.source_state_ref,
            runtime_allocation_candidates=allocation.candidates,
            runtime_envelope_shape_refs=("runtime-envelope:gpt6-g01",),
            context_refs=target.context_refs,
            trace_ref="trace:gpt6-g01-execution",
            provenance_refs=("provenance:gpt6-g01-execution",),
        )
    )
    canonical_binding = replace(
        binding.candidates[0],
        provider_candidate_ref="provider_openvins",
        capability_candidate_ref="spatial_mapping",
        capability_class_ref="capability-class:spatial-mapping",
        admitted_action_ref=admitted_action.admitted_action_ref,
        working_envelope_ref=envelope.envelope_ref,
        working_envelope_version_ref=envelope.envelope_version_ref,
    )
    canonical_allocation = replace(
        allocation.candidates[0],
        provider_candidate_ref=canonical_binding.provider_candidate_ref,
        capability_candidate_ref=canonical_binding.capability_candidate_ref,
        capability_class_ref=canonical_binding.capability_class_ref,
        admitted_action_ref=admitted_action.admitted_action_ref,
        working_envelope_ref=envelope.envelope_ref,
        working_envelope_version_ref=envelope.envelope_version_ref,
    )
    canonical_execution = replace(
        execution.candidates[0],
        provider_candidate_ref=canonical_binding.provider_candidate_ref,
        capability_candidate_ref=canonical_binding.capability_candidate_ref,
        capability_class_ref=canonical_binding.capability_class_ref,
        admitted_action_ref=admitted_action.admitted_action_ref,
        working_envelope_ref=envelope.envelope_ref,
        working_envelope_version_ref=envelope.envelope_version_ref,
    )
    binding_key = build_pregrant_authority_binding_key(
        admitted_action_ref=admitted_action.admitted_action_ref,
        working_envelope_ref=envelope.envelope_ref,
        working_envelope_version_ref=envelope.envelope_version_ref,
        execution_instance_preparation_candidate_ref=canonical_execution.execution_instance_preparation_candidate_ref,
        provider_candidate_ref=canonical_binding.provider_candidate_ref,
        capability_candidate_ref=canonical_binding.capability_candidate_ref,
    )
    safety = form_runtime_safety_prerequisite_v1(
        binding_key=(*binding_key, "runtime-execution"),
        effect_class="runtime-execution",
    )
    result = form_runtime_execution_grants(
        RuntimeExecutionGrantInputV1(
            grant_request_ref="gpt6-g01-grant-request",
            parent_cognitive_problem_ref=execution.parent_cognitive_problem_ref,
            source_state_ref=execution.source_state_ref,
            provider_binding_candidates=(canonical_binding,),
            runtime_allocation_candidates=(canonical_allocation,),
            execution_instance_preparation_candidates=(canonical_execution,),
            permission_refs=("permission:gpt6-g01",),
            safety_refs=("safety:gpt6-g01",),
            protocol_refs=("protocol:runtime-execution-grant:v1",),
            governance_refs=("governance:gpt6-g01",),
            constraint_refs=("constraint:gpt6-g01",),
            validity_scope=("scope:gpt6-g01",),
            expiry_boundary_ref="expiry:gpt6-g01",
            trace_ref="trace:gpt6-g01-grant",
            provenance_refs=("provenance:gpt6-g01-grant",),
            grant_authority_ref=case.grant_authority_ref,
            grant_responsibility_ref=case.grant_responsibility_ref,
            safety_prerequisite_ref=safety.result_ref,
            admitted_action_ref=admitted_action.admitted_action_ref,
            working_envelope_ref=envelope.envelope_ref,
            working_envelope_version_ref=envelope.envelope_version_ref,
        )
    )
    assert result.decisions
    return result, result.decisions[0]


def _frame() -> RawFrameRecordV1:
    return RawFrameRecordV1(
        frame_id="frame:gpt6-g01",
        stream_session_id="session:gpt6-g01",
        source_type="IMAGE_FILE",
        source_ref="synthetic://gpt6-g01",
        device_ref=None,
        frame_index=0,
        captured_at=1,
        width=1,
        height=1,
        pixel_format="SYNTHETIC",
        frame_payload_ref="payload:gpt6-g01",
        content_hash="hash:gpt6-g01",
        temporal_validity={"stale": False, "expired": False},
        sensitivity="LOW",
        trace_ref="trace:gpt6-g01",
        provenance_refs=("provenance:gpt6-g01",),
    )


def _admission(provider_candidate_ref: str):
    return build_vision_provider_admission_candidate_v1(
        observation_demand_ref="demand:gpt6-g01",
        observation_request_ref="request:gpt6-g01",
        capability_requirement_ref="capability-requirement:gpt6-g01",
        provider_session_ref="session:gpt6-g01",
        provider_candidate_ref=provider_candidate_ref,
        model_candidate_ref="model:gpt6-g01",
        model_admission_ref="runtime-admission:gpt6-g01",
        region_scope_candidate="bounded-frame",
        expected_evidence=(CAPABILITY_KIND,),
        bounded=True,
        provider_admitted=True,
        trace_ref="trace:gpt6-g01",
        provenance_refs=("provenance:gpt6-g01",),
        canonical_capability_model_binding_ref="capability-binding:gpt6-g01",
        canonical_capability_model_binding_version="v1",
        canonical_runtime_admission_ref="runtime-admission:gpt6-g01",
        canonical_runtime_admission_version="v1",
        canonical_model_provider_binding_ref="provider-binding:gpt6-g01",
        canonical_model_provider_binding_version="v1",
        canonical_chain_validated=True,
        require_canonical_chain=True,
    )


def test_caller_constructed_candidate_requires_current_owner_authorization() -> None:
    admission = _admission("provider-candidate:gpt6-g01")

    result = run_authorized_vision_provider_v1(
        _frame(),
        admission,
        execute_real_provider=True,
        provider_failure=True,
        model_path="/never-opened-by-this-test.pt",
    )

    assert admission.provider_invocation_authorized is True
    assert admission.canonical_chain_validated is True
    assert result.error_code == "RUNTIME_AUTHORIZATION_NOT_CURRENT"
    assert result.invocation_performed is False


def test_owner_authorized_candidate_reaches_safe_pre_effect_seam() -> None:
    _, grant = _owner_issued_grant_from_public_api()
    admission = _admission(grant.provider_candidate_ref)

    result = run_authorized_vision_provider_v1(
        _frame(),
        admission,
        execute_real_provider=True,
        runtime_authorization_grant=grant,
        provider_failure=True,
        model_path="/never-opened-by-this-test.pt",
    )

    assert result.detector_mode == "REAL_YOLO"
    assert result.error_code == "PROVIDER_INVOCATION_FAILED"
    assert result.invocation_performed is False

    mismatched = run_authorized_vision_provider_v1(
        _frame(),
        _admission("provider-candidate:gpt6-g01-mismatch"),
        execute_real_provider=True,
        runtime_authorization_grant=grant,
        provider_failure=True,
        model_path="/never-opened-by-this-test.pt",
    )
    assert mismatched.error_code == "RUNTIME_AUTHORIZATION_NOT_CURRENT"
    assert mismatched.invocation_performed is False

    invalidated = invalidate_runtime_authorization_state(
        authorization_ref=grant.authorization_ref,
        subject_ref=grant.source_execution_instance_preparation_ref,
        reason="gpt6-g01-focused-regression",
    )
    assert invalidated is not None
    assert invalidated.status == "INVALIDATED"
    revoked = run_authorized_vision_provider_v1(
        _frame(),
        admission,
        execute_real_provider=True,
        runtime_authorization_grant=grant,
        provider_failure=True,
        model_path="/never-opened-by-this-test.pt",
    )
    assert revoked.error_code == "RUNTIME_AUTHORIZATION_NOT_CURRENT"
    assert revoked.invocation_performed is False


def test_engine_transports_same_owner_grant_to_adapter(monkeypatch) -> None:
    """The engine is a mechanical transport boundary, not a grant owner."""

    _, grant = _owner_issued_grant_from_public_api()
    captured = []

    fpo_record = SimpleNamespace(
        demand=SimpleNamespace(
            demand_id="demand:gpt6-g01-engine",
            provenance_refs=(),
        ),
        trace=SimpleNamespace(control_trace_ref="trace:gpt6-g01-engine"),
        request=SimpleNamespace(
            request_id="request:gpt6-g01-engine",
            target_region_candidate="bounded-frame",
        ),
        capability_requirement=SimpleNamespace(
            requirement_id="capability-requirement:gpt6-g01-engine",
        ),
        provider_session=SimpleNamespace(session_id="session:gpt6-g01-engine"),
    )
    context_result = SimpleNamespace(
        context=SimpleNamespace(),
        validation=SimpleNamespace(trace_refs=(), provenance_refs=()),
    )
    frame = SimpleNamespace(frame_payload_ref="payload:gpt6-g01-engine")
    admission = SimpleNamespace(
        provider_invocation_authorized=True,
        canonical_chain_validated=True,
        provider_candidate_ref=grant.provider_candidate_ref,
        canonical_invalidation_refs=(),
    )

    class _FpoEngine:
        def run_case(self, _payload):
            return fpo_record

    monkeypatch.setattr(
        real_provider_engine_module,
        "FieldPerceptionActiveObservationControlEngineV1",
        _FpoEngine,
    )
    engine = RealProviderExecutionEngineV1(real_provider_engine_module.Path.cwd())
    monkeypatch.setattr(engine.ingress_engine, "_fpo_payload", lambda _case: {})
    monkeypatch.setattr(
        engine.ingress_engine,
        "_resolve",
        lambda _case, _record: (object(), object(), SimpleNamespace(module_ref="capability:gpt6-g01"), ()),
    )
    monkeypatch.setattr(
        real_provider_engine_module,
        "produce_yolo11n_governed_execution_records_v1",
        lambda _repo_root: SimpleNamespace(bundle=object()),
    )
    monkeypatch.setattr(
        real_provider_engine_module,
        "adapt_governed_bundle_to_canonical_yolo11n_records_v1",
        lambda _bundle: object(),
    )
    monkeypatch.setattr(
        real_provider_engine_module,
        "build_canonical_yolo11n_context_v1",
        lambda _records: context_result,
    )
    monkeypatch.setattr(real_provider_engine_module, "_declared_checksum", lambda _root: "checksum")
    monkeypatch.setattr(real_provider_engine_module, "_sha256", lambda _path: "checksum")
    monkeypatch.setattr(
        real_provider_engine_module,
        "resolve_yolo11n_external_provisioning_v1",
        lambda _payload: SimpleNamespace(technical_admission_status="ADMISSION_READY_CANDIDATE"),
    )
    monkeypatch.setattr(real_provider_engine_module, "_image_size_v0", lambda _path: (1, 1))
    monkeypatch.setattr(
        real_provider_engine_module,
        "adapt_raw_camera_source",
        lambda *_args, **_kwargs: SimpleNamespace(accepted=True, frames=(frame,)),
    )
    monkeypatch.setattr(
        real_provider_engine_module,
        "build_canonical_yolo11n_provider_admission_v1",
        lambda **_kwargs: SimpleNamespace(admission=admission),
    )

    def _adapter_spy(_frame, _admission, **kwargs):
        captured.append(kwargs["runtime_authorization_grant"])
        return SimpleNamespace(
            accepted=False,
            detections=(),
            error_code="RUNTIME_AUTHORIZATION_NOT_CURRENT",
            invocation_performed=False,
            trace_ref="trace:gpt6-g01-engine-provider",
            provenance_refs=(),
        )

    monkeypatch.setattr(real_provider_engine_module, "run_authorized_vision_provider_v1", _adapter_spy)
    case = build_provider_observation_cases_v1()[0]
    result = engine.run(
        case,
        source_ref="source:gpt6-g01-engine",
        model_path="model:gpt6-g01-engine",
        runtime_authorization_grant=grant,
    )

    assert len(captured) == 1
    assert captured[0] is grant
    assert result["provider_real_execution_verified"] is False
