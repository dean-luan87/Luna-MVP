# -*- coding: utf-8 -*-
"""Document Surface — Option B registry alignment dryrun v1."""

from __future__ import annotations

from typing import Any, Dict, List

PREFLIGHT_IDS = frozenset({
    "family_a_classical_helper_ok_candidate",
    "family_c_document_specific_surface_model_ok_for_preflight",
})


def run_registry_alignment_dryrun(*, admission_results: List[Dict[str, Any]]) -> Dict[str, Any]:
    per: List[Dict[str, Any]] = []
    for r in admission_results:
        cid = r["model_candidate_id"]
        is_preflight = cid in PREFLIGHT_IDS
        per.append({
            "model_candidate_id": cid,
            "active_model_id": None,
            "active_skill_id": None,
            "registry_alignment_status": "candidate_only",
            "candidate_registry_allowed": is_preflight,
            "active_registry_allowed": False,
            "runtime_registry_updated": False,
        })
    return {
        "dryrun_id": "option_b_registry_alignment_dryrun_v1",
        "records": per,
        "active_model_id_generated": False,
        "active_skill_id_generated": False,
        "active_registry_update_count": 0,
        "candidate_registry_alignment_only": True,
        "all_active_registry_blocked": all(p.get("active_registry_allowed") is False for p in per),
        "candidate_only": True,
        "not_fact": True,
    }
