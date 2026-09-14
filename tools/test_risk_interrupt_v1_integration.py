#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
风险打断闭环 V1：主线边缘集成验证（不改主链）

验证目标：
1) 普通输出进行中 + high/critical → interrupt_applied=true，task_paused=true
2) 普通输出进行中 + medium → 不抢占，只留白盒
3) whitebox-only + critical → 不抢占，只留白盒
4) 默认关闭（LUNA_ENABLE_RISK_INTERRUPT_V1=0）→ 不生成 risk_interrupt_v1 metadata

说明：
- 这里的“主线边缘”指：使用主链会产生的结果载体（VoiceFinalTextDispatchResult.metadata）
  来承载 risk_interrupt_v1 的白盒字段，验证不会污染主链默认行为。
- 不做真实 TTS 播放/中断，仅验证“裁决结果 + paused_by_risk 标记 + 白盒字段”。
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from capabilities.cross_domain.risk_interrupt_v1 import (  # noqa: E402
    OutputStateSnapshot,
    RiskInterruptEventV1,
    TaskChainStateSnapshot,
    handle_risk_interrupt_v1,
)


def _make_mainline_like_result_metadata() -> dict:
    """
    主链边缘载体：用一个最小 dict 模拟 VoiceFinalTextDispatchResult.metadata 的形态。
    说明：不直接 import dispatcher/运行时以避免引入额外依赖；本脚本验证的是“挂载行为与字段完整性”。
    """
    return {
        "notes": "mainline_output_placeholder",
        "output_category": "task_tip",
        "output_digest": "沿人行道直行 50 米",
    }


def _attach_whitebox(meta: dict, wb: dict) -> dict:
    meta2 = dict(meta)
    meta2["risk_interrupt_v1"] = wb
    return meta2


def _assert_fields(wb: dict) -> None:
    must = [
        "event_timestamp",
        "risk_event_summary",
        "original_output",
        "interrupt_applied",
        "task_paused",
        "final_spoken_output",
        "interrupt_reason",
    ]
    missing = [k for k in must if k not in wb]
    assert not missing, f"missing whitebox fields: {missing}"


def _run_case(*, name: str, env: dict, risk_level: str, expect_interrupt: bool, expect_task_paused: bool) -> None:
    # isolate env knobs for this case
    os.environ.pop("LUNA_ENABLE_RISK_INTERRUPT_V1", None)
    os.environ.pop("LUNA_RISK_INTERRUPT_WHITEBOX_ONLY", None)
    os.environ.update(env)

    meta = _make_mainline_like_result_metadata()

    task = TaskChainStateSnapshot(task_chain_id="tc1", task_status="running")
    current_output = OutputStateSnapshot(speaking=True, output_category="task_tip", output_digest=str(meta.get("output_digest") or ""))

    event = RiskInterruptEventV1.new(
        risk_type="test_risk",
        risk_level=risk_level,
        direction_hint="前",
        distance_band="near",
        confidence=0.9,
    )

    decision = handle_risk_interrupt_v1(event=event, current_output=current_output, task_state=task)

    # 默认关闭：不应生成白盒字段（由上层决定是否挂载）。本脚本按“集成口径”：
    # 只有 enabled 时才把 metadata["risk_interrupt_v1"] 挂上去。
    enabled = os.getenv("LUNA_ENABLE_RISK_INTERRUPT_V1", "").strip() in ("1", "true", "yes")
    if enabled:
        meta = _attach_whitebox(meta, decision.metadata.get("risk_interrupt_v1", {}))

    print("====", name, "====")
    print("env:", {k: os.getenv(k, "") for k in ("LUNA_ENABLE_RISK_INTERRUPT_V1", "LUNA_RISK_INTERRUPT_WHITEBOX_ONLY")})
    print("risk_level:", risk_level)
    print("interrupt_applied:", decision.interrupt_applied, "expect:", expect_interrupt)
    print("task_paused:", decision.task_paused, "expect:", expect_task_paused, "paused_by_risk:", task.paused_by_risk)
    print("interrupt_reason:", decision.interrupt_reason)
    print("final_spoken_output:", repr(decision.final_spoken_output))

    if enabled:
        wb = meta.get("risk_interrupt_v1")
        assert isinstance(wb, dict), "risk_interrupt_v1 not attached"
        _assert_fields(wb)
        assert bool(wb.get("interrupt_applied")) == bool(expect_interrupt), "whitebox interrupt_applied mismatch"
        assert bool(wb.get("task_paused")) == bool(expect_task_paused), "whitebox task_paused mismatch"
        print("whitebox:", json.dumps(wb, ensure_ascii=False, indent=2))
    else:
        assert "risk_interrupt_v1" not in meta, "disabled should not attach risk_interrupt_v1"
        print("whitebox: (not attached; disabled)")

    assert decision.interrupt_applied is bool(expect_interrupt), "decision interrupt_applied mismatch"
    assert decision.task_paused is bool(expect_task_paused), "decision task_paused mismatch"
    print("")


def main() -> None:
    # 0) 默认关闭
    _run_case(
        name="disabled_critical",
        env={"LUNA_ENABLE_RISK_INTERRUPT_V1": "0", "LUNA_RISK_INTERRUPT_WHITEBOX_ONLY": "0"},
        risk_level="critical",
        expect_interrupt=False,
        expect_task_paused=False,
    )

    # 1) 普通输出 + critical → 抢占
    _run_case(
        name="critical_preempt",
        env={"LUNA_ENABLE_RISK_INTERRUPT_V1": "1", "LUNA_RISK_INTERRUPT_WHITEBOX_ONLY": "0"},
        risk_level="critical",
        expect_interrupt=True,
        expect_task_paused=True,
    )

    # 2) 普通输出 + medium → 只白盒
    _run_case(
        name="medium_whitebox",
        env={"LUNA_ENABLE_RISK_INTERRUPT_V1": "1", "LUNA_RISK_INTERRUPT_WHITEBOX_ONLY": "0"},
        risk_level="medium",
        expect_interrupt=False,
        expect_task_paused=False,
    )

    # 3) whitebox-only + critical → 不抢占，只白盒
    _run_case(
        name="critical_whitebox_only",
        env={"LUNA_ENABLE_RISK_INTERRUPT_V1": "1", "LUNA_RISK_INTERRUPT_WHITEBOX_ONLY": "1"},
        risk_level="critical",
        expect_interrupt=False,
        expect_task_paused=False,
    )


if __name__ == "__main__":
    main()

