# -*- coding: utf-8 -*-
"""Default Vision provider registry (stub enabled; real paths disabled)."""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict


def build_default_vision_provider_registry_v0() -> Dict[str, Any]:
    """Registry snapshot: only ``vision_stub`` is enabled by default."""
    return {
        "schema_version": "vision_provider_registry_v0",
        "entries": {
            "vision_stub": {
                "enabled": True,
                "provider_level": "stub",
                "description": "Synthetic stub; no real vision model.",
            },
            "yolo_candidate": {
                "enabled": False,
                "provider_level": "heavy",
                "description": "Disabled candidate; not wired in this phase.",
            },
            "supervision_candidate": {
                "enabled": False,
                "provider_level": "lightweight",
                "description": "Disabled candidate; Supervision mainline must not run here.",
            },
            "vlm_candidate": {
                "enabled": False,
                "provider_level": "vlm",
                "description": "Disabled candidate; VLM not allowed in this phase.",
            },
        },
    }


def snapshot_registry_v0(registry: Dict[str, Any]) -> Dict[str, Any]:
    """Deep copy for ``provider_registry_snapshot`` embedding."""
    return deepcopy(registry)
