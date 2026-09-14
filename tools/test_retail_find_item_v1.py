#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最小验证：retail_find_item_v1

覆盖：
1) 默认关闭 → 不附加 metadata["retail_find_item_v1"]
2) 开启 + 非零售环境 → 不触发结论，仅白盒（或无外显）
3) 开启 + 零售环境 + 找货意图 + whitebox-only → 只留白盒，不外显
4) 开启 + 零售环境 + 找货意图 + 非 whitebox-only + 无高风险 → 产生最小结论
5) 开启 + 高风险/抢占 → output_suppressed_by_risk=true，零售链不外显
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from capabilities.cross_domain.retail_find_item_v1 import (  # noqa: E402
    FindItemIntentInput,
    OcrSummaryInput,
    RetailEnvironmentInput,
    RiskSummaryInput,
    evaluate_retail_find_item_v1,
)


def _assert(name: str, cond: bool, msg: str = "") -> None:
    if not cond:
        raise AssertionError(f"[{name}] {msg}")


def main() -> None:
    ts = 1_700_001_000_000

    env_retail = RetailEnvironmentInput(
        scene_type="retail_shelf",
        retail_context_confidence=0.8,
        shelf_visible=True,
        gating_passed=True,
    )
    env_non = RetailEnvironmentInput(
        scene_type="unknown", retail_context_confidence=0.2, shelf_visible=False
    )

    intent_active = FindItemIntentInput(
        active=True,
        query="矿泉水",
        user_requested_reading=True,
        need_text_to_progress=False,
        ocr_budget_ok=True,
    )
    intent_none = FindItemIntentInput(active=False)

    ocr_hit = OcrSummaryInput(
        text_digest="农夫山泉 矿泉水 550ml", confidence=0.8, roi_hint="shelf_mid"
    )

    # 1) 默认关闭
    os.environ.pop("LUNA_ENABLE_RETAIL_FIND_ITEM_V1", None)
    os.environ["LUNA_RETAIL_FIND_ITEM_WHITEBOX_ONLY"] = "0"
    r1 = evaluate_retail_find_item_v1(
        environment=env_retail,
        intent=intent_active,
        ocr_summary=ocr_hit,
        timestamp_ms=ts,
    )
    _assert("default_off_no_meta", "retail_find_item_v1" not in r1.metadata)
    _assert("default_off_no_spoken", r1.final_spoken_output == "")
    print("==== default_off ====")
    print("metadata keys:", list(r1.metadata.keys()))
    print("OK\n")

    # 2) 开启 + 非零售环境 → gating_failed
    os.environ["LUNA_ENABLE_RETAIL_FIND_ITEM_V1"] = "1"
    os.environ["LUNA_RETAIL_FIND_ITEM_WHITEBOX_ONLY"] = "0"
    r2 = evaluate_retail_find_item_v1(
        environment=env_non,
        intent=intent_active,
        ocr_summary=ocr_hit,
        timestamp_ms=ts,
    )
    wb2 = r2.metadata.get("retail_find_item_v1", {})
    _assert("enabled_non_retail_meta", isinstance(wb2, dict) and bool(wb2))
    _assert("non_retail_no_spoken", r2.final_spoken_output == "")
    _assert("non_retail_gating", r2.gating_passed is False)
    print("==== enabled_non_retail ====")
    print(json.dumps(wb2.get("gating_result", {}), ensure_ascii=False, indent=2))
    print("OK\n")

    # 3) 开启 + 零售环境 + 找货意图 + whitebox-only
    os.environ["LUNA_RETAIL_FIND_ITEM_WHITEBOX_ONLY"] = "1"
    r3 = evaluate_retail_find_item_v1(
        environment=env_retail,
        intent=intent_active,
        ocr_summary=ocr_hit,
        timestamp_ms=ts,
    )
    wb3 = r3.metadata.get("retail_find_item_v1", {})
    _assert("wb_only_meta", isinstance(wb3, dict) and bool(wb3))
    _assert("wb_only_no_spoken", r3.final_spoken_output == "")
    _assert(
        "wb_only_item_match_summary_logged",
        isinstance(wb3.get("item_match_summary", ""), str),
    )
    print("==== enabled_whitebox_only ====")
    print("final_spoken_output:", repr(r3.final_spoken_output))
    print("OK\n")

    # 4) 开启 + 非白盒 + 零售环境 + 找货意图 + 无高风险 → 产生最小结论
    os.environ["LUNA_RETAIL_FIND_ITEM_WHITEBOX_ONLY"] = "0"
    r4 = evaluate_retail_find_item_v1(
        environment=env_retail,
        intent=intent_active,
        ocr_summary=ocr_hit,
        risk=RiskSummaryInput(risk_level="low"),
        timestamp_ms=ts,
    )
    wb4 = r4.metadata.get("retail_find_item_v1", {})
    _assert("visible_meta", isinstance(wb4, dict) and bool(wb4))
    _assert("visible_spoken", r4.final_spoken_output != "")
    _assert("not_suppressed", r4.output_suppressed_by_risk is False)
    _assert(
        "ocr_triggered_true",
        r4.ocr_triggered is True,
        "expected ocr_triggered when user_requested_reading",
    )
    print("==== enabled_visible_conclusion ====")
    print("final_spoken_output:", repr(r4.final_spoken_output))
    print("OK\n")

    # 5) 开启 + 高风险：压制
    r5 = evaluate_retail_find_item_v1(
        environment=env_retail,
        intent=intent_active,
        ocr_summary=ocr_hit,
        risk=RiskSummaryInput(risk_level="high", risk_type="vehicle", risk_interrupt_preempt=False),
        timestamp_ms=ts,
    )
    wb5 = r5.metadata.get("retail_find_item_v1", {})
    _assert("high_risk_meta", isinstance(wb5, dict) and bool(wb5))
    _assert("high_risk_suppressed", r5.output_suppressed_by_risk is True)
    _assert("high_risk_no_spoken", r5.final_spoken_output == "")
    _assert("high_risk_wb_suppressed", wb5.get("output_suppressed_by_risk") is True)
    print("==== high_risk_suppressed ====")
    print("output_suppressed_by_risk:", r5.output_suppressed_by_risk)
    print("OK\n")

    # 6) gating 通过但无找货意图：不触发 OCR，不外显
    r6 = evaluate_retail_find_item_v1(
        environment=env_retail,
        intent=intent_none,
        ocr_summary=ocr_hit,
        risk=RiskSummaryInput(risk_level="low"),
        timestamp_ms=ts,
    )
    wb6 = r6.metadata.get("retail_find_item_v1", {})
    _assert("no_intent_meta", isinstance(wb6, dict) and bool(wb6))
    _assert("no_intent_no_ocr", r6.ocr_triggered is False)
    _assert("no_intent_no_spoken", r6.final_spoken_output == "")
    print("==== retail_no_intent ====")
    print("ocr_trigger_reason:", wb6.get("ocr_trigger_reason"))
    print("OK\n")

    print("All tests passed.")


if __name__ == "__main__":
    main()

