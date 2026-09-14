from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.permission_and_admission_manager.module.permission_and_admission_module_facade_v1 import (
    run_permission_and_admission_manager_module_v1 as _run_permission_and_admission_manager_module_v1,
)


def run_permission_and_admission_manager_module_v1(
    payload: Mapping[str, Any],
) -> Dict[str, Any]:
    return _run_permission_and_admission_manager_module_v1(payload)
