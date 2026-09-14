from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.field_perception_orchestrator.integration.field_perception_visual_handoff_facade_v1 import (
    run_field_perception_visual_handoff_integration_v1 as _run_field_perception_visual_handoff_integration_v1,
)


def run_field_perception_visual_handoff_integration_v1(
    payload: Mapping[str, Any],
) -> Dict[str, Any]:
    return _run_field_perception_visual_handoff_integration_v1(payload)
