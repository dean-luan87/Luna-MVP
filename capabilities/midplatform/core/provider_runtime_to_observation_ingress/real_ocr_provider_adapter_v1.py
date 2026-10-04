"""OCR-specific adapter for the shared LIVE_RUNTIME provider bridge.

The canonical registry identity is ``ocr_v1``.  Its existing local runtime
implementation is RapidOCR/ONNXRuntime; this module only adapts that native
result to the shared ProviderRuntime contracts.  It does not interpret text.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Tuple

from capabilities.midplatform.model_manager.registry.provider_registry_loader_v1 import (
    get_capability_entry,
    get_provider_by_id,
    list_capability_providers,
    load_model_registry,
)
from capabilities.midplatform.model_manager.engines.model_provider_routing_lifecycle_closure_v1 import (
    filter_model_provider_routing_lifecycle_eligible,
)
from capabilities.midplatform.ocr_manager.module.ocr_manager_engine_capability_adapter_v1 import (
    build_ocr_manager_engine_capability_adapter_v1,
)
from capabilities.model_ocr.rapidocr_adapter_v0 import RapidOCRAdapterV0

from .types_v1 import ProviderRuntimeRequestV1, ProviderRuntimeResultV1


CANONICAL_CAPABILITY_ID = "text_recognition"
CANONICAL_PROVIDER_MODEL_ID = "ocr_v1"


def resolve_canonical_ocr_binding_v1() -> Tuple[Dict[str, Any] | None, Tuple[str, ...]]:
    """Resolve the active OCR binding from the canonical registries."""

    errors = []
    capability = get_capability_entry(CANONICAL_CAPABILITY_ID)
    if capability is None:
        return None, ("canonical_ocr_capability_missing",)

    eligible = filter_model_provider_routing_lifecycle_eligible(list_capability_providers(CANONICAL_CAPABILITY_ID))
    selected = next(
        (item for item in eligible if item.get("model_id") == CANONICAL_PROVIDER_MODEL_ID),
        None,
    )
    if selected is None:
        return None, ("canonical_ocr_provider_not_routing_eligible",)

    provider = get_provider_by_id(CANONICAL_PROVIDER_MODEL_ID)
    model = next(
        (item for item in (load_model_registry().get("models") or [])
         if item.get("model_id") == CANONICAL_PROVIDER_MODEL_ID),
        None,
    )
    if provider is None or model is None:
        errors.append("canonical_ocr_model_or_provider_missing")
    if CANONICAL_CAPABILITY_ID not in (selected.get("capabilities") or ()):
        errors.append("canonical_ocr_provider_capability_mismatch")

    engine = build_ocr_manager_engine_capability_adapter_v1(
        {"task_ocr_request": {"preferred_engine": "rapidocr"}},
        {"admitted": True},
    )
    selected_engine = engine.get("selected_engine") or {}
    native_provider_id = str(selected_engine.get("engine_identity") or "")
    if native_provider_id != RapidOCRAdapterV0.provider_id:
        errors.append("canonical_ocr_runtime_engine_mismatch")

    if errors:
        return None, tuple(errors)

    return {
        "capability_id": CANONICAL_CAPABILITY_ID,
        "capability_ref": f"capability:{CANONICAL_CAPABILITY_ID}",
        "canonical_provider_id": CANONICAL_PROVIDER_MODEL_ID,
        "provider_ref": f"provider:{CANONICAL_PROVIDER_MODEL_ID}",
        "model_ref": f"model:{CANONICAL_PROVIDER_MODEL_ID}",
        "native_provider_id": native_provider_id,
        "native_model_config_id": RapidOCRAdapterV0.model_config_id,
        "provider_profile": provider,
        "model_profile": model,
        "engine_capability": engine,
        "provenance_refs": (
            "capability-registry:v1",
            "provider-registry:v1",
            "model-registry:v1",
            f"adapter:{native_provider_id}",
        ),
        "candidate_only": True,
    }, ()


def invoke_real_ocr_provider_v1(
    *,
    source_ref: str,
    frame_id: str,
    timestamp_ms: int,
) -> Dict[str, Any]:
    """Invoke the existing RapidOCR implementation exactly once."""

    adapter = RapidOCRAdapterV0()
    return adapter.recognize_image(
        image_path=str(Path(source_ref)),
        frame_id=frame_id,
        timestamp_ms=timestamp_ms,
    )


def normalize_ocr_native_result_v1(
    request: ProviderRuntimeRequestV1,
    binding: Dict[str, Any],
    native: Dict[str, Any],
) -> ProviderRuntimeResultV1:
    """Map native RapidOCR output without adding semantic claims."""

    native_status = str(native.get("runtime_status") or "OCR_INVOCATION_EXCEPTION")
    status = {
        "SUCCESS": "SUCCESS",
        "EMPTY_SUCCESS": "EMPTY_SUCCESS",
        "UNAVAILABLE": "UNAVAILABLE",
        "MODEL_UNAVAILABLE": "UNAVAILABLE",
        "INVALID_IMAGE": "REJECTED",
    }.get(native_status, "ERROR")
    candidates = native.get("raw_text_candidates")
    if not isinstance(candidates, list):
        candidates = []
        status = "ERROR"
        native_status = "MALFORMED_NATIVE_OUTPUT"

    confidences = []
    for item in candidates:
        if isinstance(item, dict) and item.get("confidence") is not None:
            try:
                confidences.append(float(item["confidence"]))
            except (TypeError, ValueError):
                pass

    output_candidate = None
    if status in {"SUCCESS", "EMPTY_SUCCESS"}:
        output_candidate = {
            "schema": "ocr-text-candidate-payload-v1",
            "text_candidates": candidates,
            "text_joined": str(native.get("raw_text_joined") or ""),
            "source_ref": request.input_source_ref,
            "native_provider_id": binding["native_provider_id"],
            "native_model_config_id": binding["native_model_config_id"],
            "empty_result": status == "EMPTY_SUCCESS",
            "candidate_only": True,
            "truth_declared": False,
        }

    trace_ref = f"trace:{request.execution_instance_ref}:ocr-native"
    return ProviderRuntimeResultV1(
        provider_result_ref=f"provider-result:{request.execution_instance_ref}",
        provider_request_ref=request.provider_request_ref,
        provider_ref=request.provider_ref,
        capability_ref=request.capability_ref,
        model_ref=request.model_ref,
        execution_instance_ref=request.execution_instance_ref,
        modality=request.modality,
        output_ref=f"provider-output:{request.execution_instance_ref}",
        raw_result_ref=f"provider-native-result:{request.execution_instance_ref}",
        status=status,
        confidence_candidate=max(confidences) if confidences else None,
        quality_candidate=None,
        temporal_ref=request.temporal_ref,
        spatial_refs=request.spatial_refs,
        trace_refs=tuple(dict.fromkeys((*request.trace_refs, trace_ref))),
        provenance_refs=tuple(dict.fromkeys((*request.provenance_refs, *binding["provenance_refs"]))),
        empty_result=status == "EMPTY_SUCCESS",
        candidate_only=True,
        truth_declared=False,
        provider_invoked=bool(native.get("provider_invoked")),
        model_invoked=bool(native.get("model_invoked")),
        output_candidate=output_candidate,
        error_category=str(native.get("error_category") or native_status)
        if status not in {"SUCCESS", "EMPTY_SUCCESS"} else None,
    )


__all__ = [
    "CANONICAL_CAPABILITY_ID",
    "CANONICAL_PROVIDER_MODEL_ID",
    "invoke_real_ocr_provider_v1",
    "normalize_ocr_native_result_v1",
    "resolve_canonical_ocr_binding_v1",
]
