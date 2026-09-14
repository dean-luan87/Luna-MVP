#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最小验证脚本：Risk Interrupt V1

覆盖 3 个用例：
1) high/critical 风险事件（允许抢占，非 whitebox-only）
2) medium 风险事件（不抢占，只留白盒）
3) whitebox-only 模式（即使 high 也不抢占，只留白盒）

注意：
- 不依赖任何主链；只验证旁路模块的可用性与回退边界。
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from capabilities.cross_domain.risk_interrupt_v1 import (
    OutputStateSnapshot,
    RiskInterruptEventV1,
    TaskChainStateSnapshot,
    handle_risk_interrupt_v1,
)


def _run_case(*, name: str, env: dict, event: RiskInterruptEventV1):
    os.environ.update(env)
    task = TaskChainStateSnapshot(task_chain_id="t1", task_status="running")
    out = OutputStateSnapshot(speaking=True, output_category="task_tip", output_digest="沿人行道直行 50 米")
    res = handle_risk_interrupt_v1(event=event, current_output=out, task_state=task)
    print("====", name, "====")
    print("interrupt_applied:", res.interrupt_applied)
    print("task_paused:", res.task_paused, "paused_by_risk:", task.paused_by_risk)
    print("final_spoken_output:", repr(res.final_spoken_output))
    print("interrupt_reason:", res.interrupt_reason)
    print("whitebox:", json.dumps(res.metadata.get("risk_interrupt_v1", {}), ensure_ascii=False, indent=2))
    print("")


def main() -> None:
    base_env = {
        "LUNA_ENABLE_RISK_INTERRUPT_V1": "1",
    }

    # 1) high (preempt) with whitebox-only=0
    _run_case(
        name="high_preempt",
        env={**base_env, "LUNA_RISK_INTERRUPT_WHITEBOX_ONLY": "0"},
        event=RiskInterruptEventV1.new(
            risk_type="fast_approaching_vehicle",
            risk_level="high",
            direction_hint="右",
            distance_band="near",
            confidence=0.9,
        ),
    )

    # 2) medium (no preempt)
    _run_case(
        name="medium_whitebox",
        env={**base_env, "LUNA_RISK_INTERRUPT_WHITEBOX_ONLY": "0"},
        event=RiskInterruptEventV1.new(
            risk_type="crowd_close",
            risk_level="medium",
            direction_hint="前",
            distance_band="near",
            confidence=0.6,
        ),
    )

    # 3) whitebox-only (high but no preempt)
    _run_case(
        name="high_whitebox_only",
        env={**base_env, "LUNA_RISK_INTERRUPT_WHITEBOX_ONLY": "1"},
        event=RiskInterruptEventV1.new(
            risk_type="step_hazard",
            risk_level="critical",
            direction_hint="前",
            distance_band="near",
            confidence=0.95,
        ),
    )


if __name__ == "__main__":
    main()

