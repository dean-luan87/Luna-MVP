# -*- coding: utf-8 -*-
"""Document Surface — Option B input boundary check plan v1."""

from __future__ import annotations

from typing import Any, Dict, List


def build_input_boundary_check_plan() -> Dict[str, Any]:
    return {
        "plan_id": "option_b_input_boundary_check_plan_v1",
        "check_type": "input_boundary_check",
        "output_type": "input_boundary_check_candidate",
        "allowed_input_registry_scope": [
            "controlled_fixture_registry_metadata",
            "allowed_fixture_ids",
            "path_scope_declaration",
        ],
        "forbidden_input_scope": [
            "arbitrary_user_path",
            "registry_outside_scope",
            "image_pixel_read",
            "image_content_decode",
        ],
        "rules": [
            "metadata_and_registry_scope_only",
            "no_image_read",
            "no_pixel_inspection",
        ],
        "abort_on": ["input_boundary_violation", "registry_outside_scope", "arbitrary_user_path"],
        "image_read_allowed": False,
        "candidate_only": True,
        "not_fact": True,
    }
