from __future__ import annotations

from typing import Any, Dict, Mapping


def build_field_perception_model_requirements_v1(
    capability_plan: Mapping[str, Any],
    available_model_assets: tuple[Mapping[str, Any], ...],
    temporal_context: Mapping[str, Any],
) -> Dict[str, Any]:
    requested = tuple(capability_plan.get("requested_visual_capabilities") or ())
    low_light = bool(
        temporal_context.get("low_light", False)
        or temporal_context.get("is_night", False)
    )

    preferred = []
    fallback = []
    for asset in available_model_assets:
        if not isinstance(asset, Mapping):
            continue
        model_id = str(asset.get("model_id") or "")
        supports = tuple(str(x) for x in (asset.get("supports") or ()))
        if requested and not set(requested).intersection(set(supports)):
            continue
        if bool(asset.get("preferred", False)):
            preferred.append(model_id)
        else:
            fallback.append(model_id)

    if low_light and "low_light_enhancer_v1" not in preferred:
        fallback.insert(0, "low_light_enhancer_v1")

    return {
        "schema_version": "field_perception_model_requirement_builder_v1",
        "preferred_model_candidates": tuple(dict.fromkeys(x for x in preferred if x)),
        "fallback_model_candidates": tuple(dict.fromkeys(x for x in fallback if x)),
        "model_requirements": {
            "required_capabilities": requested,
            "low_light_preferred": low_light,
            "latency_class": "near_real_time",
        },
    }
