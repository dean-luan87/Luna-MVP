# -*- coding: utf-8 -*-
"""Document Surface — Option B permission / runtime boundary protocol mapping v1."""

from __future__ import annotations

from typing import Any, Dict

FORBIDDEN_CAPABILITIES = [
    "ocr",
    "global_ocr",
    "vlm",
    "full_scene_segmentation",
    "layout_semantic_parse",
]


def build_permission_runtime_boundary_mapping() -> Dict[str, Any]:
    return {
        "mapping_id": "option_b_permission_runtime_boundary_mapping_v1",
        "runtime_boundary_contract": "Runtime Boundary Contract",
        "permission_admission_contract": "Permission / Admission Contract",
        "option_b_frozen_state": {
            "model_candidate_route": True,
            "skill_candidate_route": True,
            "active_model": False,
            "active_skill": False,
            "runtime_activation_allowed": False,
            "controlled_execution_allowed": False,
            "preflight_required": True,
            "model_skill_admission_required": True,
        },
        "forbidden_capabilities": FORBIDDEN_CAPABILITIES,
        "install_allowed": False,
        "download_allowed": False,
        "execution_allowed": False,
        "network_access_allowed": False,
        "no_runtime_activation": True,
        "no_ocr_vlm_layout": True,
        "candidate_only": True,
        "not_fact": True,
    }
