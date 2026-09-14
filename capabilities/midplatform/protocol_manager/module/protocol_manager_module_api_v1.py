from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.protocol_manager.module.protocol_manager_module_facade_v1 import (
    run_protocol_manager_module_v1 as _run_protocol_manager_module_v1,
)


def run_protocol_manager_module_v1(payload: Mapping[str, Any]) -> Dict[str, Any]:
    return _run_protocol_manager_module_v1(payload)
