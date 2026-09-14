from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.model_manager.module.model_manager_module_facade_v1 import (
    run_model_manager_module_v1,
)


def run_model_manager_module_api_v1(request: Mapping[str, Any]) -> Dict[str, Any]:
    return run_model_manager_module_v1(request)
