from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.field_perception_orchestrator.module.field_perception_module_facade_v1 import (
    run_field_perception_orchestrator_module_v1 as _run_field_perception_orchestrator_module_v1,
)


def run_field_perception_orchestrator_module_v1(
    payload: Mapping[str, Any],
) -> Dict[str, Any]:
    return _run_field_perception_orchestrator_module_v1(payload)
