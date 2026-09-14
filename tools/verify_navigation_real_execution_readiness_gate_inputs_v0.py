# -*- coding: utf-8 -*-
from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any, Dict

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))


def main() -> None:
    from capabilities.mid_platform.runtime.navigation_real_execution_readiness_gate_inputs_v0 import (
        read_navigation_real_execution_readiness_gate_inputs_v0,
    )

    # 1) none present => not applicable
    app0, out0 = read_navigation_real_execution_readiness_gate_inputs_v0(runtime_context_metadata={})
    assert app0 is False and out0 is None

    # 2) one valid gate present => applicable, with flags
    md: Dict[str, Any] = {
        "navigation_executor_gate_v0": {
            "executor_gate_present": True,
            "executor_available": False,
            "executor_status": "unavailable",
            "executor_takeover_allowed": False,
        }
    }
    app1, out1 = read_navigation_real_execution_readiness_gate_inputs_v0(runtime_context_metadata=md)
    assert app1 is True and isinstance(out1, dict)
    assert out1.get("readiness_gate_inputs_scope") == "navigation_real_execution_readiness_gate_inputs_v0"
    assert out1.get("consume_mode") == "read_only"
    assert out1.get("readiness_gate_inputs_present") is True
    assert out1.get("executor_gate_present") is True
    assert out1.get("executor_status") == "unavailable"

    print("VERIFY_NAVIGATION_REAL_EXECUTION_READINESS_GATE_INPUTS_V0: ALL_OK")


if __name__ == "__main__":
    main()

