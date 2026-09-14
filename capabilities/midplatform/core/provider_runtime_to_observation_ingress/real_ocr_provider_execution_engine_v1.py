"""LIVE_RUNTIME execution engine for the canonical local OCR provider."""

from __future__ import annotations

import dataclasses
from typing import Any, Dict, Tuple

from capabilities.midplatform.core.a_route_orchestration.a_route_orchestration_engine_v1 import (
    ARouteOrchestrationEngineV1,
)
from capabilities.midplatform.core.observation_gateway.observation_gateway_engine_v1 import (
    ObservationGatewayEngineV1,
)
from capabilities.midplatform.core.observation_runtime_ingress.adapters_v1 import (
    build_aroute_request,
    build_gateway_request,
)
from capabilities.midplatform.core.observation_runtime_ingress.types_v1 import (
    RuntimeObservationIngressCaseV1,
)
from capabilities.midplatform.field_perception_orchestrator.integration.field_perception_active_observation_control_engine_v1 import (
    FieldPerceptionActiveObservationControlEngineV1,
)

from .engine_v1 import ProviderRuntimeObservationIngressEngineV1, _jsonable
from .provider_result_adapter_v1 import provider_result_to_runtime_observation
from .real_ocr_provider_adapter_v1 import (
    invoke_real_ocr_provider_v1,
    normalize_ocr_native_result_v1,
    resolve_canonical_ocr_binding_v1,
)
from .types_v1 import (
    ProviderObservationIngressCaseV1,
    ProviderRuntimeRequestV1,
)


class RealOCRProviderExecutionEngineV1:
    """Execute one bounded OCR call, then hand off to existing cognition owners."""

    provider_invocation_authority = "Capability/Provider Runtime"
    provider_family = "ocr"
    execution_mode = "LIVE_RUNTIME"

    def __init__(self) -> None:
        self.ingress_engine = ProviderRuntimeObservationIngressEngineV1()

    @staticmethod
    def _failure(
        *,
        case: ProviderObservationIngressCaseV1,
        requirement_ref: str | None,
        resolution_status: str | None,
        request: ProviderRuntimeRequestV1 | None,
        provider_result: Any,
        provider: Any = None,
        details: Dict[str, Any],
        errors: Tuple[str, ...],
        attempted: bool,
        provider_invoked: bool = False,
        model_invoked: bool = False,
    ) -> Dict[str, Any]:
        return {
            "case_id": case.case_id,
            "case": case,
            "provider_request": request,
            "provider_result": provider_result,
            "provider": provider,
            "errors": list(errors),
            "details": details,
            "provider_real_execution_attempted": attempted,
            "provider_real_execution_verified": False,
            "provider_invoked": provider_invoked,
            "model_invoked": model_invoked,
            "capability_requirement_ref": requirement_ref,
            "capability_resolution_status": resolution_status,
        }

    def run(
        self,
        case: ProviderObservationIngressCaseV1,
        *,
        source_ref: str,
    ) -> Dict[str, Any]:
        if self.execution_mode != "LIVE_RUNTIME":
            return self._failure(
                case=case,
                requirement_ref=None,
                resolution_status=None,
                request=None,
                provider_result=None,
                details={"execution_mode": self.execution_mode},
                errors=("real_ocr_requires_live_runtime",),
                attempted=False,
            )

        case = dataclasses.replace(
            case,
            input_source_ref=source_ref,
            source_ref=source_ref,
            raw_result_ref=f"provider-native-output:{case.execution_instance_ref}",
        )
        fpo = self.ingress_engine._fpo_payload(case)
        fpo_record = FieldPerceptionActiveObservationControlEngineV1().run_case(fpo)
        requirement, assessment, resolution, resolution_errors = self.ingress_engine._resolve(case, fpo_record)
        details: Dict[str, Any] = {
            "execution_mode": self.execution_mode,
            "fpo": _jsonable(fpo_record),
        }
        if resolution_errors or requirement is None or resolution is None:
            return self._failure(
                case=case,
                requirement_ref=requirement.requirement_id if requirement else None,
                resolution_status=resolution.status if resolution else None,
                request=None,
                provider_result=None,
                details=details,
                errors=tuple(resolution_errors),
                attempted=False,
            )

        canonical_requirement_ref = (
            fpo_record.capability_requirement.requirement_id
            if fpo_record.capability_requirement
            else ""
        )
        binding, binding_errors = resolve_canonical_ocr_binding_v1()
        details["capability_assessment"] = _jsonable(assessment)
        details["capability_resolution"] = _jsonable(resolution)
        details["normalized_provider_requirement_ref"] = requirement.requirement_id
        details["canonical_binding"] = binding
        if binding_errors or binding is None:
            return self._failure(
                case=case,
                requirement_ref=canonical_requirement_ref,
                resolution_status=resolution.status,
                request=None,
                provider_result=None,
                details=details,
                errors=tuple(binding_errors),
                attempted=False,
            )

        trace_refs = tuple(dict.fromkeys((*fpo_record.demand.provenance_refs, fpo_record.trace.control_trace_ref)))
        provenance_refs = tuple(dict.fromkeys((*fpo_record.demand.provenance_refs, *binding["provenance_refs"])))
        provider_request = ProviderRuntimeRequestV1(
            provider_request_ref=f"provider-request:{case.execution_instance_ref}",
            observation_demand_ref=fpo_record.demand.demand_id,
            observation_request_ref=fpo_record.request.request_id if fpo_record.request else "",
            capability_requirement_ref=canonical_requirement_ref,
            capability_ref=resolution.module_ref,
            provider_ref=binding["provider_ref"],
            model_ref=binding["model_ref"],
            execution_instance_ref=case.execution_instance_ref,
            input_source_ref=source_ref,
            modality=case.modality,
            temporal_ref=case.temporal_ref,
            spatial_refs=case.spatial_refs,
            trace_refs=trace_refs,
            provenance_refs=provenance_refs,
            execution_mode=self.execution_mode,
            invocation_requested=True,
        )
        details["provider_request"] = _jsonable(provider_request)

        native = invoke_real_ocr_provider_v1(
            source_ref=source_ref,
            frame_id=f"ocr-frame:{case.execution_instance_ref}",
            timestamp_ms=0,
        )
        details["provider_native_result"] = native
        provider_result = normalize_ocr_native_result_v1(provider_request, binding, native)
        details["provider_runtime_result"] = _jsonable(provider_result)
        invoked = bool(native.get("provider_invoked"))
        model_invoked = bool(native.get("model_invoked"))
        observed_information_refs = (
            case.observation_information_refs
            if provider_result.status == "SUCCESS" and not provider_result.empty_result
            else ()
        )
        available_information_refs = tuple(
            dict.fromkeys((*case.available_information_refs, *observed_information_refs))
        )
        evidence_information_refs = case.evidence_information_refs or (
            (
                f"evidence:{case.execution_instance_ref}:1",
                tuple(observed_information_refs),
            ),
        ) if case.observation_information_refs else ()
        inherited_information_refs = (
            tuple(case.inherited_information_refs)
            if case.inherited_information_refs
            else tuple(case.available_information_refs)
        )
        if provider_result.status not in {"SUCCESS", "EMPTY_SUCCESS"}:
            return self._failure(
                case=case,
                requirement_ref=canonical_requirement_ref,
                resolution_status=resolution.status,
                request=provider_request,
                provider_result=provider_result,
                provider=native,
                details=details,
                errors=(f"provider:{provider_result.error_category or provider_result.status}",),
                attempted=True,
                provider_invoked=invoked,
                model_invoked=model_invoked,
            )

        envelope, adapter_errors = provider_result_to_runtime_observation(provider_request, provider_result)
        if adapter_errors or envelope is None:
            return self._failure(
                case=case,
                requirement_ref=canonical_requirement_ref,
                resolution_status=resolution.status,
                request=provider_request,
                provider_result=provider_result,
                provider=native,
                details=details,
                errors=tuple(adapter_errors),
                attempted=True,
                provider_invoked=invoked,
                model_invoked=model_invoked,
            )

        ingress_case = RuntimeObservationIngressCaseV1(
            case_id=case.case_id,
            title=case.title,
            observation=envelope,
            context_ref=case.context_ref,
            pcn_ref=f"pcn:{case.case_id}",
            intent_ref=case.intent_ref,
            role_refs=case.role_refs,
            task_refs=(case.task_ref,),
            goal_refs=(case.goal_ref,),
            concern_refs=(case.concern_ref,),
            information_need_refs=(case.information_need_ref,),
            field_refs=case.field_refs,
            relation_refs=case.relation_refs,
            required_information_refs=case.required_information_refs,
            available_information_refs=(
                available_information_refs
                if case.observation_information_refs or case.available_information_refs
                else case.required_information_refs
            ),
            evidence_information_refs=evidence_information_refs,
            inherited_information_refs=inherited_information_refs,
            cycle_index=case.cycle_index,
            prior_current_world_ref=case.prior_current_world_ref,
            prior_hypothesis_refs=case.prior_hypothesis_refs,
            prior_information_gap_ref=case.prior_information_gap_ref,
            prior_reobservation_ref=case.prior_reobservation_ref,
            prior_next_cycle_ingress_ref=case.prior_next_cycle_ingress_ref,
            prior_sufficiency_candidate=case.prior_sufficiency_candidate,
            prior_information_gap_candidate=case.prior_information_gap_candidate,
            prior_reobservation_candidate=case.prior_reobservation_candidate,
            synthetic_only=False,
            controlled_integration_only=True,
        )
        gateway = ObservationGatewayEngineV1().run_case(build_gateway_request(ingress_case))
        route = (
            ARouteOrchestrationEngineV1().run_case(build_aroute_request(ingress_case, gateway))
            if gateway.admission_state == "ADMITTED_OBSERVATION"
            else None
        )
        details["runtime_observation"] = _jsonable(envelope)
        details["gateway"] = _jsonable(gateway)
        details["a_route"] = _jsonable(route)
        proof = route.cognitive_execution if route else None
        errors = tuple(
            [f"gateway:{item.code}" for item in gateway.errors]
            + ([f"a_route:{item.code}" for item in route.errors] if route else [])
        )
        return {
            "case_id": case.case_id,
            "case": case,
            "provider_request": provider_request,
            "provider_result": provider_result,
            "provider": native,
            "runtime_observation_ref": envelope.observation_id,
            "gateway_admission_ref": gateway.runtime_admission.gateway_admission_ref if gateway.runtime_admission else None,
            "a_route_execution_ref": proof.execution_ref if proof else None,
            "sufficiency_ref": proof.sufficiency_ref if proof else None,
            "sufficiency_status": proof.sufficiency_status if proof else None,
            "information_gap_ref": proof.information_gap_ref if proof else None,
            "stop_ref": proof.stop_ref if proof else None,
            "evidence_refs": tuple(item.evidence_id for item in gateway.evidence),
            "errors": list(errors),
            "details": details,
            "provider_real_execution_attempted": True,
            "provider_real_execution_verified": bool(invoked and model_invoked and not errors),
            "provider_invoked": invoked,
            "model_invoked": model_invoked,
            "cognitive_proof": proof,
            "a_route_result": route,
            "available_information_refs": available_information_refs,
            "observed_information_refs": observed_information_refs,
            "evidence_information_refs": evidence_information_refs,
            "inherited_information_refs": inherited_information_refs,
            "capability_requirement_ref": canonical_requirement_ref,
            "capability_resolution_status": resolution.status,
        }


__all__ = ["RealOCRProviderExecutionEngineV1"]
