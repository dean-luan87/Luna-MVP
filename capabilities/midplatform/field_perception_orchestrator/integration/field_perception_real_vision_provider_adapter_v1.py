from __future__ import annotations

import hashlib
import time
from pathlib import Path
from typing import Any, Iterable, Mapping, Optional, Sequence, Tuple

from capabilities.midplatform.field_perception_orchestrator.integration.field_perception_real_vision_evidence_types_v1 import (
    CAPABILITY_KIND,
    ObservationGatewayEvidenceHandoffCandidateV1,
    ProviderNativeDetectionRecordV1,
    VisionProviderAdapterResultV1,
    VisionProviderAdmissionCandidateV1,
    VisualDetectionEvidenceCandidateV1,
)
from capabilities.midplatform.field_perception_orchestrator.integration.raw_camera_stream_types_v1 import (
    RawFrameRecordV1,
)
from capabilities.midplatform.permission_and_admission_manager.module.runtime_authorization_state_v1 import (
    query_active_authorization_for_grant,
)
from capabilities.midplatform.permission_and_admission_manager.module.runtime_execution_grant_v1 import (
    RuntimeExecutionGrantDecisionV1,
)
from capabilities.vision_runtime.yolo_candidate_adapter_v0 import (
    build_yolo_like_fixture_detections_v0,
    run_yolo_on_unit_v0,
)


def _digest(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:20]


def _result(
    *,
    frame: Optional[RawFrameRecordV1],
    admission: Optional[VisionProviderAdmissionCandidateV1],
    accepted: bool,
    invocation_performed: bool,
    detector_mode: str,
    error_code: str,
    provider: str = "yolo_candidate_adapter",
    model_ref: str = "",
    detections: Sequence[ProviderNativeDetectionRecordV1] = (),
    evidence: Sequence[VisualDetectionEvidenceCandidateV1] = (),
    gateway_handoff: Optional[ObservationGatewayEvidenceHandoffCandidateV1] = None,
    duplicate: bool = False,
    provider_error_stage: str = "",
    provider_error_detail: str = "",
) -> VisionProviderAdapterResultV1:
    frame_ref = frame.frame_id if frame else ""
    admission_ref = admission.admission_id if admission else ""
    trace_ref = admission.trace_ref if admission else f"trace:s3:vision:{_digest(frame_ref or 'rejected')}"
    provenance_refs = admission.provenance_refs if admission else (trace_ref,)
    return VisionProviderAdapterResultV1(
        accepted=accepted,
        invocation_performed=invocation_performed,
        detector_mode=detector_mode,
        error_code=error_code,
        provider=provider,
        model_ref=model_ref,
        frame_ref=frame_ref,
        detections=tuple(detections),
        evidence=tuple(evidence),
        admission_ref=admission_ref,
        trace_ref=trace_ref,
        provenance_refs=tuple(provenance_refs),
        region_scope_candidate=admission.region_scope_candidate if admission else "",
        execution_scope_mode="bounded_frame_scope",
        region_scope_enforced=False,
        region_scope_limitation="reused provider path receives a bounded frame reference; pixel-ROI enforcement is not claimed",
        gateway_handoff=gateway_handoff,
        duplicate=duplicate,
        provider_error_stage=provider_error_stage,
        provider_error_detail=provider_error_detail,
    )


def build_vision_provider_admission_candidate_v1(
    *,
    observation_demand_ref: str,
    observation_request_ref: str,
    capability_requirement_ref: str,
    provider_session_ref: str,
    provider_candidate_ref: str,
    model_candidate_ref: str,
    model_admission_ref: str,
    region_scope_candidate: str,
    expected_evidence: Iterable[str],
    bounded: bool,
    provider_admitted: bool,
    trace_ref: str,
    provenance_refs: Iterable[str],
    provider_autonomous_execution: bool = False,
    canonical_capability_model_binding_ref: str = "",
    canonical_capability_model_binding_version: str = "",
    canonical_runtime_admission_ref: str = "",
    canonical_runtime_admission_version: str = "",
    canonical_model_provider_binding_ref: str = "",
    canonical_model_provider_binding_version: str = "",
    canonical_invalidation_refs: Iterable[str] = (),
    canonical_chain_validated: bool = False,
    require_canonical_chain: bool = False,
) -> VisionProviderAdmissionCandidateV1:
    required = (
        observation_demand_ref,
        observation_request_ref,
        capability_requirement_ref,
        provider_session_ref,
        provider_candidate_ref,
        model_candidate_ref,
        model_admission_ref,
        region_scope_candidate,
        trace_ref,
    )
    canonical_invalidation = tuple(dict.fromkeys(str(x) for x in canonical_invalidation_refs if str(x).strip()))
    canonical_chain_ready = bool(
        canonical_chain_validated
        and canonical_capability_model_binding_ref
        and canonical_capability_model_binding_version
        and canonical_runtime_admission_ref
        and canonical_runtime_admission_version
        and canonical_model_provider_binding_ref
        and canonical_model_provider_binding_version
        and not canonical_invalidation
    )
    authorized = bool(
        all(str(value).strip() for value in required)
        and capability_requirement_ref.startswith("capability-requirement")
        and bounded
        and provider_admitted
        and not provider_autonomous_execution
        and CAPABILITY_KIND in tuple(expected_evidence)
        and (not require_canonical_chain or canonical_chain_ready)
    )
    return VisionProviderAdmissionCandidateV1(
        admission_id=f"vision-admission:{_digest('|'.join(str(x) for x in required))}",
        observation_demand_ref=observation_demand_ref,
        observation_request_ref=observation_request_ref,
        capability_requirement_ref=capability_requirement_ref,
        required_capability_kind=CAPABILITY_KIND,
        provider_session_ref=provider_session_ref,
        provider_candidate_ref=provider_candidate_ref,
        model_candidate_ref=model_candidate_ref,
        model_admission_ref=model_admission_ref,
        region_scope_candidate=region_scope_candidate,
        expected_evidence=tuple(str(x) for x in expected_evidence),
        bounded=bool(bounded),
        provider_autonomous_execution=bool(provider_autonomous_execution),
        provider_invocation_authorized=authorized,
        trace_ref=trace_ref,
        provenance_refs=tuple(dict.fromkeys(str(x) for x in provenance_refs)),
        canonical_capability_model_binding_ref=canonical_capability_model_binding_ref,
        canonical_capability_model_binding_version=canonical_capability_model_binding_version,
        canonical_runtime_admission_ref=canonical_runtime_admission_ref,
        canonical_runtime_admission_version=canonical_runtime_admission_version,
        canonical_model_provider_binding_ref=canonical_model_provider_binding_ref,
        canonical_model_provider_binding_version=canonical_model_provider_binding_version,
        canonical_invalidation_refs=canonical_invalidation,
        canonical_chain_validated=canonical_chain_ready,
    )


def _provider_unit(frame: RawFrameRecordV1, region_scope: str) -> dict[str, Any]:
    width = max(1, int(frame.width or 1))
    height = max(1, int(frame.height or 1))
    return {
        "unit_id": f"vision-unit:{frame.frame_id}",
        "unit_type": "frame_roi",
        "roi_id": region_scope or "bounded_frame_scope",
        "bbox_in_frame": [0, 0, width, height],
        "image_ref": frame.frame_payload_ref,
        "source_frame_id": frame.frame_id,
        "coordinate_transform": {
            "offset_x": 0,
            "offset_y": 0,
            "source_frame_width": width,
            "source_frame_height": height,
            "transformed_width": width,
            "transformed_height": height,
        },
    }


def _native_detection(
    raw: Mapping[str, Any],
    *,
    frame: RawFrameRecordV1,
    admission: VisionProviderAdmissionCandidateV1,
    model_ref: str,
    index: int,
) -> ProviderNativeDetectionRecordV1:
    bbox_raw = tuple(float(x) for x in (raw.get("bbox_xyxy") or (0, 0, 0, 0)))
    bbox = (bbox_raw + (0.0, 0.0, 0.0, 0.0))[:4]
    detection_id = str(raw.get("detection_id") or f"yolo:{frame.frame_id}:{index}")
    return ProviderNativeDetectionRecordV1(
        detection_id=detection_id,
        provider_name="yolo_candidate_adapter",
        provider_version="existing-v0-adapter",
        model_ref=model_ref,
        frame_ref=frame.frame_id,
        class_id=int(raw["class_id"]) if raw.get("class_id") is not None else None,
        class_label=str(raw.get("class_name") or "unknown"),
        bbox=bbox,
        confidence=float(raw.get("confidence") or 0.0),
        region_ref=admission.region_scope_candidate,
        frame_dimensions=(int(frame.width), int(frame.height)),
        inference_timestamp=int(time.time() * 1000),
        provider_trace_ref=f"{admission.trace_ref}:provider",
        provider_output_ref=detection_id,
    )


def _evidence(
    native: ProviderNativeDetectionRecordV1,
    *,
    frame: RawFrameRecordV1,
    admission: VisionProviderAdmissionCandidateV1,
    detector_mode: str,
) -> VisualDetectionEvidenceCandidateV1:
    evidence_id = f"visual-evidence:{_digest(native.detection_id + detector_mode)}"
    evidence_trace = f"{admission.trace_ref}:evidence:{native.detection_id}"
    return VisualDetectionEvidenceCandidateV1(
        evidence_id=evidence_id,
        provider_ref=native.provider_name,
        model_ref=native.model_ref,
        frame_ref=frame.frame_id,
        detection_ref=native.detection_id,
        class_candidate=native.class_label,
        bbox=native.bbox,
        confidence=native.confidence,
        region_ref=native.region_ref,
        temporal_ref=frame.trace_ref,
        uncertainty_refs=(f"uncertainty:{evidence_id}",),
        contradiction_refs=(),
        trace_ref=evidence_trace,
        provenance_refs=tuple(dict.fromkeys((*admission.provenance_refs, evidence_trace))),
    )


def _gateway_handoff(
    evidence: Sequence[VisualDetectionEvidenceCandidateV1],
    *,
    frame: RawFrameRecordV1,
    admission: VisionProviderAdmissionCandidateV1,
) -> ObservationGatewayEvidenceHandoffCandidateV1:
    trace_ref = f"{admission.trace_ref}:observation-gateway-handoff"
    return ObservationGatewayEvidenceHandoffCandidateV1(
        handoff_id=f"gateway-handoff:{_digest(trace_ref)}",
        ingress_type="VISION",
        evidence_refs=tuple(item.evidence_id for item in evidence),
        provider_ref="yolo_candidate_adapter",
        source_frame_ref=frame.frame_id,
        raw_output_refs=tuple(item.detection_ref for item in evidence),
        trace_ref=trace_ref,
        provenance_refs=tuple(dict.fromkeys((*admission.provenance_refs, trace_ref))),
    )


def run_authorized_vision_provider_v1(
    frame: Optional[RawFrameRecordV1],
    admission: Optional[VisionProviderAdmissionCandidateV1],
    *,
    execute_real_provider: bool = False,
    model_path: str = "",
    runtime_authorization_grant: Optional[RuntimeExecutionGrantDecisionV1] = None,
    provider_failure: bool = False,
    budget_exhausted: bool = False,
    session_revoked: bool = False,
    seen_inference_ids: Iterable[str] = (),
    synthetic_zero_detections: bool = False,
) -> VisionProviderAdapterResultV1:
    """Run only after an explicit bounded provider admission candidate exists.

    Synthetic mode uses deterministic provider-shaped fixtures. Real mode calls
    the existing local-only YOLO candidate adapter and maps its native output;
    it never writes facts or downstream owner state.
    """
    if frame is None or not str(frame.frame_payload_ref).strip():
        return _result(frame=frame, admission=admission, accepted=False, invocation_performed=False, detector_mode="rejected", error_code="INVALID_FRAME_REF")
    if admission is not None and (
        admission.required_capability_kind != CAPABILITY_KIND
        or CAPABILITY_KIND not in admission.expected_evidence
    ):
        return _result(frame=frame, admission=admission, accepted=False, invocation_performed=False, detector_mode="rejected", error_code="INVALID_CAPABILITY_REQUIREMENT")
    if admission is not None and (not admission.trace_ref or not admission.provenance_refs):
        return _result(frame=frame, admission=admission, accepted=False, invocation_performed=False, detector_mode="rejected", error_code="TRACE_MISSING")
    if admission is None or not admission.provider_invocation_authorized:
        return _result(frame=frame, admission=admission, accepted=False, invocation_performed=False, detector_mode="rejected", error_code="PROVIDER_NOT_ADMITTED")
    if execute_real_provider and admission is not None and not admission.canonical_chain_validated:
        return _result(
            frame=frame,
            admission=admission,
            accepted=False,
            invocation_performed=False,
            detector_mode="rejected",
            error_code="PROVIDER_NOT_ADMITTED",
            provider_error_stage="canonical_binding_seam",
            provider_error_detail="canonical Capability/Model, Runtime Admission, and Model/Provider references are required before real invocation",
        )
    if execute_real_provider:
        owner_authorized = bool(
            isinstance(runtime_authorization_grant, RuntimeExecutionGrantDecisionV1)
            and runtime_authorization_grant.decision == "GRANTED"
            and runtime_authorization_grant.authoritative is True
            and runtime_authorization_grant.candidate_only is False
            and runtime_authorization_grant.execution_authorized is True
            and runtime_authorization_grant.validity_status == "FRESH"
            and not runtime_authorization_grant.revocation_ref
            and runtime_authorization_grant.provider_candidate_ref
            == admission.provider_candidate_ref
            and query_active_authorization_for_grant(runtime_authorization_grant)
            is not None
        )
        if not owner_authorized:
            return _result(
                frame=frame,
                admission=admission,
                accepted=False,
                invocation_performed=False,
                detector_mode="rejected",
                error_code="RUNTIME_AUTHORIZATION_NOT_CURRENT",
                provider_error_stage="runtime_authorization",
                provider_error_detail="current Permission / Admission Manager authorization is required before real invocation",
            )
    if execute_real_provider and admission is not None and admission.canonical_invalidation_refs:
        return _result(
            frame=frame,
            admission=admission,
            accepted=False,
            invocation_performed=False,
            detector_mode="rejected",
            error_code="PROVIDER_NOT_ADMITTED",
            provider_error_stage="canonical_binding_seam",
            provider_error_detail="canonical binding or admission references are invalidated",
        )
    if session_revoked:
        return _result(frame=frame, admission=admission, accepted=False, invocation_performed=False, detector_mode="rejected", error_code="SESSION_REVOKED")
    if budget_exhausted:
        return _result(frame=frame, admission=admission, accepted=False, invocation_performed=False, detector_mode="rejected", error_code="SESSION_BUDGET_EXHAUSTED")
    inference_id = f"inference:{frame.frame_id}:{admission.provider_session_ref}"
    if inference_id in frozenset(seen_inference_ids):
        return _result(frame=frame, admission=admission, accepted=False, invocation_performed=False, detector_mode="duplicate", error_code="DUPLICATE_INFERENCE_REQUEST", duplicate=True)

    unit = _provider_unit(frame, admission.region_scope_candidate)
    detector_mode = "REAL_YOLO" if execute_real_provider else "SYNTHETIC_PROVIDER_FIXTURE"
    model_ref = model_path or admission.model_candidate_ref
    raw_detections: Sequence[Mapping[str, Any]]
    invocation_performed = False
    if provider_failure:
        return _result(frame=frame, admission=admission, accepted=False, invocation_performed=False, detector_mode=detector_mode, error_code="PROVIDER_INVOCATION_FAILED", model_ref=model_ref)
    if execute_real_provider:
        if not model_path or not Path(model_path).is_file():
            return _result(frame=frame, admission=admission, accepted=False, invocation_performed=False, detector_mode=detector_mode, error_code="MODEL_NOT_AVAILABLE", model_ref=model_ref)
        try:
            raw_detections, provider_error = run_yolo_on_unit_v0(unit, model_path=model_path)
        except Exception as exc:
            return _result(
                frame=frame,
                admission=admission,
                accepted=False,
                invocation_performed=False,
                detector_mode=detector_mode,
                error_code="PROVIDER_INVOCATION_FAILED",
                model_ref=model_ref,
                provider_error_stage="run_yolo_on_unit_v0",
                provider_error_detail=f"{type(exc).__name__}: {exc}",
            )
        if provider_error:
            return _result(
                frame=frame,
                admission=admission,
                accepted=False,
                invocation_performed=True,
                detector_mode=detector_mode,
                error_code="PROVIDER_INVOCATION_FAILED",
                model_ref=model_ref,
                provider_error_stage="run_yolo_on_unit_v0",
                provider_error_detail=str(provider_error),
            )
        invocation_performed = True
    else:
        raw_detections = () if synthetic_zero_detections else build_yolo_like_fixture_detections_v0(unit)

    try:
        native = tuple(
            _native_detection(item, frame=frame, admission=admission, model_ref=model_ref, index=index)
            for index, item in enumerate(raw_detections)
        )
        evidence = tuple(_evidence(item, frame=frame, admission=admission, detector_mode=detector_mode) for item in native)
    except (KeyError, TypeError, ValueError):
        return _result(frame=frame, admission=admission, accepted=False, invocation_performed=invocation_performed, detector_mode=detector_mode, error_code="EVIDENCE_MAPPING_FAILED", model_ref=model_ref)
    return _result(frame=frame, admission=admission, accepted=True, invocation_performed=invocation_performed, detector_mode=detector_mode, error_code="", model_ref=model_ref, detections=native, evidence=evidence, gateway_handoff=_gateway_handoff(evidence, frame=frame, admission=admission))


def deduplicate_visual_evidence_v1(
    evidence: Sequence[VisualDetectionEvidenceCandidateV1],
    *,
    seen_evidence_ids: Iterable[str] = (),
) -> Tuple[Tuple[VisualDetectionEvidenceCandidateV1, ...], bool]:
    seen = frozenset(seen_evidence_ids)
    unique = tuple(item for item in evidence if item.evidence_id not in seen)
    return unique, len(unique) != len(tuple(evidence))


__all__ = [
    "build_vision_provider_admission_candidate_v1",
    "deduplicate_visual_evidence_v1",
    "run_authorized_vision_provider_v1",
]
