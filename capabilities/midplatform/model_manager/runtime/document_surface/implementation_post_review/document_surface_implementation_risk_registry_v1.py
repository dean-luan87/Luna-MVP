# -*- coding: utf-8 -*-
"""Document Surface Implementation — risk registry v1."""

from __future__ import annotations

from typing import Any, Dict, List

RISK_REGISTRY: List[Dict[str, Any]] = [
    {"risk_id": "real_cv_implementation_not_started", "severity": "medium", "status": "deferred", "description": "Classical CV 真实实现尚未启动"},
    {"risk_id": "cv2_dependency_not_admitted", "severity": "high", "status": "deferred", "description": "cv2/OpenCV 依赖尚未通过 Controlled Execution Planning 准入"},
    {"risk_id": "real_image_dataset_not_started", "severity": "medium", "status": "deferred", "description": "受控测试图像集尚未建立"},
    {"risk_id": "classical_cv_boundary_limitations", "severity": "medium", "status": "monitored", "description": "经典 CV 边界检测在复杂遮挡/低对比场景可能不足"},
    {"risk_id": "severe_occlusion_boundary_uncertainty", "severity": "high", "status": "monitored", "description": "严重遮挡边界不确定"},
    {"risk_id": "screen_vs_document_ambiguity", "severity": "high", "status": "monitored", "description": "屏幕内容与纸张文档混淆风险"},
    {"risk_id": "layout_conflict_resolution_deferred", "severity": "medium", "status": "deferred", "description": "layout 冲突自动裁决策略未定义"},
    {"risk_id": "OCR_per_surface_not_started", "severity": "low", "status": "deferred", "description": "per-surface OCR 链路未启动"},
    {"risk_id": "protocol_patch_formal_alignment_pending", "severity": "low", "status": "parallel_track", "description": "Protocol Patch 正式回写协议体系待 Region Intelligence Protocol Alignment Post-Review"},
    {"risk_id": "field_centric_role_dryrun_pending", "severity": "low", "status": "parallel_track", "description": "Field-Centric Object Role DryRun 待并行推进"},
]


def build_implementation_risk_registry() -> Dict[str, Any]:
    unresolved = [r for r in RISK_REGISTRY if r.get("status") in ("deferred", "monitored", "parallel_track")]
    return {
        "registry_id": "document_surface_implementation_risk_registry_v1",
        "risk_count": len(RISK_REGISTRY),
        "unresolved_risk_count": len(unresolved),
        "risks": RISK_REGISTRY,
        "unresolved_risks": [r["risk_id"] for r in unresolved],
        "candidate_only": True,
        "not_fact": True,
    }
