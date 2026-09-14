from __future__ import annotations

import os
from pathlib import Path
from collections.abc import Sequence
from typing import Any, Mapping, Optional

from .types_v1 import RoboflowNativeResultV1, RoboflowProviderRequestV1


ROBOFLOW_SERVERLESS_API_URL = "https://serverless.roboflow.com"
_MAX_DIAGNOSTIC_KEYS = 32


def _declared_workflow_identity(workflow_ref: str) -> tuple[str, str]:
    parts = tuple(str(workflow_ref or "").split(":"))
    if len(parts) == 5 and parts[:2] == ("workflow", "roboflow") and parts[-1] == "v1":
        return parts[2], parts[3]
    return "", ""


def _bounded_response_shape_diagnostics(
    payload: Any,
    governed_output_path: str,
) -> Mapping[str, Any]:
    """Return bounded adapter-private shape facts, never provider payload data."""

    def type_name(value: Any) -> str:
        return type(value).__name__

    def keys(value: Any) -> list[str]:
        if not isinstance(value, Mapping):
            return []
        return sorted(str(key) for key in value.keys())[:_MAX_DIAGNOSTIC_KEYS]

    def value_shape(value: Any) -> dict[str, Any]:
        """Describe one provider value without retaining its contents."""

        shape: dict[str, Any] = {"value_type": type_name(value)}
        if isinstance(value, Mapping):
            child_keys = keys(value)
            shape["keys"] = child_keys
            shape["child_value_types"] = {
                key: type_name(value[key]) for key in child_keys
            }
            if "predictions" in value:
                predictions = value["predictions"]
                prediction_shape: dict[str, Any] = {
                    "value_type": type_name(predictions),
                }
                if isinstance(predictions, Sequence) and not isinstance(predictions, (str, bytes)):
                    prediction_shape["sequence_length"] = len(predictions)
                    first_prediction = predictions[0] if predictions else None
                    prediction_shape["first_item_type"] = (
                        type_name(first_prediction) if predictions else "EMPTY"
                    )
                    prediction_shape["first_item_keys"] = keys(first_prediction)
                shape["predictions"] = prediction_shape
        elif isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
            shape["sequence_length"] = len(value)
            first_item = value[0] if value else None
            shape["first_item_type"] = type_name(first_item) if value else "EMPTY"
            shape["first_item_keys"] = keys(first_item)
        return shape

    result: dict[str, Any] = {
        "top_level_type": type_name(payload),
        "top_level_keys": keys(payload),
        "governed_output_path": str(governed_output_path or ""),
        "governed_output_type": "UNRESOLVED",
    }
    if isinstance(payload, Sequence) and not isinstance(payload, (str, bytes)):
        result["sequence_length"] = len(payload)
        first = payload[0] if payload else None
        result["first_item_type"] = type_name(first) if payload else "EMPTY"
        result["first_item_keys"] = keys(first)
        if isinstance(first, Mapping):
            result["first_item_output_diagnostics"] = {
                key: value_shape(first[key]) for key in keys(first)
            }
        if len(payload) == 1 and isinstance(first, Mapping):
            path = str(governed_output_path or "").removeprefix("$").lstrip(".")
            if path and "." not in path and path in first:
                result["governed_output_type"] = type_name(first[path])
    elif isinstance(payload, Mapping):
        path = str(governed_output_path or "").removeprefix("$").lstrip(".")
        if path and "." not in path and path in payload:
            result["governed_output_type"] = type_name(payload[path])
    return result


def build_roboflow_provider_request_v1(
    *,
    request_id: str,
    observation_request_ref: str,
    capability_requirement_ref: str,
    provider_admission_ref: str,
    runtime_admission_ref: str,
    capability_model_binding_ref: str,
    model_provider_binding_ref: str,
    provider_ref: str,
    provider_contract_ref: str,
    workflow_ref: str,
    model_refs: tuple[str, ...],
    image_ref: str,
    frame_ref: str,
    roi_ref: str,
    requested_capabilities: tuple[str, ...],
    trace_ref: str,
    provenance_refs: tuple[str, ...],
    source_version_refs: tuple[str, ...],
    grant_refs: tuple[str, ...] = (),
    constraint_refs: tuple[str, ...] = (),
    invalidation_refs: tuple[str, ...] = (),
    real_mode: bool = False,
    goal_ref: str = "",
    concern_ref: str = "",
    workflow_output_mapping: Optional[Mapping[str, str]] = None,
) -> RoboflowProviderRequestV1:
    required = (
        request_id,
        observation_request_ref,
        capability_requirement_ref,
        provider_admission_ref,
        runtime_admission_ref,
        capability_model_binding_ref,
        model_provider_binding_ref,
        provider_ref,
        provider_contract_ref,
        workflow_ref,
        roi_ref,
        image_ref,
        frame_ref,
        trace_ref,
    )
    if not all(str(value).strip() for value in required):
        raise ValueError("Roboflow request requires governed admission, binding, image and trace refs")
    if not provenance_refs or not source_version_refs:
        raise ValueError("Roboflow request requires provenance and source versions")
    if not model_refs:
        raise ValueError("Roboflow request requires at least one governed model ref")
    if invalidation_refs:
        raise ValueError("invalidated Roboflow request cannot be constructed")
    if not requested_capabilities:
        raise ValueError("Roboflow request requires at least one capability")
    output_mapping = {
        str(key): str(value)
        for key, value in dict(workflow_output_mapping or {}).items()
        if str(key).strip() and str(value).strip()
    }
    if real_mode and (
        not output_mapping.get("detections")
        or any(value.startswith("USER_REQUIRED") for value in output_mapping.values())
        or (
            "text_recognition" in requested_capabilities
            and not output_mapping.get("ocr")
        )
    ):
        raise ValueError("real Roboflow request requires governed workflow output mapping")
    if real_mode and (not str(goal_ref).strip() or not str(concern_ref).strip()):
        raise ValueError("real Roboflow request requires goal_ref and concern_ref")
    if real_mode and any(
        str(value).startswith("USER_REQUIRED")
        for group in (grant_refs, constraint_refs, provenance_refs, source_version_refs)
        for value in group
    ):
        raise ValueError("real Roboflow request contains unresolved USER_REQUIRED governance refs")
    return RoboflowProviderRequestV1(
        request_id=request_id,
        observation_request_ref=observation_request_ref,
        capability_requirement_ref=capability_requirement_ref,
        provider_admission_ref=provider_admission_ref,
        runtime_admission_ref=runtime_admission_ref,
        capability_model_binding_ref=capability_model_binding_ref,
        model_provider_binding_ref=model_provider_binding_ref,
        provider_ref=provider_ref,
        provider_contract_ref=provider_contract_ref,
        workflow_ref=workflow_ref,
        model_refs=tuple(model_refs),
        image_ref=image_ref,
        frame_ref=frame_ref,
        roi_ref=roi_ref,
        requested_capabilities=tuple(requested_capabilities),
        trace_ref=trace_ref,
        provenance_refs=tuple(dict.fromkeys(provenance_refs)),
        source_version_refs=tuple(dict.fromkeys(source_version_refs)),
        grant_refs=tuple(grant_refs),
        constraint_refs=tuple(constraint_refs),
        invalidation_refs=tuple(invalidation_refs),
        real_mode=bool(real_mode),
        goal_ref=str(goal_ref),
        concern_ref=str(concern_ref),
        workflow_output_mapping=output_mapping,
    )


def _native_result(
    request: RoboflowProviderRequestV1,
    *,
    status: int,
    payload: Any,
    actual_provider_response: bool,
    error_class: str = "",
    error_detail: str = "",
    response_shape_diagnostics: Optional[Mapping[str, Any]] = None,
) -> RoboflowNativeResultV1:
    return RoboflowNativeResultV1(
        result_id=f"roboflow-result:{request.request_id}",
        http_status=int(status),
        payload=payload,
        provider_ref=request.provider_ref,
        workflow_ref=request.workflow_ref,
        model_refs=request.model_refs,
        request_id=request.request_id,
        trace_ref=request.trace_ref,
        provenance_refs=request.provenance_refs,
        source_version_refs=request.source_version_refs,
        invalidation_refs=request.invalidation_refs,
        actual_provider_response=actual_provider_response,
        workflow_output_mapping=request.workflow_output_mapping,
        error_class=error_class,
        error_detail=error_detail,
        response_shape_diagnostics=dict(response_shape_diagnostics or {}),
    )


def invoke_roboflow_provider_v1(
    request: RoboflowProviderRequestV1,
    *,
    native_payload: Optional[Any] = None,
) -> RoboflowNativeResultV1:
    """Invoke only in explicit real mode; structural payloads stay synthetic."""

    if request.invalidation_refs:
        return _native_result(
            request,
            status=409,
            payload={},
            actual_provider_response=False,
            error_class="INVALIDATION_PRESENT",
            error_detail="provider request is stale or invalidated",
        )

    if not request.real_mode:
        if native_payload is None:
            return _native_result(
                request,
                status=0,
                payload={},
                actual_provider_response=False,
                error_class="STRUCTURAL_MODE_NO_PROVIDER_CALL",
                error_detail="structural mode does not invoke Roboflow",
            )
        structural_payload = (
            dict(native_payload)
            if isinstance(native_payload, Mapping)
            else native_payload
        )
        return _native_result(
            request,
            status=200,
            payload=structural_payload,
            actual_provider_response=False,
        )

    api_key = str(os.environ.get("ROBOFLOW_API_KEY") or "").strip()
    api_url = str(
        os.environ.get("ROBOFLOW_API_URL")
        or os.environ.get("INFERENCE_SERVER_URL")
        or ""
    ).strip()
    workspace_name = str(os.environ.get("ROBOFLOW_WORKSPACE") or "").strip()
    workflow_id = str(os.environ.get("ROBOFLOW_WORKFLOW_ID") or "").strip()
    if not api_key or not api_url or not workspace_name or not workflow_id:
        return _native_result(
            request,
            status=0,
            payload={},
            actual_provider_response=False,
            error_class="REAL_PROVIDER_CONFIGURATION_MISSING",
            error_detail="ROBOFLOW_API_KEY, ROBOFLOW_API_URL/INFERENCE_SERVER_URL, ROBOFLOW_WORKSPACE and ROBOFLOW_WORKFLOW_ID are required",
        )
    declared_workspace, declared_workflow_id = _declared_workflow_identity(request.workflow_ref)
    if (
        api_url != ROBOFLOW_SERVERLESS_API_URL
        or not declared_workspace
        or workspace_name != declared_workspace
        or workflow_id != declared_workflow_id
    ):
        return _native_result(
            request,
            status=0,
            payload={},
            actual_provider_response=False,
            error_class="REAL_PROVIDER_CONFIGURATION_MISMATCH",
            error_detail="environment endpoint/workflow identity does not match the governed Roboflow declaration",
        )
    image_path = Path(request.image_ref)
    if not image_path.is_file():
        return _native_result(
            request,
            status=0,
            payload={},
            actual_provider_response=False,
            error_class="IMAGE_REFERENCE_INVALID",
            error_detail="real mode requires an existing local image reference",
        )
    try:
        from inference_sdk import InferenceConfiguration, InferenceHTTPClient

        client = InferenceHTTPClient(api_url=api_url, api_key=api_key)
        client.configure(InferenceConfiguration(api_key_transport="header"))
        payload = client.run_workflow(
            workspace_name=workspace_name,
            workflow_id=workflow_id,
            images={"image": str(image_path)},
            parameters={},
            use_cache=True,
        )
    except ImportError as exc:
        return _native_result(
            request,
            status=0,
            payload={},
            actual_provider_response=False,
            error_class="INFERENCE_SDK_MISSING",
            error_detail=f"{type(exc).__name__}: inference-sdk is required for real mode",
        )
    except (OSError, TypeError, ValueError) as exc:
        return _native_result(
            request,
            status=0,
            payload={},
            actual_provider_response=False,
            error_class="PROVIDER_REQUEST_FAILED",
            error_detail=f"{type(exc).__name__}: {exc}",
        )
    except Exception as exc:  # external SDK transport boundary; fail closed
        return _native_result(
            request,
            status=0,
            payload={},
            actual_provider_response=False,
            error_class="PROVIDER_REQUEST_FAILED",
            error_detail=f"{type(exc).__name__}: {exc}",
        )
    payload_is_mapping = isinstance(payload, Mapping)
    payload_is_one_image_sequence = (
        isinstance(payload, Sequence)
        and not isinstance(payload, (str, bytes))
        and all(isinstance(item, Mapping) for item in payload)
    )
    response_shape_diagnostics = _bounded_response_shape_diagnostics(
        payload,
        request.workflow_output_mapping.get("detections", ""),
    )
    if not payload_is_mapping and not payload_is_one_image_sequence:
        return _native_result(
            request,
            status=0,
            payload={},
            actual_provider_response=True,
            error_class="PROVIDER_RESULT_SCHEMA_INVALID",
            error_detail="Inference SDK workflow result must be a mapping or one-image mapping sequence",
            response_shape_diagnostics=response_shape_diagnostics,
        )
    return _native_result(
        request,
        status=200,
        payload=payload,
        actual_provider_response=True,
        response_shape_diagnostics=response_shape_diagnostics,
    )


__all__ = [
    "build_roboflow_provider_request_v1",
    "invoke_roboflow_provider_v1",
]
