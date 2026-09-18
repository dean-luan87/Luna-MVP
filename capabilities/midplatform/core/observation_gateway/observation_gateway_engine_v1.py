from __future__ import annotations

from typing import List, Tuple

from capabilities.midplatform.core.execution_mode_v1 import (
    CONTROLLED_REPLAY_RUNTIME,
    LIVE_RUNTIME,
    SYNTHETIC_CONTROLLED,
    ControlledReplayAdmissionV1,
    validate_controlled_replay_input,
    validate_execution_mode,
)

from .observation_gateway_core_types_v1 import (
    ADMISSION_STATES,
    INGRESS_TYPES,
    ROUTING_TARGETS,
    ObservationCandidateV1,
    EvidenceReferenceBindingV1,
    ObservationGatewayResultV1,
    ObservationIngressCandidateV1,
    ObservationIngressRequestV1,
    ObservationGatewayRuntimeAdmissionV1,
    ObservationGatewayAdmissionRuntimeStateV1,
    ObservationGatewayAdmissionQueryV1,
    PerceptionEvidenceV1,
)
from .observation_gateway_error_types_v1 import ObservationGatewayErrorV1, make_error
from .observation_gateway_ownership_guard_v1 import build_negative_guards
from .observation_gateway_trace_types_v1 import ObservationGatewayTraceV1
from .observation_gateway_static_validators_v1 import (
    validate_ingress_request_shape,
    validate_runtime_observation_envelope,
)


class ObservationGatewayEngineV1:
    """Deterministic evidence normalization/admission/routing coordinator."""

    __slots__ = ("__admission_runtime_state", "__admission_query")

    def __init__(self) -> None:
        self.__admission_runtime_state = ObservationGatewayAdmissionRuntimeStateV1()
        self.__admission_query = ObservationGatewayAdmissionQueryV1._from_gateway_owner(
            self.__admission_runtime_state
        )

    @property
    def admission_query(self) -> ObservationGatewayAdmissionQueryV1:
        """Return the owner-mediated current-state query surface."""

        return self.__admission_query

    @staticmethod
    def _execution_identity(request: ObservationIngressRequestV1) -> str:
        return request.execution_identity_ref or request.scenario_id

    def _ingress(self, request: ObservationIngressRequestV1) -> ObservationIngressCandidateV1:
        sid = self._execution_identity(request)
        runtime = request.runtime_observation
        return ObservationIngressCandidateV1(
            ingress_id=f"ingress:{sid}",
            ingress_type=request.ingress_type,
            provider_ref=runtime.provider_ref if runtime else request.provider_ref,
            source_ref=runtime.source_ref if runtime else request.source_ref,
            payload_ref=runtime.raw_result_ref if runtime else request.payload_ref,
            temporal_ref=runtime.temporal_ref if runtime else request.temporal_ref,
            observed_at=runtime.observed_at if runtime else request.observed_at,
            valid_from_candidate=request.valid_from_candidate,
            valid_until_candidate=request.valid_until_candidate,
            confidence_candidate=(runtime.confidence_candidate if runtime and runtime.confidence_candidate is not None else request.confidence_candidate),
            quality_candidate=(runtime.quality_candidate if runtime and runtime.quality_candidate is not None else request.quality_candidate),
            sensitivity=request.sensitivity,
            trace_ref=f"trace:{sid}:ingress",
            provenance_refs=(f"prov:{sid}:ingress", request.source_ref),
        )

    def _evidence(self, request: ObservationIngressRequestV1, index: int = 1) -> PerceptionEvidenceV1:
        sid = self._execution_identity(request)
        runtime = request.runtime_observation
        evidence_type = {
            "USER_INPUT": "user_input_evidence",
            "VISION": "visual_detection_evidence",
            "OCR": "ocr_text_evidence",
            "AUDIO": "audio_recognition_evidence",
            "SLAM_SPATIAL": "slam_spatial_evidence",
            "FIELD_REFERENCE": "field_reference_evidence",
            "SYSTEM_EVENT": "system_event_evidence",
            "EXTERNAL_PROVIDER": "external_provider_evidence",
        }.get(request.ingress_type, "provider_evidence")
        if runtime is not None and runtime.empty_result:
            evidence_type = "ocr_empty_success"
        contradiction_refs = (f"contradiction:{sid}",) if request.multi_evidence_contradiction else ()
        correction_refs = (request.correction_ref,) if request.correction_ref else ()
        uncertainty_refs = (f"uncertainty:{sid}",) if request.uncertainty else ()
        evidence_id = (
            request.evidence_refs[index - 1]
            if index <= len(request.evidence_refs)
            else f"evidence:{sid}:{index}"
        )
        return PerceptionEvidenceV1(
            evidence_id=evidence_id,
            evidence_type=evidence_type,
            source_provider=runtime.provider_ref if runtime else request.provider_ref,
            source_capability=runtime.capability_ref if runtime else f"capability:{request.ingress_type.lower()}",
            source_model_ref=(runtime.source_model_ref if runtime else request.source_model_ref),
            source_region_ref=(runtime.source_region_ref if runtime else request.source_region_ref),
            source_temporal_ref=runtime.temporal_ref if runtime else request.temporal_ref,
            raw_output_ref=runtime.raw_result_ref if runtime else request.payload_ref,
            confidence_candidate=(runtime.confidence_candidate if runtime and runtime.confidence_candidate is not None else request.confidence_candidate),
            quality_candidate=(runtime.quality_candidate if runtime and runtime.quality_candidate is not None else request.quality_candidate),
            uncertainty_refs=uncertainty_refs,
            contradiction_refs=contradiction_refs,
            correction_refs=correction_refs,
            trace_ref=f"trace:{sid}:evidence:{index}",
            provenance_refs=tuple(dict.fromkeys((*(runtime.provenance_refs if runtime else ()), f"prov:{sid}:evidence:{index}", f"provider-trace:{sid}:{index}"))),
            sensitivity=request.sensitivity,
            candidate_payload=runtime.output_candidate if runtime else None,
            empty_result=bool(runtime.empty_result) if runtime else False,
        )

    def _observation(
        self,
        request: ObservationIngressRequestV1,
        evidence: Tuple[PerceptionEvidenceV1, ...],
        admission_state: str,
    ) -> ObservationCandidateV1:
        sid = self._execution_identity(request)
        runtime = request.runtime_observation
        contradiction_refs = tuple(ref for item in evidence for ref in item.contradiction_refs)
        correction_refs = tuple(ref for item in evidence for ref in item.correction_refs)
        uncertainty_refs = tuple(ref for item in evidence for ref in item.uncertainty_refs)
        return ObservationCandidateV1(
            observation_id=runtime.observation_id if runtime else f"observation:{sid}",
            observation_type=f"{request.ingress_type.lower()}_observation_candidate",
            evidence_refs=tuple(item.evidence_id for item in evidence),
            subject_candidate=f"subject:{sid}",
            attribute_candidate=f"attribute:{sid}",
            relation_candidate=None,
            spatial_refs=runtime.spatial_refs if runtime else request.spatial_refs,
            temporal_refs=(runtime.temporal_ref, runtime.observed_at, request.valid_from_candidate) if runtime else (request.temporal_ref, request.observed_at, request.valid_from_candidate),
            uncertainty_refs=uncertainty_refs,
            contradiction_refs=contradiction_refs,
            correction_refs=correction_refs,
            admission_state=admission_state,
            routing_targets=tuple(target for target in request.routing_targets if target in ROUTING_TARGETS),
            trace_ref=f"trace:{sid}:observation",
            provenance_refs=tuple(dict.fromkeys((*(runtime.provenance_refs if runtime else ()), f"prov:{sid}:observation"))),
            sensitivity=request.sensitivity,
        )

    def _trace(
        self,
        request: ObservationIngressRequestV1,
        ingress: ObservationIngressCandidateV1 | None,
        evidence: Tuple[PerceptionEvidenceV1, ...],
        observation: ObservationCandidateV1 | None,
        errors: Tuple[ObservationGatewayErrorV1, ...],
    ) -> ObservationGatewayTraceV1:
        sid = self._execution_identity(request)
        evidence_trace_refs = tuple(item.trace_ref for item in evidence)
        provider_refs = tuple(item.source_provider for item in evidence)
        runtime = request.runtime_observation
        source_refs = tuple(ref for ref in (
            runtime.source_ref if runtime else request.source_ref,
            runtime.raw_result_ref if runtime else request.payload_ref,
            runtime.provider_ref if runtime else request.provider_ref,
            runtime.capability_ref if runtime else None,
            *(runtime.trace_refs if runtime else ()),
        ) if ref)
        observation_ref = observation.observation_id if observation else "not-formed"
        ingress_ref = ingress.ingress_id if ingress else "not-formed"
        correction_lineage = tuple(ref for ref in (request.correction_ref, request.corrected_evidence_ref, request.corrected_observation_ref) if ref)
        contradiction_lineage = (f"contradiction:{sid}",) if request.multi_evidence_contradiction else ()
        temporal_lineage = (request.temporal_ref, request.observed_at, request.valid_from_candidate)
        error_refs = tuple(f"error:{sid}:{error.code}" for error in errors)
        return ObservationGatewayTraceV1(
            root_trace_id=f"root-trace:{sid}",
            a_route_ingress_ref=f"a-route-ingress:{sid}",
            observation_trace_ref=observation.trace_ref if observation else "not-formed",
            evidence_trace_refs=evidence_trace_refs,
            provider_trace_refs=provider_refs,
            source_input_refs=source_refs,
            provenance_refs=tuple(ref for item in evidence for ref in item.provenance_refs) or (f"gateway-provenance:{sid}",),
            correction_lineage=correction_lineage,
            contradiction_lineage=contradiction_lineage,
            temporal_lineage=temporal_lineage,
            reverse_lookup_path=(
                f"a-route-ingress:{sid}", observation_ref, *evidence_trace_refs,
                *provider_refs, *source_refs, *error_refs,
            ),
        )

    def _result(
        self,
        request: ObservationIngressRequestV1,
        ingress: ObservationIngressCandidateV1 | None,
        evidence: Tuple[PerceptionEvidenceV1, ...],
        observation: ObservationCandidateV1 | None,
        admission_state: str,
        route_status: str,
        route_refs: Tuple[str, ...],
        errors: List[ObservationGatewayErrorV1],
        deferred_refs: Tuple[str, ...] = (),
        replay_admission: ControlledReplayAdmissionV1 | None = None,
        runtime_admission: ObservationGatewayRuntimeAdmissionV1 | None = None,
    ) -> ObservationGatewayResultV1:
        error_tuple = tuple(errors)
        return ObservationGatewayResultV1(
            scenario_id=request.scenario_id,
            ingress=ingress,
            evidence=evidence,
            observation=observation,
            admission_state=admission_state,
            route_status=route_status,
            route_refs=route_refs,
            errors=error_tuple,
            trace=self._trace(request, ingress, evidence, observation, error_tuple),
            negative_guards=build_negative_guards(
                execution_mode=request.execution_mode,
                synthetic_only=request.synthetic_only,
            ),
            deferred_refs=deferred_refs,
            candidate_only=request.candidate_only,
            synthetic_only=request.synthetic_only,
            execution_mode=request.execution_mode,
            replay_input_ref=(
                request.replay_input.replay_input_ref
                if request.replay_input is not None
                else None
            ),
            replay_admission=replay_admission,
            runtime_admission=runtime_admission,
        )

    def _error_result(
        self,
        request: ObservationIngressRequestV1,
        code: str,
        message: str,
        stage_id: str = "INGRESS",
    ) -> ObservationGatewayResultV1:
        sid = self._execution_identity(request)
        error = make_error(code, stage_id, message, code in {"CONTRACT_MISMATCH", "VERSION_MISMATCH"}, (f"ingress:{sid}",), f"trace:{sid}:{stage_id.lower()}")
        return self._result(request, None, (), None, "REJECTED", "BLOCKED", (), [error])

    def run_case(self, request: ObservationIngressRequestV1) -> ObservationGatewayResultV1:
        sid = self._execution_identity(request)
        shape_errors = validate_ingress_request_shape(request)
        if shape_errors:
            return self._error_result(request, "INVALID_INPUT_SHAPE", ";".join(shape_errors))
        mode_errors = validate_execution_mode(
            request.execution_mode,
            synthetic_only=request.synthetic_only,
        )
        if mode_errors:
            return self._error_result(request, "INVALID_EXECUTION_MODE", ";".join(mode_errors))
        if not request.controlled_integration_only:
            return self._error_result(request, "INVALID_INGRESS", "controlled integration is required")
        if not request.candidate_only:
            return self._error_result(request, "INVALID_INGRESS", "candidate-only ingress is required")
        if request.execution_mode == LIVE_RUNTIME:
            runtime = request.runtime_observation
            if runtime is None or not validate_runtime_observation_envelope(runtime):
                return self._error_result(request, "RUNTIME_OBSERVATION_INVALID", "runtime observation envelope is invalid", "RUNTIME_OBSERVATION")
            if request.execution_identity_ref != runtime.execution_instance_ref:
                return self._error_result(request, "RUNTIME_EXECUTION_IDENTITY_MISMATCH", "runtime observation execution identity does not match ingress identity", "RUNTIME_OBSERVATION")
            if not runtime.provider_available or not runtime.capability_available or runtime.result_status != "AVAILABLE":
                return self._error_result(request, "PROVIDER_UNAVAILABLE", "runtime provider/capability result is unavailable", "RUNTIME_OBSERVATION")
            if request.ingress_type != runtime.modality:
                return self._error_result(request, "RUNTIME_MODALITY_MISMATCH", "runtime observation modality does not match ingress type", "RUNTIME_OBSERVATION")
        replay_admission = None
        if request.execution_mode == CONTROLLED_REPLAY_RUNTIME:
            replay_errors = validate_controlled_replay_input(request.replay_input)
            if replay_errors:
                return self._error_result(
                    request,
                    "REPLAY_ADMISSION_FAILED",
                    ";".join(replay_errors),
                    "REPLAY_ADMISSION",
                )
            replay = request.replay_input
            assert replay is not None
            replay_admission = ControlledReplayAdmissionV1(
                replay_input_ref=replay.replay_input_ref,
                replay_version=replay.replay_version,
                origin_class=replay.origin_class,
                source_ref=replay.source_ref,
                evidence_refs=replay.evidence_refs,
                provenance_refs=replay.provenance_refs,
                ordering_refs=replay.ordering_refs,
                gateway_admission_ref=f"gateway-admission:{sid}:v1",
                evidence_binding=EvidenceReferenceBindingV1(
                    gateway_admission_ref=f"gateway-admission:{sid}:v1",
                    evidence_refs=tuple(replay.evidence_refs),
                ),
                admission_state="ADMITTED_OBSERVATION",
                cycle_index=replay.cycle_index,
                required_information_refs=replay.required_information_refs,
                available_information_refs=replay.available_information_refs,
                requirement_establishment_status=replay.requirement_establishment_status,
                requirement_establishment_ref=replay.requirement_establishment_ref,
                requirement_establishment_basis=replay.requirement_establishment_basis,
                required_cognitive_condition_formation_result=replay.required_cognitive_condition_formation_result,
                prior_current_world_ref=replay.prior_current_world_ref,
                prior_hypothesis_refs=replay.prior_hypothesis_refs,
                prior_information_gap_ref=replay.prior_information_gap_ref,
                prior_reobservation_ref=replay.prior_reobservation_ref,
                prior_next_cycle_ingress_ref=replay.prior_next_cycle_ingress_ref,
                prior_sufficiency_candidate=replay.prior_sufficiency_candidate,
                prior_information_gap_candidate=replay.prior_information_gap_candidate,
                prior_reobservation_candidate=replay.prior_reobservation_candidate,
                contradiction_refs=(
                    (f"contradiction:{sid}",)
                    if request.multi_evidence_contradiction
                    else ()
                ),
            )
        if request.invalid_ingress or request.ingress_type not in INGRESS_TYPES:
            return self._error_result(request, "UNSUPPORTED_INGRESS_TYPE", "unsupported or invalid ingress type")
        if request.contract_mismatch:
            return self._error_result(request, "CONTRACT_MISMATCH", "ingress contract mismatch")
        if request.version_mismatch:
            return self._error_result(request, "VERSION_MISMATCH", "ingress version mismatch")
        if request.missing_provider or not request.provider_ref:
            return self._error_result(request, "MISSING_PROVIDER_REF", "provider reference is required")
        if request.missing_provenance:
            return self._error_result(request, "MISSING_PROVENANCE", "provenance is required")
        if any(target not in ROUTING_TARGETS for target in request.routing_targets):
            return self._error_result(request, "INVALID_ROUTING_TARGET", "routing target is not governed by Observation Gateway", "ROUTING")
        if request.duplicate_ingress:
            return self._error_result(request, "DUPLICATE_INGRESS", "ingress replay rejected")
        if request.duplicate_evidence:
            return self._error_result(request, "DUPLICATE_EVIDENCE", "provider output replay rejected", "EVIDENCE")
        if request.duplicate_observation:
            return self._error_result(request, "DUPLICATE_OBSERVATION", "observation replay rejected", "OBSERVATION")
        if request.duplicate_correction:
            return self._error_result(request, "DUPLICATE_CORRECTION", "correction replay rejected", "CORRECTION")
        if request.duplicate_refresh:
            return self._error_result(request, "DUPLICATE_REFRESH", "refresh replay rejected", "TEMPORAL")
        if request.revocation_replay:
            return self._error_result(request, "REVOCATION_REPLAY", "revocation replay rejected", "ADMISSION")
        if request.expiration_replay:
            return self._error_result(request, "EXPIRATION_REPLAY", "expiration replay rejected", "ADMISSION")
        if request.supersession_replay:
            return self._error_result(request, "SUPERSESSION_REPLAY", "supersession replay rejected", "ADMISSION")

        ingress = self._ingress(request)
        evidence_count = (
            len(request.evidence_refs)
            if request.execution_mode == CONTROLLED_REPLAY_RUNTIME
            else 2
            if request.multi_evidence_agreement
            or request.multi_evidence_contradiction
            or len(request.evidence_refs) > 1
            else 1
        )
        if evidence_count < 1:
            return self._error_result(request, "REPLAY_ADMISSION_FAILED", "replay evidence refs are required", "REPLAY_ADMISSION")
        evidence = tuple(self._evidence(request, index) for index in range(1, evidence_count + 1))
        if request.rejected:
            return self._result(request, ingress, evidence, None, "REJECTED", "BLOCKED", (), [], ())
        admission = "NORMALIZED"
        if request.expired:
            admission = "EXPIRED"
        elif request.revoked:
            admission = "REVOKED"
        elif request.superseded:
            admission = "SUPERSEDED"
        elif request.contested or request.multi_evidence_contradiction:
            admission = "CONTESTED"
        elif request.needs_confirmation or request.uncertainty:
            admission = "NEEDS_CONFIRMATION"
        elif request.refresh:
            admission = "EVIDENCE_READY"
        else:
            admission = "ADMITTED_OBSERVATION"

        observation = self._observation(request, evidence, admission)
        if request.user_correction:
            observation = ObservationCandidateV1(
                **{**observation.__dict__, "admission_state": "ADMITTED_OBSERVATION", "correction_refs": (request.correction_ref or f"correction:{sid}",)},
            )
            admission = "ADMITTED_OBSERVATION"
        if request.route_to_field:
            route_targets = (*observation.routing_targets, "Field / World State")
            observation = ObservationCandidateV1(**{**observation.__dict__, "routing_targets": tuple(dict.fromkeys(route_targets))})
        if request.route_to_context:
            route_targets = (*observation.routing_targets, "Context")
            observation = ObservationCandidateV1(**{**observation.__dict__, "routing_targets": tuple(dict.fromkeys(route_targets))})
        if request.route_to_attention:
            route_targets = (*observation.routing_targets, "Attention")
            observation = ObservationCandidateV1(**{**observation.__dict__, "routing_targets": tuple(dict.fromkeys(route_targets))})

        route_status = "INGRESS_READY" if request.route_to_orchestration and admission == "ADMITTED_OBSERVATION" else "ROUTING_CANDIDATE_READY"
        route_refs = (f"a-route-ingress:{sid}",) if request.route_to_orchestration and admission == "ADMITTED_OBSERVATION" else ()
        deferred = tuple(ref for ref, enabled in (("emotion_engine", request.emotion_deferred), ("b_route", request.b_route_deferred), ("semantic_compression", request.semantic_compression_deferred)) if enabled)
        runtime_admission = None
        if request.execution_mode == LIVE_RUNTIME:
            runtime = request.runtime_observation
            assert runtime is not None
            runtime_admission = ObservationGatewayRuntimeAdmissionV1(
                gateway_admission_ref=f"gateway-admission:{sid}:v1",
                runtime_observation_ref=runtime.observation_id,
                execution_instance_ref=runtime.execution_instance_ref,
                observation_ref=observation.observation_id,
                evidence_refs=tuple(item.evidence_id for item in evidence),
                provenance_refs=tuple(dict.fromkeys((*runtime.provenance_refs, *observation.provenance_refs))),
                gateway_trace_ref=f"root-trace:{sid}",
                evidence_binding=EvidenceReferenceBindingV1(
                    gateway_admission_ref=f"gateway-admission:{sid}:v1",
                    evidence_refs=tuple(item.evidence_id for item in evidence),
                ),
                cycle_index=request.cycle_index,
                required_information_refs=tuple(request.required_information_refs),
                available_information_refs=tuple(request.available_information_refs),
                requirement_establishment_status=request.requirement_establishment_status,
                requirement_establishment_ref=request.requirement_establishment_ref,
                requirement_establishment_basis=request.requirement_establishment_basis,
                required_cognitive_condition_formation_result=request.required_cognitive_condition_formation_result,
                evidence_information_refs=tuple(
                    (evidence_ref, tuple(information_refs))
                    for evidence_ref, information_refs in request.evidence_information_refs
                ),
                inherited_information_refs=tuple(request.inherited_information_refs),
                prior_current_world_ref=request.prior_current_world_ref,
                prior_hypothesis_refs=tuple(request.prior_hypothesis_refs),
                prior_information_gap_ref=request.prior_information_gap_ref,
                prior_reobservation_ref=request.prior_reobservation_ref,
                prior_next_cycle_ingress_ref=request.prior_next_cycle_ingress_ref,
                prior_sufficiency_candidate=request.prior_sufficiency_candidate,
                prior_information_gap_candidate=request.prior_information_gap_candidate,
                prior_reobservation_candidate=request.prior_reobservation_candidate,
                contradiction_refs=tuple(
                    ref for item in evidence for ref in item.contradiction_refs
                ),
            )
        if admission == "ADMITTED_OBSERVATION":
            admission_ref = (
                replay_admission.gateway_admission_ref
                if replay_admission is not None
                else runtime_admission.gateway_admission_ref
                if runtime_admission is not None
                else f"gateway-admission:{sid}:v1"
            )
            admitted_refs = (
                tuple(replay_admission.evidence_refs)
                if replay_admission is not None
                else tuple(runtime_admission.evidence_refs)
                if runtime_admission is not None
                else tuple(item.evidence_id for item in evidence)
            )
            admission_provenance = (
                tuple(replay_admission.provenance_refs)
                if replay_admission is not None
                else tuple(runtime_admission.provenance_refs)
                if runtime_admission is not None
                else tuple(ref for item in evidence for ref in item.provenance_refs)
            )
            if not self.__admission_runtime_state._record_admission(
                execution_identity_ref=sid,
                gateway_admission_ref=admission_ref,
                evidence_refs=admitted_refs,
                execution_mode=request.execution_mode,
                trace_refs=(f"root-trace:{sid}",),
                provenance_refs=admission_provenance,
                canonical_admission=replay_admission or runtime_admission,
            ):
                return self._error_result(
                    request,
                    "ADMISSION_STATE_CONFLICT",
                    "Gateway admission state could not be recorded",
                    "ADMISSION",
                )
        return self._result(
            request,
            ingress,
            evidence,
            observation,
            admission,
            route_status,
            route_refs,
            [],
            deferred,
            replay_admission=replay_admission,
            runtime_admission=runtime_admission,
        )
