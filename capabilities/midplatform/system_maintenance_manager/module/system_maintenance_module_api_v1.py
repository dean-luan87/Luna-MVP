from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.system_maintenance_manager.module.system_maintenance_module_facade_v1 import (
    run_system_maintenance_manager_module_v1 as _run_system_maintenance_manager_module_v1,
)


def run_system_maintenance_manager_module_v1(
    payload: Mapping[str, Any],
) -> Dict[str, Any]:
    return _run_system_maintenance_manager_module_v1(payload)
