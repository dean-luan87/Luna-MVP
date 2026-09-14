"""Candidate-only adapters for the remaining canonical execution edges."""

from __future__ import annotations

from typing import Optional, Tuple

from capabilities.midplatform.core.cognitive_flow.integration.canonical_source_state_outcome_return_controlled.types_v1 import EdgeObservabilityCandidateV1

from .types_v1 import (
    AReassessmentInputCandidateV1,
    ACognitiveRequirementInputV1,
    ActionAdmissionInputCandidateV1,
    ActionResultInputV1,
    AttentionAllocationInputCandidateV1,
    DecisionActionInputV1,
    HandoffEdgeV1,
    HandoffFailureV1,
    HandoffOutputV1,
    ObservationRequestCandidateV1,
    RuntimeObservationInputV1,
    TaskActionInputV1,
    TaskResultReturnCandidateV1,
)


READY_RUNTIME_STATUS = "READY_FOR_EXECUTABLE_CANDIDATE"
STALE_MARKERS = {"STALE", "EXPIRED", "INVALID", "VERSION_MISMATCH", "REVOKED", "SUPERSEDED"}


def _edge(
    *,
    transition_id: str,
    trace_refs: Tuple[str, ...],
    producer: str,
    consumer: str,
    authority_owner: str,
    responsibility_owner: str,
    transition_class: str,
    input_refs: Tuple[str, ...],
    input_versions: Tuple[str, ...],
    output_refs: Tuple[str, ...],
    output_versions: Tuple[str, ...],
    status: str,
    invalidation_refs: Tuple[str, ...],
    provenance_refs: Tuple[str, ...],
    failure_classification: Optional[str],
    next_target: str,
) -> HandoffEdgeV1:
    trace_id = trace_refs[0] if trace_refs else f"trace:handoff:{transition_id}"
    edge_provenance = provenance_refs or (f"prov:edge:{transition_id}:handoff-adapter",)
    edge = EdgeObservabilityCandidateV1(
        transition_id=transition_id,
        trace_id=trace_id,
        parent_transition_refs=(),
        concern_ref=None,
        reasoning_cycle_ref=None,
        producer=producer,
        consumer=consumer,
        authority_owner=authority_owner,
        responsibility_owner=responsibility_owner,
        transition_class=transition_class,
        input_refs=input_refs,
        input_versions=input_versions,
        output_refs=output_refs,
        output_versions=output_versions,
        admission_or_validation_status=status,
        constraint_refs=(),
        evidence_refs=(),
        provenance_refs=edge_provenance,
        invalidation_refs=invalidation_refs,
        failure_classification=failure_classification,
        blocker_refs=(),
        next_target=next_target,
    )
    return HandoffEdgeV1(edge=edge)


def _failure(
    *,
    ref: str,
    classification: str,
    reason: str,
    responsible_owner: str,
    semantic_owner: str,
    global_owner: str,
    next_target: str,
    source_refs: Tuple[str, ...],
    trace_refs: Tuple[str, ...],
    provenance_refs: Tuple[str, ...],
    invalidation_refs: Tuple[str, ...] = (),
) -> HandoffFailureV1:
    return HandoffFailureV1(
        failure_ref=ref,
        classification=classification,
        reason=reason,
        responsible_owner=responsible_owner,
        semantic_consequence_owner=semantic_owner,
        global_consequence_owner=global_owner,
        next_target=next_target,
        source_refs=source_refs,
        trace_refs=trace_refs,
        provenance_refs=provenance_refs,
        invalidation_refs=invalidation_refs,
    )


def _result(
    *,
    output_kind: str,
    output: object,
    edge: HandoffEdgeV1,
    failure: Optional[HandoffFailureV1] = None,
) -> HandoffOutputV1:
    return HandoffOutputV1(output_kind=output_kind, output=output, edge=edge, failure=failure)


def adapt_a_requirement_to_attention(data: ACognitiveRequirementInputV1, *, handoff_id: str) -> HandoffOutputV1:
    source_refs = tuple(ref for ref in (data.cognitive_requirement_ref, data.cognitive_need_ref, data.concern_ref) if ref)
    failure: Optional[HandoffFailureV1] = None
    if not data.synthetic_only or not data.candidate_only:
        failure = _failure(ref=f"failure:a-attention:{handoff_id}:synthetic", classification="NON_SYNTHETIC_INPUT", reason="A requirement is not synthetic candidate-only input", responsible_owner="A→Attention handoff adapter", semantic_owner="A", global_owner="Brain Governance", next_target="A", source_refs=source_refs, trace_refs=data.trace_refs, provenance_refs=data.provenance_refs)
    elif not data.cognitive_need_ref:
        failure = _failure(ref=f"failure:a-attention:{handoff_id}:need", classification="COGNITIVE_NEED_MISSING", reason="A requirement has no Cognitive Need ref", responsible_owner="A", semantic_owner="A", global_owner="Brain Governance", next_target="A", source_refs=source_refs, trace_refs=data.trace_refs, provenance_refs=data.provenance_refs)
    elif not data.cognitive_requirement_ref:
        failure = _failure(ref=f"failure:a-attention:{handoff_id}:requirement", classification="COGNITIVE_REQUIREMENT_MISSING", reason="A requirement identity is missing", responsible_owner="A", semantic_owner="A", global_owner="Brain Governance", next_target="A", source_refs=source_refs, trace_refs=data.trace_refs, provenance_refs=data.provenance_refs)
    elif data.status.upper() in STALE_MARKERS or data.invalidation_refs:
        failure = _failure(ref=f"failure:a-attention:{handoff_id}:stale", classification="A_REQUIREMENT_STALE", reason="A requirement is stale or invalidated", responsible_owner="A", semantic_owner="A", global_owner="Brain Governance", next_target="A", source_refs=source_refs, trace_refs=data.trace_refs, provenance_refs=data.provenance_refs, invalidation_refs=data.invalidation_refs)
    elif data.grant_ref and any(marker in data.grant_ref.upper() for marker in ("REVOKED", "EXPIRED", "STALE")):
        failure = _failure(ref=f"failure:a-attention:{handoff_id}:grant", classification="GRANT_REVOKED", reason="Grant is revoked, expired or stale", responsible_owner="Brain Governance", semantic_owner="A", global_owner="Brain Governance", next_target="Brain Governance", source_refs=source_refs, trace_refs=data.trace_refs, provenance_refs=data.provenance_refs)
    elif not data.concern_ref or not data.reasoning_cycle_ref or not data.target_ref:
        failure = _failure(ref=f"failure:a-attention:{handoff_id}:scope", classification="A_REQUIREMENT_SCOPE_MISSING", reason="Concern, reasoning cycle or target scope is missing", responsible_owner="A", semantic_owner="A", global_owner="Brain Governance", next_target="A", source_refs=source_refs, trace_refs=data.trace_refs, provenance_refs=data.provenance_refs)
    elif not data.source_version_refs:
        failure = _failure(ref=f"failure:a-attention:{handoff_id}:version", classification="SOURCE_VERSION_MISSING", reason="A requirement source versions are missing", responsible_owner="A→Attention handoff adapter", semantic_owner="A", global_owner="Brain Governance", next_target="A", source_refs=source_refs, trace_refs=data.trace_refs, provenance_refs=data.provenance_refs)
    elif not data.provenance_refs:
        failure = _failure(ref=f"failure:a-attention:{handoff_id}:provenance", classification="PROVENANCE_INVALID", reason="A requirement provenance is missing", responsible_owner="A→Attention handoff adapter", semantic_owner="A", global_owner="Brain Governance", next_target="A", source_refs=source_refs, trace_refs=data.trace_refs, provenance_refs=data.provenance_refs)
    edge = _edge(
        transition_id=f"transition:a-attention:{handoff_id}", trace_refs=data.trace_refs,
        producer="A", consumer="Attention", authority_owner="Attention",
        responsibility_owner=failure.responsible_owner if failure else "A→Attention handoff adapter",
        transition_class="FORMATION / BINDING", input_refs=source_refs,
        input_versions=data.source_version_refs, output_refs=() if failure else (f"attention-input:{handoff_id}",),
        output_versions=() if failure else (f"attention-input-v:{handoff_id}:v1",),
        status="BLOCKED" if failure else "VALID", invalidation_refs=data.invalidation_refs,
        provenance_refs=data.provenance_refs, failure_classification=failure.classification if failure else None,
        next_target=failure.next_target if failure else "Attention",
    )
    if failure:
        return _result(output_kind="AttentionAllocationInputCandidateV1", output=None, edge=edge, failure=failure)
    output = AttentionAllocationInputCandidateV1(
        allocation_ref=f"attention-input:{handoff_id}", allocation_version=f"attention-input-v:{handoff_id}:v1",
        concern_ref=data.concern_ref or "", reasoning_cycle_ref=data.reasoning_cycle_ref or "",
        cognitive_need_ref=data.cognitive_need_ref or "", cognitive_requirement_ref=data.cognitive_requirement_ref or "",
        target_ref=data.target_ref or "", expected_evidence_refs=data.expected_evidence_refs,
        semantic_relevance_refs=data.semantic_relevance_refs, role_refs=data.role_refs,
        perspective_refs=data.perspective_refs, task_refs=data.task_refs, context_refs=data.context_refs,
        safety_refs=data.safety_refs, permission_refs=data.permission_refs, resource_refs=data.resource_refs,
        grant_ref=data.grant_ref or "", priority_input_refs=("urgency:input", "modality:input", "budget:input"),
        source_version_refs=data.source_version_refs, trace_refs=data.trace_refs, provenance_refs=data.provenance_refs,
    )
    return _result(output_kind="AttentionAllocationInputCandidateV1", output=output, edge=edge)


def adapt_runtime_to_observation(data: RuntimeObservationInputV1, *, handoff_id: str) -> HandoffOutputV1:
    executable = data.executable_candidate
    assessment = data.runtime_assessment
    runtime_invalidation_refs = data.invalidation_refs + ((assessment.expiry_staleness_refs) if assessment else ()) + ((executable.expiry_staleness_refs) if executable else ())
    source_refs = tuple(ref for ref in (data.cognitive_requirement_ref, data.expected_capability_ref, data.model_binding_ref, data.provider_binding_ref) if ref)
    failure: Optional[HandoffFailureV1] = None
    if executable is None or assessment is None:
        failure = _failure(ref=f"failure:runtime-observation:{handoff_id}:executable", classification="EXECUTABLE_CAPABILITY_MISSING", reason="Executable Capability and Runtime Admission assessment are required", responsible_owner="Runtime Admission", semantic_owner="A", global_owner="Brain Governance", next_target="Runtime Admission", source_refs=source_refs, trace_refs=data.trace_refs, provenance_refs=data.provenance_refs)
    elif assessment.admission_status in {"STALE_ADMISSION_CANDIDATE", "EXPIRED"} or assessment.expiry_staleness_refs:
        failure = _failure(ref=f"failure:runtime-observation:{handoff_id}:runtime-stale", classification="RUNTIME_ADMISSION_STALE", reason="stale Runtime Admission cannot become Observation-ready", responsible_owner="Runtime Admission", semantic_owner="A", global_owner="Brain Governance", next_target="Runtime Admission", source_refs=source_refs, trace_refs=data.trace_refs, provenance_refs=data.provenance_refs, invalidation_refs=runtime_invalidation_refs)
    elif assessment.admission_status != READY_RUNTIME_STATUS:
        failure = _failure(ref=f"failure:runtime-observation:{handoff_id}:runtime", classification="RUNTIME_ADMISSION_NOT_READY", reason="blocked, degraded or stale Runtime Admission cannot become Observation-ready", responsible_owner="Runtime Admission", semantic_owner="A", global_owner="Brain Governance", next_target="Runtime Admission", source_refs=source_refs, trace_refs=data.trace_refs, provenance_refs=data.provenance_refs, invalidation_refs=data.invalidation_refs)
    elif not executable.candidate_only or executable.provider_invocation_executed or executable.model_loading_executed:
        failure = _failure(ref=f"failure:runtime-observation:{handoff_id}:execution", classification="RUNTIME_EXECUTION_DETECTED", reason="Executable candidate carries forbidden execution state", responsible_owner="Runtime Admission", semantic_owner="A", global_owner="Brain Governance", next_target="Runtime Admission", source_refs=source_refs, trace_refs=data.trace_refs, provenance_refs=data.provenance_refs)
    elif not data.cognitive_requirement_ref or not data.concern_ref or not data.attention_refs or not data.target_refs or not data.focus_refs:
        failure = _failure(ref=f"failure:runtime-observation:{handoff_id}:scope", classification="OBSERVATION_SCOPE_MISSING", reason="Cognitive requirement, attention, target or focus refs are missing", responsible_owner="Runtime→Observation handoff adapter", semantic_owner="A", global_owner="Brain Governance", next_target="A", source_refs=source_refs, trace_refs=data.trace_refs, provenance_refs=data.provenance_refs)
    elif executable.logical_capability_ref != data.expected_capability_ref:
        failure = _failure(ref=f"failure:runtime-observation:{handoff_id}:capability", classification="CAPABILITY_REF_MISMATCH", reason="Executable Capability does not match the requested Capability", responsible_owner="Runtime Admission", semantic_owner="A", global_owner="Brain Governance", next_target="Runtime Admission", source_refs=source_refs, trace_refs=data.trace_refs, provenance_refs=data.provenance_refs)
    elif not data.model_binding_ref or data.model_binding_ref != data.expected_model_binding_ref or not data.provider_binding_ref or data.provider_binding_ref != data.expected_provider_binding_ref:
        failure = _failure(ref=f"failure:runtime-observation:{handoff_id}:binding", classification="BINDING_REF_MISMATCH", reason="Model/Provider binding refs are missing or inconsistent", responsible_owner="Capability/Provider binding boundary", semantic_owner="A", global_owner="Brain Governance", next_target="Runtime Admission", source_refs=source_refs, trace_refs=data.trace_refs, provenance_refs=data.provenance_refs)
    elif not data.grant_refs or not data.permission_refs or not data.safety_refs or not data.resource_refs:
        failure = _failure(ref=f"failure:runtime-observation:{handoff_id}:constraint", classification="CONSTRAINT_REF_MISSING", reason="Grant, Permission, Safety or Resource refs are missing", responsible_owner="Runtime Admission", semantic_owner="A", global_owner="Brain Governance", next_target="Runtime Admission", source_refs=source_refs, trace_refs=data.trace_refs, provenance_refs=data.provenance_refs)
    elif data.permission_status.upper() in {"REVOKED", "EXPIRED", "STALE", "DENIED"} or any("REVOKED" in ref.upper() for ref in data.permission_refs):
        failure = _failure(ref=f"failure:runtime-observation:{handoff_id}:permission", classification="PERMISSION_REVOKED", reason="Observation permission is revoked or stale", responsible_owner="Permission Governance", semantic_owner="A", global_owner="Brain Governance", next_target="Permission Governance", source_refs=source_refs, trace_refs=data.trace_refs, provenance_refs=data.provenance_refs)
    elif data.invalidation_refs or executable.source_state_version_ref != executable.valid_state_version_ref or executable.expiry_staleness_refs:
        failure = _failure(ref=f"failure:runtime-observation:{handoff_id}:stale", classification="SOURCE_VERSION_STALE", reason="Executable Capability or source versions are stale", responsible_owner="Runtime Admission", semantic_owner="A", global_owner="Brain Governance", next_target="Runtime Admission", source_refs=source_refs, trace_refs=data.trace_refs, provenance_refs=data.provenance_refs, invalidation_refs=runtime_invalidation_refs)
    elif not data.source_version_refs or not data.provenance_refs or not executable.provenance_refs:
        failure = _failure(ref=f"failure:runtime-observation:{handoff_id}:provenance", classification="PROVENANCE_INVALID", reason="Observation handoff provenance or source versions are missing", responsible_owner="Runtime→Observation handoff adapter", semantic_owner="A", global_owner="Brain Governance", next_target="Runtime Admission", source_refs=source_refs, trace_refs=data.trace_refs, provenance_refs=data.provenance_refs)
    edge = _edge(
        transition_id=f"transition:runtime-observation:{handoff_id}", trace_refs=data.trace_refs,
        producer="Runtime Admission", consumer="Observation", authority_owner="Observation",
        responsibility_owner=failure.responsible_owner if failure else "Runtime→Observation handoff adapter",
        transition_class="BINDING / ADMISSION", input_refs=source_refs + ((executable.executable_capability_ref,) if executable else ()),
        input_versions=data.source_version_refs + ((executable.valid_state_version_ref,) if executable else ()),
        output_refs=() if failure else (f"observation-request:{handoff_id}",), output_versions=() if failure else (f"observation-request-v:{handoff_id}:v1",),
        status="BLOCKED" if failure else "VALID", invalidation_refs=runtime_invalidation_refs,
        provenance_refs=data.provenance_refs, failure_classification=failure.classification if failure else None,
        next_target=failure.next_target if failure else "Observation",
    )
    if failure:
        return _result(output_kind="ObservationRequestCandidateV1", output=None, edge=edge, failure=failure)
    output = ObservationRequestCandidateV1(
        request_ref=f"observation-request:{handoff_id}", request_version=f"observation-request-v:{handoff_id}:v1",
        concern_ref=data.concern_ref or "", cognitive_requirement_ref=data.cognitive_requirement_ref or "",
        executable_capability_ref=executable.executable_capability_ref, capability_ref=executable.logical_capability_ref,
        model_binding_ref=data.model_binding_ref or "", provider_binding_ref=data.provider_binding_ref or "",
        attention_refs=data.attention_refs, target_refs=data.target_refs, focus_refs=data.focus_refs,
        grant_refs=data.grant_refs, permission_refs=data.permission_refs, safety_refs=data.safety_refs,
        resource_refs=data.resource_refs, source_version_refs=data.source_version_refs,
        trace_refs=data.trace_refs, provenance_refs=data.provenance_refs,
    )
    return _result(output_kind="ObservationRequestCandidateV1", output=output, edge=edge)


def _action_failure(source: str, action_ref: str, status: str, *, source_refs: Tuple[str, ...], trace_refs: Tuple[str, ...], provenance_refs: Tuple[str, ...], invalidation_refs: Tuple[str, ...]) -> Optional[HandoffFailureV1]:
    if status == "APPROVED":
        return None
    return _failure(ref=f"failure:{source}:{action_ref}:status", classification=f"{source.upper()}_{status}", reason=f"{source} source is not approved/ready for Action handoff", responsible_owner="Decision Governance" if source == "decision" else "Task", semantic_owner="A", global_owner="Brain Governance", next_target="Decision Governance" if source == "decision" else "Task", source_refs=source_refs, trace_refs=trace_refs, provenance_refs=provenance_refs, invalidation_refs=invalidation_refs)


def _build_action_output(*, source_kind: str, source_ref: str, concern_ref: str, intent_ref: Optional[str], action_type: str, target_ref: str, precondition_refs: Tuple[str, ...], dependency_refs: Tuple[str, ...], permission_refs: Tuple[str, ...], safety_refs: Tuple[str, ...], resource_refs: Tuple[str, ...], grant_refs: Tuple[str, ...], confirmation_refs: Tuple[str, ...], idempotency_refs: Tuple[str, ...], source_version_refs: Tuple[str, ...], trace_refs: Tuple[str, ...], provenance_refs: Tuple[str, ...], handoff_id: str, decision_ref: Optional[str], task_ref: Optional[str], failure: Optional[HandoffFailureV1]) -> HandoffOutputV1:
    edge = _edge(
        transition_id=f"transition:{source_kind}-action:{handoff_id}", trace_refs=trace_refs,
        producer="Decision Governance" if source_kind == "decision" else "Task",
        consumer="Action Governance", authority_owner="Action Governance",
        responsibility_owner=failure.responsible_owner if failure else "Decision/Task→Action handoff adapter",
        transition_class="BINDING / VALIDATION", input_refs=tuple(ref for ref in (source_ref, decision_ref, task_ref, target_ref) if ref),
        input_versions=source_version_refs, output_refs=() if failure else (f"action-admission-input:{handoff_id}",), output_versions=() if failure else (f"action-admission-input-v:{handoff_id}:v1",),
        status="BLOCKED" if failure else "VALID", invalidation_refs=failure.invalidation_refs if failure else (), provenance_refs=provenance_refs,
        failure_classification=failure.classification if failure else None, next_target=failure.next_target if failure else "Action Governance",
    )
    if failure:
        return _result(output_kind="ActionAdmissionInputCandidateV1", output=None, edge=edge, failure=failure)
    output = ActionAdmissionInputCandidateV1(
        admission_input_ref=f"action-admission-input:{handoff_id}", admission_input_version=f"action-admission-input-v:{handoff_id}:v1",
        source_kind=source_kind, decision_ref=decision_ref, task_ref=task_ref, concern_ref=concern_ref,
        intent_ref=intent_ref, action_type=action_type, target_ref=target_ref, precondition_refs=precondition_refs,
        dependency_refs=dependency_refs, permission_refs=permission_refs, safety_refs=safety_refs, resource_refs=resource_refs,
        grant_refs=grant_refs, confirmation_refs=confirmation_refs, idempotency_refs=idempotency_refs,
        source_version_refs=source_version_refs, trace_refs=trace_refs, provenance_refs=provenance_refs,
    )
    return _result(output_kind="ActionAdmissionInputCandidateV1", output=output, edge=edge)


def adapt_decision_to_action(data: DecisionActionInputV1, *, handoff_id: str) -> HandoffOutputV1:
    source_refs = tuple(ref for ref in (data.decision_ref, data.concern_ref, data.intent_ref, data.target_ref) if ref)
    failure = _action_failure("decision", handoff_id, data.decision_status, source_refs=source_refs, trace_refs=data.trace_refs, provenance_refs=data.provenance_refs, invalidation_refs=data.invalidation_refs)
    if failure is None and (not data.decision_ref or not data.decision_version):
        failure = _failure(ref=f"failure:decision-action:{handoff_id}:decision", classification="DECISION_REF_MISSING", reason="Decision ref/version is missing", responsible_owner="Decision Governance", semantic_owner="A", global_owner="Brain Governance", next_target="Decision Governance", source_refs=source_refs, trace_refs=data.trace_refs, provenance_refs=data.provenance_refs)
    elif failure is None and data.invalidation_refs:
        failure = _failure(ref=f"failure:decision-action:{handoff_id}:stale", classification="DECISION_STALE_OR_REVOKED", reason="Decision is stale, revoked or superseded", responsible_owner="Decision Governance", semantic_owner="A", global_owner="Brain Governance", next_target="Decision Governance", source_refs=source_refs, trace_refs=data.trace_refs, provenance_refs=data.provenance_refs, invalidation_refs=data.invalidation_refs)
    elif failure is None and (not data.action_type or not data.target_ref or not data.precondition_refs):
        failure = _failure(ref=f"failure:decision-action:{handoff_id}:target", classification="ACTION_TARGET_OR_PRECONDITION_MISSING", reason="Action type, target or preconditions are missing", responsible_owner="Decision Governance", semantic_owner="A", global_owner="Brain Governance", next_target="Decision Governance", source_refs=source_refs, trace_refs=data.trace_refs, provenance_refs=data.provenance_refs)
    elif failure is None and (not data.permission_refs or not data.safety_refs or not data.resource_refs or not data.grant_refs):
        failure = _failure(ref=f"failure:decision-action:{handoff_id}:constraint", classification="ACTION_CONSTRAINT_REF_MISSING", reason="Action constraint refs are incomplete", responsible_owner="Decision Governance", semantic_owner="A", global_owner="Brain Governance", next_target="Decision Governance", source_refs=source_refs, trace_refs=data.trace_refs, provenance_refs=data.provenance_refs)
    elif failure is None and (not data.source_version_refs or not data.provenance_refs):
        failure = _failure(ref=f"failure:decision-action:{handoff_id}:lineage", classification="PROVENANCE_OR_VERSION_INVALID", reason="Decision handoff lineage is incomplete", responsible_owner="Decision→Action handoff adapter", semantic_owner="A", global_owner="Brain Governance", next_target="Decision Governance", source_refs=source_refs, trace_refs=data.trace_refs, provenance_refs=data.provenance_refs)
    return _build_action_output(source_kind="decision", source_ref=data.decision_ref or "", concern_ref=data.concern_ref or "", intent_ref=data.intent_ref, action_type=data.action_type or "", target_ref=data.target_ref or "", precondition_refs=data.precondition_refs, dependency_refs=(), permission_refs=data.permission_refs, safety_refs=data.safety_refs, resource_refs=data.resource_refs, grant_refs=data.grant_refs, confirmation_refs=data.confirmation_refs, idempotency_refs=data.idempotency_refs, source_version_refs=data.source_version_refs, trace_refs=data.trace_refs, provenance_refs=data.provenance_refs, handoff_id=handoff_id, decision_ref=data.decision_ref, task_ref=None, failure=failure)


def adapt_task_to_action(data: TaskActionInputV1, *, handoff_id: str) -> HandoffOutputV1:
    source_refs = tuple(ref for ref in (data.task_ref, data.source_decision_ref, data.target_ref) if ref)
    failure: Optional[HandoffFailureV1] = None
    if not data.task_ref or not data.task_version:
        failure = _failure(ref=f"failure:task-action:{handoff_id}:task", classification="TASK_REF_MISSING", reason="Task ref/version is missing", responsible_owner="Task", semantic_owner="A", global_owner="Brain Governance", next_target="Task", source_refs=source_refs, trace_refs=data.trace_refs, provenance_refs=data.provenance_refs)
    elif data.task_status != "READY":
        failure = _failure(ref=f"failure:task-action:{handoff_id}:readiness", classification="TASK_NOT_READY", reason="Task readiness does not permit Action handoff", responsible_owner="Task", semantic_owner="A", global_owner="Brain Governance", next_target="Task", source_refs=source_refs, trace_refs=data.trace_refs, provenance_refs=data.provenance_refs)
    elif data.blocker_refs or data.dependency_refs:
        failure = _failure(ref=f"failure:task-action:{handoff_id}:dependency", classification="TASK_DEPENDENCY_BLOCKED", reason="Task dependencies or blockers remain", responsible_owner="Task", semantic_owner="A", global_owner="Brain Governance", next_target="Task", source_refs=source_refs, trace_refs=data.trace_refs, provenance_refs=data.provenance_refs)
    elif not data.source_decision_ref:
        failure = _failure(ref=f"failure:task-action:{handoff_id}:decision", classification="SOURCE_DECISION_MISSING", reason="Task Action handoff lacks required source Decision ref", responsible_owner="Task", semantic_owner="A", global_owner="Brain Governance", next_target="Task", source_refs=source_refs, trace_refs=data.trace_refs, provenance_refs=data.provenance_refs)
    elif not data.action_type or not data.target_ref:
        failure = _failure(ref=f"failure:task-action:{handoff_id}:target", classification="ACTION_TARGET_MISSING", reason="Task Action type or target is missing", responsible_owner="Task", semantic_owner="A", global_owner="Brain Governance", next_target="Task", source_refs=source_refs, trace_refs=data.trace_refs, provenance_refs=data.provenance_refs)
    elif not data.permission_refs or not data.safety_refs or not data.resource_refs or not data.grant_refs:
        failure = _failure(ref=f"failure:task-action:{handoff_id}:constraint", classification="ACTION_CONSTRAINT_REF_MISSING", reason="Task Action constraint refs are incomplete", responsible_owner="Task", semantic_owner="A", global_owner="Brain Governance", next_target="Task", source_refs=source_refs, trace_refs=data.trace_refs, provenance_refs=data.provenance_refs)
    elif data.invalidation_refs or not data.source_version_refs:
        failure = _failure(ref=f"failure:task-action:{handoff_id}:stale", classification="TASK_STALE", reason="Task source version is stale or invalidated", responsible_owner="Task", semantic_owner="A", global_owner="Brain Governance", next_target="Task", source_refs=source_refs, trace_refs=data.trace_refs, provenance_refs=data.provenance_refs, invalidation_refs=data.invalidation_refs)
    elif not data.provenance_refs:
        failure = _failure(ref=f"failure:task-action:{handoff_id}:provenance", classification="PROVENANCE_INVALID", reason="Task handoff provenance is missing", responsible_owner="Task→Action handoff adapter", semantic_owner="A", global_owner="Brain Governance", next_target="Task", source_refs=source_refs, trace_refs=data.trace_refs, provenance_refs=data.provenance_refs)
    return _build_action_output(source_kind="task", source_ref=data.task_ref or "", concern_ref="concern:task", intent_ref=None, action_type=data.action_type or "", target_ref=data.target_ref or "", precondition_refs=data.precondition_refs, dependency_refs=data.dependency_refs, permission_refs=data.permission_refs, safety_refs=data.safety_refs, resource_refs=data.resource_refs, grant_refs=data.grant_refs, confirmation_refs=(), idempotency_refs=(), source_version_refs=data.source_version_refs, trace_refs=data.trace_refs, provenance_refs=data.provenance_refs, handoff_id=handoff_id, decision_ref=data.source_decision_ref, task_ref=data.task_ref, failure=failure)


def _action_result_failure(data: ActionResultInputV1, *, target: str) -> Optional[HandoffFailureV1]:
    source_refs = tuple(ref for ref in (data.action_result_ref, data.task_ref, data.concern_ref) if ref)
    if not data.action_result_ref or not data.action_result_version:
        return _failure(ref=f"failure:action-result:{target}:ref", classification="ACTION_RESULT_REF_MISSING", reason="Action Result ref/version is missing", responsible_owner="Action Governance", semantic_owner="A", global_owner="Brain Governance", next_target="Action Governance", source_refs=source_refs, trace_refs=data.trace_refs, provenance_refs=data.provenance_refs)
    if data.action_execution_executed is False and data.status not in {"SUCCESS", "PARTIAL", "FAILED", "UNCERTAIN"}:
        return _failure(ref=f"failure:action-result:{target}:status", classification="ACTION_RESULT_STATUS_INVALID", reason="Action Result status is not recognized", responsible_owner="Action Governance", semantic_owner="A", global_owner="Brain Governance", next_target="Action Governance", source_refs=source_refs, trace_refs=data.trace_refs, provenance_refs=data.provenance_refs)
    if data.invalidation_refs or data.status == "STALE":
        return _failure(ref=f"failure:action-result:{target}:stale", classification="ACTION_RESULT_STALE", reason="Action Result is stale or invalidated", responsible_owner="Action Governance", semantic_owner="A", global_owner="Brain Governance", next_target="Action Governance", source_refs=source_refs, trace_refs=data.trace_refs, provenance_refs=data.provenance_refs, invalidation_refs=data.invalidation_refs)
    if not data.source_version_refs or not data.provenance_refs:
        return _failure(ref=f"failure:action-result:{target}:lineage", classification="PROVENANCE_OR_VERSION_INVALID", reason="Action Result lineage is incomplete", responsible_owner="Action Result return adapter", semantic_owner="A", global_owner="Brain Governance", next_target="Action Governance", source_refs=source_refs, trace_refs=data.trace_refs, provenance_refs=data.provenance_refs)
    return None


def adapt_action_result_to_task(data: ActionResultInputV1, *, handoff_id: str) -> HandoffOutputV1:
    failure = _action_result_failure(data, target="task")
    source_refs = tuple(ref for ref in (data.action_result_ref, data.task_ref) if ref)
    edge = _edge(transition_id=f"transition:action-result-task:{handoff_id}", trace_refs=data.trace_refs, producer="Action Governance", consumer="Task", authority_owner="Task", responsibility_owner=failure.responsible_owner if failure else "Action Result→Task return adapter", transition_class="FORMATION / EVALUATION", input_refs=source_refs, input_versions=data.source_version_refs, output_refs=() if failure else (f"task-result-return:{handoff_id}",), output_versions=() if failure else (f"task-result-return-v:{handoff_id}:v1",), status="BLOCKED" if failure else "VALID", invalidation_refs=data.invalidation_refs, provenance_refs=data.provenance_refs, failure_classification=failure.classification if failure else None, next_target=failure.next_target if failure else "Task")
    if failure:
        return _result(output_kind="TaskResultReturnCandidateV1", output=None, edge=edge, failure=failure)
    if not data.task_ref:
        failure = _failure(ref=f"failure:action-result:task:{handoff_id}:task", classification="TASK_REF_MISSING", reason="Task return requires Task ref", responsible_owner="Action Result→Task return adapter", semantic_owner="A", global_owner="Brain Governance", next_target="Task", source_refs=source_refs, trace_refs=data.trace_refs, provenance_refs=data.provenance_refs)
        return _result(output_kind="TaskResultReturnCandidateV1", output=None, edge=edge, failure=failure)
    output = TaskResultReturnCandidateV1(return_ref=f"task-result-return:{handoff_id}", action_result_ref=data.action_result_ref or "", task_ref=data.task_ref, progress_refs=data.progress_refs, completion_evidence_refs=data.completion_evidence_refs, failure_refs=data.failure_refs, partiality=data.partiality, source_version_refs=data.source_version_refs, trace_refs=data.trace_refs, provenance_refs=data.provenance_refs)
    return _result(output_kind="TaskResultReturnCandidateV1", output=output, edge=edge)


def adapt_action_result_to_a(data: ActionResultInputV1, *, handoff_id: str) -> HandoffOutputV1:
    failure = _action_result_failure(data, target="a")
    source_refs = tuple(ref for ref in (data.action_result_ref, data.concern_ref, data.task_ref) if ref)
    edge = _edge(transition_id=f"transition:action-result-a:{handoff_id}", trace_refs=data.trace_refs, producer="Action Governance", consumer="A", authority_owner="A", responsibility_owner=failure.responsible_owner if failure else "Action Result→A reassessment adapter", transition_class="FORMATION / EVALUATION", input_refs=source_refs, input_versions=data.source_version_refs, output_refs=() if failure else (f"a-reassessment:{handoff_id}",), output_versions=() if failure else (f"a-reassessment-v:{handoff_id}:v1",), status="BLOCKED" if failure else "VALID", invalidation_refs=data.invalidation_refs, provenance_refs=data.provenance_refs, failure_classification=failure.classification if failure else None, next_target=failure.next_target if failure else "A")
    if failure:
        return _result(output_kind="AReassessmentInputCandidateV1", output=None, edge=edge, failure=failure)
    if not data.concern_ref:
        failure = _failure(ref=f"failure:action-result:a:{handoff_id}:concern", classification="CONCERN_REF_MISSING", reason="A reassessment requires Concern ref", responsible_owner="Action Result→A reassessment adapter", semantic_owner="A", global_owner="Brain Governance", next_target="A", source_refs=source_refs, trace_refs=data.trace_refs, provenance_refs=data.provenance_refs)
        return _result(output_kind="AReassessmentInputCandidateV1", output=None, edge=edge, failure=failure)
    output = AReassessmentInputCandidateV1(reassessment_ref=f"a-reassessment:{handoff_id}", action_result_ref=data.action_result_ref or "", concern_ref=data.concern_ref, task_ref=data.task_ref, effect_evidence_refs=data.effect_evidence_refs, source_state_update_refs=data.source_state_update_refs, failure_refs=data.failure_refs, uncertainty_refs=data.uncertainty_refs, partiality=data.partiality, source_version_refs=data.source_version_refs, invalidation_refs=data.invalidation_refs, trace_refs=data.trace_refs, provenance_refs=data.provenance_refs)
    return _result(output_kind="AReassessmentInputCandidateV1", output=output, edge=edge)
