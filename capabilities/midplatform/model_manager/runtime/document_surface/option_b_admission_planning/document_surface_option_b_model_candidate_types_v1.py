# -*- coding: utf-8 -*-
"""Document Surface — Option B model candidate types v1."""

from __future__ import annotations

from typing import Any, Dict, List


def build_option_b_candidate_family_evaluation() -> Dict[str, Any]:
    families: List[Dict[str, Any]] = [
        {
            "family_id": "family_a_classical_lightweight_segmentation",
            "family_type": "classical_lightweight_image_segmentation_helper",
            "examples": ["GrabCut-like", "lightweight edge+region segmentation helper"],
            "pros": ["dependency_controllable", "low_cost"],
            "cons": ["limited_complex_occlusion"],
            "active_model_selected": False,
            "download_planned": False,
            "execution_planned": False,
        },
        {
            "family_id": "family_b_general_lightweight_segmentation",
            "family_type": "general_lightweight_segmentation_model",
            "examples": ["MobileSAM-like", "FastSAM-like", "lightweight SAM-like route"],
            "pros": ["strong_mask_capability"],
            "cons": ["dependency_weight_license_admission_required"],
            "active_model_selected": False,
            "download_planned": False,
            "execution_planned": False,
        },
        {
            "family_id": "family_c_document_specific_segmentation",
            "family_type": "document_specific_segmentation_surface_model",
            "examples": ["paper/receipt surface specialized models"],
            "pros": ["task_matched"],
            "cons": ["limited_availability", "generalization_unknown"],
            "active_model_selected": False,
            "download_planned": False,
            "execution_planned": False,
        },
        {
            "family_id": "family_d_depth_geometric_assisted",
            "family_type": "depth_geometric_assisted_segmentation_route",
            "examples": ["depth-assisted plane/boundary mask"],
            "pros": ["may_help_overlap_occlusion"],
            "cons": ["hardware_input_may_not_exist"],
            "active_model_selected": False,
            "download_planned": False,
            "execution_planned": False,
        },
    ]
    return {
        "evaluation_id": "document_surface_option_b_candidate_family_evaluation_v1",
        "families_evaluated": [f["family_id"] for f in families],
        "family_count": len(families),
        "all_families_abcd_evaluated": len(families) >= 4,
        "no_active_model_selected": all(f.get("active_model_selected") is False for f in families),
        "no_download_install_execution": all(
            f.get("download_planned") is False and f.get("execution_planned") is False for f in families
        ),
        "families": families,
        "candidate_only": True,
        "not_fact": True,
    }
