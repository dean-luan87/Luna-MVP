# -*- coding: utf-8 -*-
"""Default audit flags for OCR minimal mainline bridge."""

from __future__ import annotations

from typing import Any, Dict


def default_ocr_runtime_audit_v0() -> Dict[str, Any]:
    return {
        "schema": "ocr_runtime_audit_v0",
        "real_provider_invoked": False,
        "paddleocr_invoked": False,
        "rapidocr_replaced": False,
        "ocr_routing_changed": False,
        "midplatform_invoked": False,
        "world_model_written": False,
        "original_image_used_directly": False,
        "normalized_image_generated": False,
        "downscale_applied": False,
        "tile_applied": False,
        "tile_count": 0,
        "coordinate_transform_recorded": False,
        "tile_coverage_complete": True,
        "tile_truncated_to_budget": False,
        "full_image_claim_allowed": True,
        "partial_evidence_scope_recorded": False,
        "tile_evidence_generated": False,
        "tile_evidence_item_count": 0,
        "coordinate_reconstruction_applied": False,
        # Phase-OCR-Real-Provider-Adapter-Selection-001 (defaults; selection overwrites when invoked)
        "selected_provider": None,
        "selected_provider_level": None,
        "provider_selection_reason_codes": [],
        "real_provider_requested": False,
        "real_provider_allowed": False,
        "paddleocr_runtime_provider_enabled": False,
        "rapidocr_runtime_provider_enabled": False,
        "fallback_to_stub": False,
        "provider_registry_snapshot": {},
        "provider_unavailable_reason": None,
        "roi_unit_count": 0,
        "multi_roi_processed": False,
        "roi_coordinate_lift_applied": False,
        "provider_geometry_available": False,
        "original_geometry_recorded": False,
        "provider_geometry_unavailable": False,
    }
