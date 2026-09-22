"""LIVE_RUNTIME bridge for one existing local YOLO11n provider.

This module is intentionally narrow: Capability/Provider Runtime owns the
provider call, while the existing provider-result adapter, Observation
Gateway, A-Route, and Cognitive State Formation remain the downstream path.
No downstream execution authority is invoked here.
"""

from __future__ import annotations

import dataclasses
import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

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
from capabilities.midplatform.field_perception_orchestrator.integration.canonical_yolo11n_binding_seam_v1 import (
    build_canonical_yolo11n_provider_admission_v1,
)
from capabilities.midplatform.field_perception_orchestrator.integration.canonical_yolo11n_context_builder_v1 import (
    build_canonical_yolo11n_context_v1,
)
from capabilities.midplatform.field_perception_orchestrator.integration.field_perception_real_vision_provider_adapter_v1 import (
    run_authorized_vision_provider_v1,
)
from capabilities.midplatform.field_perception_orchestrator.integration.raw_camera_stream_adapter_v1 import (
    adapt_raw_camera_source,
)
from capabilities.midplatform.core.cognitive_flow.integration.governed_capability_execution_record_production_controlled.yolo11n_producer_entry_v1 import (
    adapt_governed_bundle_to_canonical_yolo11n_records_v1,
    produce_yolo11n_governed_execution_records_v1,
)
from capabilities.midplatform.permission_and_admission_manager.module.runtime_execution_grant_v1 import (
    RuntimeExecutionGrantDecisionV1,
)
from capabilities.midplatform.model_manager.model_contract_repository.yolo11n_external_provisioning.yolo11n_external_provisioning_types_v1 import (
    resolve_yolo11n_external_provisioning_v1,
)
from capabilities.vision_runtime.yolo_candidate_adapter_v0 import _image_size_v0

from .engine_v1 import ProviderRuntimeObservationIngressEngineV1, _jsonable
from .provider_result_adapter_v1 import provider_result_to_runtime_observation
from .types_v1 import (
    ProviderObservationIngressCaseV1,
    ProviderRuntimeRequestV1,
    ProviderRuntimeResultV1,
)


MODEL_ASSET_ID = "model-asset:yolo11n:weights-v1"
MODEL_GOVERNED_PATH = "vision/detection/yolo/yolo11n.pt"
PROVIDER_REF = "provider:yolo:local:v1"
MODEL_REGISTRY_RELATIVE = "capabilities/midplatform/model_manager/registries/model_registry_v1.json"


def _unique(*groups: Tuple[str, ...]) -> Tuple[str, ...]:
    return tuple(dict.fromkeys(item for group in groups for item in group if str(item).strip()))


def _sha256(path: Path) -> Optional[str]:
    if not path.is_file():
        return None
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _declared_checksum(repo_root: Path) -> Optional[str]:
    try:
        payload = json.loads((repo_root / MODEL_REGISTRY_RELATIVE).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    for model in payload.get("models", ()) if isinstance(payload, dict) else ():
        if isinstance(model, dict) and model.get("model_asset_id") == MODEL_ASSET_ID:
            value = str(model.get("declared_checksum") or "").strip()
            return value or None
    return None


def _dependency_status() -> str:
    """Check import availability without importing or invoking the provider."""
    try:
        available = bool(importlib.util.find_spec("ultralytics") and importlib.util.find_spec("torch"))
    except (ImportError, ModuleNotFoundError, ValueError):
        available = False
    return "PYTHON_DEPENDENCY_VERIFIED" if available else "PYTHON_DEPENDENCY_UNRESOLVED"


def _provider_result(
    request: ProviderRuntimeRequestV1,
    provider: Any,
) -> ProviderRuntimeResultV1:
    accepted = bool(provider.accepted)
    detections = tuple(provider.detections or ())
    provider_trace = str(provider.trace_ref)
    native_output_ref = (
        detections[0].provider_output_ref
        if detections
        else f"{provider_trace}:empty-output"
    )
    status = "SUCCESS" if accepted and detections else "EMPTY_SUCCESS" if accepted else "ERROR"
    error_ref = f"{provider_trace}:error" if provider.error_code else ""
    return ProviderRuntimeResultV1(
        provider_result_ref=f"provider-result:{request.execution_instance_ref}:{provider_trace}",
        provider_request_ref=request.provider_request_ref,
        provider_ref=request.provider_ref,
        capability_ref=request.capability_ref,
        model_ref=request.model_ref,
        execution_instance_ref=request.execution_instance_ref,
        modality=request.modality,
        output_ref=native_output_ref,
        raw_result_ref=error_ref or f"{provider_trace}:native-output",
        status=status,
        confidence_candidate=max((item.confidence for item in detections), default=None),
        quality_candidate=None if not detections else 0.8,
        temporal_ref=request.temporal_ref,
        spatial_refs=request.spatial_refs,
        trace_refs=_unique(request.trace_refs, (provider_trace,), tuple(item.provider_trace_ref for item in detections)),
        provenance_refs=_unique(request.provenance_refs, tuple(provider.provenance_refs or ()), (provider_trace,)),
        empty_result=accepted and not detections,
        candidate_only=True,
        truth_declared=False,
        provider_invoked=bool(provider.invocation_performed),
        model_invoked=bool(provider.invocation_performed),
    )


class RealProviderExecutionEngineV1:
    """Execute exactly one bounded local provider call under LIVE_RUNTIME."""

    provider_invocation_authority = "Capability/Provider Runtime"
    provider_family = "yolo"
    execution_mode = "LIVE_RUNTIME"

    def __init__(self, repo_root: Path) -> None:
        self.repo_root = repo_root
        self.ingress_engine = ProviderRuntimeObservationIngressEngineV1()

    def run(
        self,
        case: ProviderObservationIngressCaseV1,
        *,
        source_ref: str,
        model_path: str,
        runtime_authorization_grant: Optional[RuntimeExecutionGrantDecisionV1] = None,
    ) -> Dict[str, Any]:
        if self.execution_mode != "LIVE_RUNTIME":
            return {"case_id": case.case_id, "errors": ["real_provider_requires_live_runtime"]}

        case = dataclasses.replace(
            case,
            input_source_ref=source_ref,
            source_ref=source_ref,
            raw_result_ref=f"provider-native-output:{case.execution_instance_ref}",
        )
        fpo = self.ingress_engine._fpo_payload(case)
        fpo_record = FieldPerceptionActiveObservationControlEngineV1().run_case(fpo)
        requirement, assessment, resolution, resolution_errors = self.ingress_engine._resolve(case, fpo_record)
        details: Dict[str, Any] = {"fpo": _jsonable(fpo_record), "execution_mode": self.execution_mode}
        if resolution_errors or requirement is None or resolution is None:
            return {"case_id": case.case_id, "errors": list(resolution_errors), "details": details}

        # Provider admission requires the canonical FPO capability
        # requirement identity. The normalized provider-runtime resolution
        # view has a separate provider-requirement identity, so retain the
        # source requirement when crossing into provider admission.
        capability_requirement_ref = (
            fpo_record.capability_requirement.requirement_id
            if fpo_record.capability_requirement
            else ""
        )

        produced = produce_yolo11n_governed_execution_records_v1(self.repo_root)
        records = adapt_governed_bundle_to_canonical_yolo11n_records_v1(produced.bundle) if produced.bundle else None
        context_result = build_canonical_yolo11n_context_v1(records)
        details["governed_record_production"] = _jsonable(produced)
        details["canonical_context"] = _jsonable(context_result)

        trace_refs = _unique(
            tuple(fpo_record.demand.provenance_refs),
            (fpo_record.trace.control_trace_ref,),
            tuple(context_result.validation.trace_refs),
        )
        provenance_refs = _unique(
            tuple(fpo_record.demand.provenance_refs),
            tuple(context_result.validation.provenance_refs),
        )
        provider_request = ProviderRuntimeRequestV1(
            provider_request_ref=f"provider-request:{case.execution_instance_ref}",
            observation_demand_ref=fpo_record.demand.demand_id,
            observation_request_ref=fpo_record.request.request_id if fpo_record.request else "",
            capability_requirement_ref=capability_requirement_ref,
            capability_ref=resolution.module_ref,
            provider_ref=PROVIDER_REF,
            model_ref=MODEL_ASSET_ID,
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

        declared = _declared_checksum(self.repo_root)
        observed = _sha256(Path(model_path))
        manager_admission = resolve_yolo11n_external_provisioning_v1({
            "target_model_asset_id": MODEL_ASSET_ID,
            "target_governed_path": MODEL_GOVERNED_PATH,
            "source_file_ref": model_path,
            "observed_path": model_path,
            "provenance_ref": "provenance:yolo11n:real-provider-execution:v1",
            "declared_checksum": declared,
            "observed_checksum": observed,
            "dependency_status": _dependency_status(),
            "candidate_only": True,
        })
        source_width, source_height = _image_size_v0(Path(source_ref))
        raw = adapt_raw_camera_source(
            source_ref,
            source_type="IMAGE_FILE",
            observation_demand_ref=fpo_record.demand.demand_id,
            capability_requirement_ref=capability_requirement_ref,
            source_mode="REAL",
            session_id=f"real-provider-session:{case.execution_instance_ref}",
            frame_id=f"real-provider-frame:{case.execution_instance_ref}",
            width=source_width,
            height=source_height,
            max_frames=1,
            max_duration_ms=5000,
        )
        frame = raw.frames[0] if raw.frames else None
        admission_result = build_canonical_yolo11n_provider_admission_v1(
            context=context_result.context,
            observation_demand_ref=fpo_record.demand.demand_id,
            observation_request_ref=fpo_record.request.request_id if fpo_record.request else "",
            capability_requirement_ref=capability_requirement_ref,
            provider_session_ref=fpo_record.provider_session.session_id if fpo_record.provider_session else "",
            provider_candidate_ref=PROVIDER_REF,
            region_scope_candidate=fpo_record.request.target_region_candidate if fpo_record.request else "bounded-single-frame",
            expected_evidence=("VISION_DETECTION",),
            bounded=True,
            trace_ref=fpo_record.trace.control_trace_ref,
        )
        admission = admission_result.admission
        if manager_admission.technical_admission_status != "ADMISSION_READY_CANDIDATE" or not raw.accepted:
            admission = dataclasses.replace(admission, provider_invocation_authorized=False)
        details["model_admission"] = _jsonable(manager_admission)
        details["raw_source"] = _jsonable(raw)
        details["provider_admission"] = _jsonable(admission)

        provider = run_authorized_vision_provider_v1(
            frame,
            admission,
            execute_real_provider=True,
            model_path=model_path,
            runtime_authorization_grant=runtime_authorization_grant,
        )
        provider_result = _provider_result(provider_request, provider)
        details["provider_native_result"] = _jsonable(provider)
        details["provider_result"] = _jsonable(provider_result)
        if not provider.accepted:
            return {
                "case_id": case.case_id,
                "case": case,
                "provider_request": provider_request,
                "provider_result": provider_result,
                "provider": provider,
                "errors": [provider.error_code or "provider_not_accepted"],
                "details": details,
                "provider_real_execution_attempted": True,
                "provider_real_execution_verified": False,
                "provider_invoked": bool(provider.invocation_performed),
                "model_invoked": bool(provider.invocation_performed),
            }

        envelope, adapter_errors = provider_result_to_runtime_observation(provider_request, provider_result)
        if adapter_errors or envelope is None:
            return {
                "case_id": case.case_id,
                "case": case,
                "provider_request": provider_request,
                "provider_result": provider_result,
                "provider": provider,
                "errors": list(adapter_errors),
                "details": details,
                "provider_real_execution_attempted": True,
                "provider_real_execution_verified": False,
                "provider_invoked": bool(provider.invocation_performed),
                "model_invoked": bool(provider.invocation_performed),
            }

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
            available_information_refs=case.required_information_refs if provider.evidence else (),
            synthetic_only=False,
            controlled_integration_only=True,
        )
        gateway = ObservationGatewayEngineV1().run_case(build_gateway_request(ingress_case))
        route = ARouteOrchestrationEngineV1().run_case(build_aroute_request(ingress_case, gateway)) if gateway.admission_state == "ADMITTED_OBSERVATION" else None
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
            "provider": provider,
            "runtime_observation_ref": envelope.observation_id,
            "gateway_admission_ref": gateway.runtime_admission.gateway_admission_ref if gateway.runtime_admission else None,
            "a_route_execution_ref": proof.execution_ref if proof else None,
            "sufficiency_ref": proof.sufficiency_ref if proof else None,
            "information_gap_ref": proof.information_gap_ref if proof else None,
            "stop_ref": proof.stop_ref if proof else None,
            "evidence_refs": tuple(item.evidence_id for item in gateway.evidence),
            "errors": list(errors),
            "details": details,
            "provider_real_execution_attempted": True,
            "provider_real_execution_verified": bool(provider.invocation_performed and provider.accepted and not errors),
            "provider_invoked": bool(provider.invocation_performed),
            "model_invoked": bool(provider.invocation_performed),
        }


__all__ = ["RealProviderExecutionEngineV1"]
