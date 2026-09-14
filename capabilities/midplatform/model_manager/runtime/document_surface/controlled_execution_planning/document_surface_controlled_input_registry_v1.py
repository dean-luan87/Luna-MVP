# -*- coding: utf-8 -*-
"""Document Surface — controlled input registry v1."""

from __future__ import annotations

from typing import Any, Dict, List

CONTROLLED_INPUT_ROOT = "_fixtures/document_surface_real_runtime_controlled/"
ALTERNATE_INPUT_ROOT = "test_board/fixtures/document_surface_controlled_images/"

CONTROLLED_IMAGE_REGISTRY: List[Dict[str, Any]] = [
    {"image_ref": "single_flat_paper_controlled.png", "category": "single_flat_paper_controlled", "real_image_attached": False},
    {"image_ref": "two_overlapping_papers_controlled.png", "category": "two_overlapping_papers_controlled", "real_image_attached": False},
    {"image_ref": "low_contrast_paper_controlled.png", "category": "low_contrast_paper_controlled", "real_image_attached": False},
    {"image_ref": "receipt_attached_to_package_controlled.png", "category": "receipt_attached_to_package_controlled", "real_image_attached": False},
    {"image_ref": "document_on_screen_controlled.png", "category": "document_on_screen_controlled", "real_image_attached": False},
    {"image_ref": "unsupported_format_controlled.bmp", "category": "unsupported_format_controlled", "real_image_attached": False, "allowed_format": False},
]

INPUT_BOUNDARY_RULES = {
    "registry_only_read": True,
    "no_recursive_arbitrary_read": True,
    "no_user_directory_read": True,
    "no_production_data_read": True,
    "no_network_image_download": True,
    "no_implicit_benchmark_dataset": True,
}


def build_controlled_input_registry_plan() -> Dict[str, Any]:
    return {
        "registry_id": "document_surface_controlled_input_registry_v1",
        "primary_root": CONTROLLED_INPUT_ROOT,
        "alternate_root": ALTERNATE_INPUT_ROOT,
        "images": CONTROLLED_IMAGE_REGISTRY,
        "image_count": len(CONTROLLED_IMAGE_REGISTRY),
        "boundary_rules": INPUT_BOUNDARY_RULES,
        "no_arbitrary_input_directory": True,
        "planning_only": True,
        "candidate_only": True,
        "not_fact": True,
    }
