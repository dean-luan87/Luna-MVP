# -*- coding: utf-8 -*-
"""Document Surface — Option B runtime boundary protocol mapping dryrun v1."""

from __future__ import annotations

from typing import Any, Dict, List

PREFLIGHT_IDS = frozenset({
    "family_a_classical_helper_ok_candidate",
    "family_c_document_specific_surface_model_ok_for_preflight",
})


def run_runtime_boundary_protocol_mapping_dryrun(*, admission_results: List[Dict[str, Any]]) -> Dict[str, Any]:
    per: List[Dict[str, Any]] = []
    for r in admission_results:
        cid = r["model_candidate_id"]
        is_preflight = cid in PREFLIGHT_IDS
        per.append({
            "model_candidate_id": cid,
            "runtime_activation_allowed": False,
            "execution_allowed": False,
            "controlled_execution_allowed": False,
            "preflight_required": True,
            "controlled_execution_planning_required": True,
            "runtime_boundary_status": "closed",
            "preflight_planning_may_be_recommended": is_preflight,
            "execution_cannot_be_recommended": True,
        })
    return {
        "dryrun_id": "option_b_runtime_boundary_mapping_dryrun_v1",
        "runtime_boundary_contract": "Runtime Boundary Contract",
        "records": per,
        "runtime_activation_count": 0,
        "all_execution_blocked": all(p.get("execution_allowed") is False for p in per),
        "all_controlled_execution_blocked": all(p.get("controlled_execution_allowed") is False for p in per),
        "candidate_only": True,
        "not_fact": True,
    }
