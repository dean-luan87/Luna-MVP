from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.observation_manager.module.observation_manager_module_types_v1 import (
    SUPPORTED_REQUEST_TYPES,
    not_fact,
)


def build_observation_request_classification_v1(
    input_candidate: Mapping[str, Any],
) -> Dict[str, Any]:
    request_type = str(input_candidate.get("request_type") or "")
    no_observation_required = request_type == "passive_observation" and not bool(
        input_candidate.get("attention_targets")
    )
    return {
        "schema_version": "observation_manager_request_classifier_v1",
        "request_type": request_type,
        "request_type_supported": request_type in SUPPORTED_REQUEST_TYPES,
        "classification": request_type
        if request_type in SUPPORTED_REQUEST_TYPES
        else "unknown",
        "no_observation_required": no_observation_required,
        **not_fact(),
    }
