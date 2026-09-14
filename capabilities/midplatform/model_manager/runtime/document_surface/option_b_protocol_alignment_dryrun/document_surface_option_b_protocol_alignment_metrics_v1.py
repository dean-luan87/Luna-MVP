# -*- coding: utf-8 -*-
"""Document Surface — Option B protocol alignment dryrun metrics v1."""

from __future__ import annotations

from typing import Any, Dict


def compute_protocol_alignment_metrics(
    *,
    contract: Dict[str, Any],
    registry: Dict[str, Any],
    dependency: Dict[str, Any],
    output: Dict[str, Any],
    runtime: Dict[str, Any],
    change: Dict[str, Any],
    evidence: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "candidate_count": contract.get("candidate_count", 0),
        "preflight_candidate_mapping_count": contract.get("preflight_candidate_count", 0),
        "blocked_candidate_mapping_count": contract.get("blocked_admission_record_count", 0),
        "active_model_mapping_count": 0,
        "active_skill_mapping_count": 0,
        "active_registry_update_count": registry.get("active_registry_update_count", 0),
        "runtime_activation_count": runtime.get("runtime_activation_count", 0),
        "protocol_ref_completeness_rate": 1.0 if contract.get("all_mapped") else 0.0,
        "candidate_only_compliance_rate": 1.0,
        "fact_admission_block_rate": 1.0 if output.get("c2_fact_blocked") else 0.0,
        "output_contract_mapping_rate": 1.0 if output.get("all_forbidden_blocked") else 0.0,
        "permission_denial_mapping_rate": 1.0 if dependency.get("no_execution_escalation") else 0.0,
        "change_control_compliance_rate": 1.0 if change.get("freeze_boundary_respected") else 0.0,
        "evidence_chain_preservation_rate": evidence.get("evidence_chain_preservation_rate", 0.0),
        "candidate_only": True,
        "not_fact": True,
    }
