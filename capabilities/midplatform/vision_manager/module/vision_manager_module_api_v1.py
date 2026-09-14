from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.vision_manager.module.vision_manager_module_facade_v1 import (
    run_vision_manager_module_v1,
)


def run_vision_manager_module_api_v1(request: Mapping[str, Any]) -> Dict[str, Any]:
    return run_vision_manager_module_v1(request)
