from __future__ import annotations

from typing import Any, Dict, Mapping

from .task_manager_module_facade_v1 import TaskManagerModuleV1

_MODULE_SINGLETON = TaskManagerModuleV1()


def run_task_manager_module_v1(request: Mapping[str, Any]) -> Dict[str, Any]:
    return _MODULE_SINGLETON.handle(request)
