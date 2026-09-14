# -*- coding: utf-8 -*-
"""Field Scene Small Range Construction — core facade v1."""

from __future__ import annotations

from capabilities.midplatform.field_scene_small_range_builder_v1 import (
    NON_EXECUTION_FLAGS,
    assign_field_zone,
    attach_depth_hint,
    construct_small_range_field_scene,
    normalize_spatial_payload,
)
from capabilities.midplatform.field_scene_small_range_static_validators_v1 import (
    validate_camera_state,
    validate_field_entity,
    validate_field_scene,
    validate_object_observation,
    validate_user_state,
)
from capabilities.midplatform.field_scene_small_range_types_v1 import (
    CONSTRUCTION_RESULT_FIELDS,
    DEPTH_SOURCES,
    FIELD_ENTITY_CANDIDATE_FIELDS,
    FIELD_SCENE_CANDIDATE_FIELDS,
    FIELD_ZONES,
)

__all__ = [
    "NON_EXECUTION_FLAGS",
    "FIELD_ZONES",
    "DEPTH_SOURCES",
    "FIELD_SCENE_CANDIDATE_FIELDS",
    "FIELD_ENTITY_CANDIDATE_FIELDS",
    "CONSTRUCTION_RESULT_FIELDS",
    "assign_field_zone",
    "attach_depth_hint",
    "construct_small_range_field_scene",
    "normalize_spatial_payload",
    "validate_camera_state",
    "validate_field_entity",
    "validate_field_scene",
    "validate_object_observation",
    "validate_user_state",
]
