#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最小验证：Sidewalk Nav V1

1) 默认关闭：不附加 metadata["sidewalk_nav_v1"]
2) 开启 + 无高风险 + 命中人行道：最小导航提示
3) 开启 + 高风险：压下导航，output_suppressed_by_risk=true
4) 开启 + whitebox-only：只留白盒，final_spoken_output 为空
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from capabilities.cross_domain.sidewalk_nav_v1 import (
    RiskSummaryInput,
    SidewalkEnvironmentInput,
    evaluate_sidewalk_nav_v1,
)


def _assert(name: str, cond: bool, msg: str = "") -> None:
    if not cond:
        raise AssertionError(f"[{name}] {msg}")


def main() -> None:
    ts = 1_700_000_000_000
    env_walk = SidewalkEnvironmentInput(
        scene_candidate="outdoor_walkway",
        path_confidence=0.8,
        is_outdoor=True,
    )
    risk_low = RiskSummaryInput(risk_level="low", risk_type="", safe_direction_hint="")
    risk_high = RiskSummaryInput(
        risk_level="high",
        risk_type="vehicle",
        safe_direction_hint="left",
    )

    # 1) 默认关闭
    os.environ.pop("LUNA_ENABLE_SIDEWALK_NAV_V1", None)
    os.environ["LUNA_SIDEWALK_NAV_WHITEBOX_ONLY"] = "0"
    r1 = evaluate_sidewalk_nav_v1(
        environment=env_walk, risk=risk_low, timestamp_ms=ts
    )
    _assert("default_off_no_meta", "sidewalk_nav_v1" not in r1.metadata)
    print("==== default_off ====")
    print("metadata keys:", list(r1.metadata.keys()))
    print("OK\n")

    # 2) 开启 + 无高风险 + 人行道 + 非白盒
    os.environ["LUNA_ENABLE_SIDEWALK_NAV_V1"] = "1"
    os.environ["LUNA_SIDEWALK_NAV_WHITEBOX_ONLY"] = "0"
    r2 = evaluate_sidewalk_nav_v1(
        environment=env_walk, risk=risk_low, timestamp_ms=ts
    )
    wb2 = r2.metadata.get("sidewalk_nav_v1", {})
    _assert("enabled_nav", r2.navigation_hint != "")
    _assert("enabled_spoken", r2.final_spoken_output == r2.navigation_hint)
    _assert("not_suppressed", not r2.output_suppressed_by_risk)
    _assert("wb_fields", all(k in wb2 for k in (
        "scene_summary", "sidewalk_detected", "risk_summary", "navigation_hint",
        "output_suppressed_by_risk", "final_spoken_output", "event_timestamp",
    )))
    print("==== enabled_nav_hint ====")
    print(json.dumps(wb2, ensure_ascii=False, indent=2))
    print("OK\n")

    # 3) 开启 + 高风险
    r3 = evaluate_sidewalk_nav_v1(
        environment=env_walk, risk=risk_high, timestamp_ms=ts
    )
    wb3 = r3.metadata.get("sidewalk_nav_v1", {})
    _assert("high_suppress", r3.output_suppressed_by_risk)
    _assert("high_no_nav", r3.navigation_hint == "")
    _assert("high_no_spoken", r3.final_spoken_output == "")
    _assert("wb_suppressed", wb3.get("output_suppressed_by_risk") is True)
    print("==== high_risk_suppressed ====")
    print("navigation_hint:", repr(r3.navigation_hint))
    print("OK\n")

    # 4) whitebox-only：有逻辑 navigation_hint，但不外显
    os.environ["LUNA_SIDEWALK_NAV_WHITEBOX_ONLY"] = "1"
    r4 = evaluate_sidewalk_nav_v1(
        environment=env_walk, risk=risk_low, timestamp_ms=ts
    )
    wb4 = r4.metadata.get("sidewalk_nav_v1", {})
    _assert("wb_only_hint_logged", wb4.get("navigation_hint") != "")
    _assert("wb_only_no_spoken", r4.final_spoken_output == "")
    print("==== whitebox_only ====")
    print("final_spoken_output:", repr(r4.final_spoken_output))
    print("wb navigation_hint:", repr(wb4.get("navigation_hint")))
    print("OK\n")

    # 5) risk_interrupt_preempt 压下（无高风险摘要时也可由上层标记）
    os.environ["LUNA_SIDEWALK_NAV_WHITEBOX_ONLY"] = "0"
    r5 = evaluate_sidewalk_nav_v1(
        environment=env_walk,
        risk=risk_low,
        timestamp_ms=ts,
        risk_interrupt_preempt=True,
    )
    _assert("preempt_suppress", r5.output_suppressed_by_risk)
    _assert("preempt_empty_nav", r5.navigation_hint == "")
    print("==== risk_interrupt_preempt ====")
    print("output_suppressed_by_risk:", r5.output_suppressed_by_risk)
    print("OK\n")

    print("All tests passed.")


if __name__ == "__main__":
    main()
