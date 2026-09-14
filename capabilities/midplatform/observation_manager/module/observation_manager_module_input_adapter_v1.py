from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.observation_manager.module.observation_manager_module_types_v1 import (
    MODULE_SCHEMA_VERSION,
    SUPPORTED_REQUEST_TYPES,
    not_fact,
)


def adapt_observation_manager_input_v1(payload: Mapping[str, Any]) -> Dict[str, Any]:
    candidate = dict(payload)
    request_type = str(candidate.get("request_type") or "").strip()
    return {
        "schema_version": MODULE_SCHEMA_VERSION,
        "observation_request_id": str(
            candidate.get("observation_request_id") or ""
        ).strip(),
        "request_type": request_type,
        "request_type_supported": request_type in SUPPORTED_REQUEST_TYPES,
        "task_id": str(candidate.get("task_id") or "").strip(),
        "task_context": dict(candidate.get("task_context") or {}),
        "scene_context": dict(candidate.get("scene_context") or {}),
        "attention_targets": tuple(candidate.get("attention_targets") or ()),
        "region_hints": tuple(candidate.get("region_hints") or ()),
        "temporal_snapshot": dict(candidate.get("temporal_snapshot") or {}),
        "source_constraints": dict(candidate.get("source_constraints") or {}),
        "vision_requested": bool(candidate.get("vision_requested", True)),
        "ocr_requested": bool(candidate.get("ocr_requested", True)),
        "human_correction_refs": tuple(candidate.get("human_correction_refs") or ()),
        "permission_context": dict(candidate.get("permission_context") or {}),
        "version_snapshot": dict(candidate.get("version_snapshot") or {}),
        "trace_context": dict(candidate.get("trace_context") or {}),
        "vision_evidence_refs": tuple(candidate.get("vision_evidence_refs") or ()),
        "ocr_evidence_refs": tuple(candidate.get("ocr_evidence_refs") or ()),
        "candidate_only": True,
        **not_fact(),
    }
