# -*- coding: utf-8 -*-
"""Hardware Camera Runtime Adapter Stub v1 — contract-aligned placeholder; no real camera.

Phase-Hardware-Camera-Runtime-Adapter-Implementation-Stub-v1-001
"""

from __future__ import annotations

from typing import Any, Dict, Optional

ADAPTER_ID = "luna_camera_runtime_adapter_v1_stub"
ADAPTER_STATUS = "stub_only"
REAL_CAMERA_ENABLED = False

_STUB_BASE = {
    "adapter_id": ADAPTER_ID,
    "adapter_status": ADAPTER_STATUS,
    "real_camera_enabled": REAL_CAMERA_ENABLED,
    "real_hardware_called": False,
    "fact_status": "not_fact",
    "write_allowed": False,
}


def _stub_response(
    method_name: str,
    status: str,
    error_code: str,
    **extra: Any,
) -> Dict[str, Any]:
    out = {**_STUB_BASE, "method_name": method_name, "status": status, "error_code": error_code}
    out.update(extra)
    return out


def open_camera(
    camera_id: str = "primary_rgb_unknown",
    requested_mode: str = "static_reading",
    permission_context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    _ = permission_context
    return _stub_response(
        "open_camera",
        "blocked_stub_only",
        "ADAPTER_STUB_ONLY",
        opened=False,
        camera_session_id=None,
        camera_id=camera_id,
        requested_mode=requested_mode,
    )


def close_camera(camera_session_id: Optional[str] = None) -> Dict[str, Any]:
    return _stub_response(
        "close_camera",
        "no_active_session",
        "NO_ACTIVE_CAMERA_SESSION",
        closed=False,
        camera_session_id=camera_session_id,
    )


def capture_frame(
    camera_session_id: Optional[str] = None,
    capture_mode: str = "static",
    target_region_ref: Optional[str] = None,
    timeout_ms: Optional[int] = None,
) -> Dict[str, Any]:
    _ = timeout_ms
    return _stub_response(
        "capture_frame",
        "not_captured",
        "ADAPTER_STUB_ONLY",
        frame_ref=None,
        frame_timestamp=None,
        capture_status="not_captured",
        quality_placeholder="unknown",
        camera_session_id=camera_session_id,
        capture_mode=capture_mode,
        target_region_ref=target_region_ref,
        frame_is_fact=False,
        runtime_frame_captured=False,
    )


def request_zoom(
    camera_session_id: Optional[str] = None,
    zoom_level_or_policy: Optional[Any] = None,
) -> Dict[str, Any]:
    _ = zoom_level_or_policy
    return _stub_response(
        "request_zoom",
        "not_applied",
        "ZOOM_NOT_AVAILABLE_IN_STUB",
        zoom_applied=False,
        actual_zoom_placeholder=None,
        camera_session_id=camera_session_id,
    )


def request_autofocus(
    camera_session_id: Optional[str] = None,
    target_region_ref: Optional[str] = None,
) -> Dict[str, Any]:
    return _stub_response(
        "request_autofocus",
        "not_applied",
        "AUTOFOCUS_NOT_AVAILABLE_IN_STUB",
        autofocus_applied=False,
        focus_status="unknown",
        camera_session_id=camera_session_id,
        target_region_ref=target_region_ref,
    )


def request_exposure_adjustment(
    camera_session_id: Optional[str] = None,
    exposure_policy: Optional[Any] = None,
) -> Dict[str, Any]:
    _ = exposure_policy
    return _stub_response(
        "request_exposure_adjustment",
        "not_applied",
        "EXPOSURE_NOT_AVAILABLE_IN_STUB",
        exposure_applied=False,
        exposure_status="unknown",
        camera_session_id=camera_session_id,
    )


def request_stabilization(
    camera_session_id: Optional[str] = None,
    stabilization_mode: Optional[str] = None,
) -> Dict[str, Any]:
    _ = stabilization_mode
    return _stub_response(
        "request_stabilization",
        "not_applied",
        "STABILIZATION_NOT_AVAILABLE_IN_STUB",
        stabilization_applied=False,
        stabilization_status="unknown",
        camera_session_id=camera_session_id,
    )


def get_capability_report(
    hardware_profile_id: str = "unknown_placeholder",
    camera_id: str = "primary_rgb_unknown",
) -> Dict[str, Any]:
    return _stub_response(
        "get_capability_report",
        "unknown",
        "CAPABILITY_UNKNOWN_STUB",
        capability_report_candidate={
            "hardware_profile_id": hardware_profile_id,
            "camera_id": camera_id,
            "camera_available_status": "unknown",
            "zoom_supported_status": "unknown",
            "autofocus_supported_status": "unknown",
            "exposure_control_supported_status": "unknown",
            "stabilization_supported_status": "unknown",
            "frame_capture_supported_status": "unknown",
            "still_frame_supported_status": "unknown",
            "capability_status": "unknown",
            "source": "runtime_adapter_stub",
        },
        capability_status="unknown",
        stale_status="unknown",
        capability_fact_written=False,
    )


def get_health_status(
    adapter_id: str = ADAPTER_ID,
    camera_session_id: Optional[str] = None,
) -> Dict[str, Any]:
    return _stub_response(
        "get_health_status",
        "stub_only",
        "ADAPTER_STUB_ONLY",
        health_status_candidate={
            "adapter_id": adapter_id,
            "camera_session_id": camera_session_id,
            "status": "unknown",
            "failure_class_candidate": "ADAPTER_STUB_ONLY",
            "recovery_candidate": "INSTALL_RUNTIME_ADAPTER",
        },
        failure_class_candidate="ADAPTER_STUB_ONLY",
        recovery_candidate="INSTALL_RUNTIME_ADAPTER",
        system_health_report_required_later=True,
        module_health_report_generated_now=False,
    )


REQUIRED_METHODS = [
    open_camera,
    close_camera,
    capture_frame,
    request_zoom,
    request_autofocus,
    request_exposure_adjustment,
    request_stabilization,
    get_capability_report,
    get_health_status,
]

METHOD_NAMES = [fn.__name__ for fn in REQUIRED_METHODS]


def invoke_all_stub_methods_smoke() -> Dict[str, Dict[str, Any]]:
    """Invoke all 9 methods once for smoke; never touches real camera."""
    return {
        "open_camera": open_camera(),
        "close_camera": close_camera(),
        "capture_frame": capture_frame(target_region_ref="rrc_placeholder"),
        "request_zoom": request_zoom(),
        "request_autofocus": request_autofocus(target_region_ref="rrc_placeholder"),
        "request_exposure_adjustment": request_exposure_adjustment(),
        "request_stabilization": request_stabilization(),
        "get_capability_report": get_capability_report(),
        "get_health_status": get_health_status(),
    }
