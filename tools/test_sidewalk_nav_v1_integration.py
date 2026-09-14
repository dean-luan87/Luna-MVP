#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
人行道导航 V1：主线边缘集成验证（不改主链）

验证目标：
1) 默认关闭：不挂载 metadata["sidewalk_nav_v1"]，对主链载体无副作用
2) 开启 + WHITEBOX_ONLY=1：挂载白盒；navigation_hint 可非空；final_spoken_output 为空
3) 开启 + WHITEBOX_ONLY=0 + 人行道 + 低风险：final_spoken_output 有值
4) 开启 + 高风险 或 risk_interrupt_preempt：output_suppressed_by_risk，普通导航不外显

说明：
- “主线边缘”指：用与主链输出一致的最小 metadata dict（类比 VoiceFinalTextDispatchResult.metadata）
  挂载 sidewalk_nav_v1 白盒，验证合并行为与字段完整性。
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any, Dict

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from capabilities.cross_domain.sidewalk_nav_v1 import (  # noqa: E402
    RiskSummaryInput,
    SidewalkEnvironmentInput,
    SidewalkNavResult,
    evaluate_sidewalk_nav_v1,
)


def _make_mainline_like_metadata() -> Dict[str, Any]:
    """模拟主链输出 metadata 的最小形态。"""
    return {
        "notes": "mainline_output_placeholder",
        "output_category": "task_tip",
        "output_digest": "沿人行道直行 50 米",
    }


def _merge_sidewalk_nav_into_metadata(
    meta: Dict[str, Any], result: SidewalkNavResult
) -> Dict[str, Any]:
    """上层集成点：仅当旁路返回含 sidewalk_nav_v1 时并入。"""
    wb = result.metadata.get("sidewalk_nav_v1")
    if not wb:
        return dict(meta)
    out = dict(meta)
    out["sidewalk_nav_v1"] = wb
    return out


def _assert_wb_complete(wb: Dict[str, Any]) -> None:
    must = [
        "scene_summary",
        "sidewalk_detected",
        "risk_summary",
        "navigation_hint",
        "output_suppressed_by_risk",
        "final_spoken_output",
        "event_timestamp",
    ]
    missing = [k for k in must if k not in wb]
    assert not missing, f"missing whitebox fields: {missing}"


def _clear_sidewalk_env() -> None:
    os.environ.pop("LUNA_ENABLE_SIDEWALK_NAV_V1", None)
    os.environ.pop("LUNA_SIDEWALK_NAV_WHITEBOX_ONLY", None)


def main() -> None:
    ts = 1_700_000_100_000
    env_walk = SidewalkEnvironmentInput(
        scene_candidate="outdoor_walkway",
        path_confidence=0.8,
        is_outdoor=True,
    )
    risk_low = RiskSummaryInput(risk_level="low")
    risk_high = RiskSummaryInput(risk_level="high", risk_type="vehicle", safe_direction_hint="left")

    # 1) 默认关闭：不挂载，metadata 仅主链占位
    _clear_sidewalk_env()
    os.environ["LUNA_ENABLE_SIDEWALK_NAV_V1"] = "0"
    meta0 = _make_mainline_like_metadata()
    r0 = evaluate_sidewalk_nav_v1(environment=env_walk, risk=risk_low, timestamp_ms=ts)
    merged0 = _merge_sidewalk_nav_into_metadata(meta0, r0)
    assert "sidewalk_nav_v1" not in merged0, "disabled must not attach sidewalk_nav_v1"
    assert merged0 == meta0, "disabled must not mutate mainline metadata keys unexpectedly"
    print("==== disabled_zero_intrusion ====")
    print("metadata keys:", list(merged0.keys()))
    print("OK\n")

    # 2) 开启 + WHITEBOX_ONLY=1：白盒完整，不外显
    os.environ["LUNA_ENABLE_SIDEWALK_NAV_V1"] = "1"
    os.environ["LUNA_SIDEWALK_NAV_WHITEBOX_ONLY"] = "1"
    meta1 = _make_mainline_like_metadata()
    r1 = evaluate_sidewalk_nav_v1(environment=env_walk, risk=risk_low, timestamp_ms=ts)
    merged1 = _merge_sidewalk_nav_into_metadata(meta1, r1)
    wb1 = merged1.get("sidewalk_nav_v1")
    assert isinstance(wb1, dict)
    _assert_wb_complete(wb1)
    assert wb1.get("sidewalk_detected") is True
    assert wb1.get("navigation_hint"), "whitebox should log navigation_hint when walkway"
    assert wb1.get("final_spoken_output") == "", "whitebox-only must not expose spoken nav"
    assert r1.final_spoken_output == ""
    print("==== enabled_whitebox_only ====")
    print(json.dumps(wb1, ensure_ascii=False, indent=2))
    print("OK\n")

    # 3) 开启 + 非白盒 + 人行道 + 低风险：外显最小导航
    os.environ["LUNA_SIDEWALK_NAV_WHITEBOX_ONLY"] = "0"
    meta2 = _make_mainline_like_metadata()
    r2 = evaluate_sidewalk_nav_v1(environment=env_walk, risk=risk_low, timestamp_ms=ts)
    merged2 = _merge_sidewalk_nav_into_metadata(meta2, r2)
    wb2 = merged2["sidewalk_nav_v1"]
    _assert_wb_complete(wb2)
    assert wb2.get("output_suppressed_by_risk") is False
    assert wb2.get("final_spoken_output") != ""
    assert r2.final_spoken_output == wb2.get("final_spoken_output")
    print("==== enabled_nav_visible ====")
    print("final_spoken_output:", repr(r2.final_spoken_output))
    print("OK\n")

    # 4) 高风险：压制 + 白盒完整
    meta3 = _make_mainline_like_metadata()
    r3 = evaluate_sidewalk_nav_v1(environment=env_walk, risk=risk_high, timestamp_ms=ts)
    merged3 = _merge_sidewalk_nav_into_metadata(meta3, r3)
    wb3 = merged3["sidewalk_nav_v1"]
    _assert_wb_complete(wb3)
    assert r3.output_suppressed_by_risk is True
    assert wb3.get("output_suppressed_by_risk") is True
    assert r3.navigation_hint == ""
    assert r3.final_spoken_output == ""
    assert wb3.get("final_spoken_output") == ""
    print("==== high_risk_suppressed ====")
    print(json.dumps(wb3, ensure_ascii=False, indent=2))
    print("OK\n")

    # 5) risk_interrupt_preempt：压制（模拟 risk_interrupt_v1 已抢占）
    meta4 = _make_mainline_like_metadata()
    r4 = evaluate_sidewalk_nav_v1(
        environment=env_walk,
        risk=risk_low,
        timestamp_ms=ts,
        risk_interrupt_preempt=True,
    )
    merged4 = _merge_sidewalk_nav_into_metadata(meta4, r4)
    wb4 = merged4["sidewalk_nav_v1"]
    _assert_wb_complete(wb4)
    assert r4.output_suppressed_by_risk is True
    assert wb4.get("risk_summary", {}).get("risk_interrupt_preempt") is True
    assert r4.final_spoken_output == ""
    print("==== risk_interrupt_preempt_suppressed ====")
    print("output_suppressed_by_risk:", wb4.get("output_suppressed_by_risk"))
    print("OK\n")

    print("All integration checks passed.")


if __name__ == "__main__":
    main()
