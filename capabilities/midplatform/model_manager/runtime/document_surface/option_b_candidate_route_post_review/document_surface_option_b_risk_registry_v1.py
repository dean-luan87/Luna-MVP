# -*- coding: utf-8 -*-
"""Document Surface — Option B post-review risk registry v1."""

from __future__ import annotations

from typing import Any, Dict, List

CONFIRMED: List[Dict[str, Any]] = [
    {"risk_id": "option_b_execution_blocked", "status": "confirmed", "description": "execution_allowed=false 全 case 阻断"},
    {"risk_id": "option_b_download_blocked", "status": "confirmed", "description": "model_download_allowed=false"},
    {"risk_id": "option_b_active_registry_blocked", "status": "confirmed", "description": "active_registry_update_allowed=false"},
    {"risk_id": "option_b_output_contract_limited_to_candidates", "status": "confirmed", "description": "输出契约限定 candidate 类型"},
    {"risk_id": "a_b_conflict_requires_validation_review", "status": "confirmed", "description": "A/B 冲突进入 validation_review"},
    {"risk_id": "no_silent_fallback_confirmed", "status": "confirmed", "description": "无 silent fallback / confidence override"},
]

PERSISTENT: List[Dict[str, Any]] = [
    {"risk_id": "option_b_specific_model_not_selected", "status": "watch", "blocker": False},
    {"risk_id": "option_b_dependency_not_admitted", "status": "watch", "blocker": False},
    {"risk_id": "option_b_segmentation_quality_unknown", "status": "watch", "blocker": False},
    {"risk_id": "option_b_surface_mask_contract_not_executed", "status": "watch", "blocker": False},
    {"risk_id": "field_attention_gate_required_for_texture_fp", "status": "watch", "blocker": False},
    {"risk_id": "screen_fixture_semantic_mismatch_pending", "status": "watch", "blocker": False},
    {"risk_id": "option_a_limitations_remain", "status": "watch", "blocker": False},
    {"risk_id": "OCR_per_surface_not_started", "status": "deferred", "blocker": False},
    {"risk_id": "field_centric_role_dryrun_pending", "status": "parallel_track", "blocker": False},
]


def build_option_b_risk_registry() -> Dict[str, Any]:
    all_risks = CONFIRMED + PERSISTENT
    return {
        "registry_id": "document_surface_option_b_candidate_route_risk_registry_v1",
        "confirmed_governance": CONFIRMED,
        "persistent_risks": PERSISTENT,
        "unresolved_risks": [r["risk_id"] for r in PERSISTENT],
        "confirmed_count": len(CONFIRMED),
        "risk_count": len(all_risks),
        "blocker_count": 0,
        "candidate_only": True,
        "not_fact": True,
    }
