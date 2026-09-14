from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.speech_manager.module.speech_manager_module_facade_v1 import (
    run_speech_manager_module_v1 as _run_speech_manager_module_v1,
)


def run_speech_manager_module_v1(payload: Mapping[str, Any]) -> Dict[str, Any]:
    return _run_speech_manager_module_v1(payload)
