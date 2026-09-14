from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Optional


PROVIDER_STATUSES = (
    "SUCCESS_WITH_DETECTIONS",
    "SUCCESS_ZERO_DETECTIONS",
    "FAILED_WITH_DIAGNOSTIC",
)


@dataclass(frozen=True)
class YOLO11nSingleFrameExecutionResultV1:
    model_asset_id: str
    loader_contract_id: str
    provider_adapter_contract_id: str
    evidence_contract_id: str
    technical_admission_status: str
    commercial_license_status: str
    frame_ref: str
    model_ref: str
    provider_status: str
    model_load_executed: bool
    provider_invocation_executed: bool
    model_inference_executed: bool
    single_frame: bool
    invocation_count: int
    provider_error_stage: str
    provider_error_type: str
    provider_error_detail: str
    candidate_only: bool
    truth_declared: bool
    fact_admitted: bool
    provider_semantic_authority: bool
    field_state_direct_mutation: bool
    current_world_truth_declaration: bool
    intent_mutation: bool
    decision_mutation: bool
    task_mutation: bool
    ocr_execution: bool
    slam_execution: bool
    vlm_execution: bool
    semantic_interpretation: bool
    semantic_compression: bool
    network_access: bool
    automatic_model_download: bool
    automatic_package_download: bool
    automatic_dependency_install: bool
    provider_autonomous_continuous_execution: bool
    hidden_retry: bool
    raw_content_persisted: bool
    gateway_handoff_candidate: bool
    trace_ref: str
    provenance_refs: tuple[str, ...]


def provider_status_v1(provider: Any) -> str:
    accepted = bool(getattr(provider, "accepted", False))
    invoked = bool(getattr(provider, "invocation_performed", False))
    synthetic_success = str(getattr(provider, "detector_mode", "") or "") == "SYNTHETIC_PROVIDER_FIXTURE"
    if accepted and (invoked or synthetic_success):
        return "SUCCESS_WITH_DETECTIONS" if tuple(getattr(provider, "detections", ()) or ()) else "SUCCESS_ZERO_DETECTIONS"
    return "FAILED_WITH_DIAGNOSTIC"


def build_single_frame_execution_result_v1(
    *,
    manager_admission: Any,
    frame: Any,
    provider: Any,
    provider_adapter_contract_id: str,
    evidence_contract_id: str,
    model_load_executed: bool,
    invocation_count: int,
    provider_error_stage: str = "",
    provider_error_type: str = "",
    provider_error_detail: str = "",
) -> YOLO11nSingleFrameExecutionResultV1:
    status = provider_status_v1(provider)
    provider_error_stage = provider_error_stage or str(getattr(provider, "provider_error_stage", "") or "")
    provider_error_detail = provider_error_detail or str(getattr(provider, "provider_error_detail", "") or "")
    provider_error_type = provider_error_type or (str(getattr(provider, "error_code", "") or "") if status == "FAILED_WITH_DIAGNOSTIC" else "")
    evidence = tuple(getattr(provider, "evidence", ()) or ())
    return YOLO11nSingleFrameExecutionResultV1(
        model_asset_id=str(getattr(manager_admission, "target_asset_id", "model-asset:yolo11n:weights-v1")),
        loader_contract_id="loader:ultralytics:yolo:v1",
        provider_adapter_contract_id=provider_adapter_contract_id,
        evidence_contract_id=evidence_contract_id,
        technical_admission_status=str(getattr(manager_admission, "technical_admission_status", "ADMISSION_BLOCKED_CONTRACT")),
        commercial_license_status=str(getattr(manager_admission, "commercial_license_status", "REQUIRES_LICENSE_REVIEW")),
        frame_ref=str(getattr(provider, "frame_ref", "") or getattr(frame, "frame_id", "")),
        model_ref=str(getattr(provider, "model_ref", "")),
        provider_status=status,
        model_load_executed=bool(model_load_executed),
        provider_invocation_executed=bool(getattr(provider, "invocation_performed", False)),
        model_inference_executed=bool(status in {"SUCCESS_WITH_DETECTIONS", "SUCCESS_ZERO_DETECTIONS"} and getattr(provider, "invocation_performed", False)),
        single_frame=bool(frame is not None),
        invocation_count=int(invocation_count),
        provider_error_stage=provider_error_stage,
        provider_error_type=provider_error_type,
        provider_error_detail=provider_error_detail,
        candidate_only=bool(getattr(provider, "candidate_only", True)),
        truth_declared=any(bool(getattr(item, "truth_declared", False)) for item in evidence),
        fact_admitted=any(bool(getattr(item, "fact_admitted", False)) for item in evidence),
        provider_semantic_authority=bool(getattr(provider, "provider_semantic_authority", False)),
        field_state_direct_mutation=bool(getattr(provider, "field_mutation", False)),
        current_world_truth_declaration=bool(getattr(provider, "current_world_mutation", False)),
        intent_mutation=any(bool(getattr(item, "intent_created", False)) for item in evidence),
        decision_mutation=False,
        task_mutation=any(bool(getattr(item, "task_created", False)) for item in evidence),
        ocr_execution=bool(getattr(provider, "ocr_invocation", False)),
        slam_execution=bool(getattr(provider, "slam_invocation", False)),
        vlm_execution=bool(getattr(provider, "vlm_invocation", False)),
        semantic_interpretation=bool(getattr(provider, "semantic_interpretation", False)),
        semantic_compression=bool(getattr(provider, "semantic_compression", False)),
        network_access=False,
        automatic_model_download=False,
        automatic_package_download=False,
        automatic_dependency_install=False,
        provider_autonomous_continuous_execution=bool(getattr(provider, "provider_autonomous_execution", False)),
        hidden_retry=False,
        raw_content_persisted=False,
        gateway_handoff_candidate=bool(getattr(provider, "gateway_handoff", None)),
        trace_ref=str(getattr(provider, "trace_ref", "")),
        provenance_refs=tuple(str(item) for item in (getattr(provider, "provenance_refs", ()) or ())),
    )


def to_dict(value: Any) -> Dict[str, Any]:
    return asdict(value)
