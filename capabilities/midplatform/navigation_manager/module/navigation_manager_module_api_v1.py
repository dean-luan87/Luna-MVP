from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.navigation_manager.module.navigation_manager_module_facade_v1 import (
    run_navigation_manager_module_v1 as _run_navigation_manager_module_v1,
)


def run_navigation_manager_module_v1(payload: Mapping[str, Any]) -> Dict[str, Any]:
    return _run_navigation_manager_module_v1(payload)
