"""Bounded Model+Provider routing lifecycle closure.

This module sits above Owner current-state reads and below production routing
consumers. It does not own lifecycle, identity, binding, grant, or full
production eligibility authority.
"""

from __future__ import annotations

from typing import Any, Dict, Iterable, List

from capabilities.midplatform.model_manager.lifecycle.model_current_state_read_v1 import (
    read_model_current_state,
)
from capabilities.midplatform.model_manager.registry.provider_current_state_read_v1 import (
    read_provider_current_state,
)


def evaluate_model_provider_routing_lifecycle_closure(provider: Dict[str, Any]) -> Dict[str, Any]:
    """Return a bounded plain mapping for the Model+Provider prerequisite."""

    reasons = []
    provider_id = str(provider.get("provider_id", ""))
    if not provider_id:
        return {"accepted": False, "reasons": ("missing_provider_identity",)}

    provider_state = read_provider_current_state(provider_id)
    if provider_state.get("read_status") != "BOUNDED_STATIC_CURRENT_STATE":
        reasons.append("provider_current_state_unknown")
    if not provider_state.get("source_revision") or not provider_state.get("currentness_basis"):
        reasons.append("provider_current_state_unknown")
    if provider_state.get("lifecycle_state") != "active":
        reasons.append("provider_lifecycle_not_active")
    if provider_state.get("admission_status") != "admitted":
        reasons.append("provider_not_admitted")

    model_id = str(provider.get("model_id", ""))
    if not model_id:
        reasons.append("model_reference_missing")
        return {"accepted": False, "reasons": tuple(dict.fromkeys(reasons)), "provider_state": provider_state}

    model_state = read_model_current_state(model_id)
    if model_state.get("read_status") != "BOUNDED_STATIC_CURRENT_STATE":
        reasons.append("model_current_state_unknown")
    if not model_state.get("source_revision") or not model_state.get("currentness_basis"):
        reasons.append("model_current_state_unknown")
    if model_state.get("lifecycle_state") != "active":
        reasons.append("model_lifecycle_not_active")
    if model_state.get("admission_status") != "admitted":
        reasons.append("model_not_admitted")

    return {
        "accepted": not reasons,
        "reasons": tuple(dict.fromkeys(reasons)),
        "provider_state": provider_state,
        "model_state": model_state,
    }


def filter_model_provider_routing_lifecycle_eligible(
    providers: Iterable[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """Filter production candidates through one shared cross-owner closure."""

    return [
        provider
        for provider in providers
        if evaluate_model_provider_routing_lifecycle_closure(provider)["accepted"]
    ]
