"""Compose existing demand, capability, provider, Gateway, and A-Route paths."""

from __future__ import annotations

from dataclasses import asdict
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
from capabilities.midplatform.model_manager.registry.provider_registry_loader_v1 import (
    filter_routing_eligible,
    list_capability_providers,
)
from capabilities.midplatform.model_manager.registries.universal_capability_slot.capability_scope_resolution_fixture_v1 import (
    _bind,
    _slot,
    build_scope_modules,
)
from capabilities.midplatform.model_manager.registries.universal_capability_slot.universal_capability_slot_resolution_v1 import (
    resolve_scoped_capability_requirement,
)
from capabilities.midplatform.model_manager.registries.universal_capability_slot.universal_capability_slot_types_v1 import (
    CapabilityRequirementV1,
)

from .provider_result_adapter_v1 import provider_result_to_runtime_observation
from .types_v1 import (
    ProviderObservationIngressCaseV1,
    ProviderRuntimeObservationResultV1,
    ProviderRuntimeRequestV1,
    ProviderRuntimeResultV1,
)


CAPABILITY_MAP: Dict[str, Dict[str, str]] = {
    "VISION_DETECTION": {
        "capability_ref": "object_detection",
        "module_id": "object_detection",
        "problem_class": "object_presence",
        "operation": "DETECT_OBJECT",
        "input_contract": "image_evidence",
        "output_contract": "object_candidate",
        "requirement_type": "OBJECT_DETECTION",
    },
    "OCR_TEXT_EVIDENCE": {
        "capability_ref": "text_recognition",
        "module_id": "text_recognition",
        "problem_class": "text_content",
        "operation": "READ_TEXT",
        "input_contract": "image_evidence",
        "output_contract": "text_candidate",
        "requirement_type": "TEXT_READ",
    },
    "SLAM_SPATIAL_EVIDENCE": {
        "capability_ref": "spatial_mapping",
        "module_id": "spatial_mapping",
        "problem_class": "spatial_structure",
        "operation": "PROVIDE_SPATIAL_STRUCTURE",
        "input_contract": "pose_candidate",
        "output_contract": "spatial_map_candidate",
        "requirement_type": "SPATIAL_MAP",
    },
}


def _jsonable(value: Any) -> Any:
    if hasattr(value, "__dataclass_fields__"):
        return {key: _jsonable(item) for key, item in asdict(value).items()}
    if isinstance(value, dict):
        return {key: _jsonable(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_jsonable(item) for item in value]
    return value


class ProviderRuntimeObservationIngressEngineV1:
    """Provider-result bridge; it never invokes a provider itself."""

    provider_invocation_authority = "Capability/Provider Runtime"
    real_provider_execution = False

    @staticmethod
    def _fpo_payload(case: ProviderObservationIngressCaseV1) -> Dict[str, Any]:
        return {
            "case_id": case.case_id,
            "root_cycle_trace_id": f"root-cycle:{case.execution_instance_ref}",
            "context_refs": (case.context_ref,),
            "intent_ref": case.intent_ref,
            "task_ref": case.task_ref,
            "field_refs": case.field_refs,
            "information_need": case.information_need_ref,
            "expected_evidence_kinds": case.expected_evidence_kinds,
            "target_semantic": case.goal_ref,
            "target_region": "controlled-runtime-region",
            "requested_capability_kinds": (case.capability_kind,),
            "observation_goal": case.information_need_ref,
            "provider_admission_candidate": True,
            "received_evidence_refs": (f"provider-result:{case.case_id}",),
            "received_evidence_kinds": case.expected_evidence_kinds,
            "target_coverage": True,
            "semantic_coverage": True,
            "spatial_coverage": True,
            "next_cycle_requested": case.next_cycle_requested,
            "resource_budget": {"provider_calls": 1, "frames": 1},
        }

    @staticmethod
    def _universal_requirement(case: ProviderObservationIngressCaseV1, fpo: Any) -> CapabilityRequirementV1 | None:
        mapping = CAPABILITY_MAP.get(case.capability_kind)
        if mapping is None or fpo.capability_requirement is None:
            return None
        candidate = fpo.capability_requirement
        return CapabilityRequirementV1(
            requirement_id=f"provider-requirement:{case.case_id}",
            requested_module_id=mapping["module_id"],
            purpose=mapping["capability_ref"],
            task_context=case.information_need_ref,
            required_semantic_depth="EVIDENCE_CANDIDATE",
            permission_refs=("permission:capability-governance",),
            resource_refs=("resource:controlled-provider-runtime",),
            execution_boundary_ref="Observation Gateway / Field Perception Orchestrator",
            requester_ref=candidate.observation_request_ref,
            requirement_type=mapping["requirement_type"],
            problem_class=mapping["problem_class"],
            requested_operation=mapping["operation"],
            input_contract_ref=mapping["input_contract"],
            expected_output_contract_ref=mapping["output_contract"],
            required_authority="EVIDENCE_ONLY",
            task_context_refs=(case.context_ref, case.task_ref, case.goal_ref),
            trace_ref=candidate.trace_ref,
        )

    @staticmethod
    def _resolve(case: ProviderObservationIngressCaseV1, fpo: Any) -> Tuple[Any, Any, Any, Tuple[str, ...]]:
        requirement = ProviderRuntimeObservationIngressEngineV1._universal_requirement(case, fpo)
        if requirement is None:
            return None, None, None, ("capability_unresolved",)
        modules = build_scope_modules()
        module = next((item for item in modules if item.module_id == requirement.requested_module_id), None)
        if module is None:
            return requirement, None, None, ("capability_module_unresolved",)
        slot = _bind(module, _slot(f"slot:provider-runtime:{module.module_id}"))
        assessment, resolution, gap = resolve_scoped_capability_requirement(requirement, modules, (slot,))
        errors = () if assessment.in_scope and resolution.status == "READY_CANDIDATE" else ("capability_resolution_not_ready",)
        return requirement, assessment, resolution, errors

    @staticmethod
    def _select_provider(capability_ref: str) -> Dict[str, Any] | None:
        providers = filter_routing_eligible(list_capability_providers(capability_ref))
        return providers[0] if providers else None

    @staticmethod
    def _provider_request(
        case: ProviderObservationIngressCaseV1,
        fpo: Any,
        requirement: CapabilityRequirementV1,
        provider: Dict[str, Any],
        *,
        next_cycle_ingress_ref: str | None = None,
    ) -> ProviderRuntimeRequestV1:
        provider_id = str(provider["model_id"])
        trace_refs = tuple(
            ref for ref in (
                fpo.demand.trace_ref,
                fpo.request.trace_ref if fpo.request else None,
                fpo.capability_requirement.trace_ref if fpo.capability_requirement else None,
                fpo.provider_session.trace_ref if fpo.provider_session else None,
                next_cycle_ingress_ref,
            ) if ref
        )
        provenance = tuple(dict.fromkeys((*fpo.demand.provenance_refs, *trace_refs)))
        return ProviderRuntimeRequestV1(
            provider_request_ref=f"provider-request:{case.case_id}",
            observation_demand_ref=fpo.demand.demand_id,
            observation_request_ref=fpo.request.request_id if fpo.request else "",
            capability_requirement_ref=requirement.requirement_id,
            capability_ref=CAPABILITY_MAP[case.capability_kind]["capability_ref"],
            provider_ref=f"provider:{provider_id}",
            model_ref=f"model:{provider_id}",
            execution_instance_ref=case.execution_instance_ref,
            input_source_ref=case.input_source_ref,
            modality=case.modality,
            temporal_ref=case.temporal_ref,
            spatial_refs=case.spatial_refs,
            trace_refs=trace_refs,
            provenance_refs=provenance,
            invocation_requested=False,
        )

    @staticmethod
    def _provider_result(case: ProviderObservationIngressCaseV1, request: ProviderRuntimeRequestV1) -> ProviderRuntimeResultV1:
        return ProviderRuntimeResultV1(
            provider_result_ref=f"provider-result:{case.case_id}",
            provider_request_ref=request.provider_request_ref,
            provider_ref=request.provider_ref,
            capability_ref=request.capability_ref,
            model_ref=request.model_ref,
            execution_instance_ref=request.execution_instance_ref,
            modality=request.modality,
            output_ref=f"provider-output:{case.case_id}",
            raw_result_ref=case.raw_result_ref,
            status=case.provider_result_status,
            confidence_candidate=case.confidence_candidate,
            quality_candidate=case.quality_candidate,
            temporal_ref=case.temporal_ref,
            spatial_refs=case.spatial_refs,
            trace_refs=request.trace_refs,
            provenance_refs=request.provenance_refs,
        )

    def run_case(self, case: ProviderObservationIngressCaseV1) -> ProviderRuntimeObservationResultV1:
        fpo = FieldPerceptionActiveObservationControlEngineV1().run_case(self._fpo_payload(case))
        requirement, assessment, resolution, resolution_errors = self._resolve(case, fpo)
        details: Dict[str, Any] = {"fpo": _jsonable(fpo)}
        if resolution_errors or requirement is None or resolution is None:
            return ProviderRuntimeObservationResultV1(
                case_id=case.case_id,
                capability_requirement_ref=requirement.requirement_id if requirement else None,
                capability_resolution_status=resolution.status if resolution else None,
                provider_request=None,
                provider_result=None,
                runtime_observation_ref=None,
                gateway_admission_ref=None,
                a_route_execution_ref=None,
                sufficiency_ref=None,
                information_gap_ref=None,
                stop_ref=None,
                demand_ref=fpo.demand.demand_id,
                observation_request_ref=fpo.request.request_id if fpo.request else None,
                reobservation_request_ref=None,
                next_cycle_ingress_ref=fpo.next_cycle_ingress.ingress_id if fpo.next_cycle_ingress else None,
                errors=tuple(resolution_errors),
                provider_runtime_contract_verified=False,
                details=details,
            )
        provider = self._select_provider(requirement.purpose)
        if provider is None:
            return ProviderRuntimeObservationResultV1(
                case_id=case.case_id,
                capability_requirement_ref=requirement.requirement_id,
                capability_resolution_status=resolution.status,
                provider_request=None,
                provider_result=None,
                runtime_observation_ref=None,
                gateway_admission_ref=None,
                a_route_execution_ref=None,
                sufficiency_ref=None,
                information_gap_ref=None,
                stop_ref=None,
                demand_ref=fpo.demand.demand_id,
                observation_request_ref=fpo.request.request_id if fpo.request else None,
                reobservation_request_ref=None,
                next_cycle_ingress_ref=fpo.next_cycle_ingress.ingress_id if fpo.next_cycle_ingress else None,
                errors=("provider_unresolved",),
                provider_runtime_contract_verified=False,
                details=details,
            )
        provider_request = self._provider_request(
            case,
            fpo,
            requirement,
            provider,
            next_cycle_ingress_ref=fpo.next_cycle_ingress.ingress_id if fpo.next_cycle_ingress else None,
        )
        provider_result = self._provider_result(case, provider_request)
        details["capability_assessment"] = _jsonable(assessment)
        details["capability_resolution"] = _jsonable(resolution)
        details["provider"] = provider
        details["provider_result"] = _jsonable(provider_result)
        if provider_result.status not in {"SUCCESS", "EMPTY_SUCCESS"}:
            return ProviderRuntimeObservationResultV1(
                case_id=case.case_id,
                capability_requirement_ref=requirement.requirement_id,
                capability_resolution_status=resolution.status,
                provider_request=provider_request,
                provider_result=provider_result,
                runtime_observation_ref=None,
                gateway_admission_ref=None,
                a_route_execution_ref=None,
                sufficiency_ref=None,
                information_gap_ref=None,
                stop_ref=None,
                demand_ref=fpo.demand.demand_id,
                observation_request_ref=fpo.request.request_id if fpo.request else None,
                reobservation_request_ref=None,
                next_cycle_ingress_ref=fpo.next_cycle_ingress.ingress_id if fpo.next_cycle_ingress else None,
                errors=("provider_result_unavailable",) if provider_result.status == "UNAVAILABLE" else ("provider_result_not_successful",),
                provider_runtime_contract_verified=True,
                details=details,
            )
        envelope, adapter_errors = provider_result_to_runtime_observation(provider_request, provider_result)
        if adapter_errors or envelope is None:
            return ProviderRuntimeObservationResultV1(
                case_id=case.case_id,
                capability_requirement_ref=requirement.requirement_id,
                capability_resolution_status=resolution.status,
                provider_request=provider_request,
                provider_result=provider_result,
                runtime_observation_ref=None,
                gateway_admission_ref=None,
                a_route_execution_ref=None,
                sufficiency_ref=None,
                information_gap_ref=None,
                stop_ref=None,
                demand_ref=fpo.demand.demand_id,
                observation_request_ref=fpo.request.request_id if fpo.request else None,
                reobservation_request_ref=None,
                next_cycle_ingress_ref=fpo.next_cycle_ingress.ingress_id if fpo.next_cycle_ingress else None,
                errors=adapter_errors,
                provider_runtime_contract_verified=True,
                details=details,
            )
        details["runtime_observation"] = _jsonable(envelope)
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
            available_information_refs=case.available_information_refs,
        )
        gateway = ObservationGatewayEngineV1().run_case(build_gateway_request(ingress_case))
        details["gateway"] = _jsonable(gateway)
        route = None
        if gateway.admission_state == "ADMITTED_OBSERVATION":
            route = ARouteOrchestrationEngineV1().run_case(build_aroute_request(ingress_case, gateway))
        details["a_route"] = _jsonable(route)
        proof = route.cognitive_execution if route else None
        errors = tuple(
            [f"gateway:{item.code}" for item in gateway.errors]
            + ([f"a_route:{item.code}" for item in route.errors] if route else [])
        )
        return ProviderRuntimeObservationResultV1(
            case_id=case.case_id,
            capability_requirement_ref=requirement.requirement_id,
            capability_resolution_status=resolution.status,
            provider_request=provider_request,
            provider_result=provider_result,
            runtime_observation_ref=envelope.observation_id,
            gateway_admission_ref=gateway.runtime_admission.gateway_admission_ref if gateway.runtime_admission else None,
            a_route_execution_ref=proof.execution_ref if proof else None,
            sufficiency_ref=proof.sufficiency_ref if proof else None,
            information_gap_ref=proof.information_gap_ref if proof else None,
            stop_ref=proof.stop_ref if proof else None,
            demand_ref=fpo.demand.demand_id,
            observation_request_ref=fpo.request.request_id if fpo.request else None,
            reobservation_request_ref=None,
            next_cycle_ingress_ref=fpo.next_cycle_ingress.ingress_id if fpo.next_cycle_ingress else None,
            evidence_refs=tuple(item.evidence_id for item in gateway.evidence),
            errors=errors,
            provider_runtime_contract_verified=not errors,
            provider_real_execution_verified=False,
            details=details,
        )

    def build_reobservation_provider_request(self, case: ProviderObservationIngressCaseV1) -> ProviderRuntimeObservationResultV1:
        reobserve_case = ProviderObservationIngressCaseV1(**{**case.__dict__, "next_cycle_requested": True})
        fpo = FieldPerceptionActiveObservationControlEngineV1().run_case(self._fpo_payload(reobserve_case))
        requirement, assessment, resolution, resolution_errors = self._resolve(reobserve_case, fpo)
        details: Dict[str, Any] = {"fpo": _jsonable(fpo)}
        if resolution_errors or requirement is None or resolution is None:
            return ProviderRuntimeObservationResultV1(
                case_id=reobserve_case.case_id,
                capability_requirement_ref=requirement.requirement_id if requirement else None,
                capability_resolution_status=resolution.status if resolution else None,
                provider_request=None,
                provider_result=None,
                runtime_observation_ref=None,
                gateway_admission_ref=None,
                a_route_execution_ref=None,
                sufficiency_ref=None,
                information_gap_ref=None,
                stop_ref=None,
                demand_ref=fpo.demand.demand_id,
                observation_request_ref=fpo.request.request_id if fpo.request else None,
                reobservation_request_ref=None,
                next_cycle_ingress_ref=fpo.next_cycle_ingress.ingress_id if fpo.next_cycle_ingress else None,
                errors=tuple(resolution_errors),
                details=details,
            )
        provider = self._select_provider(requirement.purpose)
        if provider is None:
            return ProviderRuntimeObservationResultV1(
                case_id=reobserve_case.case_id,
                capability_requirement_ref=requirement.requirement_id,
                capability_resolution_status=resolution.status,
                provider_request=None,
                provider_result=None,
                runtime_observation_ref=None,
                gateway_admission_ref=None,
                a_route_execution_ref=None,
                sufficiency_ref=None,
                information_gap_ref=None,
                stop_ref=None,
                demand_ref=fpo.demand.demand_id,
                observation_request_ref=fpo.request.request_id if fpo.request else None,
                reobservation_request_ref=None,
                next_cycle_ingress_ref=fpo.next_cycle_ingress.ingress_id if fpo.next_cycle_ingress else None,
                errors=("provider_unresolved",),
                details=details,
            )
        request = self._provider_request(
            reobserve_case,
            fpo,
            requirement,
            provider,
            next_cycle_ingress_ref=fpo.next_cycle_ingress.ingress_id if fpo.next_cycle_ingress else None,
        )
        request = ProviderRuntimeRequestV1(
            **{**request.__dict__, "provider_request_ref": f"{request.provider_request_ref}:reobserve"}
        )
        details["capability_assessment"] = _jsonable(assessment)
        details["capability_resolution"] = _jsonable(resolution)
        details["provider"] = provider
        return ProviderRuntimeObservationResultV1(
            case_id=reobserve_case.case_id,
            capability_requirement_ref=requirement.requirement_id,
            capability_resolution_status=resolution.status,
            provider_request=request,
            provider_result=None,
            runtime_observation_ref=None,
            gateway_admission_ref=None,
            a_route_execution_ref=None,
            sufficiency_ref=None,
            information_gap_ref=None,
            stop_ref=None,
            demand_ref=fpo.demand.demand_id,
            observation_request_ref=fpo.request.request_id if fpo.request else None,
            reobservation_request_ref=request.provider_request_ref,
            next_cycle_ingress_ref=fpo.next_cycle_ingress.ingress_id if fpo.next_cycle_ingress else None,
            errors=(),
            provider_runtime_contract_verified=False,
            provider_real_execution_verified=False,
            provider_invocation=False,
            model_invocation=False,
            details=details,
        )
