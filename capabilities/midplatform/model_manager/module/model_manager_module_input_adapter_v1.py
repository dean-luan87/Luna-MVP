from __future__ import annotations

from typing import Any, Dict, Mapping, Tuple

_REQUIRED = (
    "request_id",
    "requested_capability",
    "device_ref",
    "region_ref",
    "resource_snapshot",
    "version_snapshot",
)


def _tuple_str(value: Any) -> Tuple[str, ...]:
    if value is None:
        return tuple()
    if isinstance(value, str):
        return (value,)
    return tuple(str(x) for x in value)


def adapt_model_manager_input_v1(raw: Mapping[str, Any]) -> Dict[str, Any]:
    missing = [k for k in _REQUIRED if not raw.get(k)]
    rejection = [f"missing_{k}" for k in missing]

    resource = raw.get("resource_snapshot") or {}
    if not isinstance(resource, Mapping):
        resource = {}
        rejection.append("invalid_resource_snapshot")

    version = raw.get("version_snapshot") or {}
    if not isinstance(version, Mapping):
        version = {}
        rejection.append("invalid_version_snapshot")

    adapted = {
        "request_id": str(raw.get("request_id", "")).strip(),
        "requested_capability": str(raw.get("requested_capability", "")).strip(),
        "task_ref": str(raw.get("task_ref", "")).strip(),
        "device_ref": str(raw.get("device_ref", "")).strip(),
        "region_ref": str(raw.get("region_ref", "")).strip(),
        "resource_snapshot": dict(resource),
        "allowed_model_classes": _tuple_str(raw.get("allowed_model_classes")),
        "forbidden_model_ids": _tuple_str(raw.get("forbidden_model_ids")),
        "latency_requirement": int(raw.get("latency_requirement", 3000) or 3000),
        "memory_budget": int(raw.get("memory_budget", 8192) or 8192),
        "offline_required": bool(raw.get("offline_required", False)),
        "privacy_requirement": str(raw.get("privacy_requirement", "normal")).strip(),
        "ownership_context": dict(raw.get("ownership_context") or {}),
        "version_snapshot": dict(version),
        "trace_context": dict(raw.get("trace_context") or {}),
        "rejection_reasons": tuple(rejection),
    }
    adapted["input_valid"] = len(adapted["rejection_reasons"]) == 0
    return adapted
