from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.observation_manager.module.observation_manager_module_facade_v1 import (
    run_observation_manager_module_v1 as _run_observation_manager_module_v1,
)


def run_observation_manager_module_v1(payload: Mapping[str, Any]) -> Dict[str, Any]:
    return _run_observation_manager_module_v1(payload)
