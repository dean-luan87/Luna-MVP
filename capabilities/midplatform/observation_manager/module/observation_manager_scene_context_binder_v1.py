from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.observation_manager.module.observation_manager_module_types_v1 import (
    not_fact,
)


def bind_observation_scene_context_v1(
    input_candidate: Mapping[str, Any],
) -> Dict[str, Any]:
    scene_context = dict(input_candidate.get("scene_context") or {})
    return {
        "schema_version": "observation_manager_scene_context_binder_v1",
        "scene_context_ref": scene_context.get("scene_context_ref")
        or scene_context.get("scene_id")
        or "",
        "scene_context": scene_context,
        "scene_context_present": bool(scene_context),
        **not_fact(),
    }
