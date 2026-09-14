# -*- coding: utf-8 -*-
"""Document Surface — Option B protocol alignment risk registry v1."""

from __future__ import annotations

from typing import Any, Dict, List

MITIGATED: List[Dict[str, Any]] = [
    {"risk_id": "option_b_model_skill_protocol_alignment_confirmed", "status": "mitigated"},
    {"risk_id": "model_skill_contract_mapping_complete", "status": "mitigated"},
    {"risk_id": "active_model_mapping_blocked", "status": "mitigated"},
    {"risk_id": "active_skill_mapping_blocked", "status": "mitigated"},
    {"risk_id": "active_registry_update_blocked", "status": "mitigated"},
    {"risk_id": "permission_denial_mapping_confirmed", "status": "mitigated"},
    {"risk_id": "output_contract_protocol_mapping_confirmed", "status": "mitigated"},
    {"risk_id": "evidence_chain_preserved", "status": "mitigated"},
    {"risk_id": "no_protocol_new_branch_confirmed", "status": "mitigated"},
]

PERSISTENT: List[Dict[str, Any]] = [
    {"risk_id": "option_b_specific_real_model_not_selected", "status": "watch"},
    {"risk_id": "option_b_preflight_planning_not_started", "status": "watch"},
    {"risk_id": "option_b_preflight_not_executed", "status": "watch"},
    {"risk_id": "option_b_segmentation_quality_unknown", "status": "watch"},
    {"risk_id": "wrapper_contract_not_implemented", "status": "watch"},
    {"risk_id": "model_weight_admission_not_started", "status": "watch"},
    {"risk_id": "license_review_for_real_model_not_started", "status": "watch"},
    {"risk_id": "dependency_availability_for_real_model_unknown", "status": "watch"},
    {"risk_id": "controlled_execution_not_started", "status": "watch"},
    {"risk_id": "option_a_limitations_remain", "status": "watch"},
    {"risk_id": "OCR_per_surface_not_started", "status": "deferred"},
    {"risk_id": "field_centric_role_dryrun_pending", "status": "parallel_track"},
]


def build_protocol_alignment_risk_registry() -> Dict[str, Any]:
    return {
        "registry_id": "option_b_protocol_alignment_risk_registry_v1",
        "mitigated_risks": MITIGATED,
        "unresolved_risks": [r["risk_id"] for r in PERSISTENT],
        "persistent_risks": PERSISTENT,
        "mitigated_count": len(MITIGATED),
        "unresolved_count": len(PERSISTENT),
        "candidate_only": True,
        "not_fact": True,
    }
