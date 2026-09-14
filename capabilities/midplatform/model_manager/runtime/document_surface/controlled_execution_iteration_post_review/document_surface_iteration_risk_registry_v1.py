# -*- coding: utf-8 -*-
"""Document Surface Iteration — risk registry v1."""

from __future__ import annotations

from typing import Any, Dict, List

PERSISTENT_RISKS: List[Dict[str, Any]] = [
    {"risk_id": "overlapping_documents_under_separated", "severity": "medium", "status": "watch", "blocker": False,
     "description": "Case A clear_edges 仅 1 surface，未分离成功"},
    {"risk_id": "relation_hint_missing_for_overlap_case", "severity": "low", "status": "watch", "blocker": False,
     "description": "Case A 为 uncertain_relation 非 overlaps；叠放关系证据不足时保留 watch"},
    {"risk_id": "high_overlap_surface_missed", "severity": "medium", "status": "watch", "blocker": False,
     "description": "Case C 高遮挡 0 surface，outer boundary 未稳定检出"},
    {"risk_id": "classical_cv_boundary_limitations_confirmed", "severity": "high", "status": "monitored", "blocker": False,
     "description": "Option A Classical CV 在叠放/贴附场景能力边界明显（Case A/F）"},
    {"risk_id": "screen_vs_document_ambiguity_continues", "severity": "medium", "status": "watch", "blocker": False,
     "description": "Case H defer 通过但 fixture 语义偏差，屏幕/文档歧义未消除"},
    {"risk_id": "OCR_per_surface_not_started", "severity": "low", "status": "deferred", "blocker": False,
     "description": "per-surface OCR 未启动，符合 frozen boundary"},
    {"risk_id": "field_centric_role_dryrun_pending", "severity": "low", "status": "parallel_track", "blocker": False,
     "description": "Field-Centric Object Role DryRun 待并行推进"},
]

NEW_RISKS: List[Dict[str, Any]] = [
    {"risk_id": "possible_over_segmentation_in_low_overlap_case", "severity": "medium", "status": "watch", "blocker": False,
     "description": "Case B low_overlap 输出 3 surfaces，可能存在 over-cutting"},
    {"risk_id": "texture_false_positive_candidate_remains", "severity": "medium", "status": "watch", "blocker": False,
     "description": "Case E 纹理场景仍输出 1 surface candidate"},
    {"risk_id": "receipt_attached_clear_surface_missed", "severity": "medium", "status": "watch", "blocker": False,
     "description": "Case F clear attached 未稳定输出 receipt surface，仅 uncertain_attached_to"},
    {"risk_id": "document_on_screen_fixture_semantic_mismatch", "severity": "medium", "status": "watch", "blocker": False,
     "description": "Case H fixture 为物理叠放票据，非真实屏幕截图"},
]

MITIGATED_RISKS: List[Dict[str, Any]] = [
    {"risk_id": "fake_relation_risk_mitigated", "severity": "info", "status": "mitigated", "blocker": False,
     "description": "fake_relation_rate=0，迭代策略有效抑制假关系"},
    {"risk_id": "forced_multi_surface_risk_mitigated", "severity": "info", "status": "mitigated", "blocker": False,
     "description": "forced_multi_surface_rate=0，未强行拆双 surface"},
    {"risk_id": "relation_without_evidence_risk_mitigated", "severity": "info", "status": "mitigated", "blocker": False,
     "description": "relation_hint_evidence_compliance_rate=1.0"},
]


def build_iteration_risk_registry() -> Dict[str, Any]:
    all_risks = PERSISTENT_RISKS + NEW_RISKS + MITIGATED_RISKS
    unresolved = [r["risk_id"] for r in all_risks if r.get("status") in ("watch", "monitored", "deferred", "parallel_track")]
    mitigated = [r["risk_id"] for r in all_risks if r.get("status") == "mitigated"]
    return {
        "registry_id": "document_surface_iteration_risk_registry_v1",
        "persistent_risks": PERSISTENT_RISKS,
        "new_risks": NEW_RISKS,
        "mitigated_risks": MITIGATED_RISKS,
        "risk_count": len(all_risks),
        "unresolved_risks": unresolved,
        "mitigated_risk_ids": mitigated,
        "blocker_count": 0,
        "candidate_only": True,
        "not_fact": True,
    }
