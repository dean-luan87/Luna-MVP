from __future__ import annotations

from typing import Any, Dict, Mapping, Sequence


def build_ocr_manager_engine_capability_adapter_v1(
    input_candidate: Mapping[str, Any],
    governance: Mapping[str, Any],
) -> Dict[str, Any]:
    preferred_engine = str(
        (input_candidate.get("task_ocr_request") or {}).get("preferred_engine")
        or "rapidocr"
    ).lower()
    engines: Sequence[Dict[str, Any]] = (
        {
            "engine_identity": "rapidocr_onnxruntime_v0",
            "supported_languages": ("zh", "en"),
            "supported_input_types": ("image_candidate", "roi", "poster_region"),
            "detection_capability": "candidate",
            "recognition_capability": "candidate",
            "layout_capability": "candidate",
            "engine_readiness": "ready",
            "resource_requirement_candidate": {"cpu": "medium", "memory_mb": 256},
            "fallback_candidate": "paddleocr_ppocrv5_candidate",
        },
        {
            "engine_identity": "paddleocr_ppocrv5_candidate",
            "supported_languages": ("zh", "en"),
            "supported_input_types": ("image_candidate", "roi"),
            "detection_capability": "candidate",
            "recognition_capability": "candidate",
            "layout_capability": "candidate",
            "engine_readiness": "candidate_ready",
            "resource_requirement_candidate": {"cpu": "high", "memory_mb": 768},
            "fallback_candidate": "rapidocr_onnxruntime_v0",
        },
    )

    selected = next(
        (engine for engine in engines if preferred_engine in engine["engine_identity"]),
        engines[0],
    )
    unavailable = not bool(governance.get("admitted")) or bool(
        (input_candidate.get("synthetic_integration_fixture") or {}).get(
            "force_engine_unavailable"
        )
    )
    selected_state = "unavailable" if unavailable else selected["engine_readiness"]

    return {
        "selected_engine": {
            **selected,
            "engine_readiness": selected_state,
            "candidate_only": True,
            "runtime_model_load_allowed": False,
            "network_model_allowed": False,
        },
        "engine_catalog": engines,
        "engine_handoff_candidate": {
            "engine_identity": selected["engine_identity"],
            "allowed": not unavailable,
            "fallback_candidate": selected["fallback_candidate"],
            "candidate_only": True,
        },
    }
