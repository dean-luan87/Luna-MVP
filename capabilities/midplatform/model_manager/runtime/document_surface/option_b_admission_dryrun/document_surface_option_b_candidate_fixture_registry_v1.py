# -*- coding: utf-8 -*-
"""Document Surface — Option B candidate fixture registry v1."""

from __future__ import annotations

from typing import Any, Dict, List

ALLOWED_OUTPUTS = [
    "surface_mask_candidate",
    "document_surface_candidate",
    "boundary_candidate",
    "partial_surface_candidate",
    "occlusion_surface_hint_candidate",
    "runtime_error_candidate",
]

FORBIDDEN_OUTPUTS = [
    "ocr_text",
    "document_type_fact",
    "layout_semantic_fact",
    "final_owner_fact",
    "document_content",
    "relation_fact",
    "caption",
    "natural_language_interpretation",
]


def _base(
    *,
    model_candidate_id: str,
    family_type: str,
    dependency_profile: Dict[str, Any],
    weight_profile: Dict[str, Any],
    license_status_candidate: str,
    raw_output_profile: str = "mask_only",
    wrapper_available: bool = False,
) -> Dict[str, Any]:
    return {
        "model_candidate_id": model_candidate_id,
        "family_type": family_type,
        "capability": "detect_document_surface_mask_candidate",
        "output_types_allowed": list(ALLOWED_OUTPUTS),
        "output_types_forbidden": list(FORBIDDEN_OUTPUTS),
        "dependency_profile": dependency_profile,
        "weight_profile": weight_profile,
        "license_status_candidate": license_status_candidate,
        "raw_output_profile": raw_output_profile,
        "wrapper_available": wrapper_available,
        "execution_mode_candidate": "not_admitted",
        "local_runtime_possible": False,
        "external_runtime_possible": False,
        "expected_input": "controlled_fixture_image_bgr",
        "expected_output": "surface_mask_candidate",
        "candidate_only": True,
        "not_fact": True,
        "active_status": False,
        "controlled_execution_required": True,
        "preflight_required": True,
        "validation_required": True,
    }


def build_candidate_fixture_registry() -> Dict[str, Any]:
    fixtures: List[Dict[str, Any]] = [
        _base(
            model_candidate_id="family_a_classical_helper_ok_candidate",
            family_type="classical_lightweight_segmentation_helper",
            dependency_profile={"type": "python_builtin_or_existing", "controlled": True},
            weight_profile={"type": "no_weight"},
            license_status_candidate="clear",
        ),
        _base(
            model_candidate_id="family_a_requires_uncontrolled_binary",
            family_type="classical_lightweight_segmentation_helper",
            dependency_profile={"type": "runtime_binary_uncontrolled", "controlled": False},
            weight_profile={"type": "no_weight"},
            license_status_candidate="clear",
        ),
        _base(
            model_candidate_id="family_b_lightweight_sam_like_weight_missing",
            family_type="general_lightweight_segmentation_model",
            dependency_profile={"type": "declared_only"},
            weight_profile={"type": "model_weight_missing", "present": False},
            license_status_candidate="clear_candidate",
        ),
        _base(
            model_candidate_id="family_b_sam_like_license_unknown",
            family_type="general_lightweight_segmentation_model",
            dependency_profile={"type": "declared_only"},
            weight_profile={"type": "model_weight", "present": True, "size_mb": 50},
            license_status_candidate="license_unknown",
        ),
        _base(
            model_candidate_id="family_b_sam_like_caption_or_text_default",
            family_type="general_lightweight_segmentation_model",
            dependency_profile={"type": "declared_only"},
            weight_profile={"type": "model_weight", "present": True, "size_mb": 80},
            license_status_candidate="clear_candidate",
            raw_output_profile="caption_or_text_possible",
            wrapper_available=False,
        ),
        _base(
            model_candidate_id="family_c_document_specific_surface_model_ok_for_preflight",
            family_type="document_specific_segmentation_surface_model",
            dependency_profile={"type": "declared_only", "controlled": True},
            weight_profile={"type": "model_weight", "present": True, "size_mb": 30},
            license_status_candidate="clear_candidate",
        ),
        _base(
            model_candidate_id="family_c_document_model_outputs_document_type_fact",
            family_type="document_specific_segmentation_surface_model",
            dependency_profile={"type": "declared_only"},
            weight_profile={"type": "model_weight", "present": True},
            license_status_candidate="clear_candidate",
            raw_output_profile="document_type_fact_by_default",
        ),
        _base(
            model_candidate_id="family_d_depth_geometric_requires_hardware",
            family_type="depth_geometric_assisted_segmentation",
            dependency_profile={"type": "hardware_requirement", "gpu_required": True, "available": False},
            weight_profile={"type": "no_weight"},
            license_status_candidate="clear_candidate",
        ),
    ]
    return {
        "registry_id": "document_surface_option_b_candidate_fixture_registry_v1",
        "fixture_count": len(fixtures),
        "fixtures": fixtures,
        "candidate_only": True,
        "not_fact": True,
    }
