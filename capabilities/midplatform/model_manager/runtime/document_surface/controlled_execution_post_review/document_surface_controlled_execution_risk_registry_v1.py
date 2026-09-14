# -*- coding: utf-8 -*-
"""Document Surface Controlled Execution — risk registry v1."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

RISK_REGISTRY: List[Dict[str, Any]] = [
    {"risk_id": "overlapping_documents_under_separated", "severity": "medium", "status": "watch", "blocker": False,
     "description": "Case B 叠放票据仅输出 1 surface，未分离 paper_A/paper_B"},
    {"risk_id": "relation_hint_missing_for_overlap_case", "severity": "medium", "status": "watch", "blocker": False,
     "description": "Case B 无 overlaps/occludes relation_hint"},
    {"risk_id": "low_contrast_false_surface_risk", "severity": "medium", "status": "watch", "blocker": False,
     "description": "Case C 低对比场景产生多个 surface 候选，存在噪声风险"},
    {"risk_id": "candidate_count_noise_in_low_contrast_case", "severity": "medium", "status": "watch", "blocker": False,
     "description": "Case C 输出 9 个 surface candidates，候选数量偏高"},
    {"risk_id": "receipt_attachment_boundary_uncertain", "severity": "medium", "status": "watch", "blocker": False,
     "description": "Case D receipt/package 分离不稳定，low confidence 为主"},
    {"risk_id": "screen_vs_document_ambiguity_continues", "severity": "medium", "status": "watch", "blocker": False,
     "description": "Case E 屏幕文档仍 defer_to_screen_surface_detector，未作 fact 判定"},
    {"risk_id": "classical_cv_boundary_limitations_confirmed", "severity": "medium", "status": "monitored", "blocker": False,
     "description": "首次受控真实执行确认 Option A 在叠放/低对比场景存在局限"},
    {"risk_id": "registry_item_count_case_count_mismatch_explained", "severity": "low", "status": "explained", "blocker": False,
     "description": "registry_item_count=7（manifest 图片条目） vs dryrun_case_count=8（A–H 行为 case，含无图 Case F）"},
    {"risk_id": "real_runtime_not_activated", "severity": "low", "status": "by_design", "blocker": False,
     "description": "Controlled Execution 未激活 production runtime registry"},
    {"risk_id": "OCR_per_surface_not_started", "severity": "low", "status": "deferred", "blocker": False,
     "description": "per-surface OCR 链路未启动，符合当前边界"},
    {"risk_id": "field_centric_role_dryrun_pending", "severity": "low", "status": "parallel_track", "blocker": False,
     "description": "Field-Centric Object Role DryRun 待并行推进"},
    {"risk_id": "first_dryrun_blocked_by_missing_fixtures_historical", "severity": "info", "status": "resolved", "blocker": False,
     "description": "首次 DryRun 因 fixture 缺失 BLOCKED_BY_MISSING_FIXTURES；补齐后 GO，仅作历史记录"},
]


def build_controlled_execution_risk_registry(*, watch_ids: Optional[List[str]] = None) -> Dict[str, Any]:
    watch = watch_ids or []
    for risk in RISK_REGISTRY:
        if risk["risk_id"] in watch:
            risk = dict(risk)
            risk["status"] = "watch"
    unresolved = [r for r in RISK_REGISTRY if r.get("status") in ("watch", "monitored", "deferred", "parallel_track")]
    return {
        "registry_id": "document_surface_controlled_execution_risk_registry_v1",
        "risk_count": len(RISK_REGISTRY),
        "watch_count": sum(1 for r in RISK_REGISTRY if r.get("status") == "watch"),
        "blocker_count": sum(1 for r in RISK_REGISTRY if r.get("blocker")),
        "risks": RISK_REGISTRY,
        "unresolved_risks": [r["risk_id"] for r in unresolved],
        "review_watch_items": [
            "overlapping_documents_under_separated",
            "relation_hint_missing_for_overlap_case",
            "registry_item_count_case_count_mismatch_explained",
        ],
        "candidate_only": True,
        "not_fact": True,
    }
