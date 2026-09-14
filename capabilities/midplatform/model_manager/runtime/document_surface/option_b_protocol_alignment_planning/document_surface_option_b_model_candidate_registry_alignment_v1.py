# -*- coding: utf-8 -*-
"""Document Surface — Option B model candidate registry protocol alignment v1."""

from __future__ import annotations

from typing import Any, Dict, List

REGISTRY_CONTRACT = "Model Manager Admission / Registry"

REGISTRY_FIELD_ALIGNMENT = [
    "model_candidate_id",
    "family_type",
    "capability",
    "output_types_allowed",
    "output_types_forbidden",
    "dependency_profile",
    "weight_profile",
    "license_status_candidate",
    "execution_mode_candidate",
    "local_runtime_possible",
    "external_runtime_possible",
    "admission_status_candidate",
    "active_status",
    "controlled_execution_required",
    "preflight_required",
    "validation_required",
    "candidate_only",
    "not_fact",
]


def build_model_candidate_registry_alignment(*, dryrun_registry: Dict[str, Any]) -> Dict[str, Any]:
    fixtures: List[Dict[str, Any]] = dryrun_registry.get("fixtures") or []
    per: List[Dict[str, Any]] = []
    for f in fixtures:
        per.append({
            "model_candidate_id": f.get("model_candidate_id"),
            "registry_contract_fields_present": all(k in f for k in REGISTRY_FIELD_ALIGNMENT if k != "admission_status_candidate"),
            "active_status": f.get("active_status"),
            "active_registry_update_allowed": False,
            "interpretation": "candidate_registry_entry_not_active_model",
        })
    admitted = [f["model_candidate_id"] for f in fixtures if f.get("model_candidate_id") in (
        "family_a_classical_helper_ok_candidate",
        "family_c_document_specific_surface_model_ok_for_preflight",
    )]
    return {
        "alignment_id": "option_b_model_candidate_registry_alignment_v1",
        "registry_contract": REGISTRY_CONTRACT,
        "field_alignment": REGISTRY_FIELD_ALIGNMENT,
        "fixture_count": len(fixtures),
        "per_candidate": per,
        "admitted_for_preflight_candidate_ids": admitted,
        "active_model_selected": False,
        "active_registry_update_allowed": False,
        "admitted_for_preflight_not_equal_model_admitted": True,
        "admitted_for_preflight_not_equal_skill_admitted": True,
        "admitted_for_preflight_not_equal_runtime_admitted": True,
        "candidate_only": True,
        "not_fact": True,
    }
