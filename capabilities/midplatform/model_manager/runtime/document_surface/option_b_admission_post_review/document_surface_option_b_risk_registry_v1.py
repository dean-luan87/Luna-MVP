# -*- coding: utf-8 -*-
"""Document Surface — Option B admission post-review risk registry v1."""

from __future__ import annotations

from typing import Any, Dict, List

MITIGATED: List[Dict[str, Any]] = [
    {"risk_id": "option_b_admission_gate_functional", "status": "mitigated", "description": "admission gate dryrun GO，expectation_met_rate=1"},
    {"risk_id": "uncontrolled_dependency_blocked", "status": "mitigated", "description": "A2 blocked_dependency_not_admitted_candidate"},
    {"risk_id": "missing_weight_blocked", "status": "mitigated", "description": "B1 blocked_model_weight_missing_candidate"},
    {"risk_id": "unknown_license_blocked", "status": "mitigated", "description": "B2 blocked_license_not_cleared_candidate"},
    {"risk_id": "caption_text_output_blocked_or_requires_wrapper", "status": "mitigated", "description": "B3 blocked_or_requires_wrapper_candidate"},
    {"risk_id": "document_type_fact_output_blocked", "status": "mitigated", "description": "C2 blocked_output_contract_violation_candidate"},
    {"risk_id": "missing_hardware_blocked", "status": "mitigated", "description": "D1 blocked_hardware_requirement_missing_candidate"},
    {"risk_id": "active_model_selection_blocked", "status": "mitigated", "description": "active_model_selection_rate=0"},
    {"risk_id": "active_registry_update_blocked", "status": "mitigated", "description": "active_registry_update_rate=0"},
]

PERSISTENT: List[Dict[str, Any]] = [
    {"risk_id": "option_b_specific_real_model_not_selected", "status": "watch", "blocker": False},
    {"risk_id": "option_b_preflight_not_started", "status": "watch", "blocker": False},
    {"risk_id": "option_b_segmentation_quality_unknown", "status": "watch", "blocker": False},
    {"risk_id": "wrapper_contract_not_implemented", "status": "watch", "blocker": False},
    {"risk_id": "model_weight_admission_not_started", "status": "watch", "blocker": False},
    {"risk_id": "license_review_for_real_model_not_started", "status": "watch", "blocker": False},
    {"risk_id": "dependency_availability_for_real_model_unknown", "status": "watch", "blocker": False},
    {"risk_id": "controlled_execution_not_started", "status": "watch", "blocker": False},
    {"risk_id": "option_a_limitations_remain", "status": "watch", "blocker": False},
    {"risk_id": "OCR_per_surface_not_started", "status": "deferred", "blocker": False},
    {"risk_id": "field_centric_role_dryrun_pending", "status": "parallel_track", "blocker": False},
]


def build_option_b_admission_risk_registry() -> Dict[str, Any]:
    return {
        "registry_id": "document_surface_option_b_admission_risk_registry_v1",
        "mitigated_risks": MITIGATED,
        "unresolved_risks": [r["risk_id"] for r in PERSISTENT],
        "persistent_risks": PERSISTENT,
        "mitigated_count": len(MITIGATED),
        "unresolved_count": len(PERSISTENT),
        "blocker_count": 0,
        "candidate_only": True,
        "not_fact": True,
    }
