# -*- coding: utf-8 -*-
"""Document Surface — Model Manager runtime binding v1."""

from __future__ import annotations

from typing import Any, Dict

from capabilities.midplatform.model_manager.runtime.document_surface.document_surface_detector_model_manager_registry_v1 import (
    DOCUMENT_SURFACE_RUNTIME_REGISTRY,
    match_capability_for_document_surface,
)
from capabilities.midplatform.model_manager.runtime.document_surface.document_surface_detector_types_v1 import (
    RUNTIME_ID,
)


def bind_document_surface_runtime(
    *,
    attention_gate_status: str,
    source_region_id: str = "region_001",
) -> Dict[str, Any]:
    """Model Manager Runtime Binding — attention gate required."""
    if attention_gate_status != "allowed":
        return {
            "binding_id": "dsb_blocked",
            "runtime_id": RUNTIME_ID,
            "runtime_binding_status_candidate": "skipped_by_attention_gate",
            "source_region_id": source_region_id,
            "attention_gate_status": attention_gate_status,
            "runtime_call_count": 0,
            "registry_entry": DOCUMENT_SURFACE_RUNTIME_REGISTRY.get(RUNTIME_ID),
            "candidate_only": True,
        }

    match = match_capability_for_document_surface(attention_gate_status=attention_gate_status)
    return {
        "binding_id": "dsb_bound",
        "runtime_id": RUNTIME_ID,
        "runtime_binding_status_candidate": "bound",
        "source_region_id": source_region_id,
        "attention_gate_status": attention_gate_status,
        "capability_match": match,
        "runtime_call_count": 1,
        "registry_entry": DOCUMENT_SURFACE_RUNTIME_REGISTRY.get(RUNTIME_ID),
        "model_manager_managed_runtime": True,
        "candidate_only": True,
    }
