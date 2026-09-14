#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
retail_find_item_v1：主线边缘集成验证（不改主链）

验证目标：
1) 默认关闭：不挂载 metadata["retail_find_item_v1"]，主链零侵入
2) 开启 + WHITEBOX_ONLY=1：挂载白盒；item_match_summary/task_evidence 有值（零售+意图）；final_spoken_output 为空
3) 开启 + WHITEBOX_ONLY=0 + 零售环境 + 找货意图 + 无高风险：final_spoken_output 有值
4) 开启 + 高风险 或 risk_interrupt_preempt：output_suppressed_by_risk=true，零售链不外显
5) 开启 + 非零售环境：不外显结论，不误入零售主流程

说明：
- “主线边缘”指：用与主链输出一致的最小 metadata dict（类比 VoiceFinalTextDispatchResult.metadata）
  挂载 retail_find_item_v1 白盒，验证合并行为与字段完整性。
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any, Dict

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from capabilities.cross_domain.retail_find_item_v1 import (  # noqa: E402
    FindItemIntentInput,
    OcrSummaryInput,
    RetailEnvironmentInput,
    RetailFindItemResult,
    RiskSummaryInput,
    evaluate_retail_find_item_v1,
)


def _make_mainline_like_metadata() -> Dict[str, Any]:
    return {
        "notes": "mainline_output_placeholder",
        "output_category": "task_tip",
        "output_digest": "你现在在逛超市",
    }


def _merge_retail_find_item_into_metadata(
    meta: Dict[str, Any], result: RetailFindItemResult
) -> Dict[str, Any]:
    wb = result.metadata.get("retail_find_item_v1")
    if not wb:
        return dict(meta)
    out = dict(meta)
    out["retail_find_item_v1"] = wb
    return out


def _assert_wb_complete(wb: Dict[str, Any]) -> None:
    must = [
        "scene_summary",
        "gating_result",
        "ocr_trigger_reason",
        "ocr_summary",
        "item_match_summary",
        "task_evidence",
        "output_suppressed_by_risk",
        "final_spoken_output",
        "event_timestamp",
    ]
    missing = [k for k in must if k not in wb]
    assert not missing, f"missing whitebox fields: {missing}"


def _clear_env() -> None:
    os.environ.pop("LUNA_ENABLE_RETAIL_FIND_ITEM_V1", None)
    os.environ.pop("LUNA_RETAIL_FIND_ITEM_WHITEBOX_ONLY", None)


def main() -> None:
    ts = 1_700_002_000_000

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
        ocr_budget_ok=True,
    )
    intent_none = FindItemIntentInput(active=False)

    ocr_hit = OcrSummaryInput(text_digest="农夫山泉 矿泉水 550ml", confidence=0.8, roi_hint="shelf_mid")

    # 1) 默认关闭：零侵入
    _clear_env()
    os.environ["LUNA_ENABLE_RETAIL_FIND_ITEM_V1"] = "0"
    meta0 = _make_mainline_like_metadata()
    r0 = evaluate_retail_find_item_v1(
        environment=env_retail,
        intent=intent_active,
        ocr_summary=ocr_hit,
        timestamp_ms=ts,
    )
    merged0 = _merge_retail_find_item_into_metadata(meta0, r0)
    assert "retail_find_item_v1" not in merged0, "disabled must not attach retail_find_item_v1"
    assert merged0 == meta0, "disabled must not mutate mainline metadata unexpectedly"
    print("==== disabled_zero_intrusion ====")
    print("metadata keys:", list(merged0.keys()))
    print("OK\n")

    # 2) 开启 + WHITEBOX_ONLY=1：白盒完整，不外显
    os.environ["LUNA_ENABLE_RETAIL_FIND_ITEM_V1"] = "1"
    os.environ["LUNA_RETAIL_FIND_ITEM_WHITEBOX_ONLY"] = "1"
    meta1 = _make_mainline_like_metadata()
    r1 = evaluate_retail_find_item_v1(
        environment=env_retail,
        intent=intent_active,
        ocr_summary=ocr_hit,
        risk=RiskSummaryInput(risk_level="low"),
        timestamp_ms=ts,
    )
    merged1 = _merge_retail_find_item_into_metadata(meta1, r1)
    wb1 = merged1.get("retail_find_item_v1")
    assert isinstance(wb1, dict)
    _assert_wb_complete(wb1)
    assert wb1.get("final_spoken_output") == "", "whitebox-only must not expose spoken conclusion"
    assert wb1.get("item_match_summary"), "whitebox should log item_match_summary (retail+intent)"
    assert isinstance(wb1.get("task_evidence"), dict) and wb1.get("task_evidence"), "whitebox should log task_evidence"
    print("==== enabled_whitebox_only ====")
    print(json.dumps(wb1, ensure_ascii=False, indent=2))
    print("OK\n")

    # 3) 开启 + 非白盒 + 零售环境 + 找货意图 + 无高风险：外显最小结论
    os.environ["LUNA_RETAIL_FIND_ITEM_WHITEBOX_ONLY"] = "0"
    meta2 = _make_mainline_like_metadata()
    r2 = evaluate_retail_find_item_v1(
        environment=env_retail,
        intent=intent_active,
        ocr_summary=ocr_hit,
        risk=RiskSummaryInput(risk_level="low"),
        timestamp_ms=ts,
    )
    merged2 = _merge_retail_find_item_into_metadata(meta2, r2)
    wb2 = merged2["retail_find_item_v1"]
    _assert_wb_complete(wb2)
    assert wb2.get("output_suppressed_by_risk") is False
    assert wb2.get("final_spoken_output"), "visible mode should produce a conclusion"
    assert r2.final_spoken_output == wb2.get("final_spoken_output")
    print("==== enabled_conclusion_visible ====")
    print("final_spoken_output:", repr(r2.final_spoken_output))
    print("OK\n")

    # 4) 高风险：压制 + 白盒完整
    meta3 = _make_mainline_like_metadata()
    r3 = evaluate_retail_find_item_v1(
        environment=env_retail,
        intent=intent_active,
        ocr_summary=ocr_hit,
        risk=RiskSummaryInput(risk_level="high", risk_type="vehicle", risk_interrupt_preempt=False),
        timestamp_ms=ts,
    )
    merged3 = _merge_retail_find_item_into_metadata(meta3, r3)
    wb3 = merged3["retail_find_item_v1"]
    _assert_wb_complete(wb3)
    assert r3.output_suppressed_by_risk is True
    assert wb3.get("output_suppressed_by_risk") is True
    assert r3.final_spoken_output == ""
    assert wb3.get("final_spoken_output") == ""
    print("==== high_risk_suppressed ====")
    print("output_suppressed_by_risk:", wb3.get("output_suppressed_by_risk"))
    print("OK\n")

    # 4b) risk_interrupt_preempt：压制（模拟 risk_interrupt_v1 已抢占）
    meta4 = _make_mainline_like_metadata()
    r4 = evaluate_retail_find_item_v1(
        environment=env_retail,
        intent=intent_active,
        ocr_summary=ocr_hit,
        risk=RiskSummaryInput(risk_level="low", risk_interrupt_preempt=True),
        timestamp_ms=ts,
    )
    merged4 = _merge_retail_find_item_into_metadata(meta4, r4)
    wb4 = merged4["retail_find_item_v1"]
    _assert_wb_complete(wb4)
    assert r4.output_suppressed_by_risk is True
    assert wb4.get("risk_summary", {}).get("risk_interrupt_preempt") is True
    assert r4.final_spoken_output == ""
    print("==== risk_interrupt_preempt_suppressed ====")
    print("output_suppressed_by_risk:", wb4.get("output_suppressed_by_risk"))
    print("OK\n")

    # 5) 非零售环境：不外显、不误触发
    meta5 = _make_mainline_like_metadata()
    r5 = evaluate_retail_find_item_v1(
        environment=env_non,
        intent=intent_active,
        ocr_summary=ocr_hit,
        risk=RiskSummaryInput(risk_level="low"),
        timestamp_ms=ts,
    )
    merged5 = _merge_retail_find_item_into_metadata(meta5, r5)
    wb5 = merged5["retail_find_item_v1"]
    _assert_wb_complete(wb5)
    assert r5.gating_passed is False
    assert r5.final_spoken_output == ""
    assert wb5.get("gating_result", {}).get("passed") is False
    print("==== non_retail_no_conclusion ====")
    print(json.dumps(wb5.get("gating_result", {}), ensure_ascii=False, indent=2))
    print("OK\n")

    # 6) 零售环境但无意图：不外显、不误触发 OCR
    meta6 = _make_mainline_like_metadata()
    r6 = evaluate_retail_find_item_v1(
        environment=env_retail,
        intent=intent_none,
        ocr_summary=ocr_hit,
        risk=RiskSummaryInput(risk_level="low"),
        timestamp_ms=ts,
    )
    merged6 = _merge_retail_find_item_into_metadata(meta6, r6)
    wb6 = merged6["retail_find_item_v1"]
    _assert_wb_complete(wb6)
    assert r6.ocr_triggered is False
    assert r6.final_spoken_output == ""
    assert wb6.get("ocr_trigger_reason") == "no_active_intent"
    print("==== retail_no_intent ====")
    print("ocr_trigger_reason:", wb6.get("ocr_trigger_reason"))
    print("OK\n")

    print("All integration checks passed.")


if __name__ == "__main__":
    main()

