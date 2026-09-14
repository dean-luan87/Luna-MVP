#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
跨域旁路统一 orchestrator（V1）验证

覆盖：
1) 三条旁路全部关闭 → 主链零侵入；不出现 cross_domain_orchestrator_v1 摘要
2) 只开 risk_interrupt_v1 → 仅有 risk_interrupt_v1 metadata；摘要 enabled/executed 正确
3) 三条都开且高风险 → sidewalk/retail 白盒存在且 output_suppressed_by_risk=true；摘要 suppressed 含后两条
4) 三条都开且无高风险 → 三条 metadata 可共存；三条均在 executed_capabilities
5) metadata_keys_attached 与三条旁路实际挂载一致
"""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from capabilities.voice.runtime.voice_input_session_manager import (  # noqa: E402
    VoiceInputSessionManager,
)
from capabilities.voice.schemas.voice_runtime_context import VoiceRuntimeContext  # noqa: E402


def _assert(name: str, cond: bool, msg: str = "") -> None:
    if not cond:
        raise AssertionError(f"[{name}] {msg}")


def _bypass_keys_in_metadata(md: dict) -> list:
    keys = ("risk_interrupt_v1", "sidewalk_nav_v1", "retail_find_item_v1")
    return [k for k in keys if k in md]


def _dispatch(ctx: VoiceRuntimeContext) -> dict:
    mgr = VoiceInputSessionManager()
    res = mgr.process_final_text_with_dispatch(
        "帮我设一个三分钟的计时器",
        now=time.time(),
        is_task_mode=True,
        session_id="s_orch",
        runtime_context=ctx,
    )
    return res.to_dict()


def main() -> None:
    # 保持 orchestrator 默认启用（禁用回退开关必须不设置）
    os.environ.pop("LUNA_DISABLE_CROSS_DOMAIN_ORCHESTRATOR_V1", None)

    base_ctx = VoiceRuntimeContext(
        current_session_id="s_orch",
        metadata={
            "risk_summary_v1": {"risk_level": "low", "risk_interrupt_preempt": False, "timestamp_ms": 1700006000000},
            "sidewalk_env_summary_v1": {"scene_candidate": "outdoor_walkway", "path_confidence": 0.8, "is_outdoor": True},
            "retail_env_summary_v1": {"scene_type_candidate": "retail_shelf", "retail_context_confidence": 0.8, "shelf_visible": True, "gating_passed": True},
            "find_item_intent_summary_v1": {"active": True, "query": "矿泉水", "user_requested_reading": True, "ocr_budget_ok": True},
        },
    )

    # 1) all off
    os.environ["LUNA_ENABLE_RISK_INTERRUPT_V1"] = "0"
    os.environ["LUNA_RISK_INTERRUPT_WHITEBOX_ONLY"] = "1"
    os.environ["LUNA_ENABLE_SIDEWALK_NAV_V1"] = "0"
    os.environ["LUNA_SIDEWALK_NAV_WHITEBOX_ONLY"] = "1"
    os.environ["LUNA_ENABLE_RETAIL_FIND_ITEM_V1"] = "0"
    os.environ["LUNA_RETAIL_FIND_ITEM_WHITEBOX_ONLY"] = "1"
    d0 = _dispatch(base_ctx)
    md0 = d0.get("metadata") or {}
    _assert("all_off_no_keys", "risk_interrupt_v1" not in md0 and "sidewalk_nav_v1" not in md0 and "retail_find_item_v1" not in md0)
    _assert("all_off_no_orch_summary", "cross_domain_orchestrator_v1" not in md0)
    base_dispatch_type = d0.get("dispatch_type")
    base_notes = d0.get("notes")

    # 2) only risk on
    os.environ["LUNA_ENABLE_RISK_INTERRUPT_V1"] = "1"
    os.environ["LUNA_ENABLE_SIDEWALK_NAV_V1"] = "0"
    os.environ["LUNA_ENABLE_RETAIL_FIND_ITEM_V1"] = "0"
    d1 = _dispatch(base_ctx)
    md1 = d1.get("metadata") or {}
    _assert("risk_only_present", "risk_interrupt_v1" in md1)
    _assert("risk_only_absent_others", "sidewalk_nav_v1" not in md1 and "retail_find_item_v1" not in md1)
    _assert("risk_only_no_output_change", d1.get("dispatch_type") == base_dispatch_type and d1.get("notes") == base_notes)
    orch1 = md1.get("cross_domain_orchestrator_v1") or {}
    _assert("risk_only_orch_enabled", orch1.get("enabled_capabilities") == ["risk_interrupt_v1"])
    _assert("risk_only_orch_executed", orch1.get("executed_capabilities") == ["risk_interrupt_v1"])
    _assert("risk_only_orch_keys", orch1.get("metadata_keys_attached") == _bypass_keys_in_metadata(md1))
    _assert("risk_only_orch_order", orch1.get("orchestration_order") == ["risk_interrupt_v1", "sidewalk_nav_v1", "retail_find_item_v1"])
    _assert("risk_only_wb", orch1.get("whitebox_only_mode") is True)
    _assert("risk_only_near_real", orch1.get("near_real_output_candidate_any") is False)

    # 3) all on + high risk
    os.environ["LUNA_ENABLE_SIDEWALK_NAV_V1"] = "1"
    os.environ["LUNA_ENABLE_RETAIL_FIND_ITEM_V1"] = "1"
    ctx_high = VoiceRuntimeContext(
        current_session_id="s_orch",
        metadata={**(base_ctx.metadata or {}), "risk_summary_v1": {"risk_level": "high", "risk_interrupt_preempt": False, "timestamp_ms": 1700006000001}},
    )
    d2 = _dispatch(ctx_high)
    md2 = d2.get("metadata") or {}
    _assert("all_on_keys", all(k in md2 for k in ("risk_interrupt_v1", "sidewalk_nav_v1", "retail_find_item_v1")))
    _assert("sidewalk_suppressed", (md2.get("sidewalk_nav_v1") or {}).get("output_suppressed_by_risk") is True)
    _assert("retail_suppressed", (md2.get("retail_find_item_v1") or {}).get("output_suppressed_by_risk") is True)
    orch2 = md2.get("cross_domain_orchestrator_v1") or {}
    _assert("high_risk_preempt", orch2.get("risk_preempt_active") is True)
    _assert("high_suppressed_list", set(orch2.get("suppressed_capabilities") or []) == {"sidewalk_nav_v1", "retail_find_item_v1"})
    _assert("high_executed_three", orch2.get("executed_capabilities") == ["risk_interrupt_v1", "sidewalk_nav_v1", "retail_find_item_v1"])
    _assert("high_orch_keys", orch2.get("metadata_keys_attached") == _bypass_keys_in_metadata(md2))
    _assert(
        "high_enabled_three",
        orch2.get("enabled_capabilities")
        == ["risk_interrupt_v1", "sidewalk_nav_v1", "retail_find_item_v1"],
    )

    # 4) all on + low risk
    ctx_low = base_ctx
    d3 = _dispatch(ctx_low)
    md3 = d3.get("metadata") or {}
    _assert("all_on_coexist", all(k in md3 for k in ("risk_interrupt_v1", "sidewalk_nav_v1", "retail_find_item_v1")))
    orch3 = md3.get("cross_domain_orchestrator_v1") or {}
    _assert("low_risk_preempt", orch3.get("risk_preempt_active") is False)
    _assert("low_suppressed_empty", (orch3.get("suppressed_capabilities") or []) == [])
    _assert("low_executed_three", orch3.get("executed_capabilities") == ["risk_interrupt_v1", "sidewalk_nav_v1", "retail_find_item_v1"])
    _assert("low_orch_keys", orch3.get("metadata_keys_attached") == _bypass_keys_in_metadata(md3))
    _assert(
        "low_enabled_three",
        orch3.get("enabled_capabilities")
        == ["risk_interrupt_v1", "sidewalk_nav_v1", "retail_find_item_v1"],
    )

    print("All cross-domain orchestrator checks passed.")


if __name__ == "__main__":
    main()

