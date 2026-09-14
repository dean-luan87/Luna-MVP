# -*- coding: utf-8 -*-
"""Document Surface Detector — risk registry v1."""

from __future__ import annotations

from typing import Any, Dict, List

RISK_REGISTRY: List[Dict[str, Any]] = [
    {
        "risk_id": "real_detector_model_selection_deferred",
        "severity": "medium",
        "status": "deferred",
        "description": "第一个真实 document/surface detector 模型尚未选定，需 Implementation Planning 阶段决策。",
        "mitigation": "Implementation Planning 限定可控实现路径与基准口径，不直接执行。",
    },
    {
        "risk_id": "document_vs_screen_ambiguity",
        "severity": "high",
        "status": "monitored",
        "description": "屏幕显示文档与纸张文档在视觉边界上可能混淆。",
        "mitigation": "defer_to_screen_surface_detector guard；screen_surface_not_document_surface_fact。",
    },
    {
        "risk_id": "severe_occlusion_boundary_uncertainty",
        "severity": "high",
        "status": "monitored",
        "description": "严重遮挡、折角、边界模糊时 surface 边界不确定。",
        "mitigation": "needs_more_evidence + request_more_evidence_candidate；禁止强行写 document fact。",
    },
    {
        "risk_id": "layout_detector_conflict_resolution_deferred",
        "severity": "medium",
        "status": "deferred",
        "description": "layout detector hint 与 document surface 输出冲突时自动裁决策略未定义。",
        "mitigation": "validation_review；不自动按 confidence 覆盖；layout 不抢 ownership。",
    },
    {
        "risk_id": "real_image_benchmark_not_started",
        "severity": "medium",
        "status": "deferred",
        "description": "真实图像基准集与评测口径尚未建立。",
        "mitigation": "Implementation Planning 定义测试图集与基准口径。",
    },
    {
        "risk_id": "OCR_per_surface_not_started",
        "severity": "low",
        "status": "deferred",
        "description": "per-surface text detection 链路尚未启动。",
        "mitigation": "DryRun 已冻结 next_slot=text_detection_per_surface；禁止 global OCR。",
    },
    {
        "risk_id": "field_centric_role_dryrun_pending",
        "severity": "low",
        "status": "parallel_track",
        "description": "L1 Field-Centric Object Role DryRun 尚未执行，语义主线与视觉 runtime 接缝需后续对齐。",
        "mitigation": "标记为 parallel_next_track；不阻塞 Implementation Planning。",
    },
]


def build_risk_registry() -> Dict[str, Any]:
    unresolved = [r for r in RISK_REGISTRY if r.get("status") in ("deferred", "monitored", "parallel_track")]
    return {
        "registry_id": "document_surface_detector_risk_registry_v1",
        "risk_count": len(RISK_REGISTRY),
        "unresolved_risk_count": len(unresolved),
        "risks": RISK_REGISTRY,
        "unresolved_risks": [r["risk_id"] for r in unresolved],
        "candidate_only": True,
        "not_fact": True,
    }
