# -*- coding: utf-8 -*-
"""Document Surface — Option B evidence chain mapping dryrun v1."""

from __future__ import annotations

from typing import Any, Dict, List


def run_evidence_chain_mapping_dryrun(
    *,
    admission_results: List[Dict[str, Any]],
    contract_mapping: Dict[str, Any],
) -> Dict[str, Any]:
    per: List[Dict[str, Any]] = []
    for r in admission_results:
        abort = r.get("abort_rollback") or {}
        per.append({
            "model_candidate_id": r["model_candidate_id"],
            "admission_evidence_ref": f"admission_dryrun:{r['model_candidate_id']}",
            "candidate_fixture_ref": f"fixture_registry:{r['model_candidate_id']}",
            "protocol_ref": "LUNA-PROTO-L1-MODEL-SKILL-ADMISSION-CONTRACT-V1",
            "risk_ref": f"admission_risk:{r.get('admission_status_candidate')}",
            "abort_rollback_ref": abort.get("rollback_action") or "none",
            "admission_not_execution_result": r.get("execution_allowed") is False,
            "active_status_preserved_false": r.get("active_status") is False,
            "trace_retained": abort.get("trace_retained", True),
        })
    preserved = all(
        p.get("admission_not_execution_result") is True
        and p.get("active_status_preserved_false") is True
        for p in per
    )
    return {
        "dryrun_id": "option_b_evidence_chain_mapping_dryrun_v1",
        "evidence_chain_contract": "LUNA-PROTO-L1-PROTOCOL-TRACEABILITY-GOVERNANCE-V1",
        "records": per,
        "admission_refs_preserved": len(per) == 8,
        "protocol_refs_preserved": contract_mapping.get("protocol_ref") is not None,
        "evidence_chain_preservation_rate": 1.0 if preserved and len(per) == 8 else 0.0,
        "candidate_only": True,
        "not_fact": True,
    }
