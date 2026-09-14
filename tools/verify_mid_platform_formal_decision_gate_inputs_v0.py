# -*- coding: utf-8 -*-
from __future__ import annotations

import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))


def main() -> None:
    from capabilities.mid_platform.runtime.formal_decision_gate_inputs_v0 import (
        read_formal_decision_gate_inputs_v0,
    )

    # 场景：只读承接 safety_gate_v0 + task_validity_v0（不伪造）
    applicable, gi = read_formal_decision_gate_inputs_v0(
        runtime_context_metadata={
            "safety_gate_v0": {
                "safety_gate_present": True,
                "safety_status": "safe",
                "safety_preempt_active": False,
            },
            "task_validity_v0": {
                "task_validity_present": True,
                "task_validity_status": "active",
            },
        }
    )
    assert applicable is True and isinstance(gi, dict)
    assert gi.get("consume_mode") == "read_only"
    assert gi.get("safety_gate_v0_present") is True
    assert gi.get("safety_status") == "safe"
    assert gi.get("task_validity_v0_present") is True
    assert gi.get("task_validity_status") == "active"

    print("VERIFY_MID_PLATFORM_FORMAL_DECISION_GATE_INPUTS_V0: ALL_OK")


if __name__ == "__main__":
    main()

