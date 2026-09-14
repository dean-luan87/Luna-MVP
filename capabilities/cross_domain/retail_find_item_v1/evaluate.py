#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
retail_find_item_v1：超市找商品最小旁路（默认关闭）。

边界（V1）：
- 不 import 主链；不新增模型
- OCR 仅作为“补证源”：本模块只给出触发决策与摘要接入，不做常驻 OCR 主导链
- 高风险时必须压制零售链外显输出（安全链优先）
"""

from __future__ import annotations

import os
import time
from dataclasses import dataclass, field
from typing import Any, Dict, Optional


def _env_truthy(name: str, *, default: bool = False) -> bool:
    raw = os.getenv(name, "")
    if raw == "":
        return bool(default)
    return raw.strip().lower() in ("1", "true", "yes")


def retail_find_item_enabled() -> bool:
    return _env_truthy("LUNA_ENABLE_RETAIL_FIND_ITEM_V1", default=False)


def retail_find_item_whitebox_only() -> bool:
    # 默认 true：先只白盒验证控噪与触发边界
    return _env_truthy("LUNA_RETAIL_FIND_ITEM_WHITEBOX_ONLY", default=True)


@dataclass(frozen=True)
class RetailEnvironmentInput:
    """最小零售环境输入（V1 可规则占位，后续再接视觉/定位管线）。"""

    scene_type: str = "unknown"  # retail_shelf / retail_aisle / unknown
    retail_context_confidence: float = 0.0
    shelf_visible: bool = False
    # gating 可由上游提供；若为 None，则由本模块用最小规则推断
    gating_passed: Optional[bool] = None


@dataclass(frozen=True)
class FindItemIntentInput:
    """最小找货意图输入（V1 简化）。"""

    active: bool = False
    query: str = ""  # 用户要找的商品名/类别（可为空）
    user_requested_reading: bool = False  # 用户显式要求读标签
    need_text_to_progress: bool = False  # 系统判断需要文字补证才能推进
    ocr_budget_ok: bool = True  # V1 频控占位（由上层计数/冷却后回填）


@dataclass(frozen=True)
class OcrSummaryInput:
    """OCR 补证摘要（V1 作为接口位；可为空）。"""

    text_digest: str = ""
    confidence: float = 0.0
    roi_hint: str = ""  # 如 “center_0.4x0.4” / “shelf_mid”


@dataclass(frozen=True)
class RiskSummaryInput:
    """只读风险摘要（用于压制外显，不做风险生成）。"""

    risk_level: str = "low"  # low|medium|high|critical
    risk_type: str = ""
    risk_interrupt_preempt: bool = False


def _normalize(s: str) -> str:
    return (s or "").strip()


def _normalize_level(level: str) -> str:
    return (level or "").strip().lower()


def _is_high_risk(level: str) -> bool:
    return _normalize_level(level) in ("high", "critical")


def _classify_scene(env: RetailEnvironmentInput) -> tuple[str, bool, float]:
    """
    返回 (scene_type, gating_passed, confidence)。
    V1：若上游给了 gating_passed 就信；否则用最小规则推断。
    """
    scene = (env.scene_type or "").strip().lower()
    conf = float(env.retail_context_confidence or 0.0)

    if isinstance(env.gating_passed, bool):
        gating = bool(env.gating_passed)
    else:
        gating = (scene in ("retail_shelf", "retail_aisle")) and (conf >= 0.45 or bool(env.shelf_visible))

    if scene in ("retail_shelf", "retail_aisle"):
        scene_type = scene
    else:
        scene_type = "unknown"

    return scene_type, gating, max(0.0, min(1.0, conf))


def _decide_ocr_trigger(
    *, gating_passed: bool, intent: FindItemIntentInput
) -> tuple[bool, str]:
    """
    V1 OCR 触发：只做决策，不执行 OCR。
    """
    if not gating_passed:
        return False, "gating_failed"
    if not bool(intent.active):
        return False, "no_active_intent"
    if not bool(intent.ocr_budget_ok):
        return False, "ocr_budget_blocked"
    if bool(intent.user_requested_reading):
        return True, "user_requested_reading"
    if bool(intent.need_text_to_progress):
        return True, "need_text_to_progress"
    return False, "conditions_not_met"


def _match_item(*, query: str, ocr_text: str) -> tuple[str, str]:
    """
    返回 (item_match_status, item_match_summary)。
    V1：弱匹配占位：query 为子串则 weak_match，否则 unknown/no_match。
    """
    q = _normalize(query).lower()
    t = _normalize(ocr_text).lower()

    if not q:
        return "unknown", "未提供目标商品词，暂不做匹配。"
    if not t:
        return "unknown", f"目标为「{query}」，暂无 OCR 补证摘要。"
    if q in t:
        return "weak_match", f"OCR 文本可能包含「{query}」。"
    return "no_match", f"OCR 文本未见「{query}」相关字样（V1 弱匹配）。"


def _minimal_spoken_conclusion(*, query: str, match_status: str, ocr_text: str) -> str:
    if match_status == "weak_match":
        return f"我可能在标签里看到了「{query}」，你面前这排可以重点找一下。"
    if match_status == "no_match":
        return f"我在这块标签里没看到「{query}」，可能需要换一排或再对准标签。"
    # unknown
    if query:
        return f"目标是「{query}」，我可以再帮你读一下标签。"
    if ocr_text:
        return "我读到了一些标签文字，你可以告诉我你要找的具体商品名。"
    return ""


@dataclass(frozen=True)
class RetailFindItemResult:
    scene_type: str
    gating_passed: bool
    ocr_triggered: bool
    item_match_summary: str
    task_evidence: Dict[str, Any]
    output_suppressed_by_risk: bool
    final_spoken_output: str
    # state fields
    current_scene_type: str
    active_find_item_intent: bool
    item_match_status: str
    task_step_updated: bool
    metadata: Dict[str, Any] = field(default_factory=dict)


def evaluate_retail_find_item_v1(
    *,
    environment: RetailEnvironmentInput,
    intent: FindItemIntentInput,
    ocr_summary: Optional[OcrSummaryInput] = None,
    risk: Optional[RiskSummaryInput] = None,
    timestamp_ms: Optional[int] = None,
) -> RetailFindItemResult:
    """
    主入口：零售环境 gating + 找货意图对齐 + OCR 决策占位 + 最小结论 + 白盒。

    说明：
    - 默认关闭：返回 metadata={}（上层不应挂载 retail_find_item_v1）
    - whitebox-only：只留白盒，不外显结论
    - 高风险/抢占：压制外显结论，但仍可留白盒
    """
    ts = int(timestamp_ms if isinstance(timestamp_ms, int) else (time.time() * 1000.0))
    risk = risk or RiskSummaryInput()
    ocr_summary = ocr_summary or OcrSummaryInput()

    scene_type, gating_passed, scene_conf = _classify_scene(environment)

    # 默认关闭：零侵入（不写 metadata key）
    if not retail_find_item_enabled():
        return RetailFindItemResult(
            scene_type=scene_type,
            gating_passed=gating_passed,
            ocr_triggered=False,
            item_match_summary="",
            task_evidence={},
            output_suppressed_by_risk=False,
            final_spoken_output="",
            current_scene_type=scene_type,
            active_find_item_intent=bool(intent.active),
            item_match_status="unknown",
            task_step_updated=False,
            metadata={},
        )

    whitebox_only = retail_find_item_whitebox_only()
    high_risk = _is_high_risk(risk.risk_level) or bool(risk.risk_interrupt_preempt)
    output_suppressed_by_risk = bool(high_risk)

    ocr_triggered, ocr_trigger_reason = _decide_ocr_trigger(
        gating_passed=gating_passed, intent=intent
    )

    item_match_status = "unknown"
    item_match_summary = ""
    if gating_passed and intent.active:
        item_match_status, item_match_summary = _match_item(
            query=intent.query, ocr_text=ocr_summary.text_digest
        )

    # task evidence (V1: minimal)
    task_evidence: Dict[str, Any] = {
        "intent_query": str(intent.query or ""),
        "ocr_triggered": bool(ocr_triggered),
        "ocr_text_digest": str(ocr_summary.text_digest or ""),
        "item_match_status": str(item_match_status),
        "event_timestamp": ts,
    }
    task_step_updated = bool(gating_passed and intent.active)

    # spoken output candidate (V1)
    final_spoken = ""
    if not output_suppressed_by_risk and not whitebox_only and gating_passed and intent.active:
        final_spoken = _minimal_spoken_conclusion(
            query=intent.query,
            match_status=item_match_status,
            ocr_text=ocr_summary.text_digest,
        )

    wb = {
        "scene_summary": {
            "scene_type_input": environment.scene_type,
            "classified_scene_type": scene_type,
            "retail_context_confidence": scene_conf,
            "shelf_visible": bool(environment.shelf_visible),
        },
        "gating_result": {
            "passed": bool(gating_passed),
            "confidence": scene_conf,
        },
        "ocr_trigger_reason": str(ocr_trigger_reason),
        "ocr_summary": {
            "text_digest": str(ocr_summary.text_digest or ""),
            "confidence": float(ocr_summary.confidence or 0.0),
            "roi_hint": str(ocr_summary.roi_hint or ""),
        },
        "item_match_summary": str(item_match_summary),
        "task_evidence": dict(task_evidence),
        "output_suppressed_by_risk": bool(output_suppressed_by_risk),
        "final_spoken_output": str(final_spoken),
        "whitebox_only": bool(whitebox_only),
        "risk_summary": {
            "risk_level": _normalize_level(risk.risk_level) or "low",
            "risk_type": str(risk.risk_type or ""),
            "risk_interrupt_preempt": bool(risk.risk_interrupt_preempt),
        },
        "event_timestamp": ts,
    }

    return RetailFindItemResult(
        scene_type=scene_type,
        gating_passed=bool(gating_passed),
        ocr_triggered=bool(ocr_triggered),
        item_match_summary=str(item_match_summary),
        task_evidence=task_evidence,
        output_suppressed_by_risk=bool(output_suppressed_by_risk),
        final_spoken_output=str(final_spoken),
        current_scene_type=scene_type,
        active_find_item_intent=bool(intent.active),
        item_match_status=str(item_match_status),
        task_step_updated=bool(task_step_updated),
        metadata={"retail_find_item_v1": wb},
    )

