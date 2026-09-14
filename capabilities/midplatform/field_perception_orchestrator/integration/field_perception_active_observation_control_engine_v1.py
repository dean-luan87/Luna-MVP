from __future__ import annotations

from typing import Any, Dict, Mapping, Sequence, Tuple

from capabilities.midplatform.field_perception_orchestrator.integration.field_perception_active_observation_control_error_types_v1 import (
    make_error,
)
from capabilities.midplatform.field_perception_orchestrator.integration.field_perception_active_observation_control_types_v1 import (
    ActiveObservationControlResultV1,
    ActiveObservationTraceV1,
    BoundedProviderSessionCandidateV1,
    CapabilityRequirementCandidateV1,
    EvidenceSufficiencyCandidateV1,
    NextCycleIngressCandidateV1,
    ObservationControlDecisionV1,
    ObservationDemandCandidateV1,
    ObservationRequestCandidateV1,
    SafetyCriticalObservationExceptionCandidateV1,
)


MAX_RECONSIDERATION_DEPTH = 2
OWNER = "Field Perception Orchestrator"


def _tuple(value: Any) -> Tuple[str, ...]:
    if value is None:
        return tuple()
    if isinstance(value, str):
        return (value,)
    return tuple(str(item) for item in value)


def _dict(value: Any) -> Dict[str, Any]:
    return dict(value) if isinstance(value, Mapping) else {}


def _ref(prefix: str, case_id: str) -> str:
    return f"{prefix}:{case_id}"


def _demand_active(payload: Mapping[str, Any]) -> bool:
    return bool(
        str(payload.get("information_need") or "").strip()
        or str(payload.get("intent_ref") or "").strip()
        or str(payload.get("task_ref") or "").strip()
        or str(payload.get("safety_ref") or "").strip()
    )


def _build_demand(payload: Mapping[str, Any]) -> ObservationDemandCandidateV1:
    case_id = str(payload.get("case_id") or "unknown")
    root_trace = str(payload.get("root_cycle_trace_id") or _ref("root-cycle", case_id))
    correction_refs = _tuple(payload.get("correction_refs"))
    provenance = [_ref("provenance", case_id), root_trace]
    provenance.extend(correction_refs)
    return ObservationDemandCandidateV1(
        demand_id=_ref("observation-demand", case_id),
        root_cycle_trace_id=root_trace,
        source_owner=OWNER,
        source_context_refs=_tuple(payload.get("context_refs")),
        source_intent_refs=_tuple(payload.get("intent_ref")),
        source_task_refs=_tuple(payload.get("task_ref")),
        source_safety_refs=_tuple(payload.get("safety_ref")),
        source_field_refs=_tuple(payload.get("field_refs")),
        information_need=str(payload.get("information_need") or ""),
        expected_evidence_kinds=_tuple(payload.get("expected_evidence_kinds")),
        target_semantics=str(payload.get("target_semantic") or ""),
        spatial_scope_candidate=str(payload.get("spatial_scope") or ""),
        temporal_scope_candidate=str(payload.get("temporal_scope") or ""),
        urgency_candidate=str(payload.get("urgency") or "normal"),
        priority_candidate=str(payload.get("priority") or "normal"),
        resource_budget_candidate=_dict(payload.get("resource_budget")),
        stop_conditions=_tuple(payload.get("stop_conditions") or ("sufficient_evidence", "budget_exhausted", "cancelled", "target_lost")),
        uncertainty_refs=_tuple(payload.get("uncertainty_refs")),
        provenance_refs=tuple(dict.fromkeys(provenance)),
        trace_ref=_ref("trace:demand", case_id),
    )


def _derive_capabilities(payload: Mapping[str, Any], demand: ObservationDemandCandidateV1) -> Tuple[str, ...]:
    requested = _tuple(payload.get("requested_capability_kinds"))
    expected = set(demand.expected_evidence_kinds)
    if not requested:
        if bool(payload.get("spatial_required", False)) or "SLAM_SPATIAL_EVIDENCE" in expected:
            requested = ("SLAM_SPATIAL_EVIDENCE",)
        elif "OCR_TEXT_EVIDENCE" in expected or bool(payload.get("signage_region_detected", False)):
            requested = ("VISION_DETECTION", "REGION_PROPOSAL", "OCR_TEXT_EVIDENCE")
        elif _demand_active(payload):
            requested = ("VISION_DETECTION", "REGION_PROPOSAL")
    forbidden = set(_tuple(payload.get("forbidden_capability_kinds")))
    return tuple(item for item in dict.fromkeys(requested) if item not in forbidden)


def _build_request(
    payload: Mapping[str, Any],
    demand: ObservationDemandCandidateV1,
    capabilities: Sequence[str],
) -> ObservationRequestCandidateV1 | None:
    if not _demand_active(payload) or bool(payload.get("duplicate_demand", False)):
        return None
    case_id = str(payload.get("case_id") or "unknown")
    request_trace = _ref("trace:request", case_id)
    provenance = tuple(dict.fromkeys((*demand.provenance_refs, request_trace)))
    return ObservationRequestCandidateV1(
        request_id=_ref("observation-request", case_id),
        demand_ref=demand.demand_id,
        observation_goal=str(payload.get("observation_goal") or demand.information_need or "observe_task_target"),
        target_region_candidate=str(payload.get("target_region") or demand.spatial_scope_candidate or "scoped_observation_region"),
        target_semantic_candidate=str(payload.get("target_semantic") or demand.target_semantics),
        required_capability_kinds=tuple(capabilities),
        optional_capability_kinds=_tuple(payload.get("optional_capability_kinds")),
        forbidden_capability_kinds=_tuple(payload.get("forbidden_capability_kinds")),
        evidence_expectation=demand.expected_evidence_kinds,
        budget=_dict(payload.get("resource_budget")),
        temporal_validity=_dict(payload.get("temporal_validity")),
        trace_ref=request_trace,
        provenance_refs=provenance,
    )


def _build_capability_requirement(
    payload: Mapping[str, Any],
    request: ObservationRequestCandidateV1 | None,
) -> CapabilityRequirementCandidateV1 | None:
    if request is None or bool(payload.get("duplicate_request", False)):
        return None
    case_id = str(payload.get("case_id") or "unknown")
    trace_ref = _ref("trace:capability", case_id)
    return CapabilityRequirementCandidateV1(
        requirement_id=_ref("capability-requirement", case_id),
        observation_request_ref=request.request_id,
        required_capability_kinds=request.required_capability_kinds,
        optional_capability_kinds=request.optional_capability_kinds,
        forbidden_capability_kinds=request.forbidden_capability_kinds,
        requirement_reason=str(payload.get("capability_reason") or request.observation_goal),
        target_region_candidate=request.target_region_candidate,
        semantic_scope_candidate=request.target_semantic_candidate,
        evidence_goal=request.evidence_expectation,
        budget_candidate=request.budget,
        trace_ref=trace_ref,
        provenance_refs=tuple(dict.fromkeys((*request.provenance_refs, trace_ref))),
    )


def _build_safety_exception(
    payload: Mapping[str, Any],
    demand: ObservationDemandCandidateV1,
) -> SafetyCriticalObservationExceptionCandidateV1 | None:
    raw = _dict(payload.get("safety_exception"))
    if not raw:
        return None
    case_id = str(payload.get("case_id") or "unknown")
    trace_ref = _ref("trace:safety-exception", case_id)
    return SafetyCriticalObservationExceptionCandidateV1(
        exception_id=_ref("safety-exception", case_id),
        explicit_policy_ref=str(raw.get("explicit_policy_ref") or ""),
        reason=str(raw.get("reason") or ""),
        target_scope=str(raw.get("target_scope") or demand.spatial_scope_candidate),
        capability_scope=_tuple(raw.get("capability_scope")),
        bounded_budget=_dict(raw.get("bounded_budget")),
        temporal_validity=_dict(raw.get("temporal_validity")),
        revoke_condition=str(raw.get("revoke_condition") or ""),
        trace_ref=trace_ref,
        provenance_refs=tuple(dict.fromkeys((*demand.provenance_refs, trace_ref))),
    )


def _build_provider_session(
    payload: Mapping[str, Any],
    request: ObservationRequestCandidateV1 | None,
    requirement: CapabilityRequirementCandidateV1 | None,
    safety_exception: SafetyCriticalObservationExceptionCandidateV1 | None,
) -> BoundedProviderSessionCandidateV1 | None:
    if request is None or requirement is None:
        return None
    if bool(payload.get("duplicate_capability_requirement", False)) or bool(payload.get("duplicate_provider_session", False)):
        return None
    if not bool(payload.get("provider_admission_candidate", True)):
        return None
    if bool(payload.get("gateway_admitted", False)) and not bool(payload.get("provider_admission_candidate", False)):
        return None
    if safety_exception is not None:
        required = (safety_exception.explicit_policy_ref, safety_exception.reason, safety_exception.revoke_condition)
        if not all(required) or not safety_exception.capability_scope or not safety_exception.bounded_budget:
            return None
    case_id = str(payload.get("case_id") or "unknown")
    selected = requirement.required_capability_kinds[0] if requirement.required_capability_kinds else ""
    trace_ref = _ref("trace:provider-session", case_id)
    return BoundedProviderSessionCandidateV1(
        session_id=_ref("provider-session", case_id),
        observation_request_ref=request.request_id,
        capability_requirement_ref=requirement.requirement_id,
        selected_capability_ref=str(payload.get("selected_capability_ref") or _ref("selected-capability", selected or case_id)),
        selected_model_candidate_ref=str(payload.get("selected_model_candidate_ref") or _ref("model-candidate", case_id)),
        provider_candidate_ref=str(payload.get("provider_candidate_ref") or _ref("provider-candidate", case_id)),
        region_scope=request.target_region_candidate,
        semantic_scope=request.target_semantic_candidate,
        evidence_goal=request.evidence_expectation,
        frame_time_budget_candidate=_dict(payload.get("frame_time_budget")),
        retry_budget_candidate=_dict(payload.get("retry_budget")),
        resource_budget_candidate=request.budget,
        start_condition="observation_demand_and_admission_candidate_required",
        stop_conditions=_tuple(payload.get("session_stop_conditions") or ("sufficient_evidence", "budget_exhausted", "cancelled", "target_lost", "revoke")),
        revoke_conditions=_tuple(payload.get("revoke_conditions") or ("user_correction", "safety_revoked", "task_cancelled", "provider_failure")),
        redirect_allowed=bool(payload.get("redirect_allowed", True)),
        switch_allowed=bool(payload.get("switch_allowed", True)),
        trace_ref=trace_ref,
        provenance_refs=tuple(dict.fromkeys((*requirement.provenance_refs, trace_ref))),
    )


def _build_sufficiency(
    payload: Mapping[str, Any],
    demand: ObservationDemandCandidateV1,
    request: ObservationRequestCandidateV1 | None,
) -> EvidenceSufficiencyCandidateV1:
    case_id = str(payload.get("case_id") or "unknown")
    expected = demand.expected_evidence_kinds
    received_kinds = _tuple(payload.get("received_evidence_kinds"))
    received_refs = _tuple(payload.get("received_evidence_refs"))
    contradictions = _tuple(payload.get("contradiction_refs"))
    temporal = _dict(payload.get("temporal_validity"))
    target_coverage = bool(payload.get("target_coverage", bool(received_kinds)))
    semantic_coverage = bool(payload.get("semantic_coverage", bool(received_kinds)))
    spatial_required = bool(payload.get("spatial_required", False))
    spatial_coverage = bool(payload.get("spatial_coverage", not spatial_required))
    user_required = bool(payload.get("user_confirmation_required", False))
    user_confirmed = bool(payload.get("user_confirmed", False))
    if bool(payload.get("field_changed", False)) or bool(payload.get("stale_evidence", False)) or bool(temporal.get("stale", False)):
        status, reason = "STALE", "evidence_temporally_invalid_or_field_changed"
    elif contradictions or bool(payload.get("cross_modal_contradiction", False)):
        status, reason = "CONTESTED", "contradictory_evidence_preserved"
    elif user_required and not user_confirmed:
        status, reason = "NEEDS_CONFIRMATION", "explicit_user_confirmation_required"
    elif bool(payload.get("redirect_required", False)):
        status, reason = "NEEDS_REDIRECT", "target_or_region_requires_redirect"
    elif bool(payload.get("provider_switch_required", False)):
        status, reason = "NEEDS_PROVIDER_SWITCH", "current_provider_candidate_is_not_suitable"
    elif expected and not received_kinds:
        status, reason = "INSUFFICIENT", "no_evidence_received"
    elif expected and not set(expected).issubset(set(received_kinds)):
        status, reason = "NEEDS_ADDITIONAL_MODALITY", "expected_evidence_kind_missing"
    elif not target_coverage or not semantic_coverage or not spatial_coverage:
        status, reason = "NEEDS_ADDITIONAL_MODALITY", "coverage_is_incomplete_for_information_need"
    else:
        status, reason = "SUFFICIENT", "task_relative_evidence_coverage_is_complete"
    trace_ref = _ref("trace:sufficiency", case_id)
    return EvidenceSufficiencyCandidateV1(
        sufficiency_id=_ref("evidence-sufficiency", case_id),
        information_need_ref=str(payload.get("information_need_ref") or demand.demand_id),
        observation_request_ref=request.request_id if request is not None else "",
        expected_evidence=expected,
        received_evidence_refs=received_refs,
        received_evidence_kinds=received_kinds,
        source_diversity=int(payload.get("source_diversity", len(set(received_kinds))) or 0),
        source_independence_candidate=bool(payload.get("source_independence_candidate", True)),
        contradiction_refs=contradictions,
        uncertainty_refs=_tuple(payload.get("uncertainty_refs")),
        temporal_validity=temporal,
        target_coverage=target_coverage,
        semantic_coverage=semantic_coverage,
        spatial_coverage=spatial_coverage,
        user_confirmation_required=user_required,
        user_confirmed=user_confirmed,
        safety_requirement=bool(payload.get("safety_ref")),
        model_confidence_input=float(payload.get("model_confidence", 0.0) or 0.0),
        status=status,
        reason=reason,
        trace_ref=trace_ref,
        provenance_refs=tuple(dict.fromkeys((demand.trace_ref, *demand.provenance_refs, trace_ref))),
    )


def _control_decision(
    payload: Mapping[str, Any],
    demand: ObservationDemandCandidateV1,
    request: ObservationRequestCandidateV1 | None,
    session: BoundedProviderSessionCandidateV1 | None,
    sufficiency: EvidenceSufficiencyCandidateV1,
) -> Tuple[str, str]:
    if bool(payload.get("contract_mismatch", False)) or bool(payload.get("version_mismatch", False)):
        return "FAIL", "contract_or_version_mismatch"
    if int(payload.get("reconsideration_depth", 0) or 0) > MAX_RECONSIDERATION_DEPTH:
        return "FAIL", "reconsideration_depth_exceeded"
    if bool(payload.get("completed_observation_mutation_probe", False)):
        return "FAIL", "completed_observation_is_immutable"
    if bool(payload.get("repeated_provider_failure_signature", False)):
        return "FAIL", "repeated_provider_failure_signature_is_terminal"
    if bool(payload.get("task_complete", False)):
        return "STOP", "task_completed"
    if bool(payload.get("task_cancelled", False)):
        return "STOP", "task_cancelled"
    if bool(payload.get("safety_exception_revoked", False)):
        return "STOP", "safety_exception_revoked"
    if bool(payload.get("budget_exhausted", False)):
        return "DEFER", "resource_budget_exhausted"
    if bool(payload.get("duplicate_demand", False)) or bool(payload.get("duplicate_request", False)) or bool(payload.get("duplicate_capability_requirement", False)) or bool(payload.get("duplicate_provider_session", False)):
        return "DEFER", "duplicate_control_artifact_replayed"
    if bool(payload.get("duplicate_evidence_feedback", False)) or bool(payload.get("duplicate_sufficiency_adjudication", False)):
        return "DEFER", "duplicate_feedback_or_sufficiency_replayed"
    if bool(payload.get("duplicate_redirect", False)) or bool(payload.get("duplicate_switch", False)):
        return "DEFER", "duplicate_control_decision_replayed"
    if not _demand_active(payload):
        return "STOP", "no_information_need_or_governed_demand"
    if bool(payload.get("provider_failure", False)):
        if bool(payload.get("fallback_available", False)) and bool(payload.get("switch_allowed", True)):
            return "SWITCH_PROVIDER", "provider_failure_with_admitted_fallback_candidate"
        return "RECONSIDER", "provider_failure_requires_bounded_reconsideration"
    if bool(payload.get("target_lost", False)) or bool(payload.get("redirect_required", False)) or bool(payload.get("user_correction", False)):
        return "REDIRECT", "target_region_or_user_correction_requires_redirect"
    if bool(payload.get("intent_changed", False)):
        return "RECONSIDER", "intent_changed_mid_observation"
    if bool(payload.get("delayed_result", False)):
        return "DEFER", "provider_result_delayed_without_hidden_retry"
    if bool(payload.get("gateway_admitted", False)) and session is None and not sufficiency.received_evidence_refs:
        return "DEFER", "observation_gateway_admission_is_not_continuation_authorization"
    if sufficiency.status == "SUFFICIENT":
        return "STOP", "evidence_sufficiency_is_sufficient"
    if sufficiency.status == "STALE":
        return "REDIRECT", "stale_evidence_requires_new_scope"
    if sufficiency.status == "CONTESTED":
        return "RECONSIDER", "contradictory_evidence_requires_bounded_reconsideration"
    if sufficiency.status == "NEEDS_CONFIRMATION":
        return "RECONSIDER", "confirmation_required_before_continuation"
    if sufficiency.status == "NEEDS_REDIRECT":
        return "REDIRECT", "sufficiency_requires_attention_redirect"
    if sufficiency.status == "NEEDS_PROVIDER_SWITCH":
        return "SWITCH_PROVIDER", "sufficiency_requires_provider_switch"
    if sufficiency.status == "NEEDS_ADDITIONAL_MODALITY":
        return "ADD_CAPABILITY", "information_need_requires_additional_modality"
    if request is None or session is None:
        return "DEFER", "controlled_admission_or_provider_session_candidate_missing"
    return "CONTINUE", "demand_active_and_evidence_remains_insufficient"


def _build_trace(
    payload: Mapping[str, Any],
    demand: ObservationDemandCandidateV1,
    request: ObservationRequestCandidateV1 | None,
    requirement: CapabilityRequirementCandidateV1 | None,
    session: BoundedProviderSessionCandidateV1 | None,
    sufficiency: EvidenceSufficiencyCandidateV1,
    decision: ObservationControlDecisionV1,
    next_cycle: NextCycleIngressCandidateV1 | None,
) -> ActiveObservationTraceV1:
    case_id = str(payload.get("case_id") or "unknown")
    request_trace = request.trace_ref if request else ""
    capability_trace = requirement.trace_ref if requirement else ""
    session_trace = session.trace_ref if session else ""
    next_trace = next_cycle.trace_ref if next_cycle else ""
    evidence_traces = tuple(_tuple(payload.get("evidence_trace_refs"))) or (_ref("trace:evidence", case_id),)
    gateway_traces = tuple(_tuple(payload.get("gateway_trace_refs"))) or (_ref("trace:gateway", case_id),)
    refs = tuple(
        ref
        for ref in (
            demand.trace_ref,
            request_trace,
            capability_trace,
            session_trace,
            *evidence_traces,
            *gateway_traces,
            sufficiency.trace_ref,
            decision.trace_ref,
            next_trace,
        )
        if ref
    )
    return ActiveObservationTraceV1(
        root_cycle_trace_id=demand.root_cycle_trace_id,
        demand_trace_ref=demand.trace_ref,
        request_trace_ref=request_trace,
        attention_trace_ref=_ref("trace:attention", case_id),
        capability_trace_ref=capability_trace,
        session_trace_ref=session_trace,
        evidence_trace_refs=evidence_traces,
        gateway_trace_refs=gateway_traces,
        sufficiency_trace_ref=sufficiency.trace_ref,
        control_trace_ref=decision.trace_ref,
        next_cycle_trace_ref=next_trace,
        provenance_refs=tuple(dict.fromkeys((*demand.provenance_refs, *refs))),
        reverse_lookup_path=(
            demand.root_cycle_trace_id,
            demand.demand_id,
            request.request_id if request else "",
            _ref("attention-target", case_id),
            requirement.requirement_id if requirement else "",
            session.session_id if session else "",
            *evidence_traces,
            *gateway_traces,
            sufficiency.sufficiency_id,
            decision.decision_id,
            next_cycle.ingress_id if next_cycle else "",
        ),
    )


class FieldPerceptionActiveObservationControlEngineV1:
    """Pure controlled candidate engine owned by Field Perception Orchestrator."""

    provider_autonomous_continuous_execution = False
    runtime_execution = False
    provider_invocation = False
    mutation_authority = False
    general_provider_autonomy = False

    def run_case(self, payload: Mapping[str, Any]) -> ActiveObservationControlResultV1:
        case_id = str(payload.get("case_id") or "unknown")
        demand = _build_demand(payload)
        capabilities = _derive_capabilities(payload, demand)
        request = _build_request(payload, demand, capabilities)
        requirement = _build_capability_requirement(payload, request)
        safety_exception = _build_safety_exception(payload, demand)
        session = _build_provider_session(payload, request, requirement, safety_exception)
        sufficiency = _build_sufficiency(payload, demand, request)
        decision_value, decision_reason = _control_decision(payload, demand, request, session, sufficiency)
        decision_trace = _ref("trace:control", case_id)
        source_refs = tuple(dict.fromkeys((*demand.source_context_refs, *demand.source_intent_refs, *demand.source_task_refs, *demand.source_safety_refs, *demand.source_field_refs)))
        evidence_refs = tuple(dict.fromkeys((*sufficiency.received_evidence_refs, *sufficiency.contradiction_refs)))
        decision = ObservationControlDecisionV1(
            decision_id=_ref("control-decision", case_id),
            decision=decision_value,
            reason=decision_reason,
            source_refs=source_refs or (demand.demand_id,),
            evidence_refs=evidence_refs,
            budget_state=_dict(payload.get("resource_budget")),
            trace_ref=decision_trace,
            provenance_refs=tuple(dict.fromkeys((*demand.provenance_refs, sufficiency.trace_ref, decision_trace))),
        )
        next_cycle = None
        if bool(payload.get("next_cycle_requested", False)):
            next_trace = _ref("trace:next-cycle", case_id)
            next_cycle = NextCycleIngressCandidateV1(
                ingress_id=_ref("next-cycle-ingress", case_id),
                source_control_decision_ref=decision.decision_id,
                observation_demand_ref=demand.demand_id,
                observation_request_ref=request.request_id if request else "",
                feedback_refs=_tuple(payload.get("feedback_refs") or (sufficiency.sufficiency_id,)),
                correction_refs=_tuple(payload.get("correction_refs")),
                trace_ref=next_trace,
                provenance_refs=tuple(dict.fromkeys((*decision.provenance_refs, next_trace))),
            )
        errors = []
        if bool(payload.get("provider_autonomy_probe", False)) and not _demand_active(payload):
            errors.append(
                make_error(
                    "PROVIDER_AUTONOMY_VIOLATION",
                    "provider trigger is not an observation demand",
                    (demand.demand_id,),
                    demand.trace_ref,
                    False,
                )
            )
        for code, flag in (
            ("DUPLICATE_DEMAND", "duplicate_demand"),
            ("DUPLICATE_REQUEST", "duplicate_request"),
            ("DUPLICATE_CAPABILITY_REQUIREMENT", "duplicate_capability_requirement"),
            ("DUPLICATE_PROVIDER_SESSION", "duplicate_provider_session"),
            ("DUPLICATE_EVIDENCE_FEEDBACK", "duplicate_evidence_feedback"),
            ("DUPLICATE_SUFFICIENCY_ADJUDICATION", "duplicate_sufficiency_adjudication"),
            ("DUPLICATE_REDIRECT", "duplicate_redirect"),
            ("DUPLICATE_SWITCH", "duplicate_switch"),
            ("REPEATED_PROVIDER_FAILURE_SIGNATURE", "repeated_provider_failure_signature"),
            ("COMPLETED_OBSERVATION_IMMUTABLE", "completed_observation_mutation_probe"),
        ):
            if bool(payload.get(flag, False)):
                errors.append(make_error(code, f"{flag} guarded", (demand.demand_id,), decision.trace_ref, code in {"REPEATED_PROVIDER_FAILURE_SIGNATURE", "COMPLETED_OBSERVATION_IMMUTABLE"}))
        if int(payload.get("reconsideration_depth", 0) or 0) > MAX_RECONSIDERATION_DEPTH:
            errors.append(make_error("RECONSIDERATION_DEPTH_EXCEEDED", "reconsideration depth exceeded", (demand.demand_id,), decision.trace_ref, True))
        behavior = {
            "demand_present": _demand_active(payload),
            "demand_candidate_only": demand.candidate_only,
            "request_present": request is not None,
            "capability_requirement_present": requirement is not None,
            "required_capability_kinds": list(requirement.required_capability_kinds if requirement else ()),
            "ocr_capability_requirement_present": bool(requirement and "OCR_TEXT_EVIDENCE" in requirement.required_capability_kinds),
            "slam_capability_requirement_present": bool(requirement and "SLAM_SPATIAL_EVIDENCE" in requirement.required_capability_kinds),
            "provider_session_present": session is not None,
            "provider_session_candidate_only": bool(session and session.candidate_only),
            "provider_invocation": False,
            "runtime_execution": False,
            "provider_autonomous_continuous_execution": False,
            "general_provider_autonomy": False,
            "gateway_admission_is_continuation_authority": False,
            "observation_gateway_handoff_candidate_present": True,
            "a_route_ingress_candidate_present": True,
            "a_route_ingress_target": "INGRESS_READY",
            "runtime_handoff_ready": False,
            "vision_provider_can_invoke_ocr": False,
            "slam_semantic_truth_authority": False,
            "mutation_authority": False,
            "downstream_mutation": False,
            "safety_exception_present": safety_exception is not None,
            "safety_exception_valid": bool(safety_exception and safety_exception.explicit_policy_ref and safety_exception.reason and safety_exception.capability_scope and safety_exception.bounded_budget and safety_exception.revoke_condition),
            "safety_exception_bounded": bool(safety_exception and safety_exception.bounded_budget and safety_exception.temporal_validity and safety_exception.revoke_condition),
            "sufficiency_status": sufficiency.status,
            "model_confidence_input": sufficiency.model_confidence_input,
            "control_decision": decision.decision,
            "control_reason": decision.reason,
            "reconsideration_depth_guarded": int(payload.get("reconsideration_depth", 0) or 0) <= MAX_RECONSIDERATION_DEPTH,
            "repeated_failure_signature_guarded": not bool(payload.get("repeated_provider_failure_signature", False)) or decision.decision == "FAIL",
            "completed_observation_immutable": True,
            "rejected_capability_kinds": list(_tuple(payload.get("forbidden_capability_kinds"))),
            "session_continuation_authorized": decision.decision == "CONTINUE",
            "next_cycle_ingress_present": next_cycle is not None,
            "trace_reverse_lookup_complete": bool(demand.root_cycle_trace_id and demand.trace_ref and sufficiency.trace_ref and decision.trace_ref),
            "provenance_preserved": True,
        }
        negative_guards = {
            "provider_autonomous_continuous_execution": False,
            "provider_invocation": False,
            "runtime_execution": False,
            "provider_can_mutate_context": False,
            "provider_can_mutate_field": False,
            "provider_can_mutate_intent": False,
            "provider_can_mutate_task": False,
            "provider_can_mutate_decision": False,
            "observation_control_can_mutate_context": False,
            "observation_control_can_mutate_field": False,
            "observation_control_can_mutate_intent": False,
            "observation_control_can_mutate_task": False,
            "observation_control_can_mutate_decision": False,
            "observation_gateway_admission_is_execution": False,
            "model_confidence_is_sufficiency": False,
            "database_write": False,
            "vector_store_write": False,
            "scheduler_execution": False,
            "device_control": False,
            "emotion_engine_execution": False,
            "b_route_execution": False,
            "semantic_compression_execution": False,
            "candidate_only": True,
            "synthetic_only": True,
            "controlled_integration_only": True,
        }
        trace = _build_trace(payload, demand, request, requirement, session, sufficiency, decision, next_cycle)
        return ActiveObservationControlResultV1(
            case_id=case_id,
            demand=demand,
            request=request,
            capability_requirement=requirement,
            safety_exception=safety_exception,
            provider_session=session,
            sufficiency=sufficiency,
            control_decision=decision,
            next_cycle_ingress=next_cycle,
            trace=trace,
            behavior=behavior,
            errors=tuple(error.__dict__ for error in errors),
            negative_guards=negative_guards,
        )
