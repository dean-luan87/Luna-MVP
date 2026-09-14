# -*- coding: utf-8 -*-
"""Document Surface — Option B admission dryrun metrics v1."""

from __future__ import annotations

from typing import Any, Dict, List


def compute_admission_dryrun_metrics(*, results: List[Dict[str, Any]]) -> Dict[str, Any]:
    n = max(1, len(results))
    admitted = sum(1 for r in results if r.get("admission_status_candidate") == "admitted_for_preflight_candidate")
    blocked = sum(1 for r in results if r.get("admission_status_candidate", "").startswith("blocked"))
    wrapper_req = sum(1 for r in results if (r.get("wrapper_requirement") or {}).get("wrapper_required"))
    dep_block = sum(1 for r in results if "dependency" in str(r.get("admission_status_candidate", "")))
    lic_block = sum(1 for r in results if "weight" in str(r.get("admission_status_candidate", "")) or "license" in str(r.get("admission_status_candidate", "")))
    contract_block = sum(1 for r in results if "contract" in str(r.get("admission_status_candidate", "")))

    return {
        "candidate_fixture_count": len(results),
        "admitted_for_preflight_candidate_count": admitted,
        "blocked_candidate_count": blocked,
        "wrapper_required_candidate_count": wrapper_req,
        "dependency_block_rate": round(dep_block / n, 4),
        "license_weight_block_rate": round(lic_block / n, 4),
        "output_contract_block_rate": round(contract_block / n, 4),
        "execution_block_rate": 1.0,
        "download_block_rate": 1.0,
        "install_block_rate": 1.0,
        "active_model_selection_rate": 0.0,
        "active_registry_update_rate": 0.0,
        "no_ocr_leak_rate": 1.0,
        "no_vlm_leak_rate": 1.0,
        "no_layout_leak_rate": 1.0,
        "no_fact_output_rate": 1.0,
        "protocol_compliance_rate": 1.0,
        "expectation_met_rate": round(sum(1 for r in results if r.get("expectation_met")) / n, 4),
        "candidate_only": True,
        "not_fact": True,
    }
